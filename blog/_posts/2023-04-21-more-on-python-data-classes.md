---
title: "Let's Learn More About Python Data Classes"
categories:
  - Tutorials
toc: true
author: Bala Priya C

internal-links:
 - Python
 - Python Classes
---

Since their introduction in Python 3.7, data classes have emerged as a popular choice for Python classes that store data. In a [previous tutorial](/blog/python-data-classes), we talked about what data classes are and some of their features, including out-of-the-box support for object comparison, type hints, and default values of fields. In this follow-up tutorial, we'll continue to explore a few more features of Python data classes. 

Over the next few minutes, we'll take a closer look at setting default values with `default_factory`, initializing new fields from pre-existing fields with `__post_init__`, and much more. We'll also discuss the *improved* support for `__slots__` in data classes since Python 3.10.

Let's get started!

## Useful Features of Python Data Classes

<div class="notice--big--primary">
### Before You Begin
This tutorial assumes a basic understanding of Python data classes. You need Python 3.10 or a later version to run the code example in the section on `__slots__`. All other code snippets will work as expected with Python 3.7+.
</div>

To keep things simple, I'll use the `Student` class from the previous tutorial on data classes:

~~~{.python caption="main.py"}
# main.py
from dataclasses import dataclass, field


@dataclass
class Student:
    name: str
    roll_no: str
    major: str
    year: str
    gpa: float
    classes: list = field(default_factory=list)
~~~

Before we go any further, let's review what we know about data classes.

**What we've learned thus far:**

- Data classes have a default implementation of the `__init__`, `__repr__`, and `__eq__` methods. 
- They support type hints and default values for fields. Data class definitions do not allow mutable default arguments for fields.
- All data class instances are *mutable* by default, but you can set the `frozen` parameter to `True` in the `@dataclass` decorator to make instances immutable.

### Set More Complex Default Values With `default_factory`

`classes: list = field(default_factory=list)`

- Remove the `classes` field.
- Rename the `roll_no` field to `roll_num`.

~~~{.python caption="main.py"}
# main.py
@dataclass
class Student:
    name: str
    roll_num: str
    major: str
    year: str
    gpa: float
~~~

~~~{.python caption="main.py"}
import random
import string

random.seed(42)
alphabet = string.ascii_uppercase + string.digits

def generate_roll_num():
    roll_num = ''.join(random.choices(alphabet,k=9))
    return roll_num
~~~

~~~{.python caption="main.py"}
# main.py
@dataclass
class Student:
    name: str
    major: str
    year: str
    gpa: float
    roll_num: str = field(default_factory=generate_roll_num)
~~~

~~~{.python caption=""}
>>> from main import Student
>>> jane = Student('Jane','Computer Science','senior',3.99)
>>> jane
~~~

~~~{ caption="Output"}
Student(name='Jane', major='Computer Science', year='senior', gpa=3.99, roll_num='XAJI0Y6DP')
~~~

### Exclude Fields from the Constructor

~~~{.python caption=""}
>>> julia = Student('Julia','Economics','junior',3.72,"don't know")
>>> julia
~~~

~~~{ caption="Output"}
Student(name='Julia', major='Economics', year='junior', gpa=3.72, roll_num="don't know")
~~~

~~~{.python caption="main.py"}
# main.py
@dataclass
class Student:
    name: str
    major: str
    year: str
    gpa: float
    roll_num: str = field(default_factory=generate_roll_num, init=False)
~~~

~~~{.python caption=""}
>>> jake = Student('Jake','Math','sophomore',3.33,'MyRollNum')
~~~

~~~{ caption="Output"}
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: __init__() takes 4 positional arguments but 5 were given
~~~

### Use `__post_init__` to Create Fields Post Initialization

~~~{.python caption="main.py"}
@dataclass
class Student:
    first_name: str
    last_name: str
    major: str
    year: str
    gpa: float
    roll_num: str = field(default_factory=generate_roll_num, init=False)
    email: str = field(init=False)
~~~

~~~{.python caption="main.py"}
# main.py
    def __post_init__(self):
        self.email = f"{self.first_name}.{self.last_name}@uni.edu"
~~~

~~~{.python caption=""}
>>> jane = Student('Jane','Lee','Computer Science','senior',3.99)
>>> jane
~~~

~~~{ caption="Output"}
Student(first_name='Jane', last_name='Lee', major='Computer Science', year='senior', gpa=3.99, roll_num='XAJI0Y6DP', email='Jane.Lee@uni.edu')
~~~


### Order and Sort Data Class Instances

~~~{.python caption="main.py"}
@dataclass(order=True)
class Student:
    sort_index:int = field(init=False,repr=False)
    first_name: str
    last_name: str
    major: str
    year: str
    gpa: float
    roll_num: str = field(default_factory=generate_roll_num, init=False)
    email: str = field(init=False)
    tuition: int = 10000
~~~

~~~{.python caption="main.py"}
jane = Student('Jane','Lee','Computer Science','senior',3.99)
julia = Student('Julia','Doe','Economics','junior',3.63,27000)
~~~

~~~{.python caption="main.py"}
print(julia > jane)
~~~

~~~{ caption="Output"}
Traceback (most recent call last):
  File "main.py", line 52, in <module>
    print(julia > jane)
TypeError: '>' not supported between instances of 'Student' and 'Student'
~~~
  
### Subclass Data Classes to Extend Functionality

### Use Slots for Improved Performance

## Conclusion

And that's a wrap. So did we cover *everything* about data classes? No. But these are what you'll need when working with data classes.

