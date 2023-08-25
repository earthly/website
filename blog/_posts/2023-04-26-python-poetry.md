---
title: "Managing Dependencies Using Poetry in Python"
categories:
  - Tutorials
toc: true
author: Ashutosh Krishna
editor: Bala Priya C

internal-links:
 - Python
 - Dependencies
 - Poetry
 - Virtual Environments
excerpt: |
    
---
**We're [Earthly](https://earthly.dev/). We streamline software building using containerization. Earthly, combined with Poetry, can make your Python project builds smoother and faster. [Check it out](/).**

Python is a versatile language used for various applications. However, managing dependencies, the [packages](/blog/setup-typescript-monorepo) a project relies on can be a complex and time-consuming task. With the growth of the Python ecosystem, developers need to manage a large number of packages and dependencies and ensure that they are compatible with each other.

Poetry provides a solution to these challenges. [Poetry](https://python-poetry.org/) is a package manager for Python that allows developers to manage dependencies, create virtual environments, and package their projects for distribution, all using a single command-line tool.

In this tutorial, you will learn the basics of using Poetry to manage dependencies in Python projects. You'll create a library called `weather-update` that uses the [OpenWeatherMap API](https://openweathermap.org/api) and the `requests` library to retrieve the current weather of a given city.

## Prerequisites

To follow this tutorial, it is recommended that you have the following:

- Python 3.7+ installed
- Basic understanding of [virtual environments, modules, and packages](https://docs.python.org/3/tutorial/venv.html)

You can find the code samples used in this tutorial in [this repository](https://github.com/ashutoshkrris/weather-update).

## Installation

Poetry is designed to be compatible with multiple platforms, including Linux, macOS, and [Windows](/blog/makefiles-on-windows). It features a customized installer that installs Poetry in a separate virtual environment, isolating it from the rest of the system. This prevents accidental upgrades or uninstalls of dependencies and enables Poetry to manage its environment effectively.

To install Poetry on **Windows**, open the Windows Powershell and run the following command:

~~~{.bash caption=">_"}
(Invoke-WebRequest -Uri https://install.python-poetry.org\
 -UseBasicParsing).Content | python -
~~~

To install Poetry on **Linux**, **macOS** and **Windows (WSL)**, open a terminal and run the following command:

~~~{.bash caption=">_"}
curl -sSL https://install.python-poetry.org | python3 -
~~~

This will download and install the latest version of Poetry. To verify that Poetry has been installed correctly, run the following command:

~~~{.bash caption=">_"}
poetry --version
~~~

If you see something like `Poetry (version 1.3.2)`, your installation is ready to use!

## Getting Started With Poetry

In this section, you will learn how to create a new Python project using Poetry and set up the project's name, version, and description. Additionally, you will understand the role of the `pyproject.toml` file in managing dependencies and how it serves as the central configuration file for the project. You will also learn how to initialize a pre-existing project with Poetry to start managing its dependencies effectively.

### Creating a New Project

You can use the [`new`](https://python-poetry.org/docs/cli/#options-1) command followed by the project name to create a new Poetry project. For example, you can use the following command to create a project named `weather-update` for your library:

~~~{.bash caption=">_"}
poetry new weather-update
~~~

The command creates a new folder `weather-update` with the following structure:

~~~{ caption=""}
weather-update
├── pyproject.toml
├── README.md
├── weather_update
│   └── __init__.py
└── tests
     └── __init__.py
~~~

The folder `weather-update` contains two files named `pyproject.toml` and `README.md` and two packages named `weather_update` to store the source code files and `tests` to store the test files.

If you prefer using the name `src` instead of `weather_update`, you can add the `--src` flag while creating the project as below:

~~~{.bash caption=">_"}
poetry new --src weather-update
~~~

### Understanding the `pyproject.toml` File

The `pyproject.toml` file serves as the configuration file that contains information about the project and its dependencies. By default, the [`pypoetry.toml`](https://python-poetry.org/docs/pyproject/) contains three [tables](https://toml.io/en/v1.0.0#table) - `tool.poetry`, `tool.poetry.dependencies` and `build-system`.

~~~{.toml caption="pyproject.toml"}
# pyproject.toml

[tool.poetry]
name = "weather-update"
version = "0.1.0"
description = ""
authors = ["Ashutosh Krishna <contact@ashutoshkrris.in>"]
readme = "README.md"
packages = [{include = "earthly_poetry_demo"}]
~~~

The `tool.poetry` table of the `pyproject.toml` file is composed of multiple key/value pairs. While the `name`, `version`, `description`, and `authors` keys are required, others are optional.

Poetry assumes that a package with the same name as the `tool.poetry.name` specified in the `pyproject.toml` file is located at the root of the project. If the package location is different, the packages and their locations can be specified in the `tool.poetry.packages` key.

~~~{.toml caption="pyproject.toml"}
# pyproject.toml

[tool.poetry.dependencies]
python = "^3.9"
~~~

It is mandatory to declare the Python version for which your package is compatible in the `tool.poetry.dependencies` table.

~~~{.toml caption="pyproject.toml"}
# pyproject.toml

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
~~~

The last table [`build-system`](https://peps.python.org/pep-0517/) has two keys - `requires` and `build-backend`. The `requires` key is a list of dependencies required to build the package and the `build-backend` key is the Python object used to perform the build process.

The file looks like [this](https://github.com/ashutoshkrris/weather-update/blob/8ef5702c946ad6b86dd3f2d7cf687c84fdd935fe/pyproject.toml).

TOML is the preferred configuration format for Poetry. Starting from version 3.11, Python provides a `tomllib` module for parsing TOML files.

### Initializing a Pre-Existing Project

There can be situations where you have an existing project, and you wish to add Poetry to it for managing your dependencies. In that case, the `poetry new` command won't be very useful as it will create a new project from scratch.

Suppose, you have a project named `existing-project` containing a `main.py` file with the following contents:

~~~{.python caption="main.py"}
# main.py

print("Earthly is awesome!")
~~~

In this case, you can use the `init` command to initialize Poetry in your project. It helps you interactively create a `pyproject.toml` file in the `existing-project` directory.

<div class="wide">
![poetry-init-interactively]({{site.images}}{{page.slug}}/KiiHcOZ.gif)
</div>

The `poetry init` command initiates an interactive session for creating the `pyproject.toml` file. Poetry offers suggestions for the majority of configurations needed for setup, and pressing Enter allows for their usage. In the end, it will also preview the file before generating it. Once you confirm the generation, it will generate the file.

## Managing Virtual Environments

As you learn Python and start building different projects, you'll quickly find that each project may have different versions of libraries and dependencies. If these versions conflict with each other, it can lead to unexpected errors and [make](/blog/makefiles-on-windows) it difficult to manage the projects. This is where virtual environments can help.

Virtual environments are isolated environments for your Python projects. This means that each project can have its own set of dependencies, without affecting other projects or your system's Python installation. This is particularly useful when you have multiple projects that require different versions of the same dependency.

Virtual environments ensure compatibility, reproducibility, and reduce the risk of conflicts with other projects on your system.

Let's say you are working on two different Python projects: Project A and Project B. Project A requires version 2.26.0 of the library `requests`, while Project B requires version 2.28.2. If you try to install both versions of `requests` globally on your system at the same time, the second installation will remove the `requests` library which was installed first.

However, by using virtual environments, you can isolate the dependencies of each project. You can create a virtual environment for Project A and install version 2.26.0 of `requests` in it. Then, you can create another virtual environment for Project B and install version 2.28.2 of `requests` in it.

<div class="wide">
![Python Virtual Environments]({{site.images}}{{page.slug}}/foXhfQK.png)
</div>

This way, the two projects are isolated from each other, and each has its own version of the library `requests` without creating any compatibility issues.

### Creating Virtual Environments With Poetry

Poetry makes it easy to create virtual environments for your projects. To create a virtual environment for your `weather-update` library, simply run the `env use` command in your project directory:

~~~{.bash caption=">_"}
poetry env use /full/path/to/python
~~~

The `/full/path/to/python` specifies the full path to the Python executable.
Example:

~~~{.bash caption=">_"}
poetry env use /usr/local/bin/python3.9
~~~

Output:

~~~{ caption="Output"}
Creating virtualenv weather-update-HkPi_rXk-py3.9 in \
/Users/ashutoshkrris/Library/Caches/pypoetry/virtualenvs
Using virtualenv: \
/Users/ashutoshkrris/Library/Caches/pypoetry/virtualenvs/\
weather-update-HkPi_rXk-py3.9
~~~

If you have the python executable in your `PATH` you can use it:

~~~{.bash caption=">_"}
poetry env use python3.9
~~~

You can even just use the minor Python version in this case:

~~~{.bash caption=">_"}
poetry env use 3.9
~~~

The minor Python version refers to the second component of the Python version number, for example, 3.9 in the case of Python version 3.9.16.

To disable the explicitly activated virtual environment, use the `system` as the Python version to revert to default behavior.

~~~{.bash caption=">_"}
poetry env use system
~~~

Sometimes you may need to use the system-wide Python installation for compatibility reasons or to perform a specific task. In such cases, you can use the special `system` Python version to retrieve the default behavior.  

## Working With Poetry

In this section, you'll learn how to work with Poetry to manage dependencies in your Python projects. In addition to that, you'll also learn about dependency groups in Poetry.

### Managing Dependencies

Since your `weather-update` library will interact with OpenWeatherMap API under the hood, it will need the `requests` library to be installed.
If you remember, you had a `[tool.poetry.dependencies]` table in your `pyproject.toml` file to specify your dependencies. You can add them directly to your project:

~~~{.toml caption="pyproject.toml"}
# pyproject.toml

[tool.poetry.dependencies]
python = "^3.9"
requests = "^2.28.2"
~~~

Poetry provides another way to add dependency in your project. While you can add it manually, you should use the `add` command to install the dependency. It ensures that the dependencies are installed correctly, version constraints are properly defined, and the pyproject.toml file is automatically updated with the correct information.

~~~{.bash caption=">_"}
poetry add requests
~~~

Output:

~~~{ caption="Output"}
Using version ^2.28.2 for requests

Updating dependencies
Resolving dependencies...

Writing lock file

Package operations: 5 installs, 0 updates, 0 removals

  • Installing certifi (2022.12.7)
  • Installing charset-normalizer (3.0.1)
  • Installing idna (3.4)
  • Installing urllib3 (1.26.14)
  • Installing requests (2.28.2)
~~~

Similarly, you can use the `remove` command to remove any dependencies that you don't require:

~~~{.bash caption=">_"}
poetry remove <some-dependency>
~~~

The command will remove the dependency and update the `pyproject.toml` and `poetry.lock` files. But you don't need to run the command at this moment since you don't have any extra dependency.

### The `poetry.lock` File

During the installation, removal, or updation of a dependency, Poetry keeps a record of the exact versions of all dependencies used in a project in a `poetry.lock` file. The `poetry.lock` file lists all packages, the exact versions of those packages, and the hashes of their source files, guaranteeing that your project uses the correct dependencies.

After you installed the `requests` library, your `poetry.lock` file will look like [this](https://github.com/ashutoshkrris/weather-update/blob/e37d4ad27004aaa74721e214f4f9bb2dcc6b45d3/poetry.lock).

In the file, you can see that the file records the exact versions and hashes of the installed dependencies. In the later sections when you'll add more dependencies, you'll see this file tracking the changes.

When you share your project, the `poetry.lock` file ensures that others will be using the same dependencies that you used to build and test your project. Thus, it is important to commit the `poetry.lock` file to your version control.

You can create a `requirements.txt` file from your `poetry.lock` file as:

~~~{.bash caption=">_"}
poetry export --output requirements.txt
~~~

### Developing Your Application

![dev]({{site.images}}{{page.slug}}/dev.png)\

So far, you have just installed the `requests` library. Your application has no functionality. Thus, in this section, you'll be adding your application logic. Create a `weather.py` file in the `src/weather_update` package and follow along.

Import the `os`, `requests`, and `configparser` libraries for use in the rest of the code

~~~{.python caption="weather.py"}
# weather.py

import os
import requests
import configparser

# Global variable for the configuration file
CONFIG_FILE = "config.ini"
~~~

The `CONFIG_FILE` global variable stores the name of the configuration file. This file will store the OpenWeatherMap API Key.

~~~{.python caption="weather.py"}
# weather.py

def get_weather(location: str):
    """
    Get the weather updates for the specified location

    Arguments:
    location: str -- location for which the weather updates are needed

    Returns:
    dict -- weather updates for the specified location
    """
    api_key = get_api_key()
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(weather_url)
    return response.json()
~~~

The `get_weather` function takes the location as an argument and returns the weather updates for that location. It calls the `get_api_key` function to get the API key and then uses the API key to make a request to the OpenWeatherMap API to get the weather updates.

~~~{.python caption="weather.py"}
# weather.py

def get_api_key():
    """
    Get the OpenWeatherMap API key from the configuration file
    """
    config = configparser.ConfigParser()
    api_key = None

    if not os.path.exists(CONFIG_FILE):
        print("You don't have an API Key set for OpenWeatherMap.")
        set_api_key()

    try:
        config.read(CONFIG_FILE)
        api_key = config.get("DEFAULT", "api_key")
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print(f"Error while reading the API key:\n {e}")
        set_api_key()
        api_key = config.get("DEFAULT", "api_key")

    return api_key
~~~

The `get_api_key` function first checks if the `config.ini` file exists, and if it doesn't, it calls the `set_api_key` function to create the file and set the API key. It then reads the API key from the configuration file using the `configparser` library.

~~~{.python caption="weather.py"}
# weather.py

def set_api_key():
    """
    Set the OpenWeatherMap API key in the configuration file
    """
    try:
        config = configparser.ConfigParser()
        api_key = input("Enter your OpenWeatherMap API key: ")
        config["DEFAULT"] = {"api_key": api_key}
        with open(CONFIG_FILE, "w") as configfile:
            config.write(configfile)
    except PermissionError:
        print("Error: You do not have permission to write to the file.")
    except configparser.Error:
        print("Error: Unable to write to the configuration file.")
~~~

The `set_api_key` function sets the API key in the configuration file using the `configparser` library. The function prompts the user to enter the API key and writes it to the file.

To check whether the code works, you can create a `main.py` file and add the following code:

~~~{.python caption="main.py"}
# main.py

from src.weather_update.weather import get_weather


if __name__ == '__main__':
    location = input("Enter the location: ")
    response = get_weather(location)
    if response['cod'] == 200:
        print(f"The weather in {location} is \
        {response['weather'][0]['description']}")
    else:
        print(response['message'])
~~~

The code imports the `get_weather` function from the `weather` module in the `src.weather_update` package. It prompts the user to enter a location and then retrieves the weather updates for that location using the `get_weather` function.

For the first run, the code will also ask for the OpenWeatherMap API Key.

~~~{ caption="Output"}
Enter the location: Bengaluru
You don't have an API Key set for OpenWeatherMap.
Enter your OpenWeatherMap API key: myopenweathermapapi
The weather in Bengaluru is overcast clouds
~~~

For the subsequent runs, the code won't ask you for the API Key as it has already set it.

~~~{ caption="Output"}
Enter the location: Gaya
The weather in Gaya is clear sky
~~~

Suppose you set an incorrect value of the API Key, you'll get an error:

~~~{ caption="Output"}
Enter the location: Gaya
Invalid API key. 
Please see https://openweathermap.org/faq#error401 for more info.
~~~

### Dependency Groups

Next, you'll be testing your application using PyTest. For that, you'll need to install two libraries: `pytest` and `requests-mock`. Apart from that, in your development environment, you'll also be using the `black` library to format your code. You can see that we just introduced two different environments: test and dev.

In a more complex application, you can have more environments such as *dev*, *test*, *pre-prod*, and *prod*. For each of the environments, the dependencies can vary as per requirements.

Starting from version 1.2.0, Poetry offers a method for organizing dependencies into groups. So instead of installing all the dependencies in one table (`[tool.poetry.dependencies]`), you can create dependency groups for each of the environments. This way, the dependencies are not cluttered but organized as per their usage in different environments.

To create a new dependency group, use the `tool.poetry.group.<group>` section, where `<group>` represents the name of the dependency group (e.g. "dev"):

~~~{.toml caption="pyproject.toml"}
#pyproject.toml

[tool.poetry.group.dev]  # Group definition

[tool.poetry.group.dev.dependencies]
black = "^23.1.0"
~~~

In a later section, you'll learn a way to add a dependency in a better way rather than adding dependencies to a specific group manually. So, you can avoid adding dependencies at this moment.

### Adding a Dependency to a Group

As mentioned above, there is one more way to add dependencies to a group. You can use the `add` command to add dependencies to a group. Use the `--group` or `-G` option to specify the group name.

The `add` command not only adds the dependency to the specified group in the `pyproject.toml` file but also updates the `poetry.lock` file, which keeps track of the exact version of each dependency used in the project. This helps in avoiding conflicts and inconsistencies in the dependencies and their versions, which can arise from manual edits. The `add` command automatically creates a group if it doesn't already exist.

In the `dev` environment, you'll install the `black` library.

~~~{.bash caption=">_"}
poetry add black --group dev
~~~

Similarly, for testing purposes, you'll require two libraries - `pytest` and `requests-mock`. You will use PyTest to write and run the unit tests, and the `requests-mock` library allows you to mock the HTTP requests made using the `requests` library.

You can add the two libraries in the `test` group as:

~~~{.bash caption=">_"}
poetry add pytest requests-mock --group test 
~~~

After installing the libraries, your `pyproject.toml` file will look like this:

~~~{.toml caption="pyproject.toml"}
#pyproject.toml

[tool.poetry]
name = "weather-update"
version = "0.1.0"
description = ""
authors = ["Ashutosh Krishna <ashutoshbritish@gmail.com>"]
readme = "README.md"
packages = [{include = "weather_update", from = "src"}]

[tool.poetry.dependencies]
python = "^3.9"
requests = "^2.28.2"

[tool.poetry.group.dev.dependencies]
black = "^23.1.0"

[tool.poetry.group.test.dependencies]
pytest = "^7.2.1"
requests-mock = "^1.10.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
~~~

If you notice, you didn't create the `dev` and `test` groups. They were created automatically.

After this section, your `poetry.lock` file will now look something like [this](https://github.com/ashutoshkrris/weather-update/blob/546e3492e9fd9cc93fb7bd1575611be816f1d436/poetry.lock).

### Optional and Non-Optional Dependency Groups

In Poetry, optional groups are collections of dependencies that are not required to run the project but are useful for certain use cases. For example, your project needs to have an optional group for development dependencies, which includes tools such as `black`. These dependencies are not necessary for the normal operation of the project, but they are needed to run the tests. By making these dependencies optional, you can reduce the size of the project's virtual environment and avoid having unnecessary dependencies installed.

To specify a group as optional, you can add the `optional = true` setting to the group's definition in the `pyproject.toml` file.

~~~{.toml caption="pyproject.toml"}
#pyproject.toml

[tool.poetry.group.dev]
optional = true

[tool.poetry.group.dev.dependencies]
black = "^23.1.0"
~~~

Similarly, you can make the `test` group optional too because the dependencies such as `pytest` and `requests-mock` are used in the testing environment only.

~~~{.toml caption="pyproject.toml"}
#pyproject.toml

[tool.poetry.group.test]
optional = true

[tool.poetry.group.test.dependencies]
pytest = "^7.2.1"
requests-mock = "^1.10.0"
~~~

Non-optional groups in Poetry refer to the groups of dependencies that are required for a project to function properly. They are not designated as optional in the pyproject.toml file and their dependencies are considered part of the default set of dependencies for a project. Unlike optional groups, non-optional groups are always installed, and their dependencies are always available for use in your project.

Optional and non-optional dependency groups are functionally independent and isolated. Packages in one group are not automatically made available to another group, and packages installed in one group do not affect packages installed in another group. This allows you to manage different sets of dependencies for different parts of your project, making it easier to manage the dependencies of your project as it evolves.

The default dependencies for a project in Poetry consist of two types of dependencies: the dependencies specified in the `tool.poetry.dependencies` table of the `pyproject.toml` file and the dependencies specified in the non-optional groups.

### Removing Dependencies From a Group

While you haven't added any extra dependency to your project, you might download some dependencies just to try them out. In those cases, you'll need to remove those dependencies after their usage. You can use the `remove` command to remove dependencies from a group. Use the `--group` or `-G` option to specify the group name.
Suppose you wish to remove a dependency called `some-dependency` from the `dev` group:

~~~{.bash caption=">_"}
poetry remove <some-dependency> --group dev
~~~

It is recommended to remove extra dependencies because they can increase the size of the project, make it harder to manage, slow down performance, and create security vulnerabilities. Keeping only the necessary dependencies can help keep the project lightweight, maintainable, and secure. Additionally, it can also help improve the stability of the application and make it easier to test and debug.`

After you remove any dependency, your `pyproject.toml` and `poetry.lock` files will be updated automatically.

### Installing Group Dependencies

Poetry provides a `poetry install` command to install dependencies specified in your `pyproject.toml` file.

~~~{.bash caption=">_"}
poetry install
~~~

Some use cases when the `poetry install` command can be useful:

 1. Remember when you added the dependencies manually in your `pyproject.toml` file? In that case, you'll need to run the `poetry install` command explicitly to install the dependencies.
 2. By default, executing the `poetry install` command installs dependencies from all non-optional groups. In addition to that, the command also provides you with options to exclude or include groups as per requirements.

You'll not need to install the dependencies specified in the `dev` and `test` environments, because they're not useful for the project to work. Thus, you can use the `--without` option in the `poetry install` command to exclude the `dev` and `test` groups:

~~~{.bash caption=">_"}
poetry install --without dev,test
~~~

If you remember, we covered that the `poetry install` command installs the dependencies from all the non-optional groups. But suppose you've completed the development of the project and want to test the code now, you'll need to install the dependencies specified in the `test` group. But it is inside the `test` group which is optional. In that case, you can use the `--with` option to install the `test` group in addition to the default groups:

~~~{.bash caption=">_"}
poetry install --with test
~~~

The `--without` option takes priority over `--with` when both are used. For example, the following command installs only the dependencies specified in the optional `dev` group:

~~~{.bash caption=">_"}
poetry install --with dev,test --without test
~~~

Think of the situation when you completed the development of the application and now you want to format it. You'll need to install the `dev` group dependencies for that. You can also install only specific dependency groups using the `--only` option:

~~~{.bash caption=">_"}
poetry install --only dev
~~~

Note that the above command will install just the dependencies in the `dev` group and not even the default set of dependencies.

### Writing the Tests

![dev]({{site.images}}{{page.slug}}/write.png)\

To recall, you had created a `get_weather` function to get weather updates for a location. Now that you have installed the testing environment dependencies, you can write the code to test the functionality of your application.

Create a `test_weather.py` file inside the `tests` package and add the following content:

~~~{.python caption="test_weather.py"}
# test_weather.py

import requests_mock
import pytest

from src.weather_update.weather import get_api_key, get_weather

# Global variable for the configuration file
CONFIG_FILE = "config.ini"
API_KEY = get_api_key()

def test_get_weather():
    # create a mock response for the API call
    with requests_mock.Mocker() as mock:
        mock.get(
            f"http://api.openweathermap.org/data/2.5/weather?q=London&appid={API_KEY}&units=metric",
            json={
                "weather": [{"description": "cloudy"}],
                "main": {"temp": 15.0}
            }
        )

        # test the get_weather function
        weather = get_weather("London")
        assert weather == {
            "weather": [{"description": "cloudy"}],
            "main": {"temp": 15.0}
        }

def test_get_weather_failure():
    # create a mock response for the API call to return a failure
    with requests_mock.Mocker() as mock:
        mock.get(
            f"http://api.openweathermap.org/data/2.5/weather?q=London&appid={API_KEY}&units=metric",
            status_code=400
        )

        # test the get_weather function
        with pytest.raises(Exception):
            get_weather("London")
~~~

The code tests the functionality of the `get_weather` function from the `weather.py` file. The `test_get_weather` test case uses the `requests-mock` library to create a mock response for the API call to the OpenWeatherMap API and tests the `get_weather` function to check if it returns the expected response.

The `test_get_weather_failure` test case creates a mock response to return a failure status code and tests the `get_weather` function to see if it raises an exception as expected.

In both test cases, the API key is obtained from the `get_api_key` function and used in the URL for the API call. The test cases run by pytest will determine if the `get_weather` function is working correctly, by comparing the actual results to the expected results. You can add more test cases or modify the existing ones to test the application logic more thoroughly.

Poetry provides a `run` command to execute the given command inside the project's virtual environment. Thus, execute the following command to run the tests:

~~~{.bash caption=">_"}
poetry run pytest
~~~

It is important to execute the `pytest` command inside the virtual environment because you'll need to use the testing dependencies.

Output:

~~~{ caption="Output"}
======================== test session starts ====================
platform darwin -- Python 3.9.16, pytest-7.2.1, pluggy-1.0.0
rootdir: /Users/ashutoshkrris/Projects/test/weather-update
plugins: requests-mock-1.10.0
collected 2 items

tests/test_weather.py .. [100%]

======================== 2 passed in 0.10s ====================
~~~

### Synchronizing Dependencies

Dependency synchronization ensures that only the dependencies specified in the `poetry.lock` file are present in the environment by removing any unnecessary dependencies.
For example, your current `poetry.lock` file might look something like [this](https://github.com/ashutoshkrris/weather-update/blob/546e3492e9fd9cc93fb7bd1575611be816f1d436/poetry.lock). But if in any condition, your virtual environment contains dependencies that are not locked in the `poetry.lock` file, the synchronization will remove extra dependencies.
You can use the `--sync` option with the `poetry install` command to synchronize the dependencies:

~~~{.bash caption=">_"}
poetry install --sync
~~~

You can use the `--sync` option with the other dependency group-related options such as `--with`, `--without`, and `--only`:

~~~{.bash caption=">_"}
poetry install --without dev --sync
poetry install --with dev --sync
poetry install --only dev --sync
~~~

## Publishing a Package

Your project at this stage will look like [this](https://github.com/ashutoshkrris/weather-update). You can copy the contents of the README file from [GitHub](https://github.com/ashutoshkrris/weather-update/blob/main/README.md). Now that you have created your library, you can publish it online for others to install. Poetry provides an easy and efficient way to publish a package by using the `publish` command.

But before you can publish your library, you will need to package it using the `build` command:

~~~{.bash caption=">_"}
poetry build
~~~

Output:

~~~{ caption="Output"}
Building weather-update (0.1.0)
  - Building sdist
  - Built weather-update-0.1.0.tar.gz
  - Building wheel
  - Built weather_update-0.1.0-py3-none-any.whl
~~~

Packaging a project before publishing it is important because it makes the project easier to distribute, install, and use for others. Poetry uses the information specified in the `pyproject.toml` file, such as the project name, version, and dependencies, to package the project in two different formats: `sdist` and `wheel`. Wheel distributions are pre-compiled [packages](/blog/setup-typescript-monorepo) that can be installed quickly, while source distributions contain the raw source code and require compilation.

Next, you have to [configure your PyPI credentials](https://python-poetry.org/docs/repositories/#configuring-credentials) properly as Poetry will publish the library to PyPI by default.

Once you have packaged your library, you can publish it using the `publish` command:

~~~{.bash caption=">_"}
poetry publish
~~~

The command will publish the package to the Python Package Index (PyPI), making them available for installation through Poetry.
After publishing the package, you can search for it on PyPI. For example, you can find the `weather-update` library [PYPI](https://pypi.org/project/weather-update/). You can then install it on your system and try using it.

## Conclusion

Managing dependencies is crucial in Python development. Poetry provides an efficient solution for this. This tutorial covered using Poetry for Python projects, including installation, managing dependencies, and publishing a package. You've learned about virtual environments, adding, removing, and synchronizing dependencies, and packaging Python project.

If you've breezed through managing Python dependencies with Poetry and are looking for ways to further streamline your build process, you might want to take it up a notch with [Earthly](https://www.earthly.dev/). It's a tool that can make your builds even smoother. Check it out!

{% include_html cta/bottom-cta.html %}
