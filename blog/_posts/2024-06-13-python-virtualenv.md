---
title: "How to Create a Python Virtual Environment with virtualenv"
toc: true
author: Michael Nyamande

internal-links:
 - create a python virtual environment
 - how to create a python virtual environment with virtualenv
 - create a python virtual environment with virtualenv
 - python virtual environment with virtualenv
 - virtualenv to create a python virtual environment
categories:
  - python-tooling
  - python
---

Managing dependencies for multiple projects is a common challenge for developers, particularly in Python, where all dependencies are installed globally by default. Imagine working on multiple projects, each requiring different versions of the same library or even different versions of Python. If not properly isolated, these dependencies may clash, causing various problems and wasting valuable project time debugging the issues.

Thankfully, virtual environments can help. Virtual environments allow you to create dedicated environments for your projects, ensuring that each project has its own set of isolated dependencies that don't interfere with other projects.

In this article, you'll learn about Python virtual environments and why they're important. You'll also learn how to create and manage virtual environments using [virtualenv](https://virtualenv.pypa.io/).

## What Is a Virtual Environment?

![Virtual]({{site.images}}{{page.slug}}/virt.png)\

In Python, a virtual environment is an isolated environment that allows you to install and manage packages independently from the global Python installation. This isolation is beneficial for several reasons, as you can:

- **Avoid dependency conflicts:** Different projects can depend on different versions of the same package. For example, one project might require Flask 3.0, while another needs Flask 2.0. Virtual environments ensure that each project uses the correct version of its dependencies without affecting others.
- **Reproduce environments:** By isolating dependencies, you can ensure that your project will run the same way on any machine, as long as the virtual environment is recreated properly. This makes it easier to collaborate on projects since you can easily share your environment with teammates.
- **Use different Python versions:** You can use virtual environments to work with multiple Python versions on the same machine. This is especially useful for testing code compatibility.
- **More easily test and debug:** With virtual environments, you can quickly switch between different environments to test how your code behaves with different sets of dependencies or configurations. For example, when your favorite web framework releases a new version, you can easily create a new environment to test for breaking changes before upgrading.

## Virtual Environments Using `virtualenv`

While there are multiple tools available for setting up virtual environments in Python, such as [venv](https://docs.python.org/3/library/venv.html), [Poetry](https://python-poetry.org/), and [conda](https://docs.conda.io/en/latest/), virtualenv is a [popular choice](https://lp.jetbrains.com/python-developers-survey-2022/#PythonPackaging) due to its simplicity, effectiveness, and ability to work seamlessly with older versions of Python. It offers key benefits like dependency isolation (ensuring that each project has its own set of dependencies), reproducibility across different machines, and the ability to manage multiple Python versions.

Let's learn how you can use virtualenv to manage your Python project dependencies.

### Installing virtualenv and Creating a Project

The first thing you need to do is install virtualenv. Since virtualenv is available as a Python package, you can install it using pip:

~~~{.bash caption=">_"}
pip install virtualenv
~~~

Once you've installed virtualenv, you need to create a directory for your new project using the following commands:

~~~{.bash caption=">_"}
mkdir my_project
cd my_project
~~~

This directory serves as the root for your project's files and virtual environment. This step is optional but recommended for better organization.

### Creating a Virtual Environment

To create a virtual environment with virtualenv, run the following command inside your project directory:

~~~{.bash caption=">_"}
virtualenv venv
~~~

Here, `venv` is the name of your virtual environment folder. You can name it anything you like, but `venv` is a common convention.

This step sets up a directory structure that contains its own Python interpreter and a `site-packages` directory where all the dependencies for your project will be installed. This keeps your project's dependencies isolated from other projects.

At times, you may need to create a virtual environment with a specific version of Python. Thankfully, virtualenv allows you to specify which Python interpreter to use. For instance, if you have multiple versions of Python installed, you can select the desired one using `-p` or `--python`, followed by the path to the Python executable.

To create a virtual environment with Python 3.11, use the following command and specify the path to the version of Python you want to use:

~~~{.bash caption=">_"}
virtualenv -p /path/to/python3.11 venv
~~~

Or, if the `python3.11` executable is in your system's PATH, you can simplify it like this:

~~~{.bash caption=">_"}
virtualenv -p python3.11 venv
~~~

This command tells virtualenv to use Python 3.11 to create the virtual environment. The resulting environment has its own Python 3.11 interpreter, along with a separate `site-packages` directory. If you want to learn about other CLI options for virtualenv, check out the [documentation](https://virtualenv.pypa.io/en/latest/cli_interface.html).

### Activating Your Virtual Environment

Once you've created a virtual environment, you need to activate it. Activating the virtual environment modifies your shell's environment variables to use the Python interpreter and libraries from the virtual environment. This ensures that any packages you install and any scripts you run use the isolated environment.

To activate your environment on Windows, use the following command:

~~~{.bash caption=">_"}
venv\Scripts\activate
~~~

On macOS and Linux, use the following:

~~~{.bash caption=">_"}
source venv/bin/activate
~~~

After activation, your command prompt will change to indicate that the virtual environment is active, typically by showing the name of the environment in parentheses, like this: `(venv)`.

### Installing Packages in a Virtual Environment

With the virtual environment active, you can install packages using pip, just as you would globally. For example, the following command shows you how to install [Flask](https://flask.palletsprojects.com/), a popular web framework:

~~~{.bash caption=">_"}
pip install flask
~~~

You can specify a particular version in the install command using the syntax `pip install package==version`. For example, the following command installs version 2.2.5 of Flask:

~~~{.bash caption=">_"}
pip install flask==2.2.5
~~~

This command installs the Flask library within the virtual environment, making it available for your project without affecting the global Python installation.

### Managing and Removing Packages

Managing packages in a virtual environment is crucial for maintaining project consistency. One helpful practice is to use a `requirements.txt` file to keep track of your project's dependencies. You can create this file by running the following:

~~~{.bash caption=">_"}
pip freeze > requirements.txt
~~~

This command lists all installed packages and their versions, saving them to `requirements.txt`. To recreate the environment on another machine or after deleting the environment, you can use the following:

~~~{.bash caption=">_"}
pip install -r requirements.txt
~~~

This ensures that the exact versions of the dependencies are installed, making your project environment reproducible.

When you're done with development and want to stop using the virtual environment, you can deactivate it to restore your shell to its global settings. If you no longer need the environment, you can deactivate it and delete the environment folder. This can be helpful to free up space if you're working on a big project with multiple environments.

To deactivate an environment, you can use the following command:

~~~{.bash caption=">_"}
deactivate
~~~

To delete the environment folder, use the following command:

~~~{.bash caption=">_"}
rm -rf venv
~~~

This removes the virtual environment and all the packages installed within it.

## Limitations of `virtualenv`

![Limitations]({{site.images}}{{page.slug}}/limitations.png)\

While virtualenv is a powerful tool, it has some limitations:

- **System-level dependencies:** virtualenv only isolates Python packages. It does not handle setting up system-level dependencies that some Python packages require. For example, packages like libpng or libfreetype, used in the Matplotlib library, require certain dependencies to be installed separately on the system.
- **Reproducibility across different platforms:** virtualenv does not guarantee reproducibility across different operating systems and hardware platforms. It only simplifies environment reproducibility when you're not dealing with system- or platform-specific dependencies.
- **Integration with CI/CD pipelines:** While virtualenv is great for working locally, it fails to seamlessly integrate with CI/CD pipelines. Ensuring the CI/CD environment matches the local development setup requires additional configuration and management.

[Earthly](https://earthly.dev/) is a CI/CD framework that allows you to build, test, and deploy your projects consistently across different environments. It excels at sandboxing system-level dependencies, ensuring your projects can run anywhere without the typical "it works on my machine" issues. By leveraging Earthly, you can overcome the limitations of virtualenv to ensure that both Python and system-level dependencies are managed efficiently, leading to more stable and reproducible builds.

Here's how Earthly works:

- **It defines dependencies in an Earthfile:** Earthly allows you to define all your dependencies, including system-level ones, in an [Earthfile](https://docs.earthly.dev/docs/earthfile). This ensures a consistent setup across different machines.
- **It builds consistent environments:** Earthly uses containerization to build environments, ensuring all dependencies are properly isolated and consistent.
- **It integrates with CI/CD pipelines:** Earthly integrates seamlessly with CI/CD pipelines, allowing you to automate your workflows and run your builds, tests, and deployments in a consistent environment. This integration ensures that your application behaves the same throughout the development lifecycle.

The following is an example of an Earthfile for a Flask web app project. This setup installs both system-level and Python dependencies:

~~~{.dockerfile caption="Earthfile"}
# Use a specific Python version
FROM python:3.8
WORKDIR /app

# Install system-level dependencies
deps:
    RUN apt-get update && apt-get install -y libpq-dev

    # Install Python packages
    COPY requirements.txt .
    RUN pip install -r requirements.txt

    # Copy the project files
    COPY . .

# Run unit tests
test:
    FROM +deps
    RUN python -m unittest discover

# Build the target and start the application
docker:
  ENV FLASK_APP=src/app.py
  ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--port=3000"]
  SAVE IMAGE my-python-app:latest
~~~

For more details on using Earthly with Python, check out [this Earthly blog post](https://earthly.dev/blog/python-earthly/).

## Conclusion

In this article, you learned how to create and manage Python virtual environments using virtualenv. Virtual environments are essential for maintaining clean and conflict-free project dependencies, and virtualenv makes this process straightforward. You also explored some limitations of virtualenv and how [Earthly](https://earthly.dev/) can help manage system-level dependencies and create reproducible environments.

By mastering these tools, you can ensure that your Python projects are well organized and free from dependency conflicts, allowing you to focus on what matters most: writing great code.

{% include_html cta/bottom-cta.html %}
