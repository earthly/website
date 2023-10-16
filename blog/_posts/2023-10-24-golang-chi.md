---
title: "GoLang Chi - Your First Application"
categories:
  - Tutorials
toc: true
author: Milap Neupane
editor: Mustapha Ahmad Ayodeji

internal-links:
 - jbuilding first application with golang chi
 - build apps with golang chi
 - golang chi to build apps
 - using golang chi
---

## Building Your First Application with Go and Chi

Go, developed by Google in 2007, was a response to the increasing popularity of multicore processors. Existing programming languages such as Java, Python, and C++ were widely used but had certain limitations.

For instance, Java and C++ were fast but had lengthy compile times. Moreover, C++ lacked automatic garbage collection. Meanwhile, Python was simple but not fast enough for multicore systems.

Go was designed to be a simpler language that promotes developer productivity. Unlike dynamic languages, such as Ruby and Python, which offer multiple ways to solve a problem, Go emphasizes a single, efficient solution. It avoids expressive features such as maps and filters, which can introduce unnecessary complexity and expense.

In this article, you'll learn how to build an application using Go and Chi. [chi](https://github.com/go-chi/chi) is a lightweight and composable router specifically designed for building Go HTTP services. It supports standard HTTP methods, such as GET, POST, HEAD, PUT, PATCH, DELETE, OPTIONS, TRACE, and CONNECT. Additionally, chi's middleware functions are stdlib [net/http middleware handlers](https://pkg.go.dev/github.com/opentracing-contrib/go-stdlib/nethttp) which means it's compatible with any middleware in the community. By incorporating middleware, you gain the ability to define pre-handler and post-handler stages, which simplifies the implementation of various features, such as authentication, logging, and tracing. This approach enables you to manage these functionalities effectively and efficiently within your system.

## Chi Router

An HTTP router facilitates the seamless association of requested URLs with designated handlers to generate relevant responses. Within this context, the chi router aids in breaking down a large system into smaller components. This simplifies the process of constructing substantial REST API services while maintaining a high level of manageability. Characterized by its lightweight nature, idiomatic approach, and composability, the Chi router is an invaluable asset when it comes to routing and web service development.

When handling an HTTP request, various routing parameters can be provided, such as within a request body, URL parameters, or query parameters. Extracting these input parameters is easy with chi as we will see later.

## Set Up the Environment

Now that you know how the chi router works, you can start building the application. Before you begin, make sure you have Go installed on your computer. If you already have it, skip ahead to the next section. If not, follow the [installation instructions](https://go.dev/doc/install) from the Go documentation.

Verify that the installation is successful by running the following command:

~~~{.bash caption=">_"}
go version
~~~

### Set Up the Project Structure and Install chi

After you've installed Go, you need to create a project structure and install the chi router to build the application.

Start by creating a new project directory where you can build the project. Name the project something like `golang-chi-crud-api`:

~~~{.bash caption=">_"}
mkdir golang-chi-crud-api
cd golang-chi-crud-api
~~~

Then it's time to initialize the Go module. The [Go module](https://go.dev/blog/using-go-modules) is Go's dependency management system, which makes it easier to manage dependency versions. A module is a collection of dependent Go packages stored in the root directory in the `go.mod` file.

You can manually create a `go.mod` file in the root directory and add the dependencies, or you can use the `go mod init` command to initialize the module. If you choose the second option, run the `go mod init` command in the root directory by specifying the module path:

~~~{.bash caption=">_"}
go mod init github.com/milap-neupane/golang-chi-crud-api
~~~

Your output will look like this:

~~~{ caption="Output"}
// Output
go: creating new go.mod: module github.com/milap-neupane/golang-chi-crud-api
~~~

The module path must be a path that the module can be downloaded from. Here, `github.com/milap-neupane/golang-chi-crud-api` is the GitHub repository where the module is published. Ensure you replace this with a repository you create (*ie* `github.com/<your-account>/golang-chi-crud-api`).

After running the `go mod init` command, you should see a `go.mod` file in your root directory:

<div class="wide">
![`go.mod` file in root directory]({{site.images}}{{page.slug}}/EuP22qN.png)
</div>

Once the `go.mod` has been initialized, it's time to install the `chi router`. To install it as a dependency, run the following command:

~~~{.bash caption=">_"}
go get -u github.com/go-chi/chi/v5
~~~

Output:

~~~{ caption="Output"}
go: downloading github.com/go-chi/chi v1.5.4
go: downloading github.com/go-chi/chi/v5 v5.0.8
go: added github.com/go-chi/chi/v5 v5.0.8
~~~

This command downloads and adds the `chi router` to the `go.mod` file. A new `go.sum` file is also created, which is an autogenerated lock file for the dependencies.

Now that Chi has been installed, it's time to start building the REST API.

## Building the REST API

In this tutorial, you'll be building a book application that allows create, read, update, and delete (CRUD) operations on the book resource. The book service stores information about books, such as the title, author, genre, published date, and original language.

In JSON format, a book resource data model looks like this:

~~~{.json caption=""}
{
    "id": 1,
    "title": "7 Habits of Highly Effective People",
    "author": "Stephen Covey",
    "published_date": "15/08/1989",
    "original_language": "English",
}
~~~

### Creating a Health Check Endpoint

To build the REST API, start with a simple health check endpoint that returns `200 OK` if the service is up and running. In the function that will process requests, you need to set up a logger, a route path, and an HTTP server that listens to a port that you define.

To build the endpoint, create a `main.go` file in the root directory and add the following code:

~~~{.go caption="main.go"}
package main

import (
    "net/http"

    "github.com/go-chi/chi/v5"
    "github.com/go-chi/chi/v5/middleware"
)

func main() {
    r := chi.NewRouter()
    r.Use(middleware.Logger)
    r.Get("/", func(w http.ResponseWriter, r *http.Request) {
        w.Write([]byte("OK"))
    })
    http.ListenAndServe(":3000", r)
}
~~~

In this code block, you import two packages: `chi` and `chi` middleware.

You also create a new router using the [`chi.NewRouter`](https://pkg.go.dev/github.com/go-chi/chi#NewRouter) class.

You can add a logging middleware to the router with the following:

~~~{.go caption="main.go"}
r.Use(middleware.Logger)
~~~

The logger will log information about incoming requests like the request method, path, and the response status.

After that, you need to set up a route to the root path that listens for GET requests and returns an `OK` back to the client:

~~~{.go caption="main.go"}
    r.Get("/", func(w http.ResponseWriter, r *http.Request) {
        w.Write([]byte("OK"))
    })
~~~

Then, start a server that listens on port 3000:

~~~{.go caption="main.go"}
http.ListenAndServe(":3000", r)
~~~

Run the server by running the `main.go` file:

~~~{.bash caption=">_"}
go run main.go
~~~

Then in a new terminal, run a `curl` command to get the "/" endpoint:

~~~{.bash caption=">_"}
curl localhost:3000/
~~~

Output:

~~~{ caption="Output"}
OK
~~~

This is the log you should see on the server:

~~~{.bash caption=">_"}
"GET http://localhost:3000/ HTTP/1.1" from \
127.0.0.1:57630 - 200 2B in 128.042µs
~~~

The log shows the request method, path, the version of the HTTP used, the source IP address and port, the response status, the size of the response, and the time it takes the server to process the request.

### Creating the Routes for the Book Resource

After you run the server, you need to add the CRUD routes for the book resource using the `r.Route` method. Each of these routes needs to have handler functions to handle the requests.

To help keep the code organized, create a new file called `books.go`. In this file create a `BookHandler` struct that has functions to perform the CRUD operations. The function needs to be defined in this format; `func (b BookHandler) <FunctionName>(w http.ResponseWriter, r *http.Request)  {}`. Notice that the handler takes `http.ResponseWriter` and `http.Request` as parameters. The `http.ResponseWriter` helps you respond to the HTTP request whereas the `http.Request` helps you read the HTTP request.

Add the following function handlers to the BookHandler struct:

~~~{.go caption="book.go"}
// Handlers for the router yet to be implemented
package main

import "net/http"

type BookHandler struct {
}

func (b BookHandler) ListBooks(w http.ResponseWriter, r *http.Request)  {}
func (b BookHandler) GetBooks(w http.ResponseWriter, r *http.Request)   {}
func (b BookHandler) CreateBook(w http.ResponseWriter, r *http.Request) {}
func (b BookHandler) UpdateBook(w http.ResponseWriter, r *http.Request) {}
func (b BookHandler) DeleteBook(w http.ResponseWriter, r *http.Request) {}
~~~

Then, in `main.go`, add the CRUD routes to the book resource by mounting the handler function that is defined above:

~~~{.go caption="main.go"}
package main

import (
    "net/http"

    "github.com/go-chi/chi/v5"
    "github.com/go-chi/chi/v5/middleware"
)

func main() {
    r := chi.NewRouter()
    r.Use(middleware.Logger)
    r.Get("/", func(w http.ResponseWriter, r *http.Request) {
        w.Write([]byte("OK"))
    })
    r.Mount("/books", BookRoutes())

    http.ListenAndServe(":3000", r)
}

func BookRoutes() chi.Router {
    r := chi.NewRouter()
    bookHandler := BookHandler{}
    r.Get("/", bookHandler.ListBooks)
    r.Post("/", bookHandler.CreateBook)
    r.Get("/{id}", bookHandler.GetBooks)
    r.Put("/{id}", bookHandler.UpdateBook)
    r.Delete("/{id}", bookHandler.DeleteBook)
    return r
}
~~~

Here, the `BookRoutes` function creates routes for the book resource. You use Chi's `NewRouter` function to initialize a new router. With this router, you use the `Get`, `Post`, `Put`, and `Delete` functions to attach a route to a specific handler. Here, `Get( "/"` is attached to the `ListBooks` handler that was declared above.

In the following line of code, the route is mounted to the main route in the `main` function. This mount is required to link all the routes to a root path `/books`:

~~~{.go caption="main.go"}
 r.Mount("/books", BookRoutes())
~~~

Run the program to make sure everything is working as expected:

~~~{.bash caption=">_"}
go run *.go
~~~

You can see the logs output because of the logging middleware previously added in the main function after making a curl request.

~~~{.bash caption=">_"}
curl localhost:3000/books/
~~~

This is what your output will look like:

~~~{ caption="Output"}
# 2023/05/08 16:39:16 "GET http://localhost:3000/books/ 
HTTP/1.1" from 127.0.0.1:58592 - 000 0B in 716.042µs
~~~

As you can see, the `curl` command doesn't return anything. You need to implement the handlers so that they create, update, delete, and list the resources.

### Implementing the Handler Functions

Handler functions read and handle the request (if necessary) and perform the CRUD operation on the resource. The handlers need storage to read/write the book resource. That means, before implementing the handler function, you need to first define the structure of a book resource by defining a `Book` struct.

You need a place to store these book resources before you can perform CRUD operations on them. Normally, these resources are stored in a database, but in this tutorial, you can store them in in-memory storage which in this case is a slice of pointer to the Book struct.

In the `models.go` file, create a `Book` struct and a slice of pointer to the `Book` struct:

~~~{.go caption="models.go"}
package main

type Book struct {
    ID               string `json:"id"`
    Title            string `json:"title"`
    Author           string `json:"author"`
    PublishedDate    string `json:"published_date"`
    OriginalLanguage string `json:"original_language"`
}

var books = []*Book{
    {
        ID:               "1",
        Title:            "7 habits of Highly Effective People",
        Author:           "Stephen Covey",
        PublishedDate:    "15/08/1989",
        OriginalLanguage: "English"
    },
}

func listBooks() []*Book {
    return books
}  
~~~

The `listBooks` function returns the books as a function instead of directly using the `books` variable.

Now you can implement the handler functions defined previously.

To return the books as a response in the `ListBooks` handler, you will encode the list of books as json data.

Open the `books.go` file and add the following code:

~~~{.go caption="books.go"}
package main

import (
    "encoding/json"
    "net/http"
)

type BookHandler struct {
}

func (b BookHandler) ListBooks(w http.ResponseWriter, r *http.Request) {
    err := json.NewEncoder(w).Encode(listBooks())
    if err != nil {
        http.Error(w, "Internal error", http.StatusInternalServerError)
        return
    }
}
~~~

In this code, the `json.NewEncoder` method from the `encoding/json` package is used to encode the book's resource and write it to the JSON response data `w`. The response writer `w` is a `http.ResponseWriter` object passed as an argument in the `ListBooks` handler.

If it's successful, you don't need to return anything because the `NewEncoder` already writes the response to the `ResponseWriter`.

Similarly, to implement the Read, Write, Update, and Delete APIs, implement the other CRUD handlers. However, before you do that, you need to store, delete, update, list, and create book resources in `models.go`. These functions perform the CRUD operation in memory on the `books` global variable, which is a slice of pointer to the `Book` struct, that was previously defined as the `listBooks`function:

~~~{.go caption="books.go"}
    …

func listBooks() []*Book {
    return books
}
~~~

This function returns a slice of pointers to Book structs. It simply returns the entire `books` collection.

The `getBook` function:

~~~{.go caption="books.go"}
func getBook(id string) *Book {
    for _, book := range books {
        if book.ID == id {
            return book
        }
    }
    return nil
}
~~~

Given an ID as input, this function searches for a `book` with a matching ID in the `books` collection. If found, it returns a pointer to that book. Otherwise, it returns `nil`.

The `storeBook` function:

~~~{.go caption="books.go"}
func storeBook(book Book) {
    books = append(books, &book)
}
~~~

This function adds a new `book` to the `books` collection. It takes a `Book` struct as input and appends a pointer to that struct to the `books` slice.

The `deleteBook` function:

~~~{.go caption="books.go"}
func deleteBook(id string) *Book {
    for i, book := range books {
        if book.ID == id {
            books = append(books[:i], (books)[i+1:]...)
            return &Book{}
        }
    }
    return nil
}
~~~

This function removes a`book` from the `books` collection based on the provided `id`. It iterates over the collection, finds the `book` with a matching ID, removes it from the `books` slice, and returns a pointer to the deleted book. If no book is found with the given ID, it returns `nil`.

The `updateBook` function:

~~~{.go caption="books.go"}
func updateBook(id string, bookUpdate Book) *Book {
    for i, book := range books {
        if book.ID == id {
            books[i] = &bookUpdate
            return book
        }
    }
    return nil
}
~~~

This function updates a book in the `books` collection. It searches for a book with the provided ID, replaces it with the `bookUpdate` struct, and returns a pointer to the original book. If no book is found with the given ID, it returns nil.

These functions can be used in the `books.go` handlers to handle the different CRUD HTTP route requests:

**GetBooks Handler:**

~~~{.go caption="books.go"}
func GetBooks(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")
    book := getBook(id)
    if book == nil {
        http.Error(w, "Book not found", http.StatusNotFound)
    }
    err := json.NewEncoder(w).Encode(book)
    if err != nil {
        http.Error(w, "Internal error", http.StatusInternalServerError)
        return
    }
}
~~~

The GetBooks handler reads the requested book ID from the URL using the `chi.URLParam` function. This ID is passed to the `getBook` function. If no book is found or there is an error encoding the book, `http.Error` is used to respond with the appropriate error.

**CreateBook Handler:**

~~~{.go caption="books.go"}

func CreateBook(w http.ResponseWriter, r *http.Request) {
    var book Book
    err := json.NewDecoder(r.Body).Decode(&book)
    if err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    storeBook(book)
    err = json.NewEncoder(w).Encode(book)
    if err != nil {
        http.Error(w, "Internal error", http.StatusInternalServerError)
        return
    }
}
~~~

The CreateBook handler reads the request body by using the `json.NewDecoder` function. The request is mapped to the book variable and this book variable is passed to the `storeBook` function to create the book resource. The errors are handled where required.

**UpdateBook Handler:**

~~~{.go caption="books.go"}

func UpdateBook(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")
    var book Book
    err := json.NewDecoder(r.Body).Decode(&book)
    if err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    updatedBook := updateBook(id, book)
    if updatedBook == nil {
        http.Error(w, "Book not found", http.StatusNotFound)
        return
    }
    err = json.NewEncoder(w).Encode(updatedBook)
    if err != nil {
        http.Error(w, "Internal error", http.StatusInternalServerError)
        return
    }
}
~~~

The UpdateBook handler is similar to CreateBook. It reads the request body and decodes it to the book variable. This variable is passed to `updateBook` along with the ID of the book that needs to be updated. The ID is read from the URL using the `chi.URLParam` method.

**DeleteBook Handler:**

~~~{.go caption="books.go"}

func DeleteBook(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")
    book := deleteBook(id)
    if book == nil {
        http.Error(w, "Book not found", http.StatusNotFound)
        return
    }
    w.WriteHeader(http.StatusNoContent)
}
~~~

The DeleteBook handler reads the book ID from the URL using `chi.URLParam`, and passes it to `deleteBook` function. The `w.WriteHeader` function is used to respond with a `StatusNoContent` header and no response body.

Here, the [URLParam](https://pkg.go.dev/github.com/go-chi/chi#URLParam) function provided by Chi reads the URL param. Then the HTTP response writer writes the header and response to the HTTP. Alternatively, you can also use the [optional render subpackage](https://github.com/go-chi/render) to write the response.

### Handling Errors in `chi`

Thankfully, handling errors in chi is simple. You can use the `http` package's `Error()` function to respond to the request with the specified error message and HTTP code. However, the function doesn't end the request, so you need to return after calling the function.

There are useful HTTP status code constants (like `StatusNotFound` translated to 404) defined in the `http` package that you can use:

~~~{.go caption="books.go"}
http.Error(w, "Book not found", http.StatusNotFound)
return
~~~

## Test the Application

As you know, testing your application is imperative when it comes to building reliable applications. This includes both unit and integration tests. Unit tests provide fast, reliable business logic tests, whereas integration tests provide end-to-end coverage.

### Unit Testing

When you're unit testing your application, you want to mock any external dependencies, such as a database or a network call. There are mock packages, such as [gomock](https://github.com/golang/mock), that you can use to mock these calls; however, with Go, you can make the testing simpler using an interface. Moreover, you can have a test implementation and an actual implementation of these external dependencies.

To implement unit testing, you need to refactor and restructure the code a bit. In the `model.go` file, create an interface that the test cases will use to perform the storage operations:

~~~{.go caption="model.go"}
package main

type BookStorage interface {
    List() []*Book
Get(string)*Book
    Update(string, Book) *Book
    Create(Book)
Delete(string)*Book
}
~~~

Then create a struct that implements these functions that are defined by the interface:

~~~{.go caption="model.go"}
type BookStore struct {}
~~~

Implement all the CRUD operations as a method for the struct:

~~~{.go caption="model.go"}
func (b BookStore) Get(id string) *Book {
    for _, book := range books {
        if book.ID == id {
            return book
        }
    }
    return nil
}

func (b BookStore) List() []*Book {
    return books
}

func (b BookStore) Create(book Book) {
    books = append(books, &book)
}

func (b BookStore) Delete(id string) *Book {
    for i, book := range books {
        if book.ID == id {
            books = append[books[:i], (books](i+1:)...)
            return &Book{}
        }
    }
    return nil
}

func (b BookStore) Update(id string, bookUpdate Book) *Book {
    for i, book := range books {
        if book.ID == id {
            books[i] = &bookUpdate
            return book
        }
    }
    return nil
}
~~~

Then in the `books.go` file (where all the endpoint handlers are), use the interface to access the storage:

~~~{.go caption="books.go"}
package main

import (
    "encoding/json"
    "net/http"

    "github.com/go-chi/chi/v5"
)

type BookHandler struct {
    storage BookStorage
}

func (b BookHandler) ListBooks(w http.ResponseWriter, r *http.Request) {
    err := json.NewEncoder(w).Encode(b.storage.List()) //new
    if err != nil {
        http.Error(w, "Internal error", http.StatusInternalServerError)
        return
    }
}

func (b BookHandler) GetBooks(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")
    book := b.storage.Get(id) //new
    if book == nil {
        http.Error(w, "Book not found", http.StatusNotFound)
    }
    err := json.NewEncoder(w).Encode(book)
    if err != nil {
        http.Error(w, "Internal error", http.StatusInternalServerError)
        return
    }
}

func (b BookHandler) CreateBook(w http.ResponseWriter, r *http.Request) {
    var book Book
    err := json.NewDecoder(r.Body).Decode(&book)
    if err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    b.storage.Create(book) //new
    err = json.NewEncoder(w).Encode(book)
    if err != nil {
        http.Error(w, "Internal error", http.StatusInternalServerError)
        return
    }
}

func (b BookHandler) UpdateBook(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")
    var book Book
    err := json.NewDecoder(r.Body).Decode(&book)
    if err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    updatedBook := b.storage.Update(id, book) //new
    if updatedBook == nil {
        http.Error(w, "Book not found", http.StatusNotFound)
    }
    err = json.NewEncoder(w).Encode(updatedBook)
    if err != nil {
        http.Error(w, "Internal error", http.StatusInternalServerError)
        return
    }
}

func (b BookHandler) DeleteBook(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")
    book := b.storage.Delete(id) //new
    if book == nil {
        http.Error(w, "Book not found", http.StatusNotFound)
    }
    w.WriteHeader(http.StatusNoContent)
}
~~~

This gives you the option to change the storage for the handler when you're testing the function, enabling your tests to run faster.

To test the endpoints, create a `books_test.go` file and create a fake implementation of the books storage:

~~~{.go caption="books_test.go"}
package main

import (
    "encoding/json"
    "io/ioutil"
    "net/http"
    "net/http/httptest"
    "testing"
)

var fakeBooks = []*Book{{
    ID:               "1",
    Title:            "7 Habits of Highly Effective People",
    Author:           "Stephen Covey",
    PublishedDate:    "15/08/1989",
    OriginalLanguage: "English",
}}

type fakeStorage struct {
}

func (s fakeStorage) Get(_ string) *Book {
    return fakeBooks[0]
}

func (s fakeStorage) Delete(_ string) *Book {
    return nil
}  

func (s fakeStorage) List() []*Book {
    return fakeBooks
}

func (s fakeStorage) Create(_ Book) {
    return
}

func (s fakeStorage) Update(*string,* Book) *Book {
    return fakeBooks[1]
}

~~~

Then use this fake implementation for the unit test:

~~~{.go caption="books_test.go"}
func TestGetBooksHandler(t *testing.T) {
    req := httptest.NewRequest(http.MethodGet, "/books/1", nil)
    w := httptest.NewRecorder()
    bookHandler := BookHandler{
        storage: fakeStorage{},
    }
    bookHandler.GetBooks(w, req)
    res := w.Result()
    defer res.Body.Close()
    data, err := ioutil.ReadAll(res.Body)
    if err != nil {
        t.Errorf("expected error to be nil got %v", err)
    }
    book := Book{}
    json.Unmarshal(data, &book)
    if book.Title != "7 habits of highly effective people" {
        t.Errorf("expected ABC got %v", string(data))
    }
}
~~~

Go provides an [`httptest` package](https://pkg.go.dev/net/http/httptest) that can be used to perform tests with any HTTP handler functions. And any HTTP handler method (*ie* `GetBooks`) requires `w http.ResponseWriter, r *http.Request` as a parameter. In this code, you build this parameter using the [NewRequest](https://pkg.go.dev/net/http/httptest#NewRequest) and [NewRecorder](https://pkg.go.dev/net/http/httptest#NewRecorder) functions.

You also build a `bookHandler` struct with `fakeStorage` and use this to call the `GetBooks` handler. Using the `bookHandler` with a `fakeStorage` call the `GetBook` handler with the `responseWriter` variable `w` constructed using `httptest.NewRecorder` and request constructed using the `httptest.NewRequest`. In this scenario, you can read the response and assert if the response matches what is expected. This makes it easy to unit test any code without being dependent on the storage.

Run the test using the following command:

~~~{.bash caption=">_"}
go test ./... -v
~~~

~~~{ caption="Output"}
=== RUN   TestGetBooksHandler
--- PASS: TestGetBooksHandler (0.00s)
PASS
ok      github.com/milap-neupane/golang-chi-crud-api    0.133s
~~~

### Integration Testing

Integration testing is a type of test where you combine your components and test them without mocking, using the actual implementation. In addition, instead of testing just the handler function, you can test the response that starts the HTTP request. To do so, start a test server so that you can use the same router for the test and the main server, and refactor the code to move the route setup in a `setupServer` function:

~~~{.go caption="main.go"}
package main

func main() {
    r := setupServer()
    http.ListenAndServe(":3000", r)
}

func setupServer() chi.Router {
    r := chi.NewRouter()
    r.Use(middleware.Logger)
    r.Get("/", func(w http.ResponseWriter, r *http.Request) {
        w.Write([]byte("OK"))
    })
    r.Mount("/books", BookRoutes())
    return r
}
~~~

Then start a server for testing using the same function. Create a new file called `books_integration_test.go` and run the test server.

To test the list endpoint, use the `http` package `Get` function with the book URL. The server URL can be obtained from the test `httpServer`:

~~~{.go caption="books_integration_test.go"}
package main

import (
    "fmt"
    "net/http"
    "net/http/httptest"
    "testing"
)

func runTestServer() *httptest.Server {
    return httptest.NewServer(setupServer())
}

func TestIntegrationGetBooksHandler(t *testing.T) {
    testServer := runTestServer()
    defer testServer.Close()

    resp, err := http.Get(fmt.Sprintf("%s/books", testServer.URL))

    if err != nil {
        t.Fatalf("Expected no error, got %v", err)
    }

    if resp.StatusCode != 200 {
        t.Errorf("expected 200 got: %v", resp.StatusCode)
    }
}
~~~

This example asserts that the response should be `200`. You can also add more assertions, such as the response body; just make sure you're running the `defer testServer.Close()` to ensure that the server shuts down gracefully (making sure any running process is complete) once the test is complete.

The `books` application doesn't use any database and is not dependent on any other external server. This means in the `runTestServer` function, only the HTTP server is running. If you want to add more dependencies to the application, you need to add it to the `runTestServer` function.

Run the test using the following command:

~~~{.bash caption=">_"}
$ go test ./… -v
~~~

Output:

~~~{ caption="Output"}
=== RUN   TestIntegrationGetBooksHandler
2023/06/27 21:36:41 "GET <http://127.0.0.1:50605/books> \
HTTP/1.1" from 127.0.0.1:50606 - 200 144B in 154.375µs
--- PASS: TestIntegrationGetBooksHandler (0.00s)
=== RUN   TestGetBooksHandler
--- PASS: TestGetBooksHandler (0.00s)
PASS
ok      github.com/milap-neupane/golang-chi-crud-api    0.133s
~~~

## Deploy the Application

Now that you've built and tested your application, it's time to deploy the Go app.

To do so, you can build the binary from one system to be deployed in a different system. The following command generates the binary for different operating systems:

~~~{.bash caption=">_"}
GOARCH=amd64 GOOS=darwin go build *.go -o books-application-darwin
GOARCH=amd64 GOOS=linux go build*.go -o books-application-linux
GOARCH=amd64 GOOS=windows go build *.go -o books-application-windows
~~~

This binary can be shipped to any infrastructure like AWS, GCP, Azure, or on-premise servers. Then you can deploy the Go binary in the following ways:

- You can deploy the binary to a serverless function, such as [Amazon Web Service (AWS) Lambda](https://aws.amazon.com/lambda/).
- You can package the binary as a [Docker](https://www.docker.com/) file and use a container orchestration tool like [Kubernetes](https://kubernetes.io/) to deploy it.
- The simplest option is to use the [systemd](https://systemd.io/) service to run the Go application using the Go binary.

You should choose your deployment based on your application type. If the application is trigger-based or processes async tasks, a serverless function is the best option. Or if the application is a small monolith, you can use systemd to run the application. If you're building a large-scale, scalable application or microservices, you should use Docker to containerize it and deploy it using Kubernetes.

## Conclusion

In this article, you learned all about Go and Chi, and you used Chi's routing capabilities to create a well-structured, maintainable application.

Go and Chi both excel in terms of their speed and lightweight nature, making them ideal for developing REST API applications. Go brings the benefits of effortless unit testing and integration testing due to its powerful standard library. Moreover, Go applications are highly portable, enabling easy deployment by creating binaries for multiple operating systems.

The full source code for this tutorial is available in this [GitHub repo](https://github.com/milap-neupane/golang-chi-crud-api).

{% include_html cta/bottom-cta.html %}

## Outside Article Checklist

- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
