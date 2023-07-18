---
title: "Introduction to Pyscript"
categories:
  - Tutorials
toc: true
author: Ukeje Goodness
excerpt: |
    Learn how to use PyScript, a Python-based front-end web framework, to build powerful browser applications using an HTML interface. Discover its features, such as browser support, ecosystem support, Python-Javascript interoperability, and flexibility, and see how you can run Python code in HTML, import files and libraries, and visualize data and images in the browser. Whether you're a beginner or an expert, PyScript offers a user-friendly experience for creating web applications with Python.
internal-links:
 - Pyhton
 - Numpy
 - PyScript
 - Pyodide
 - Django
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and faster using containerization. Earthly can help streamline your builds and amplify your productivity. [Give us a try](/).**

<div class="wide">

<img src="{{site.images}}{{page.slug}}/image 1.png" alt="Pyscript header image">

</div>

### Introduction

Python is widely used in so many applications, from data science to machine learning, robotics, and artificial intelligence.

On the web, python is mainly used for backend development, using frameworks such as Flask and Django.

Since the [World Wide Web Consortium(W3C) announced web assembly](https://www.w3.org/2019/12/pressrelease-wasm-rec.html.en#:~:text=https%3A%2F%2Fwww.w3.org,for%20efficient%20execution%20and%20compact) specifications as an official web standard, developers of various languages have seemed to support their favorite language on the Web, with Python developers having Pyodide to their rescue.

On the 30th of April 2022, ****Anaconda, a company widely known for its data science products in Python and R programming languages, announced that it had just released a framework that would help users create python applications using HTML.

This publication will help you get started writing PyScript, a JSFiddle-like Python framework.

### Prerequisites

To follow this tutorial, you'll need to meet these requirements.

- Knowledge of working with HTML.
- A text editor or IDE of your choice.

## What Is PyScript

<img src="{{site.images}}{{page.slug}}/what.jpg" width="80%" height="60%">

PyScript is a Python-based front-end web framework for building powerful browser applications in Python using an HTML interface.

PyScript delivers Python developers uniform style conventions, expressiveness, and ease of use for building web applications by providing support for the following:

- **Browser support**: Python Developers can manage content generated in programs and host external files and apps without servers.
- **Ecosystem support**: Python Developers can easily use their favorite Python packages, including the scientific stack (data science packages and libraries) with PyScript.
- **Python** **-** **Javascript Interoperability**: Programs can communicate synergically(two-way) using Python and Javascript objects and namespace.
- **Flexibility**: Developers may define specific packages and files, use selected UI components for visuals, and create new components and plugins.

PyScript was developed using Pyodide, WebAssembly to offer clean APIs to support, and extend standard HTML.

Underneath the scenes, PyScript runs as WASM and isn't designed to replace Javascript in the browser but to give Python developers, especially data scientists, more power and flexibility.

## Getting Started With PyScript

PyScript is easy to use and very intuitive. To get started, you can [download the required files](https://github.com/pyscript/pyscript/archive/refs/heads/main.zip) or use them by following the instructions on the [website](http://pyscript.net).

In this tutorial, you will be learning how to use PyScript via [the website](http://pyscript.net)(linking the components to your HTML file); however, if you want to use PyScript in production, you should host it yourself for speed.

### Step1: Create an HTML File

Create a HTML file and fill the code as you normally would, to display text in your browser.

~~~{.bash caption=">_"}
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>

</body>
</html>
~~~

### Step2:  Add These Lines to Your Html

Since you are using PyScript from the pyscript website, all you have to do is include these lines in your HTML before the closing head tag.

~~~{.bash caption=">_"}
<link rel="stylesheet" href="https://pyscript.net/alpha/pyscript.css"/>
<script defer src="https://pyscript.net/alpha/pyscript.js"></script>
~~~

You can now use the CSS and Javascript files from the PyScript repository in your page.

~~~{.bash caption=">_"}
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
<link rel="stylesheet" href="https://pyscript.net/alpha/pyscript.css"/>
<script defer src="https://pyscript.net/alpha/pyscript.js"></script>
</head>
<body>

</body>
</html>
~~~

## Running Python Code in HTML

PyScript allows you to run Python code in HTML using the `<py-script>` tag in the body of your HTML. Just like most HTML Tags, all PyScript tags have opening and closing tags `<py-script> <py-script>`.

Write Python code in the `<py-script>` tags and view the code in your browser for results.

![The string in the print statement is output to the browser as regular text]({{site.images}}{{page.slug}}/carbon_(1).png)

### Passing Python Code Variables to HTML

As you use PyScript, you might want to pass variables from your python program to your regular HTML code. PyScript provides a `write` method providing functionality for passing strings.

~~~{.bash caption=">_"}
<h3>Testing <label id='name'></label></h3>

<py-script>
    name = "PyScript";
    pyscript.write("name", name)
</py-script>
~~~

Using an `id`, you get to pass strings displayed as regular text.

`pyscript.write` accepts the id value and the variable to be given.

![Testing Pyscript]({{site.images}}{{page.slug}}/image 3.png)\

## Importing Files, Modules, and Libraries

One of the main features of PyScript is that you can use Python files, modules, and libraries.

For modules and libraries in the Python standard library, you can import and use them in the `<py-script>` tags.

~~~{.bash caption=">_"}
<py-script>
    import string
    name = "Human"
    print(string.ascii_uppercase)
</py-script>
~~~

PyScript also supports a wide range of modules and libraries that are not part of the standard library.

You can use third-party packages by specifying them in the `<py-env>` tag and listing the names as shown below.

~~~{.bash caption=">_"}
<py-env>
        - requests
        - beautifulsoup4
</py-env>

<body>
<py-script>
    from requests import *
    from bs4 import BeautifulSoup
</py-script>
</body>
~~~

The code snippet above specifies you want to use the requests and beautifulsoup libraries, after which you import them in the `<py-script>` tag.

Ensure that you do not use the `<py-env>` tag in the body of your HTML; use above the `<body>` tag.

If you have a Python file or module in that you want to use in your HTML, you can import it by specifying the path as thus.

~~~{.bash caption=">_"}
<py-env>
- paths:
    - /main.py
</py-env>
~~~

Paths are relative to the HTML location and You can now import functions and methods and use them in the HTML using the `<py-script>` tags.

PyScript reads

## Running Python Code in Browser

PyScript also provides [functionality for running Python code REPL in browsers](https://pyscript.net/examples/repl.html). To run a Python REPL on your browser, you use the `<py-repl`> tag.

~~~{.bash caption=">_"}
<py-repl id="my-repl" auto-generate=true> </py-repl>
~~~

This creates a REPL text area in your browser in which you can type and run Python code whose output is displayed in the browser.

![Testing]({{site.images}}{{page.slug}}/image 4.png)\

## Image and Data Visualization In-Browser using PyScript

The most powerful use of PyScript comes is the ease of image and data visualization in the browser using raw Python. Data analysts can now visualize data plotted with libraries like Seaborn and [Matplotlib](/blog/python-matplotlib-docker), unlike in the past when the image had to be saved locally to be displayed.

Let's see how a Matplotlib plot in PyScript can be used to visualize data and images in the browser easily.

~~~{.bash caption=">_"}
<py-env>
      - numpy
      - matplotlib
</py-env>

<body>
<py-script>
    import matplotlib.pyplot as plt
 import numpy as np

 x_coordinates = np.random.randn(100)
 y_coordinates = np.random.randn(100)
 figure, axis = plt.subplots()
 axis.scatter(x_coordinates ,y_coordinates)
 figure
</py-script>
</body>
~~~

![Testing Board]({{site.images}}{{page.slug}}/image 5.png)\

We started by importing the NumPy and [Matplotlib](/blog/plotting-rainfall-data-with-python-and-matplotlib) libraries which are popularly used for scientific computing in Python; then, we assigned two variables `x_coordinates` and `y_coordinates`, to `np.random.randn` which created NumPy arrays of normally distributed numbers.

The `figure` and `axis` variables to `plt.subplots` set the figure and axis on the graph, `axis.scatter` plots the NumPy arrays on the figure, which is displayed by passing the variable on a new line in the `<py-script>` tag.

## PyScript or Pyodide

![Pyodide Logo]({{site.images}}{{page.slug}}/image 6.png)\

Pyodide is an open-source project developed by Mozilla using Web Assembly that allows Python developers to run Python in the browser.

Unlike PyScript, which abstracts developers from everything else and empowers pure python code in HTML, Pyodide is a port of CPython to WebAssembly that provides more functionality.

Some features of Pyodide include:

1. Ability to use all Python packages with a Wheel on Pypi using micropip

2. Functionality to use packages with C extensions, including the scientific stack.
3. Functionality to mix Python and Javascript code in programs with support for error handling and efficiency.

4. Functionality to use Web APIs easily.

### Comparing Pyscript To Pyodide

| Metric | Pyscript | Pyodide |
| --- | --- | --- |
| Javascript Interoperability | One way (Python - Javascript only) | Two way |
| Experience | Beginner Friendly | Expert knowledge is required |
| Web API functionality | Simply API provision | Flexible, Powerful API provision |

So, as you can see, Pyscript is great to get started, but if you need to use C-based packages or have performance issues, you may want to take a look at Pyodide.

PyScript was built using Pyodide, Web assembly, and Emscripten allowing PyScript to inherit important features from Pyodide while simplifying functionality to run Python in the browser.

Pyodide would be a more suitable option if you're building performance-intensive applications, especially machine learning-related applications.

Learn more about PyScript and Pyodide from these resources.

- [The PyScript website.](https://pyscript.net/)
- [The Pyodide official documentation.](https://pyodide.org/en/stable/usage/index.html)
- [PyScript Examples](https://pyscript.net/examples/)

### Conclusion

In this tutorial, we've explored PyScript, a tool that allows running Python code in HTML with functionalities like external packages, Python REPLs, and visualization of Python-generated images in a browser. PyScript, an alpha stage tool, makes it easier to use Python scripts in HTML and its scientific stack on the client side, though it's not yet production-ready.

As you continue to build your PyScript apps, consider boosting your build efficiency with [Earthly](https://www.earthly.dev/), your new favorite tool for reproducible builds. Earthly can be a game-changer in ensuring consistent and reliable results in your development process.

{% include_html cta/bottom-cta.html %}
