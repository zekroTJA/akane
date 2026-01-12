import subprocess
from typing import Sequence


def exec_process(cmd: Sequence[str], unchecked=False, raw=False, **kwargs) -> subprocess.CompletedProcess:
    """
    Take a command and executes it using `subprocess.run` and returns the
    completed process with captured output.

    The status code will be checked and the function will raise an exception
    when the return code is non-zero. Pass `unchecked` as `True` to disable
    return code checking.
    """
    res = subprocess.run(cmd, capture_output=True, text=not raw, **kwargs)
    if not unchecked:
        res.check_returncode()
    return res


def exec(cmd: Sequence[str], raw=False, **kwargs) -> str:
    """
    Take a command and executes it using `subprocess.check_output`.

    STDERR is piped into STDOUT, so both outputs will be combined.
    """
    return subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=not raw, **kwargs)
