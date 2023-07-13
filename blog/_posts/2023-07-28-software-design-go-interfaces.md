---
title: "Designing Extensible Software with Go Interfaces"
categories:
  - Tutorials
toc: true
author: Ben Smitthimedhin
editor: Muhammad Badawy

internal-links:
 - designing extensible software
 - designing software
 - designing software with go interfaces
 - go interfaces
 - extensible software with go
---

[Go](https://go.dev/), also known as Golang, is a simple and efficient programming language that's been adopted by many tech companies, including Uber, Twitch, and Microsoft. Similar to other programming languages such as Java and C++, Go supports interfaces, which provide a powerful mechanism for ensuring that class objects inherit a defined set of properties.

In this article, you'll learn how to use interfaces in Go to design extensible, modular software. Moreover, you'll learn how to use interfaces to promote code reusability, flexible architecture, and an improved development experience.

> **Please note:** Familiarity with object-oriented programming concepts is a prerequisite to walking through the article.

## Why You Need Interfaces

Interfaces have played a fundamental role in programming since the need to abstract the definition of a function from the implementation arose in [object-oriented programming](https://www.geeksforgeeks.org/introduction-of-object-oriented-programming/). A great example of why you need interfaces can be found in Eric Freeman and Elisabeth Robson's book [*Head First Design Patterns*](https://a.co/d/bCjS9z5). In it, Freeman and Robson mention a scenario in which a software engineer, Joe, creates a `Duck` superclass that can `quack()`, `swim()`, and `display()`, something all ducks can do. A `MallardDuck` and a `RedheadDuck` class can, therefore, be created that inherits the `Duck` superclass. Although these two classes must have the `quack()`, `swim()`, and `display()` functions since they inherit the `Duck` superclass, they can customize how these functions work according to their class.

However, when Joe is asked by his boss to add a `fly()` function, he quickly realizes that he needs to customize his whole stack since not all ducks can fly.

In this scenario, an interface is a great solution for this problem since Joe can abstract away the `fly()` function to a separate interface called `flyable`. This ensures that the `Duck` superclass still functions as expected; ducks that can fly will simply implement the `flyable` interface, and ducks that can't, won't.

Interfaces allow you to achieve this effect through composition, where you define smaller, focused interfaces that can be combined to create more complex behavior. This principle is called [composition over inheritance](https://www.digitalocean.com/community/tutorials/composition-vs-inheritance).

## Basics of Interfaces in Go

The code for all the examples in this tutorial can be found in [this GitHub repo](https://github.com/jsmitthimedhin/go-interface-examples).

In Go, you can define structs with certain methods like this:

~~~{.go caption="animals.go"}
type (
    dog struct {
        name string
    }
    cat struct {
        name string
    }
)

func requiresBath(d dog) bool {
fmt.Printf("%s, needs a bath!", d.name)
return true
}

func (d dog) walk() {
fmt.Println("The dog is walking")
}

func (c cat) walk() {
    fmt.Println("The cat is walking")
}
~~~

Here, you define two struct types: a `dog` and a `cat`, both of which require the property `name` in string format. Then you define a function, `requiresBath,` which takes in a `dog` struct in its parameter. Lastly, you have two `walk` functions: one defined for a `dog` struct and one for the `cat` with different implementations.

As you can see, while Go's type-safety system is helpful in most cases, it can sometimes prevent you from creating more generic functions. For instance, the `requiresBath` function could ideally take in both `cat` and `dog` structs. However, the function requires you to define a specific object to pass in the parameter. But how do you create a function that can take in both `cat` and `dog` structs?

[*Head First Go*](https://a.co/d/1fk7wVs) author Jay McGavren informs you that interfaces allow you to "define variables and function parameters that will hold *any* type, as long as that type defines certain methods." Defining an interface in Go is fairly straightforward:

~~~{.go caption="animals.go"}
type walkable interface { 
walk() 
}
~~~

In this example, `walkable` is the name of the interface, and it contains one method, `walk()`. If you want to define two interfaces, you can write a shorthand like the following:

~~~{.go caption="animals.go"}
type (
    walkable interface {
        walk()
    }
    bathable interface {
        requiresBath() bool
    }
)
~~~

## Implementing Interfaces in Go

When it comes to implementing an interface, Go is a bit unique. As opposed to explicitly defining the class as implementing a specific interface, Go simply requires you to define a type that has the same method signatures as the interface. This means it only needs the following:

~~~{.go caption="animals.go"}
type cat struct{}
func (c cat) walk() { // however the function works }
~~~

In this example, `cat` implements the `walkable` interface because it implements the `walk()` function with the same parameters (the `walk` function in the interface passes nothing in) and the same return type (returning nothing). When an interface has multiple methods, a struct needs to contain all the methods within that interface (with the same parameters and return type) to implement that interface.

Since both `cat` and `dog` have their own `walk()` methods, you can assume that they both implement the `walkable` interface. Now you can refactor the `requiresBath` function to take in both `cat` and `dog` objects by accepting any object that implements `walkable` instead:

~~~{.go caption="animals.go"}
func requiresBath(i walkable) bool {
return true
}
~~~

### The Empty Interface

In addition to defining interfaces with specific method signatures, Go also has an empty interface, a typewritten as `interface{}` or `any`:

~~~{.go caption="print.go"}
var i interface{}
var a any  
~~~

Using what you've learned earlier, you know that for a `cat` to implement the `walkable` interface, it must implement `walk` and any other method of that interface (if you decide to add more). But if you have an empty interface with no method signatures defined, you have an interface that is automatically implemented in every single struct ever defined. But why do you need this?

Just like an `any` type in any programming language, an empty interface can be useful in situations where you need a generic function that accepts and returns multiple types. For instance, say you have a function that you want to create that automatically loops through a slice and prints each value individually. Since Go's type-safety system requires you to define the type of slice in the parameter, you would have to create multiple functions that take in different kinds of slices. In this way, having an empty interface allows you to create a workaround of Go's type-safety system for cases that require exceptions:

~~~{.go caption="print.go"}
// instead of this:
func printStrings(s []string) { //loop and print}
func printIntegers(s []int) { //loop and print}
// we can do this:
func printAnything(s interface{}) { //loop and print}
~~~

> **Please note:** The empty interface/`any` type should be used carefully only after the developer has considered possible type errors that could occur with the function. Other ways to constrain the possibility of types in a function can be found in this [Go Blog post](https://go.dev/blog/when-generics).

### Extensibility Through Interfaces

One of the key benefits of using interfaces is that they promote extensibility, meaning new kinds of structs can be added that implement the interface without changing the interface itself. By defining interfaces, you can decouple them from the structs that implement them, making it easier to modify or replace the problematic structs without affecting other parts of the code.

Interfaces provide the abstractions you need, allowing you to write code that depends on an interface rather than a specific implementation. This is the [dependency inversion principle](https://blog.logrocket.com/dependency-inversion-principle-typescript/) in action, which states that high-level modules should not depend on low-level modules; both should depend on abstractions.

Look at some practical examples of how interfaces can be used to design modular, extensible software.

### Designing a Storage System

Suppose you're building a system that needs to store data. There are several different types of storage systems you might want to use, such as file-based storage, database storage, or cloud storage. Instead of tying your code to a specific storage system, you can define an interface for the storage system like this:

~~~{.go caption="storage.go"}
type Storage interface { 
ListValues(prefix string) ([]byte, error)
GetValue(path string) (byte, error)
PutValue(path string, value []byte) error
DeleteValue(path string) error
}
~~~

This interface defines standard CRUD (create, read, update, delete) methods for interacting with storage. You can then write code that depends on this interface rather than a specific implementation of the storage system, and the specific type of storage you'd like can be passed in as a parameter or part of the struct.

For example, if you have a `database` struct that implements the `Storage` interface, you can then create a `saveToStorage` function that takes in a `Storage` interface as one of the parameters:

~~~{.go caption="storage.go"}
type database struct {}

func (d *database) ListValues(prefix string) ([]byte, error) {
    // unique code for listing values from the database here
}

// ... other Storage methods that the database struct implements

func saveToStorage(Storage, path string, values []byte) error {
    // code for saving things to storage
}
~~~

However, when you actually call that function, you can pass a specific struct that implements the `Storage` interface instead. This ensures that your function remains agnostic as to what type of storage is being sent:

~~~{.go caption="storage.go"}
func main() {
    db := &database{}
           values := make([]byte, 0)
    saveToStorage(db, "path", values)
}
~~~

Now, if you want to change which storage you save to, you don't need to touch the `saveToStorage` function at all. You can simply replace what you pass into it, making your code cleaner in its definition and implementation.

### Logger Interface

Creating a logger interface is a common use case for interfaces in Go. A logger interface can be used as a simple interface that provides a method for writing log messages and (once again) is agnostic of the specific type of logger you use:

~~~{.go caption="logger.go"}
type logger interface { 
log(message string) 
}
~~~

To use this interface, you can implement it in different ways, depending on your needs. For example, you might implement a console logger that writes log messages to the console. You can also add a file logger that writes log messages to a file. Both would implement the logger interface by holding the same method signature:

~~~{.go caption="logger.go"}
type (
    consoleLogger struct{}
    fileLogger    struct{ filePath string }
)

func (cl consoleLogger) log(message string) {
    fmt.Println(message)
}

func (fl fileLogger) log(message string) {
    file, err := os.OpenFile(fl.filePath, \
    os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
    if err != nil {
        fmt.Println("Error opening log file:", err)
        return
    }
    defer file.Close()
    logMessage := fmt.Sprintf("%v - %v\n", \
    time.Now().Format(time.RFC3339), message)
    if _, err = file.WriteString(logMessage); err != nil {
        fmt.Println("Error writing to log file:", err)
    }
}
~~~

Here, you define two struct types: a `consoleLogger` and a `fileLogger`. The `consoleLogger` struct has no required properties, though the `fileLogger` one requires a `filePath` property in string format. Then you define the `log` function for each struct type. The `consoleLogger`'s `log` function simply logs whatever message is passed to the console. On the other hand, the `fileLogger`'s `log` function opens or creates a text file using the `filePath` property from the struct, writes the message in it, and closes the file, all with error handling in each of the steps.

By using interfaces to define a common set of methods, you can easily switch between different logger implementations without having to change the code that uses the logger. Just as mentioned earlier, this allows you to modify which type of logger you'd like to implement easily without having to redefine the methods or the interface.

## Advanced Interface Techniques

When it comes to advanced interface techniques, type assertions, type switches, interface embedding, and interface values emerge as powerful tools, enabling developers to navigate and manipulate complex data structures with finesse and precision. Take a look at each of these techniques:

### Type Assertion

Go provides a way to extract an underlying value of an interface if it exists. This can be helpful if you want to assign a variable to an underlying property associated with an interface.

For instance, in the previous `Logger` example, both `ConsoleLogger` and `FileLogger` implement the `Logger` interface. If you were to initialize a variable of the `Logger` interface type and assign it a `FileLogger` struct, you could grab the `FilePath` property and assign it to a variable like this:

~~~{.go caption="logger.go"}
func main() {
    var i logger = fileLogger{filePath: "Hello"}
    s := i.(fileLogger)
    fmt.Println(s)
     /// This will print out "Hello"
    s, ok := i.(fileLogger)
    /// Type assertion also returns true/false depending 
    
    /// on if the underlying type exists
    fmt.Println(s, ok)
    /// This will print out "Hello true"
}
~~~

### Type Switches

Another related advanced technique is performing type switches to test the underlying type of an interface value and perform different actions depending on the type.

For example, if you were to write a function that determines the type of `Logger` being passed, you could do something like this:

~~~{.go caption="logger.go"}
func determineLogger(l Logger) string {
    switch v := l.(type) {
    case fileLogger:
        return "It's a file logger!"
    case consoleLogger:
        return "It's a console logger!"
    default:
        fmt.Printf("Type %T! logger\n", v)
        return "It's an unknown logger!"
    }
}
~~~

### Interface Embedding

[Interface embedding](https://www.geeksforgeeks.org/embedding-interfaces-in-golang/) is another advanced technique that allows you to define new interfaces by combining multiple existing interfaces. By embedding one interface inside another, you can create a new interface that inherits all the methods from both interfaces.

Using the previous example with `bathable` and `walkable` interfaces, you can create a third interface, `talkable`, that combines the two. This means that any struct implementing `talkable` must have all the methods listed in the `bathable` and `walkable` interface:

~~~{.go caption="animals.go"}
type (
    walkable interface {
        walk()
    }
    bathable interface {
        requiresBath() bool
    }
    talkable interface {
        walkable
        bathable
        talk()
    }
        
)
~~~

### Interface Values

Lastly, methods or values that are part of the interface can be accessed freely regardless of the struct implementing the interface. Say you have a method that runs the `Log()` method of a `Logger` interface regardless of the specific struct like this:

~~~{.go caption="logger.go"}
func main() {
    var l logger = consoleLogger{}
    useLogger(l)
}

func useLogger(l logger) {
    l.log("Running method")
}
~~~

Go lets you access the `log()` method regardless of the actual implementation defined by the struct. In this case, the `log()` method being run is the one defined by the `consoleLogger` type.

### Testing With Interfaces

Interfaces can be useful for testing code because they allow you to replace real dependencies with mock implementations. As long as your mock is implementing the methods associated with your interface, you are good to go!

For example, in this test file, you're testing the function `determineLogger(l Logger)`, which takes in the `Logger` interface as a parameter. Creating a `mockLogger` type and defining the `Log` method in accordance with the `Logger` interface means that you can now pass it into the `determineLogger(l Logger)` function since it fulfills the requirements of the interface:

~~~{.go caption="logger_test.go"}
type mockLogger struct {}

func (m mockLogger) log(message string) {
    fmt.Println("Fake logger implementation!")
}
func TestDetermineLogger_UnknownLogger(t *testing.T) {
    m := mockLogger{}
    // My expected result of the test is that it would return the 
    // string below:
    expected := "It's an unknown logger!"
    // I call the function and pass in the mockLogger object:
    result := determineLogger(m)
    // and assert that what's expected will equal the result:
    assert.Equal(t, expected, result)
}
~~~

Interfaces can also be useful for test-driven development because they allow you to define the expected behavior of your code before you write the implementation. However, [there are many in the Go community](https://www.ardanlabs.com/blog/2016/10/avoid-interface-pollution.html) who warn against defining interfaces beforehand for the purposes of test-driven development. As [Rob Pike](https://www.amazon.com/Ultimate-Go-Notebook-William-Kennedy/dp/1737384426), one of the creators of Go, warns, "Don't design with interfaces, discover them." In other words, interfaces should be defined only when a need for abstraction arises.

## Best Practices for Interfaces

When using interfaces, it's important to consider when they're appropriate. Interfaces can be useful for defining a common set of methods for different types, but they can also add unnecessary complexity if overused.

It's important to design interfaces that are small and focused, with a clear and well-defined purpose. This means having as few methods as possible for a given interface since implementing the interface requires defining the same methods for that particular struct with its own logic. Having multiple structs that implement multiple methods in an interface can quickly lead to cluttered code.

Teiva Harsanyi in [*100 Go Mistakes and How to Avoid Them*](https://a.co/d/3MUFMDR) mentions that, generally, the three use cases that interfaces are useful for include "factoring out a common behavior, creating some decoupling, and restricting a type to a certain behavior," all three of which are covered here.

## Conclusion

Go interfaces are a powerful tool for designing extensible and modular software. By defining a common set of methods for different types, interfaces can promote code reusability, flexible architecture, and testable code that's easy to mock.

Interfaces can be used for purposes such as creating generic storage systems or loggers, among many other abstractions. While interfaces can be useful, it's important to use interfaces only when the need arises and to make them as tiny as possible.

{% include_html cta/bottom-cta.html %}

## Outside Article Checklist

- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images

