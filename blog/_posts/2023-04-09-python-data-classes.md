---
title: "Getting Started with Python Data Classes"
categories:
  - Tutorials
toc: true
author: Bala Priya C

internal-links:
 - Python
 - Python Classes
---

In Python, classes let you group together data and behavior by defining attributes and methods, respectively. Typically, a class contains both attributes and a set of methods that add functionality. But what if you have a class that stores—a lot of attributes—with almost no functionality? Do you still need to use regular classes, or is there a better alternative? 

**Data classes**, first introduced in Python 3.7, provide a convenient way of defining and managing such **data-oriented classes** (who would've guessed!).

**If you already have a Python class that exposes a lot of methods, you don't need a data class**. However, if you’re interested in learning about this new feature to manage your data-oriented classes better, then this tutorial is for you.

You’ll learn the basics of data classes and how they’re different from regular Python classes. In addition, you’ll learn how data classes support type hints, default values beyond basic data types, immutability, and more.

Let’s get started!

<div class="notice--big--primary">
#### 📑 Before You Begin

To follow along, you need [Python 3.7 or a later version](https://www.python.org/downloads/) installed in your preferred development environment. You can find the code examples used here in [this GitHub repository](https://github.com/balapriyac/dataclasses-tutorial).
  
This tutorial assumes you’re familiar with the working of [Python classes and objects](https://earthly.dev/blog/how-cls-obj-work-python/).
  
</div>

## Python Classes and Boilerplate Code

You’ll first create a regular [Python class](https://earthly.dev/blog/how-cls-obj-work-python/). In doing so, you'll realize how much bolierplate code you need to write to get a minimal working class. You'll then rewrite the existing Python class as a *data class* to understand how data classes can help you escape the monotony of boilerplate code.

As our goal is to *understand and use* data classes—and not to write fancy classes—let's create a simple class such as a `Student` or an `Employee` class.

So `Student` or `Employee`? 

![student-vs-employee-class]({{site.images}}{{page.slug}}/5.png)\

I’ll choose `Student` class for now. Let's get coding!

### The `__init__()` Method

Let’s create a `Student` class with the attributes: `name`, `roll_no`, `major`, and `year`. To initialize instances of the `Student` class by passing in values for these attributes in the constructor, you can define the `__init__()` method:

~~~{.python caption="main.py"}
# main.py
class Student:
    def __init__(self, name, roll_no, major, year):
        self.name = name
        self.roll_no = roll_no
        self.major = major
        self.year = year
~~~

Now that you’ve created the `Student` class, start a Python REPL, import the `Student` class, and create a student object `jane`:

~~~{.python caption=""}
>>> from main import Student
>>> jane = Student('Jane','CS1234','Computer Science','junior')
~~~

You inspect this object `jane` at the REPL: 

~~~{.python caption=""}
>>> jane
<main.Student object at 0x007EE628>
~~~

As seen, the default representation returned `<main.Student object at 0x007EE628>` is not very helpful; it does *not* contain any information on the attributes of the instance `jane`. If you need a helpful string representation of the object, you should implement the `__repr__()` method. 

### Adding a Helpful `__repr__()`

After adding the `__repr__()`, the `Student` class should look like this:

~~~{.python caption="main.py"}
# main.py
class Student:
    def __init__(self, name, roll_no, major, year):
        self.name = name
        self.roll_no = roll_no
        self.major = major
        self.year = year

    def __repr__(self):
        return f"Student: {self.name} {self.roll_no} {self.major} {self.year}"
~~~

![why]({{site.images}}{{page.slug}}/1.png)\

### Implementing the `__eq__()` Method

## How to Create Data Classes in Python

## Type Hints and Default Values in Python Data Classes

### How Do Type Hints Help? 

#### Enforcing Type Checks

### Setting Default Values for Data Class Attributes

<div class="notice--big--primary">
#### The Curious Case of Mutable Default Arguments in Python
  
  ![curious]({{site.images}}{{page.slug}}/3.png)\
  
</div>


## Defining Methods in a Python Data Class

## Are Immutable Data Classes Helpful?

## Python Data Classes vs. NamedTuples

## Conclusion













