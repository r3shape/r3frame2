from .globals import os, datetime

# ------------------------------------------------------------ #
class R3logger:
    COLORS = {
        "INFO": "\033[92m",     # Green
        "ERROR": "\033[91m",    # Red
        "DEBUG": "\033[94m",    # Blue
        "WARNING": "\033[93m",  # Yellow
        "RESET": "\033[0m"      # Reset
    }

    DEBUG_MODE: bool = True

    @staticmethod
    def _log(message: str, level: str = "INFO", out: bool = False) -> None:
        if not R3logger.DEBUG_MODE: return
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fmt = f"[{time}] [{level}] {message}"
        msg = f"{R3logger.COLORS.get(level, '')}{fmt}{R3logger.COLORS['RESET']}\n"
        print(msg)

    @staticmethod
    def info(message, out: bool = False) -> None: R3logger._log(message, "INFO", out)

    @staticmethod
    def error(message, out: bool = False) -> None: R3logger._log(message, "ERROR", out)

    @staticmethod
    def debug(message, out: bool = False) -> None: R3logger._log(message, "DEBUG", out)

    @staticmethod
    def warning(message, out: bool = False) -> None: R3logger._log(message, "WARNING", out)
# ------------------------------------------------------------ #