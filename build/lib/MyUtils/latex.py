# =============================================================================
# PACKAGES
# =============================================================================
import pandas as pd

# =============================================================================
# MAIN
# =============================================================================
# REGRESSION TABLES


def add_se_note(dfoutput, se_note):
    """
    Add a note to the regression output table

    Arguments:
        dfoutput {Summary} -- output from summary3 function
        se_note {str} -- Note on SE

    Returns:
        None
    """
    se_note_df = pd.DataFrame(
        dfoutput.tables[-1].shape[1] * [" "],
        index=dfoutput.tables[-1].columns,
        columns=[f"\t {se_note}"],
    ).T
    dfoutput.tables[-1] = dfoutput.tables[-1].append(se_note_df)
    return None


def quote(string):
    return '"' + string + '"'


def thead(*args):
    thead = f"\thead{{ "
    for arg in args:
        thead += f"{arg} \\\\"

    thead = thead[:-2]
    thead += f"}}"
    return thead
