---
title: "Database Operations in Go using GORM"
categories:
  - Tutorials
toc: true
author: Mercy Bassey
editor: Ubaydah Abdulwasiu

internal-links:
 - database operations
 - go using gorm
 - database operations in go
 - database operations using gorm
excerpt: |
    
---

**We're [Earthly](https://earthly.dev/). We make building software simpler and, therefore, faster. Earthly is open-source and written in go. So if you're interested in a simpler way to build, then [check us out](/).**

In Go, one library stands out when simplifying database interactions. This library is called GORM, which stands for **Go Object-Relational Mapper**.

[GORM](https://gorm.io/docs/index.html) is a developer-friendly library that automates database operations, simplifying the creation, retrieval, updating, and deletion of records. With support for various databases, such as PostgreSQL and MySQL, the GORM library offers a standardized interface to interact with your data, regardless of the underlying database.

This article will dive deep into using the GORM library to perform database operations in Go. You will learn the steps involved in setting up the development environment, connecting to a PostgreSQL database, performing basic CRUD (Create, Retrieve, Update, Delete) operations, and exploring some advanced features of the GORM library. This article will provide a comprehensive guide to managing data effectively using the GORM library.

## Prerequisites

To follow along in this tutorial, you are required to have the following:

- Familiarity with the fundamentals of the Go programming language.
- Some familiarity with relational databases, such as MySQL or PostgreSQL, is beneficial. Knowledge of tables, columns, queries (CRUD operations), and basic SQL syntax will help you grasp the database-related concepts in the article.
- [Go](https://golang.org/doc/install) installed on your machine.
- A PostgreSQL database is already set up, and a user is granted permission to interact with the database. You can check [this guide](https://itslinuxfoss.com/install-setup-postgresql-database-ubuntu-22-04/).

**Note**: You can find the code snippets used in this tutorial [on Github](https://github.com/mercybassey/gorm).

## Setting Up the Environment

To get started, you will need to set up your development environment. Begin by installing the GORM library, which can be done using the following command:

~~~{.bash caption=">_"}
go get -u gorm.io/gorm
~~~

This will fetch and install the GORM library, making it available for use in your Go project.

Next, you need to install the database driver for [PostgreSQL](https://gorm.io/docs/connecting_to_the_database.html#PostgreSQL); doing this will allow the GORM library to communicate with the PostgreSQL database and perform database operations seamlessly.

Execute the following command to install the PostgreSQL driver:

~~~{.bash caption=">_"}
go get -u gorm.io/driver/postgres
~~~

This will install the PostgreSQL driver specifically designed for the GORM library.

<div class="wide">
![Installing postgresql driver for gorm]({{site.images}}{{page.slug}}/GzT6sfO.png)
</div>

<div class="notice--info">

The GORM library also provides database drivers for [MySQL](https://gorm.io/docs/connecting_to_the_database.html#MySQL), [SQLite](https://gorm.io/docs/connecting_to_the_database.html#SQLite), [SQL Server](https://gorm.io/docs/connecting_to_the_database.html#SQL-Server), [TiDB](https://gorm.io/docs/connecting_to_the_database.html#TiDB) and [Clickhouse](https://gorm.io/docs/connecting_to_the_database.html#Clickhouse). You can visit the [GORM library documentation](https://gorm.io/docs/connecting_to_the_database.html) to see how to use these database drivers and create your custom drivers.
</div>

Once you have installed the GORM library and the PostgreSQL database driver, you can connect to your PostgreSQL database and perform database operations.

## Connecting to a Database with the GORM Library

In this section, you will explore how the GORM library handles database connections. To begin, you need to import the GORM library and the PostgreSQL driver package like this:

~~~{.go caption="main.go"}
package main

import (
    "gorm.io/driver/postgres"
    "gorm.io/gorm"
)
~~~

Next, you must provide the connection details to your PostgreSQL database, such as the `host`, `user`, `password`, `dbname`, and `port`. These details are used to construct a connection string called the Data Source Name (DSN). The DSN specifies how to connect to the database.

Add the following code in your `main.go` function to establish a connection:

~~~{.go caption="main.go"}
func main() {
    //Create a new Postgresql database connection
    dsn := "host=<your_host> user=<your_user> \
    password=<your_password> dbname=<your_dbname> port=<your_port>"

    // Open a connection to the database
    db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
    if err != nil {
        panic("failed to connect to database: " + err.Error())
    }
}
~~~

In the code snippet, here's what the code does:

- A connection string using the `dsn` variable is defined. This variable represents the Data Source Name. It contains the necessary information to connect to the PostgreSQL database.

<div class="notice--info">

In this case, be sure to replace the following placeholders - `<your_host>`, `<your_user>`, `<your_password>`, `<your_dbname>`, and `<your_port>` with the actual values corresponding to your own PostgreSQL database configuration.
</div>

- Next, a connection is established to the PostgreSQL database using the `gorm.Open()` function, which takes in two arguments: the first argument is the driver for PostgreSQL, `postgres.Open(dsn)`, which is provided by the GORM library, and the second argument is the configuration, `&gorm.Config{}`. This function returns a database instance (`db`) and an error (`err`).
- Finally, it checks if an error occurs while connecting to the database `(err != nil)`. If an error occurs, the `panic()` function is called with an error message concatenated to it `"failed to connect to the database: " + err.Error()`. This causes the program to exit and print the provided error message alongside the actual error, indicating the failure to connect to the database.

## Performing CRUD operations With the GORM Library

Once you have established a connection to the database using the GORM library, the next step is to define a Go [struct](https://gorm.io/docs/models.html) that represents the model for the corresponding database table. This struct will serve as the schema or blueprint for interacting with the data in the table.

~~~{.go caption="main.go"}
import (
  ...
    "time"
)

type User struct {
        gorm.Model
        FirstName      string    `gorm:"uniqueIndex"`
        LastName       string    `gorm:"uniqueIndex"`
        Email          string    `gorm:"not null"`
        Country        string    `gorm:"not null"`
        Role           string    `gorm:"not null"`
        Age            int       `gorm:"not null;size:3"`
        CreatedAt      time.Time `gorm:"autoCreateTime"`
        UpdatedAt      time.Time `gorm:"autoUpdateTime"`
        DeletedAt gorm.DeletedAt
    }

// --- main function ---
~~~

In the code snippet above, the `time` package is imported to track when a user record is created, updated, and deleted. Then a `User` struct is defined with fields corresponding to the database table's columns. Here's what each field and its associated tag do:

<div class="notice--info">

The GORM library uses [tags](https://gorm.io/docs/models.html#Fields-Tags), which are annotations added to struct fields using backticks (``), to provide additional metadata or instructions to the ORM framework. These tags are crucial in mapping struct fields to database columns, defining column names, specifying data types, enforcing constraints, and configuring table relationships. They provide essential information about the structure and characteristics of the database table and its columns.
</div>

- `gorm.Model`: This field embeds the `gorm.Model` struct, which provides common fields like `ID`, `CreatedAt`, `UpdatedAt`, and `DeletedAt` for tracking the model's metadata.
- `FirstName` and `LastName`: These fields represent the user's first name and last name and have the `gorm:"uniqueIndex"` tag, indicating that the combination of first name and last name is unique in the database, which means you won't be able to have two users with the same first name and last name.
- `Email`, `Country`, `Role`: These fields represent the user's email, country, and role; and have the `gorm:"not null"` tag, ensuring that they are required fields and cannot be empty.
- `Age`: This field represents the user's age and has the `gorm:"not null;size:3"` tag. It is an integer field with a size constraint of `3` digits.
- `CreatedAt`  and `UpdatedAt`: These fields represent the timestamp when the user record was created and updated. They are of type `time.Time` and have the `gorm:"autoCreateTime"` and `gorm:"autoUpdateTime"` tags, respectively, indicating that they should be automatically populated with the current timestamp when a new user record is created or modified.
- `DeletedAt`: This field is of type `gorm.DeletedAt` and is used to handle soft-deletes in GORM. It allows GORM to track the deletion timestamp of a user record and handle logical deletions instead of physically removing the record from the database.

<div class="notice--info">

In the GORM library, "[soft delete](https://gorm.io/docs/delete.html#Soft-Delete)" is a mechanism where records are marked as deleted instead of being physically removed from the database. By defining a `DeletedAt` field with the `gorm.DeletedAt` type in your Go struct, the GORM library sets the value of this field to the current timestamp when a record is deleted, indicating that it's considered deleted but still retained in the database. This provides advantages such as easy retrieval and restoration of deleted records, maintaining a history of changes, and data integrity control. If you prefer not to use the soft delete, you can omit the `DeletedAt` field from your Go struct; that way, the GORM library will perform a hard delete by physically removing the records from the database when you delete them.
</div>

By defining the `User` struct with these fields and tags, the GORM library can automatically handle database operations such as inserting, updating, querying, and deleting records.

### Setting Up Auto Migrations

Once you have defined the Go struct that represents your data model, the next crucial step is to set up auto migrations. [Auto migrations](https://gorm.io/docs/migration.html) is a feature provided by the GORM library that allows you to automatically create or update the database schema based on your Go struct definitions. With auto migrations, you define the structure of your models using Go structs, and the GORM library will generate the necessary SQL statements to create or modify the database schema accordingly. It helps simplify managing the database schema and keeps it in sync with your Go code.

Add the following code snippets to your `main` function right after the database connection code:

~~~{.go caption="main.go"}
// ... Main function ...
// ... Database connection setup code ...

// AutoMigrate will create the necessary tables based on the \
// defined models/structs
err = db.AutoMigrate(&User{})
if err != nil {
    panic("failed to perform migrations: " + err.Error())
}
~~~

This will automatically migrate the `User` struct and ensure the necessary database tables are created or updated based on the defined `User` struct.  

### Creating Records with the GORM Library

Creating records is a fundamental operation when working with databases, as it allows you to store new data in a database table. It involves defining a new instance of the corresponding struct, `User` in this case, and saving it to the database using the GORM library `Create()` function. The GORM library simplifies the process by automatically generating the necessary SQL statements for insertion.

Import the `fmt` package and add the following code snippet to your main function:

~~~{.go caption="main.go"}
import (
...
    "fmt"
)
func main() {
    ...
    // ... Auto Migration Code ...

    // ... Define a new post instance ...

    newUser := User{
        FirstName: "Jane",
        LastName: "Doe",
        Email: "janedoe@gmail.com",
        Country: "Spain",
        Role: "Chef",
        Age: 30,
    }

    // ... Create a new user record...
    result := db.Create(&newUser)
    if result.Error != nil {
        panic("failed to create user: " + result.Error.Error())
    }
     // ... Handle successful creation ...
    fmt.Printf("New user %s %s was created successfully!\\n", \
    newUser.FirstName, newUser.LastName)
}
~~~

The code snippet above does the following:

- Defines a new `User` struct instance with the desired field values for the user, such as `first_name`, `last_name`, `email`, `country`, `role`, and `age`.

<div class="notice--info">

### A Quick Note On Field Names

When working with the GORM library, whether you define field names in your struct with uppercase or lowercase letters, the field names will be automatically converted to lowercase letters in the database. If a field name contains more than one word, an underscore (_) will separate it in the database.
</div>

- Uses the `db.Create(&newUser)` method to create a new user record in the database. The `&newUser` is a pointer to the `newUser` struct, allowing the GORM library to modify the struct with an auto-generated primary key and other database-managed fields.
- Checks for any error that occurs during the creation process. If an error is encountered, the application panics and displays the error message `"failed to create user: " + result.Error.Error()` alongside the actual error.
- Lastly, if the user record creation is successful, it prints a confirmation message using `fmt.Printf`, indicating that the new user has been created. The message includes the first name and last name of the newly created user.

Now, execute the `go run` command and head to your Postgres database to confirm the `User` record has been created.

~~~{ caption="Output"}
New User Jane Doe was created successfully!
~~~

~~~

 id |           created_at              |           updated_at          | deleted_at    | first_name    | last_name | email              |country| role | age
----+-------------------------------+-------------------------------+------------+------------+-----------+-------------------+---------+------+-----
  1 |   2023-07-21 08:11:49.017357+01   | 2023-07-21 08:11:49.017357+01 |               | Jane          | Doe       | janedoe@gmail.com  | Spain | Chef | 30
(1 row)
~~~

At this point, you have successfully created a record with the GORM library.

### Retrieving Records with the GORM Library

Whether there is a need to fetch single or multiple records, the GORM library offers a convenient and powerful solution for querying the database. Here, you will use the GORM library to fetch a single record from the database and retrieve multiple records.

You can use the `First` method when retrieving a single record.

Let's start by retrieving the `User` record created in the previous section, `Jane Doe`. You can achieve this using the following code:

~~~{.go caption="main.go"}
func main() {
        // ...AutoMigrate code ...

        // Retrieve the first user from the database
        var user User
        result := db.First(&user)
        if result.Error != nil {
            panic("failed to retrieve user: " + result.Error.Error())
    }

    // Use the user record
    fmt.Printf("User ID: %d, Name: %s %s, Email: %s\n", user.ID, \
    user.FirstName, user.LastName, user.Email)
}
~~~

The updated code shows that the `newUser` instance and the `result` variable of `db.Create(&newUser)` used to create a user record in the previous section have been removed. This change is necessary because keeping these variables in your code is unnecessary once you have successfully added the user record to the database.

They were originally used to create a new user instance, handle errors during user creation, and display a success message. However, since the user has already been added, these steps are optional for this code snippet.

Considering the updated code snippet above, the following actions were performed:

- A variable `user` of type `User` (i.e., the struct called `User` ) was declared to store the retrieved user record.
- The database was queried, and the first user record was retrieved using the  `db.First(&user)` method call.

<div class="notice--info">

When retrieving a single record, the GORM library provides multiple methods to suit different scenarios; it offers additional methods like [`Take`](https://gorm.io/docs/query.html) and [`Last`](https://gorm.io/docs/query.html) alongside the [`First`](https://gorm.io/docs/query.html) method. These methods allow you to fetch a single record based on different criteria. For detailed information and examples on using these methods, I recommend referring to the comprehensive [GORM library documentation](https://gorm.io/docs/query.html#Retrieving-a-single-object), which will help you effectively leverage them in your code.
</div>

- If an error occurs during retrieval, such as the user not being found, the code will panic and display an error message `"failed to retrieve user: " + result.Error.Error()"`; alongside the actual error; otherwise, the `user` variable is used to access and work with the user's attributes and then print out the user's `ID`, `first_name`, `last_name`, and `email` in a formatted string `fmt.Printf`.

Once you run the code, you are expected to have the following output:

~~~{ caption="Output"}
User ID: 1, Name: Jane Doe, Email: janedoe@gmail.com
~~~

<div class="notice--info">

Additionally, you can retrieve a record using its primary key. The following example is from the [GORM library documentation](https://gorm.io/docs/query.html#Retrieving-objects-with-primary-key). Or, If you'd like to fetch more than one record by their primary keys, you can pass the primary key value(s) to the `Find` method. See how to use the [`Find` method](https://gorm.io/docs/query.html#Retrieving-objects-with-primary-key).
</div>

For cases where you'd need to retrieve records based on certain conditions, you can use the [`Where`](https://gorm.io/docs/query.html#Conditions) method like this:

~~~{.go caption="main.go"}
...
var users []User
result := db.Where("ID = ?", 1).Find(&users)
if result.Error != nil {
    panic("failed to retrieve user: " + result.Error.Error())
}

// iterate over the users slice and print the details of each user
for _, user := range users {
    fmt.Printf("User ID: %d, Name: %s %s, Email: %s\n", user.ID, \
    user.FirstName, user.LastName, user.Email)
}
~~~

Here, records are retrieved from the `User` table where the ID equals `1` using the `Where` method.

If you'd like to chain multiple conditions, you can say:

~~~{.go caption="main.go"}
...
var users []User
result := db.Where("FirstName = ?", "Jane").Where("Country = ?", "Spain")/
.Find(&users)
if result.Error != nil {
    panic("failed to retrieve users: " + result.Error.Error())
}

// Use the user records
for _, user := range users {
    fmt.Printf("User ID: %d, Name: %s %s, Email: %s\n", user.ID, /
    user.FirstName, user.LastName, user.Email)
}
~~~

This will retrieve the record where the `first_name` is `Jane` and the `country` is `Spain`:

~~~{ caption="Output"}
User ID: 1, Name: Jane Doe, Email: janedoe@gmail.com
~~~

<div class="notice--info">

For other condition types like [`Or`](https://gorm.io/docs/query.html#Or-Conditions) and [`Not`](https://gorm.io/docs/query.html#Not-Conditions) you can see the following [guide](https://gorm.io/docs/query.html#Specify-Struct-search-fields)
</div>

Finally, using the `Find` method, you can retrieve multiple records without specific conditions. Here's an example code snippet:

~~~{.go caption="main.go"}
var users []User
result := db.Find(&users)
if result.Error != nil {
    // handle error
    panic("failed to retrieve users: " + result.Error.Error())
}

// Iterate over the users slice and print the details of each user
for _, user := range users {
    fmt.Printf("User ID: %d, Name: %s %s, Email: %s\n", user.ID, \
    user.FirstName, user.LastName, user.Email)
}
~~~

The code above will retrieve a collection of users from the database using the `Find` method of the `db` object. If an error occurs during the retrieval process, the code will panic and display the error message. Afterward, it iterates over the retrieved users and prints their details, including the user `ID`, `first name`, `last name`, and `email`.

### Updating Records with the GORM Library

When working with the GORM library, you can update records by modifying the fields of a struct and then saving the changes to the database.

~~~{.go caption="main.go"}
    // Retrieve the record you want to update
    var user User
    result := db.First(&user, 1)
    if result.Error != nil {
        panic("failed to retrieve user: " + result.Error.Error())
    }

    // Modify the attributes of the retrieved record, in this case, \
    // the first three columns
    user.FirstName = "Agnes"
    user.LastName = "Doe"
    user.Email = "agnesdoe@example.com"

    // Save the changes back to the database
    result = db.Save(&user)
    if result.Error != nil {
        panic("failed to update user: " + result.Error.Error())
    }

    fmt.Println("User updated successfully")
~~~

The code above will retrieve a specific user record from the database using the `First`method of the `db` object. If an error occurs during the retrieval process, the code will panic and display the error message.

Then, it modifies the attributes of the retrieved record, specifically the `first_name`, `last_name`, and `email`. The changes are saved to the database using the `Save` method. If an error occurs during the update process, the code will panic and display the error message.

Finally, it prints a message indicating the user has been updated successfully.

<div class="notice--info">

If you want to update a single column with the GORM library, use the `Update` or `Updates` method with a `map` or `struct` specifying the column and its new value. Here's an example of updating a single column using the `update` method with a `struct`:
</div>

~~~{.go caption="main.go"}
 // Update the 'role' column of the record with ID 1
 result := db.Model(&User{}).Where("id = ?", 1).Update("role", "admin")
 if result.Error != nil {
     panic("failed to update user: " + result.Error.Error())
 }
 
 fmt.Println("User role updated successfully")
~~~

When you execute the code above, you should have the following output:

~~~{ caption="Output"}
User updated successfully
~~~

~~~
id  |          created_at           |          updated_at           | deleted_at | first_name | last_name |        email         | country | role | age 
----+-------------------------------+-------------------------------+------------+------------+-----------+----------------------+---------+------+-----
1   | 2023-07-21 08:11:49.017357+01 | 2023-07-21 08:18:11.986069+01 |            | Agnes      | Doe       | agnesdoe@example.com | Spain   | Chef |  30
(1 row)
~~~
  
Alternatively, you can update records using a struct `User` to define the changes. Here's an example:

~~~{.go caption="main.go"}
// Update the record with ID 1
    result := db.Model(&User{}).Where("id = ?", 1).Updates(User{
        FirstName: "John",
        LastName:  "Doe",
        Email:     "johndoe@example.com",
    })
    if result.Error != nil {
        panic("failed to update user: " + result.Error.Error())
    }

    fmt.Println("User updated successfully")
~~~

~~~{ caption="Output"}
User updated successfully
~~~

In this case, you don't need to retrieve the user before updating. The code directly updates the user record with ID `1` using the `Updates` method on the model. It specifies the new values for the user's `first_name`, `last_name`, and `email` fields.

### Deleting Records with the GORM Library

The GORM library provides several methods to delete records based on different criteria. You can either delete a single record or delete multiple records.

To delete a single record, you can use the [`Delete`](https://gorm.io/docs/delete.html) method from the GORM library. The `Delete` method takes the model instance as an argument and deletes the corresponding record from the database. Here's an example:

~~~{.go caption="main.go"}
var user User
result := db.First(&user)
if result.Error != nil {
    panic("failed to retrieve user: " + result.Error.Error())
}

result = db.Delete(&user)
if result.Error != nil {
    panic("failed to delete user: " + result.Error.Error())
} else if result.RowsAffected == 0 {
    panic("no user record was deleted")
} else {
    fmt.Println("User record deleted successfully")
}
~~~

The code retrieves the first user record from the database using the GORM library's  `First` method and then deletes that user record using the `Delete` method. If any error occurs during the retrieval or deletion, the code panics with the corresponding error messages. Additionally, it checks if any user records were deleted and prints a success message if the deletion is successful.

<div class="notice--info">

In the given code, the condition `else if result.RowsAffected == 0` determines the number of rows affected by the database operation. It represents the number of rows that were successfully deleted from the database. By checking the value of `RowsAffected`, different scenarios can be handled based on whether any records were deleted.
</div>

You can use the `Delete` method with a condition to delete multiple records that match certain criteria. The condition is specified using the `Where` method as shown below:

~~~{.go caption="main.go"}
// Delete the record where the country is "Spain"
record := db.Where("country = ?", "Spain").Delete(&User{})
if record.Error != nil {
    panic("failed to delete user: " + record.Error.Error())
}
fmt.Println(record.RowsAffected, "user record(s) deleted successfully")
~~~

Once you run this code, the following output is expected, meaning that one row has been affected and a record with the country `Spain` has been marked deleted:

~~~{ caption="Output"}
1 user record(s) deleted successfully
~~~

On your PostgreSQL database, you should have the following output:

~~~
 id |          created_at           |          updated_at           |          deleted_at           | first_name | last_name |        email        | country | role | age 
----+-------------------------------+-------------------------------+-------------------------------+------------+-----------+---------------------+---------+------+-----
  1 | 2023-07-21 08:11:49.017357+01 | 2023-07-21 08:22:54.662504+01 | 2023-07-21 08:23:52.095621+01 | John       | Doe       | johndoe@example.com | Spain   | Chef |  30
(1 row)
~~~

## Exploring Advanced Features with the GORM Library

The GORM library is used to perform basic CRUD operations and provides several advanced mechanisms to handle complex database tasks efficiently. In this section, you will briefly learn about [Transactions](https://gorm.io/docs/transactions.html), [Preloading/eager loading](https://gorm.io/docs/preload.html), and [Hooks](https://gorm.io/docs/hooks.html).

Transactions allow you to group a set of database operations into a unit of work. This ensures that all operations succeed or fail. You can use the GORM library transaction methods to begin a transaction, perform database operations within the transaction, and commit or roll back the transaction based on success or failure. Here's an example:

~~~{.go caption="main.go"}
// ... Auto migration code ...
// Begin a transaction
tx := db.Begin()

// Create a new user
newUser := User{
    FirstName: "Billy",
    LastName: "John",
    Email: "billy56@gmail.com",
    Country: "Germany",
    Role: "Developer Advocate",
    Age: 40,
}

// Perform database operations within the transaction
if err := tx.Create(&newUser).Error; err != nil {
    tx.Rollback() // Rollback the transaction if an error occurs
    panic("failed to create user: " + err.Error())
}

// Update the user's profile
newUser.Country = "Morocco"
if err := tx.Save(&newUser).Error; err != nil {
    tx.Rollback() // Rollback the transaction if an error occurs
    panic("failed to update user: " + err.Error())
}

// Commit the transaction if all operations succeed
tx.Commit()

fmt.Println("User created and updated successfully")
~~~

The code above starts a transaction with `db.Begin()`. A new user is created and saved to the database within the transaction using `tx.Create(&newUser)`. If an error occurs during the creation, the transaction is rolled back to ensure data consistency. Next, the user's profile is updated, and the changes are saved using `tx.Save(&newUser)`. If there's an error, the transaction is rolled back. Finally, if all operations succeed, the transaction is committed with `tx.Commit()`.

Once you run this code, the following output is expected:

~~~{caption="Output"}
User created and updated successfully
~~~

~~~
 id |          created_at           |          updated_at           |          deleted_at           | first_name | last_name |        email        | country |        role        | age 
----+-------------------------------+-------------------------------+-------------------------------+------------+-----------+---------------------+---------+--------------------+-----
  1 | 2023-07-21 08:11:49.017357+01 | 2023-07-21 08:22:54.662504+01 | 2023-07-21 08:23:52.095621+01 | John       | Doe       | johndoe@example.com | Spain   | Chef               |  30
  2 | 2023-07-21 08:30:21.006221+01 | 2023-07-21 08:30:21.007037+01 |                               | Billy      | John      | billy56@gmail.com   | Morocco | Developer Advocate |  40
(2 rows)
~~~

The GORM library preloading feature enhances data fetching by automatically joining tables and fetching related data in a single query, improving efficiency. However, since this tutorial focuses on a single table scenario, exploring the preloading feature is beyond its scope. For a comprehensive understanding of this powerful feature, refer to the [official GORM library documentation](https://gorm.io/docs/preload.html).

Finally, hooks are callback functions executed at various stages of the ORM lifecycle. Hooks enable you to perform custom actions before or after specific database operations such as create, update, delete, or query. You can define hooks for your models to implement custom logic, validations, or trigger side effects based on specific events. Here's an example:

~~~{.go caption="main.go"}
// ... User Struct ...
func (u *User) BeforeCreate(tx *gorm.DB) error {
    // Perform some actions before creating a user
    fmt.Println("Preparing to create user:", u.FirstName, u.LastName)
    return nil
}

func (u *User) AfterCreate(tx *gorm.DB) error {
    // Perform some actions after creating a user
    fmt.Println("User created successfully:", u.FirstName, u.LastName)
    return nil
}

// ... main function ...
func main() {
        // ... database connection code ...

    // ... Auto migration code ...

    // Begin a transaction
    tx := db.Begin()

    // Create a new user
    newUser := User{
        FirstName: "John",
        LastName: "mark",
        Email: "john@gmail.com",
        Country: "Argentina",
        Role: "Technical Writer",
        Age: 35,
    }

    // Perform database operations within the transaction
    ...
    // Update the user's profile
    ...
    // Commit the transaction if all operations succeed
    tx.Commit()
    
    fmt.Println("User created and updated successfully")
}
~~~

This defines two hooks, `BeforeCreate` and `AfterCreate`, for the `User` struct. The `BeforeCreate` hook is executed before creating a user, and the `AfterCreate` hook is executed after creating a user.

Once you run this code, the following output is expected:

~~~{caption="Output"}
Preparing to create user: John Mark
User created successfully: John Mark
User created and updated successfully
~~~

This indicates that the `BeforeCreate` and `AfterCreate` hooks were triggered before and after the transaction created the user - `John Mark`. The following string was outputted at the transaction: `User created and updated successfully`. For examples of how to use hooks, you can see the following from the [GORM library documentation](https://gorm.io/docs/hooks.html).

## Conclusion

As you have seen, GORM is a powerful ORM library for Go, simplifying database operations and enhancing productivity. This article covered key concepts about the GORM library, like model definition, CRUD operations, querying, and advanced features such as transactions, preloading, and hooks.

To optimize your Go applications with the GORM library, consider these best practices:

- Establish clear naming conventions for models, fields, and relationships to improve readability and maintainability.
- Utilize the GORM library migration feature for efficient database schema management and versioning.
- Leverage transactions to ensure data consistency and atomicity when performing multiple database operations.
- Implement proper data validation and error handling to maintain data integrity.

Following these practices will give you a solid foundation for building robust and efficient applications with the GORM library. For further exploration, consider delving into creating multiple structs, establishing relationships, and maximizing the potential of the GORM library preloading feature.

{% include_html cta/bottom-cta.html %}
