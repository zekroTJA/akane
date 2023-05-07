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
