---
title: "Querying Relational Databases With SQLAlchemy in Python"
categories:
  - Tutorials
toc: true
author: Mercy Bassey
editor: Mustapha Ahmad Ayodeji

internal-links:
 - Relational Databases
 - SQLAlchemy
 - Python
 - Database
excerpt: |
    
---
**We're [Earthly](https://earthly.dev/). We simplify and speed up software builds with containerization. If you're wrestling with Python, Earthly can make your build process a breeze. [Give it a whirl](/).**

If you are interested in working with relational databases in Python, then you need to know what SQLAlchemy is. It is a Python library that provides a high-level, SQL abstraction layer for relational databases. With SQLAlchemy, you can interact with databases using Python objects and methods, rather than writing raw SQL queries.
In this tutorial, you will learn how to get started with SQLAlchemy and also learn how to interact with and query an [SQLite](https://sqlite.org/index.html) relational database with the SQLAlchemy library.

## Pre-Requisites

If you'd like to follow along in this tutorial, you'll need to have the following:

- A basic knowledge of [OOP](https://earthly.dev/blog/python-classes-and-objects/) in Python.
- A text editor with the [SQLite viewer extension](https://marketplace.visualstudio.com/items?itemName=qwtel.sqlite-viewer) installed - this tutorial uses [VScode](https://code.visualstudio.com/).

## What Is Sqlalchemy

![What]({{site.images}}{{page.slug}}/what.png)\

[SQLAlchemy](https://docs.sqlalchemy.org/en/20/) is a popular open-source SQL toolkit and Object-Relational Mapping (ORM) library for Python. It provides a set of high-level APIs and tools for interacting with relational databases such as MySQL, PostgreSQL, SQLite, Oracle, and Microsoft SQL Server. SQLAlchemy is designed to provide developers with a unified and consistent API for accessing different relational database systems.

Relational databases are a type of database that store data in a structured format, using tables with columns and rows to represent data entities. They are designed to ensure data consistency and provide powerful querying capabilities, making them popular for many types of applications, including web applications, finance, and e-commerce.

Connecting and interacting with relational databases in Python can be a complex and time-consuming process due to the need to establish a connection, handle errors, and write queries in a database-specific SQL syntax. So, the process requires a deep understanding of SQL and the database's schema to effectively manipulate data. This is where SQLAlchemy comes in, easing the stress of connecting and interacting with relational databases in Python.

With SQLAlchemy, developers can use a unified and consistent API to connect to different databases, perform CRUD operations, generate complex SQL queries, and manage database transactions and constraints. This allows developers to focus on building their application logic, rather than dealing with the low-level details of the database system.

Some of the features of SQLAlchemy include the following:

- **Object-Relational Mapping (ORM**): SQLAlchemy provides a powerful ORM system that allows developers to map Python classes to database tables and vice versa. This makes it easy to perform CRUD operations on database records using Python objects.
- **SQL Expression Language**: SQLAlchemy provides a flexible SQL expression language that allows developers to generate complex SQL queries in a Pythonic way. This makes it easy to write and execute SQL queries without having to deal with the low-level details of the database system.
- **Database Connection Pooling**: SQLAlchemy provides a built-in connection pooling system that allows developers to manage multiple database connections efficiently. This helps to improve the performance and scalability of database applications.
- **Data Integrity and Transactions**: SQLAlchemy provides support for transactions and data integrity constraints, such as foreign keys, unique constraints, and check constraints. This helps to ensure that data is consistent and accurate across different tables in the database.
- **Cross-database Compatibility:** SQLAlchemy provides a consistent API for interacting with different database systems, making it easy to write database applications that can work with different databases.

## Setting Up Sqlalchemy

Before getting started with SQLAlchemy, you need to first install the SQLAlchemy library. Execute the following command in your terminal or command prompt. This command will install the SQLAlchemy library via [pip](https://pypi.org/project/pip/):

~~~{.bash caption=">_"}
pip install SQLAlchemy
~~~

If you have it installed successfully, you should have the following output:

<div class="wide">
![Installing the sqlalchemy library]({{site.images}}{{page.slug}}/oqHbE7L.png)
</div>

Create a file named `main.py` (you can of course name this file whatever you want) and import the following from the SQLAlchemy library:

**[`create_engine`](https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine)**, **[`ForeignKey`](https://docs.sqlalchemy.org/en/20/core/constraints.html#sqlalchemy.schema.ForeignKey)**, **[`Column`](https://docs.sqlalchemy.org/en/20/core/metadata.html#sqlalchemy.schema.Column)**, **[`String`](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.String)**, **[`Integer`](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.Integer)**, **[`CHAR`](https://docs.sqlalchemy.org/en/20/core/type_basics.html#sqlalchemy.types.CHAR)**, and **[`CheckConstraint`](https://docs.sqlalchemy.org/en/20/core/constraints.html#check-constraint)**,
**[`join`](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.join)**.

~~~{.python caption="main.py"}
from sqlalchemy import create_engine, ForeignKey, Column, \
String, Integer, CHAR, CheckConstraint, join
~~~

Here's what each class and functions are responsible for:

- **`create_engine`**: This function is used to create an SQLAlchemy engine that connects to a database. It is the starting point for interacting with databases using SQLAlchemy and will be used to create an engine to connect to the SQLite database.
- **`ForeignKey`**: This class provides a way to define foreign keys in SQLAlchemy classes. Foreign keys are used to establish relationships between tables in a relational database.
- **`Column`**: This class is used to define columns in SQLAlchemy classes. Columns represent individual fields in a database table.
- **`String`**: This class is used to define a string data type for SQLAlchemy columns.
- **`Integer`**: This class is used to define an integer data type for SQLAlchemy columns.
- **`CHAR`**: This class represents a character column in a database table.
- **`CheckConstraint`**: This class defines a check constraint in a table, which is a condition that must be met for the data to be valid.
- **`join`**: This function constructs a SQL join between two or more tables, which allows data from different tables to be combined in a single query result.

Next, add the following line of code to import the **`declarative_base`** function from the **`sqlalchemy.ext.declarative`** module.

~~~{.python caption="main.py"}
from sqlalchemy.ext.declarative import declarative_base
~~~

<div class="notice--big--primary">
💡 The **`declarative_base`** function is used to create a base class that is used to define the database schema. This base class allows us to define the database schema in a way that is more like defining regular Python classes, and it makes it easy to create new database tables and columns.

After creating the base class by using the **`declarative_base`** function, we can define classes that inherit from the base class, and each of these classes represents a table in the database. We can define the columns of the table as attributes of the class, and we can define relationships between tables using attributes as well. Once we have defined all of our classes, we can use SQLAlchemy to create the database schema and interact with the database using the classes we have defined.
</div>

Add the following line of code to import the **`sessionmaker`** class and the **`relationship`** function from the SQLAlchemy ORM (Object Relational Mapper) module.

~~~{.python caption="main.py"}
from sqlalchemy.orm import sessionmaker, relationship
~~~

These classes do the following;

1. **`sessionmaker`**: It is a factory class that returns a new **`Session`** class when called with a database engine. The **`Session`** class is used to create database sessions, which are used to communicate with the database and perform CRUD (Create, Read, Update, Delete) operations.
2. **`relationship`**: It is a function that is used to define relationships between two database tables. It is used to specify how data in one table is related to data in another table. The **`relationship`** function is used to create a bidirectional relationship between two database tables.

Finally, create a new instance of the **`declarative_base`** class provided by SQLAlchemy and assign it to the variable **`Base`**. This instance will be used as a base class for the definition of database models using the SQLAlchemy ORM (Object-Relational Mapping) framework.

~~~{.python caption="main.py"}
Base = declarative_base()
~~~

## Creating a Table

Now that we have SQLAlchemy all setup, let's see how we can create a table and store it in an SQLite database.

First, we'll define an SQLAlchemy model class **`User`** that represents a table called *users* in a database. This could be any class of your choice (a **`Persons`** class or a **`Students`** class):

~~~{.python caption="main.py"}
class User(Base):
    __tablename__ = "users"

    ssn = Column("ssn", Integer, primary_key=True)
    firstname =  Column("FirstName", String)
    lastname = Column("LastName", String)
    country = Column("Country", String)
    gender = Column("Gender", CHAR(1), \
    CheckConstraint('gender = upper(gender)'))
    expertise = Column("Expertise", String)
    age = Column("Age", Integer)
~~~

The class above has several attributes that correspond to columns in the database table:

- **`ssn`**: a column of integers representing the user's social security number (SSN). This column is the primary key of the table.
- **`firstname`**: a column of strings representing the user's first name.
- **`lastname`**: a column of strings representing the user's last name.
- **`country`**: a column of strings representing the user's country.
- **`gender`**: a column of characters representing the user's gender, with a check constraint that ensures that the gender is always stored in uppercase letters.
- **`expertise`**: a column of strings representing the user's area of expertise.
- **`age`**: a column of integers representing the user's age.

Create a constructor method for the **`User`**class by adding the below code snippets:

~~~{.python caption="main.py"}

def __init__(self, ssn, firstname, lastname, country, gender, \
expertise, age):
        self.ssn = ssn
        self.firstname = firstname
        self.lastname = lastname
        self.country = country
        self.gender = gender
        self.expertise = expertise
        self.age = age
~~~

This takes in seven arguments **`ssn`**, **`firstname`**, **`lastname`**, **`country`**, **`gender`**, **`expertise`**, and **`age`**, and assigns them to the corresponding instance variables of the **`User`**object using the **`self`**keyword. This method is called automatically when a new instance of the **`User`**
 class is created. Without this method, the attributes of the instance would not be initialized, and the instance would not be useful for interacting with the database.

Next, create a method that defines a string representation of the User object when you print a **`User`** object:

~~~{.python caption="main.py"}
def __repr__(self):
        return f"({self.ssn}) {self.firstname} \
        {self.lastname} ({self.gender},{self.age})"
~~~

With the code above the string returned will include the user's *SSN*, *firstname*, *lastname*, *gender*, and *age*.

Create a database engine using SQLAlchemy's **`create_engine`** method and set it to use an SQLite database file named *mydb.db*:

~~~{.python caption="main.py"}
engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)
~~~

The **`echo`** parameter is set to **`True`**. This will enable SQLAlchemy to log the SQL statements it executes.

If you'd like to use another type of relational database, say MySQL or MariaDB you can see the following [guide](https://docs.sqlalchemy.org/en/20/dialects/mysql.html).

Add the below code snippets to create a **`Session`** class using the **`sessionmaker`** class. The **`Session`**  is bound to the database engine created earlier using the **`create_engine`** function. This class will be responsible for managing database connections and transactions.

~~~{.python caption="main.py"}
Session = sessionmaker(bind=engine)
session = Session()
~~~

Add instances of the **`User`**class to the session and commit the changes to the database by adding the following code snippets:

~~~{.python caption="main.py"}

user1 =  User(1000, "John", "Doe", "San Fransisco", "F", \
"Software Engineer", 35)
user2 = User(1001, "Jane", "Doe", "Mexico", "M", "Data Analyst", 25)
user3 = User(1002, "Bob", "Smith", "Los Angeles", "M", \
"Python Developer", 30)
user4 = User(1003, "Brandy", "Smith", "Califonia", "F", \
"Technical Writer", 23)
user5 = User(1004, "Blue", "Ivy", "Texas", "F", "Singer", 21)
session.add(user1)
session.add(user2)
session.add(user3)
session.add(user4)
session.add(user5)
session.commit()
~~~

In total, the overall code looks like the following:

~~~{.python caption="main.py"}
from sqlalchemy import create_engine, ForeignKey, Column, \
String, Integer, CHAR, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    ssn = Column("ssn", Integer, primary_key=True)
    firstname =  Column("FirstName", String)
    lastname = Column("LastName", String)
    country = Column("Country", String)
    gender = Column("Gender", CHAR(1), \
    CheckConstraint('gender = upper(gender)'))
    expertise = Column("Expertise", String)
    age = Column("Age", Integer)

    def __init__(self, ssn, firstname, lastname, \
    country, gender, expertise, age):
        self.ssn = ssn
        self.firstname = firstname
        self.lastname = lastname
        self.country = country
        self.gender = gender
        self.expertise = expertise
        self.age = age

    def __repr__(self):
        return f"({self.ssn}) {self.firstname} {self.lastname} \
        ({self.gender},{self.age})"
    
engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

user1 =  User(1000, "John", "Doe", "San Fransisco", "F", \
"Software Engineer", 35)
user2 = User(1001, "Jane", "Doe", "Mexico", "M", "Data Analyst", 25)
user3 = User(1002, "Bob", "Smith", "Los Angeles", "M", \
"Python Developer", 30)
user4 = User(1003, "Brandy", "Smith", "Califonia", "F", \
"Technical Writer", 23)
user5 = User(1004, "Blue", "Ivy", "Texas", "F", "Singer", 21)
session.add(user1)
session.add(user2)
session.add(user3)
session.add(user4)
session.add(user5)
session.commit()
~~~

And when you execute this code, you should have the following output and a database file containing the table:

~~~{ caption="Output"}

2023-03-25 20:53:48,932 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2023-03-25 20:53:48,932 INFO sqlalchemy.engine.Engine PRAGMA \
main.table_info("users")
2023-03-25 20:53:48,933 INFO sqlalchemy.engine.Engine [raw sql] ()
2023-03-25 20:53:48,933 INFO sqlalchemy.engine.Engine PRAGMA \
temp.table_info("users")
2023-03-25 20:53:48,933 INFO sqlalchemy.engine.Engine [raw sql] ()
2023-03-25 20:53:48,934 INFO sqlalchemy.engine.Engine 
CREATE TABLE users (
        ssn INTEGER NOT NULL, 
        "FirstName" VARCHAR, 
        "LastName" VARCHAR, 
        "Country" VARCHAR, 
        "Gender" CHAR(1) CHECK (gender = upper(gender)), 
        "Expertise" VARCHAR, 
        "Age" INTEGER, 
        PRIMARY KEY (ssn)
)

2023-03-25 20:53:48,935 INFO sqlalchemy.engine.Engine [no key 0.00015s] ()
2023-03-25 20:53:48,947 INFO sqlalchemy.engine.Engine COMMIT
2023-03-25 20:53:48,950 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2023-03-25 20:53:48,953 INFO sqlalchemy.engine.Engine INSERT INTO users \
("FirstName", "LastName", "Country", "Gender", "Expertise", "Age") \
VALUES (?, ?, ?, ?, ?, ?), (?, ?, ?, ?, ?, ?), (?, ?, ?, ?, ?, ?), \
(?, ?, ?, ?, ?, ?), (?, ?, ?, ?, ?, ?) RETURNING ssn
2023-03-25 20:53:48,953 INFO sqlalchemy.engine.Engine [generated in \
0.00025s (insertmanyvalues)] ('John', 'Doe', 'San Fransisco', 'F', \
'Software Engineer', 35, 'Jane', 'Doe', 'Mexico', 'M', 'Data Analyst', \
25, 'Bob', 'Smith', 'Los Angeles', 'M', 'Python Developer', 30, 'Brandy', \
'Smith', 'Califonia', 'F', 'Technical Writer', 23, 'Blue', 'Ivy', 'Texas', \
'F', 'Singer', 21)
2023-03-25 20:53:48,955 INFO sqlalchemy.engine.Engine COMMIT
~~~

<div class="wide">
![Viewing database file]({{site.images}}{{page.slug}}/vIjGoR5.png)
</div>

Since you have now created and populated the `users` table, you can now delete the following lines of code:

~~~{.python caption="main.py"}
session.add(user1)
session.add(user2)
session.add(user3)
session.add(user4)
session.add(user5)
session.commit()
~~~

If you'd like to add more users, you can simply declare a variable, assign it to the values you'd like that user to have, and then call the `session.add()` and `session.commit()` methods again.

## Creating Relationships Between Tables

Now that you have seen how to create a table, it's time to create another table that relates to the **`users`** table we created earlier on. This table will be called **`pets`.** So ideally, we will create a many-to-one relationship where a single user can have many pets.

First, let's create a relationship between the **`Users`**  table and the **`pets`**  table we are about to create by adding the following line of code before the `__init__` method in the  **`Users`** class:

~~~{.python caption="main.py"}
pets = relationship('Pet', back_populates='owner')
~~~

The code above creates a relationship between the **`User`** and **`Pet`** models (class), where a **`user`**can has multiple **`Pets`** and each **`Pet`** belongs to one **`user`**. In other words, this means that each **`user`** can have multiple **`pet`** instances associated with them, but each **`pet`** instance can only have one **`User`**as its owner.

Now add the following code snippets below the **`User`** class:

~~~{.python caption="main.py"}
class Pet(Base):
    __tablename__ = 'pets'

    id = Column("ID", Integer, primary_key=True)
    name = Column("NAME", String)
    owner_id = Column("OWNER", Integer, ForeignKey('users.ssn'))

    def __init__(self, id, name, owner_id):
        self.id = id
        self.name = name
        self.owner_id = owner_id

    def __repr__(self):
        return f"({self.id}) ({self.name}) ({self.owner_id})"

    owner = relationship('User', back_populates='pets')
~~~

The code above defines a model for a pet with a name and an owner. The model has a primary key `id`, a column for the pet's `name`, and a foreign key `owner_id` that references the `ssn` column of the `users` table.

Now insert values into the pets table by adding the following lines of code at the bottom of the `main.py` file:

~~~{.python caption="main.py"}
pet1 = Pet(1, "Dog", user1.ssn)
pet2 = Pet(2, "Cat", user1.ssn)
pet3 = Pet(3, "Rabbit", user4.ssn)
pet4 = Pet(4, "Rabbit", user3.ssn)
session.add(pet1)
session.add(pet2)
session.add(pet3)
session.add(pet4)
session.commit()
~~~

When you execute this code, you will have the output below which shows that the `pets` table has been created and the values above have been added to the `pets` table:

~~~{ caption="Output"}

2023-03-27 11:59:29,850 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2023-03-27 11:59:29,850 INFO sqlalchemy.engine.Engine PRAGMA \
main.table_info("users")
2023-03-27 11:59:29,850 INFO sqlalchemy.engine.Engine [raw sql] ()
2023-03-27 11:59:29,851 INFO sqlalchemy.engine.Engine PRAGMA \
main.table_info("pets")
2023-03-27 11:59:29,851 INFO sqlalchemy.engine.Engine [raw sql] ()
2023-03-27 11:59:29,851 INFO sqlalchemy.engine.Engine PRAGMA \
temp.table_info("pets")
2023-03-27 11:59:29,851 INFO sqlalchemy.engine.Engine [raw sql] ()
2023-03-27 11:59:29,853 INFO sqlalchemy.engine.Engine 
CREATE TABLE pets (
        "ID" INTEGER NOT NULL, 
        "NAME" VARCHAR, 
        "OWNER" INTEGER, 
        PRIMARY KEY ("ID"), 
        FOREIGN KEY("OWNER") REFERENCES users (ssn)
)

2023-03-27 11:59:29,853 INFO sqlalchemy.engine.Engine [no key 0.00017s] ()
2023-03-27 11:59:29,871 INFO sqlalchemy.engine.Engine COMMIT
2023-03-27 11:59:29,879 INFO sqlalchemy.engine.Engine BEGIN (implicit)
2023-03-27 11:59:29,881 INFO sqlalchemy.engine.Engine INSERT INTO pets \
("ID", "NAME", "OWNER") VALUES (?, ?, ?)
2023-03-27 11:59:29,881 INFO sqlalchemy.engine.Engine \
[generated in 0.00031s] [(1, 'Dog', 1000), (2, 'Cat', 1000), \
(3, 'Rabbit', 1003), (4, 'Rabbit', 1002)]
2023-03-27 11:59:29,884 INFO sqlalchemy.engine.Engine COMMIT
~~~

Now if you view your database file, which is, in this case, called *mydb.db* you should have two tables, select the `pets` table and you should have the below output:

<div class="wide">
![Viewing the pets table]({{site.images}}{{page.slug}}/wXxuGXQ.png)
</div>

## Querying a Table

Now that you have seen how to create relationships between tables, how about querying a table with SQLAlchemy?

Up until now, you are expected to have the following snippets in your main.py file:

~~~{.python caption="main.py"}

from sqlalchemy import create_engine, ForeignKey, Column, String, \
Integer, CHAR, CheckConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    ssn = Column("ssn", Integer, primary_key=True)
    firstname =  Column("FirstName", String)
    lastname = Column("LastName", String)
    country = Column("Country", String)
    gender = Column("Gender", CHAR(1), \
    CheckConstraint('gender = upper(gender)'))
    expertise = Column("Expertise", String)
    age = Column("Age", Integer)

    pets = relationship('Pet', back_populates='owner')

    def __init__(self, ssn, firstname, lastname, country, \
    gender, expertise, age):
        self.ssn = ssn
        self.firstname = firstname
        self.lastname = lastname
        self.country = country
        self.gender = gender
        self.expertise = expertise
        self.age = age

    def __repr__(self):
        return f"({self.ssn}) {self.firstname} {self.lastname} \
        ({self.gender},{self.age})"
    
class Pet(Base):
    __tablename__ = 'pets'

    id = Column("ID", Integer, primary_key=True)
    name = Column("NAME", String)
    owner_id = Column("OWNER", Integer, ForeignKey('users.ssn'))

    def __init__(self, id, name, owner_id):
        self.id = id
        self.name = name
        self.owner_id = owner_id

    def __repr__(self):
        return f"({self.id}) ({self.name}) ({self.owner_id})"

    owner = relationship('User', back_populates='pets')
    
engine = create_engine("sqlite:///mydb.db", echo=True)
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()

user1 =  User(1000, "John", "Doe", "San Fransisco", \
"F", "Software Engineer", 35)
user2 = User(1001, "Jane", "Doe", "Mexico", "M", "Data Analyst", 25)
user3 = User(1002, "Bob", "Smith", "Los Angeles", "M", \
"Python Developer", 30)
user4 = User(1003, "Brandy", "Smith", "Califonia", "F", \
"Technical Writer", 23)
user5 = User(1004, "Blue", "Ivy", "Texas", "F", "Singer", 21)

pet1 = Pet(1, "Dog", user1.ssn)
pet2 = Pet(2, "Cat", user1.ssn)
pet3 = Pet(3, "Rabbit", user4.ssn)
pet4 = Pet(4, "Rabbit", user3.ssn)
~~~

And now, we can use SQLAlchemy to list all the entries or data from the **`users`** table using the following command:

~~~{.python caption="main.py"}
output = session.query(User).all()
print(output)
~~~

The command above queries the database for all the rows in the *users* table, using SQLAlchemy's query API. It returns a list of User objects that correspond to the rows in the table.

The **`query(User)`** part specifies that we want to query the *User* class (which represents the *users* table) and the **`.all()`** method specifies that we want to retrieve all the rows.

The resulting list of User objects is stored in the **`output`** variable and then printed to the console using the **`print`** function.

Now when you execute this code, you should have the following output:

<div class="wide">
![Viewing all entries from the user's table]({{site.images}}{{page.slug}}/dU4fn9l.png)
</div>

You can see from the image above that the output was shown using the  `__repr__` method format for the **`User`** class as a list of Python objects.

You can also output all entries from the **`pets`** table with the following command:

~~~{.python caption="main.py"}
output = session.query(Pet).all()
print(output)
~~~

<div class="wide">
![Viewing all entries from pets table]({{site.images}}{{page.slug}}/qE7dY0P.png)
</div>

### Filtering Data

You can also filter results based on certain conditions. The command below will output users that have `Doe` as their last names:

~~~{.python caption="main.py"}
output = session.query(Pet).filter(User.lastname == "Doe")
for i in output:
    print(i)
~~~

<div class="wide">
![Filtering out users with last name (doe) from users table]({{site.images}}{{page.slug}}/FoESeM4.png)
</div>

From the image above, we have two results, **`John Doe`** and **Jane Doe`**.

Additionally, you can also search for all the pets in the database that have the name *Rabbit* using the below line of code:

~~~{.python caption="main.py"}
output = session.query(Pet).filter(Pet.name == "Rabbit")
for i in output:
    print(i)
~~~

The code above searches for all the pets in the database that have the name *Rabbit* using the [**`filter()`**](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.filter) method. Then, it loops through the results and prints each pet's information to the console using a **`for`** loop and the **`print()`**function.

<div class="wide">
![Filtering all pets with name (Rabbit) from pets table]({{site.images}}{{page.slug}}/HjsCVKo.png)
</div>

From the output above you can see that you have two results, a pet named *Rabbit* for users with *ssn* numbers 1003 and 1002 respectively.

Finally, you can retrieve all the users whose country starts with the letter "M" from the `users` table using the following command:

~~~{.python caption="main.py"}
output = session.query(User).filter(User.country.like("M%"))
for i in output:
    print(i)
~~~

<div class="wide">
![Filtering users with countries that start with (M) from *users* table]({{site.images}}{{page.slug}}/IlHIVRr.png)
</div>

If you'd like to know more about the `filter()` method, you can see this [guide](https://github.com/juliotrigo/sqlalchemy-filters)

### Sorting Data

Other than filtering you can also sort data too. To sort data with SQLAlchemy, you can use the [**`.order_by()`**](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.order_by) method of a query object. This method takes one or more columns as arguments and sorts the query result based on those columns.

For example, let's say you want to sort the **`User`** objects by age in descending order. You can modify the query like the following:

~~~{.python caption="main.py"}
output = session.query(User).order_by(User.age.desc()).all()
for i in output:
    print(i)
~~~

<div class="wide">
![Sorting the User object by age in descending order]({{site.images}}{{page.slug}}/anpVj0y.png)
</div>

Sorting the User object by age in descending order

The **`.desc()`** method sorts the data in descending order. You can also use the **`.asc()`**
 method to sort in ascending order.

If you want to sort by multiple columns, you can pass multiple arguments to **`.order_by()`**. For example, if you want to sort by age first and then by first name, you can do:

~~~{.python caption="main.py"}
output = session.query(User).order_by(User.age.desc(), \
User.firstname.asc()).all()
for i in output:
    print(i)
~~~

<div class="wide">
![Sorting the User object by age in descending order and then by firstname in ascending order]({{site.images}}{{page.slug}}/4AQUKoF.png)
</div>

From the image above, the **`User`**object is sorted by age in descending order first, then by first name in ascending order.

### Joining Tables

SQLAlchemy allows you to join tables in a query by using the [**`join()`**](https://docs.sqlalchemy.org/en/14/orm/query.html#sqlalchemy.orm.join) function. Here's an example that demonstrates how to join the **`User`**and **`Pet`**tables and select data from both:

~~~{.python caption="main.py"}
j = join(User, Pet, User.ssn == Pet.owner_id)
result = session.query(User.firstname, Pet.name).select_from(j).all()

for row in result:
    print(row)
~~~

The code above creates a **`join`** object that joins the **`User`**and **`Pet`**tables on the **`ssn`** column of **`User`** and **`owner_id`** column of **`Pet`**. Then, it uses the [**`select_from()`**](https://docs.sqlalchemy.org/en/20/orm/queryguide/query.html#sqlalchemy.orm.Query.select_from) method to select data from the joined tables, specifically the first name of the user and the name of their pet. Finally, the **`all()`** method is called to retrieve all the rows that match the query, and the results are printed out.

<div class="wide">
![Joining and selecting from the user and pet tables]({{site.images}}{{page.slug}}/Xj5Wkjl.png)
</div>

## Conclusion

You now know the magic of SQLAlchemy for managing databases in Python. You can create tables, form relationships between them, and even fetch data using the `query()` method. Exciting stuff, right?

Dive deeper into SQLAlchemy by checking out the [official documentation](https://docs.sqlalchemy.org/en/20/orm/queryguide/index.html). For all the code snippets, just visit this [GitHub repo](https://github.com/mercybassey/sqlalchemy-for-python.git).

And if you enjoyed tweaking databases with SQLAlchemy, you might also want to try [Earthly](https://www.earthly.dev/) for efficient and reproducible build automation.

Happy coding!

{% include_html cta/bottom-cta.html %}
