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

