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
last_modified_at: 2023-07-19
---
**We're [Earthly](https://earthly.dev/). Our build automation tool makes building software simpler and faster using containerization. Earthly can make your Python projects easier to build and troubleshoot. [Check us out](/).**

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

---------------------------------------------------------------------------
ZeroDivisionError                         Traceback (most recent call last)
Cell In[1], line 4
      2 a = 10
      3 b = 0
----> 4 c = a/b

ZeroDivisionError: division by zero
~~~

In the above example, the program attempts to divide a number by zero, which results in a `ZeroDivisionError` during the runtime of the program.

Understanding the different types of errors in Python is important for effective [debugging](/blog/printf-debugging) and error handling. Syntax errors can be easily detected and resolved during the compilation phase, while runtime errors require a more sophisticated error handling mechanism such as the `try-except` blocks. By learning how to handle different types of errors, developers can create robust and reliable Python programs.

## `try-except` Block

The `try-except` block is the primary mechanism for handling exceptions in Python. It allows developers to write code that can detect and handle runtime errors, without causing the program to crash. In a `try-except` block, the code that is likely to raise an exception is placed inside the `try` block, and the code that handles the exception is placed inside the `except` block. Here's an example of a simple `try-except` block in Python:

~~~{.python caption="error-handling-in-python.ipynb"}
try:
    a = 10
    b = 0
    c = a/b
except ZeroDivisionError:
    print("Cannot divide by zero!")
~~~

When this code is run, the exception handler will catch the error raised when attempting to divide a number by zero. The output below will be returned with the message `"cannot divide by zero!"`.

Output:

~~~{ caption="Output"}
Cannot divide by zero!
~~~

In the above example, the code inside the try block attempts to divide a number by zero, which results in a `ZeroDivisionError`. The except block catches the exception and prints a user-friendly message to the console.

The try-except block works by first executing the code inside the try block. If an exception is raised, the program jumps to the except block and executes the code inside it. If no exception is raised, the except block is skipped. It's important to note that try-except blocks should only be used to handle expected exceptions, and not as a general-purpose error handling mechanism.

Here are a few scenarios where the `try-except` blocks can be useful for handling errors in Python:

1. Reading a file: When reading a file in Python, there is a possibility that the file may not exist, or the program may not have sufficient permissions to read the file. In such cases, a try-except block can be used to catch the [`FileNotFoundError`](https://docs.python.org/3/library/exceptions.html) and [`PermissionError`](https://docs.python.org/3/library/exceptions.html) exceptions that are raised respectively for the two scenarios. A user-friendly message can then be provided to the user.

      This is shown in the code below:

      ~~~{.python caption="error-handling-in-python.ipynb"}
      try:
          with open('example.txt') as f:
              data = f.read()
      except (FileNotFoundError, PermissionError) as e:
          print(f"Error: {e}")
      ~~~

      Output:

      ~~~{ caption="Output"}
      Error: [Errno 2] No such file or directory: 'example.txt'
      ~~~

2. Handling invalid input: When a user enters invalid input, such as a non-numeric value for a number, the program will raise a `ValueError`. A try-except block can be used to catch the exception and prompt the user to enter valid input as shown below:

~~~{.python caption="error-handling-in-python.ipynb"}
try:
    x = int(input("Enter a number: "))
except ValueError:
    print("Invalid input! Please enter a number.")
~~~

By using the `try-except` blocks, developers can write code that can gracefully handle errors and provide a better user experience.

## Handling Specific Exceptions

In Python, specific exceptions can be handled using the try-except block. When an exception is raised, the except block can be used to catch the specific exception and handle it appropriately. This allows for more fine-grained error handling, where different exceptions can be handled differently.

Here's an example of how to handle the `FileNotFoundError` and the `ValueError` exceptions:

~~~{.python caption="error-handling-in-python.ipynb"}
try:
    with open("file.txt") as f:
        content = f.read()
    num = int("abc")
except FileNotFoundError:
    print("File not found!")
except ValueError:
    print("Invalid value!")
~~~

Output:

~~~{ caption="Output"}
File not found!
~~~

In the above example, the code in the try block attempts to read the contents of a file and convert a string to an integer. If the file is not found, the `FileNotFoundError` exception is raised and the corresponding except block is executed. Similarly, if the string `"abc"` cannot be converted to an integer, the `ValueError` exception is raised and the corresponding except block is executed.

Here's another example that demonstrates how to handle multiple exceptions in a single try-except block:

~~~{.python caption="error-handling-in-python.ipynb"}
try:
    with open("example.txt", "r") as file:
        contents = file.read()
    value = int(input("enter a number: "))
    num = 10 / value
except ZeroDivisionError:
    print("Cannot divide by zero")
except ValueError:
    print("Cannot convert string to integer")
except FileNotFoundError:
    print("Cannot find the file")
~~~

In the above example, the code in the `try` block attempts to open and read the content of a file, divide a number by an integer value that the user enters, convert a string to an integer.

If the file does not exist, the `except` block for the `FileNotFoundError` exception is executed and the following output is printed in the console:

Output:

~~~{ caption="Output"}
Cannot find the file
~~~

If the user enters a zero value, the `except` block for the `ZeroDivisionError` will be executed and the following output will be printed:

Output:

~~~{ caption="Output"}
Cannot divide by zero
~~~

If the user enters a string value, it results in a `ValueError` exceptions as the `int` function tries to convert the string to integer. This exception is handled by the `except` block for the `ValueError` and the following output is printed in the console:

Output:

~~~{ caption="Output"}
Cannot convert string to integer
~~~

By handling specific exceptions, developers can write more robust and reliable code that can gracefully handle errors and provide a better user experience for users.

## Raising Exceptions

In Python, exceptions can be raised using the [`raise`](https://docs.python.org/3/tutorial/errors.html) statement. This allows developers to manually raise an exception when a specific error condition is detected. Here's a simple example:

~~~{.python caption="error-handling-in-python.ipynb"}
x = 10
if x > 5:
    raise ValueError("x should be less than or equal to 5")
~~~

The code above will produce the following output:

Output:

~~~{ caption="Output"}
----------------------------------------------------------
ValueError              Traceback (most recent call last)
Cell In[7], line 3
      1 x = 10
      2 if x > 5:
----> 3     raise ValueError("x should be less than or equal to 5")
ValueError: x should be less than or equal to 5
~~~

In the above example, the `raise` statement is used to raise a `ValueError` exception if the value of `x` is greater than 5. When the `raise` statement is executed, a traceback is printed to the console along with the message associated with the exception.

Python built-in exceptions like `ValueError`, `TypeError`, and `IndexError` can be explicitly raised using the `raise` statement. Here's an example to demonstrate this:

~~~{.python caption="error-handling-in-python.ipynb"}
def get_element(data, index):
    if index >= len(data):
        raise IndexError("Index out of range")
    return data[index]
~~~

In the above example, the `get_element` function raises an `IndexError` if the specified index is out of range for the given data. This allows the caller of the function to handle the exception appropriately.

Developers can also create their own custom exceptions by creating a new class that inherits from the [`Exception`](https://docs.python.org/3/tutorial/errors.html) class. Here's an example:

~~~{.python caption="error-handling-in-python.ipynb"}
class CustomException(Exception):
    pass

def some_function():
    raise CustomException("An error occurred")

try:
    some_function()
except CustomException as e:
    print("Error:", e)
~~~

In the above example, the `CustomException` class is defined by inheriting from the `Exception` class. The `some_function` function raises a `CustomException` when called. The `try-except` block catches the `CustomException` and prints the error message to the console.

Raising exceptions allows for better error reporting and debugging, as exceptions provide a detailed traceback that can help identify the source of the error.

## Finally Block

In Python, the finally block specifies code that should execute regardless of whether an exception was raised or not. It is particularly useful for performing cleanup tasks, such as closing files or releasing resources, after an error occurs. As long as the try block was executed, the finally block will always be executed, regardless of whether an exception was raised or not.

Here's an example of how to use the `finally` block:

~~~{.python caption="error-handling-in-python.ipynb"}
file = None
try:
    file = open("file.txt")
    # do some work with the file
except:
    print("An error occurred!")
finally:
    if file:
         file.close()
~~~

The code above opens a file named file.txt and performs some work on it, and then closes the file. If an error occurs while opening or working with the file, the code will catch the exception and print an error message. Regardless of whether an error occurred, the `finally` block is executed, which closes the file using the `close()` method. This ensures that the file is properly closed and any resources are released, even if an error occurred.

The `finally` block can also be used in combination with the `try-except` block to perform more complex cleanup tasks. Here's an example:

~~~{.python caption="error-handling-in-python.ipynb"}
import os

try:
    file = open("file.txt")
    # do some work with the file
except:
    print("An error occurred!")
finally:
    if file:
          file.close()
    if os.path.exists("file.txt"):
          os.remove("file.txt")
~~~

In the above example, the `os.remove()` function is called in the `finally` block to delete the file if it exists. This ensures that any resources associated with the file are released, even if an error occurred.

It's important to note that the `finally` block is always executed, even if the `try` block contains a `return` statement, which would normally prevent any further code from being executed. This allows for important cleanup tasks to be performed before the function returns.
By using the `finally` block, developers can ensure that resources are properly cleaned up and released, even in the event of an error. This can help prevent resource leaks and ensure that the program runs efficiently and reliably.

## The Assert Statements

In Python, the [`assert`](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement) statements are a [debugging](/blog/printf-debugging) tool used to check for certain conditions that should always be true. If the condition is not true, an [`AssertionError`](https://docs.python.org/3/library/exceptions.html) is raised, which can help identify bugs in the code. The `assert` statement takes an expression as its argument and an optional error message.
Here's an example of using an `assert` statement:

~~~{.python caption="error-handling-in-python.ipynb"}
def divide(a, b):
    assert b != 0, "Cannot divide by zero!"
    return a / b
~~~

In the above example, the `divide` function takes two arguments and uses an `assert` statement to check that the second argument (`b`) is not equal to zero. If `b` is zero, the `assert` statement raises an `AssertionError` with the message `"Cannot divide by zero!"`. If the condition is true, the function returns the result of the division.

~~~{.python caption="error-handling-in-python.ipynb"}
divide(2, 0)
~~~

Output:

~~~{ caption="Output"}
divide(2, 0)
------------------------------------------------------------
AssertionError             Traceback (most recent call last)
Cell In[9], line 1
----> 1 divide(2, 0)

Cell In[8], line 2, in divide(a, b)
      1 def divide(a, b):
----> 2     assert b != 0, "Cannot divide by zero!"
      3     return a / b

AssertionError: Cannot divide by zero!
~~~

The `assert` statements can also be used to check the type or value of a variable. Here's an example:

~~~{.python caption="error-handling-in-python.ipynb"}
def greet(name):
    assert isinstance(name, str), "Name must be a string!"
    print(f"Hello, {name}!")

greet(23)
~~~

Output:

~~~{ caption="Output"}
---------------------------------------------------------
AssertionError          Traceback (most recent call last)
Cell In[11], line 1
----> 1 greet(23)

Cell In[10], line 2, in greet(name)
      1 def greet(name):
----> 2     assert isinstance(name, str), "Name must be a string!"
      3     print(f"Hello, {name}!")

AssertionError: Name must be a string!
~~~

In the above example, the `greet` function uses an `assert` statement to verify that the `name` argument is a string. If the argument is not a string, an `AssertionError` is raised with the message `"Name must be a string!"`. If the argument is a string, the function prints a greeting message.

The `assert` statements are useful for catching errors early in the development process and can help developers identify and fix bugs quickly. However, they should not be used as a replacement for proper error handling, as they are intended for [debugging](/blog/printf-debugging) purposes only. It's also important to note that `assert` statements can be disabled globally using the [`-O` (optimize) command line option](https://docs.python.org/3/using/cmdline.html#cmdoption-O) or the [`PYTHONOPTIMIZE`](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONOPTIMIZE) environment variable, so they should not be used for security checks or other critical conditions.

## Best Practices for Error Handling

![Error Handling]({{site.images}}{{page.slug}}/error comp.png)\

When it comes to error handling in Python, there are a few best practices that can help you write more robust and reliable code. Here are some tips to keep in mind:

1. **Handle exceptions at the appropriate level of abstraction:** When handling exceptions, it's important to consider the level of abstraction at which the exception occurs. For example, If you have a function that opens a file and reads its content, it would be best to handle any errors that may occur while opening or reading the file within that function. This way, you can catch and handle the error immediately, without passing it up to a higher-level function that may not have enough context to handle the error effectively.

2. **Write clear and informative error messages:** Error messages should be clear and informative, providing enough information to help the user or developer understand what went wrong and how to fix it. The message should include the type of error, the function or module where the error occurred, and any relevant details or context.

3. **Use consistent error handling throughout your code:** To make your code more maintainable and easier to debug, use consistent error handling throughout your codebase. This means using the same style and approach to error handling across all of your functions and modules.

4. **Test error handling code:** When testing your code, be sure to test error handling as well. This means testing both for cases where exceptions are raised (to ensure they are handled correctly) and cases where exceptions are not raised (to ensure that the code works as expected in normal conditions).

5. **Document error handling:** It's important to document your error handling code so that other developers (and your future self) can understand how errors are handled and why. This includes documenting the types of errors that can be raised, how they are handled, and any relevant context or details.

6. **Use logging to track errors:** [Logging](/blog/understanding-docker-logging-and-log-files) is a useful tool for tracking errors in your code. You can use the built-in Python [`logging` module](https://docs.python.org/3/library/logging.html) to log error messages and other information, which can help you debug issues and monitor the performance of your code.

7. **Avoid bare `except` clauses:** In general, it's best to avoid using bare `except` clauses (which catch all exceptions) as they can make it harder to debug issues in your code. Instead, use specific exception types or catch exceptions at the appropriate level of abstraction.
By following these best practices, you can write more reliable, maintainable, and robust code that is easier to debug and understand.

## Conclusion

This article provided insights on Python error handling, such as various error types, usage of 'try-except' and 'finally' blocks, raising exceptions, and the use of assert statements for debugging. We've also discussed best practices like writing clear error messages, testing, consistency, documentation, and logging.

After reading, you should be adept at handling errors in Python to create more reliable code. All code discussed is available on [GitHub](https://github.com/Boadzie/error-handling-in-python).

And as you continue to refine your Python skills, you might also be looking for ways to streamline your build process. If so, consider taking your workflow up a notch with [Earthly](https://www.earthly.dev/), a tool designed to simplify build automation.

{% include_html cta/bottom-cta.html %}
