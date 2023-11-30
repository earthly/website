---
title: "How to Use MongoDB with Go"
categories:
  - Tutorials
toc: true
author: Ukeje Goodness

internal-links:
 - MongoDB
 - Go
 - Atlas
 - Cluster
 - Database
excerpt: |
    Learn how to use MongoDB with Go in this tutorial. Discover how to connect to a MongoDB Atlas cluster, perform CRUD operations, and query the database using the Go MongoDB driver.
last_modified_at: 2023-07-19
---
**This article explores the integration of MongoDB in Go applications. Earthly simplifies the build process for Go developers working with MongoDB. [Check it out](https://cloud.earthly.dev/login).**

Recently, NoSQL Databases like [MongoDB](https://earthly.dev/blog/mongodb-docker/), LevelDB, Redis, and others have been preferred for building and deploying applications. [MongoDB](/blog/mongodb-docker) is one of the most popular and adopted NoSQL databases due to its simplicity and ease of use.

The Go MongoDB driver provides functionality for using the MongoDB database in Go. The Go MongoDB driver is the official driver provided, maintained, and fully supported by MongoDB.

This tutorial will teach you how to use MongoDB databases with the Go programming language by connecting to your MongoDB Atlas cluster.

### Prerequisites

Following this tutorial requires that you meet these requirements.

- You have a recent version of Go (preferably 1.16 and above) installed on your computer.
- You have created a MongoDB Atlas Cluster.
- You have experience using MongoDB and the MongoDB Query Language (MQL).

Once you have met these requirements, it will be easy to follow this hands-on tutorial.

## Getting Started With MongoDB and Go

Getting started with MongoDB operations in Go requires that you have a Mongo shell installed or a MongoDB Atlas Cluster to connect to. In this tutorial, you'll be learning to use MongoDB with Go by connecting the Atlas cluster; however, the operations are ninety-nine percent the same once you have connected to a Cluster or shell.

To use MongoDB with Go, you have to install two `mongo-go-driver` packages that help connect to a MongoDB Cluster and run operations in Go.

After setting up your Go workspace, run these commands on your terminal to install the packages.

~~~{.go caption="main.go"}
go get go.mongodb.org/mongo-driver/bson
go get go.mongodb.org/mongo-driver/mongo
~~~

Once you have installed the packages and have created your Go workspace, import these required packages and modules for this tutorial.

~~~{.go caption="main.go"}
import (
 "context"
 "fmt"
 "go.mongodb.org/mongo-driver/bson"
 "go.mongodb.org/mongo-driver/mongo"
 "go.mongodb.org/mongo-driver/mongo/options"
 "go.mongodb.org/mongo-driver/mongo/readpref"
 "log"
 "time"
)
~~~

The `context` and `time` modules were imported to set timeouts for your operations. The `log` module is for logging errors to your console; you'll use the `mongo-driver` packages across this tutorial for MongoDB operation.

## Connecting to a MongoDB Atlas Cluster

After creating a [MongoDB Atlas cluster](https://www.mongodb.com/basics/clusters/mongodb-cluster-setup), you'll need to get a connection URI String to connect to your Cluster from your application.

Click on **connect**, choose "**connect to your application**," choose **Go** as your preferred language, select a Go version, and copy the connection URI string.

<div class="wide">

![Screenshot from 2022-05-13 15-16-12.png]({{site.images}}{{page.slug}}/first.png)\
</div>

<div class="wide">

![textsthththtt.png]({{site.images}}{{page.slug}}/second.png)\

</div>

Once you have the connection URI string, you can now connect to the MongoDB Atlas cluster.

First, you have to declare a context for connection and query timeouts. Making the context, a global variable is reasonable since you'll use it in many parts of your program.

~~~{.go caption="main.go"}
var ctx, cancel = context.WithTimeout(context.Background(), 20*time.Second)
~~~

In the code above, context, and cancel variables were declared and set to timeout in 20 seconds.

Next, you declare a client variable representing the connection to the MongoDB Client, as shown below, after which you can choose to close the connection.

`options.Client()` creates a new client instance, and the `ApplyURI` method takes in the connection URI string you got from your Atlas cluster.

~~~{.go caption="main.go"}
 clientOptions := options.Client().ApplyURI("Your URI String")
 defer cancel()
~~~

If you're connecting to your mongo shell, you'll use a [localhost](http://localhost) connection on your specified port; the default port is set to `27017`.

~~~{.go caption="main.go"}
client, err := mongo.Connect(context.TODO(), options.Client().ApplyURI("mongodb://localhost:27017"))
 if err != nil {
    panic(err)
}
~~~

Then, you can go ahead and connect your client instance using the Connect method, and handling any errors that might occur.

~~~{.go caption="main.go"}
client, err = mongoClient.Connect(ctx)
 if err != nil {
  log.Fatal("There was a connection error", err)
 }
~~~

On a successful connection, there will be no output; however, you may experience authentication and other errors, so you have to handle an error.

## Validating a Mongodb Database Connection with Go

To validate your connection, you can ping the Atlas Cluster and print out the list of names in the databases in the Cluster.

You can ping the database as shown below.

~~~{.go caption="main.go"}
err = mongoClient.Ping(context.TODO(), readpref.Primary())
 if err != nil {
  panic(err)
 }

 defer mongoClient.Disconnect(ctx)
~~~

The `Ping` method on the `mongoClient` variable takes in a context `context.TODO()` and a read preference `readpref.Primary()` after which the error is handled and logged on to the console if any. If there are no errors, you've made a successful connection.

You can print the list of database names using the `ListDatabaseNames` method on your client variable.

~~~{.go caption="main.go"}
 databases, err := mongoClient.ListDatabaseNames(ctx, bson.M{})
 if err != nil {
  log.Fatal(err)
 }
 fmt.Println(databases)
~~~

The `ListDatabaseNames` method takes in a context and `bson.M`; it outputs the database names as shown below.

~~~{.ini caption="Output"}
>>> [sample_airbnb sample_analytics sample_geospatial sample_guides sample_mflix sample_restaurants sample_supplies sample_training sample_weatherdata admin local]
~~~

You have successfully made and validated a connection to your Atlas cluster;

### A Few Things to Note as You Explore Using Mongodb with Go

MongoDB stores information in BSON(Binary JSON), and while using the Go driver package, you'll be passing in arguments from the Mongo driver `bson` subpackage.

Here's an explanation of the arguments we will be using in this tutorial.

- The **`bson.M`** argument is used to insert documents or specify criteria. It is of the type `map[string]interface{}`. When you use `**bson.M`,** the return order of results isn't important.

- The `**bson.D`**argument performs the same functions as the `bson.M` argument, except that when you use `**bson.D`,** the order in which the results are returned is important.

- The **`bson.A`** argument ****is used for inserting arrays into a collection as part of the fields in an unordered fashion.

<div class="wide">

![Screenshot 2022-06-02 at 15.04.14.png]({{site.images}}{{page.slug}}/third.png)\
</div>

You can learn more about the [MongoDB `bson` package here](https://pkg.go.dev/go.mongodb.org/mongo-driver/bson@v1.9.1).

## Using MongoDB Databases and Collections with Go

Once you're connected to your Atlas cluster, you can access and use the available databases and collections.

Remember that MongoDB is structured such that you'll have to access a database to access a collection, and the same applies when you're writing your programs.

You can access a database using the `Database` method of your client instance as thus.

~~~{.go caption="main.go"}
aDatabase := client.Database("Music")
~~~

A new database will be created for your operations if the database doesn't exist.

In the same vein, you can use the `Collection` method to specify the collection you want to access on the database instance. A collection will also be created if it doesn't exist.

~~~{.go caption="main.go"}
theCollection := aDatabase.Collection("New Music")
~~~

Once you've specified the database and collection, you can perform various operations on MongoDB documents with Go.

**Note:** The collection above; `theCollection` will be used throughout this article for operations.

## Creating/Inserting Documents Into  A Mongodb Cluster With Go

Inserting documents with Go is easy; you can insert one or many documents and get the `objectID` of the inserted document.

You can insert one document into a collection using the `InsertOne` method on your collection instance. The `InsertOne` method takes in a context, and a MongoDB bson map `bson.D` where the data is specified.

~~~{.go caption="main.go"}
insertResult, err := theCollection.InsertOne(ctx, bson.D{
 {"Name", " John Doe"},
 {"Song", "Don't Dance"},
 {"tags", bson.A{"New", "CodeJams", "Pop Culture"}},
})

if err != nil {
 log.Println("There was an errr in trying to migrate the data into the database")
}

fmt.Println(insertResult.InsertedID)
~~~

In the example above, a document containing the fields `Name`, `Song`, and an array of `tags` was inserted into the database. A migration error was handled, and the inserted ID was printed out.

Here's the result of the insertion on the command line and MongoDB's Atlas UI
<div class="wide">

![Screenshot 2022-05-30 at 16.36.31.png]({{site.images}}{{page.slug}}/fourtha.png)\
</div>

<div class="wide">

![Screenshot 2022-05-30 at 16.36.39.png]({{site.images}}{{page.slug}}/fourthb.png)\
</div>

Similarly, you can insert multiple documents at once into a cluster using the `InsertMany` method.

The `InsertMany` method takes in a context and an interface of BSON documents `bson.D`.

Here's how to insert many documents into a collection.

~~~{.go caption="main.go"}
insertResult, err := theCollection.InsertMany(ctx, []interface{}{
  bson.D{
   {"Name", " Deen Bread"},
   {"Song", "Run Away"},
   {"tags", bson.A{"New", "AfroCompile", "Woke Culture"}},
  },
  bson.D{
   {"Name", " May Slindesloff"},
   {"Song", "Come over"},
   {"tags", bson.A{"New", "Rap Interpreter", "Work Culture"}},
  },
 })

 if err != nil {
  log.Println("There was an err in trying to migrate the data into the database")

 }
 fmt.Println(insertResult.InsertedIDs)
~~~

Two documents identical to the documents in the `InsertOne` example were inserted, the error was handled, and the inserted IDs were printed.

Here's the result of the insertion
<div class="wide">

![Screenshot 2022-05-30 at 21.41.56.png]({{site.images}}{{page.slug}}/fifth.png)\
</div>

## Querying a Mongodb Database Using Go

You'll be querying your database collection for data most of the time. The Go MongoDB driver provides as many functionalities as MongoDB Query Language(MQL) for querying databases.

Here's an overview of some query operations.

## Retrieving All Documents in a Database

You can retrieve all the documents in a collection using the `Find` method of the collection instance. Since you want all values, the `bson.M` argument will be empty.

~~~{.go caption="main.go"}
 cursor, err := theCollection.Find(ctx, bson.M{})
 if err != nil {
  log.Println(err)

 }
 var music []bson.M
 if err = cursor.All(ctx, &music); err != nil {
  log.Println(err)
 }
 fmt.Print(music)
~~~

In the example above, after specifying that all documents in the collection should be returned, a slice of `bson.M[]`  named `music` was declared. The query results were decoded into the `music` slice.

Here's the result of printing out the `music` slice.

<div class="wide">

![Screenshot 2022-06-01 at 20.45.31.png]({{site.images}}{{page.slug}}/sixth.png)\
</div>

You can go on to manipulate the slice of maps and format it; that's why decoding the results into a native Go data structure was important.

## Querying the Database by Filtering

You can also choose to be specific and query for documents that meet certain criteria. You can do this by using the `Find` method on the collection instance. In this case, the `bson.M` argument would take in a map(key-value pair) of strings.

~~~{.go caption="main.go"}
var music []bson.M

filter, err := theCollection.Find(ctx, bson.M{"Song" :"Don't Dance"})
if err != nil {
 log.Println(err)
} 
if err = filter.All(ctx, &music); err != nil {
  log.Println(err)
}
fmt.Println(music)
~~~

The filter criteria above for searches for `Songs` with the title "`Don't Dance`" inserted in the example of the ***inserting document*** above.

The query's result was decoded into the declared music struct, and possible errors were handled.

<div class="wide">

![Screenshot 2022-06-01 at 22.09.24.png]({{site.images}}{{page.slug}}/seventh.png)\
</div>

If you're interested in only one result, you can use the `FindOne` method instead to retrieve the first result of your collections query.

### Updating Mongodb Documents With Go

There are numerous, similar implement methods for updating documents in the Go driver. Some of these include `UpdateByID()`, `UpdateOne()`, `UpdateMany()`, `ReplaceOne()`, `FindOneAndUpdate()` and `FindOneAndReplace()` which all operate as their names imply.

Here's how to update many documents at once by setting criteria for the documents that should be updated.

~~~{.go caption="main.go"}
results, err := theCollection.UpdateOne(ctx, bson.M{ // this is the
  "Name": "Deen Bread",
 }, bson.D{
  {"$set", bson.D{
   {"Song", "Why are you running?"}}},
 })

 if err != nil {
  log.Print(err)
 }

fmt.Println(results.ModifiedCount)
~~~

In the code above, a context, a `bson.M`, and `bson.D` parameters were passed into the `UpdateMany` method of the collection.

The `bson.M` should take in the criteria for the update; in this case, the updates will occur on documents with the name field equal to "`Deen Bread`".

Finally, the `bson.D` argument takes in two parameters, an MQL update operation, e.g. ($set, $inc e.t.c), and another bson containing a different value and the key it should be inserted into.

Possible errors were handled, and a modified count was printed using the `ModifiedCount` method.
<div class="wide">

![Screenshot 2022-06-02 at 17.46.06.png]({{site.images}}{{page.slug}}/eight.png)\
</div>

Here's the result of the update from the Atlas cluster; notice that the value of the Song field was changed from "`Don't Run`" to "`Why are you running`."

## Replacing Mongodb Documents With Go

You can replace a document using the `ReplaceOne` method of the collection. The `ReplaceOne` method takes in a context, a specification for the document to be replaced, and the values the document should be replaced with.

{% raw %}

```go
result, err := theCollection.ReplaceOne(ctx,
  bson.D{{"Name", "May Slindesloff"}},
  bson.D{{"Name", "May Slindesloff"}, {"rating", 9}, {"tags", bson.A{"code musically", "compiler beats"}}},
 )
 fmt.Println(result.ModifiedCount)
```

{% endraw %}

In the example above, the document with the `Name` equal to "`May Slindesloff`" was modified such that it doesn't have a song field, the `tags` array values were modified, and a new field `rating` was introduced.

Here's the result of the replacement from the Atlas Cluster.

<div class="wide">

![Screenshot 2022-06-02 at 18.11.07.png]({{site.images}}{{page.slug}}/eleventh.png)\
</div>

You have seen how to create, update, and insert documents. Let's see how you can delete documents in [MongoDB](/blog/mongodb-docker) Collections using the Go programming language.

## Deleting Mongodb Documents With Go

You can delete a document off a collection using the `DeleteMany` and `DeleteOne` methods.

Here's how to delete one document in a collection.

The `DeleteOne` method takes in a contest and a `bson.M`, which contains specifications of the document to be deleted as arguments.

~~~{.go caption="main.go"}
 result, err := theCollection.DeleteOne(ctx, bson.M{"Song": "Don't Dance"})
 if err != nil {
  log.Fatal(err)
 }
 fmt.Println(result.DeletedCount)
~~~

In the code above, a collection with the field of "Song" of value "Don't Dance" was deleted, possible errors were handled, and a deleted count was printed.

Recall that there were three documents in the Cluster; the delete operation has reduced it to two.
<div class="wide">

![Screenshot 2022-06-02 at 15.30.08.png]({{site.images}}{{page.slug}}/tenth.png)\
</div>

Deleting all documents in a collection is the same as deleting the collection itself; let's overview how you can delete a collection.

## Deleting a MongoDB Collection with Go

There are many cases where you might want to delete a collection; it's easy to do that with the driver.

Use the `Drop` method on the collection you want to drop, pass in a context and handle possible errors.

~~~{.go caption="main.go"}
if err = theCollection.Drop(ctx); err != nil {
    log.Println(err)
}
~~~

The collection must exist for you to delete it or get an error as handled above.

## Conclusion

This tutorial has equipped you with the basics of commonly used MongoDB operations using the Go driver.

Here are some additional resources to help you delve deeper:

- [Using MongoDB with Docker](https://earthly.dev/blog/mongodb-docker/).
- [MongoDB & Go Quick Reference](https://www.mongodb.com/docs/drivers/go/current/quick-reference/#std-label-go-quick-reference).
- [The Go.dev MongoDB Go Driver Documentation](https://pkg.go.dev/go.mongodb.org/mongo-driver).

Using MongoDB with Go will prove beneficial across various fields including backend development, data science, machine learning, and DevOps. Remember, your MQL skills are crucial in conducting more complex operations with Go. So, keep exploring and happy coding!

And as you continue your learning journey, consider taking your efficiency up a notch with [Earthly](https://www.earthly.dev/), your new tool for optimized builds.

{% include_html cta/bottom-cta.html %}
