# =============================================================================
# Packages
# =============================================================================
# =============================================================================
# Printing support functions
# =============================================================================
# ------------------------------
# PYTHON PRINTING
# ------------------------------


def title(title):
    print("\n" + "=" * 80)
    title = "|" + title + "|"
    print("{0: ^80}".format(title))
    print("=" * 80)
    return None


def subtitle(subtitle):
    subtitle = "|" + subtitle + "|"
    n = len(subtitle)
    print("\n" + "-" * n)
    print(subtitle)
    print("-" * n)
    return None


# FORMATTING
def time_string(seconds):
    """Returns time in seconds as a string formatted HH:MM:SS."""
    s = int(round(seconds))  # round to nearest second
    h, s = divmod(s, 3600)  # get hours and remainder
    m, s = divmod(s, 60)  # split remainder into minutes and seconds
    return "%2i:%02i:%02i" % (h, m, s)


# ------------------------------
#  TXT PRINTING
# ------------------------------
def write_header(file, title):
    n = len(title)
    file.write(n * "#" + "\n")
    file.write(f"{title}\n")
    file.write(n * "#" + "\n\n")


def write_title(file, title):
    n = len(title)
    file.write(n * "=" + "\n")
    file.write(f"{title}\n")
    file.write(n * "=" + "\n\n")


def write_subtitle(file, title):
    n = len(title)
    file.write(n * "-" + "\n")
    file.write(f"{title}\n")
    file.write(n * "-" + "\n\n")


def write_subsubtitle(file, title):
    n = len(title)
    file.write(f"{title}\n")
    file.write(n * "-" + "\n")
