import subprocess
from typing import Callable, List, Optional, Tuple
from rich import print


_TestFunc = Callable[[], Optional[bool | Tuple[bool, str]]]
_SetupFunc = Callable[[], Optional[bool | Tuple[bool, str]]]
_TeardownFunc = Callable[[], Optional[bool | Tuple[bool, str]]]

tests: List[Callable[[], bool]] = []
setups: List[Callable[[], bool]] = []
teardowns: List[Callable[[], bool]] = []


def test(name: Optional[str] = None):
    """
    Decorator generator to register a test function.

    Tests are either executed by calling the decorated
    function or by calling `run_tests`.

    ## Error behaviour

    The test is interpreted as failure if the decorated
    function does one of the following things:
    - Raises an exception.
    - Returns `False`.
    - Returns `(False, "some message")`.

    When a tuple of `(False, msg)` is returned from the
    test function, `msg` is displayed as error message.
    """
    def decorator(fn: _TestFunc):
        def f():
            return _run("Running test", fn, name)
        tests.append(f)
        return f

    return decorator


def setup(name: Optional[str] = None):
    """
    Decorator generator to register a setup function.

    Setups are either executed by calling the decorated
    function or by calling `run_setups`.

    The error behavior is the same with the `test`
    decorator.
    """
    def decorator(fn: _SetupFunc):
        def f():
            return _run("Running setup", fn, name)
        setups.append(f)
        return f

    return decorator


def teardown(name: Optional[str] = None):
    """
    Decorator generator to register a teardown function.

    Teardowns are either executed by calling the decorated
    function or by calling `run_setups`.

    The error behavior is the same with the `test`
    decorator.
    """
    def decorator(fn: _TeardownFunc):
        def f():
            return _run("Running teardown", fn, name)
        teardowns.append(f)
        return f

    return decorator


def run_tests() -> Tuple[int, int]:
    """
    Runs all previously registered `test` functions in the
    order of registration.

    Returns a tuple containing first the number of successful
    tests and secondly the number of failed tests.
    """
    return _run_funcs(tests)


def run_setups() -> Tuple[int, int]:
    """
    Runs all previously registered `setup` functions in the
    order of registration.

    If a `setup` function failed, the execution will be
    canceled.

    Returns a tuple containing first the number of successful
    setups and secondly the number of failed setups.
    """
    return _run_funcs(setups, fail_fast=True)


def run_teardowns() -> Tuple[int, int]:
    """
    Runs all previously registered `teardown` functions in the
    order of registration.

    Returns a tuple containing first the number of successful
    teardowns and secondly the number of failed teardowns.
    """
    return _run_funcs(teardowns)


def run_all() -> int:
    """
    First, all setup steps will be run with `run_setups`. If
    one of the setup steps fails, the execution is canceled.

    After that, all registered tests will be run with
    `run_tests`.

    After that, all teardown steps will be executed with
    `run_teardowns.`

    Finally, a short summary is printed.

    Returns the total number of failed steps.
    """
    (_, setups_failed) = run_setups()
    (tests_successful, tests_failed) = (0, 0)
    (_, teardowns_failed) = (0, 0)

    if setups_failed != 0:
        print("\n[red]Execution has been canceled because setup failed.[/]")
        return setups_failed

    try:
        _print_delim()
        (tests_successful, tests_failed) = run_tests()
    finally:
        _print_delim()
        (_, teardowns_failed) = run_teardowns()

    print()

    if tests_failed == 0:
        print(f"[green]All {tests_successful} tests were successful.[/]")
    else:
        print(f"[red]{tests_failed} tests failed and "
              f"{tests_successful} tests were successful.[/]")

    if teardowns_failed != 0:
        print(f"[red]{teardowns_failed} teardown steps failed.[/]")

    return tests_failed + teardowns_failed


# HELPERS

def _run(
    prefix: str,
    fn: _TestFunc,
    name: Optional[str] = None,
) -> bool:
    txt = f"{prefix} [cyan]{name or fn.__name__}[/]"
    print(
        "{txt:<{width}} ... ".format(txt=txt, width=60),
        end='')

    try:
        ret = fn()
        if type(ret) == bool and not ret:
            print("[bold red]failed[/]")
            print("[red]error: test returned false[/]")
            return False

        if type(ret) == tuple and not ret[0]:
            print("[bold red]failed[/]")
            print(f"[red]error: {ret[1]}[/]")
            return False

        print("[bold green]ok[/]")
        return True

    except subprocess.CalledProcessError as e:
        print("[bold red]failed[/]")
        print(f"[red]error: command error: [{e.returncode}] {e}[/]")
        return False

    except Exception as e:
        print("[bold red]failed[/]")
        print(f"[red]error: {e}[/]")
        return False


def _run_funcs(
        funcs: List[Callable[[], bool]],
        fail_fast: bool = False,
) -> Tuple[int, int]:
    successful = 0
    failed = 0

    for f in funcs:
        if f():
            successful += 1
        else:
            failed += 1
            if fail_fast:
                break

    return (successful, failed)


def _print_delim():
    print(f"[dim]{'-'*65}[/]")
