---
title: "Python Data Classes vs Named Tuples: Differences You Should Know"
categories:
  - Tutorials
toc: true
author: Bala Priya C

internal-links:
 - Python
---

Data classes, introduced in Python 3.7, provide a convenient way to define classes that are a collection of fields. But for such use cases, namedtuples, built into the collections module in the Python standard library, are good choices too. Namedtuples have been around since Python 2.6, and several features have been added in the recent Python 3.x releases.

Given that Python data classes are popular, are namedtuples still relevant? What are the key differences between the two? Are there advantages of using one over the other—depending on what we’d like to do?

Let's take a closer look at both data classes and namedtuples, and try to answer these questions.

## Python Data Classes and Named Tuples: An Overview

### Python Data Classes

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
TL; DR: If you want an immutable container data type with a small subset of fields taking default values, consider namedtuples. If you want all the features and extensibility of Python classes, use data classes instead.
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

Namedtuples are tuples, so they are immutable. Meaning you cannot modify them in place. In this example, you cannot modify namedtuple instances after they are created. If you try doing so you will run into errors.

~~~{caption="main.py"}
book2 = BookNT('Deep Work','Cal Newport','Nonfiction', True)
book2.title = 'Digital Minimalism'
~~~

~~~{caption="Output"}
Traceback (most recent call last):
  File "main.py", line 30, in <module>
    book3.title = 'Digital Minimalism'
AttributeError: can't set attribute
~~~

**Can we have immutable data class instances and mutable namedtuple instances?**
You can make data class instances immutable by setting `frozen` to `True` in the `@dataclass` decorator. But you *cannot* have mutable namedtuple instances.

<div class="notice--info">
#### A Note on `_replace()`
Using the `_replace()` method, you can get a shallow copy of a namedtuple instance where the value of a particular field is replaced with an updated value. 
  
This `_replace()` method can also be used to create shallow copies of data class instances.
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

downside: This can be hard to maintain if there are too many fields.

Aside: get default values
You can get all the default values using the `get_default()` method on the namedtuple instance. 

With Python data classes, you can also use `default_factory` to use any callable to initialize a field with default values.

### Comparing Objects

Unlike a regular Python class that requires you to define dunder methods such as `__repr__` and `__eq__`, both data classes and namedtuples come with some built-in support for representation and object comparison.

We can compare two data class instances for equality. 

But namedtuples are just tuples. So they’ll also compare two instances of different namedtuple types. :/


### Type Hints

From the way we create data classes and namedtuples, it’s easy to see how data classes support type hints out of the box.

Since Python 3.6, you can use `NamedTuples` from the typing module to add type hints for fields.

<show the list of tuples [(field_name,type),...] syntax here>

~~~{.python caption="main.py"}
from dataclasses import dataclass, field


~~~

In Python 3.8 and later, you can use the familiar class syntax and create NamedTuple instances with type hints. (Very similar to how you can create data classes.)

~~~{.python caption="main.py"}



~~~

<div class="notice--big--primary">
All Instances are Tuple Subclasses
```
class Derived(Base):
     pass 
```
This means the `Derived` class inherits from the `Base` class. But this is not the case here. The namedtuple object is not a subclass of NamedTuple. Rather it’s a subclass of tuple.
</div>

### Creating Objects and Accessing Fields

What this section should cover:

Named tuples are memory efficient than data classes. (But data classes with slots are more efficient.)

Also check if attribute access is faster for namedtuples than for data classes.

## Summing Up the Discussion
 
|Features| Data Classes| NamedTuples|
|--------|-------------|------------|
|Immutability of instances|Mutable by default; Set `frozen = True` in the `@dataclass` to create immutable instances| Immutable by default|
|Default Values|Can set both literal defaults and complex defaults using `default_factory`| Use `defaults` to specify a list of default values for the last `k` fields|
|Type Hints|Out-of-the-box support for type hints|Use `typing.NamedTuple` to specify type hints for fields|
|Comparison|Comparison is valid *only* between two instances of the same data class| Can compare two instances of any namedtuple type (not very useful!)|
|Memory Efficiency|Data classes with slots have lower memory footprint|More efficient than regular data classes|
|Maintability|(Almost always) easy to maintain|Can be hard to maintain, especially when there are many default fields|

## Conclusion

<wrap up discussion>
<pointers to explore other related pkgs>

When sifting through Python codebases, you’d have also come across third-party Python packages like [Pydantic]() and [atrrs](). These provide support for building such data classes and automating some best practices to work with Python classes.
