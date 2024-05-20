---
title: "Python Environment Management with Hatch"
categories:
  - Tutorials
toc: true
author: Gourav Singh Bais

internal-links:
 - just an example
---

[Hatch](https://github.com/pypa/hatch) is a modern, extensible Python project manager that's known for its ability to seamlessly manage multiple environments for a single Python application.

For example, if you're developing an application that runs on different Python versions (such as [3.10](https://www.python.org/downloads/release/python-3100/) and [3.11](https://www.python.org/downloads/release/python-3110/)), you'd need to create separate virtual environments using tools like [venv](https://docs.python.org/3/library/venv.html) or [conda](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html) to accommodate varying dependency requirements. Similarly, for production-grade apps, you need to maintain different environments for development, testing, and documentation, necessitating different sets of dependencies. As your application scales, manually managing these environments becomes cumbersome. Thankfully, Hatch can help handle these environments automatically so that you're free to focus on coding.

In this article, you'll learn more about Hatch and how it can help you manage multiple virtual environments in a single Python repo.

## What Is Hatch?

As an extensible Python project manager, Hatch can define versions, declare dependencies, and publish packages to PyPI via its [build backend](https://peps.python.org/pep-0517/) called [Hatchling](https://hatch.pypa.io/latest/history/hatchling/). Unlike [setuptools](https://pypi.org/project/setuptools/), Hatchling stands out in terms of [configurability, reproducibility, and extensibility](https://hatch.pypa.io/latest/why/#build-backend).

Additionally, while tools like [tox](https://tox.wiki/en/4.14.2/) and [Nox](https://nox.thea.codes/en/stable/) require preinstalled Python versions, Hatch dynamically downloads required Python distributions on demand, thus ensuring seamless execution.

Thanks to Hatch's Python management capabilities, Hatch is cross-platform compatible, simplifies development workflows, and offers [faster dependency installation](https://hatch.pypa.io/latest/why/) when compared to [venv](https://docs.python.org/3/library/venv.html) and [pyenv](https://github.com/pyenv/pyenv).

## How to Create Virtual Environments Using Hatch

Now that you know how Hatch can help you, you can learn how to create different virtual environments for a single Python application using Hatch.

### Installing Hatch

Installing Hatch in Python is easy; simply run `pip install hatch`. Your output will look something like this:

~~~
gouravbais08@Gouravs-Air ~ % pip install hatch
Collecting hatch
Obtaining dependency information for hatch from https://files.pythonhosted.org /packages/05/38/ba8f90264d19ed39851f37a22f2a4be8e9644a1203f114b16647f954bb02/hat
ch-1.9.4-py3-none-any.whl.metadata
Downloading hatch-1.9.4-py3-none-any.whl.metadata (5.2 kB)
Collecting click>=8.0.6 (from hatch)
Obtaining dependency information for click>=8.0.6 from https://files.pythonhos
ted.org/packages/00/2e/d53fabefbf2cfa713304affc7ca780ce4fc1fd8710527771658311a3
229/click-8.1.7-py3-none-any.whl.metadata
Downloading click-8.1.7-py3-none-any.whl.metadata (3.0 kB)
Collecting hatchling<1.22 (from hatch)
Obtaining dependency information for hatchling<1.22 from https://files. pythonh osted.org/packages/3a/bb/40528a09a33845bd7fd75c33b3be7faec3b5c8f15f68a58931da674
20fb9/hatchling-1.21.1-py-none-any.whl.metadata
Downloading hatchling-1.21.1-py3-none-any.whl.metadata (3.8 kB)
Collecting httpx>=0.22.0 (from hatch)
Obtaining dependency information for httpx>=0.22.0 from https://files. pythonho sted.org/packages/ 41/7b/ddacf6dcebb42466abd03f368782142baa82e08fc0c1f8eaa05b4bae
87d5/httpx-0.27.0-py3-none-any.whl.metadata
~~~

You can also install Hatch as an application on [Windows and Mac](https://hatch.pypa.io/latest/install/#installers) operating systems. [Conda](https://hatch.pypa.io/latest/install/#conda), [pipx](https://hatch.pypa.io/latest/install/#pipx), [Homebrew](https://hatch.pypa.io/latest/install/#homebrew), [MacPorts](https://hatch.pypa.io/latest/install/#macports), [Fedora](https://hatch.pypa.io/latest/install/#fedora), and [Void Linux](https://hatch.pypa.io/latest/install/#void-linux) installation methods are also available.

### Creating a Project

When you create any Python application, you have to create a folder structure for your application logic, tests, documentation, and other project-specific files like `pyproject.toml`. As a project manager, Hatch lets you initialize a Python application that contains all the project setup files and folders. You just need to make changes to these files to fit your application.

To create a new project, all you have to do is run the `hatch new <project name>` command. This command creates a project directory containing a source code directory (`src`), a test directory (`tests`), and a configuration file for project-related tools (`pyproject.toml`).

For this tutorial, let's create a simple Python application named `hatch-demo` that uses a [Flask API](https://flask.palletsprojects.com/en/3.0.x/). To do so, run `hatch new "Hatch Demo"`. The folder structure that's created will look like this:

~~~
gouravbais08@Gouravs-Air Hatch_Project % hatch new "Hatch Demo"
hatch-demo
|---- src
|     |---- hatch_demo
|           |---- __about__.py
|           |---- __init__.py
|---- tests
|     |---- __init__.py
|---- LICENSE.txt
|---- README.md
|---- pyproject.toml
~~~

> **Note:** If you want to initialize an existing project, you can do so using the `hatch new --init` command. If there is a `setup.py` file available in your project, a `setuptools` file will be generated from it. Otherwise, Hatch interactively guides you to produce the content for the configuration file.

Once you've created your Python application, open the `pyproject.toml` file. You should see that a lot of your project configuration values, such as dependencies and the Python version, are prefilled by Hatch. You'll also notice other sections with the pattern `[tool.hatch.*]`, which is where you'll configure your project to use different Python dependencies, environments, and Python versions.

### Understanding Hatch Virtual Environments

Python environments offer isolated workspaces for development, testing, and documentation, each capable of having its own dependencies and Python versions. Hatch's primary feature lies in its ability to generate multiple environments for a single Python application.

If you go back to your `pyproject.toml` file, you'll notice that a few environments—including `default` (`[tool.hatch.envs.default]`) and `types` (`[tool.hatch.envs.types]`)—have already been created.

> **Please note:** Defaults may vary depending on your version of Hatch. This article uses Hatch version 1.9.4.

You can also run `hatch env show` to see a full list of environments:

![Hatch show envs](https://i.imgur.com/34UxFxK.png)

Each of these environments is populated with some dependencies (*eg* `pytest` and `mypy`). You can also define project-specific dependencies if desired or run different Python scripts in different environments by specifying them in the `scripts` section of the environment. When no environment is chosen explicitly, Hatch uses the `default` environment.

### Creating a Python Application with Hatch

Now that you're familiar with the `pyproject.toml` file, go ahead and create a simple Flask API (`app.py`) in the `src/hatch_demo` directory and a test script (`test_app.py`) in the `tests` directory.

Add the following code to the `app.py` file:

~~~
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
~~~

This code imports the Flask dependency and creates an endpoint named `hello` that prints a simple message.

To test the app, add the following lines of code to the `test_app.py` file:

~~~
import unittest

class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()
~~~

This code performs [unit testing](https://docs.python.org/3/library/unittest.html) by converting a simple string to uppercase.

Now that the setup is complete, it's time to explore the environments in Hatch.

### Creating a Hatch Environment and Specifying Dependencies

Apart from the default environment, you can also create different environments with Hatch. To do so, run the following command in your terminal:

~~~
hatch env create
~~~

After you've run this command, head over to the `pyproject.toml` file and add a new `[tool.hatch.envs.<name>]` section for a specific environment.

For this Flask app, you'll use the default environment to run the Flask application and create a new environment named `test` to run the unit tests with [pytest](https://docs.pytest.org/en/8.0.x/).

Make the following changes to the `default` environment:

~~~
[tool.hatch.envs.default]
dependencies = [
  "coverage[toml]>=6.5",
  "flask"
]
[tool.hatch.envs.default.scripts]
app = "python src/hatch_demo/app.py"
~~~

As you can see, Flask is mentioned in the dependencies, and the script that you need to test is mentioned in the `scripts` section of the environment.

To create the `test` environment, add the following lines of code to the `pyproject.toml` file:

~~~
[tool.hatch.envs.test]
dependencies = [
  "pytest",
  "pytest-cov",
  "pytest-watcher"
]

[tool.hatch.envs.test.scripts]
test = "pytest {args:tests}"
test-cov = "coverage run -m pytest {args:tests}"
cov-report = [
  "- coverage combine",
  "coverage report",
]
cov = [
  "test-cov",
  "cov-report",
]
~~~

Here, a new `test` environment is created with Python testing dependencies, and the `scripts` section uses `pytest`.

### Handling Multiple Python Versions with Matrices

If you want to provide a list of supported Python versions for an environment, you can use the `matrix` section in the environment configuration. For example, to use two distinct Python versions in the `test` environment, you can include the following lines in your `pyproject.toml` file:

~~~
[[tool.hatch.envs.test.matrix]]
python = ["3.10", "3.11"]
~~~

Based on this setup, Hatch generates two distinct virtual environments for testing: one for Python 3.10 and one for Python 3.11. The dependencies specified for the `test` environment will be present in both virtual environments. You can review the complete `pyproject.toml` file on [GitHub](https://github.com/gouravsinghbais/How-to-Create-a-Python-Virtual-Environment-with-Hatch/blob/master/pyproject.toml).

### Running Scripts in an Environment

To run a Python script using Hatch, you can use the `hatch run` command, which supports several arguments, including one for specifying the desired environment. If no environment is specified, the default environment and its dependencies are used to run the script.

To start your Flask app in the default environment, run the following:

~~~
hatch run app
~~~

Your output should look like this:

~~~
* Serving Flask app 'app'
* Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment.
Use a production WSGI server instead.
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:3000
* Running on http://192.168.1.34:3000
~~~

If you want to run a script from another environment, you need to specify the environment name and the script name. You can do this by adding `<ENV_NAME>:` before the script in the run commands. The value before `:` specifies the environment name, and the value after `:` specifies the script name.

For example, you can run the test script in the `test` environment like this:

~~~
hatch run test:test
~~~

Your output should look something like this:

~~~
platform darwin -- Python 3.11.5, pytest-8.1.1, pluggy-1.4.0
rootdir: /Users/gouravbais08/Projects_and_Learning/Personal_Projects/Hatch_Proje
ct/hatch-demo configfile: pyproject.toml
plugins: cov-5.0.0
collected 1 item
tests/test_app.py •
[100%]
============================ 1 Passed in 0.01s ==================================
~~~

Another way to specify an environment is with the `-e`/`--env` flag. For instance, you can run the same test script using the `-e` flag like this:

~~~
hatch -e test run test
~~~

The `--env` flag would work the same way here.

#### Removing an Environment

Once you're finished with the development, testing, and deployment of your Python application, you need to remove the environments so that they don't occupy your memory space.

To remove an environment, run the `hatch env remove <ENV NAME>` command. You can also remove all the project environments with the `hatch env prune` command.

For example, if you want to remove the `test` environment, run `hatch env remove test`:

![Hatch remove environment](https://i.imgur.com/PuMr6tP.png)

All the code for this tutorial is available in [this GitHub repo](https://github.com/gouravsinghbais/How-to-Create-a-Python-Virtual-Environment-with-Hatch).

## Limitations of Virtual Environments with Hatch

While Hatch provides many benefits, there are a few limitations you need to be aware of:

- **Lack of system-level (non-Python) dependency management:** One of the major issues you'll encounter when utilizing Hatch for multiple environments is the ["it works on my machine"](https://www.activestate.com/blog/how-to-eliminate-works-on-my-machine-issues/) dilemma. Despite having identical Python dependencies in two environments, variations in non-Python dependencies can produce different results. This discrepancy is commonly observed with libraries like [Matplotlib](https://matplotlib.org/) that rely on system-level libraries for tasks such as image rendering. These system-level dependencies may vary across systems, resulting in inconsistencies.
- **Not suitable for extension modules:** Hatch lacks support for interfacing with interpreters or compilers, making it unsuitable for developing [Python extension modules](https://llllllllll.github.io/c-extension-tutorial/what-is-an-extension-module.html) that need direct interaction with interpreters. It's recommended that you utilize configuration management tools such as [setuptools](https://pypi.org/project/setuptools/) or other backends specifically designed for interfacing with compilers.
- **No support for patch release versions:** Hatch uses a minor release granularity that follows the most recent patch release. Currently, it doesn't allow the installation of certain patch release versions. It's recommended that you use a different installation method if you place a high value on a particular patch release.

## How to Sandbox System-Level Dependencies with Earthly

While you can manually create and manage an environment and its dependencies, it can become tedious as the project grows. You need a solution that can simplify dependency management across different stages of your application development, including testing, staging, and deployment.

An effective approach to simplifying dependency management is to leverage [Earthly](https://earthly.dev/) for tasks like testing, continuous integration (CI), and building container images. When you create an [Earthfile](https://docs.earthly.dev/docs/earthfile), which resembles a Dockerfile, you can define Python requirements, both Python and system-level dependencies, environments, and other Python testing details.

For instance, the following is a sample `Earthfile` for a Flask API:

~~~
# Use a specific Python version
FROM python:3.8
WORKDIR /code

deps:
    # Install system-level dependencies
    RUN apt-get update && apt-get install -y libpq-dev

    # Install Python packages
    COPY requirements.txt ./
    RUN pip3 install -r requirements.txt

    # Copy in code
    COPY --dir src tests
    
test:
  FROM +deps
  RUN python -m unittest tests/test_app.py
 
# Build the target and start the application
docker:
  ENV FLASK_APP=src/app.py
  ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--port=3000"]
  SAVE IMAGE my-python-app:latest
 
integration-tests:
    FROM +deps
    RUN apk update && apk add postgresql-client
    WITH DOCKER --compose docker-compose.yml
        RUN python test_db_end_to_end.py
    END
~~~

To learn more about the specifics of the code here and how Earthly can help you solve the issue of system-level dependencies, check out [this article](https://earthly.dev/blog/python-earthly/).

## Conclusion

Handling multiple virtual environments for a single application can be difficult. Hatch, a popular Python project manager, helps you easily create and maintain different virtual environments for a single application with the help of a `pyproject.toml` file.

In this article, you learned how to create, manage, and delete virtual environments using Hatch.

While Hatch offers features such as project management, dependency management, and environment management, it can't handle system-level dependencies, which significantly impacts code reproducibility. While manually creating and managing environments can mitigate this issue, it's cumbersome and challenging to maintain consistency across different systems. Thankfully, [Earthly](https://cloud.earthly.dev/login) can help streamline your development processes and resolve system-level dependencies with the help of a single Earthfile. This file can manage your Python dependencies and system-level dependencies all in one place while providing a step-by-step execution flow like Docker.

## Outside Article Checklist

- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
- [ ] Would any images look better `wide` or without the `figcaption`?
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links
- [ ] Add Earthly `CTA` at bottom `{% include_html cta/bottom-cta.html %}`
