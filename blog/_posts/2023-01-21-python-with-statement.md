---
title: "Introduction to Context Managers and the with Keyword in Python"
categories:
  - Tutorials
toc: true
author: Ashutosh Krishna

internal-links:
 - Python
 - Context Manager
 - Handling
excerpt: |
    Learn how to use the `with` keyword in Python to handle exceptions and ensure proper resource management. This article explains the concept of context managers and provides examples of creating your own classes and functions that support the `with` statement. Whether you're working with files, locks, or other types of connections, understanding the `with` statement is essential for writing clean and efficient Python code.
last_modified_at: 2023-07-19
---
**This article explains the `with` statement in Python. The `with` statement in Python streamlines exception handling. Earthly simplifies the build process in continuous integration. [Check it out](https://cloud.earthly.dev/login).**

The `with` keyword in python is used for exception handling when working with certain resources like files or database connections. These resources may need to have additional actions performed if an exception is raised.

For example, if there is an error reading from a file, we'd like to be certain the file gets closed before the program exits and raises the error. The `with` statement is not limited to files or database connections, it can also be used with locks, sockets, sub-processes, telnet, and other types of connections.

In this article, we'll take a deeper look at the `with` keyword. We'll look at how it works, when you should use it, and how you can create your own classes and functions that support `with`.

## Prerequisites

- Working knowledge of Python
- Python 3.8+

## How the `with` Statement Works

Let's start by taking a look at one of the most common uses for the 'with' statement: working with files.

### File Handling without the `with` Statement

Let's start with some simple code to write to a file.

~~~{.python caption=""}
file = open("sample1.txt", "w")
file.write("Earthly is great!")
file.close()
~~~

The code above:

- Opens a file called `sample1.txt` in write mode
- Writes some text to the file
- Closes the file

As long as everything executes as expected, this code should work just fine, but a problem arises if at any point our program encounters and error and we don't end up getting to the line where we close the file. If you don't close a file properly, it can lead to data loss, resource leakage, or security vulnerabilities. In addition to that, it can also prevent other processes from being able to interact with the file in the future.

To avoid the above problems, you can use the `try-finally` block as shown below:

~~~{.python caption=""}
file = open("sample2.txt", "w")
try:
    file.write("Earthly is great!")
finally:
    file.close()
~~~

The above code opens a file called `sample2.txt` in a similar fashion as the previous example, but here we use the `write()` method inside a `try` block and the `close()` method inside the `finally` block. The `finally` block ensures that the file closes properly if an exception occurs or not.

> Learn more about exception handling in Python in this [tutorial](/blog/error-handling-in-python/).

### File Handling using the `with` Statement

In the previous example, you learned how to utilise exception handling to ensure a file closes in case of an error. But, you can do the same using the `with` statement as shown below:

~~~{.python caption=""}
with open("sample3.txt", "w") as file:
    file.write("Earthly is great!")
~~~

In addition to helping you clean up resources after usage, the `with` statement also allows you to include logic for acquiring resources or creating objects that will be used within the `with` statement block.

For example, you can use a `try-finally` block to acquire a lock as below:

~~~{.python caption=""}
import threading

lock = threading.Lock()

lock.acquire()
try:
    # Critical section of code
finally:
    lock.release()
~~~

However, the same can be written using `with` statement in the following way:

~~~{.python caption=""}
import threading

lock = threading.Lock()

with lock:
    # Critical section of code
    # lock is automatically released when execution leaves this block
~~~

As you can see, the `with` statement allows you to write this code more concisely and clearly. The `with` statement automatically takes care of calling the `acquire()` and `release()` methods of the lock object, so you don't have to include them in the `try-finally` block.

## How to Create a Class That Supports the `with` Statement

![How]({{site.images}}{{page.slug}}/how.jpg)\

You can create your own classes that support the `with` statement. A class or a function that supports the `with` statement is known as a **Context Manager**. The `open` function is an example of a context manager.

A Python class that implements the methods below qualifies as a context manager:

- `__enter__()`: This method is called when the `with` statement is executed, and it returns an object that will be bound to the variable specified in the `as` clause of the `with` statement.
- `__exit__()`: This method is called when the block of code inside the `with` statement has finished executing (regardless of whether an exception was raised or not). It is responsible for cleaning up any resources that the context manager might have acquired. The `__exit__()` method can also handle exceptions that are raised within the `with` block.

Once you implement the above two methods in your class, you can use the `with` statement with the class.

When you call the `with` statement, the context manager class invokes the `__enter__()` method under the hood, and when you exit the scope of the `with` statement, the class invokes the `__exit__()` method.

Observe the code below to get a clearer picture:

~~~{.python caption=""}
class CustomFileWriter:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        self.file = open(self.filename, 'w')
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

# using the CustomFileWriter class for writing to a file
with CustomFileWriter('sample4.txt') as file:
    file.write('Earthly is great!')
~~~

In the above code example, the `CustomFileWriter` class is a context manager. It has three methods. The `__init__()`, `__enter__()` and the `__exit__()` method

1. Python calls the `__init__()` method (which is the constructor of the class) when you create an object from the class. In this method, you store the filename parameter as an instance variable of the object so that you can access it later.
2. Python calls the `__enter__()` method when it executes the `with` statement. The method is used to set up the context for the block of code that follows. In this case, the method opens the file with the given filename in write mode and returns a reference to the file object.
3. Python calls the `__exit__()` method when it finishes executing the block of code under the `with` statement. This method cleans up any resources (closing the file in this case) that the block accesses.

### How to Create a Context Manager as a Function

In the previous section, you created a context manager class. However, you can also create a context manager function (like the `open()` function) with the [contexlib](https://docs.python.org/3/library/contextlib.html) library:

~~~{.python caption=""}
from contextlib import contextmanager

@contextmanager
def custom_open(filename):
    try:
        file_ptr = open(filename, "w")
        yield file_ptr
    finally:
        file_ptr.close()


with custom_open("sample5.txt") as file:
    file.write("Earthly is great!")
~~~

The above code defines a `custom_open()` function, which is decorated with the `@contextmanager` decorator. This allows you to define a context manager as a [generator function](https://wiki.python.org/moin/Generators), rather than defining a class with specific methods.

The generator function yields a file object when it is called. When the `with` statement is executed and the generator function is called, it opens the file with the given filename in *write* mode and returns a reference to the file object.

When the code in the `with` statement block has finished executing, Python executes the `finally` block, which closes the file. This ensures that the file is always closed, even if an error occurs while writing to the file.

## Conclusion

The `with` statement in Python, used with context managers, provides a simpler way than 'try-finally' blocks to ensure resources are immediately closed after use. In this tutorial, you've learned its function, how to use it in your custom objects and how it manages resources even when exceptions arise. While it's commonly used in file handling, it has wider applications too.

As you continue to master Python, why not explore build efficiency too? Check out [Earthly]((https://cloud.earthly.dev/login)). This tool could be your next step in optimizing your development process.

{% include_html cta/bottom-cta.html %}
