# Color codes,  **CREDIT** SNIPPET Author: Rene-D --  https://gist.github.com/rene-d -- 2018 
class Colors:
    """ ANSI color codes """
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"
    # cancel SGR codes if we don't write to a terminal
    if not __import__("sys").stdout.isatty():
        for _ in dir():
            if isinstance(_, str) and _[0] != "_":
                locals()[_] = ""
# ^*rene-d 2018 Github*^

USE_COLOR = True
THEME = {
    "title": Colors.BOLD + Colors.CYAN,
    "header": Colors.CYAN,
    "line": Colors.BLUE,
    "row_even": Colors.LIGHT_PURPLE,
    "row_odd": Colors.LIGHT_WHITE,
    "error": Colors.RED + Colors.BOLD,
    "success": Colors.GREEN,
    "warning": Colors.YELLOW + Colors.BOLD,
    "prompt": Colors.BLUE,
    "text": Colors.LIGHT_GRAY,
}


def colorize(text: str, role: str = "text") -> str:
    if not USE_COLOR:
        return text
    prefix = THEME.get(role, "")
    return f"{prefix}{text}{Colors.END}"
