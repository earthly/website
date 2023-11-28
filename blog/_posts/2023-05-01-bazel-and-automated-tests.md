---
title: "Using Bazel to Improve Your Automated Test Suite"
categories:
  - Tutorials
toc: true
author: Ali Mannan Tirmizi
author2: Aniket Bhattacharyea
editor: Bala Priya C
sidebar:
  nav: "bazel"
internal-links:
 - Bazel
 - Automation
 - CI/CD
excerpt: |
    Learn how to improve your automated test suite using Bazel, an open source software tool. Bazel can speed up the testing process, save time and computing resources, and ensure reliable and scalable deployments.
last_modified_at: 2023-07-11
---
**This article teaches you Bazel test automation. If you use Bazel for build automation, Earthly enhances it with reproducible, efficient containerized builds. [Explore more](/).**

To ensure that your code works as expected even when you ship it to production, you need to integrate automated testing. Automated testing is critical for enterprise-grade software development and delivery. It saves you time and money by rapidly running tests and improves software quality by allowing engineers to run lengthy and time-consuming tests in the background.

If you're looking to improve your automated test suite, you may want to consider [Bazel](https://bazel.build/), an open source software tool used to automate software builds and test software for large projects with multi language dependencies.

In this tutorial, you'll learn how to use [Bazel](/blog/monorepo-with-bazel) to improve your automated test suite. You'll create a Python project and write tests using `pytest` while using Bazel to run the test suite.

## Why Bazel?

![why]({{site.images}}{{page.slug}}/why.png)\

When running automated tests to aid the continuous integration, continuous delivery (CI/CD) process, time is critical. The [CI/CD](/blog/ci-vs-cd) pipeline is integral in allowing organizations to iterate quickly and increase production, and large organizations, like Google, Tesla, and Etsy, all incorporate CI/CD practices in their businesses.

Bazel can help speed up the CI/CD process and build and test software quickly and reliably by utilizing several built-in features. One of Bazel's most notable features is caching. During testing, Bazel only rebuilds what's required instead of the entire project. Additionally, it caches all previously passed tests. For each test that's run, the unchanged parts are simply skipped. This helps avoid redundant testing, which saves you time and computing resources.
In addition, Bazel uses parallel execution, which allows efficient resource usage and increases throughput by running multiple jobs at the same time. Bazel is both scalable and reliable, making your deployments smoother and faster.

Bazel also allows QA testers to specify a test time-out where tests are automatically aborted or failed when they reach a specified threshold value. This enables software engineers to abort code testing in a timely manner and ensure various nonfunctional requirements are met.

Bazel can work with and build code for a variety of different languages and platforms, including [C++](/blog/g++-makefile), Python, Android, and iOS. Bazel uses designated workspaces and a powerful [query language](https://bazel.build/query/language) capable of evaluating dependencies.

## How to Use Bazel to Improve Your Automated Test Suite

To follow along with the tutorial, you need to have [Bazel installed](https://bazel.build/install), and you'll need to have the [latest version of Python](https://www.python.org/downloads/). You can find the code examples used in this tutorial in [this GitHub repo](https://github.com/heraldofsolace/Bazel_testing).

### Creating a Project

To begin, you need to create a project in Python with automated unit tests using [`pytest`](https://docs.pytest.org/en/7.2.x/). You can use any language that Bazel supports.

You need to create a project directory and enable a virtual environment:

~~~{.bash caption=">_"}
mkdir bazel-tutorial
cd bazel-tutorial
python -m venv env
source env/bin/activate
~~~

Then install `pytest`:

~~~{.bash caption=">_"}
pip install pytest
~~~

Create a directory named `lib` and create an empty `__init__.py` file in it. Then create the file `prime.py` inside `lib` and place the following code in it:

~~~{.python caption="prime.py"}
# lib/prime.py

from math import sqrt

def is_prime(n):
    flag = True
    for i in range(2, int(sqrt(n)) + 1):
        if n % i == 0:
            flag = False
            break
    return flag
~~~

This file defines a function called `is_prime` that checks whether a given integer is prime.

Next, you need to create `lib/test_prime.py`:

~~~{.python caption="test_prime.py"}
# lib/test_prime.py

from lib.prime import is_prime

def test_primes():
    primes = [ 3, 5, 17, 31, 43]
    for p in primes:
        assert is_prime(p) == True
def test_non_primes():
    non_primes = [ 4, 10, 56, 48 ]
    for p in non_primes:
        assert is_prime(p) == False

if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__]))
~~~

Here, two unit tests are defined for the `is_prime` function. Now you can use `pytest` to run the unit tests and verify that they pass:

~~~{.bash caption=">_"}
$ pytest lib/test_prime.py
~~~

~~~{ caption="Output"}
==================== test session starts ==================
platform linux -- Python 3.10.8, pytest-7.2.1, pluggy-1.0.0
rootdir: /home/aniket/bazeltest
collected 2 items                           

lib/test_prime.py ..                                  [100%]

======================== 2 passed in 0.00s ================
~~~

Then create a script that uses the `prime` library and write tests for that. In the root directory, create `main.py` and write the following code:

~~~{.python caption="main.py"}
# main.py

from lib.prime import is_prime

def get_all_primes():
    primes = []
    for i in range(1, 100):
        if is_prime(i):
            primes.append(i)
    return primes

if __name__ == "__main__":
    primes = get_all_primes()
    for prime in primes:
        print(prime)
~~~

This code uses the `is_prime` library function to calculate all primes between 1 and 100. Next, create `test_main.py` in the root directory:

~~~{.python caption="test_main.py"}
# test_main.py

from main import get_all_primes

def test_main():
    expected_primes = [1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, \
    31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    actual_primes = get_all_primes()
    assert expected_primes == actual_primes
~~~

Now you can run `pytest` and verify that all the test cases pass:

~~~{.bash caption=">_"}
$ pytest
~~~

~~~{ caption="Output"}

======================= test session starts =====================
platform linux -- Python 3.10.8, pytest-7.2.1, pluggy-1.0.0
rootdir: /home/aniket/bazeltest
collected 3 items                                        

test_main.py .                                          [ 33%]
lib/test_prime.py ..                                    [100%]

========================== 3 passed in 0.01s =====================
~~~

### Configuring Bazel

To get started with Bazel in a project, you need to declare a workspace. To do so, create a file named `WORKSPACE` at the root of the project. Usually, an empty `WORKSPACE` file is enough for Bazel to recognize a workspace, but if you want to, you can have project-specific configurations in this file.

For this particular project, you need to load the [Python rules](https://bazel.build/reference/be/python) by placing the following code in the `WORKSPACE` file:

~~~{ caption="WORKSPACE"}
# WORKSPACE

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "rules_python",
    sha256 = "8c15896f6686beb5c631a4459a3aa8392daccaab805ea899c9d14215074b60ef",
    strip_prefix = "rules_python-0.17.3",
    url = "https://github.com/bazelbuild/rules_python/archive/refs/tags/0.17.3.tar.gz",
)

load("@rules_python//python:repositories.bzl", "py_repositories")

py_repositories()
~~~

To tell Bazel how to build, run, or test a particular code, you need to utilize `BUILD` files. A `BUILD` file must contain one or more rules that tell Bazel how to build the desired output, which can be an executable, a library, or a test.

Let's start by creating a `BUILD` file in the `lib` directory with the following code:

~~~{ caption="BUILD.bazel"}
# lib/BUILD

py_library(
    name = "lib_prime",
    srcs = ["prime.py"],
    visibility = ["//visibility:public"]
)

py_test(
    name = "test_prime",
    srcs = [ "test_prime.py" ],
    deps = [
        "//lib:lib_prime"
    ]
)
~~~

Here, two rules have been used:

1. The [`py_library`](https://bazel.build/reference/be/python#py_library) rule builds a Python library. The `name` argument is used to provide a name to the target. You can use this name to refer to this particular target from other `BUILD` files. The `srcs` argument lists the source files, which in this case is `prime.py`. The `visibility` argument is used to set the visibility of this target as `public` so that you can use it from the root level `BUILD` file when you write that later.
2. The [`py_test`](https://bazel.build/reference/be/python#py_test) rule builds a unit test from `test_primes.py`. Note that the `deps` array includes the `lib_prime` target mentioned previously. This will [make](/blog/makefiles-on-windows) sure the `lib_prime` target is built *before* the `test_prime` target is built. It also tells Bazel to rebuild `test_prime` if `lib_prime` is updated, which means that tests will be rerun if `prime.py` is modified.

You can run the tests using the `bazel test` command from the root of the project like this:

~~~{.bash caption=">_"}
bazel test //lib:test_prime
~~~

You should see the following output:

~~~{ caption="Output"}
Starting local Bazel server and connecting to it...
INFO: Analyzed target //lib:test_prime (22 packages loaded, \
271 targets configured).
INFO: Found 1 test target...
Target //lib:test_prime up-to-date:
  bazel-bin/lib/test_prime
INFO: Elapsed time: 1.760s, Critical Path: 0.25s
INFO: 2 processes: 2 linux-sandbox.
INFO: Build completed successfully, 2 total actions
//lib:test_prime                                  PASSED in 0.2s

Executed 1 out of 1 test: 1 test passes.
INFO: Build completed successfully, 2 total actions
~~~

As you can see, all the tests pass successfully.

![success]({{site.images}}{{page.slug}}/success.png)\

Let's see what happens if there is a failing test. Modify `test_prime.py` and add a new test case that fails:

~~~{.python caption="test_prime.py"}
# lib/test_prime.py

def test_failing():
    assert is_prime(57) == True
~~~

Rerun the `bazel tes //lib:test_primet` command. You should get the following output:

~~~{ caption="Output"}

INFO: Analyzed target //lib:test_prime (0 packages loaded, \
0 targets configured).
INFO: Found 1 test target...
FAIL: //lib:test_prime (see /home/aniket/.cache/bazel/_bazel_aniket/ec2610a69f8eaaebf15791a22f7f56d5/execroot/__main__/bazel-out/k8-fastbuild/testlogs/lib/test_prime/test.log)
Target //lib:test_prime up-to-date:
  bazel-bin/lib/test_prime
INFO: Elapsed time: 0.305s, Critical Path: 0.25s
INFO: 2 processes: 2 linux-sandbox.
INFO: Build completed, 1 test FAILED, 2 total actions
//lib:test_prime                                       FAILED in 0.2s
  /home/aniket/.cache/bazel/_bazel_aniket/ec2610a69f8eaaebf15791a22f7f56d5/execroot/__main__/bazel-out/k8-fastbuild/testlogs/lib/test_prime/test.log

INFO: Build completed, 1 test FAILED, 2 total actions
~~~

As you can see, it shows that the test fails. Bazel also creates a `bazel-testlogs` directory (among three other directories) where you can find more details about the tests that were run. The log will be stored in `bazel-testlogs/<target-name>/test.log`. In this case, it's `bazel-testlogs/lib/test_prime/test.log`:

~~~{.bash caption=">_"}
$ cat bazel-testlogs/lib/test_prime/test.log
~~~

~~~{ caption="Output"}
exec ${PAGER:-/usr/bin/less} '$0' || exit 1
Executing tests from //lib:test_prime
---------------------------------------------------
================== test session starts =============
platform linux -- Python 3.10.8, pytest-7.2.1, pluggy-1.0.0
rootdir: /home/aniket/.cache/bazel/_bazel_aniket/ec2610a69f8eaaebf15791a22f7f56d5/sandbox/linux-sandbox/3/execroot/__main__/bazel-out/k8-fastbuild/bin/lib/test_prime.runfiles/__main__
collected 3 items

lib/test_prime.py ..F                        [100%]

================== FAILURES ======================
___________________ test_failing _________________

    def test_failing():
>       assert is_prime(57) == True
E       assert False == True
E        +  where False = is_prime(57)

lib/test_prime.py:13: AssertionError
================== short test summary info ====================
FAILED lib/test_prime.py::test_failing - assert False == True
================== 1 failed, 2 passed in 0.02s =================
~~~

Remove the failing test and rerun the `bazel test` command so that all the tests pass again.

Let's now tell [Bazel](/blog/monorepo-with-bazel) to run tests for the main application. Again, in order to tell Bazel what to build and how to build, you need a `BUILD` file. Create a `BUILD` file in the root directory and place the following code in it:

~~~{ caption="BUILD.bazel"}
# BUILD

py_binary(
    name = "main",
    srcs = ["main.py"],
    deps = [
        "//lib:lib_prime"
    ],
)

py_test(
    name = "test_main",
    srcs = [ "test_main.py" ],
    deps = [
        ":main"
    ]
)
~~~

This `BUILD` file is similar to the `BUILD` file of the `lib` package. The only difference is that this time, `py_binary` is used instead of `py_library`. The `py_binary` rule creates an executable file in the `bazel-bin` directory when the target is built with the `bazel build` command.

You can now run all the tests with the following command:

~~~{.bash caption=">_"}
bazel test //...
~~~

You should see the following output:

~~~{ caption="Output"}
INFO: Analyzed 4 targets (0 packages loaded, 0 targets configured).
INFO: Found 2 targets and 2 test targets...
INFO: Elapsed time: 0.128s, Critical Path: 0.07s
INFO: 2 processes: 2 linux-sandbox.
INFO: Build completed successfully, 2 total actions
//lib:test_prime                       (cached) PASSED in 0.2s
//:test_main                           PASSED in 0.1s

Executed 1 out of 2 tests: 2 tests pass.
INFO: Build completed successfully, 2 total actions
~~~

Note that both test suites were run. In addition, note the output of `//lib:test_prime`. As you can see, it says "cached." This is because Bazel caches all passed tests, and since the `prime.py` file has not changed between the last two runs, there's no need to run the tests again, so Bazel loads the result from the cache. If you run the command again, you'll see both tests are now loaded from the cache:

~~~{ caption="Output"}
INFO: Analyzed 4 targets (0 packages loaded, 0 targets configured).
INFO: Found 2 targets and 2 test targets...
INFO: Elapsed time: 0.048s, Critical Path: 0.01s
INFO: 1 process: 1 internal.
INFO: Build completed successfully, 1 total action
//:test_main                           (cached) PASSED in 0.1s
//lib:test_prime                       (cached) PASSED in 0.2s

Executed 0 out of 2 tests: 2 tests pass.
INFO: Build completed successfully, 1 total action
~~~

In a big project with a large number of automated test cases, Bazel's caching can save a lot of time since you don't have to run tests unnecessarily. This improves the development and deployment speed of your project by cutting down the test time by a significant amount.

Bazel is also infinitely customizable because you can create custom rules that can change the testing method however you like. For example, if you want to use [nose2](https://github.com/nose-devs/nose2) instead of `pytest`, you can do so by writing a custom rule similar to `py_test`.

## Conclusion

In this article, you learned about Bazel, a fast and reliable tool that supports multiple languages and helps you with automated tests.

[Bazel](/blog/monorepo-with-bazel) is useful when you're working with different operating systems utilizing different languages, as you would only have to write the code once. Bazel enables users to create rules for rapid application testing and provides the ability to define custom rules, resulting in increased flexibility.

Another useful tool to speed up automated testing is [Earthly](https://earthly.dev/). Earthly is a simple framework that enables the creation of pipelines that can be developed locally and executed on any platform. It uses containers to run the pipelines, making them self-sufficient, repeatable, portable, and capable of running in parallel. It helps speed up builds since the cache is retained between builds.

{% include_html cta/bottom-cta.html %}