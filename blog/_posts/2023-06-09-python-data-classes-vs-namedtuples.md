---
title: "Python Data Classes vs Named Tuples: Differences You Should Know"
categories:
  - Tutorials
toc: true
author: Bala Priya C

internal-links:
 - Python
---

Data classes, introduced in Python 3.7, provide a convenient way to define classes that are a collection of fields. But for such use cases, named tuples, built into the collections module in the Python standard library, are good choices too. Named tuples have been around since Python 2.6, and several features have been added in the recent Python 3.x releases.

Given that Python data classes are popular, are named tuples still relevant? What are the key differences between the two? Are there advantages of using one over the other—depending on what we’d like to do?

Let's take a closer look at both data classes and named tuples, and try to answer these questions.

To follow along, you need to have Python 3.8 or later version. To run the example on slots, you need Python 3.10.

## Python Data Classes and Named Tuples: An Overview

### Python Data Classes

In Python data classes are good choices when you need to create classes that store information and do not have a ton of functionality. Unlike regular Python classes, data classes require less boilerplate code, and come with default implementation of methods for string representation and comparing equality of attributes.

~~~{.python caption="main.py"}
from dataclasses import dataclass

@dataclass
class BookDC:
    title:str
    author:str
    genre:str
    standalone:bool
~~~


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

We would often need such objects to be immutable, perhaps, we can use tuples? However, with tuples, you need to remember what each of the field stands for—and access them using the index. You can consider switching to a dictionary because the keys will now indicate what the fields are. But you can modify a dictionary in place, so you may accidentally modify fields that you do not intend to. And each created tuple or dictionary object is an independent entity; there is no template that we can use to create objects of similar type.

Here's where named tuples can help. Named tuples are tuples with named attributes. So they give you the immutability of tuples and readability of dictionaries. In addition, once you define a named tuple of a specific type, you can use that to create many instances of that named tuple type.


~~~{.python caption="main.py"}
from collections import namedtuple

BookNT = namedtuple('BookNT','title author genre standalone')
~~~

~~~{.python caption="main.py"}
book2 = BookNT('Deep Work','Cal Newport','Nonfiction', True)
print(book2)
~~~

~~~{caption="Output"}
BookNT(title='Deep Work', author='Cal Newport', genre='Nonfiction', standalone=True)
~~~

## Data Classes vs Named Tuples: A Comprehensive Comparison

<div class="notice--big--primary">
TL; DR: If you want an immutable container data type with a small subset of fields taking default values, consider named tuples. If you want all the features and extensibility of Python classes, use data classes instead.
</div>

### Immutability

Data class instances are mutable by default. So you can modify the value of one or more fields after the instance has been created.

~~~{.python caption="main.py"}
book3 = BookDC('Elantris','Brandon Sanderson','Epic Fantasy',True)
~~~

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

Named tuples are tuples, too. s\So they are immutable. Meaning you cannot modify them in place. In this example, you cannot modify named tuple instances after they are created. If you try doing so you will run into errors.

~~~{caption="main.py"}
book2 = BookNT('Deep Work','Cal Newport','Nonfiction', True)
book2.title = 'Digital Minimalism'
~~~

~~~{caption="Output"}
Traceback (most recent call last):
  File "main.py", line 30, in <module>
    book2.title = 'Digital Minimalism'
AttributeError: can't set attribute
~~~

<div class="notice--big--primary">
**Can we have immutable data class instances and mutable named tuple instances?**
  
- You can make data class instances immutable by setting `frozen` to `True` in the `@dataclass` decorator. 
- But you *cannot* have mutable named tuple instances.

</div>

<div class="notice--info">
#### A Note on `_replace()`
Using the `_replace()` method, you can get a shallow copy of a named tuple instance where the value of a particular field is replaced with an updated value. 

~~~{caption="main.py"}
book2 = BookNT('Deep Work','Cal Newport','Nonfiction', True)
book2_copy = book2._replace(title='Digital Minimalism')
~~~

~~~{caption="main.py"}
print(book2.title)
print(book2_copy.title)
~~~

~~~{caption="Output"}
Deep Work
Digital Minimalism
~~~

You can as well use the `_replace()` method to create shallow copies of data class instances.
</div>

### Setting Default Values

When you create data classes you can specify the default values for one or more fields. 

~~~{.python caption="main.py"}
from dataclasses import dataclass

@dataclass
class BookDC:
    title:str
    author:str
    genre:str
    standalone:bool=True
~~~

~~~{.python caption="main.py"}
book4 = BookDC('Coraline','Neil Gaiman','Fantasy')
print(book4)
~~~

~~~{caption="Output"}
BookDC(title='Coraline', author='Neil Gaiman', genre='Fantasy', standalone=True)
~~~

But can you set default values in namedtuples? 

Though this may not be obvious, in Python 3.7+, you can use the `defaults` field in the `namedtuple()` factory function to set default values. You can set `defaults` to a list of `k` values to specify the default values for the last `k` fields.

~~~{.python caption="main.py"}
from collections import namedtuple

BookNT = namedtuple('BookNT','title author genre standalone',defaults=[True])
~~~

~~~{.python caption="main.py"}
book5 = BookNT('Piranesi','Susanna Clarke','Fantasy')
print(book5)
~~~

~~~{caption="Output"}
BookNT(title='Piranesi', author='Susanna Clarke', genre='Fantasy', standalone=True)
~~~

~~~{.python caption="main.py"}
print(book_5._field_defaults)
~~~

~~~{caption="Output"}
{'standalone': True}
~~~

downside: This can be hard to maintain if there are too many fields.

Aside: get default values
You can get all the default values using the `get_default()` method on the namedtuple instance. 

With Python data classes, you can also use `default_factory` to use any callable to initialize a field with default values.

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

~~~{.python caption="main.py"}
book4 = BookDC('Coraline','Neil Gaiman','Fantasy')
print(book4)
~~~

~~~{caption="Output"}
BookDC(title='Coraline', author='Neil Gaiman', genre='Fantasy', standalone=True, rating=5)
~~~

### Comparing Objects

Unlike a regular Python class that requires you to define dunder methods such as `__repr__` and `__eq__`, both data classes and namedtuples come with some built-in support for representation and object comparison.

We can compare two data class instances for equality. And when we compare two instances of different data classes with the same values for each attribute, we get `False` as expected. 

~~~{.python caption="main.py"}
from dataclasses import dataclass

@dataclass
class AnotherBookDC:
    title:str
    author:str
    genre:str
    standalone:bool=True
~~~

~~~{.python caption="main.py"}
book_a = BookDC('Coraline','Neil Gaiman','Fantasy')
print(book_a)

book_b = AnotherBookDC('Coraline','Neil Gaiman','Fantasy')
print(book_b)
~~~

~~~{caption="Output"}
BookDC(title='Coraline', author='Neil Gaiman', genre='Fantasy', standalone=True)
AnotherBookDC(title='Coraline', author='Neil Gaiman', genre='Fantasy', standalone=True)
~~~

~~~{.python caption="main.py"}
print(book_a == book_b)
False
~~~

But named tuples are just tuples. So compare two instances of different named tuple types with same values returns `True`.

~~~{.python caption="main.py"}
from collections import namedtuple

AnotherBookNT = namedtuple('AnotherBookNT','title author genre standalone',defaults=[True])
~~~

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

~~~{.python caption="main.py"}
print(book_a == book_b)
True
~~~

### Type Hints

From the way we create data classes and named tuples, it’s easy to see how data classes support type hints out of the box.

Since Python 3.6, you can use `NamedTuple` from the [typing]() module to add type hints for fields.

<show the list of tuples [(field_name,type),...] syntax here>

~~~{.python caption="main.py"}
BookNT = NamedTuple(
    "BookNT", [("title", str), ("author", str), ("genre", str), ("standalone", bool)]
)
book = BookNT("Six of Crows", "Leigh Bardugo", "Fantasy", False)
print(book)
~~~

~~~{caption="Output"}
BookNT(title='Six of Crows', author='Leigh Bardugo', genre='Fantasy', standalone=False)
~~~

In Python 3.8 and later, you can use the familiar class syntax and create NamedTuple instances with type hints. (Very similar to how you can create data classes.)

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
NamedTuple Types Are Tuple Subclasses

This means the `Derived` class inherits from the `Base` class. But this is not the case here. The namedtuple object is not a subclass of NamedTuple. Rather it’s a subclass of tuple.
~~~{.python caption="main.py"}
class Derived(Base):
     pass 
~~~

~~~{.python caption="main.py"}  
print(issubclass(BookNT,NamedTuple))
# False

print(issubclass(BookNT,tuple))
# True 
~~~
  

</div>

### Creating Objects and Accessing Fields

What this section should cover:

Named tuples are memory efficient than data classes. (But data classes with slots are more efficient.)

Also check if attribute access is faster for namedtuples than for data classes.

## Summing Up the Discussion

Let's wrap up our discussion by summarizing the key differences between data classes and named tuples.
 
|Features| Data Classes| NamedTuples|
|--------|-------------|------------|
|Immutability of instances|Mutable by default; Set `frozen = True` in the `@dataclass` to create immutable instances| Immutable by default|
|Default Values|Can set both literal defaults and complex defaults using `default_factory`| Use `defaults` to specify a list of default values for the last `k` fields|
|Type Hints|Out-of-the-box support for type hints|Use `typing.NamedTuple` to specify type hints for fields|
|Comparison|Comparison works as expected between two instances of the *same* data class| Comparison between two instances of *any* namedtuple type returns `True` so long as the attributes are equal|
|Memory Efficiency|Data classes with slots have lower memory footprint|More efficient than regular data classes|
|Maintability|(Almost always) easy to maintain|Can be hard to maintain, especially when there are many default fields|

## Conclusion

In this article we explored how data classes and named tuples can both help us create classes that store attributes. We then compared them across a set of features: from immutability to memory efficiency.

We chose data classes and named tuples for this discussion as they are both built into the Python standard library, but there are popular third-party Python packages—data class alternatives—to build such classes. When sifting through Python codebases, you'll have likely come across Python packages like [Pydantic]() and [atrrs](). These provide support for building such data classes while automating some best practices to work with Python classes. You may explore these packages and use them in your upcoming projects as needed.
