---
title: "Building and Deploying a Python App with Bazel"
categories:
  - Tutorials
toc: true
author: Artem Oppermann
sidebar:
  nav: "bazel"
internal-links:
 - Python
 - Bazel
 - Deploy
 - Dependencies
excerpt: |
    
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster. This article is about Bazel. If you are looking for a simpler approach to monorepo builds then [check us out](/).**

## What Is Bazel

![What]({{site.images}}{{page.slug}}/what.jpg)\

Bazel automates the build process and testing of software. In this respect, it can be compared to build tools like `make`, Ant, Maven, and Gradle.

Bazel grew out of the need for highly scalable builds. Developers who have worked on larger projects have probably experienced a problem between unit tests and a new feature. In this scenario, typically, several new files are added to a project in each sprint until the whole thing eventually becomes so large that the scaling of the builds, especially in larger projects, sometimes takes 15 minutes.

Incremental builds are vital for better build performance. In an incremental build, code changes in small increments, and therefore, it doesn't make sense to rebuild the entire application every time something changes.

Of course, there are parts of the codebase that are affected by the changes and need to be tested, which is where [Bazel](/blog/monorepo-with-bazel) comes into play. With Bazel, the application can be divided into different build units, and the scope of a build can be very granular. This means that only the code that has been changed needs to be rebuilt.

Since significantly less code has to be plowed through per build, builds in Bazel are faster than other tools like Make, and developers using Bazel are able to do quick builds and test runs—locally and in continuous integration (CI) test systems.

The tool itself is written in Java, but it can be used in conjunction with several programming languages, including Java, C++, Objective-C, D, Groovy, JavaScript, Python, Rust, and Scala. Regardless of the programming language or platform, with Bazel, developers can create and test the entire source code with a single command.

In this article you'll learn about Bazel, what it's used for, and what features make this build tool so special. You'll also learn how to develop and run a basic application using Python with Bazel.

## Implementing Bazel for Building Python Apps

![Implement]({{site.images}}{{page.slug}}/implement.png)\

In the following tutorial, a simple application in [Bazel](/blog/monorepo-with-bazel) will be implemented and deployed using Python and Flask, which is a lightweight micro web framework for programming web applications. A calculator application will be created that sums up two random numbers and shows the sum in the browser. Then a unit test will be implemented to test the functionality of the app.

Before beginning, the following are needed:

* [Visual Studio (VS) Code](https://code.visualstudio.com/)
* [Bazel 5.1.0](https://docs.bazel.build/versions/main/install.html)
* [Python 3.10.7](https://www.python.org/downloads/release/python-3107/)

### Creating the Folder Structure

The first step of creating the calculator app is to create the proper folder structure in VS Code.

In Bazel, the software is built from source code that is organized in a directory tree called a workspace. In the workspace, the source files need to be organized in a nested package hierarchy. Here, each package is a directory that contains a number of source files and one `BUILD` file that specifies what software will be built from the source files.

In this project, the folder `MY-PYTHON-APP` serves as the root directory for the workspace. In it, the package calculator, app, and third party are created. The package app will contain the source code of the calculator and the unit tests. In the app, the main code for the actual application will be stored. Additionally, a `third-party` folder will be created that will be responsible for any third-party dependencies:

<div class="wide">

![Folder structure]({{site.images}}{{page.slug}}/wnNRmbo.png)

</div>

### Creating the WORKSPACE File and Declaring the Bazel Version

The root directory `MY-PYTHON-APP` serves as the workspace and will contain all the source code needed to build the software.

To declare this directory as the workspace, a `WORKSPACE` file needs to be created. This file contains all the references to external dependencies that are needed to build the app.

To create the file, either use the terminal by executing the command `touch WORKSPACE.bazel` or do it manually by using the **New File** option when right-clicking on the `MY-PYTHON-APP` folder.

After this, the file `.bazelversion` needs to be created in the same directory. This file declares the version of Bazel being used for the app (5.1.0). The `.bazelversion` file is created analogous to the `WORKSPACE` file.

Following this, the `WORKSPACE` file has to be filled with references to external dependencies. In order to use Python, the [Python rules for Bazel](https://bazel.build/reference/be/python), which provide the basis of support for Python in Bazel, will be used. To import the Python rules, add some commands to the `WORKSPACE` file:

~~~{ caption="WORKSPACE.bazel"}
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
http_archive(
    name = "rules_python",
    sha256 = "8c8fe44ef0a9afc256d1e75ad5f448bb59b81aba149b8958f02f7b3a98f5d9b4",
    strip_prefix = "rules_python-0.13.0",
    url = "https://github.com/bazelbuild/rules_python/archive/refs/tags/0.13.0.tar.gz",
)
~~~

Next, utilize the third-party dependency Flask. This is a `pip` dependency that is added to the `WORKSPACE` by loading the function `pip_install`. Then call this function to install the required dependency:

~~~{ caption="WORKSPACE.bazel"}
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")
http_archive(
    name = "rules_python",
    sha256 = "8c8fe44ef0a9afc256d1e75ad5f448bb59b81aba149b8958f02f7b3a98f5d9b4",
    strip_prefix = "rules_python-0.13.0",
    url = "https://github.com/bazelbuild/rules_python/archive/refs/tags/0.13.0.tar.gz",
)
 
load("@rules_python//python:pip.bzl", "pip_install")
 
pip_install(
   name = "python_deps",
   requirements = "//third_party:requirements.txt",
)
~~~

The function `pip_install` installs all dependencies listed in the file `requirements.txt` that need to be created in the third-party directory. This file contains Flask as the only external dependency needed:

~~~{ caption="requirments.txt"}
Flask==2.0.2
~~~

### Implementing the Calculator

After defining Flask as an internal dependency, write the source code for the calculator. The file `calculator.py` in the directory `calculator` looks like this:

~~~{.python caption="calculator.py"}
class Calculator:
  def add(self, x, y): return x + y;
~~~

The class `Calculator` takes two variables, `x` and `y`, as arguments and returns the sum of these variables. This class will be the basis for the calculator app.

To build the software from the source, create the file `BUILD.bazel` in the same directory as the source code. The file defines and declares this directory as a Bazel package.
Because of this, Bazel knows exactly what source code has to be built during the build process. Here, build the calculator source code as a Python library:

~~~{ caption="WORKSPACE.bazel"}
py_library(
    name = "calculator",
    srcs = ["calculator.py"],
    visibility = ["//visibility:public"]
)
~~~

In this code, some attributes, including the `name`, `srcs`, and `visibility`, are provided. The `name` simply defines the name of the build library. The attribute `srcs` specifies the source code for the build process, and `visibility` allows the build library to be used outside this particular [Bazel](/blog/monorepo-with-bazel) package.

### Implementing a Unit Test

Let's write a unit test. The test class will be called `calculator_test.py` and will be in the same directory as the class `calculator.py`.
The source code for the unit test is depicted here:

~~~{.python caption="calculator_test.py"}
import unittest
from calculator import Calculator
 
class TestSum(unittest.TestCase):
 
  def test_sum(self):
    calculator = Calculator()
    self.assertEqual(calculator.add(1, 2), 3)
 
  if __name__ =="__main__":
    unittest.main()
~~~

In this code, the unit test simply checks whether the sum of 1 and 2 equals 3.

Then extend the previous `BUILD.bazel` file with a `py_test` rule that compiles the source code of the unit test:

~~~{ caption="WORKSPACE.bazel"}
py_library(
    name = "calculator",
    srcs = ["calculator.py"],
    visibility = ["//visibility:public"]
)
 
py_test(
    name = "calculator_test",
    srcs = ["calculator_test.py"],
    deps = [
        "//calculator:calculator"
    ],
)
~~~

The `py_test` requires the attributes `name`, `srcs`, and `deps`. The first two attributes are analogous to the previously defined `py_library`. The third attribute, `deps`, specifies the path to the library that is required by the unit test.

For the unit test, use the previously defined library named `calculator`.

## Running a Unit Test in Bazel

In this section, building the previously written source code and running the unit test are discussed. By executing the command `bazel test calculator/…`, the source code is built in the [Bazel](/blog/monorepo-with-bazel) package `calculator`, and then Bazel runs the unit test. The output should look like this:

<div class="wide">

![Terminal output of the unit test]({{site.images}}{{page.slug}}/FBeMeE9.png)

</div>

The output shows that Bazel successfully built the source code and that the unit test has passed.

## Creating a Flask App

Now a Flask app that uses the calculator to find the sum of two random numbers needs to be created. The sum will then be displayed in the browser.

### Creating the Source Code

To begin, create the source code:

~~~{.python caption="main.py"}
from calculator.calculator import Calculator
from flask import Flask
from random import randint
 
app = Flask(__name__)
calculator = Calculator()
 
@app.route('/')
def randomNumberCalculator():
  randomInt1 = randint(0, 250)
  randomInt2 = randint(0, 250)
  return "{} + {} = {}?".format(randomInt1, randomInt2, \
  calculator.add(randomInt1, randomInt2))
 
if __name__ == '__main__':
  app.run(host='0.0.0.0')
~~~

The code is saved in the file `main.py` in the previously created directory `app`.

### Modifying the BUILD File

Then create a `BUILD.bazel` file in order to declare this directory as a Bazel package:

~~~{ caption="WORKSPACE.bazel"}
py_binary(
  name = "main",
  srcs = ["main.py"],
  deps = ["//calculator:calculator",
          requirement("Flask")
  ]
)
~~~

Here, the Python rule `py_binary` is used since this will be a runnable application. Analogous to `py_library` and `py_test`, `py_binary` requires three arguments: `name`, `srcs`, and `deps`. `srcs` is the source code that is going to be built as a binary. In this case, it's the `main.py` file. The dependency `deps` is the calculator library.

In the code of the application, Flask is being used as an external dependency. Because of this, the `BUILD.bazel` file has to be further modified to ensure that the third-party dependency can be consumed by the package. The modification can be seen in the first line of the file:

~~~{ caption="WORKSPACE.bazel"}
load("@python_deps//:requirements.bzl", "requirement")
 
py_binary(
  name = "main",
  srcs = ["main.py"],
  deps = ["//calculator:calculator",
          requirement("Flask")
  ]
)
~~~

Previously, a pip dependency was added to the `WORKSPACE`, and `pip_install` was used to install Flask. Here, this external dependency was referenced as `python_deps`. By incorporating the first line in the `BAZEL.build` file, this external requirement is loaded into the package `app`. Then Flask is added as a dependency to the `py_binary` rule, and with that, the application is finished.

### Building and Running the Application

By running the command `bazel run //app:main`, the project is built, and the main application is run. The Flask app is now running in the browser, where the sum of two randomly generated numbers is shown:

<div class="wide">
![Browser output of the app]({{site.images}}{{page.slug}}/2Qj5wzg.png)
</div>

## Conclusion

In this article, the fundamentals of Bazel, specifically what Bazel is, what it's used for, and how to prepare the `WORKSPACE` and `BUILD` files, were explained. In the practical part of the article, a simple application was implemented in Python and Flask. Bazel was then used to build the source code, run a unit test, and run the main application in the browser.

Bazel isn't the only solution for the automation of building and testing software. [Earthly](https://earthly.dev/) provides a convenient framework to build images or stand-alone artifacts by leveraging containers for the execution of pipelines.

A Earthfile for testing our calculator app could look like this:

~~~{.dockerfile caption="Earthfile"}
VERSION 0.7
FROM python:3.10.7
WORKDIR /app

deps:
  RUN pip install -r ./third_party/requirements.txt
  COPY ./calculator/calculator.py .

unit_test:
  FROM +deps
  COPY ./calculator/calculator_test.py .
  RUN python -m unittest discover
~~~

[Earthly](https://earthly.dev/) combines the best ideas from Dockerfiles and Makefiles into one specification, making the containers self-contained, repeatable, portable, and parallel.

{% include_html cta/bottom-cta.html %}
