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

We’ll first create a regular [Python class](https://earthly.dev/blog/how-cls-obj-work-python/), then rewrite it as a data class. In the process, we’ll try to understand some out-of-the-box features of data classes that make them a better choice.

As our goal is to *understand and use* data classes—and not to write fancy classes—let's create a simple class such as a `Student` or an `Employee` class.

So `Student` or `Employee`? 

![student-vs-employee-class]({{site.images}}{{page.slug}}/5.png)\

I’ll choose `Student` class for now.

### The `__init__()` Method

### Adding a Helpful `__repr__()`

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













