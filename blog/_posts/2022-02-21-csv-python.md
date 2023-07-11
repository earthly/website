---
title: "How To Read A CSV File In Python"
categories:
  - Tutorials
toc: true
author: Kelly Moreira

internal-links:
 - python csv
 - csv read
topic: python
last_modified_at: 2023-04-17
excerpt: |
    Learn how to read a CSV file in Python using both the `csv` and `pandas` libraries. Discover the different methods and possible delimiter issues, and find out how to overcome them.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about reading a CSV file in Python. Earthly is a popular choice for users who want to simplify and speed up their software building process using containerization. [Check us out](/).**

<iframe width="560" height="315" src="https://www.youtube.com/embed/H-hagjt65cE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster. If you're interested in a simple and containerized approach to building Python code then [check us out](/).**

## What Is A CSV File

I first began to work with CSV files when taking the backend portion of my software engineering bootcamp curriculum. It wasn't until I began to dive more into the data science portion of my continued learning that I began to use them on a regular basis.

CSV stands for comma-separated values, and files containing the `.csv` extension contain a collection of comma-separated values used to store data.

In this tutorial we will be using the public `Beach Water Quality` data set stored in the `bwq.csv` file. You can obtain the file by downloading it from [Kaggle](https://raw.githubusercontent.com/adamgordonbell/python-examples/main/readcsv/bwq.csv), however, you should be able to read any csv file following the instructions below.

## Read A CSV File Using Python

There are two common ways to read a `.csv` file when using Python. The first by using the `csv` library, and the second by using the `pandas` library.

### 1. Using the CSV Library

~~~{.python caption=""}
import csv

with open("./bwq.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
    print(row)
~~~

Here we are importing the `csv` library in order to use the `.reader()` method it contains to help us read the `csv` file.

The `with` keyword allows us to both open and close the file without having to explicitly close it.

The `open()` method takes two arguments of type `string`. First the file name, and second a mode argument. We are using `r` for read, however this can be omitted as `r` is assumed by default.

We then iterate over all the rows.

You should expect an output in the terminal to look something like this:

![Python Terminal Output]({{site.images}}{{page.slug}}/2370.png)

### 2. Using the Pandas Library

~~~{.python caption=""}
import pandas as pd
data = pd.read_csv("bwq.csv")
data
~~~

Here we're importing Pandas, a Python library used to conduct data manipulation and analysis. It contains the `.read_csv()` method we need in order to read our `csv` file.

You should expect the output to look something like this:

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/2440.png --alt {{ jupyter notebook output of code snippet }} %}
<figcaption></figcaption>
</div>

## Possible Delimiters Issues

The majority of `csv` files are separated by commas, however, there are some that are separated by other characters, like colons for example, which can output strange results in Python.

### Solution For Delimiters Using the CSV Library

To change the delimiter using the `csv` library, simply pass in the `delimiter= ':'` argument in the `reader()` method like so:

~~~{.python caption=""}
import csv

with open("./fileWithColonDelimeter.csv", 'r') as file:
  csvreader = csv.reader(file, delimiter=':')
  for row in csvreader:
    print(row)
~~~

For other edge cases in reading `csv` files using the `csv` library, check out [this page](https://docs.python.org/3/library/csv.html) in the Python docs.

### Solution For Delimiters Using the Pandas Library

To change the delimiter using the `pandas` library, simply pass in the argument `delimiter= ':'` in the `read_csv()` method like so:

~~~{.python caption=""}
import pandas as pd
data = pd.read_csv("fileWithColonDelimeter.csv", delimiter= ':')
data
~~~

 For other edge cases in reading `csv` files using the Pandas library check out [this page](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html) the Pandas docs.

## Up Next

[Better Dependency Management in Python](/blog/python-earthly/) is a great introduction to using Earthly with Python and if you want to bring your CI to the next level, check out [Earthly's open source build tool](/).

{% include_html cta/bottom-cta.html %}