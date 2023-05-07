# akane

A very simple, strongly typed library to easily create test cases for anything.

> **Info**  
> This project is mostly purpose built to create e2e integration tests for my CLI apps
> (like [goup](https://github.com/zekroTJA/goup), for example). I wanted something lean
> which takes almost no effort to write tests with. Feel free to use it for your own 
> projects, but don't expect a great developer experience.  
>
> If you are looking for proper testing libraries, feel free to take a look into the
> following resources.  
> - [unittest](https://docs.python.org/3/library/unittest.html)
> - [Robot Framework](https://robotframework.org/)
> - [pytest](https://github.com/pytest-dev/pytest)

## Installation

```
pip install akane
```

or

```
pip install git+https://github.com/zekrotja/akane.git
```

## Example

> This example is also availble in the [examples](examples/simple/main.py) directory.
```py
import os
import akane
from akane.assertions import assert_eq
from akane.procedures import setup, test, teardown


@setup()
def init_env_vars():
    os.environ["FOO"] = "bar"


@test(name="environment variables")
def test_env():
    assert_eq("bar", os.environ["FOO"])


@test(name="environment in shell")
def test_cmd():
    res = akane.exec(("sh", "-c", "echo $FOO"))
    assert_eq("bar\n", res)


@test(name="failing test")
def fails():
    return (False, "whoops")


@teardown(name="environment variables")
def delete_env_vars():
    del os.environ["FOO"]


def main() -> int:
    return akane.run_all()


if __name__ == "__main__":
    exit(main())
```