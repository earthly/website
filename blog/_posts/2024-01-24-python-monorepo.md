---
title: "Building a Monorepo with Python"
categories:
  - Tutorials
toc: true
author: Furqan Butt

internal-links:
 - building a monorepo
 - monorepo with python
 - build a monorepo
 - building a monorepo with python
 - using python to build a monorepo
excerpt: |
    This article explains the benefits of using a monorepo setup in software development and provides a tutorial on how to build a monorepo with Python using build tools like Pants and Earthly. It covers topics such as project structure, setting up build files, running tests, fixing linting and formatting issues, and containerizing the project.
---
**This article explains how to set up a monorepo in Python. Earthly efficiently orchestrates complex builds in monorepos. [Check it out](https://cloud.earthly.dev/login).**

Many software organizations opt to create and maintain repositories based on individual projects, applications, or teams. While this approach allows for full autonomy over each project, it often results in isolated projects that impede cross-team collaboration, particularly as the organization grows and adds more projects or services.

That's why many have begun to opt for a monorepo setup, where a single repository contains the entire codebase for the organization. Monorepos are beneficial for several reasons. They help increase collaboration across teams, ensure unified build pipelines, and help reduce duplication.

However, creating a monorepo can be complicated, specifically in Python. That's why, in this article, you'll learn more about monorepos in Python—including how to put one together using [Earthly](https://earthly.dev/), a build tool designed for managing monorepos.

## How to Build a Monorepo With Python

To help you better understand how to build a monorepo Python project, let's consider a real-world use case where you, the developer, are building a health and fitness application that lets its users calculate their body mass index (BMI) and their daily calorie intake.

All the code for this article is available in [this GitHub repository](https://github.com/furqanshahid85-python/python-monerepo/tree/main).

The monorepo setup for this application consists of multiple components, including services and packages that are developed by different teams as independent components but are still shared and managed within the same repository.

The application consists of two backend services and three shared packages, and the project structure is as follows:

~~~{ caption=""}
.
├── README.md
├── health_fitness_app
│   ├── __init__.py
│   ├── bmi_service
│   │   ├── __init__.py
│   │   ├── bmi_service.py
│   │   └── test_bmi_service.py
│   ├── calorie_intake_service
│   │   ├── __init__.py
│   │   ├── calorie_intake_service.py
│   │   └── test_calorie_intake_service.py
│   ├── main.py
│   └── packages
│       ├── bmi
│       │   ├── __init__.py
│       │   ├── bmi_calculator.py
│       │   └── test_bmi_calculator.py
│       ├── bmr
│       │   ├── __init__.py
│       │   ├── bmr_calculator.py
│       │   └── test_bmr_calculator.py
│       └── calorie
│           ├── __init__.py
│           ├── calorie_calculator.py
│           └── test_calorie_calculator.py
└── requirements.txt
~~~

The two services and three packages are part of a single repo. The `packages` directory is a shared space for all custom-implemented packages that can be shared between the two services (or any number of services that are added to the application in the future).

The first service, `bmi_service`, calculates the BMI of the user with weight and height inputs. It uses the methods defined in the `bmi` package in the shared `packages` directory.

The code for `bmi_service` looks like this:

~~~{.python caption="bmi_service.py"}
from health_fitness_app.packages.bmi.bmi_calculator import (
    calculate_bmi,
    get_bmi_category,
)


def cal_bmi(weight, height):
    """To get your bmi enter your weight(kg) and height(m)"""
    bmi = calculate_bmi(weight, height)
    bmi_category = get_bmi_category(bmi)
    return {"bmi_value": bmi, "bmi_category": bmi_category}
~~~

The second service, `calorie_intake_service`, calculates a user's daily calorie intake requirements using the following input provided by the user: `weight`, `height`, `age`, `sex`, and `activity_level`. This service also uses two shared packages, `bmr` and `calorie`, to calculate the basal metabolic rate (BMR) value and calorie intake for the user.

Here's the code for `calorie_intake_service`:

~~~{.python caption="calorie_intake_service.py"}
from health_fitness_app.packages.bmr.bmr_calculator import calculate_bmr
from health_fitness_app.packages.calorie.calorie_calculator import (
    calculate_calorie_intake,
)


def cal_calories(weight, height, age, sex, activity_level):
    """To get your bmr and daily calorie intake enter your: weight(lbs),
    height(in), age(years), sex(male/female), and
    activity_level(sedentary/lightly active/moderately active/very active)"""

    bmr = calculate_bmr(weight, height, age, sex)
    calories = calculate_calorie_intake(bmr, activity_level)

    return {"daily_calorie_intake": calories}
~~~

`bmi`, `bmr`, and `calorie` are custom packages residing in the `packages` directory. They contain `bmi_calculator.py`, `bmr_calculator.py`, and `calorie_calculator.py`, respectively.

The codebase for `bmi_calculator` looks like this:

~~~{.python caption="bmi_calculator.py"}
# package containing methods for BMI calculations


def calculate_bmi(weight, height):
    try:
        weight = float(weight)
        height = float(height)
        bmi = weight / (height**2)
        return int(bmi)
    except ValueError:
        return None


def get_bmi_category(bmi):
    if bmi is None:
        return "Invalid input"
    elif bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"
~~~

The codebase for `bmr_calculator` looks like this:

~~~{.python caption="bmr_calculator.py"}
# package containing methods for BMR calculations


def calculate_bmr(weight, height, age, sex):
    try:
        weight = float(weight)
        height = float(height)
        age = int(age)
        sex = str(sex)
        if sex == "male":
            bmr = 66 + (6.3 * weight) + (12.9 * height) - (6.8 * age)
        else:
            bmr = 655 + (4.3 * weight) + (4.7 * height) - (4.7 * age)
        return int(bmr)
    except ValueError:
        return None
~~~

The following is the codebase for `calorie_calculator`:

~~~{.python caption="calorie_calculator.py"}
# package containing methods for daily calorie intake calculations


def calculate_calorie_intake(bmr, activity_level):
    try:
        activity_level = str(activity_level)
        if activity_level == "sedentary":
            calories = bmr * 1.2
        elif activity_level == "lightly active":
            calories = bmr * 1.375
        elif activity_level == "moderately active":
            calories = bmr * 1.55
        else:
            calories = bmr * 1.725
        return int(calories)
    except ValueError:
        return None
~~~

At this point, you can already start to see some of the advantages that come with a monorepo setup, including reusable code, consistent tooling, easier integration, and increased collaboration opportunities.

In the upcoming sections, you'll learn how to use a couple of build tools ([Pants](https://www.pantsbuild.org/) and [Earthly](https://earthly.dev/)) to help you with monorepo management.

## Monorepo Management With Pants

A build tool helps you run tests, fix linting issues, containerize your application, and create builds that would otherwise be challenging and time-consuming. There are several popular build tools available, including Pants, [Bazel](https://bazel.build/), [Buck](https://buck.build/), and Earthly.

Pants is a popular monorepo management tool that is fast, user-friendly, and scalable. It supports Python, Java, Scala, Kotlin, Go, and Docker.

For a more in-depth tutorial on using Pants for Python projects, check out [this Earthly article](https://earthly.dev/blog/pants-python-monorepo/).

### Initializing Pants

To initialize Pants as a project, navigate to your project root directory and run the following command:

~~~{.bash caption=">_"}
pants
~~~

Executing this command creates hidden folders that Pants uses and a `pants.toml` file in which the configuration of the projects is defined.

Paste the following into your project's `pants.toml` file:

~~~{.toml caption="pants.toml"}
[GLOBAL]
pants_version = "2.18.1"
backend_packages.add = [
  "pants.backend.python",
  "pants.backend.python.lint.black",
  "pants.backend.build_files.fmt.black",
  "pants.backend.python.lint.docformatter",
  "pants.backend.python.lint.flake8",
  "pants.backend.python.typecheck.mypy",
]


[anonymous-telemetry]
enabled = false

[source]
root_patterns = ["/"]

[python]
interpreter_constraints = [">=3.9.*"]


[python-bootstrap]
search_path = [
    "/usr/bin/python3",
]
~~~

Make sure you create a `.flake8` file in your project's root directory with the following code:

~~~{.flake8 caption="flake8"}
[flake8]
extend-ignore:
  E203,  # whitespace before ':'
  E231,  # Bad trailing comma
  E501,  # line too long
~~~

This will prevent any configuration errors between the different linters you'll be using later on.

### Setting Up BUILD Files

Pants uses `BUILD` files to store metadata for each application or module that's created in each directory within the project.

To initialize the `BUILD` files, run the following command:

~~~{.bash caption=">_"}
pants tailor ::
~~~

This initializes a `BUILD` file in each of the directories within the project, including the root.

The project structure after initialization looks like this:

~~~{ caption=""}
├── BUILD
├── README.md
├── health_fitness_app
│   ├── BUILD
│   ├── __init__.py
│   ├── bmi_service
│   │   ├── BUILD
│   │   ├── __init__.py
│   │   ├── bmi_service.py
│   │   └── test_bmi_service.py
│   ├── calorie_intake_service
│   │   ├── BUILD
│   │   ├── __init__.py
│   │   ├── calorie_intake_service.py
│   │   └── test_calorie_intake_service.py
│   ├── main.py
│   └── packages
│       ├── bmi
│       │   ├── BUILD
│       │   ├── __init__.py
│       │   ├── bmi_calculator.py
│       │   └── test_bmi_calculator.py
│       ├── bmr
│       │   ├── BUILD
│       │   ├── __init__.py
│       │   ├── bmr_calculator.py
│       │   └── test_bmr_calculator.py
│       └── calorie
│           ├── BUILD
│           ├── __init__.py
│           ├── calorie_calculator.py
│           └── test_calorie_calculator.py
├── .flake8
├── pants.toml
└── requirements.txt
~~~

As you can see, seven `BUILD` files are created. Each `BUILD` file contains targets for both non-test and test files:

~~~{ caption="BUILD"}
# This target sets the metadata for all the Python non-test files 
# in this directory.
python_sources(
    name="lib",
)

# This target sets the metadata for all the Python test files 
# in this directory.
python_tests(
    name="tests",
)
~~~

You can refer to the [GitHub repo](https://github.com/furqanshahid85-python/python-monerepo) to see how each of the `BUILD` files should be set up for this project.

### Checking for Build Errors

Before you move on to the next step, make sure you run the following command to see if there are any errors in the setup of your project:

~~~{.bash caption=">_"}
pants tailor --check ::
~~~

If you don't get an output, your project setup is ready to go.

### Running Project Tests

Use the following command to run the unit tests defined for your project:

~~~{.bash caption=">_"}
pants test ::
~~~

Your output should look like this:

<div class="wide">
![Pants project tests]({{site.images}}{{page.slug}}/gS7g6vm.png)
</div>

### Fixing Linting and Formatting Issues

Pants supports many of the popular linting and formatting tools for Python, including [Flake8](https://flake8.pycqa.org/en/latest/), [Black](https://black.readthedocs.io/en/stable/), and [docformatter](https://docformatter.readthedocs.io/en/latest/).

To activate any linter or formatter, all you need to do is add a backend configuration in your `pants.toml` file. For instance, to run the linter, execute the following command:

~~~{.bash caption=">_"}
pants lint ::
~~~

This lists all the linting issues in your project:

<div class="wide">
![List of all the linting issues in your project]({{site.images}}{{page.slug}}/6kjQB0b.png)
</div>

To fix any linting or formatting issues in your project, execute the following command:

~~~{.bash caption=">_"}
pants fmt ::
~~~

Your output should look like this:

<div class="wide">
![Command output]({{site.images}}{{page.slug}}/H2v9VXQ.png)
</div>

To fix the linting issues, run `pants lint ::` again:

<div class="wide">
![Fixed linting issues]({{site.images}}{{page.slug}}/89UpMjl.png)
</div>

### Creating a Pants Package and Running the Application

Even though Python is not a compiled language and does not require a build, you can still package and build your project to easily maintain your code, isolate dependencies, and effectively share it with others.

To create a Pants build, run the following command:

~~~{.bash caption=">_"}
pants package health_fitness_app/main.py ::
~~~

This creates a `pex_binary.pex` file under `dist/health_fitness_app`:

~~~{ caption=""}
├── dist
│   ├── health_fitness_app
│   │   └── pex_binary.pex
│   ├── health_fitness_app.bmi.bmi_calculator-0.0.1-py3-none-any.whl
│   ├── health_fitness_app.bmi.bmi_calculator-0.0.1.tar.gz
│   ├── health_fitness_app.bmr.bmr_calculator-0.0.1-py3-none-any.whl
│   ├── health_fitness_app.bmr.bmr_calculator-0.0.1.tar.gz
│   ├── health_fitness_app.calorie.calorie_calculator-0.0.1-py3-none-any.whl
│   └── health_fitness_app.calorie.calorie_calculator-0.0.1.tar.gz
~~~

Execute the following command to run your application:

~~~{.bash caption=">_"}
pants run health_fitness_app/main.py
~~~

Your output should look like this:

~~~{ caption="Output"}
{'bmi_value': 24, 'bmi_category': 'Normal weight'}
{'daily_calorie_intake': 1808}
~~~

## Monorepo Management With Earthly

Now that you know how to use Pants for monorepo management, it's time to see how Earthly differs. As you now know, Pants supports Python, making it a suitable choice for large Python-based monorepo projects. It offers features like fine-grained caching for accelerated builds and static analysis for dependency resolution. However, it lacks support for JavaScript and Rust and primarily focuses on build and test steps within workflows.

On the other hand, Earthly supports a wide range of languages, including JavaScript, Python, Java, C++, Go, and Rust, making it well-suited for multilanguage monorepos. Embracing a containerized model often likened to "Docker for builds," Earthly enables the execution of various build tools compatible with Linux environments.

### Setting Up Your Monorepo with Earthly

Earthly uses an [`Earthfile`](https://docs.earthly.dev/docs/earthfile) to manage each service or package. The following is a list of the various components in the application:

~~~{ caption=""}
.
├── Earthfile
├── health_fitness_app
│   ├── __init__.py
│   ├── bmi_service
│   │   ├── __init__.py
│   │   ├── bmi_service.py
│   │   └── test_bmi_service.py
│   ├── calorie_intake_service
│   │   ├── __init__.py
│   │   ├── calorie_intake_service.py
│   │   └── test_calorie_intake_service.py
│   ├── main.py
│   └── packages
│       ├── bmi
│       │   ├── __init__.py
│       │   ├── bmi_calculator.py
│       │   └── test_bmi_calculator.py
│       ├── bmr
│       │   ├── __init__.py
│       │   ├── bmr_calculator.py
│       │   └── test_bmr_calculator.py
│       └── calorie
│           ├── __init__.py
│           ├── calorie_calculator.py
│           └── test_calorie_calculator.py
└── requirements.txt
~~~

An `Earthfile` has a Docker-like syntax, so if you're familiar with Docker, using it is easy.

### Setting Up the Earthfile

The `Earthfile` for your health and fitness app looks like this:

~~~{.dockerfile caption="Earthfile"}
VERSION 0.7
FROM python:3
WORKDIR /code

deps:
    RUN pip install --upgrade pip
    RUN pip install wheel
    COPY requirements.txt ./
    RUN pip wheel -r requirements.txt --wheel-dir=wheels
    SAVE ARTIFACT wheels /wheels

build:
    FROM +deps
    COPY health_fitness_app health_fitness_app
    SAVE ARTIFACT health_fitness_app /health_fitness_app

unit-tests:
    COPY +deps/wheels wheels
    COPY +build/health_fitness_app health_fitness_app
    COPY requirements.txt ./
    RUN pip install --no-index --find-links=wheels -r requirements.txt
    RUN pytest health_fitness_app

docker:
    COPY +deps/wheels wheels
    COPY +build/health_fitness_app health_fitness_app
    COPY requirements.txt ./
    ARG tag='latest'
    RUN pip install --no-index --find-links=wheels -r requirements.txt
    ENTRYPOINT ["python3", "health_fitness_app/main.py"]
    SAVE IMAGE python-earthly-monorepo:$tag
~~~

This `Earthfile` contains four different sections, or [targets](https://docs.earthly.dev/basics/part-1-a-simple-earthfile#creating-your-first-targets): `deps`, `build`, `unit-tests`, and `docker`. Each of these targets can be executed independently via the command `earthly +<target>`.

If you want to resolve your project dependencies, you can execute the following:

~~~{.bash caption=">_"}
earthly +deps
~~~

Your output would look like this:

<div class="wide">
![Resolving dependencies]({{site.images}}{{page.slug}}/DsgWeWz.png)
</div>

### Creating the Project Build

You can create your project build via the following command:

~~~{.bash caption=">_"}
earthly +build
~~~

This command creates your project's build, and any artifacts created in the build can be used in other targets:

<div class="wide">
![Creating the project build]({{site.images}}{{page.slug}}/uDCOo6D.png)
</div>

### Executing Unit Tests

To execute unit tests for your services and packages, you can run the following command:

~~~{.bash caption=">_"}
earthly +unit-tests
~~~

Your output should look like this:

<div class="wide">
![Running unit-tests]({{site.images}}{{page.slug}}/6VxrevN.png)
</div>

### Containerizing Your Project

Finally, if you want to containerize your project, you can do so with the following command:

~~~{.bash caption=">_"}
earthly +docker
~~~

Your output will look like this:

<div class="wide">
![Containerizing your project]({{site.images}}{{page.slug}}/FLq62Mc.png)
</div>

If you navigate to Docker Desktop, you can see that Earthly successfully created a Docker image for the project:

<div class="wide">
![Docker image]({{site.images}}{{page.slug}}/n42OIa1.png)
</div>

Earthly provides a simpler way to manage a Python monorepo when compared to Pants. Earthly's Dockerized approach, which utilizes an `Earthfile`, allows you to define the project dependencies and individual build or test steps to easily containerize the application.

## Conclusion

In this article, you learned all about monorepos and why you'd want to use one. You also learned how to build a monorepo in Python and how you can simplify monorepo management with two popular build tools: Pants and Earthly.

If your projects deal with containerized microservices, [Earthly](https://earthly.dev/) is an ideal tool, as it offers extensive capabilities through its Docker-like syntax and container-based approach. This facilitates the effortless creation of distinct builds for each service within your application, providing flexibility, quick build creation, and caching functionalities.

{% include_html cta/bottom-cta.html %}
