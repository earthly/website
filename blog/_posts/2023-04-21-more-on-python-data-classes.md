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

This tutorial assumes a basic understanding of [Python data classes](/blog/python-data-classes/).

- To run the code example in the section on `__slots__`, you need Python 3.10 or a later version.
- All other code snippets will work as expected with Python 3.7+.
</div>

To keep things simple, I'll use the `Student` class from the previous tutorial on data classes:

~~~{.python caption="main.py"}
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

Before we go any further, let's review what we *know* about data classes.

**What we've learned thus far**:

- Data classes have a default implementation of the `__init__`, `__repr__`, and `__eq__` methods.
- They support type hints and default values for fields. Data class definitions do not allow mutable default arguments for fields.
- All data class instances are *mutable* by default, but you can set the `frozen` parameter to `True` in the `@dataclass` decorator to make instances immutable.

Now let's go beyond the basics of data classes!

### Set More Complex Default Values With `default_factory`

Previously, we talked about how data classes allow us to specify [default values for fields](/blog/python-data-classes/), both literals and callables. We also learned that they *do not* allow us to use *mutable defaults*. If you remember, we added a `classes` field, and used the `field()` function with `default_factory` set to the callable `list`, `classes: list = field(default_factory=list)`.

However, you can use `default_factory` for other built-in and user-defined functions as well.

Now, let's modify the `Student` data class a bit:

- Remove the `classes` field.
- Rename the `roll_no` field to `roll_num`. (Why? `roll_num` reads better than `roll_no`!)

At this point, the `Student` data class looks like this:

~~~{.python caption="main.py"}
from dataclasses import dataclass, field


@dataclass
class Student:
    name: str
    roll_num: str
    major: str
    year: str
    gpa: float
~~~

Next, let's define a `generate_roll_num()` function that returns a `roll_num` string. The returned string is nine characters long, the characters sampled at random from the `alphabet` of uppercase letters and the digits 0-9:

~~~{.python caption="main.py"}
import random
random.seed(42)
import string
...
alphabet = string.ascii_uppercase + string.digits

def generate_roll_num():
    roll_num = ''.join(random.choices(alphabet,k=9))
    return roll_num
...
~~~

As default arguments should follow non-default arguments, let’s move `roll_num` as the last field in the data class definition. And set `default_factory` in the `field()` function to `generate_roll_num`.

~~~{.python caption="main.py"}
from dataclasses import dataclass, field


@dataclass
class Student:
    name: str
    major: str
    year: str
    gpa: float
    roll_num: str = field(default_factory=generate_roll_num)
~~~

The `default_factory` calls the `generate_roll_num` function to initialize the `roll_num` field with a *default* value - whenever an instance of the `Student` class is created.

Let’s instantiate a `Student` object to verify this:

~~~{.python caption=""}
>>> from main import Student
>>> jane = Student('Jane','Computer Science','senior',3.99)
>>> jane
~~~

And we see that `jane` has a `roll_num` field:

~~~{ caption="Output"}
Student(
    name="Jane", major="Computer Science", year="senior", gpa=3.99, roll_num="XAJI0Y6DP"
)
~~~

### Exclude Fields from the Constructor

Setting a default value makes a field *optional* in the constructor. And the default value is used only if the user does *not* provide the value for that field in the constructor.

So users of the class can still pass in whatever they like for the `roll_num` field. Here's an example:

~~~{.python caption=""}
>>> julia = Student('Julia','Economics','junior',3.72,"don't know")
>>> julia
~~~

For the `Student` object `julia`, the `roll_num` field has been set to the string "don't know":

~~~{ caption="Output"}
Student(name='Julia', major='Economics', year='junior', gpa=3.72, roll_num="don't know")
~~~

Suppose you need the following behavior instead: Users are *required* to use the roll numbers generated by the `generate_roll_num` function; they should not be able to initialize this field.

![email]({{site.images}}{{page.slug}}/2.png)\

**So how do we do that?** The field function also has an `init` parameter that we can set to `False`.

~~~{.python caption="main.py"}
from dataclasses import dataclass, field


@dataclass
class Student:
    name: str
    major: str
    year: str
    gpa: float
    roll_num: str = field(default_factory=generate_roll_num, init=False)
~~~

Now try initializing the `roll_num` field by passing in a value to the constructor:

~~~{.python caption=""}
>>> jake = Student('Jake','Math','sophomore',3.33,'MyRollNum')
~~~

You'll get the following error:

~~~{ caption="Output"}
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: __init__() takes 4 positional arguments but 5 were given
~~~

The traceback reads that the constructor can take *only* four positional arguments; it cannot take the fifth positional argument corresponding to the `roll_num` field. So now, the only way to initialize `roll_num` is to use the `generate_roll_num()` function. And that's the behavior we wanted, yes? Great. What's next?

<div class="notice--info">
#### A Note on Keyword-Only Arguments
In all the examples thus far, we've passed in the values as positional arguments in the constructor. However, if you want to enforce that the users specify *only* keyword arguments to instantiate objects, you can set the `kw_only` parameter in the `@dataclass` decorator to `True`. This can help improve readability.
</div>

### Use `__post_init__` to Create Fields Post Initialization

So far, we've learned how to use `default_factory` to generate default values from custom functions, and exclude fields from the constructor by setting `init` to `False`. Next, let's learn how to construct new fields from existing fields.

As a first step, remove the `name` field and add two new fields, `first_name` and `last_name`:

~~~{.python caption="main.py"}
from dataclasses import dataclass, field

@dataclass
class Student:
    first_name: str
    last_name: str
    ...
~~~

Say you'd like to add an `email` field, a string of the form `first_name.last_name@uni.edu` (not super fancy, but works!). And we don't want the users of the class to initalize this field, so we set `init=False`:

~~~{.python caption="main.py"}
from dataclasses import dataclass, field

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

We know the following:

- To initialize the `email` field, use the `first_name` and the `last_name` fields.
- To ensure users cannot initalize this field, set `init=False` in the `field()` function.

![email]({{site.images}}{{page.slug}}/1.png)\

So far so good. But, wait! We'll get to know the `first_name` and the `last_name` only *after* the `Student` object has been instantiated. **So when and how do we initialize the `email` field?** Here's where the `__post_init__` method can help.

The `__post_init__` special method is called immediately *after* an object is instantiated. Meaning by the time `__post_init__` is called, we already know the `first_name` and the `last_name`.

So we can go ahead and set the `email` field to the f-string `f"{self.first_name}.{self.last_name}@uni.edu"`:

~~~{.python caption="main.py"}
    def __post_init__(self):
        self.email = f"{self.first_name}.{self.last_name}@uni.edu"
~~~

Is the `__post_init__` method working as expected? Let's create a `Student` object to verify that:

~~~{.python caption=""}
>>> jane = Student('Jane','Lee','Computer Science','senior',3.99)
>>> jane
~~~

And yes! 📧 The `email` field has been set for the student 'Jane Lee':

~~~{ caption="Output"}
Student(
    first_name="Jane",
    last_name="Lee",
    major="Computer Science",
    year="senior",
    gpa=3.99,
    roll_num="XAJI0Y6DP",
    email="Jane.Lee@uni.edu",
)
~~~


### Order and Sort Data Class Instances

Sorting data class instances on a field can often be helpful. And we'll learn how to do that.

![sorting]({{site.images}}{{page.slug}}/3.png)\

Let's add a `tuition` field to the `Student` data class, an integer with a default value of 10000:

~~~{.python caption="main.py"}
...
@dataclass
class Student:
    first_name: str
    last_name: str
    major: str
    year: str
    gpa: float
    roll_num: str = field(default_factory=generate_roll_num, init=False)
    email: str = field(init=False)
    tuition: int = 10000
~~~

#### What's the Goal?

Given a list of instances of the `Student` data class, we'd like to sort them in the increasing order of `tuition`. As of now, we don't quite know how to do that, but we'll get there soon!

Next, create two `Student` objects:

~~~{.python caption="main.py"}
jane = Student('Jane','Lee','Computer Science','senior',3.99)
julia = Student('Julia','Doe','Economics','junior',3.63,27000)
~~~

For `jane`, the deafult `tuition` of 10000 will be used. Let's try doing `julia > jane`:

~~~{.python caption="main.py"}
print(julia > jane)
~~~

We see that the comparison doesn't make sense as yet:

~~~{ caption="Output"}
Traceback (most recent call last):
  File "main.py", line 52, in <module>
    print(julia > jane)
TypeError: '>' not supported between instances of 'Student' and 'Student'
~~~

If you remember, data classes come with the `__eq__` method that lets us compare two objects for equality of attributes. However, other comparisons between objects are not supported by default. So what's the plan? 🤔

#### Enter `order` And `sort_index`

To be able to enforce ordering among data class instances, and subsequently, sort them, you should set `order` to `True` in the `@dataclass` decorator and define a `sort_index`. 

You can add the `sort_index` field to the data class. And you should see the patterns in the `field()` function already:

- Users need not initialize the `sort_index`, so set `init` to `False`.
- You can as well exclude the field from the representation string by setting `__repr__` to `False`.

~~~{.python caption="main.py"}
...
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

Here again, we'd like to use `tuition` as the key to sort on, but we'll get to know the `tuition` only *after* the objects are instantiated. And you already know what to do, right? Yeah, use the `__post_init__` method. ✅

Just the way you set the `email` field, you can set the `sort _index` to `tuition` in the `__post_init__` method, too:

~~~{.python caption="main.py"}
    def __post_init__(self):
        self.email = f"{self.first_name}.{self.last_name}@uni.edu"
        self.sort_index = self.tuition
~~~

Now create a few more `Student` objects:

~~~{.python caption="main.py"}
jane = Student('Jane','Lee','Computer Science','senior',3.99,30000)
julia = Student('Julia','Doe','Economics','junior',3.63,27000)
jake = Student('Jake','Langdon','Math','senior',3.89,28000)
joy = Student('Joy','Smith','Political Science','sophomore',4.00)
~~~

Collect the instances in a list and call the `sort()` method on it - just the way you'd sort a list of integers or strings:

~~~{.python caption="main.py"}
instance_list = [jane,julia,jake,joy]
instance_list.sort()
pprint(instance_list)
~~~

You can see that the instance list has been sorted in the increaisng order of `tuition`:

~~~{ caption="Output"}
[
    Student(
        first_name="Joy",
        last_name="Smith",
        major="Political Science",
        year="sophomore",
        gpa=4.0,
        roll_num="D4V30T9NT",
        email="Joy.Smith@uni.edu",
        tuition=10000,
    ),
    Student(
        first_name="Julia",
        last_name="Doe",
        major="Economics",
        year="junior",
        gpa=3.63,
        roll_num="BHSAHXTHV",
        email="Julia.Doe@uni.edu",
        tuition=27000,
    ),
    Student(
        first_name="Jake",
        last_name="Langdon",
        major="Math",
        year="senior",
        gpa=3.89,
        roll_num="3A3ZMF8MD",
        email="Jake.Langdon@uni.edu",
        tuition=28000,
    ),
    Student(
        first_name="Jane",
        last_name="Lee",
        major="Computer Science",
        year="senior",
        gpa=3.99,
        roll_num="XAJI0Y6DP",
        email="Jane.Lee@uni.edu",
        tuition=30000,
    ),
]
~~~

If that's hard to parse, let's print out the names of the students and the corresponding `tuition`:

~~~{.python caption="main.py"}
for instance in instance_list:
    print(f"{instance.first_name} {instance.last_name}'s tuition: {instance.tuition}")
~~~

Well, there you go! The sorting works as expected.

~~~{ caption="Output"}
Joy Smith's tuition: 10000
Julia Doe's tuition: 27000
Jake Langdon's tuition: 28000
Jane Lee's tuition: 30000
~~~

<div class="notice--big--primary">
#### Setting `order=True` Facilitates Comparison. But How?

We set `order=True` and specified the sorting index. Somehow the instance list was sorted, based on the `tuition` field, just the way we wanted. But how did it happen?
  
To achieve this in a regular Python class, you'll have to define the comparison methods `__gt__`, `__ge__`, `__lt__`, and `__le__`. But in a data class, when you set `order=True`, you get a ready-to-use implementation of these methods.

Let's go ahead and get the methods associated with the `Student` data class:
  
~~~{.python caption="main.py"}
from inspect import getmembers,isfunction
from pprint import pprint
...
pprint(getmembers(Student,isfunction))
~~~

And we see all the four comparison methods:
  
~~~{ caption="Output"}
[('__eq__', <function __create_fn__.<locals>.__eq__ at 0x01C93CD0>),
 ('__ge__', <function __create_fn__.<locals>.__ge__ at 0x01C93DA8>),
 ('__gt__', <function __create_fn__.<locals>.__gt__ at 0x01C93D60>),
 ('__init__', <function __create_fn__.<locals>.__init__ at 0x01C93BF8>),
 ('__le__', <function __create_fn__.<locals>.__le__ at 0x01C93D18>),
 ('__lt__', <function __create_fn__.<locals>.__lt__ at 0x01C93C40>),
 ('__post_init__', <function Student.__post_init__ at 0x01C93BB0>),
 ('__repr__', <function __create_fn__.<locals>.__repr__ at 0x01C93C88>)]
~~~

So for anything we want to do with classes and their instances, **data classes = batteries included**? Yeah, it seems safe to say so.
</div>
  
### Subclass Data Classes to Extend Functionality

Suppose you need a TA class to store information about students who work as teaching assistants.

![inheritance]({{site.images}}{{page.slug}}/4.png)\

**Well, TAs are students, too**. So each TA object will have *all* the fields that a `Student` object has. In addition, let's say TAs need to have the following three fields:

- `course` for which they work as a teaching assistant,
- `hours_per_week`, and
- `stipend`.

Instead of creating a new `TA` data class with the same attributes as the student and a few additional attributes, we can extend the functionality of the `Student` class using inheritance.

![inheritance]({{site.images}}{{page.slug}}/inheritance.png)\

Let’s create a `TA` subclass that inherits from the `Student` class:

~~~{.python caption="main.py"}
@dataclass
class TA(Student):
    course: str = None
    hours_per_week: int = 0
    stipend: int = 100
~~~

~~~{.python caption=""}
>>> from main import TA
>>> fanny = TA('Fanny','Gray','Math','senior',4.00,33000,'Combinatorics',20,500)
>>> fanny.course
'Combinatorics'
>>> fanny.hours_per_week
20
>>> fanny.stipend
500
~~~

<div class="notice--info">
### What You Should Know About Inheritance and Default Values for Fields
  
~~~{.python caption="main.py"}
@dataclass
class TA(Student):
    course: str 
    hours_per_week: int
    stipend: int 
~~~

~~~{caption="Output"}
Traceback (most recent call last):
  File "main.py", line 47, in <module>
    class TA(Student):
    ...
    raise TypeError(f'non-default argument {f.name!r} '
TypeError: non-default argument 'course' follows default argument
~~~
</div>
  
### Use Slots for Improved Performance


<div class="notice--big--primary">
#### What I Learned About `sys.getsizeof()`
  
~~~{.python caption=""}
>>> dict_1 = {"key1": "value1"}
>>> dict_2 = {"key1": {"key2": "value2"}}
>>> dict_3 = {"key1": {"key2": {"key3": "value3"}}}
~~~
  
~~~{.python caption=""}
>>> import sys
>>> sys.getsizeof(dict_1)
128
>>> sys.getsizeof(dict_2)
128
>>> sys.getsizeof(dict_3)
128
~~~
  
</div>
  
~~~{.bash caption=">_"}
$ pip3 install pympler
~~~
  
<div class="wide">
![size-of-objects]({{site.images}}{{page.slug}}/5.png)\
</div>

## Conclusion

And that's a wrap. So did we cover *everything* about data classes? No. But these are what you'll need when working with data classes.

{% include cta/cta1.html %}
