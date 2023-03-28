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

Since their introduction in Python 3.7, data classes have emerged as a popular choice for classes that store data. In a [previous tutorial](/blog/python-data-classes), we talked about what data classes are and some of their features, including out-of-the-box support for object comparison, type hints, and default values of fields.

In this follow-up tutorial, we'll continue to explore a few more features of Python data classes.

## Useful Features of Python Data Classes

~~~{.python caption="main.py"}
# main.py
@dataclass
class Student:
    name: str
    roll_no: str
    major: str
    year: str
    gpa: float
    classes: list = field(default_factory=list)
~~~



### Set More Complex Default Values With `default_factory`

~~~{.python caption="main.py"}
# main.py
@dataclass
class Student:
    name: str
    roll_no: str
    major: str
    year: str
    gpa: float
~~~

~~~{.python caption="main.py"}
import random
import string

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

### Exclude Fields from the Constructor

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


### Subclass Data Classes to Extend Functionality

### Use Slots for Improved Performance

## Conclusion

