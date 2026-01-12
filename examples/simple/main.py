import os

import akane
from akane.assertions import assert_eq
from akane.procedures import setup, teardown, test


@setup()
def init_env_vars():
    os.environ["FOO"] = "bar"


@test(name="environment variables")
def test_env():
    assert_eq("bar", os.environ["FOO"])


@test(name="environment in shell")
def test_cmd():
    res = akane.exec(("bash", "-c", "echo $FOO"))
    assert_eq("bar\n", res)


@test(name="stdin to cat")
def test_cmd_stdin():
    res = akane.exec("cat", input="foo bar baz")
    assert_eq("foo bar baz", res)


@test(name="capture stderr")
def test_cmd_stderr():
    res = akane.exec(("sh", "-c", "echo err >&2"))
    assert_eq("err\n", res)


@test(name="split stdout and stderr")
def test_cmd_split_output():
    res = akane.exec_process(("sh", "-c", "echo from stderr >&2; echo from stdout"))
    assert_eq("from stdout\n", res.stdout)
    assert_eq("from stderr\n", res.stderr)


@test(name="this is supposed to fail")
def fails():
    return (False, "whoops")


@teardown(name="environment variables")
def delete_env_vars():
    del os.environ["FOO"]


def main() -> int:
    return akane.run_all()


if __name__ == "__main__":
    exit(main())
