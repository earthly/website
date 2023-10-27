---
title: "Abstract Base Classes in Python"
categories:
  - Tutorials
toc: true
author: Kabaki Antony
editor: Bala Priya C

internal-links:
 - OOP
 - Python
 - Abstract Class
 - Inheritance
 - Abstraction
excerpt: |
    Learn how to create Abstract Base Classes (ABCs) in Python to enforce the implementation of certain methods or attributes in subclasses. ABCs promote code reuse, consistency, and modularity, and can be used for type checking at runtime. Discover the benefits of using ABCs and explore real-world use cases for this powerful feature in Python programming.
last_modified_at: 2023-07-19
---
**We're [Earthly](https://earthly.dev/). We simplify and speed up software building using containerization. Earthly works great with Python projects. [Check it out](/).**

Object-oriented programming (OOP) is a popular programming paradigm used in many modern programming languages, including Python. At the core of OOP are classes that allow us to create objects with attributes and methods. However, regular classes in Python have limitations that can make it challenging to create modular and maintainable code.

One limitation of regular classes is that they cannot enforce the implementation of certain methods or attributes, making it difficult for objects of different classes to be used interchangeably in code. Additionally, regular classes cannot be used for type checking at runtime, which can lead to errors in code.

**Abstract Base Classes** (ABCs) offer a solution to these limitations by allowing us to define a set of common methods and attributes that must be implemented by any class that inherits from the ABC. This ensures that objects of different classes can be used interchangeably in our code and provides a way to catch errors at runtime through type checking. ABCs also promote code reuse and modularity by enforcing consistency across their subclasses. They ensure consistent behavior in subclasses and enable objects of different classes to be used interchangeably.

In this article, we will explore the concept of ABCs and learn how they differ from regular classes. We will also examine the relationship between ABCs and interfaces and show how to implement them in Python. Finally, we will discuss the benefits of using ABCs and provide some real-world examples to illustrate their usefulness.

The code examples used in this tutorial can be found in [this GitHub repository](https://github.com/KabakiAntony/abstract_base_classes_tutorial).

## What Are Abstract Base Classes?

In Python, classes are user-defined blueprints for creating objects that have attributes and methods. When we define a regular Python class, we can add any number of attributes and methods to it. We can then create instances of the class and use them to perform operations.

However, one limitation of regular Python classes is that they do not enforce the implementation of certain methods or attributes in the classes that inherit from them. This means that if we have two classes that are related in some way, there is no guarantee that they will have the same methods or attributes. As a result, objects of different classes may not be able to be used interchangeably in our code.

This is where Abstract Base Classes (ABCs) come in. An ABC is a special type of class that contains one or more abstract methods. Abstract methods are methods that have no implementation in the ABC but must be implemented in any class that inherits from the ABC. In other words, an ABC provides a set of common methods or attributes that its subclasses must implement.

The main difference between an ABC and a regular class is that you cannot create an instance of an ABC. Instead, you can only inherit from it and implement all the abstract methods it has defined. This ensures that all subclasses of the ABC have the same set of methods or attributes, making them interchangeable in our code.

In summary, ABCs are a way of defining a set of common methods or attributes that must be implemented by any class that inherits from the ABC. This promotes code reuse, consistency, and modularity in our code.

### What Then Is Abstraction?

![Confused]({{site.images}}{{page.slug}}/confused.png)\

To understand abstraction in Python, it is important to first understand the concept of regular Python classes. In Python, we can create classes that define a set of behaviors and properties, and then create objects from those classes. However, when we inherit from a regular class, we are inheriting both the attributes and methods of the parent class, and we can override or add new methods as needed.

On the other hand, ABCs allow us to create abstract methods that must be implemented by any subclass of the ABC, without specifying how those methods should be implemented. This is the key difference between regular classes and ABCs - ABCs allow us to define a set of behaviors that must be implemented by any class that inherits from the ABC.

<div class="notice--info">
Abstraction, therefore, is the process of defining a set of behaviors or properties without specifying how they should be implemented. This allows us to create generic classes that can be reused across different parts of our code and also creates interfaces that specify the required behavior of a class without getting bogged down in the implementation details.
</div>

ABCs are a powerful tool for achieving abstraction in Python, as they allow us to enforce a consistent set of behaviors across different classes and promote code reuse and modularity.

### Interfaces and ABCs

Interfaces define a common behavior that can be shared by multiple classes. So that any class that implements some given interface has to provide the behavior specified by the interface, this ensures that all classes that implement that particular interface have certain common behaviors. This is very beneficial in that we can write code that can work with any object that implements that interface, without having to know the specific implementation detail.

Python, unlike other languages, does not natively support interfaces, therefore to implement an interface in Python we use the `abc`  module. Therefore ABCs are very similar to interfaces, the only subtle difference between an interface and an ABC is that an ABC can have concrete methods whereas an interface will just have the method signature in this case just abstract methods. Another difference is that a class can implement multiple interfaces and only inherit from a single ABC.

Another difference even though it is not clear in Python due to the lack of native support of interfaces is that you implement an interface and inherit an ABC, to expound on this is that other languages have keywords like `implements` and `extends` that clearly indicate the action you are taking in child class in relation to a parent class.

Here is an example of an interface for a shape that requires implementing classes to have methods for calculating area and perimeter.

~~~{.python caption="shape.py"}
# shape.py

from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
              pass
    
    @abstractmethod
    def perimeter(self):
                  pass
~~~

In the above code we have defined an interface `Shape` and any class that inherits this interface must implement the `area` and `perimeter` methods. Therefore, a `Rectangle` class that implements a `Shape`  interface would look like this.

~~~{.python caption="shape.py"}
# shape.py

class Rectangle(Shape):
    def __init__(self, length, width):
    self.length = length
    self.width = width
    
    def area(self):
              return self.length * self.width
     
    def perimeter(self):
              return 2 * (self.length + self.width)
~~~

In the above code we have a `Rectangle` class that is a subclass of the `Shape` interface. It has two instance variables, `length` and `width`, which are passed in as parameters to the `__init__` method. The `area` method calculates the area of the rectangle by multiplying the length and width together, while the `perimeter` method calculates the perimeter by adding the length and width and then multiplying the result by two.

Let's then look at an abstract base class that has abstract methods and one concrete method.

~~~{.python caption="vehicle_I.py"}
# vehicle_I.py

from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    def beep(self):
        print("Beep beep!")
~~~

In the above example we have a `Vehicle` ABC that has two abstract methods, `start` and `stop`. It also has a concrete method `beep`, the concrete method is implemented in this ABC so when called by an instance object of the `Vehicle` subclass it will print "Beep, beep!". All the methods will be available to any `Vehicle` subclass.

Let's create a `Car` subclass that will implement the `start` and `stop` methods, it will also inherit the `beep` method. So when we create an instance of the `Car` it will have access to all the methods.

~~~{.python caption="vehicle_I.py"}
# vehicle_I.py

class Car(Vehicle):
    def start(self):
        print("Starting the car.")

    def stop(self):
        print("Stopping the car.")

my_car = Car()

~~~

~~~{.python caption="vehicle_I.py"}
#  vehicle_I.py

my_car.start() # Output: Starting the car.
my_car.stop() # Output: Stopping the car.
my_car.beep() # Output: Beep beep!
~~~

In the above code we have a `Car` class that subclasses the `Vehicle` therefore, the `start` and `stop` methods are implemented in the `Car` subclass. Then we create an instance of the `Car`, so the `Car` object will have access to the `Car` class methods and also it will have access to the `beep` method that is implemented in the `Vehicle` ABC.

We have, therefore, seen that an interface will only have abstract methods but an ABC can have abstract methods and concrete methods.

### Metaclasses and ABCs

In Python, everything is an object and so are classes, and just like any other object, it is an instance of a class. This means that there must be a class that defines what a class is and how it behaves, and this is where `metaclasses` come in. A `metaclass` is a class that defines the behavior of other classes.

When you define a class in Python, you can specify its `metaclass` using the metaclass keyword argument. If no `metaclass` argument is specified, the `type` metaclass is used by default. The `type` metaclass is responsible for creating new classes in Python.

To better understand how metaclasses work, let's consider an example. We are going to create a custom metaclass that ensures that objects of a subclass are only instantiated with strings.

~~~{.python caption="string_meta.py"}
# string_meta.py

class StringOnlyMeta(type):
    def __call__(cls, *args, **kwargs):
              for arg in args:
                       if not isinstance(arg, str):
                    raise TypeError("Arguments must be strings")
             return super().__call__(*args, **kwargs)

~~~

In the above code we have a custom metaclass that ensures that objects are only instantiated with strings. When an instance of a class that uses this metaclass is created, the `__call__` method is called.

The `__call__` method takes in the class object `cls` as its first argument, followed by any positional arguments (*args) and keyword arguments (**kwargs) that were passed to the constructor.

In this implementation, the `__call__` method checks each positional argument to make sure it is an instance of the `str` class. If any argument is not a string, a `TypeError` is raised. If all arguments are strings, the `super().__call__` method is called to create and return a new instance of the class.

This metaclass can be used to enforce the requirement that certain arguments passed to the constructor of a class must be strings. Here is an example of its use in a class.

~~~{.python caption="string_meta.py"}
# string_meta.py

class MyStringOnlyClass(metaclass=StringOnlyMeta):
    def __init__(self, name, description):
        self.name = name
        self.description = description

~~~

In the above code we have a class `MyStringOnlyClass` that takes the `StringOnlyMeta` metaclass, it has a constructor that takes in two string arguments `name` and `description`. Therefore, when an object of `MyStringOnlyClass` is created the `StringOnlyMeta` metaclass will ensure that the arguments supplied to the object are strings. Let's see an example

~~~{.python caption="string_meta.py"}
# string_meta.py

# This will work because both arguments are strings
obj1 = MyStringOnlyClass("name", "description")

# This will raise a TypeError because the second argument is not a string
obj2 = MyStringOnlyClass("name", 123)

~~~

We have seen that the `StringOnlyMeta` metaclass can be used to ensure that objects are only instantiated with strings, by checking the arguments passed to the constructor and raising a `TypeError` if any argument is not a string. Therefore, the `StringOnlyMeta` customizes the behavior of the other classes that inherit from it.

In summary, we see that metaclasses are used to customize the behavior of classes in Python. ABCs are special classes that are used as blueprints for other classes, and they are defined using the `abc.ABC` metaclass.

## Implementing ABCs

Before we implement an ABC let's look at an illustration that shows a `Vehicle` ABC and how its subclasses will implement the abstract methods it defines. We are going to use the interface we defined above of a `Vehicle` and a `Car` subclass.

<div class="wide">
![How to inherit from an ABC]({{site.images}}{{page.slug}}/ABC-inheritance-illustration.png)
</div>

In the above illustration we have a `Vehicle` ABC that defines two abstract methods `start` and `stop`  and then we have two subclasses `Car` and `MotorCycle` that inherit from the ABC and implement the `start` and `stop` methods.

Let's, therefore, go ahead and look at how we implement an ABC in Python. To implement an ABC in Python we use the `abc` module. The following steps show how to create an ABC using the `abc` module and how we define some abstract methods, then implement the ABC in a concrete class.

### Import the `abc` Module

The first step is to import the  `abc`  module using the code below.

~~~{.python caption="main.py"}
# main.py

from abc import ABCMeta, abstractmethod

~~~

This will avail the `ABCMeta` metaclass and the `abstractmethod` decorator.

- `ABCMeta` is a class that is used as a metaclass to define ABCs.
- `abstractmethod` is a decorator function used to define an abstract method within an ABC.

### Create the ABC and Define an Abstract Method

To create an ABC we will use the `ABCMeta` metaclass that we imported above. We will also define one abstract method in our class and denote it using the `@abstractmethod` decorator. Here is an example.

~~~{.python caption="main.py"}
#  main.py

class MyAbstractClass(metaclass=ABCMeta):
  
   @abstractmethod
   def my_abstract_method(self):
       pass 
~~~

The code defines an abstract class called `MyAbstractClass`, it is an ABC since we have set its `metaclass` argument to `ABCMeta`. The class also has one abstract method `my_abstract_method` which is denoted using the `@abstractmethod` decorator. The method is not implemented in the ABC so we just use the keyword `pass` to show it is not implemented.

Here is an example of a `Vehicle` ABC that has two abstract methods `start` and `stop`.

~~~{.python caption="vehicle_II.py"}
# vehicle_II.py

from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def start(self):
        pass

   @abstractmethod
   def stop(self):
      pass
~~~

Now that we have a `Vehicle` ABC let's define a `Truck` concrete class that inherits from `Vehicle` and we are going to only implement the `start` method and try to create an instance of the `Truck` subclass.

~~~{.python caption="vehicle_II.py"}
# vehicle_II.py

class Truck(Vehicle):
    def start(self):
        print("Truck started")


my_truck = Truck()
my_truck.start()

~~~

In the `Truck` subclass we will just implement the `start` method. Then create an instance of the `Truck`  subclass and call the `start` method using the `Truck` instance. However, doing that gives us the error below since `Truck` is a subclass of the `Vehicle` class which is an ABC that requires all methods of the parent ABC to be implemented in the subclasses.

~~~{ caption="Output"}

TypeError: Can't instantiate abstract class Truck with abstract method stop 
~~~

Therefore, creating ABCs and having methods marked as abstract methods using the `@abstractmethod` decorator ensures that all methods in the ABC are implemented in their subclasses.

### Using an ABC in a Concrete Class

This is a class that provides a full implementation for all its methods and can be instantiated directly. This means that it provides implementations for all methods that it defines. Concrete classes, therefore, represent real-world objects while ABCs are blueprints for other classes. However, just using concrete classes will not enforce any kind of structure, and will not force any methods or attributes to be implemented.

ABCs on the other hand define the structure and behavior of subclasses, they ensure certain methods and attributes are implemented. So, if you wanted to have some structure and clarity in your concrete classes it is great when you use an ABC. So you will define an ABC as a parent class and then a concrete class will subclass the ABC and implement all the methods defined in the ABC. This will also be beneficial in the future if you want to extend and modify your code.

Let's consider the `Shape` ABC we defined in the interfaces section, we have different shapes such as circles, rectangles, and triangles. Each shape has an area and a perimeter, so any class that inherits from `Shape` must implement both the `area` and `perimeter` methods. For example, we can define a `Square` concrete class that will inherit from `Shape` and provide implementations for both methods.

~~~{.python caption="shape.py"}
# shape.py

class Square(Shape):
    def __init__(self, side_length):
              self.side_length = side_length
        
    def area(self):
              return self.side_length ** 2
    
    def perimeter(self):
              return 4 * self.side_length
~~~

In the above code we have a concrete class `Square` that inherits from the `Shape` abstract base class. The `Square` class provides real implementations for both the `area` and `perimeter` methods, which are required by the `Shape` abstract class.

By inheriting from the `Shape` abstract class, the `Square` class ensures that it has a common behavior with other shapes, such as circles, rectangles, and triangles. This means that any code that works with a `Shape` object will also work with a `Square` object, without needing to know the specifics of the `Square` class. Let's look at an example

~~~{.python caption="shape.py"}
# shape.py

def print_shape_info(shape):
    print(f"Area: {shape.area()}")
    print(f"Perimeter: {shape.perimeter()}")

square = Square(5)
rectangle = Rectangle(3,5)

print_shape_info(square)
print_shape_info(rectangle)

~~~

By defining a common behavior in an abstract class, you can ensure that all of your subclasses have the required methods and can be used interchangeably in your program.

The above code defines a `print_shape_info` function that takes a `shape` parameter that is expected to be an instance of a class that inherits from `Shape` and implements the `area` and `perimeter` methods. The function calls these methods on the `shape` object and prints outs the corresponding area and perimeter. So that example shows how objects of different descendants of an ABC can be used interchangeably without knowing their implementation details.

### Real-World Use Cases for ABCs

ABCs have multiple applications in the real world, in this section, we are going to look at an example of how we could use an ABC and use it to enforce type checking and ensure compatibility in a Python project.

Consider a large project that involves multiple modules and different developers working on different parts of the code. We could ensure that the different parts of the code are compatible. An ABC is an excellent choice since it will lay down what each module needs to implement.

Let's say you have a program that needs to work with different types of animals. Each animal has a name and can make a sound, but different types of animals have different behaviors. For example, a dog can bark, a cat can meow, and a bird can chirp.

You could define an ABC called `Animal` with abstract methods `get_name` and `make_sound`, and then define concrete subclasses for each type of animal:

Let's see an illustration first showing the `Animal` ABC and different types of animal subclasses that have to implement the methods it has defined.

<div class="wide">
![An abc and concrete subclasses]({{site.images}}{{page.slug}}/animal-abc-and-concrete-classes.png)
</div>

Let's implement the parent ABC:

~~~{.python caption="animal.py"}
# animal.py

from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def get_name(self):
        pass
    
    @abstractmethod
    def make_sound(self):
        pass
~~~

Here we have the `Animal` ABC that defines two abstract methods, `get_name` and `make_sound`, which must be implemented by any concrete subclass. The `Dog`, `Cat`, and `Bird` classes indicated in the illustration are concrete subclasses that inherit from the `Animal` ABC and provide implementations for both abstract methods. To show how they will be implemented we will just implement just one subclass but the idea is the same for the other subclasses.

Here is an example of the implementation of the `Bird` subclass.

~~~{.python caption="animal.py"}
# animal.py 

class Bird(Animal):
    
    def __init__(self, name):
        self.name = name
    
    def get_name(self):
        return self.name
    
    def make_sound(self):
        return "Chirp chirp!"

~~~

We have defined a concrete subclass `Bird` that inherits from the `Animal` abstract class. The `Bird` class represents a type of animal that can make the sound "Chirp chirp!".

The `Bird` class has an `__init__` method that takes a name parameter, which is used to set the `name` attribute of the `Bird` object. The `get_name` and `make_sound` methods are required by the `Animal` abstract class and are implemented in the `Bird` class.

The `get_name` method returns the `name` attribute of the `Bird` object, while the `make_sound` method returns the string "Chirp chirp!". These methods ensure that any object created from the `Bird` class has the required behavior defined in the `Animal` abstract class.

By defining an `Animal` abstract class with abstract methods `get_name` and `make_sound`, we have ensured that any class that inherits from the `Animal` abstract class will have the same behavior. This makes it easy to work with different types of animals in our program since we know that they all have the required methods.

For example, we could create a list of different types of animals and call their `get_name` and `make_sound` methods:

~~~{.python caption="animal.py"}
# animal.py

animals = [Dog("Rufus"), Cat("Whiskers"), Bird("Tweety")]

for animal in animals:
    print(animal.get_name(), animal.make_sound())

~~~

This code will create a list of different types of animals, including a `Dog`, a `Cat`, and a `Bird`. It will then iterate over the list, calling the `get_name` and `make_sound` methods on each animal and printing out the corresponding values.

By using an abstract class to define the required behavior of different types of animals, we can ensure that our program is flexible and extensible. We can easily add new types of animals to our program by defining new subclasses of the `Animal` abstract class and implementing the required methods

### Creating Plugin Architectures Using ABCs

A plugin in software development is where a software application is designed to allow for third-party modules which extend the functionality of the given application. Therefore, a common way of implementing the architecture to use plugins in the given application is through the use of ABCs. So developers of the given application will create a standard interface that plugins must implement for them to be compatible with the application.

So they will define an ABC that will specify the required methods and attributes for a plugin to interact with the application and this will ensure that plugins are compatible and follow the same set of rules.

A plugin architecture could be used in a content management system (CMS), allowing developers to create custom plugins for things like image galleries, contact forms, and others. The CMS will then define an ABC that specifies the required methods and attributes for the plugin to interact with the CMS, such as configuration and how to render on a webpage. The developer then will create the concrete class that implements the required methods. This will ensure the plugin is compatible with the CMS and follows the same set of rules as other plugins.

Say we have a CMS called "MyCMS" and we want to allow developers to create plugins for it. We could define an ABC called `MyCMSPlugin` that specifies the required methods and attributes for a plugin to interact with MyCMS:

~~~{.python caption="cmsplugin.py"}
# cmsplugin.py

from abc import ABC, abstractmethod

class MyCMSPlugin(ABC):
    @abstractmethod
    def get_config(self):
        pass
    
    @abstractmethod
    def render(self):
        pass

~~~

In the above code, we define the `MyCMSPlugin` ABC with two abstract methods `get_config` and `render`. `get_config` is responsible for returning a configuration object for the plugin, while `render` is responsible for rendering the plugin on a webpage.

Now, a developer who wants to create a plugin for MyCMS can subclass `MyCMSPlugin` and provide concrete implementations for the `get_config` and `render` methods. Here's an example of a plugin for an image gallery:

~~~{.python caption="cmsplugin.py"}
# cmsplugin.py

class ImageGalleryPlugin(MyCMSPlugin):
    def get_config(self):
        return {
            'image_folder': '/path/to/images',
            'max_images': 10
        }
    
    def render(self):
        # Render the image gallery on a webpage
        pass

~~~

In the above code, we define a concrete class called `ImageGalleryPlugin` that inherits from `MyCMSPlugin` and provides concrete implementations for `get_config` and `render`.

By using an ABC to define the required interface for plugins, we ensure that all plugins follow the same set of rules and are compatible with MyCMS. This makes it easier for developers to create plugins for MyCMS and for users to install and use those plugins.

## Benefits of ABCs

![Benefits]({{site.images}}{{page.slug}}/benefits.png)\

Throughout the article we have covered how to create ABCs and the application of ABCs in real-world scenarios. In this section, let's look at some of their benefits.

- They encourage consistency and modularity, by defining a set of common methods and attributes that must be implemented by subclasses, this makes sure that our code is broken into self-contained modules that do just the things laid out in the ABC, the code is also easier to read and more predictable.
- They enable code to be extended easily, this is especially useful in plugin architecture where concrete classes follow a given interface.
- They help enforce contracts, when an ABC is used it defines the expected behavior of a class or a function. So by enforcing these contracts developers can ensure that their code behaves as expected.
- ABCs allow for type checking, by defining  common methods and attributes, ABCs allow for type checking at runtime.

## Conclusion

In this piece, we've covered the ins and outs of abstract base classes (ABCs) - what they are, how they differ from regular classes, and their relation to interfaces in object-oriented programming. We walked you through creating and using ABCs while sharing some practical examples. We also shed light on how ABCs in Python shape your code, making it more reusable, modular, consistent, and organized.

Just as ABCs simplify and streamline your Python code, [Earthly](https://www.earthly.dev/) can simplify your build process. If you've enjoyed exploring Python's ABCs, you'll love how Earthly can make your build process more efficient and manageable. Give it a try!

{% include_html cta/bottom-cta.html %}
