import subprocess
from typing import Sequence


def exec(cmd: Sequence[str]) -> str:
    """
    Take a command and executes it using `subprocess.check_output`
    in a shell and returns the output as an UTF-8 encoded string.
    """
    res = subprocess.check_output(cmd, shell=True, stderr=subprocess.PIPE)
    return res.decode('utf-8')
