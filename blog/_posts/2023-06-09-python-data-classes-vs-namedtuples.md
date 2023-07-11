---
title: "Python Data Classes vs Named Tuples: Differences You Should Know"
categories:
  - Tutorials
toc: true
author: Bala Priya C

internal-links:
 - Python
excerpt: |
    In this article, we explore the differences between Python data classes and named tuples. We discuss their features, such as immutability, default values, type hints, comparison, memory efficiency, and maintainability. Whether you're a beginner or an experienced Python developer, understanding these differences can help you make informed decisions when choosing between data classes and named tuples for your projects.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about Python data classes vs named tuples. Earthly is a powerful build tool that can be used in conjunction with Python projects, including those that utilize data classes and named tuples. [Check us out](/).**

[Data classes](/blog/python-data-classes), introduced in Python 3.7, provide a convenient way to define classes that are a collection of fields. But for such use cases, named tuples, built into the collections module in the Python standard library, are good choices too. Named tuples have been around since Python 2.6, and several features have been added in the recent Python 3.x releases.

Given that Python data classes are popular, are named tuples still relevant? What are the key differences between the two? Are there advantages of using one over the other—depending on what we'd like to do?

Let's take a closer look at both data classes and named tuples, and try to answer these questions.

To follow along, you need to have Python 3.8 or later version. To run the example on slots, you need Python 3.10. You can find the code examples used in this tutorial [on GitHub](https://github.com/balapriyac/dataclasses-tutorial/tree/main/dataclasses-vs-namedtuples).

## Python Data Classes and Named Tuples: An Overview

We'll start by reviewing the basics of data classes and named tuples.

### Python Data Classes

In Python [data classes](/blog/python-data-classes) are good choices when you need to create classes that store information and do not have a ton of functionality. [Unlike regular Python classes](/blog/python-data-classes/#python-classes-and-boilerplate-code), data classes require less boilerplate code, and come with default implementation of methods for string representation and comparing equality of attributes.

We'll use the following `BookDC` data class that contains fields such as `title`, `author`, `genre`, and more.

~~~{.python caption="main.py"}
from dataclasses import dataclass

@dataclass
class BookDC:
    title:str
    author:str
    genre:str
    standalone:bool
~~~

After creating the `BookDC` data class, we can create instances by passing in the values for the various fields in the constructor:

~~~{.python caption="main.py"}

book1 = BookDC('To the Lighthouse','Virginia Woolf','Modernism',True)
print(book1)
~~~

~~~{caption="Output"}
BookDC(
    title="To the Lighthouse",
    author="Virginia Woolf",
    genre="Modernism",
    standalone=True,
)
~~~

### What Are Named Tuples?

When you want to store attributes and efficiently look up and use the values, do we need classes at all? Won't basic data structures like lists, tuples, and dictionaries suffice?

We would often need such objects to be immutable, perhaps, we can use tuples? However, with tuples, we need to remember what each of the field stands for—and access them using the index.

We can consider switching to a dictionary because the keys will now indicate what the fields are. But we *can* modify a dictionary in place, so we may accidentally modify fields that you do not intend to. And each created tuple or dictionary object is an independent entity; there is no template that we can use to create objects of similar type.

![image]({{site.images}}{{page.slug}}/1.png)\

Here's where named tuples can help. Named tuples are tuples with **named attributes**. So they give you the immutability of tuples and readability of dictionaries. In addition, once you define a named tuple of a specific type, you can use that to create many instances of that named tuple type.

To create a named tuple, you can use `namedtuple` from the `collections` module that is built into the Python standard library. You can pass in the named tuple type (this is analogous to the class name) and the fields as a space-delimited string. You can as well pass in the field names as a list of strings.

`BookNT` is the functional named tuple equivalent of the `BookDC` data class:

~~~{.python caption="main.py"}
from collections import namedtuple

BookNT = namedtuple('BookNT','title author genre standalone')
~~~

You can now create instances of `BookNT`:

~~~{.python caption="main.py"}
book2 = BookNT('Deep Work','Cal Newport','Nonfiction', True)
print(book2)
~~~

~~~{caption="Output"}

BookNT(title='Deep Work', author='Cal Newport', genre='Nonfiction', standalone=True)
~~~

## Data Classes vs Named Tuples: A Comprehensive Comparison

<div class="notice--big--primary">
🔖 **TL; DR**: If you want an immutable container data type with a small subset of fields taking default values, consider named tuples. If you want all the features and extensibility of Python classes, use data classes instead.
  
Factoring in the memory footprint: named tuples are much more memory efficient than data classes, but data classes with slots are more memory efficient.
</div>

### Immutability

Data class instances are mutable by default. So you can modify the value of one or more fields after the instance has been created.

Consider the following instance of the `BookDC` data class:

~~~{.python caption="main.py"}

book3 = BookDC('Elantris','Brandon Sanderson','Epic Fantasy',True)
~~~

Let's update the `title` and `standalone` fields of `book3`:

~~~{.python caption="main.py"}
book3.title = 'Mistborn'
book3.standalone = False

print(book3)
~~~

~~~{caption="Output"}
BookDC(
    title="Mistborn", author="Brandon Sanderson", genre="Epic Fantasy", standalone=False
)
~~~

**Named tuples are tuples, too**. So they are immutable. Meaning you cannot modify them in place. In this example, you cannot modify named tuple instances after they are created. If you try doing so you will run into errors.

Try updating the `title` field of the `book2` instance we created:

~~~{caption="main.py"}
book2 = BookNT('Deep Work','Cal Newport','Nonfiction', True)
book2.title = 'Digital Minimalism'
~~~

You'll see that it results in an `AttributeError` exception:

~~~{caption="Output"}
Traceback (most recent call last):
  File "main.py", line 30, in <module>
    book2.title = 'Digital Minimalism'
AttributeError: can't set attribute
~~~

📑 So far, we know that data class instances are mutable by default, and named tuple instances are immutable. **But can we have immutable data class instances and mutable named tuple instances?**
  
- You can make data class instances immutable by setting `frozen` to `True` in the `@dataclass` decorator.
- But you *cannot* have mutable named tuple instances.

<div class="notice--info">
#### 📌 A Note on `_replace()`
<br>
Using the `_replace()` method, you can get a *shallow copy* of a named tuple instance where the value of a particular field is replaced with an updated value. As an example, create a shallow copy of the `book2` instance with a modified `title` field:

~~~{.python caption="main.py"}
book2 = BookNT('Deep Work','Cal Newport','Nonfiction', True)
book2_copy = book2._replace(title='Digital Minimalism')
~~~

The `title` field of the shallow copy `book2_copy` has been updated while the `title` of `book2` remains unchanged:

~~~{.python caption="main.py"}
print(book2.title)
print(book2_copy.title)
~~~

~~~{.md caption="Output"}
Deep Work
Digital Minimalism
~~~

You can as well use the `_replace()` method to create shallow copies of data class instances.
</div>

### Setting Default Values

When you create data classes you can specify the default values for one or more fields.

Here we set the `standalone` field in the `BookDC` data class to take a default value of `True`:

~~~{.python caption="main.py"}
from dataclasses import dataclass

@dataclass
class BookDC:
    title:str
    author:str
    genre:str
    standalone:bool=True
~~~

We instantiate an object for Neil Gaiman's book Coraline *without* specifying the value of `standalone` in the constructor:

~~~{.python caption="main.py"}
book4 = BookDC('Coraline','Neil Gaiman','Fantasy')
print(book4)
~~~

And the `standalone` field takes the default value of `True`:

~~~{caption="Output"}

BookDC(title='Coraline', author='Neil Gaiman', genre='Fantasy', standalone=True)
~~~

**But can you set default values in named tuples?**

Though this may not be obvious, in Python 3.7+, you can use the `defaults` field in the `namedtuple()` factory function to set default values. You can set `defaults` to a list of `k` values to specify the default values for the last `k` fields.

Let's specify the default value for `standalone` in the `BookNT` named tuple. Here the `defaults` list contains only one element, `True`, the default value of the last field `standlone`:

~~~{.python caption="main.py"}
from collections import namedtuple

BookNT = namedtuple('BookNT','title author genre standalone',defaults=[True])
~~~

The `standalone` field of any instance created without the specifying its value in the function call will now be set to `True`:

~~~{.python caption="main.py"}
book5 = BookNT('Piranesi','Susanna Clarke','Fantasy')
print(book5)
~~~

~~~{caption="Output"}

BookNT(title='Piranesi', author='Susanna Clarke', genre='Fantasy', standalone=True)
~~~

When you want to look up all the default values, you can check the `_field_defaults` attribute of the named tuple instances:

~~~{.python caption="main.py"}
print(book_5._field_defaults)
~~~

The `_field_defaults` attribute is a dictionary of containing the fields with default values and the corresponding default values as key-value pairs:

~~~{caption="Output"}
{'standalone': True}
~~~

Though we can add literal defaults in named tuples, it can be hard to maintain if there are too many fields.

<div class="notice--info">
#### 📑 Initializing Default Values With Default Factory
<br>
Both data classes and named tuples support setting literal defaults. With Python data classes, you can also use `default_factory` to use any callable to initialize a field with default values.
  
For the `BookDC` class, we can add a `rating` field that is initialized with a default value whenever a data class instance is created without specifying the `rating` field.

Here `get_rating()` is a simple function that returns a number between 1 and 5 (yeah, not the best way to rate a book!). The `default_factory` initializes the `rating` field with a default value by calling the `get_rating()` function.

~~~{.python caption="main.py"}
from dataclasses import dataclass, field
import random

def get_rating():
    return random.choice(range(3,6))

@dataclass
class BookDC:
    title:str
    author:str
    genre:str
    standalone:bool=True
    rating:str=field(default_factory=get_rating)
~~~

Now both `standalone` and `rating` are *optional* fields in the constructor:

~~~{.python caption="main.py"}
book4 = BookDC('Coraline','Neil Gaiman','Fantasy')
print(book4)
~~~

~~~{.md caption="Output"}

BookDC(title='Coraline', author='Neil Gaiman', genre='Fantasy', standalone=True, rating=5)
~~~

</div>

### Comparing Instances

![image]({{site.images}}{{page.slug}}/4.png)\

Unlike a regular Python class that requires you to define dunder methods such as `__repr__` and `__eq__`, both data classes and named tuples come with some built-in support for representation and object comparison.

Suppose we have `AnotherBookDC`, another data class with the same fields as `BookDC`.

~~~{.python caption="main.py"}
from dataclasses import dataclass

@dataclass
class AnotherBookDC:
    title:str
    author:str
    genre:str
    standalone:bool=True
~~~

In this example, `book_a` and `book_b` are instances of `BookDC` and `AnotherBookDC`, respectively:

~~~{.python caption="main.py"}
book_a = BookDC('Coraline','Neil Gaiman','Fantasy')
print(book_a)

book_b = AnotherBookDC('Coraline','Neil Gaiman','Fantasy')
print(book_b)
~~~

And both the instances take the same values for all the fields:

~~~{caption="Output"}

BookDC(title='Coraline', author='Neil Gaiman', genre='Fantasy', standalone=True)
AnotherBookDC(title='Coraline', author='Neil Gaiman', genre='Fantasy', standalone=True)
~~~

But when we check for equality, we get `False`:

~~~{.python caption="main.py"}
print(book_a == book_b)
# False
~~~

Which is expected because they are instances of two *different* data classes—though they have identical values.

But what happens when you try to do the same for name tuples? Well, named tuples are just tuples. So comparing two named tuples with identical values — whether they are instances of the same or different named tuple type — returns `True`.

~~~{.python caption="main.py"}
from collections import namedtuple

AnotherBookNT = namedtuple('AnotherBookNT','title author genre standalone',defaults=[True])
~~~

Create instances of both `BookNT` and `AnotherBookNT`. Make sure they have identical values for the fields:

~~~{.python caption="main.py"}
book_a = BookNT('Piranesi','Susanna Clarke','Fantasy')
print(book_a)

book_b = AnotherBookNT('Piranesi','Susanna Clarke','Fantasy')
print(book_b)
~~~

~~~{caption="Output"}

BookNT(title='Piranesi', author='Susanna Clarke', genre='Fantasy', standalone=True)
AnotherBookNT(title='Piranesi', author='Susanna Clarke', genre='Fantasy', standalone=True)
~~~

Though they are instances of two different named tuple types, element-wise equality between them holds `True` and the comparison returns `True`.

~~~{.python caption="main.py"}
print(book_a == book_b)
# True
~~~

### Type Hints

From the way we create data classes and named tuples, it's easy to see how data classes support type hints out of the box.

Since Python 3.6, you can use `NamedTuple` from the [typing](https://docs.python.org/3/library/typing.html) module to add type hints for fields. You can pass in the field names and their corresponding types as a *list of tuples*. Here's how you can add type hints to the `BookNT` named tuple:

~~~{.python caption="main.py"}
from typing import NamedTuple

BookNT = NamedTuple(
    'BookNT', [('title', str), ('author', str), ('genre', str), ('standalone', bool)]
)
book = BookNT('Six of Crows', 'Leigh Bardugo', 'Fantasy', False)
print(book)
~~~

~~~{caption="Output"}

BookNT(title='Six of Crows', author='Leigh Bardugo', genre='Fantasy', standalone=False)
~~~

You can also use the familiar class syntax and create named tuple instances with type hints. This is very similar to how you create data classes:

~~~{.python caption="main.py"}
from typing import NamedTuple

class BookNT(NamedTuple):
    title:str
    author:str
    genre:str
    standalone:bool=True
~~~

~~~{.python caption="main.py"}
book = BookNT('Six of Crows','Leigh Bardugo','Fantasy',False)
print(book)
~~~

~~~{caption="Output"}

BookNT(title='Six of Crows', author='Leigh Bardugo', genre='Fantasy', standalone=False)
~~~

<div class="notice--big--primary">
#### 🏷️ All NamedTuple Types Are Tuple Subclasses
<br>
Consider the following code snippet:

~~~{.python caption=""}
class Derived(Base):
     pass 
~~~

We use such a construct when creating subclasses that inherit from a base class; the `Derived` class inherits from the `Base` class. Notice that we use a similar syntax when creating named tuple types.
  
~~~{.python caption=""}
class SomeNamedTuple(NamedTuple):
     pass 
~~~

Though this may look like `SomeNamedTuple` is a subclass of `NamedTuple`, `SomeNamedTuple` *is* a subclass of tuple and not `NamedTuple`. You can verify this using the built-in `issubclass()` function:

~~~{.python caption="main.py"}  
print(issubclass(BookNT,NamedTuple))
# False

print(issubclass(BookNT,tuple))
# True 
~~~

</div>

### Memory Footprint and Attribute Access

![image]({{site.images}}{{page.slug}}/3.png)\

How do data classes and named tuples compare in terms of memory footprint? Is one more memory efficient than the other? We'll answer these questions in a bit.

To get the approximate size of the objects in memory, we'll use [Pympler](https://pypi.org/project/Pympler/)'s `asizeof` module. Install `pympler` using `pip`: `pip install pympler`.

In the snippet below, `book_dc` and `book_nt` are instances of the `Book_DC` and `Book_NT` data class, respectively.

~~~{.python caption="main.py"}
from pympler.asizeof import asizeof

book_dc = BookDC('Hyperfocus','Chris Bailey','Nonfiction',True)
book_nt = BookNT('Hyperfocus','Chris Bailey','Nonfiction',True)

s1 = asizeof(book_dc)
s2 = asizeof(book_nt)

print(f"Size of BookDC data class: {s1}")
print(f"Size of BookNT named tuple: {s2}")
~~~

We see that the name tuple instance `book_nt` takes up much less memory than the data class instance `book_dc`:

~~~{caption="Output"}
Size of BookDC data class: 608
Size of BookNT named tuple: 296
~~~

<div class="notice--info">
#### 🔖 Named Tuples and Tuples Have the Same Memory Footprint
<br>
The size of any named tuple instance is the same as that of a simple tuple. Let's verify this:

~~~{.python caption="main.py"}
book_t = ('Hyperfocus','Chris Bailey','Nonfiction',True)

from pympler.asizeof import asizeof
size_book_t = asizeof(book_t)
print(size_book_t)
# 296 (equal to the size of `book_nt`)
~~~

</div>

You can use slots to make [data classes more memory efficient](/blog/more-on-python-data-classes/#use-slots-for-more-efficient-data-classes). Using slots prevents the creation of the instance variables dictionary resulting in substantial memory savings.

To use slots you can set `slots` to `True` in the `@dataclass` decorator:

~~~{.python caption="main.py"}
from dataclasses import dataclass, field

@dataclass(slots=True)
class BookDC:
    title:str
    author:str
    genre:str
    standalone:bool=True
~~~

Create an instance of data class that uses slots:

~~~{.python caption="main.py"}

book_dc_slots = BookDC('Hyperfocus','Chris Bailey','Nonfiction',True)
~~~

As seen, the size of a data class instance with slots is smaller than that of a named tuple.

~~~{caption="Output"}
Size of BookDC data class with slots: 288
~~~

When comparing attribute access speeds, both data classes and named tuples seem to have almost similar performance. In this example, we access the `title` field of both the data class and named tuple instance:

~~~{.python caption="main.py"}
from functools import partial
import timeit

def get(book):
    book.title

t1 = min(timeit.repeat(partial(get,book_dc)))
t2 = min(timeit.repeat(partial(get,book_nt)))

print(f"Attribute access time for data class instance: {t1:.2f}")
print(f"Attribute access time for named tuple instance: {t2:.2f}")
~~~

The following results are for Python 3.10 on Ubuntu 22.04 LTS:

~~~{caption="Output"}
Attribute access time for data class instance: 0.05
Attribute access time for named tuple instance: 0.06
~~~

## Summing Up the Discussion

Let's wrap up our discussion by summarizing the key differences between data classes and named tuples.

![image]({{site.images}}{{page.slug}}/2.png)\

|Features| Data Classes| Named Tuples|
|