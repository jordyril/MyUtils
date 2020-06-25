# =============================================================================
# Packages
# =============================================================================
import logging
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
# =============================================================================
# support functions
# =============================================================================


# def debug(x, index=None):
#     """
#     Assisting function, showing the name of a variable and its value(s)
#     """
#     if index is not None:
#         print(x + '[' + str(index) + ']:', globals()[x][index])
#     else:
#         print(x + ':', globals()[x])
#     return None

def intersection(*d):
    sets = iter(map(set, d))
    result = next(sets)
    for s in sets:
        result = result.intersection(s)
    return result


def create_subfolder(foldername):
    if not os.path.exists(foldername):
        os.makedirs(foldername)


def create_outputfolder():
    create_subfolder("Output")


def create_logfolder():
    create_subfolder("Logs")


def create_my_folders():
    create_logfolder()
    create_outputfolder()


def create_logging(
    name,
    level=logging.INFO,
    formatting="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
    delete_previous=False,
):

    create_logfolder()
    # logging
    log_file = f"Logs/{name}.log"  # file name

    formatter = logging.Formatter(formatting)  # logging format

    logger = logging.getLogger(name)  # create logger
    logger.setLevel(level)

    writing_permission = "w" if delete_previous else "a"
    file_handler = logging.FileHandler(
        log_file, mode=writing_permission
    )  # 'w' clears logs form previous runs
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


def clean_company_name(name):
    name = " " + name + " "
    cleaned = (
        name.upper()
        .replace(".", " ")
        .replace(",", " ")
        .replace("'", " ")
        .replace("-", " ")
        .replace("&", " ")
        .replace("(THE)", " ")
        .replace(" INC ", " INCORPORATED ")
        .replace(" DEVS ", " DEVICES ")
        .replace(" PETROL ", " PETROLEUM ")
        .replace(" US ", " UNITEDSTATES ")
        .replace(" RES ", " RESOURCES ")
        .replace(" ELEC ", " ELECTRIC ")
        .replace(" ELE ", " ELECTRIC ")
        .replace(" PAC ", " PACIFIC ")
        .replace(" INTL ", " INTERNATIONAL ")
        .replace(" TECHS ", " TECHNOLOGIES ")
        .replace(" TECH ", " TECHNOLOGIES ")
        .replace(" TECHNOLOGY ", " TECHNOLOGIES ")
        .replace(" PROPS ", " PROPERTIES ")
        .replace(" PROP ", " PROPERTIES ")
        .replace(" PROPERTY ", " PROPERTIES ")
        .replace(" INDS ", " INDUSTRIES ")
        .replace(" SYS ", " SYSTEMS ")
        .replace(" UNVL ", " UNIVERSAL ")
        .replace(" SERVICS ", " SERVICES ")
        .replace(" SVS ", " SERVICES ")
        .replace(" BUS ", " BUSINESS ")
        .replace(" COS ", " COMPANIES ")
        .replace(" MAT ", " MATERIALS ")
        .replace(" MIDST ", " MIDSTREAM ")
        .replace(" INTERPUB ", " INTERPUBLIC ")
        .replace(" PUB ", " PUBLIC ")
        .replace(" SW ", " SOUTHWEST ")
        .replace(" NAT ", " NATIONAL ")
        .replace(" INVR ", " INVESTORS ")
        .replace(" INV ", " INVESTMENT ")
        .replace(" GEN ", " GENERAL ")
        .replace(" RUB ", " RUBBER ")
        .replace(" BREWIN ", " BREWING ")
        .replace(" TST ", " TRUST ")
        .replace(" TS ", " TRUST ")
        .replace(" EDUR ", " EDUCATORS ")
        .replace(" PWR ", " POWER ")
        .replace(" REAL ", " REALTY ")
        .replace(" UTD ", " UNITED ")
        .replace(" PRDS ", " PRODUCTS ")
        .replace(" PTNS ", " PARTNERS ")
        .replace(" PTN ", " PARTNERS ")
        .replace(" FED ", " FEDERAL ")
        .replace(" LTD ", " LIMITED ")
        .replace(" AMER ", " AMERICAN ")
        .replace(" AM ", " AMERICA ")
        .replace(" MNFG ", " MANUFACTURINGS ")
        .replace(" PIPE ", " PIPELINE ")
        .replace(" MANUFACTURING ", " MANUFACTURINGS ")
        .replace(" COMMNS ", " COMMUNITIES ")
        .replace(" COMMS ", " COMMUNICATIONS ")
        .replace(" FINL ", " FINANCIAL ")
        .replace(" FIN ", " FINANCIAL ")
        .replace(" GP ", " GROUP ")
        .replace(" GRP ", " GROUP ")
        .replace(" PACK ", " PACKAGING ")
        .replace(" STL ", " STEEL ")
        .replace(" NTRL ", " NATURAL ")
        .replace(" ALU ", " ALUMINIUM ")
        .replace(" ALUM ", " ALUMINIUM ")
        .replace(" SCIEN ", " SCIENTIFIC ")
        .replace(" BK ", " BANK ")
        .replace("NEW YORK", "NY")
        .replace(" CORP ", " CORPORATION ")
        .replace(" EN ", " ENERGY ")
        .replace(" HDG ", " HOLDING ")
        .replace(" HLTH ", " HEALTH ")
        .replace(" PLC ", " ")
        .replace(" CPRT ", " ")
        .replace(" CRP ", " ")
        .replace(" THE ", " ")
        .replace(" OF ", " ")
        .replace(" COM ", " ")
        .replace(" CO ", " ")
        .replace(" AND ", " ")
        .replace(" NV ", " ")
        .replace(" N V ", " ")
        .replace(" COR ", " ")
        .replace(" LLC ", " ")
        .replace(" IN ", " ")
        .replace(" LP ", " ")
        .replace(" L P ", " ")
        .replace(" COMPANY ", " ")
        .replace(" COMPANIES ", " ")
        .replace(" INCORPORATED ", " ")
        .replace(" INTERNATIONAL ", " ")
        .replace(" CORPORATION ", " ")
        .replace(" PUBLIC ", " ")
        .replace(" GROUP ", " ")
        .replace(" LIMITED ", " ")
        .replace(" INCOME ", " ")
        .replace(" HOLDING ", " ")
        .replace(" HOLDINGS ", " ")
        .replace("!", " ")
        .replace(" ", "")
    )
    return cleaned


def remove_duplicates_in_list(l):
    return list(dict.fromkeys(l))


def get_duplicate_columnnames(df):
    old_list = df.columns.to_list()
    new_list = remove_duplicates_in_list(old_list)
    if len(old_list) == len(new_list):
        return []
    else:
        doubles = []
        for i in new_list:
            occurrence = old_list.count(i)
            if occurrence != 1:
                doubles.append(i)
    return doubles


def get_duplicate_columns(df):
    duplicates = get_duplicate_columnnames(df)  # identify duplicates

    problem = []  # list for duplicate columnnames, but not values

    # Check if values are also the same
    for col in duplicates:
        subdf = df[col]
        n = subdf.shape[1]
        temp_df = pd.DataFrame(
            index=subdf.index,
            columns=[f'{i}' for i in range(n)]
        )
        for i in range(n):
            temp_df[i] = subdf.iloc[:, i]

        temp_list = [(temp_df[0].fillna(0.) == temp_df[i].fillna(0.)).all()
                     for i in range(1, n)]
        if False in temp_list:
            problem.append(col)

    return duplicates, problem


def drop_duplicate_columns(df, ignore_error=False):
    duplicates, problems = get_duplicate_columns(df)

    if len(problems) > 0:
        if not ignore_error:
            raise ValueError(
                f'Some columns have the same name, but different values'
            )
        else:
            print(f'Some columns have the same name, but different values')
            return df.loc[:, ~df.columns.duplicated()]

    if len(duplicates) == 0:
        return df

    # split main and duplicates
    duplicates_df = df[duplicates]
    # drop duplicate column (based on names, but checked above that values are equal too)
    duplicates_df = duplicates_df.loc[:, ~duplicates_df.columns.duplicated()]

    # Drop ALL duplicates form main
    final = df.loc[:, ~df.columns.isin(duplicates)]

    # Add the single columns again (were before duplicated)
    final = pd.concat([final, duplicates_df], axis=1)

    return final


def plot_rolling_regression_results(betas, stdv, dates, multiplier=2):
    upper = betas + multiplier * stdv
    lower = betas - multiplier * stdv
    nbr_estimates = len(betas)

    fig, ax = plt.subplots()
    ax.plot(dates[-nbr_estimates:], betas, label=r"$\hat{\beta}$")
    ax.fill_between(
        dates[-nbr_estimates:],
        lower,
        upper,
        color="red",
        alpha=0.2,
        label=f"{multiplier} x STDV",
    )

    ax.plot(dates[-nbr_estimates:], np.zeros(nbr_estimates), ls="-", c="black")
    plt.xlabel("Time")
