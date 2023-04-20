import warnings

from tqdm import tqdm

# from statsmodels.tsa.stattools import grangercausalitytests
from statsmodels.tools.tools import add_constant
from scipy import stats
from statsmodels.tools.validation import int_like
from statsmodels.regression.linear_model import OLS
from statsmodels.tools.sm_exceptions import InfeasibleTestError


import pandas as pd

idx = pd.IndexSlice

import numpy as np

# ################################################################################
# WRITE OWN Granger Causality TEST, able to handle missing values...
# ################################################################################


class MyGCResults(object):
    """
    Results wrapper for "my_grangercausality". For ease of use.
    """

    def __init__(self, org_data, cleaned_data, W, maxlag, dfd, ylags, xlags):
        self.df = org_data

        self.dta = cleaned_data
        self.W = W
        self.maxlag = self.dfn = maxlag
        self.dfd = dfd
        self.p_value = stats.f.sf(W, maxlag, dfd)

        self._ylags = ylags
        self._xlags = xlags

        self.K = maxlag
        self.T = cleaned_data.shape[0]

    def __repr__(self) -> str:
        return f"{self.W, self.p_value, self.dfd, self.dfn}"


def my_grangercausality(df, maxlag, addconst=True):
    """
    Basically copy pasted original source code from "statsmodels.tsa.stattools.grangercausalitytests" and adapted it to my use case and made adjustments to handle e.g. missing values, ...
    Dropped redundant tests from original (I just don't need them for now, but can be easily implemented)
    I chose to keep using pandas as it allows for keeping the (time) index, which is relevant for the shift to be (time) correct original basically assumes no missing values and does a simple "naive" shift/lagging.
    The use of pandas is probably slowing it down immensely and is not optimal at all, but it has to do (for now)
    """
    # check entries
    if isinstance(maxlag, (int, np.int32)):
        if maxlag <= 0:
            raise ValueError("maxlag must a positive integer")
        lags = np.arange(1, maxlag + 1)
    elif isinstance(maxlag, list):
        if len(maxlag) > 1:
            NotImplementedError("Only one lag at a time can be tested for now")
        lags = np.arange(1, maxlag[0] + 1)
        lags = lags[-1:]
    else:
        raise NotImplementedError("maxlag must be a positive integer or list")

    # create lags of both time series
    dta = df.copy()
    dta.columns = ["y", "x"]
    shifted_list = []
    for lag in lags:
        # pass
        _temp_shifted = dta.shift(lag)
        _temp_shifted.columns = [f"{col}_t-{lag}" for col in _temp_shifted.columns]
        shifted_list.append(_temp_shifted)
    dta = pd.concat([dta] + shifted_list, axis=1)

    # add constant
    const_list = []
    if addconst:
        dta = add_constant(dta, prepend=False)
        const_list.append("const")

    # Construct 2 exog samples for the "own" and "full" reg
    ylags = [f"y_t-{lag}" for lag in lags]
    xlags = [f"x_t-{lag}" for lag in lags]

    own_exog = ylags + const_list
    full_exog = ylags + xlags + const_list

    # drop missing obs, respecting same observations (so dropna on full dta) #Warning
    dta_noex = dta[["y"] + full_exog].dropna()

    if dta_noex.shape[0] <= len(full_exog):
        raise ValueError(
            f"The shape of the Resulting data ({dta_noex.shape[0]}) is too small to perform the necessary regressions (#exog variables = {len(full_exog)})"
        )
    # run OLS
    resown = OLS(dta_noex["y"], dta_noex[own_exog]).fit()
    resfull = OLS(dta_noex["y"], dta_noex[full_exog]).fit()
    # resfull.summary()

    # Granger Causality test using ssr (F statistic) - seems to be the one "xtgcause" uses
    if resfull.model.k_constant:
        tss = resfull.centered_tss
    else:
        tss = resfull.uncentered_tss
    if (
        tss == 0
        or resfull.ssr == 0
        or np.isnan(resfull.rsquared)
        or (resfull.ssr / tss) < np.finfo(float).eps
        or resfull.params.shape[0] != dta_noex[full_exog].shape[1]
    ):
        raise InfeasibleTestError(
            "The Granger causality test statistic cannot be computed "
            "because the VAR has a perfect fit of the data."
        )

    # Wald test statistic
    W = (resown.ssr - resfull.ssr) / resfull.ssr / maxlag * resfull.df_resid
    # p_value = stats.f.sf(W, maxlag, resfull.df_resid)

    # write necessary info to own results class
    results = MyGCResults(df, dta_noex, W, maxlag, resfull.df_resid, ylags, xlags)
    return results


class PanelGC(object):
    def __init__(
        self,
        data,
        maxlag,
        freq=None,
        x=None,
        y=None,
        initiate_individual_results=False,
        unused_entity_warning=True,
        single_lag=False,
    ):
        # INDEX RELATED
        # perform initial data check
        self._check_set_data(data, x, y, freq)
        self._check_K(maxlag)
        self.single_lag = single_lag
        self.minimum_flag = True
        self.W_i = np.zeros(self.N) * np.nan
        self.T_i = np.zeros(self.N) * np.nan
        self._unused_warning = unused_entity_warning
        self.gc_i = {}
        self._individual_results = False
        if initiate_individual_results:
            self._perform_individual_gc()

    def _check_set_data(self, data, x, y, freq):
        _index = data.index

        if (not isinstance(_index, pd.MultiIndex)) | (len(_index.names) != 2):
            raise ValueError("Data must have a MultiIndex of size 2 (Entity-time)")

        # check which one is time
        _index_types = [
            isinstance(_index.levels[x], pd.DatetimeIndex) for x in range(2)
        ]
        if np.array(_index_types).sum() != 1:
            raise ValueError("At least/Only 1 level has to be a pd.DateTimeIndex")

        # change order if necessary
        if _index_types[0]:
            data = data.swaplevel()

        data.index = data.index.remove_unused_levels()
        data = data.sort_index()
        _index = data.index

        self._entities, self._times = _index.levels
        self._entities = self._entities.sort_values()
        self._times = self._times.sort_values()

        self.N = len(self._entities)
        self.T = len(self._times)

        # EXOG-ENDOG related
        # check endog and exog (x, y)
        if not np.array([col is None for col in [x, y]]).sum() in [0, 2]:
            raise ValueError(
                "either both 'x' and 'y' have to be set or it is assumed that the first (second) column is the 'y' ('x') column"
            )

        self.freq = freq
        # self.freq = data.index.levels[1].freq
        # if freq:
        #     assert (
        #         freq == self.freq
        #     ), "The given frequency does not align with the inferred frequency from the DateIndex"

        y = data.columns[0] if not y else y
        x = data.columns[1] if not x else x
        # make sure first column is the 'y' column
        data = data[[y, x]]

        # uniformize the names of columns
        data.columns = ["y", "x"]

        self.dta = data

    def _check_K(self, maxlag):
        if isinstance(maxlag, (int, np.int32)):
            self.K_i = np.ones(self.N) * maxlag
            self.K_i = self.K_i.astype(int)
        else:
            raise NotImplementedError("For now only allow integer (same K for all)")
            # self.K_i = K

        assert (
            len(self.K_i) == self.N
        ), "Provided K does not have desired length, should equal number of entities"

        if not np.all(self.K_i >= 1):
            raise ValueError("maxlag must be a (list of) positive integer(s)")

        self.lag_order = maxlag

    def _perform_individual_gc(self):
        for i, ent in tqdm(
            enumerate(self._entities), desc="Individual GC", leave=False, total=self.N
        ):
            _temp = self.dta.loc[idx[ent, :], :]

            _temp.index = [x[1] for x in _temp.index]
            _temp = _temp.resample(
                self.freq
            ).last()  # WARNINGS - make sure all times are there between start,end

            try:
                if self.single_lag:
                    _max_lag = [self.K_i[i]]
                else:
                    _max_lag = self.K_i[i]
                gc = my_grangercausality(_temp, maxlag=_max_lag)
                self.gc_i[ent] = gc
                self.W_i[i] = gc.W
                self.T_i[i] = gc.T

            except ValueError:
                # print(ent)
                self.gc_i[ent] = "Infeasible"
                self.W_i[i] = np.nan
                self.T_i[i] = np.nan  # will cause the mask to cancel this obs out

        self._individual_results = True

    def _verify_minimum_condition(self):
        self.mask = self.T_i > 5 + 2 * self.K_i
        if False in self.mask:
            self.minimum_flag = False
            if self._unused_warning:
                warnings.warn(
                    f"Some entities do not fulfill the minimum requirements: {', '.join([str(x) for x in self._entities[~self.mask]])}. Results are provided leaving these ones out of further computations",
                    RuntimeWarning,
                )
        self.N_masked = int(self.mask.sum())
        self.T_i = np.where(self.mask, self.T_i, np.nan)

    def _verify_initialization(self):
        if not self._individual_results:
            self._perform_individual_gc()

    def _check_individual_results(self):
        self._verify_initialization()
        self._verify_minimum_condition()

    @property
    def E_W_i_tilde(self):
        self._check_individual_results()
        E_W_tilde_i = (
            self.K_i * (self.T_i - 2 * self.K_i - 1) / (self.T_i - 2 * self.K_i - 3)
        )
        # return E_W_tilde_i[self.mask]
        return np.where(self.mask, E_W_tilde_i, np.nan)

    @property
    def Var_W_i_tilde(self):
        self._check_individual_results()
        Var_W_tilde_i = (
            2
            * self.K_i
            * (self.T_i - 2 * self.K_i - 1) ** 2
            * (self.T_i - self.K_i - 3)
            / ((self.T_i - 2 * self.K_i - 3) ** 2 * (self.T_i - 2 * self.K_i - 5))
        )
        # return Var_W_tilde_i[self.mask]
        return np.where(self.mask, Var_W_tilde_i, np.nan)

    @property
    def W_bar(self):
        self._check_individual_results()
        # return self.W_i[self.mask].mean()
        return np.nanmean(np.where(self.mask, self.W_i, np.nan))

    @property
    def Z_bar_tilde(self):
        Z_bar_tilde = (
            np.sqrt(self.N_masked)
            * (self.W_bar - np.nanmean(self.E_W_i_tilde))
            / np.sqrt(np.nanmean(self.Var_W_i_tilde))
        )
        return Z_bar_tilde

    @property
    def _p_value(self):
        return stats.norm.sf(self.Z_bar_tilde)

    @property
    def E_W_i(self):
        "asymptotic one (T->inf, N->inf)"
        return self.lag_order

    @property
    def Var_W_i(self):
        "asymptotic one (T->inf, N->inf)"
        return 2 * self.lag_order

    @property
    def Z_bar(self):
        "asymptotic one (T->inf, N->inf)"
        Z_bar = (
            np.sqrt(self.N_masked) * (self.W_bar - self.E_W_i) / np.sqrt(self.Var_W_i)
        )
        return Z_bar

    def DH_test(self, zbar=False):
        results_dic = {
            "W_bar": self.W_bar,
            "Z_bar_tilde": self.Z_bar_tilde,
            "p_value": self._p_value,
            "lag_order": self.lag_order,
            "N": self.N,
        }
        if zbar:
            results_dic["Z_bar"] = self.Z_bar
        if not self.minimum_flag:
            results_dic["N_masked"] = self.N_masked
            results_dic["Entities_unused"] = [x for x in self._entities[~self.mask]]
        return results_dic
