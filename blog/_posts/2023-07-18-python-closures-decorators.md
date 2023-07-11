---
title: "An Introduction To Closures and Decorators in Python"
categories:
  - Tutorials
toc: true
author: Rahul K

internal-links:
 - Closures
 - Decorators
 - Python
 - Function Modification
 - Variable Hiding
excerpt: |
    Learn how to use closures and decorators in Python to hide variables, modify function behavior, and add functionality to existing functions or classes. This guide provides examples and explanations of closures and decorators, as well as their practical applications in Python programming.
---

Python is a high-level general-purpose language that supports classes as part of its built-in object-oriented programming (OOP) paradigm. Occasionally, when working with variables in Python, you may want to hide a variable without writing an unnecessary class to keep the code more maintainable. Moreover, you may want to add minor functionality to a function without creating another redundant function. In such scenarios, closures, and decorators can be used as solutions: closures for variable hiding and decorators for function modification. This guide will demonstrate the concept of closures and decorators, explain how and where to use them, and explain when it's most appropriate to use them instead of traditional classes and unnecessary functions.

At the outset, it is imperative to mention that closures and decorators might look similar owing to the fact that both involve functions, but they serve different conceptual purposes.

**Closures**: A closure is a function object that remembers values in the enclosing scope, even if they are not present in memory. A closure is created when a nested function references variables from its enclosing scope. The closure "closes over" the variables it references, thus preserving their values even if the enclosing scope is no longer active. Closures are often used to implement data encapsulation and maintain the state between function calls.

**Decorators**: A decorator is a way to modify the behavior of a function or a class without directly changing its source code. It allows adding functionality to an existing function or class by wrapping it with another function or class. Decorators are commonly used for tasks such as logging, timing, input validation, authentication, and more. They provide a method to separate concerns and keep the code modular and reusable.

Before diving deeper into the concept of closures and decorators, let's start with simple pedagogical examples of both using code.

## A Simple Closure Example

Put simply, a closure is a function that can remember and access the values of variables from its surrounding environment, even after the execution of the outer function has finished.

In Python, closures can be created by defining a function inside another function and returning the inner function. Here is an example:

~~~{.python caption=""}
def outer_function(x):
    def inner_function(y):
        return x + y
    return inner_function

closure = outer_function(5)
print(closure(3))  # Output: 8
~~~

In the example provided above, the 'outer_function' takes an argument 'x' and defines an inner function called 'inner_function' that takes another argument 'y' and returns the sum of 'x' and 'y.'

The 'outer_function' then returns the inner function 'inner_function.' Since 'inner_function' is a nested function, it has access to the variables in the enclosing scope of 'outer_function', which in this case is the variable 'x.'

When 'outer_function' is called with the argument '5', it returns the function 'inner_function', **which remembers the value of 'x' as '5'**. This function object is assigned to the variable `closure`.

Finally, `closure` is called with argument '3', which adds '3' to the value of 'x' (which is '5'), resulting in output '8.'

Therefore, the output of the code is '8', which demonstrates that the inner function 'inner_function' has retained the value of 'x' from the outer scope, even after the execution of the 'outer_function' has finished.

## Why and How to Use Closures

![Why]({{site.images}}{{page.slug}}/why.png)\

Closures are used in Python for various reasons, such as:

Implementing data hiding: In Python, closures can be used to hide data within a function by defining a variable inside the outer function and then using it in the inner function. This helps in encapsulating the data and prevents it from being modified from outside the function.

Implementing decorators: Closures are also used to implement decorators in Python. Decorators are functions that modify the behavior of other functions.

Now you will learn how data hiding can be simplified with the use of closures compared to the class method. Therefore a comparative approach will be followed to explain it better. To start with, here is an example of how to use a class to hide data in Python

~~~{.python caption=""}
class SecureData:
    def __init__(self, data):
        self.data = data
        self.password = 'secret'

    def get_data(self, passwd):
        if passwd == self.password:
            return self.data
        else:
            return None

secure_data = SecureData('my sensitive data')

print(secure_data.get_data('secret'))  # Output: 'my sensitive data'
print(secure_data.get_data('wrong password'))  # Output: None
~~~

The `SecureData` class has an `__init__` method that initializes two instance variables: `data` and `password`.

The `get_data` method is defined within the `SecureData` class, which takes a password as a parameter. It compares the provided password with the `password` instance variable of the class. If they match, it returns the `data` instance variable. Otherwise, it returns `None`.

To retrieve the secure data, an instance of the `SecureData` class is created (`secure_data`). You can then call the `get_data` method on the `secure_data` instance, passing the password as an argument.

The output of this code is `my sensitive data` when the correct password is provided and `None` when an incorrect password is provided.

By using a class, the data and associated behavior are encapsulated within the class methods. The instance variables (`data` and `password`) are accessible and modifiable only through the defined methods of the class, providing data hiding and access control.

Now let us move to the closures. Here is an example of how to use closures to hide data in Python:

~~~{.python caption=""}
def create_secure_data(data):
    password = 'secret'

    def get_data(passwd):
        if passwd == password:
            return data
        else:
            return None

    return get_data

secure_data = create_secure_data('my sensitive data')

# Now, the 'secure_data' variable contains a reference to 
# the inner function 'get_data' which can access the 'password' 
# and 'data' variables of the outer function 'create_secure_data'.

# To retrieve the secure data, you need to call the 'secure_data' 
# function with the correct password.
print(secure_data('secret')) # Output: 'my sensitive data'
print(secure_data('wrong password')) 
~~~

In this example, the `create_secure_data` function takes in some data and returns an inner function `get_data`. The `get_data` function takes in a password as an argument and checks if it matches the password variable defined in the outer function. If the password is correct, the `get_data` function returns the enclosed data variable, otherwise, it returns `None`.
By using closures in this way, you have hidden the data variable and only allow access to it if the correct password is provided. This provides a simple way of implementing data hiding in Python.

## What Are Decorators

A decorator is a higher-order function that takes another function as an argument, adds some functionality to it, and returns a new function without modifying the original function's source code. Decorators allow you to modify the behavior of functions or classes by wrapping them inside another function. Here is an example:

~~~{.python caption=""}
def decorator_function(func):
    def wrapper_function():
        print("Before function is called.")
        func()
        print("After function is called.")
    return wrapper_function

@decorator_function
def hello():
    print("Hello, world!")

hello()
~~~

Run the above code and you will receive an output similar to this:

~~~{ caption="Output"}
Before function is called.
Hello, world!
After function is called.
~~~

In the example provided above, you define a decorator function 'decorator_function' that takes a function 'func' as an argument and returns a new function 'wrapper_function.' The 'wrapper_function' adds some functionality to the original function 'func.'
The '@decorator_function' syntax is used to decorate the 'hello' function with the 'decorator_function' decorator. When 'hello' is called, it is actually calling the 'wrapper_function' returned by 'decorator_function.' This allows modifying the behavior of `hello` without changing its source code directly.

When 'hello' is called, it prints "Before function is called." using the print function, then it calls the original func (which in this case is print("Hello, world!")), and finally it prints "After function is called."

## Exploring Decorators in Detail

![Exploring]({{site.images}}{{page.slug}}/exploring.png)\

In Python, decorators enable [meta-programming](https://en.wikipedia.org/wiki/Metaprogramming), which refers to a programming technique in which the code can manipulate other code at either compile-time or run-time. So as an example of metaprogramming technique, decorators provide a means to modify the behavior of functions or classes without modifying their source code.

Here's an example of how to use decorators for meta-programming in Python:

~~~{.python caption=""}
def debug(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__} with args: {args}, \
        kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned: {result}")
        return result

    return wrapper

@debug
def add(a, b):
    return a + b

result = add(3, 5)
print(result)  
~~~

In this example, you define a decorator called `debug` that adds debugging information to the decorated function. The `debug` decorator wraps the original function (`add`) with a closure function called `wrapper`. The `wrapper` function prints the function name, arguments, and keyword arguments before calling the original function. It also prints the returned result after executing the original function.

By using the `@debug` syntax, you can apply the `debug` decorator to your `add` function. This enhances your `add` function with debugging information without modifying its original implementation.

When you call `add(3, 5)`, the `debug` decorator intercepts the function call, prints the debugging information, executes the original `add` function, captures the result, prints the result, and returns it.

So, the output of the example would be:

~~~{ caption="Output"}
Calling add with args: (3, 5), kwargs: {}
add returned: 8
8
~~~

Now, to test the `add` function further, let us feed the keyword arguments to the `add` function. For example, run the following modified code:

~~~{.python caption=""}
result2 = add(a="pin", b="point")
print(result2)  
~~~

And you will get the following output, printing the keys and :

~~~{ caption="Output"}
Calling add with args: (), kwargs: {'a': 'pin', 'b': 'point'}
add returned: pinpoint
pinpoint
~~~

You see once you created your debug decorator it can be applied to any function which takes arguments or keyword arguments.

In summary, decorators are a powerful feature in Python that can be used for meta-programming, enabling you to modify the behavior of functions and classes without altering their source code.

Having understood the meta-programming example, you should turn to another use, i.e., runtime modification of a function.

### Runtime Modification of a Class Using Decorators in Python

In Python, decorators can be used for runtime modification of a class as well. Decorators can add or modify behavior of a class without modifying its source code. Here you will understand how to implement  [the singleton pattern](https://python-patterns.guide/gang-of-four/singleton/) using decorators. In software design, the singleton pattern is a pattern where only a single instance of a class is instantiated and used throughout the designed system. Here's an example code:

~~~{.python caption=""}
def make_singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper

@make_singleton
class DatabaseConnection:
    def __init__(self, url):
        self.url = url
        print("Initializing database connection.")

    def execute_query(self, query):
        print(f"Executing query: {query} on database: {self.url}")

# Create two instances of DatabaseConnection
connection1 = DatabaseConnection("https://example.com/db")
connection2 = DatabaseConnection("https://example.com/db")

print(connection1 is connection2)  # Output: True
~~~

In this example, you define a decorator called `make_singleton` that transforms a class into a singleton. The `make_singleton` decorator wraps the class with a closure function called `wrapper`. The `wrapper` function maintains a dictionary `instances` to keep track of instances of the class. When creating a new instance, the decorator checks if an instance of the class already exists. If it does, the existing instance is returned. Otherwise, a new instance is created and stored in the `instances` dictionary.

By using the `@make_singleton` syntax, you can apply the `make_singleton` decorator to your desired class. This modifies the behavior of the class by ensuring that only a single instance of the class is created and shared.

When you create multiple instances of the class, the decorator intercepts the class instantiation and returns the same instance for all of them. This is because the decorator converts the class into a singleton, allowing only one instance to be created. As a result, all references to the class will point to the same object.

This approach is useful when you need to have a single instance of a class shared across different parts of your program. By applying the `make_singleton` decorator, you can ensure that there is only one instance of the class throughout your codebase.

This approach can be used to add any kind of behavior to a function or class at runtime. For example, you can use a decorator to add logging, error handling, performance monitoring, or any other functionality that you want to apply to multiple functions.

## Decorators for Timing Purposes in Python

![Timing]({{site.images}}{{page.slug}}/timing.png)\

In Python, decorators can be used for timing purposes to measure the execution time of a function. Timing a function can be useful for optimizing its performance or measuring its efficiency. Here's an example of how to use decorators for timing purposes:

~~~{.python caption=""}
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time}")
        return result
    return wrapper

@timer
def my_function():
    time.sleep(2)

my_function()
~~~

Run the above code, you will receive an output similar to this:

~~~{ caption="Output"}
Execution time: 2.0001144409179688
~~~

You observe that applying the decorator `@timer to my_funcation()` also prints the time duration of the execution of the function.

## Applying Multiple Decorators to a Single Function

You can apply multiple decorators to a single function in Python. When you apply multiple decorators to a function, the decorators are applied from the inside out. That is, the innermost decorator is applied first, followed by the next innermost, and so on until the outermost decorator is applied.
Here's an example of how to apply multiple decorators to a single function:

~~~{.python caption=""}
def decorator1(func):
    def wrapper():
        print("Before decorator1")
        func()
        print("After decorator1")
    return wrapper

def decorator2(func):
    def wrapper():
        print("Before decorator2")
        func()
        print("After decorator2")
    return wrapper

@decorator1
@decorator2
def my_function():
    print("my_function")

my_function()
~~~

In the above example, two decorators, `decorator1` and `decorator2`, are defined, which add some print statements before and after the decorated function is called. Then, both decorators are applied to the `my_function` function using the `@decorator1` and `@decorator2` syntax.

When you call `my_function()`, the output will be:

~~~{ caption="Output"}
Before decorator1
Before decorator2
my_function
After decorator2
After decorator1
~~~

As you can see, the decorators are applied from the inside out, so `decorator2` is applied first, followed by `decorator1`.

## Performing Type Checking of Function Parameters

As the most advanced application of decorators in Python, you can also use decorators to perform type-checking of function parameters. This approach can be useful if you want to add type-checking to existing functions without modifying their source code.
Here's an example of how to use a decorator to do type checking of function parameters:

~~~{.python caption=""}
def type_check(func):
    def wrapper(*args, **kwargs):
        # iterate over the function arguments and their types
        for arg, arg_type in zip(args, func.__annotations__.values()):
            # check if the argument type is correct
            if not isinstance(arg, arg_type):
                raise TypeError(f"Argument {arg} has incorrect type \
                {type(arg)}")
        # call the original function with the given arguments
        return func(*args, **kwargs)
    return wrapper
~~~

This decorator function takes the original function as an argument and returns a new wrapper function that can take any number of positional and keyword arguments `*args` and `**kwargs`. It then iterates over the function arguments and their types, which are specified using function annotations. For each argument, it checks if the argument type is correct using the `isinstance()` function. If the argument type is incorrect, it raises a `TypeError` with a helpful error message. If all the arguments are of the correct type, it calls the original function with the given arguments and returns its result.

Here's an example usage of this decorator:

~~~{.python caption=""}
@type_check
def add(x: int, y: int) -> int:
    return x + y

print(add(1, 2))  # Output: 3
print(add("1", "2"))  
# Raises: TypeError: Argument 1 has incorrect type <class 'str'>
~~~

In this example, the `add()` function is decorated with the `type_check()` decorator. The function takes two integer arguments, `x` and `y`, and returns their sum as an integer. The function annotations specify the argument types and the return type of the function.
When you call the `add()` function with two integer arguments, it returns their sum as expected. However, when you call the function with two string arguments, the decorator raises a `TypeError` with a helpful error message indicating that the first argument has an incorrect type.

This approach can be used to add type-checking to any function that you want to modify. You can apply the `type_check` decorator to any function that you want to check, and it will automatically perform type-checking on its arguments.

In summary, decorators can be used for performing type checking of function parameters in Python. This approach allows you to add type checking to existing functions without modifying their source code and can be helpful in catching type errors before the code is executed.

You have seen multiple uses of decorators above. So it can be summarised that decorators are a powerful feature in Python that can be used for runtime modification of a function or class, allowing you to add or modify behavior without changing their source code.

## Conclusions

Closures and decorators are programming concepts in Python that enable developers to write more flexible and powerful code. Closures enable you to create functions that can retain access to the values in their outer scope, even after the execution of the outer function has finished. On the other hand, decorators allow you to modify the behavior of functions or classes without altering their source code. By combining closures and decorators, you can create even more powerful and flexible functions and classes that can further enhance the functionality and reusability of your code.

{% include_html cta/bottom-cta.html %}
