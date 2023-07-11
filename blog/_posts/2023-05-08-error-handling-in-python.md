---
title: "Error Handling in Python"
categories:
  - Tutorials
toc: true
author: Daniel Boadzie

internal-links:
 - Python
 - Error Handling
 - Debugging
 - Exceptions
excerpt: |
    Learn how to handle errors in Python with this comprehensive article. From syntax errors to runtime errors, you'll discover how to use the `try-except` block, raise custom exceptions, and implement best practices for error handling.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about error handling in Python. Earthly is a powerful build tool that can be used in combination with Python projects to automate the build process and ensure reliable error handling. [Check us out](/).**

Error handling is a critical aspect of programming, and it involves detecting and resolving errors that occur during program execution. Python is a high-level programming language that provides built-in features and libraries for error handling, making it easier for developers to detect and handle errors in their programs. In Python, errors can occur due to dynamic typing and a lack of compile-time checks, making it even more important to properly handle exceptions.

This article will introduce the concept of exception handling in Python and cover the built-in exceptions provided by the language. The article will also cover how to define and raise custom exceptions in Python, and how to use the `try-except block` to handle exceptions. Other related statements like `try-finally` and `raise` will also be discussed in detail. The article will also cover best practices for error handling.

By the end of the article, you will have a comprehensive understanding of error handling in Python and how to build robust and reliable Python applications. You will learn how to handle exceptions in your programs, use the `try-except` block and other related statements to handle exceptions, and implement best practices for error handling.

## Types of Errors in Python

![Error]({{site.images}}{{page.slug}}/error.png)\

In Python, errors can be broadly classified into two categories: syntax errors and runtime errors. Understanding the difference between these two types of errors is important for effective [debugging](/blog/printf-debugging) and error handling in Python programs.

1. **Syntax Errors**: Syntax errors, also known as parsing errors, occur when the Python interpreter is unable to parse a line of code due to a violation of the language's syntax rules. These errors are detected during the compilation phase, which means that the program will not run until the syntax errors are resolved. Some common examples of syntax errors include incorrect indentation, missing colons, and misspelled keywords. Here is an example of a syntax error in Python:

      ~~~{.python caption="error-handling-in-python.ipynb"}
      # incorrect indentation
      def add_numbers(x, y):
      return x + y
      ~~~

      In the above example, the function definition is missing the required indentation, which results in a syntax error:

      ~~~{ caption="Output"}
      File "<ipython-input-1-7163263e7970>", line 2
          return x + y
          ^
      IndentationError: expected an indented block
      ~~~

2. **Runtime Errors:** Runtime errors, also known as exceptions, occur during the execution of a program. These errors can occur due to a variety of reasons, such as invalid input, incorrect data types, or unexpected behavior of the program. Some common examples of runtime errors in Python include [ZeroDivisionError](https://docs.python.org/3/library/exceptions.html#ZeroDivisionError), [ValueError](https://docs.python.org/3/library/exceptions.html#ValueError), and [TypeError](https://docs.python.org/3/library/exceptions.html#TypeError). Here is an example of a runtime error in Python:

~~~{.python caption="error-handling-in-python.ipynb"}
# dividing a number by zero
a = 10
b = 0
c = a/b
~~~

This code attempts to divide the value of the variable `a` which is equal to 10 by the value of the variable `b` which is equal to 0. Division by zero is not defined mathematically, so this code will throw an error. Specifically, it will raise a `ZeroDivisionError` in Python.

Output:

~~~{ caption="Output"}