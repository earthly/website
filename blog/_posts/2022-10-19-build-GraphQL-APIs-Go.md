---
title: "How to Build GraphQL APIs Using Go"
categories:
  - Tutorials
toc: true
author: Rose Chege

internal-links:
 - GraphQL
 - API
 - Go
 - MySQL
excerpt: |
    Learn how to build GraphQL APIs using Go and MySQL. This tutorial covers the basics of GraphQL, setting up a Go GraphQL server using gqlgen, connecting to a MySQL database, and implementing resolvers for mutations and queries. If you're interested in building efficient and type-safe APIs with Go, this article is for you.
last_modified_at: 2023-07-19
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. If you're into building GraphQL APIs using Go, you should definitely take a look. Earthly can streamline your build process and save you time. [Check it out](/).**

## Prerequisites

To follow along with this guide, it is essential to have the following:

- [Golang installed](https://go.dev/doc/install) and ready to run Go code.
- [MySQL server](https://dev.mysql.com/downloads/mysql/) correctly installed together with MySQL Workbench for MySQL database management.

You can jump ahead and get the code used for this guide in this [GitHub repository]( https://github.com/Rose-stack/go-mysql-graphql-api).

## Getting Started with GraphQL and Go

GraphQL is a query language for APIs used to communicate data between a client and a server. It's defined using schema to query data from a server or mutate data remotely. GraphQL provides strongly typed tooling for your server.

Implementing a GraphQL API with Go benefits from the fact that both GraphQL and Go are typed languages. This ensures that your APIs are checked before compile time, making it very convenient for your Go code base to [make](/blog/makefiles-on-windows) the valid query, while GraphQL ensures results are correctly checked.

Go allows you to use libraries to generate type-safe code for GraphQL APIs. Such tools include the [gqlgen](https://gqlgen.com/).

## Gqlgen for Go GraphQL APIs

Gqlgen is a Go GraphQL library that allows you to build robust GraphQL servers without creating everything from scratch. Gqlgen is a schema first library meaning it creates the API schema using GraphQL [schema definition language](https://graphql.org/learn/schema/). Using that schema as the input, gqlgen generates the GraphQL server code. This way, you can build applications quickly. All you need is to implement the core logic of your GraphQL resolvers.

## Generating Boilerplate Go GraphQL API Using Gqlgen

Let's dive in and implement the API using gqlgen. First, initialize a [Golang](/blog/top-3-resources-to-learn-golang-in-2021) application inside the directory where you want the project to live:

~~~{.bash caption=">_"}
go mod init go-graphql-api
~~~

Install the gqlgen library to your project dependencies:

~~~{.bash caption=">_"}
go get github.com/99designs/gqlgen
~~~

At the root directory of your application, create a `tools.go` file and add an import for gqlgen:

~~~{.go caption="tools.go"}
package tools
 
import (
_ "github.com/99designs/gqlgen"
)
~~~

This file allows you to add the installed missing dependencies the project requires. Run the following command to add your direct dependencies:

~~~{.bash caption=">_"}
go mod tidy
~~~

Initialize gqlgen to build your boilerplate Go GraphQL API:

~~~{.bash caption=">_"}
go run github.com/99designs/gqlgen init
~~~

This will create a basic GraphQL API with the following file structure:

~~~{.text caption=""}
| gqlgen.yml
| server.go
|   
\---graph
    | resolver.go
    | schema.graphqls
    | schema.resolvers.go
    |   
    +---generated
    | generated.go
    |       
    \---model
            models_gen.go
~~~

- `gqlgen.yml` - contains the gqlgen configurations.
- `server.go` - the application entry point that serves your GraphQL endpoint.
- `graph/resolver.go` - contains the type for your resolvers.
- `graph/schema.graphqls` - a file to write down your API schemas.
- `graph/schema.resolvers.go` - contains the generated resolvers methods that you use to implement your API Mutation and Query types.
- `graph/model/models_gen.go` - contains structs generated from the schema file.
- `graph/generated/generated.go` - contains the generated runtime for GraphQL.

## Setting up GraphQL Schema for Go

gqlgen lets you create a schema that fits your application and then generates the resolvers and structs using the created schema. To create a post API, for example, you need to build a schema for posts based on the [Schema Definition Language](https://graphql.org/learn/schema/). Navigate to the `graph/schema.graphqls` file and replace the existing schema with the following post schema:

~~~{.text caption="schema.graphqls"}
type Post {
  id: Int!
  Title: String!
  Content: String!
  Author: String!
  Hero: String!
  Published_At: String!
  Updated_At: String!
}
 
type Query {
  GetAllPosts: [Post!]!
  GetOnePost(id: Int!): Post!
}
 
input NewPost {
  Title: String!
  Content: String!
  Author: String
  Hero: String
  Published_At: String
  Updated_At: String
}
 
type Mutation {
  CreatePost(input: NewPost!): Post!
  UpdatePost(PostId: Int!, input: NewPost): Post!
}
~~~

A schema defines the types of data you want to handle and the operations you want to be able to make on that data. First, we create a type of `Post` with different fields associated with a post. This type includes all the post fields you want to fetch using GraphQL. The type Query sets the operations related to how we can read post data. In this case, the schema will create two queries:

- Retrieve all the posts.
- Retrieve a single post based on the post ID of that specific record.

To handle mutations, or writes, we create an input type to manage the data that mutates. Then we can create a type Mutation to handle all mutation operations. These are:

- Creating a post
- Updating the post values

These are the parameters that gqlgen will look for to create the structs and the different resolvers for both Mutation and Query.

## Generating GraphQL Resolvers With Gqlgen

Using the above schema, gqlgen will auto-generate the structs and resolves. This will be executed using a single command to generate these code blocks. Run the following command:

~~~{.bash caption=">_"}
go run github.com/99designs/gqlgen generate
~~~

If you head over to the `graph/schema.resolvers.go`, your post resolvers will be created based on your schema.

~~~{.go caption="schema.resolvers.go"}
package graph
 
// This file will be automatically regenerated based on the schema,\
any resolver implementationswill be copied through when generating \
and any unknown code will be moved to the end.
 
import (
    "context"
    "fmt"
    "go-graphql-api/graph/generated"
    "go-graphql-api/graph/model"
)
 
// CreatePost is the resolver for the CreatePost field.
  func (r *mutationResolver) CreatePost(ctx context.Context, \
  input model.NewPost) (*model.Post, error) {
  panic(fmt.Errorf("not implemented: CreatePost - CreatePost"))
}
 
// UpdatePost is the resolver for the UpdatePost field.
  func (r *mutationResolver) UpdatePost(ctx context.Context, postID int, \
  input *model.NewPost) (*model.Post, error) { \
  panic(fmt.Errorf("not implemented: UpdatePost - UpdatePost"))
}
 
// GetAllPosts is the resolver for the GetAllPosts field.
  func (r *queryResolver) GetAllPosts(ctx context.Context) \
  ([]*model.Post, error) {
  panic(fmt.Errorf("not implemented: GetAllPosts - GetAllPosts"))
}
 
// GetOnePost is the resolver for the GetOnePost field.
  func (r *queryResolver) GetOnePost(ctx context.Context, id int)\
  (*model.Post, error) {
  panic(fmt.Errorf("not implemented: GetOnePost - GetOnePost"))
}
 
// Mutation returns generated.MutationResolver implementation.
  func (r *Resolver) Mutation() generated.MutationResolver \
  { return &mutationResolver{r} }
 
// Query returns generated.QueryResolver implementation.
  func (r *Resolver) Query() generated.QueryResolver \
  { return &queryResolver{r} }
 
  type mutationResolver struct{ *Resolver }
  type queryResolver struct{ *Resolver }
~~~

The `graph/model/models_gen.go` file will have the structs for your posts.

~~~{.go caption="models_gen.go"}
// Code generated by github.com/99designs/gqlgen, DO NOT EDIT.
 
package model
 
type NewPost struct {
  Title       string  `json:"Title"`
  Content     string  `json:"Content"`
  Author *string `json:"Author"`
  Hero *string `json:"Hero"`
  PublishedAt *string `json:"Published_At"`
  UpdatedAt *string `json:"Updated_At"`
}
 
type Post struct {
  ID          int    `json:"id"`
  Title       string `json:"Title"`
  Content     string `json:"Content"`
  Author      string `json:"Author"`
  Hero        string `json:"Hero"`
  PublishedAt string `json:"Published_At"`
  UpdatedAt   string `json:"Updated_At"`
}
~~~

## Setting Up the Database Dependencies

To correctly implement this API, we need to use a database to interact directly with data on the actual server. Also, we will use [Gorm ORM](https://gorm.io/) to perform all database-related connections effectively. Gorm has support for MySQL, PostgreSQL, SQLite, and SQL Server. It makes it easier to interact with SQL-based databases with [features](https://gorm.io/docs/index.html) such as:

- ORM,
- Auto database migration,
- CRUD hooks methods such as create, update, etc.

To install it, run:

~~~{.bash caption=">_"}
go get github.com/jinzhu/gorm   
~~~

We'll use the MySQL database. Ensure [MySQL drivers](https://github.com/go-sql-driver/mysql) are installed in your application:

~~~{.bash caption=">_"}
go get github.com/go-sql-driver/mysql
~~~

At this point, ensure your [MySQL](/blog/docker-mysql) server is up and running. Then follow these instructions to establish a database connection to your server:

## Connecting Database To Go

To start interactions with the database, you need to establish a connection to it using Go. First, create a `dbmodel` directory and add a `db_model.go` file. Then create a Model of Posts using Gorm.

~~~{.go caption="db_model.go"}
package dbmodel
 
 
type Post struct {
  ID uint64 `sql:"AUTO_INCREMENT" gorm:"primary_key"`
  Title string `gorm:"not null"`
  Content string `gorm:"not null"`
  Author string `gorm:"not null; unique"`
  Hero string `json:"Hero"`
  Published_At string `json:"PublishedAt"`
  Updated_At string `json:"UpdateAt"`
}
~~~

**Note**: You can use the `Post` struct generated by gqlgen. However, it's good to take advantage of Gorm and describe your database structure with a few lines of code.

Create a `database` directory and add a `mysql.go` file. Then set your connection as follows:

Add the module package name and import the dependencies

~~~{.go caption="mysql.go"}
package database
 
import (
  "fmt"
  _ "github.com/go-sql-driver/mysql"
  "github.com/jinzhu/gorm"
  "go-graphql-api/dbmodels"
)
~~~

You can still run the `go mod tidy` command to ensure any missing dependencies are added to your direct dependencies.

Create the following variables:

~~~{.go caption="mysql.go"}
// a variable to store database connection
var DBInstance *gorm.DB
// Var for error handling
var err error
// the db connection string
var CONNECTION_STRING string = \
"db_username:your_user_password@tcp(localhost:3306)/?charset=utf8&parseTime=True&loc=Local"
~~~

Your `CONNECTION_STRING` should reflect the credentials of your MySQL server, such as your user and the MySQL user password.

Establish the connection to your database:

~~~{.go caption="mysql.go"}
// connecting to the db
func ConnectDB() {
  // pass the db connection string
  ConnectionURI := CONNECTION_STRING
  // check for db connection
  DBInstance, err = gorm.Open("mysql", ConnectionURI)
  if err != nil {
  fmt.Println(err)
  // if the connection was unsuccessful
  panic("Database connection attempt was unsuccessful.....")
 } else {
  // if the connection was successful
  fmt.Println("Database Connected successfully.....")
 }
 // log all database operations performed by this connection
 DBInstance.LogMode(true)
}
~~~

The `CONNECTION_STRING` opens a connection to the MySQL server. The result of your connection will be logged in your terminal when running the application. `LogMode(true)` will allow the application to log all database operations to your terminal. You can set it to false if you don't need database operations output.

Create a database:

~~~{.go caption="mysql.go"}
func CreateDB() {
  // Create a database
  DBInstance.Exec("CREATE DATABASE IF NOT EXISTS Blog_Posts")
 // make the database available to this connection
  DBInstance.Exec("USE Blog_Posts")
}
~~~

Instead of manually creating a database, use the Gorm ORM to handle this. It will execute the above query and create the database for you.

Migrate Post Model to a database table:

~~~{.go caption="mysql.go"}
func MigrateDB() {
  // migrate and sync the model to create a db table
  DBInstance.AutoMigrate(&dbmodel.Post{})
  fmt.Println("Database migration completed....")
}
~~~

The Post models the structure of the database table. This migration will ensure that a table Post is created and synced with the fields of the Post struct.

This database connection needs to be accessed by the resolvers. The created resolver doesn't have the objects to get this connection. For the Resolvers to access the stored database connection, head over to the `graph/resolver.go`. Add the connection to the resolver's struct:

~~~{.go caption="resolver.go"}
import (
  "github.com/jinzhu/gorm"
)
 
type Resolver struct {
  Database *gorm.DB
}
~~~

Finally, you need to execute the database connection on our server. The connection will get executed once the application is started. The established connection will then be saved within the Resolver struct created above. This way, it is easier to execute this connection using the generated resolvers to perform different operations.

Navigate to the `server.go` file and import the database package:

~~~{.go caption="server.go"}
import(
  "go-graphql-api/database"
)
~~~

Execute the following database functions:

~~~{.go caption="server.go"}
  // establish connection
  database.ConnectDB()
  // create db
  database.CreateDB()
  // migrate the db with Post model
  database.MigrateDB()
~~~

Save the established database connection in the Resolver struct of your `srv` variable generated by gqlgen:

~~~{.go caption="server.go"}
srv := handler.NewDefaultServer(generated.NewExecutableSchema\
(generated.Config{Resolvers: &graph.Resolver{
  Database: database.DBInstance,
}}))
~~~

The database is now set to execute a connection and carry out the expected database operations.

First, run the application to ensure the set database works as expected. To run the server, use [Air](https://github.com/cosmtrek/air) so that you can live reload the server when you make new changes. This way, focus on your code. Once you run the server once, Air will execute your new changes and reload the app for you. To install Air run:

~~~{.bash caption=">_"}
$ go install github.com/cosmtrek/air@latest
~~~

Then initialize it using:

~~~{.bash caption=">_"}
$ air init
~~~

Note: You may be required to delete the `tools.go` file created earlier. You can confidently delete this file as we no longer need it. Otherwise, Air will generate an error **tool.go:4:2: import "github.com/99designs/gqlgen" is a program, not an importable package.**

Now that Air is set, at the root directory of your application, run:

~~~{.bash caption=">_"}
$ air
~~~

This should perform the database connection methods created. This includes establishing a connection to the database, creating the database, and performing the database migration. The results of these operations should be logged on to your terminal as follows:

You can confirm if these changes were recoded to your database:

## Implementing the Resolvers

The generated resolves do not have the logic of a Post API. You need to implement the logic for the resolver methods for performing GraphQL mutations and queries.

### Building Go Mutation Resolver

In your `graph/schema.resolvers.go` file, two mutations resolvers were generated:

- CreatePost is the resolver for creating a post.
- UpdatePost is the resolver for updating post fields.

These mutations, however, have not yet been handled. They are still the boilerplate code. We need to modify them to handle the mutations logic. Head over to your `graph/schema.resolvers.go` and start working on the mutation methods as follows:

#### Creating Posts Mutation

First, add time to your imports. Some fields require time, and the time parameter format is added to the database.

To create a post, modify the `CreatePost` method as follows:

~~~{.go caption="graph/schema.resolvers.go"}
// CreatePost is the resolver for the CreatePost field.
func (r *mutationResolver) CreatePost(ctx context.Context, \
input model.NewPost) (*model.Post, error) {
 Addpost := model.Post{
  Title: input.Title,
  Content: input.Content,
  Author: *input.Author, 
  Hero: *input.Hero,
  PublishedAt: time.Now().Format("20-08-2022"),
  UpdatedAt: time.Now().Format("20-08-2022"),
 }
 
 if err := r.Database.Create(&Addpost).Error; err != nil {
  fmt.Println(err)
  return nil, err
 
 }
 
 return &Addpost, nil
}
~~~

We can create values into the database using the SQL `Create()` method. It takes the parameter of the Post model that you want to add. The `Addpost` variable perfectly describes this.

To execute the `CreatePost` mutation, ensure the server is still up and running. Otherwise, re-run your server using the `air` command. To test the API, open `http://localhost:8080/` to access your API GraphQL playground in the browser.

The GraphQL playground is ready, and you see all the GraphQL root types for each kind of operation related to the created API.

On your GraphQL playground, execute the following mutation:

~~~{.text caption=""}
mutation createPost {
  CreatePost(
    input: {
      Title: "How to Build GraphQL API using Go and MySQL",
      Content: "We will create a Build GraphQL API using \
      the MySQL database server to perform the different operations \
      using the GraphQL API.",
      Author: "Rose Chege",
      Hero: \
      "https://cdn.pixabay.com/photo/2016/12/28/09/36/web-1935737_1280.png",
    })
  {
    id
    Title
  }
}
~~~

Once you hit the Play Button, the new post will be added to the database.

Go ahead and add different posts using the above schema as an example.

You can confirm this addition on your MySQL database to see if a new post got added.

#### Updating Posts Mutation

Modify the `UpdatePost()` method to add the update mutation resolver:

~~~{.go caption="graph/schema.resolvers.go"}
// UpdatePost is the resolver for the UpdatePost field.
func (r *mutationResolver) UpdatePost(ctx context.Context, \
postID int, input *model.NewPost) (*model.Post, error) {
  Updatepost := model.Post{
    Title: input.Title,
    Content: input.Content,
    UpdatedAt: time.Now().Format("20-08-2022"),
  }
 
 if err := r.Database.Model(&model.Post{}).Where("id=?", postID)\
 .Updates(&Updatepost).Error; err != nil {
    fmt.Println(err)
    return nil, err
 }
 
 Updatepost.ID = postID
  return &Updatepost, nil
}
~~~

First, add the fields to execute on the update mutation as described in the `Updatepost` variable. To alter any available posts, you need to execute a SQL query matching the updated post. The `Where` clause takes the post id parameter to check the mutated database record.

Updating mutates your saved data. Therefore, a mutation of new data is sent to your database to update a post. To edit an existing post, use the following schema on your GraphQL playground:

~~~{.text caption=""}
mutation UpdatePost {
  UpdatePost(PostId:10 input:{
 
    Title: "How to Build GraphQL API using MongoDB and Go"
    Content : "This guide will help you create a Go MongoDB API"
  }){
    id
    Title
    Content
  } 
}
~~~

Note: The value of the `postId` should be the database id of the exiting post that you want to update.

Go ahead and check if the changes were implemented to the selected post.

### Building Go Query Resolver

#### Retrieve All Posts Query

Add the following modifications to the `GetAllPosts` method in `graph/schema.resolvers.go` to add a resolver that fetches all posts.

~~~{.go caption="graph/schema.resolvers.go"}
// GetAllPosts is the resolver for the GetAllPosts field.
func (r *queryResolver) GetAllPosts(ctx context.Context) \
([]*model.Post, error) {
 posts := []*model.Post{}
 
 GetPosts := r.Database.Model(&posts).Find(&posts)
 
 if GetPosts.Error != nil {
  fmt.Println(GetPosts.Error)
  return nil, GetPosts.Error
 }
 return posts, nil
}
~~~

Create a variable `post` to save all the fields you want to get from the post model. This example fetches all fields. The database will execute the models that match the posts table using the SQL `Find()` method to find records that match the given conditions.

Send the following query to retrieve all the posts saved in your database:

~~~{.text caption=""}
query GetAllPosts{
  GetAllPosts{
    id
    Title
    Content
    Author
    Hero
    Published_At
    Updated_At
  }
}
~~~

#### Retrieve A Single Post Query

Modify the `GetOnePost` method to execute the query resolver for getting a single post.

~~~{.go caption="graph/schema.resolvers.go"}

// GetOnePost is the resolver for the GetOnePost field.
func (r *queryResolver) GetOnePost(ctx context.Context, id int)\
 (*model.Post, error) {
 post := model.Post{}
 
 if err := r.Database.Find(&post, id).Error; err != nil {
  fmt.Println(err)
  return nil, err
 }
 
 return &post, nil
}
~~~

Just like `GetAllPosts`, use the `Find()` method to find records that match the given conditions. In this case, `Find()` will fulfill the condition of getting one post. Therefore, the id parameter will be executed to fetch the post that matches the passed id.

To get a single post, pass the post id to your query as follows:

~~~{.text caption=""}
query GetOnePost{
  GetOnePost(id:11) {
    id
    Title
    Content
    Author
    Hero
    Published_At
    Updated_At
  }
}
~~~

## Conclusion

Go is a fast, evolving language for backend applications. This guide explored GraphQL implementation with Go.

Also if you're building Go applications, consider automating your build process with [Earthly](https://www.earthly.dev/) for a more consistent build process. Earthly is built it using Go.

The implemented code from this guide is available on this [GitHub repository](https://github.com/Rose-stack/go-mysql-graphql-api).

Enjoy coding with Go!

{% include_html cta/bottom-cta.html %}
