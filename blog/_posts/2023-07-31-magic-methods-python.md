---
title: "Exploring the Magic Methods in Python"
categories:
  - Tutorials
toc: true
author: Ashutosh Krishna
editor: Ubaydah Abdulwasiu

internal-links:
 - just an example
---

**We're [Earthly](https://earthly.dev/). We make building software simpler and, therefore, faster. If you're interested in a simple and containerized approach to building Python code, then [check us out](/).**

In Python programming, a set of special methods exists, often called "magic methods" or "dunder methods". Magic methods provide a way to define and customize the behavior of classes in Python. You do not call them directly; the interpreter implicitly calls them in response to specific operations or events. For example, when you add two numbers using the `+` operator, the `__add__()` method gets called internally.

The magic methods are often called "dunder methods". The term "dunder" is short for "double underscore", as these methods are identified by their names enclosed in double underscores (e.g., `__init__`). By using these methods' capabilities, you can define how your Python objects should behave in various scenarios, such as string representation, arithmetic operations, etc.

In this tutorial, you'll explore the fascinating world of magic methods in Python. You'll discover how these magic methods fit into object-oriented programming (more on this in the next section). You'll also learn about some common magic methods used widely in Python. You'll also see how these methods help you achieve [operator overloading in Python](https://www.programiz.com/python-programming/operator-overloading). By the end, you'll grasp magic methods and have the tools to design powerful code in Python's object-oriented world.

## Understanding the Basics of Object-Oriented Programming in Python

[Object-oriented programming](https://blog.ashutoshkrris.in/object-oriented-programming-in-python) (OOP) is a programming paradigm that organizes code to resemble real-world objects or entities. Objects are instances of classes with specific properties (characteristics) and behaviors (actions) in OOP. This approach allows you to organize your code more intuitively and modularly, making it easier to manage and reuse. Using OOP, you can model complex systems, solve problems more efficiently, and build software that is easier to understand and maintain.

In Python, you can create objects by defining classes. Classes act as blueprints or templates for objects. Strings, lists, and dictionaries are some examples of built-in Python classes. A class consists of variables, called attributes, and methods that define how the object behaves. Creating an object based on a class is like using the blueprint to build a specific item.

In the next section, you will dive deeper into the world of object-oriented programming in Python by exploring how magic methods fit into the object-oriented paradigm.

### How Magic Methods Fit Into the OOP Paradigm

Magic methods are an integral part of the object-oriented programming paradigm in Python. They allow you to define special behaviors for classes and objects, enabling them to respond to specific operations or events. By implementing magic methods, you can customize how objects are created, represented as strings, compared to one another, modified using arithmetic operations, and much more. Magic methods fit smoothly into the OOP paradigm, increasing the flexibility and expressiveness of your code.

Consider the following basic example to demonstrate these concepts:

~~~
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height


# Creating object from the Rectangle class
rect = Rectangle(4, 5)

# Accessing attributes
print(rect.width)

# Printing the rectangle object
print(rect)
~~~

The above code demonstrates the implementation of a `Rectangle` class in Python. This class is a blueprint for creating rectangle objects with specific attributes and behaviors. The class has a special method called `__init__` or the constructor. This method is automatically called when a new object is created from the class. It takes in parameters for `width` and `height` and assigns them to the respective attributes of the object using `self.width` and `self.height`.

To create an actual object from the `Rectangle` class, you initialize an instance, `rect` in the above example, by passing the arguments 4 and 5 to the constructor. This sets the `width` attribute of `rect` to 4 and the `height` attribute to 5. Lastly, the code accesses the `width` attribute of the `rect` object and prints its value and the `rect` object.

Output:

~~~
4
<__main__.Rectangle object at 0x000001DA57973150>
~~~

You can observe that when the `rect` object is printed, the output shows the object's class name and memory address. This is the default representation of a class.

To provide a more meaningful representation of the `rect` object when printing, you can implement the `__str__` magic method within the class to return a string with the desired information about the object.

~~~
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def __str__(self):
        return f"Rectangle: width={self.width}, height={self.height}"


# Creating object from the Rectangle class
rect = Rectangle(4, 5)

# Accessing attributes
print(rect.width)

# Printing the rectangle object
print(rect)
~~~

In the updated code, the `Rectangle` class now includes a custom `__str__` magic method. This method overrides the default string representation of the object and provides a more meaningful output when the object is printed.

Output:

~~~
4
Rectangle: width=4, height=5
~~~

Now, it is clear how the magic methods seamlessly integrate with the object-oriented programming paradigm and offer impressive functionalities and customizability.

## Commonly Used Magic Methods

Now that you understand magic methods, it's time to explore some commonly used ones and their functionalities through practical code examples. This will allow you to see these magic methods in action and better understand how they can be leveraged in Python programming.

### The `__init__` Method

The `__init__` method is used to initialize objects of a class. It is called automatically when an object is created from the class and allows you to set initial values for its attributes.

Consider a `Playlist` class as an example:

~~~
class Playlist:
    def __init__(self, name):
        self.name = name


playlist = Playlist("My Favorite Songs")
print(playlist.name)
~~~

In the above code, the `__init__` method takes a `name` parameter and assigns it to the `name` attribute of the `playlist` object. By passing "My Favorite Songs" as an argument during object creation, the `name` attribute is initialized with the value "My Favorite Songs". Subsequently, accessing `playlist.name`

Output:

~~~
My Favorite Songs
~~~

### The `__str__` Method

The `__str__` method provides a string representation of an object. It is called when you use the `str()` function or the print statement on an object. The primary purpose of this method is to provide a human-readable representation of the object.

Let's extend the previous example to include the `__str__` method:

~~~
class Playlist:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Playlist Name: {self.name}"


playlist = Playlist("My Favorite Songs")
print(playlist)
~~~

Here, the `__str__` method is implemented to return a formatted string that represents the playlist's name. When `print(playlist)` is executed, it calls the `__str__` method, resulting in the following output:

~~~
Playlist Name: My Favorite Songs
~~~

As previously discussed, if you do not implement the `__str__` method and print the object, the output shows the object's class name and memory address.

### The `__repr__` Method

The `__repr__` method provides a formal string representation of an object, typically used for debugging and development purposes. It is called when the `repr()` function is used on an object.

Let's extend the previous example to include the `__repr__` method:

~~~
class Playlist:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"Playlist Name: {self.name}"

    def __repr__(self):
        return f"Playlist(name={self.name})"


playlist = Playlist("My Favorite Songs")
print(repr(playlist))
~~~

In this code, the `__repr__` method is defined to return a formatted string containing the constructor arguments of the `Playlist` object. Invoking `repr(playlist)` calls the `__repr__` method and provides a formal representation of the object as shown below:

~~~
Playlist(name=My Favorite Songs)
~~~

The returned string should ideally contain information that can be used to recreate the object. "Recreating" an object, in the context of the `__repr__` method, means being able to create a new object that is identical or very similar to the original object based on the information provided by the `__repr__` method.

For example:

~~~
import datetime

date1 = datetime.datetime.now()
date2 = eval(repr(date1))

print("Repr of date1: ", repr(date1))
print("Repr of date2: ", repr(date2))

print(date1 == date2)
~~~

The above code snippet creates the `date2` object from the `repr()` string for `date1`, and then verifies that the values of both objects are equal.

Output:

~~~
Repr of date1:  datetime.datetime(2023, 6, 28, 12, 39, 25, 134013)
Repr of date2:  datetime.datetime(2023, 6, 28, 12, 39, 25, 134013)
True
~~~

Note that when you use the Python interactive shell and evaluate the line containing only the variable name `playlist`, the output displays the string representation returned by `__repr__()`.

~~~
>>> playlist = Playlist(name='My Favorite Songs') 
>>> playlist
Playlist(name=My Favorite Songs)
~~~

However, when you use the `print` function, the output displays the representation returned by `__str__()`.

~~~
>>> print(playlist)
Playlist Name: My Favorite Songs
~~~

> The main differences between the `__repr__` method and the `__str__` method in Python are their intended purposes and default behaviors. The`__repr__` method is designed to provide a formal and unambiguous string representation of an object. It is primarily used for debugging and development purposes. On the other hand, the `__str__` method is intended to provide a more readable and user-friendly string representation of an object. It is used when the `str()` function or the built-in `print()` function is called on an object.

### The `__len__` Method

The `__len__` method allows objects to define their length or size. It is called when the `len()` function is used on an object.

For example, let's add a `songs` attribute to the `Playlist` class and implement the `__len__` method:

~~~
class Playlist:
    def __init__(self, name, songs=[]):
        self.name = name
        self.songs = songs

    # Other Methods...

    def __len__(self):
        return len(self.songs)


playlist1 = Playlist("My Favorite Songs")
print(len(playlist1))

playlist2 = Playlist("My Favorite Songs", ["Song1", "Song2", "Song3"])
print(len(playlist2))
~~~

In this scenario, the `__len__` method is implemented to return the length of the `songs` attribute, representing the number of songs in the playlist.

Next, you create two instances of the `Playlist` class. The name is provided in the first instance, `playlist1`, but no songs are specified. In the second instance, `playlist2`, the name and a list of songs are provided.

Output:

~~~
0
3
~~~

### The `__getitem__` Method

The `__getitem__` method enables objects to support indexing and accessing elements using square brackets `[]`. By defining this method, you can treat objects as containers or sequences.

As of now, if you try to access any song of the playlist using the index, say `playlist[1]`, you'll get a `TypeError` as below:

~~~
print(playlist[1])
      ~~~~~~~~^^^
TypeError: 'Playlist' object is not subscriptable
~~~

Now, let's implement the `__getitem` method in the `Playlist` class to allow indexing to retrieve songs:

~~~
class Playlist:
    def __init__(self, name, songs=[]):
        self.name = name
        self.songs = songs
    
    # Other Methods...
    
    def __getitem__(self, index):
        return self.songs[index]


playlist = Playlist("My Favorite Songs", ["Song1", "Song2", "Song3"])
print(playlist[1])
~~~

In this example, the `__getitem__` method is implemented to return the song at the specified index of the `songs` list. When you print the `playlist[1]`, the `__getitem__` method is invoked with `1` as the index, resulting in the following output:

~~~
Song2
~~~

### The `__setitem__` Method

The `__setitem__` method allows objects to support item assignment using indexing. It is called when an item is assigned to an index using the assignment operator `=`.

Let's enhance the `Playlist` class to support item assignment:

~~~
class Playlist:
    def __init__(self, name, songs=[]):
        self.name = name
        self.songs = songs

    # Other Methods...

    def __setitem__(self, index, value):
        self.songs[index] = value


playlist = Playlist("My Favorite Songs", ["Song1", "Song2", "Song3"])
playlist[1] = "New Song"
print(playlist.songs)
~~~

In this code, the `__setitem__` method is implemented to assign a song to the specified index in the `songs` attribute. By executing `playlist[1] = "New Song"`, the `__setitem__` method is invoked with `1` as the index and `"New Song"` as the song, resulting in the modification of the playlist.

Output:

~~~
['Song1', 'New Song', 'Song3']
~~~

> Note: If you try to assign a new song that doesn't have an index in the songs attribute using `__setitem__`, it may not work as expected. By default, if the index doesn't exist, `__setitem__` will raise an `IndexError` indicating that the specified index is not found.

### The `__delitem__`  Method

The `__delitem__` method allows objects to support item deletion using indexing. It is called when an item is deleted using the `del` statement.

Let's extend the `Playlist` class to enable removing songs from the playlist:

~~~
class Playlist:
    def __init__(self, name, songs=[]):
        self.name = name
        self.songs = songs

    # Other Methods...

    def __delitem__(self, index):
        del self.songs[index]


playlist = Playlist("My Favorite Songs", ["Song1", "Song2", "Song3"])
print(playlist.songs)
del playlist[1]
print(playlist.songs)
~~~

In this example, the `__delitem__` method is implemented to delete the song at the specified index from the `songs` attribute. By executing `del playlist[1]`, the `__delitem__` method is called with `1` as the index, resulting in the deletion of the song at index `1`.

Output:

~~~
['Song1', 'Song2', 'Song3']
['Song1', 'Song3']
~~~

### The `__call__` Method

The `__call__` method enables objects to be called as if they were functions. It is invoked when parentheses `()` follow an object.

Let's implement the `__call__` method in the `Playlist` class:

~~~
class Playlist:
    def __init__(self, name, songs=[]):
        self.name = name
        self.songs = songs

    # Other Methods...

    def __call__(self):
        print("Playing the playlist...")


playlist = Playlist("My Favorite Songs", ["Song1", "Song2", "Song3"])
playlist()
~~~

In this example, when the object `playlist` is called using parentheses `()`, the `__call__` method is invoked, resulting in the following output:

~~~
Playing the playlist...
~~~

By implementing the `__call__` method, you made the `playlist` object callable, just like a function.

In this section, you explored commonly used magic methods in Python. The next section will teach you about operator overloading with magic methods. You will explore how you can redefine the behavior of operators like arithmetic operators, comparison operators, logical operators, and membership operators. This will further help you to create more expressive and versatile code.

## Operator Overloading With Magic Methods

Operator overloading is a concept in programming that allows you to give special meanings to operators when they are used with specific objects or data types. In simple terms, you can define what an operator does for your custom objects. Just like the `+` operator works differently for numbers and strings, you can make it work differently for your objects. This allows you to write code that looks more natural and intuitive.

For example, you can add or compare two objects using the custom logic you define. Operator overloading helps make your code more expressive and flexible by extending operators' capabilities beyond their default behaviors.

In this section, you will explore how magic methods enable you to overload the arithmetic, comparison, logical, and container operators and customize them as per your needs.

### Arithmetic Operators

You can customize the arithmetic operators such as addition (+), subtraction (-), multiplication (*), and division (/) for objects of a class by using their corresponding magic methods.

Here's a table that lists the internal magic methods associated with the arithmetic operators:

| Operator          | Internal Magic Method |
|-------------------|-----------------------|
| Addition          | `__add__`             |
| Subtraction       | `__sub__`             |
| Multiplication    | `__mul__`             |
| Division          | `__truediv__`         |
| Floor Division    | `__floordiv__`        |
| Remainder(Modulo) | `__mod__`             |
| Power             | `__pow__`             |

Consider a `Vector` class that represents a two-dimensional vector:

~~~
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Creating two vector objects
v1 = Vector(2, 3)
v2 = Vector(4, 5)
~~~

Next, you can define the magic methods to customize the behavior of the arithmetic operators.

#### The `__add__` Method

This method overloads the `+` operator and is used for adding two objects together.
For example:

~~~
def __add__(self, other):
return Vector(self.x + other.x, self.y + other.y)

# Addition
result = v1 + v2
print(result.x, result.y)
~~~

Output:

~~~
6 8
~~~

#### The `__sub__` Method

This method overloads the `-` operator and is used for subtracting one object from another.
For example:

~~~
def __sub__(self, other):
return Vector(self.x - other.x, self.y - other.y)

# Subtraction
result = v2 - v1
print(result.x, result.y)
~~~

Output:

~~~
2 2
~~~

#### The `__mul__` Method

This method overloads the `*` operator and is used for multiplying two objects together.
For example:

~~~
def __mul__(self, scalar):
    return Vector(self.x * scalar, self.y * scalar)

# Multiplication
result = v1 * 2
print(result.x, result.y)
~~~

Output:

~~~
4 6
~~~

#### The `__truediv__` Method

This method overloads the `/` operator and is used for dividing one object by another.
For example:

~~~
def __truediv__(self, scalar):
    return Vector(self.x / scalar, self.y / scalar)

# Division
result = v2 / 2
print(result.x, result.y)
~~~

Output:

~~~
2.0 2.5
~~~

You can find the entire code example on [GitHub](https://github.com/ashutoshkrris/magic-methods-tutorial/blob/main/operator-overloading/example1.py).

### Comparison Operators

Comparison operators such as less than (<), greater than (>), equal to (==), and not equal to (!=) can be customized using the corresponding magic methods.

Here's a table that lists the internal magic methods associated with the comparison operators:

| Operator                 | Internal Magic Method |
|--------------------------|-----------------------|
| Less than                | `__lt__`              |
| Less than or equal to    | `__le__`              |
| Equal to                 | `__eq__`              |
| Not equal to             | `__ne__`              |
| Greater than             | `__gt__`              |
| Greater than or equal to | `__ge__`              |

For instance, consider a `Point` class that represents a point in a two-dimensional space:

~~~

import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_from_origin(self):
        return math.sqrt(self.x**2 + self.y**2)

# Creating two point objects
p1 = Point(2, 3)
p2 = Point(4, 5)
~~~

In the above code, the `distance_from_origin` method calculates the distance of the point from the origin using the Pythagorean theorem.

Next, you can define the magic methods to compare points based on their distances from the origin.

#### The `__lt__` Method

This method overloads the `<` operator and is used for comparing if an object is less than another object. In the `Point` class example, the method compares the distances from the origin of two points and returns True if the distance of the current point is less than the distance of the other point.
For example:

~~~
def __lt__(self, other):
        return self.distance_from_origin() < other.distance_from_origin()

# Less than
result = p1 < p2
print(result)
~~~

Output:

~~~
True
~~~

#### The `__gt__` Method

This method overloads the `>` operator and is used for comparing if an object is greater than another object. In the Point class example, it compares the distances from the origin of two points and returns True if the distance of the current point is greater than the distance of the other point.
For example:

~~~
def __gt__(self, other):
        return self.distance_from_origin() > other.distance_from_origin()

# Greater than
result = p1 > p2
print(result)
~~~

Output:

~~~
False
~~~

#### The `__eq__` Method

This method overloads the `==` operator and is used for comparing if two objects are equal. In the `Point` class example, it compares the distances from the origin of two points and returns True if the distance of the current point is equal to the distance of the other point.
For example:

~~~
def __eq__(self, other):
return self.distance_from_origin() == other.distance_from_origin()

# Equal to
result = p1 == p2
print(result)
~~~

Output:

~~~
False
~~~

#### The `__ne__` Method

This method overloads the `!=` operator and is used for comparing if two objects are not equal. In the `Point` class example, it compares the distances from the origin of two points and returns True if the distance of the current point is not equal to the distance of the other point.
For example:

~~~
def __ne__(self, other):
        return self.distance_from_origin() != other.distance_from_origin()

# Not equal to
result = p1 != p2
print(result)
~~~

Output:

~~~
True
~~~

### Logical Operators

Logical operators `and` and `or` can also be customized for objects by implementing the magic methods `__and__` and `__or__`, respectively.

Consider a `Boolean` class that represents a boolean value and define the `__and__` and `__or__` magic methods to customize the behavior of logical operators:

~~~
class Boolean:
    def __init__(self, value):
        self.value = value

    def __and__(self, other):
        return Boolean(self.value and other.value)

    def __or__(self, other):
        return Boolean(self.value or other.value)
~~~

In the above code, the `__and__` method performs a logical AND operation on boolean objects, and the `__or__` method performs a logical OR operation.

~~~
# Creating two boolean objects
b1 = Boolean(True)
b2 = Boolean(False)

# Logical AND
result = b1 and b2
print(result.value)

# Logical OR
result = b1 or b2
print(result.value)
~~~

Output:

~~~
False
True
~~~

### Membership Operators

Membership operators `in` and `not in` can be customized using the `__contains__` magic method.

Consider a `ShoppingBasket` class that represents your general shopping baskets. You can define the `__contains__` magic method to customize the behavior of the `in` operator:

~~~
class ShoppingBasket:
    def __init__(self, items):
        self.items = items

    def __contains__(self, item):
        return item in self.items
~~~

In this example, the `__contains__` method checks if an item is present in the `items` list of the `ShoppingBasket` object.

~~~
# Creating a shopping basket object
my_basket = ShoppingBasket(["Apple", "Mango", "Pineapple"])

# Checking if an item exists in the basket
result = "Apple" in my_basket
print(result)

result = "Oranges" in my_basket
print(result)
~~~

Output:

~~~
True
False
~~~

In this section, you explored the concept of operator overloading with magic methods in Python. You learned how to redefine the behavior of various operators, such as arithmetic, comparison, logical, and membership operators, by implementing specific magic methods. In the next section, you'll learn about the concept of Context Managers in Python.

## Context Managers With Magic Methods

In Python, a class or a function that supports the `with` statement is known as a [Context Manager](https://earthly.dev/blog/python-with-statement/). The `open` function is an example of a context manager. With their magic methods, context managers offer a convenient way to manage resources and handle exceptions within a specific context. By defining the `__enter__` and `__exit__` methods, objects can be used as context managers, ensuring the proper setup and cleanup of resources.

In this section, you will explore the `__enter__` and `__exit__` methods, understand how to use the `with` statement and discover the benefits context managers bring to Python code.

### The `__enter__` and `__exit__` Methods

The `__enter__` and `__exit__` methods allow you to automatically set up and tear down resources when entering and exiting a context. The `__enter__` method is executed at the beginning of a `with` statement block and is responsible for acquiring the necessary resources or performing setup operations. The `__exit__` method is executed at the end of the `with` statement block and handles resource cleanup or any necessary finalization steps.

Here's an example that demonstrates the usage of `__enter__` and `__exit__` methods in a context manager:

~~~
class FileHandler:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        print("Opening the file...")
        self.file = open(self.filename, "w")
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()
        print("Closed the file...")


# Using the context manager
with FileHandler("example.txt") as file:
    print("Writing to the file...")
    file.write("Earthly is great!")
~~~

In the above code, the `FileHandler` class acts as a context manager. The `__enter__` method opens the specified file in write mode and returns the file object. This file object is assigned to the `file` variable in the `with` statement block. Once the block is exited, the `__exit__` method is automatically called, ensuring that the file is properly closed, regardless of any exceptions that may have occurred.

Output:

~~~
Opening the file...
Writing to the file...
Closed the file...
~~~

The above output shows the sequence of events. First, "Opening the file..." is printed, indicating that the `__enter__` method is being executed and the file is being opened. Then, "Writing to the file..." is printed, demonstrating that the code performs some operations with the file. Finally, "Closed the file..." is printed, signifying that the `__exit__` method is being executed and the context manager has properly closed the file.

> Learn more about context managers and the `with` statement in Python in [this tutorial](https://earthly.dev/blog/python-with-statement/).

## Conclusion

In this tutorial, you explored the world of magic methods in Python. You learned how magic methods fit into the object-oriented programming paradigm and saw examples of commonly used magic methods such as `__init__`, `__str__`, and `__len__`. You also explored operator overloading, where you can redefine the behavior of operators like `+`, `-`, and `==` using magic methods.

Next, you discovered the power of context managers with the `__enter__` and `__exit__` methods, which allow you to manage resources efficiently using the `with` statement.

However, this is just the tip of the iceberg. There is much more to discover and learn about magic methods. The best way to master magic methods is through practice and hands-on experience. So, go ahead and dive into your projects, explore different use cases, and unleash the power of magic methods to create elegant and powerful code in Python's object-oriented world. Happy coding!

You can find all the code samples used in the tutorial in this [GitHub repository](<https://github.com/as>

{% include_html cta/bottom-cta.html %}

## Outside Article Checklist

- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
  - Would any images look better `wide` or without the `figcaption`?
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links
