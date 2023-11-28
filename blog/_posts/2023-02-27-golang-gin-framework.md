---
title: "Go with the Gin Framework"
categories:
  - Tutorials
toc: true
author: Ukeje Goodness

internal-links:
 - APIs
 - Go
 - Gin
 - Framework
 - Web Application
excerpt: |
    Learn how to build web applications in Go using the Gin framework. This tutorial will guide you through developing a CRUD API and using features like routing, JSON parsing, and database operations with GORM.
last_modified_at: 2023-07-19
---
**In this article, we provide a detailed tutorial on using the Gin framework with Go. If you want to speed up your build process, learn how Earthly can enhance your CI pipeline by integrating with Gin. [Discover more](/).**

Go is increasing in popularity for many reasons, from speed to ease of use and so much more. The Go standard library has most of the functionalities you'll need to build web applications in the `net/http` package. There are many web-based [packages](/blog/setup-typescript-monorepo) in the Go ecosystem to build fast web applications.

The Gin framework is one of the popular web packages in the Go ecosystem for building web applications. Gin provides most of the functionalities you'll need in a web framework featuring a [martini-like](https://github.com/go-martini/martini) API with high performance and easy error management.

<div class="wide">

![Untitled]({{site.images}}{{page.slug}}/Untitled.png)\
</div>

Gin is extendable, and the package provides built-in rendering support for HTML, [JSON](/blog/convert-to-from-json), and XML rendering with documentation support, among many other features.

This tutorial will walk you through developing web applications in Go with the Gin framework. You'll learn how to use Gin by building a CRUD API. You'll use the Gin framework for routing, JSON parsing, request-response-related operations, and the GORM package for the database (SQLite) auto migrations and operations.

Note: You can find the complete code for this tutorial on this [GitHub Gist](https://gist.github.com/Goodnessuc/e4fdc78b04965e991efc440f50705ece).

## Prerequisites

You'll need to meet a few prerequisites to understand and follow this hands-on tutorial:

1. You have experience working with Go and Go installed on your machine.
2. Experience working with the GORM package and SQL databases in Go is a plus.

## Getting Started With Gin and GORM

<div style="height= 50%">
![Starting]({{site.images}}{{page.slug}}/start.png)\
</div>

Once you've set up your Go workspace, install the `gin` package in your working directory using this command.

~~~{.bash caption=">_"}
go get github.com/gin-gonic/gin
~~~

You'll also need to install the `gorm` package and the `gorm` [sqlite](/blog/golang-sqlite) driver for connecting to the SQLite database.

Run these commands in your working directory to install the packages:

~~~{.bash caption=">_"}
go get gorm.io/gorm
go get gorm.io/driver/sqlite
~~~

These are the imports you'll need for this tutorial:

~~~{.go caption="gin.go"}
import (
    "github.com/gin-gonic/gin"
    "gorm.io/driver/sqlite"
    "gorm.io/gorm"
    "log"
    "net/http"
)
~~~

You'll use the `log` package for logging-related operations and the `http` package for starting a server and other operations.

## Setting Up GORM and SQLite for Persistence

GORM uses structs for the database model. You can declare the struct with constraint tags and set up auto migrations for the struct.

Here's an example `company` struct with `gorm` and `json` tags:

~~~{.go caption="gin.go"}
type Companies struct {
    Name    string `gorm:"primary_key" json:"name"`
    Created int `json:"created"`
    Product string `json:"product"`
}
~~~

The `Name` field has the primary key constraint, and the constraints would reflect on table creation.

On database migrations, GORM creates a table that matches the struct model. Here's an example of a database table matching the struct model after a series of POST requests.

<div class="wide">
![Untitled]({{site.images}}{{page.slug}}/Untitled (1).png)\
</div>

You can declare a function to manage database connections and auto migrations.

~~~{.go caption="gin.go"}
func DBConnection() (*gorm.DB, error) {
    db, err := gorm.Open(sqlite.Open("test.db"), &gorm.Config{})
    if err != nil {
        return db, err
    }

    err = db.AutoMigrate(&Companies{})
    if err != nil {
        return nil, err
    }

    return db, nil
}
~~~

The `DBConnection` function returns a GORM database instance `*gorm.DB` and an error. The `Open` method returns a database connection after creating a connection with the `Open` method of the `sqlite` driver package.

The `AutoMigrate` method helps with auto-migrating the `Companies` struct.

## Setting Up Handler Functions With Gin

Handler functions will house your business logic based on the input and response of your API. In this tutorial, you'll learn how to implement the CRUD handler functions for your API.

A typical handler `gin` handler function takes in the `gin` context struct.

~~~{.go caption="gin.go"}
func GetCompany(ctx *gin.Context) {

}
~~~

Most of the functionalities you'll need in your handler function are methods of the `Context` struct.

### Mounting Handlers and Setting Up a Server

You'll need to mount the handlers, define the routes and their respective handler functions, then start the server before interacting with your API endpoints.

You can use the `Default` method to create a `gin` router instance. The `Default` method returns a router instance.

~~~{.go caption="gin.go"}
func main() {
    router := Gin.Default()
    log.Fatal(router.Run(":8080"))
}
~~~

After creating the router instance, you can use the `GET`, `POST`, `PUT`, and `DELETE` methods to define routes and their respective handler functions.

The `Run` method of your router instance starts a server to run on the specified port. You can now define your handler functions and mount them in the main function.

### The `POST` Request Handler

The `POST` request handler function will accept JSON input from the client for GORM to migrate to the decoded JSON struct database:

~~~{.go caption="gin.go"}
func PostCompany(ctx *gin.Context) {
    var company Companies
    if err := ctx.ShouldBindJSON(&company); err != nil {
        ctx.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }
    newCompany := Companies{
        Name:    company.Name,
        Created: company.Created,
        Product: company.Product,
    }
    db, err := DBConnection()
    if err != nil {
        log.Println(err)
    }
    if err := db.Create(&newCompany).Error; err != nil {
        ctx.JSON(http.StatusInternalServerError, \
        gin.H{"error": "Database Migration Error"})
    }
    ctx.JSON(http.StatusOK, company)

}
~~~

The `PostCompany` handler function receives POST requests from the server, parses the JSON into the `newCompany` struct, and the `Create` method of your database instance creates a new row of the struct inputs in the database.

If there's an error decoding the JSON request body or migrating the data, the handler function returns the JSON from the error handling `if` statement.

You can mount the `PostCompany` handler function and assign a route to the handler function with the `POST` method of your writer instance that takes in the route string and the handler function.

~~~{.go caption="gin.go"}
func main() {
    router := Gin.Default()
    router.POST("/company", PostCompany)
    log.Fatal(router.Run(":8080"))
}
~~~

Here's a CURL request that tests the `PostCompany` handler function:

~~~{.bash caption=">_"}
curl -X POST -H "Content-Type: application/json" \
-d '{"name": "TestCompany", "created": "2021-01-01", \
"product": "TestProduct"}' "http://localhost:8080/api/v1/company"
~~~

<div class="wide">

![Untitled]({{site.images}}{{page.slug}}/Untitled (2).png)\
</div>

The CURL request sends a POST request to the `/company` endpoint with a JSON payload containing fields that match the `Companies` struct.

### The `GET` Request Handler

The `GET` request will accept a parameter (the company name) from the client and return a JSON response to the client from the `Companies` database.

~~~{.go caption="gin.go"}
func GetCompany(ctx *gin.Context) {
    var company Companies
    name := ctx.Param("company")
    db, err := DBConnection()
    if err != nil {
        log.Println(err)
    }
    if err := db.Where("name= ?", name).First(&company).Error; err != nil {
        ctx.JSON(http.StatusNotFound, gin.H{"Failed": "Company not found"})
        return
    }
    ctx.JSON(http.StatusOK, company)

}
~~~

The `GetCompany` handler function retrieves the `company` name from the request using the `Param` method of the context instance, creates a database connection, and retrieves the row where the `Name` field equals the name from the request.

You can mount the `GetCompany` handler function with the `GET` method of your router instance. The `GET` method, just like the `POST` method, takes in the route and the handler function as parameters

~~~{.go caption="gin.go"}
func main() {
    router := Gin.Default()
    router.GET("api/v1/:company", GetCompany)
    router.POST("/company", PostCompany)

    log.Fatal(router.Run(":8080"))
}

~~~

Here's the CURL request for the `GetCompany` handler function. The `CURL` request sends a request to the `/api/v1/:company` route with the data attached to the URL:

~~~{.bash caption=">_"}
curl -X GET "http://localhost:8080/api/v1/TestCompany"

{"name": "TestCompany", "created": "2021-01-01", "product": "TestProduct"}

~~~

<div class="wide">
![Untitled]({{site.images}}{{page.slug}}/Untitled (3).png)\
</div>

### The `PUT` Request Handler

`PUT` request handlers are responsible for the update operations. The `PUT` request will receive a parameter and a [JSON](/blog/convert-to-from-json) request body from the client and search the database before updating the database entry.

~~~{.go caption="gin.go"}
func UpdateCompany(ctx *gin.Context) {

    var company Companies
    name := ctx.Param("company")
    db, err := DBConnection()
    if err != nil {
        log.Println(err)
    }

    if err := db.Where("company = ?", name).First(&company).Error; \
    err != nil {
        ctx.JSON(http.StatusNotFound, \
        gin.H{"error": "Company doesn't exist "})
        return
    }

    if err := ctx.ShouldBindJSON(&company); \
    err != nil {
        ctx.JSON(http.StatusBadRequest, \
        gin.H{"error": err.Error()})
        return
    }

    if err := db.Model(&company).Updates(Companies{
        Name:    company.Name,
        Created: company.Created,
        Product: company.Product,
    }).Error; err != nil {
        ctx.JSON(http.StatusInternalServerError, \
        gin.H{"error": err.Error()})
        return
    }
    ctx.JSON(http.StatusOK, company)

}
~~~

The `UpdateCompany` handler function retrieves the company name from the request with the `Param` method and updates the row with the JSON from the request with the `Updates` method of your database instance.

Similar to the POST and GET handler functions, you can mount the `UpdateCompany` handler function with the `PUT` method of the router instance.

~~~{.go caption="gin.go"}
func main() {
    router := Gin.Default()
    router.GET("api/v1/:company", GetCompany)
    router.POST("/company", PostCompany)
    router.PUT("api/v1/:company", UpdateCompany)

    log.Fatal(router.Run(":8080"))
}
~~~

Here's the CURL request that tests the `UpdateCompany` handler function. Insert a company name in the specified field to run the CURL request effectively:

~~~{.bash caption=">_"}
curl -X PUT -H "Content-Type: application/json" \
-d '{"name": "TestCompany", "created": "2022-01-01", \
"product": "UpdatedProduct"}' "http://localhost:8080/api/v1/<company_name>"

{"name": "TestCompany", "created": "2022-01-01", \
"product": "UpdatedProduct "}

~~~

The CURL request sends a PUT request to the `api/v1/:company` endpoint with a [JSON](/blog/convert-to-from-json) payload as the replacement for the update operation.

<div class="wide">

![Untitled]({{site.images}}{{page.slug}}/Untitled (4).png)\
</div>

### The `DELETE` Request Handler

Your `DELETE` request handler will receive a parameter from the client's request and search through the database for the valid entry to delete the row with the access.

~~~{.go caption="gin.go"}
func DeleteCompany(ctx *gin.Context) {

    var company Companies
    name := ctx.Param("company")
    db, err := DBConnection()
    if err != nil {
        log.Println(err)
    }

    if err := db.Where("company = ?", name).First(&company).Error; \
    err != nil {
        ctx.JSON(http.StatusNotFound, gin.H{"error": "company not found!"})
        return
    }

    if err := db.Delete(&company).Error; err != nil {
        ctx.JSON(http.StatusInternalServerError, \
        gin.H{"error": err.Error()})
        return
    }
    ctx.JSON(http.StatusOK, gin.H{"message": "Company Deleted"})

}
~~~

The `DeleteCompany` handler function retrieves the company name from the request, creates a database connection, searches for the company with the `Where` method of the database instance, and deletes the row from the database.
After a valid request, the `DeleteCompany` handler function returns a message and the 200 HTTP status code to the client.

You can mount the `DeleteCompany` handler function with the `DELETE` method.

~~~{.go caption="gin.go"}
func main() {
    router := Gin.Default()
    router.GET("api/v1/:company", GetCompany)
    router.POST("/company", PostCompany)
    router.PUT("api/v1/:company", UpdateCompany)
    router.DELETE("api/v1/:company", DeleteCompany)

    log.Fatal(router.Run(":8080"))
}
~~~

Here's the CURL request for the `DeleteCompany` handler function. Insert a company name in the specified field to run the CURL request effectively:

~~~{.bash caption=">_"}
    curl -X DELETE "http://localhost:8080/api/v1/<company_name>"

     {"message": "Company Deleted"% }
~~~

The CURL request sends a DELETE request to the `api/v1/:company` endpoint to delete the matching row from the database.

## Conclusion

This tutorial guided you through building web applications using the Gin Framework, including creating an API with CRUD functionalities. To further your skills, explore the [Gin documentation](https://gin-gonic.com/docs/). It will help you implement more complex functionalities for your apps.

And as you continue to develop your web applications, consider taking your build process up a notch with [Earthly](https://www.earthly.dev/). It's an efficient tool for creating reproducible builds, which can be a great addition to your development toolkit.

Enjoyed using Gin for web development? You'll likely appreciate what Earthly has to offer. Check it out!

{% include_html cta/bottom-cta.html %}