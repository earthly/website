---
title: "How to use PyInstaller"
categories:
  - Tutorials
toc: true
author: Vivek Kumar Maskara

internal-links:
 - create a python virtual environment with pyinstaller
 - pyinstaller for creating virtual environment
 - creating a python virtual environment
 - creating a virtual environment with pyinstaller 
excerpt: |
    This tutorial explains how to create a Python virtual environment using PyInstaller, a packaging tool for Python applications, and distribute them across different operating systems. PyInstaller analyzes dependencies, bundles the application and its dependencies into a single package, and generates an executable file that can be easily shared and run without installing Python separately.
---
If your Python application depends on specific packages, these dependencies must be installed before running the application. However, managing dependencies within a Python application can quickly become complicated, necessitating compatibility checks across various Python versions, resolution of dependency conflicts, and negotiation of platform-specific requirements.

Before you can run an application, you must install a precise Python version, configure [pip](https://pypi.org/project/pip/) for package installation, establish a [virtual environment](https://docs.python.org/3/tutorial/venv.html) to isolate dependencies, and install the application's package dependencies. These tasks demand a nuanced comprehension of Python's development ecosystem and can present challenges when distributing the application to non-developer systems.

To simplify the distribution of Python apps to different operating systems, you can use [PyInstaller](https://pyinstaller.org/en/stable/usage.html), a packaging tool for Python applications. PyInstaller analyzes dependencies for the Python application and bundles the application and its dependencies into a single package, making it easier for users to install and run without installing Python separately.

In this article, you'll learn how to create a virtual environment using PyInstaller, install applications on that virtual environment, and distribute them with PyInstaller.

## What Is PyInstaller?

PyInstaller supports Python version 3.8 or newer and works for Windows, Mac, and Linux operating systems (OSs). If you want to generate a packaged app for an OS, you need to run PyInstaller on that OS, as it doesn't support cross-compilations.

To bundle an application, PyInstaller examines your Python code, identifies its dependencies, and subsequently bundles them into the appropriate format. For more information on how PyInstaller analyzes the Python program to identify other modules and libraries, check out the [documentation](https://pyinstaller.org/en/stable/operating-mode.html#analysis-finding-the-files-your-program-needs).

PyInstaller simplifies the distribution of Python applications by creating standalone executables. This means you can easily share your command line interface (CLI) tools or applications, including your dependencies, with users who don't have Python installed. For example, if you have a CLI that fetches the top news stories of the day and displays their summaries, it can be packaged using PyInstaller and distributed across platforms, ensuring a consistent user experience.

PyInstaller can also handle application dependencies like external libraries (*eg* NumPy or Matplotlib) and modules. It also converts Python code into executable binaries, enhancing code security and making it harder for users to reverse engineer or modify your application. This feature is particularly useful for commercial or proprietary projects.

PyInstaller reads your Python script and analyzes its code to discover every module and library that your script depends on. It copies all the files (including the active Python interpreter) to a single folder or generates a single executable file based on the options passed.

## Using a Python Virtual Environment with PyInstaller

In this tutorial, you'll create a Python application and use PyInstaller to generate an executable.

To start, create a new directory for your Python project by executing the following command in your terminal:

~~~{.bash caption=">_"}
mkdir pyinstaller_sample
~~~

### Creating a Virtual Environment

[`virtualenv`](https://virtualenv.pypa.io/en/latest/) lets you create a virtual environment to isolate Python packages in separate directories. Execute the following command in your terminal to install `virtualenv` using [pip](http://www.pip-installer.org/):

~~~{.bash caption=">_"}
pip install virtualenv
~~~

Then, create a new virtual environment named `myenv` using the following command:

~~~{.bash caption=">_"}
cd pyinstaller_sample
virtualenv myenv
~~~

This creates a folder named `myenv` in the `pyinstaller_sample` directory.

Execute the following command to activate the virtual environment:

~~~{.bash caption=">_"}
source myenv/bin/activate
~~~

Any subsequent Python or pip commands will also be executed in this environment.

### Installing PyInstaller and Creating a Python Application

If you use `pip`, PyInstaller can be installed just like any other Python package from [PyPI](https://pypi.org/project/pyinstaller/). Execute the following command to install PyInstaller:

~~~{.bash caption=">_"}
pip install pyinstaller
~~~

This command installs the `pyinstaller` package in the `myenv` virtual environment since it's currently active.

For this tutorial, you need to create a simple Python script that generates a random number based on the maximum number input by the user. You can use the [numpy](https://numpy.org/install/) Python package to generate a random number. Execute the following command to install numpy:

~~~{.bash caption=">_"}
pip install numpy
~~~

Next, create an `app.py` file in the `pyinstaller_sample` directory and add the following code:

~~~{.python caption="app.py"}
import numpy as np

def generate_random_number(max_number):
    return np.random.randint(1, max_number)

if __name__ == "__main__":
    max_number = int(input("Enter the maximum allowed number: "))
    random_number = generate_random_number(max_number)
    print("Random number:", random_number)
~~~

This script lets the user input `max_number` and uses the `numpy.random.randint` function to return a random number between `1` and `max_number`.

### Creating the dist Package and Executable

When you run PyInstaller, it analyzes the script, collects the required modules, builds the packages, and generates the executable file for the current OS. To create a dist package and executable, navigate to the `pyinstaller_sample` directory and execute the following command:

~~~{.bash caption=">_"}
pyinstaller app.py --paths myenv/lib/python3.9/site-packages
~~~

The `--paths` parameter specifies where PyInstaller should look for package dependencies. This example specifies the path of the virtual environment. Your output should look something like this:

~~~{.bash caption=">_"}
153 INFO: PyInstaller: 6.5.0, contrib hooks: 2024.3
153 INFO: Python: 3.9.12 (conda)
160 INFO: Platform: macOS-14.4.1-arm64-arm-64bit
161 INFO: wrote /Users/vivekmaskara/pyinstaller_sample_app/app.spec
---OUTPUT OMITTED---
2031 INFO: Building EXE from EXE-00.toc completed successfully.
2032 INFO: checking COLLECT
2032 INFO: Building COLLECT because COLLECT-00.toc is non existent
2032 INFO: Building COLLECT COLLECT-00.toc
2241 INFO: Building COLLECT COLLECT-00.toc completed successfully.
~~~

Here, you've generated `build` and `dist` directories and a [`.spec` file](https://pyinstaller.org/en/stable/spec-files.html). At this point, your directory structure should look like this:

~~~{. caption=""}
├── pyinstaller_sample
│   ├── build
│   │   ├── app
│   ├── dist
│   │   ├── app 
│   │   │   ├── _internal
│   │   ├── app (executable file)
│   ├── app.py
│   ├── app.spec
~~~

The `.spec` file tells PyInstaller how to process the script. The name of the `.spec` file is based on your Python script's file name. It encodes the names of the scripts and the parameters provided to the `pyinstaller` command.

The `build` directory contains most of the metadata and internal tasks required to compile your executable using PyInstaller. It's also helpful for debugging if the generated application does not work as expected.

The `dist` directory contains the bundled executable you can distribute to your users. Inside the `dist` directory is an `app` directory named after your Python script.

### Testing the Executable

If you want to test the executable, navigate to the `dist/app` directory through the terminal and run the `app` executable using the following commands:

~~~{.bash caption=">_"}
cd dist/app
./app
~~~

Executing the application displays a prompt to enter the maximum number allowed, and you can enter a maximum number to generate a random number within that range:

~~~{.bash caption=">_"}
Enter the maximum allowed number: 1000
Random number: 384
~~~

> **Note:** You can also execute the application by opening the `dist/app` folder in your OS file system and double-clicking the `app` executable file to start it.

## PyInstaller Configuration Options

PyInstaller offers various configuration options to customize the output of the executable, including the `--name`, `--onefile`, `--hidden-import`, and `--exclude-module` parameters.

### The `--name` Argument

If you want to customize the name of the artifacts and the `.spec` file, you can specify the `--name` parameter:

~~~{.bash caption=">_"}
pyinstaller app.py --name randomGen
~~~

This command generates a `randomGen.spec` file along with `randomGen` directories under `build` and `dist`.

If the `--name` option is not specified, the artifacts and `.spec` file names will match the name of the Python script.

### The `--onefile` Argument

The `--onefile` configuration option instructs PyInstaller to generate an executable file without a folder with dependencies:

~~~{.bash caption=">_"}
pyinstaller app.py --onefile
~~~

Executing this command generates a `dist/app` executable file.

### The `--hidden-import` Argument

Sometimes, PyInstaller's analysis phase cannot detect all the imports. For instance, if your code uses `__import__()` or `importlib.import_module()` to import a module, PyInstaller cannot detect this import. In such cases, you can use the [`--hidden-import` option](https://pyinstaller.org/en/stable/when-things-go-wrong.html#listing-hidden-imports) to tell PyInstaller about the hidden imports.

For example, if your application uses the `requests` Python package and PyInstaller was unable to detect it, you could fix the issue like this:

~~~{.bash caption=">_"}
pyinstaller app.py --hidden-import=requests
~~~

You can use the `--hidden-import` parameter multiple times in the same command if you want to include multiple dependencies.

### The `--exclude-module` Argument

The `--exclude-module` command lets you exclude specific dependencies from being packaged with the executable. For example, you could use this option to exclude developer-only dependencies such as `pytest`:

~~~{.bash caption=">_"}
pyinstaller app.py --exclude-module=pytest
~~~

## Packaging and Distributing the Executable

If you want to allow others to run your application, you must distribute the entire `dist/app` folder. This folder contains the application's dependencies and an executable file with the same name (*ie* `app`). To better convey the purpose of the application, you can rename `app` to a more descriptive name, such as `randomGenerator`.

If you used the `--onefile` option while generating the executable, the `dist` folder includes a single executable file instead of an `app` folder with dependencies. You can compress this `dist/app` directory as a ZIP and share it with others.

As previously mentioned, PyInstaller doesn't support cross-compilation, so you must ensure that the target machine runs the same OS as the one used to compile the application. For example, if you need to support Windows, Linux, and Mac operating systems, you need to compile your application separately on each platform. You can utilize virtualization to do this on a single device using software such as [VirtualBox](https://www.virtualbox.org/), [VMware](https://www.vmware.com/solutions/anywhere-workspace.html), or [Parallels](https://www.parallels.com/). On a virtual machine, all you need to do is install Python, the support packages, and PyInstaller, and then you can use it to bundle your application.

All the code used in this tutorial is available on [GitHub](https://github.com/maskaravivek/pyinstaller_sample_app).

### Limitations of PyInstaller

While PyInstaller has many advantages, it doesn't handle system-level dependencies, which can lead to compatibility issues for applications that depend on non-Python dependencies. For example, users may encounter runtime errors if your application requires specific system libraries or external tools not included in the bundled package. To address this, you may need to configure PyInstaller manually or provide additional instructions to ensure all dependencies are properly bundled.

Additionally, bundled executables can be large and include numerous dependencies and resource files, impacting storage requirements and download times. To mitigate these issues, you could consider containerizing the application using Docker or a similar technology. However, users would need to follow manual setup steps to run a containerized application locally.

[Earthly](https://earthly.dev/) is a build framework that lets you make consistent builds that you write once and run everywhere. It can address these pain points by helping manage system-level dependencies along with Python dependencies. For more information on how you can integrate Earthly with your Python project, check out [this article](https://earthly.dev/blog/python-earthly/).

## Conclusion

This tutorial showed you how to use [PyInstaller](https://pyinstaller.org/en/stable/) to package and distribute a Python application with dependencies across multiple platforms. PyInstaller analyzes Python scripts, bundles the Python interpreter along with the required packages, and generates an executable file that can be run on other devices without setting up a Python environment. While this solution works well for simple applications, if you have system dependencies, you'll probably run into compatibility issues.

Thankfully, [Earthly](https://earthly.dev/) can help. It enables developers to easily create reproducible builds for their projects, ensuring reliability and consistency across different environments. If this sounds too good to be true, [try Earthly out for free](https://cloud.earthly.dev/login) and get started streamlining your builds and releases for your Python applications.

{% include_html cta/bottom-cta.html %}
