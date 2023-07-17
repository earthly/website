---
title: "Five Common Mistakes To Avoid When Learning Golang"
categories:
  - Tutorials
toc: true
author: Ubaydah Abdulwasiu
editor: Mustapha Ahmad Ayodeji

internal-links:
 - Golang
 - Common Mistakes
 - Improvement
 - Learning
excerpt: |
    In this article, we explore five common mistakes to avoid when learning Golang. From understanding pointers and interfaces to utilizing concurrency and third-party libraries effectively, we cover key concepts and best practices to help you become a more proficient Go developer. Don't miss out on these valuable insights to enhance your Golang skills!
---
**We're [Earthly](https://earthly.dev/). We simplify and speed up software building with containerization, making it a great tool for Golang devs. [Check it out](/).**

Golang (or Go) is an open-source programming language that was developed by Google engineers. It was designed to build efficient, reliable, and robust applications, and it is a [statically compiled](https://stackoverflow.com/questions/12600296/dynamically-compiled-language-vs-statically-compiled-language) language used for building modern and scalable applications.
Go is known for it's concurrency support, which makes it easy to write programs that can perform multiple tasks simultaneously. It has a [garbage-collected runtime](https://tip.golang.org/doc/gc-guide) and a rich standard library, making it easy to develop applications without relying on external dependencies.

It has gained popularity among developers over the years for a variety of reasons. One of the main reasons is its simplicity. Go has a clean, easy-to-learn syntax, which makes it easy for new developers to pick up and start using. Additionally, it places a strong emphasis on readability, which makes it easier for teams to collaborate and maintain code.
Go is also known for its performance. It is a compiled language, which means that it is compiled into [machine code](/blog/compiling-containers-dockerfiles-llvm-and-buildkit) that can be directly executed by the computer's processor. This makes Go programs fast and efficient, especially when compared to interpreted languages like Python or Ruby.
However, when learning [Golang](/blog/top-3-resources-to-learn-golang-in-2021), there are common mistakes made by beginners or experienced developers in understanding basic concepts.

In this article, we will go over these five common mistakes and how to ensure we avoid them.

## Prerequisites

- Basic Understanding of Programming Concepts
- Familiarity with Golang
- Understanding of basic Golang concepts

All relevant codes utilized in this tutorial can be found in this [repository](https://github.com/Ubaydah/golang-mistakes-tutorial).

## Mistake 1: Not Understanding Pointers And References

In Go, a pointer is a variable that stores the memory address of another variable. We can think of a pointer as a "reference" to another value stored in memory. Pointers are useful for passing the memory address of a variable to a function, allowing the function to modify the original value stored at that address.

Here is an example of how we can use a pointer in Go:

~~~{.go caption="main.go"}

package main

import "fmt"

func main() {
    // Let's declare a variable x and assign it a value of 10
    x := 10

    // Let's declare a pointer p that points to x
    p := &x

    // Let's print the value of x using the pointer
    fmt.Println(*p)  // Output: 10

    // Let's modify the value of x using the pointer
    *p = 20

    // Let's print the modified value of x
    fmt.Println(x)  // Output: 20
}

~~~

This outputs:

~~~{ caption="Output"}

10
20

~~~

In the code block above, `p` is a pointer to the variable `x`. We use the `&` operator to get the memory address of `x`, and we use the `*` operator to dereference the pointer and access the value stored at that address.
We can also use the [`new`](https://go.dev/doc/effective_go#allocation_new) function to allocate memory for a new variable and return a pointer to it:

~~~{.go caption="main.go"}

p := new(int)  
// We allocate memory for an int and return a pointer to it
*p = 10
// We then assigned the value 10 to the memory location pointed to by p
fmt.Println(*p) 
// Output: 10

~~~

For a [struct field](https://golangbot.com/structs/), we use the `&` operator to get the memory address
Here's an example:

~~~{.go caption="main.go"}

// We declare a new struct named book
type Book struct {
    Name string
    Author string 
    Price  int
}

func main() {
    b := Book{"Half of a sun", "John doe", 8000}
    p := &b.Price
    // Let's get the memory address of the Price field of the Book struct
    *p = 7000
    // Let's modify the Price field using the pointer
    fmt.Println(b.Price)  // Output: 7000
}

~~~

In the code block above, we declare a struct named `Book` with fields of `Name`, `Author`, and `Price`. Next, We create a variable `b` in our `main` function to assign values to the struct. The `&` operator gets the memory address of the `Price` field of the struct `b`. We then use the `*` operator to modify the value of the price.
Not understanding how pointers and references work in Go can lead to certain errors and bugs in our codes. Here are some scenarios:

### Not Using the `*` and `&` Operators Correctly

If we use the `*` and `&` operators incorrectly, we will get errors from the compiler, and our codes will not behave as expected.
Here's an example:

~~~{.go caption="main.go"}

x := 10
p := *x
// Incorrect use of the * operator
fmt.Println(p)
// invalid operation: cannot indirect x (variable of type int)

~~~

This output:

~~~{ caption="Output"}

./main.go:7:8: invalid operation: cannot indirect x (variable of type int)
~~~

In the example above, we tried to use the `*` operator to get the memory address of the variable `x` instead of the `&` operator. This will cause a compiler error because `x` is not a pointer, and our codes won't run.

### Deferencing a `Nil` Pointer

A `nil` pointer is a pointer that doesn't point to any memory address. It is a pointer that is declared and not initialized to any value, hence it is set to `nil` by default.
In Go, dereferencing a `nil` pointer returns a runtime error.
Here's an example

~~~{.go caption="main.go"}

package main
import "fmt"

func main() {
    var q *int
    // Declare a pointer q
    fmt.Println(*q)
    // Dereference q, which causes an error: panic: runtime error: \
    invalid memory address or nil pointer dereference
}

~~~

This outputs:

~~~{.runtime caption="Output"}

[signal SIGSEGV: segmentation violation code=0x2 addr=0x0 pc=0x100c50024]
goroutine 1 [running]:
main.main()
    /Users/Me/Desktop/DSA/backtracking/main.go:7 +0x24
exit status 
~~~

In the code block above, the pointer `p` is not initialized to point to any memory address. When we try to dereference `p` using the `*` operator, it causes a runtime error because we are trying to access the value stored at a `nil` memory address.
To avoid this error, we should always ensure that a pointer is initialized to point to a valid memory address before dereferencing it. We can do this by using the `new` function to allocate memory for a new variable and assigning the resulting pointer to the pointer variable:

~~~{.go caption="main.go"}

p := new(int)
// Allocate memory for an int and return a pointer to it
*p = 10
// Assign the value 10 to the memory location pointed to by p
fmt.Println(*p) 
// Output: 10
~~~

This outputs:

~~~{ caption="Output"}

10
~~~

### Dereferencing A Pointer To A Different Type

If we dereference a pointer to a different type than the type it was originally declared as, we will get a runtime error.
Here's an example:

~~~{.go caption="main.go"}

package main

import "fmt"

func main() {
    p := new(int)
    *p = 10

    var q *float64 = p
    // cannot use p (variable of type *int) as type \
    *float64 in variable declaration
    fmt.Println(*q)  
}
~~~

In the code block above, we declared a new pointer `p` as an integer. Then we assigned a new type `float64` to it. This will result in a compiler "incompatible assignment" error in our codes.

It outputs:

~~~{ caption="Output"}

./main.go:9:19: cannot use p (variable of type *int) \
as type *float64 in variable declaration
~~~

In conclusion, avoiding pointer and reference errors is very important when programming in [Golang](/blog/top-3-resources-to-learn-golang-in-2021). We should ensure the right operator is used when deferencing pointers and avoid calling nil pointers. Mastering these concepts might be hard at first, but with enough practice, we get better.

## Mistake 2: Not Utilizing Interfaces Effectively

Interfaces in Golang are a way to define a set of methods that a struct or other type must implement to conform to that interface.
For example, let's say we have a struct called `Animal` and we want to [make](/blog/makefiles-on-windows) sure that any struct that is considered an `Animal` must have a method called `Speak()` that returns a string. We can create an interface called `Speakable` that defines this method:

~~~{.go caption="main.go"}

type Speakable interface {
    Speak() string
}

~~~

We can then define our struct `Animal` and make sure it implements the `Speakable` interface by defining the `Speak()` method:

~~~{.go caption="main.go"}

type Animal struct {
    Name string
}

func (a *Animal) Speak() string {
    return "I am an animal and my name is " + a.Name
}

~~~

Next, We can create an instance of a new animal struct in a `main` function and call the `Speak` method on it:

~~~{.go caption="main.go"}

func main() {
    a := Animal{
        Name: "goat",
    }
    fmt.Println(a.Speak())
}

~~~

In the code above, we created a new instance of an animal and defined its `Name` field as "goat." We then call the `Speak()` method on it as defined in our interface.
This outputs:

~~~{ caption="Output"}

I am an animal and my name is goat

~~~

Interfaces in Golang are important because they allow for loose coupling between structs and other types, making it easier to change and extend code. The only required methods in a `struct` that implement an interface are the ones we define on the `interface`. The struct can still have other methods and properties that are not part of the interface. This allows for flexibility in the implementation while still ensuring that certain functionality is available. Additionally, interfaces allow for [polymorphism](https://en.wikipedia.org/wiki/Polymorphism_(computer_science)), where a single function or method can work with multiple types that implement the same interface.
In Go, interfaces are implemented implicitly, meaning that a struct does not need to explicitly declare that it implements an interface. A struct automatically implements an interface if it has all the methods defined in that interface. This makes it easy to add new interfaces to structs without changing the struct itself.

For Example:

~~~{.go caption="main.go"}

package main
import "fmt"
type Printer interface {
    Print()
}

type LaserPrinter struct {}

func (lp LaserPrinter) Print() {
    // Implement the Print method for LaserPrinter
    fmt.Println("Welcome")
}

~~~

In the code block above, we declared an interface `Printer` with the `Print()` method and a struct `LaserPrinter` that implements the `Print()` method of the interface. Go considers that the `LaserPrinter` struct satisfies the `Printer` interface implicitly because the struct has the `Print` method that matches the signature of the `Print` method in the `Printer` interface. However, Go does not perform this check at compile time, and instead waits until we use the `LaserPrinter` struct as a `Printer`.

The code can be extended to explicitly declare the `LaserPrinter` struct on the interface in a function.

For example:

~~~{.go caption="main.go"}

package main
import "fmt"
type Printer interface {
    Print()
}

type LaserPrinter struct {}

func (lp LaserPrinter) Print() {
    // Implement the Print method for LaserPrinter
    fmt.Println("Welcome")
}

func main() {
    var p Printer
    p = LaserPrinter{}
    p.Print()
}

~~~

This output:

~~~{caption="Output"}

Welcome

~~~

Not understanding how interfaces work in Go can lead to certain errors and bugs in our codes. Here are some scenarios:

### Invoking an Unimplemented Method Defined in an Interface

One common mistake when working with interfaces is calling a method that is not implemented by the struct but defined in the interface. For example, if we have an interface called `Speakable` with two methods, `Speak()` and `Listen()`, and we define a struct (that implements this interface) that only implements `Speak()` in our function but not the `Listen()` method of the interface. The program will not compile. If we try to invoke the `Listen()` method:

~~~{.go caption="main.go"}

type Speakable interface {
    Speak() string
    Listen() string
}

type Animal struct {
    Name string
}

func (a *Animal) Speak() string {
    return "I am an animal and my name is " + a.Name
}

func main() {
    a := Animal{
        Name: "goat",
    }
    fmt.Println(a.Listen())
    // error: a.Listen undefined (type Animal has no field \
    or method Listen)
}

~~~

This outputs an error:

~~~{ caption="Output"}

./main.go:22:19: a.Listen undefined (type Animal has \
no field or method Listen)

~~~

In the code block above, we defined the interface `Speakable` and defined two methods for it, namely `Speak()` and `Listen()`. We implemented only the `Speak()` method for the defined struct `Animal`. When calling the interface methods on an instance of the struct, we invoked the unimplemented method `Listen()` which led to an error.

> Note: A struct doesn't necessarily need to implement all the methods defined in an interface but the struct mustn't invoke an unimplemented function to avoid an error.

To avoid unnecessary errors and bugs when defining interfaces in Go, we should ensure that only the methods defined in the interface and implemented by the structs are invoked.

### Calling A `Nil` Interface

A `nil` pointer dereference error in interfaces in [Golang](/blog/top-3-resources-to-learn-golang-in-2021) occurs when we call a function or method on a `nil` pointer, causing a [runtime panic](https://go.dev/ref/spec#Run_time_panics). The `nil` pointer error happens when a struct implements an interface but the struct pointer is not initialized. For example:

~~~{.go caption="main.go"}

type Speakable interface {
    Speak() string
}

type Animal struct {
    Name string
}

func (a *Animal) Speak() string {
    return "I am an animal and my name is " + a.Name

}

func main() {
    var i Speakable
    i.Speak()
    // runtime error: invalid memory address or nil pointer dereference
}

~~~

This outputs:

~~~{ caption="Output"}

panic: runtime error: invalid memory address or nil pointer dereference
[signal SIGSEGV: segmentation violation code=0x2 addr=0x0 pc=0x100952b10]

goroutine 1 [running]:
main.main()
        /Users/Me/Desktop/DSA/backtracking/main.go:19 +0x20
exit status 2

~~~

In the code block above, we declared a variable `i` as an interface type, but it is not initialized with any value. When we call the `Speak()` method on `i`, it will cause a `nil` pointer dereference error because `i` is a `nil` pointer. To fix this, we need to initialize the variable `i` with a value of type `Animal` or any other type that implements the `Speakable` interface:

~~~{.go caption="main.go"}

func main() {
    var i Speakable
    i = &Animal{Name: "john doe"}
    i.Speak()
}

~~~

We must check the variable of the initialized interface is not nil before calling any function or method on it to prevent such errors.

For Example:

~~~{.go caption="main.go"}

import "fmt"

func main() {
    var myInterface interface{}

    if myInterface != nil {
        fmt.Println("myInterface is not nil")
    } else {
        fmt.Println("myInterface is nil")
    }
}

~~~

This outputs:

~~~{ caption="Output"}

myInterface is nil

~~~

In the code block above, we declared an empty Interface and did a check if it isn't `nil` using the `!=` operator.

### Type Assertion Errors

A [type assertion error](https://www.golinuxcloud.com/golang-type-assertion/) in interfaces in Go occurs when a type assertion is used to convert an interface value to a specific type but the value does not implement that type. Type assertions are used to check if an interface value holds a specific concrete type and to extract that value. The syntax of a type assertion is:

~~~{.go caption="main.go"}

x.(T)

~~~

Where x is an interface value, and `T` is the type that x is being asserted to.

For example, let's consider the following code:

~~~{.go caption="main.go"}

type Speakable interface {
    Speak() string
}

type People struct {
}

func main() {
    var f Speakable
    s := f.(*People) //impossible type assertion: f.(*People)

    s.Speak()
}

~~~

This outputs:

~~~{ caption="Ouptut"}

./main.go:14:7: impossible type assertion: f.(*People)
        *People does not implement Speakable (missing Speak method)
./main.go:16:4: s.Speak undefined (type *People has no field or \
method Speak)

~~~

In the code block above, we defined a new struct `People` that doesn't implement the `Speak()` method of the interface. We then initialized an interface type `f` and asserted it on the `People` struct. A type assertion error is returned because the `People` struct doesn't implement the interface `Speakable`.

To avoid this type of error, we should ensure the interface value implements the type we are asserting it to.

## Mistake 3: Not Utilizing Concurrency Effectively

Concurrency in Go (also known as [goroutines](https://gobyexample.com/goroutines)) allows multiple tasks to be executed [concurrently rather than sequentially](https://medium.com/codex/go-concurrency-vs-parallelism-c3fc9cec55c8). This can improve performance by allowing the program to make better use of available resources such as the CPU and memory.
A [goroutine](https://go.dev/tour/concurrency/1) is a lightweight thread of execution managed by the Go runtime. They are created by using the [go keyword](https://go.dev/ref/spec#Go_statements), followed by a function call.

The syntax of the goroutine is:

~~~{.go caption="main.go"}

go function()

~~~

Here's an example:

~~~{.go caption="main.go"}

package main

import (
    "fmt"
    "time"
)

func printNumbers() {
    for i := 1; i <= 10; i++ {
        fmt.Println(i)
    }
}

func main() {
    go printNumbers() // create a goroutine
    go printNumbers() // create another goroutine
    time.Sleep(1 * time.Second)
    // main function continues to execute here
}

~~~

In the code block above, we created a function named `printNumbers()` to print numbers between 1 and 10 by initializing a counter `i` and incrementing the counter in the loop. We then called the `printNumbers()` function as a goroutine twice, allowing them to execute simultaneously. The `time.Sleep()` method is used to pause the execution of the `main` function for 1 second so all the go routines get executed successfully.

> Note: Without the `time.Sleep()` method, the `main` function terminates without allowing the go routines to execute successfully, and nothing will output in our terminal. This happens because the `main` function executes prematurely, terminating the goroutine before it completes successfully.  

![sleep]({{site.images}}{{page.slug}}/sleep.png)\

Goroutines can also be used in conjunction with [channels](https://go.dev/ref/spec#Channel_types), which enable goroutines to communicate and synchronize their execution. They are created with the [`make`](https://www.educative.io/answers/what-is-golang-function-maket-type-size-integertype-type)  function and have a specific type, for example, `chan int` for a channel that sends and receives integers.

Here's an example:

~~~{.go caption="main.go"}

func printNumbers(c chan int) {
    for i := 1; i <= 10; i++ {
        c <- i
    }
    close(c)
}

func main() {
    c := make(chan int)
    go printNumbers(c)
    for n := range c {
        fmt.Println(n)
    }
}

~~~

In the code block above, the `printNumbers` function sends the numbers 1 through 10 to the channel `c`. The `main` function then receives those numbers from the channel and prints them. This allows the goroutine executing the `printNumbers` function to run concurrently with the `main` function, and also allows them to synchronize their execution using the channel.

Concurrency in Go boosts performance by allowing a program to better utilize available resources, such as multiple CPU cores. It also enables a program to respond to multiple events at the same time, rather than waiting for one event to finish before moving on to the next.

Not understanding how concurrency works in Go can lead to certain errors and bugs in our codes. Here are some scenarios:

### Not Using Channels To Synchronize Goroutines

Channels are a key feature in Go's concurrency model and are used to coordinate and synchronize the execution of goroutines. They allow goroutines to communicate with each other and to share data in a safe and controlled way.
Failure to use channels to synchronize our goroutines can result in unexpected code behavior and [race conditions](https://www.baeldung.com/cs/race-conditions), as multiple goroutines may attempt to access shared data at the same time without proper coordination.

Here's an example:

~~~{.go caption="main.go"}

package main

import "fmt"

var counter int

func printNumbers() {
    for i := 0; i < 10; i++ {
        counter++
    }
}
func main() {
    go printNumbers()
    go printNumbers()
    fmt.Println(counter)
}

~~~

It outputs:

~~~{ caption="Ouput"}

0

~~~

In the code block above, the `printNumbers` function is called twice as a goroutine, both are incrementing the same `counter` variable, but there's no synchronization between them, so the final value of the `counter` will be unpredictable. The output is `0` which is not what we expected.

This can be fixed by using channels to synchronize the two goroutines by sending and receiving data between them.

For example:

~~~{.go caption="main.go"}

func printNumbers(c chan int) {
    for i := 1; i <= 10; i++ {
        c <- i
    }
    close(c)
}

func main() {
    c := make(chan int)
    go printNumbers(c)
    for n := range c {
        fmt.Println(n)
    }
    d := make(chan int)
    go printNumbers(d)
    for n := range d {
        fmt.Println(n)
    }
}

~~~

This outputs:

~~~{ caption="Output"}

1
2
3
4
5
6
7
8
9
10
1
2
3
4
5
6
7
8
9

~~~

In the code block above, we created two channels in our `main` function, `c` and `d` to receive data from our goroutines and output them. From the output, the channel synchronized the two go routines, and we got the expected output.
This will ensure the goroutines are executed perfectly before the `main` function terminates.

### Not Handling Goroutine Leaks

A [goroutine leak](https://medium.com/golangspec/goroutine-leak-400063aef468) occurs when a goroutine is started but not properly terminated, leading to the goroutine running indefinitely. This can cause resource leaks, performance issues, and unexpected behavior in the program.

Here is an example of code that can cause a goroutine leak:

~~~{.go caption="main.go"}

package main

import "fmt"

func infiniteLoop() {
    for {
        fmt.Println("Here we are")
    }
}

func main() {
    go infiniteLoop()
}

~~~

In the code block above, we started the `infiniteLoop()` function as a goroutine, but it never terminates. This means that the goroutine will continue to run indefinitely, even after the `main()` function has finished executing.
To fix this, we can use a channel to [signal](https://medium.com/@matryer/golang-advent-calendar-day-two-starting-and-stopping-things-with-a-signal-channel-f5048161018) when the goroutine should terminate:

~~~{.go caption="main.go"}

func infiniteLoop(done chan bool) {
    for {
        select {
        case <-done:
            return
        default:
            // Do something
        }
    }
}

func main() {
    done := make(chan bool)
    go infiniteLoop(done)
    // Do something else
    done <- true
}

~~~

In the code block above, we passed the `done` channel to the `infiniteLoop()` function as an argument. Inside the loop, the function uses a [`select`](https://www.geeksforgeeks.org/select-statement-in-go-language/) statement to check for a message on the `done` channel. If a message is received, the function exits the loop and terminates the goroutine. In the `main()` function, a message is sent on the `done` channel to signal the goroutine to terminate.

> Note: The sign `<-` is used to send and receive values on the channel, i.e., `done <- true` means we are sending a bool value `true` to channel `done`.

## Mistake 4: Not Using third-party Libraries Effectively

There is a wide range of third-party libraries available for Golang that can help developers build high-performance and feature-rich applications. These libraries provide a variety of functionality, including:

- **Web Development**:
There are several web development libraries available for Golang, such as the popular [Gin](https://github.com/gin-gonic/gin), [Fiber](https://github.com/gofiber/fiber), and [Echo](https://github.com/labstack/echo) frameworks, which provide a lightweight and fast way to build web applications.

- **Database Access**:
Golang has several libraries for interacting with various types of databases, including SQL and NoSQL databases. Popular libraries include [Gorm](https://github.com/go-gorm/gorm) for interacting with MySQL, PostgreSQL, and [SQLite](/blog/golang-sqlite), and [Mongo-Go-Driver](https://github.com/mongodb/mongo-go-driver) for interacting with MongoDB.

- **Logging**:
There are several libraries available for [logging](/blog/understanding-docker-logging-and-log-files) in Golang, such as [Logrus](https://github.com/sirupsen/logrus) and [Zap](https://github.com/uber-go/zap), which provide a way to log messages and trace errors in your application.

- **Package Management**:
There are many libraries available for package management in Golang, such as the Go module, [Glide](https://github.com/Masterminds/glide), and [Dep](https://github.com/golang/dep), which provide a way to manage dependencies and versioning in your application.

- **Command-Line Interface**:
Several libraries are available for building command-line interfaces in Golang, such as [Cobra](https://github.com/spf13/cobra) and [Cmd](https://github.com/devfacet/gocmd), which provide a way to build command-line applications.
Not using third-party libraries effectively in Golang can cause problems and errors; here are some examples of common errors:

### Not Updating Third-Party Libraries

When using third-party libraries in Golang, it's important to keep them up-to-date to ensure that they are compatible with the latest version of Golang and that they have the latest bug fixes and features.
One way to do this is to use a package management tool like [Go modules](https://www.digitalocean.com/community/tutorials/how-to-use-go-modules) to automate updates or check the library's documentation to see if there are any updates available.

Here's the command to update a library in the Go module:

~~~{.bash caption=">_"}

$ go get -u <package-name>

~~~

### Importing an Unused Library

In Golang, importing an unused library will lead to the code not compiling properly, so it's important to always check that all libraries imported are in use.

For example:

~~~{.go caption="main.go"}

package main

import "fmt"

func main(){

}

~~~

In the code block above, we imported the `fmt` library without utilizing it. Go won't compile the code and will output the following error when the code is run:

~~~{caption="Output"}

./main.go:3:8: imported and not used: "fmt"

~~~

We can run the following command to tidy up our code when working on a large codebase with `go.mod` file:

~~~{.bash caption=">_"}

$ go mod tidy

~~~

### Not Checking for Errors When Using the Libraries

It is important to check for errors when using third-party libraries in Go, as they can indicate issues with the library or its configuration. For example, if we are using a library to connect to a database, we should check for errors when opening the connection.

![error]({{site.images}}{{page.slug}}/error.jpg)\

~~~{.go caption="main.go"}

connection, err := sql.Open("postgres", "user=pqgotest \
dbname=pqgotest sslmode=verify-full")
if err != nil {
    log.Fatal(err)
}

~~~

Not checking for errors can lead to unexpected behaviors in our codes. It can also affect the maintainability of the codes as uncaught errors accumulate and make it hard to fix issues when they occur.

### Mistake 5: Not Properly Handling Errors

Error handling in Golang is done using the built-in [`error` type and the `return` statement](https://earthly.dev/blog/golang-errors/). Unlike the `try..except` in other languages, Go handles errors by comparing the returned error to `nil` where a `nil` value indicates no error has occurred.

Here's an example:

~~~{.go caption="main.go"}

package main

import "fmt"

func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, fmt.Errorf("cannot divide by zero")
    }
    return a / b, nil
}

func main() {
    result, err := divide(5, 0)
    if err != nil {
        fmt.Println(err)
        return
    }
    fmt.Println(result)
}

~~~

This outputs:

~~~{caption="Output"}

cannot divide by zero

~~~

In the code block above, we created a function to divide two integers and wrote an error statement when the number to divide with is `0`. We then handled the error in our `main` function when calling the `divide` function by checking if the error is `nil`.
This will ensure a proper error message is returned when `b` is 0 and will prevent our code from *panicking*.

Here are some common mistakes made when handling errors in Go:

### Panicking Instead of Returning Errors

Panicking an error instead of returning an actual error message isn't a best practice when handling errors in Go because it leads to the program stopping its execution and closing all functions currently executing. Thereby, it's recommended to return an actual error message so the program can handle the error in a more predictable and controlled manner.

![panick]({{site.images}}{{page.slug}}/panick.png)\

For example, let's rewrite the previous code block by panicking the error message:

~~~{.go caption="main.go"}

func divide(a, b int) int {
    if b == 0 {
        panic("Cannot divide by zero")
    }
    return a / b
}

func main() {
    result := divide(5, 0)
    fmt.Println("Result:", result)
}

~~~

In the code block above, we use the built-in [`panic`](https://www.educative.io/answers/what-is-panic-in-golang)  function to stop the execution of the function when `b` is zero.

This will output to our terminal:

~~~{ caption="Output"}

panic: Cannot divide by zero
goroutine 1 [running]:
main.divide(...)
        /Users/Me/Desktop/DSA/backtracking/main.go:100
main.main()
        /Users/Me/Desktop/DSA/backtracking/main.go:106 +0x30
exit status 2

~~~

### Not Providing Detailed Error Messages

A vague error message doesn't help when debugging, and it is best practice to provide a clear and helpful error message when handling errors in Golang.

For example, in our `divide` function above, assuming we wrote a vague error message like this:

~~~{.go caption="main.go"}

func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, fmt.Errorf("an error occurred")
    }
    return a / b, nil
}

~~~

This won't provide enough context for what might have caused the error compared to the former error message, which is `cannot divide by 0`.
A detailed error message helps in [debugging](/blog/printf-debugging) faster and identifying what the issue is.

## Conclusion

In conclusion, Golang is a powerful and efficient programming language that can be used to build a wide range of applications. However, it is important to be aware of these common mistakes that can occur when learning the Go language, as they can save us time and frustration as we learn and work with Go. The five mistakes include:

- Not properly understanding pointers and deferences
- Not fully utilizing the interface effectively
- Not utilizing concurrency effectively
- Not using third-party libraries
- Not properly handling errors

Let's also remember to take advantage of the vast resources available online and in the Go community, as well as to practice and experiment with different code snippets and examples to improve our skills.

{% include_html cta/bottom-cta.html %}
