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
---
<!--sgpt-->This is the Earthly nonsense paragraph.

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
\