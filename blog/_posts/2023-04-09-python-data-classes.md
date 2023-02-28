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

In Python, classes let you group together data and behavior by defining attributes and methods, respectively. Typically, a class contains both attributes and a set of methods that add functionality. **But what if you have a class that stores a lot of attributes with almost no functionality?** Do you still need to use regular classes, or is there a better alternative? 

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

So which class do we pick: `Student` or `Employee`? 

![student-vs-employee-class]({{site.images}}{{page.slug}}/5.png)\

I’ll choose `Student` class for now. Let's get coding!

### The `__init__` Method

Let’s create a `Student` class with the attributes: `name`, `roll_no`, `major`, and `year`. To initialize instances of the `Student` class by passing in values for these attributes in the constructor, you can define the `__init__` method:

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

As seen, the default representation returned `<main.Student object at 0x007EE628>` is not very helpful; it does *not* contain any information on the attributes of the instance `jane`. If you need a helpful string representation of the object, you should implement the `__repr__` method. 

### Adding a Helpful `__repr__`

Let’s add a `__repr__` method that returns a string containing the values of the instance attributes:

~~~{.python caption="main.py"}
    def __repr__(self):
        return f"Student: {self.name} {self.roll_no} {self.major} {self.year}"
~~~

After adding the `__repr__`, the `Student` class should look like this:

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

Now go back to the REPL and look at the `__repr__` for `jane`:

~~~{.python caption="main.py"}
>>> jane
Student: Jane CS1234 Computer Science junior
~~~

That's much better! 

But remember, *you* added the `__repr__` method. *So it's only as helpful as you choose to make it*. You can as well write a `__repr__` that only returns the string "Student object". Clearly, such a `__repr__` is not more helpful than the default `<main.Student object at 0x007EE628>` (just saying!).

Next, create another instance of the `Student` class `also_jane` with the same values for the instance attributes:

~~~{.python caption=""}
>>> also_jane = Student('Jane','CS1234','Computer Science','junior')
~~~

You can verify the equality of the various attributes of `jane` and `also_jane`, like so:

~~~{.python caption=""}
>>> jane.name == also_jane.name
True
>>> jane.roll_no == also_jane.roll_no
True
>>> jane.major == also_jane.major
True
>>> jane.year == also_jane.year
True
~~~

**But what happens when you try to compare `jane` and `also_jane`?**

~~~{.python caption=""}
>>> jane == also_jane
False
~~~

Well, `jane == also_jane` returns `False`. **Why?**

![why]({{site.images}}{{page.slug}}/1.png)\

By default, the **==** operator compares the IDs of the two objects. And comparison of objects in terms of attributes doesn’t make sense until you implement the `__eq__` method. Okay, let's do that!

### Implementing the `__eq__` Method

For now, we know the following:

- Comparison is valid *only* between two objects belonging to the *same* class. 
- The values of the various instance variables of the two objects should be equal.

Let’s define the `__eq__` method to compare any two instances of two instances of the `Student` class:

~~~{.python caption="main.py"}
 def __eq__(self, another):
        if self.__class__ == another.__class__:
            return (self.name, self.roll_no, self.major, self.year) == (
                another.name,
                another.roll_no,
                another.major,
                another.year,
            )
        else:
            return "InvalidComparison"
~~~

When you try to check if `jane == also_jane` after adding the `__eq__` method, you'll see that it evaluates to `True` as expected:

~~~{.python caption=""}
>>> jane == also_jane
True
~~~

To create `Student` class with *four* attributes, a helpful string representation, and support for object comparison, we have the following in main.py:

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

    def __eq__(self, another):
        if self.__class__ == another.__class__:
            return (self.name, self.roll_no, self.major, self.year) == (
                another.name,
                another.roll_no,
                another.major,
                another.year,
            )
        else:
            return "InvalidComparison"
~~~

Suppose you need to add the GPA for each student, remove the `name` attribute and add two new attributes: `first_name` and `last_name`, the list of classes each student has taken, and a bunch more. 

**What do you do next?**

- You need to first update the `__init__` method. Cool. 
- How’ll you remember the newly added attributes if you don’t add them to the `__repr__`? Okay, so you’ll go and modify the `__repr__`. 
- Oh wait, you should update the `__eq__` method, too.

Clearly, it's not super fun anymore!

And as you keep modifying the class, you'll *likely* forget to update one of these. No, I'm not challenging you!

## How to Create Data Classes in Python

~~~{.python caption="main.py"}
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    roll_no: str
    major: str
    year: str
    gpa: float
~~~

~~~{.python caption=""}
>>> from main import Student
>>> jane = Student('Jane','CS1234','Computer Science','junior',3.98)
~~~

~~~{.python caption=""}
>>> jane
Student(name='Jane', roll_no='CS1234', major='Computer Science', year='junior', gpa=3.98)
~~~

~~~{.python caption=""}
>>> also_jane = Student('Jane','CS1234','Computer Science','junior',3.98)
>>> jane == also_jane
True
~~~

<div class="notice--big--primary">
### Where Did `__init__`, `__repr__`, and `__eq__` Come From?
  
![wondering]({{site.images}}{{page.slug}}/2.png)\

~~~{.python caption="main.py"} 
# main.py
from inspect import getmembers,isfunction
...
print(getmembers(Student,isfunction))
~~~

~~~{ caption="Output"} 
[('__eq__', <function __create_fn__.<locals>.__eq__ at 0x014F6A48>), ('__init__', <function __create_fn__.<locals>.__init__ at 0x014F6970>), ('__repr__', <function __create_fn__.<locals>.__repr__ at 0x014F6A00>)]
~~~

~~~{.python caption="main.py"} 
# main.py
from inspect import getmembers,isfunction
from pprint import pprint
...
pprint(getmembers(Student,isfunction))
~~~


~~~{ caption="Output"} 
[('__eq__', <function __create_fn__.<locals>.__eq__ at 0x014F6A48>),
('__init__', <function __create_fn__.<locals>.__init__ at 0x014F6970>),
('__repr__', <function __create_fn__.<locals>.__repr__ at 0x014F6A00>)]
~~~



</div>

<div class="notice--info">
### Create Data Classes With `make_dataclass`

To create a data class, you can also use `make_dataclass` from the dataclasses module:
  
~~~{.python caption=""}
from dataclasses import make_dataclass
Student = make_dataclass('Student',['name','roll_no','major','year','gpa'])
~~~
However, I prefer using the `@dataclass` decorator; the code is a lot easier to read and maintain, especially when there are many fields.
</div>

## Type Hints and Default Values in Python Data Classes

### How Do Type Hints Help? 

<div class="wide">
![type-hints-0]({{site.images}}{{page.slug}}/type-hints0.png)\
</div>

<div>
![type-hints-1]({{site.images}}{{page.slug}}/type-hints1.png)\
</div>

#### Enforcing Type Checks

~~~{.bash caption=">_"}
$ pip3 install mypy
~~~

~~~{ caption="Output"}
main.py:12: error: Argument 2 to "Student" has incompatible type "float"; expected "str"  [arg-type]
main.py:12: error: Argument 5 to "Student" has incompatible type "str"; expected "float"  [arg-type]
Found 2 errors in 1 file (checked 1 source file)
~~~


### Setting Default Values for Data Class Attributes

<div class="notice--big--primary">
#### The Curious Case of Mutable Default Arguments in Python

![curious]({{site.images}}{{page.slug}}/3.png)\
~~~{.python caption=""}
>>> def add_to_reading_list(item,this_list=[]):
...     if item not in this_list:
...         this_list.append(item)
...     return this_list
...
~~~
 
~~~{.python caption=""}
>>> books = ['Deep Work']
>>> new_book = 'Hyperfocus'
>>> add_to_reading_list(new_book,books)
['Deep Work', 'Hyperfocus']
~~~
  
~~~{.python caption=""}
>>> add_to_reading_list('Mindset')
['Mindset']
>>> add_to_reading_list('Grit')
['Mindset', 'Grit']
>>> add_to_reading_list('Flow')
['Mindset', 'Grit', 'Flow']
~~~
</div>


## Defining Methods in a Python Data Class

## Are Immutable Data Classes Helpful?

## Python Data Classes vs. NamedTuples

## Conclusion













