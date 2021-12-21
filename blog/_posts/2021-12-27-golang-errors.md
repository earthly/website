---
title: "Effective Error Handling in Golang"
categories:
  - Tutorials
toc: true
author: Brandon

internal-links:
 - just an example
---
Error handling in Go is a little different than other mainstream programming languages like Java, JavaScript, or Python. Go's built-in errors don't contain stack traces, nor do they support conventional `try`/`catch` methods to handle them. Instead, errors in Go are just values returned by functions, and they can be treated in much the same way as any other datatype - leading to a surprisingly lightweight and simple design.

In this article, we'll demonstrate the basics of handling errors in Go, as well as some simple strategies you can follow in your code to ensure your program is robust and easy to debug.

## The Error Type

The error type in Go is implemented as the following interface:

~~~{.go}
type error interface {
    Error() string
}
~~~

So basically, an error is anything that implements the `Error()` method, which returns an error message as a string. It's that simple!

### Constructing Errors

Errors can be constructed on the fly using Go's built-in `errors` or `fmt` packages. For example, the following function uses the `errors` package to return a new error with a static error message:

~~~{.go caption="main.go"}
package main

import "errors"

func DoSomething() error {
    return errors.New("something didn't work")
}
~~~

Similarly, the `fmt` package can be used to add dynamic data to the error, such as an `int`, `string`, or another `error`. For example:

~~~{.go caption="main.go"}
package main

import "fmt"

func Divide(a, b int) (int, error) {
    if b == 0 {
        return 0, fmt.Errorf("can't divide '%d' by zero", a)
    }
    return a / b, nil
}
~~~

Note that `fmt.Errorf` will prove extremely useful when we use it to wrap another error using the `%w` format verb - but we'll get into more detail on that further down in the article.

There are a few other important things we should take notice of in the example above.

* Errors can be returned as `nil`, and in fact, it's the default, or "zero", value of on error in Go. This is important since checking `if err != nil` is the idiomatic way to determine if an error was encountered (replacing the `try`/`catch` statements you may be familiar with in other programming languages).

* Errors are typically returned as the last argument in a function. Hence in our example above, we return an `int` and an `error`, in that order.

* When we do return an error, the other arguments returned by the function are typically returned as their default "zero" value. A user of a function may expect that if a non-nil error is returned, then the other arguments returned are not relevant.

* Lastly, error messages are usually written in lower-case and don't end in punctuation. Exceptions can be made though, for example when including a proper noun, a function name that begins with a capital letter, etc.

### Defining Expected Errors

Another important technique in Go is defining expected Errors so we can check for them explicitly in other parts of our code. This becomes useful if we need to execute a different branch of code when a certain kind of error is encountered.

#### Defining Sentinel Errors

Building on our `Divide` function from earlier, we can improve the error signaling by predefining a "Sentinel" error so that any calling function knows how to check for a "divide by zero" error.

The following program takes two integers, `a` and `b` as command-line arguments and attempts to call `Divide` on them, checking for our particular error using the `errors.Is` built-in method:

~~~{.go caption="main.go"}
package main

import (
    "errors"
    "fmt"
    "os"
    "strconv"
)

var ErrDivideByZero = errors.New("divide by zero")

func Divide(a, b int) (int, error) {
    if b == 0 {
        return 0, ErrDivideByZero
    }
    return a / b, nil
}

func main() {
    var a, b, result int
    var err error

    if len(os.Args) != 3 {
        fmt.Println("expected two command line arguments")
        return
    }

    a, err = strconv.Atoi(os.Args[1])
    if err != nil {
        fmt.Printf("argument '%s' in not a valid int: %s\n", os.Args[1], err)
        return
    }

    b, err = strconv.Atoi(os.Args[2])
    if err != nil {
        fmt.Printf("argument '%s' is not a valid int: %s\n", os.Args[2], err)
        return
    }

    result, err = Divide(a, b)
    if err != nil {
        switch {
        case errors.Is(err, ErrDivideByZero):
            fmt.Println("divide by zero error")
        default:
            fmt.Printf("unexpected division error: %s\n", err)
        }
        return
    }

    fmt.Printf("%d / %d = %d\n", a, b, result)
}
~~~

For further reading on parsing command line arguments in Go, check out [this page](https://gobyexample.com/command-line-arguments) on the "Go by Example" website.

#### Defining Custom Error Types

Many error-handling use cases can be covered using our strategy above, however, there are times when we want a little more functionality. Perhaps we want our error to carry additional data fields, or maybe we want our error's message to be populated with dynamic values when we print it.

We can do that in Go by implementing our own custom errors type.

Below is a slight rework of our previous example, notice the new type `DivisionError`, which implements the `Error` `interface`. We can also use `errors.As` to check and convert a standard error to our more specific `DivisionError`.

~~~{.go caption="main.go"}
package main

import (
    "errors"
    "fmt"
    "os"
    "strconv"
)

type DivisionError struct {
    IntA int
    IntB int
    Msg  string
} 

func (e *DivisionError) Error() string { 
    return e.Msg
}

func Divide(a, b int) (int, error) {
    if b == 0 {
        return 0, &DivisionError{
            Msg: fmt.Sprintf("cannot divide '%d' by zero", a),
            IntA: a, IntB: b,
        }
    }
    return a / b, nil
}

func main() {
    var a, b, result int
    var err error

    if len(os.Args) != 3 {
        fmt.Println("expected two command line arguments")
        return
    }

    a, err = strconv.Atoi(os.Args[1])
    if err != nil {
        fmt.Printf("argument '%s' in not a valid int: %s\n", os.Args[1], err)
        return
    }

    b, err = strconv.Atoi(os.Args[2])
    if err != nil {
        fmt.Printf("argument '%s' is not a valid int: %s\n", os.Args[2], err)
        return
    }

    result, err = Divide(a, b)
    if err != nil {
        var divErr *DivisionError
        switch {
        case errors.As(err, &divErr):
            fmt.Printf("%d / %d is not mathematically valid: %s\n", 
              divErr.IntA, divErr.IntB, divErr.Error())
        default:
            fmt.Printf("unexpected division error: %s\n", err)
        }
        return
    }

    fmt.Printf("%d / %d = %d\n", a, b, result)
}
~~~

Note: when necessary, you can also customize the behavior of the `errors.Is` and `errors.As`. See [this Go.dev blog](https://go.dev/blog/go1.13-errors) for an example.

Another note: `errors.Is` and `errors.As` were added in Go 1.13. More on that below.

## Wrapping Errors

In our examples thus far, the errors have been created, returned, and handled with a single function call. In other words, the stack of functions involved in "bubbling" up the error is only a single level deep.

Often in our real-world programs, we'll have many more functions involved - from the function where the error is produced, to where it is eventually handled, and any number of additional functions in-between.

In Go 1.13, several new error APIs were introduced, including `errors.Wrap` and `errors.Unwrap`, which are useful in applying additional context to an error as it "bubbles up", as well as checking for particular error types, regardless of how many times the error has been "wrapped".

> **A bit of history**: Before Go 1.13 was released in 2019, the standard library didn't contain many APIs for working with errors - it was basically just `errors.New` and `fmt.Errorf`. As such, you may encounter legacy Go programs in the wild that do not implement some of the newer error APIs. Many legacy programs also used 3rd-party error libraries such as [`pkg/errors`](https://github.com/pkg/errors). Eventually, [a formal proposal](https://go.googlesource.com/proposal/+/master/design/go2draft-error-inspection.md) was documented in 2018, which suggested many of the features we see today in Go 1.13+.

### The Old Way (Before Go 1.13)

It's easy to see just how useful the new error APIs are in Go 1.13+ are by looking at some examples where the old API was limiting.

Let's consider a simple program that manages a database of users. In this program, we'll have a few functions involved in the lifecycle of a database error.

For simplicity's sake, let's replace what would be a real database with an entirely "fake" database that we import from `"example.com/fake/users/db"`.

Let's also assume that this fake database already contains some functions for finding and updating user records. And that the user records are defined to be a struct that looks something like:

~~~{.go caption="fake/users/db.go"}
package db

type User struct {
  ID       string
  Username string
  Age      int
}

func FindUser(username string) (*User, error) { /* ... */ }
func SetUserAge(user *User, age int) error { /* ... */ }
~~~

Here's our example program:

~~~{.go caption="main.go"}
package main

import (
    "errors"
    "fmt"

    "example.com/fake/users/db"
)

func FindUser(username string) (*db.User, error) {
    return db.Find(username)
}

func SetUserAge(u *db.User, age int) error {
    return db.SetAge(u, age)
}

func FindAndSetUserAge(username string, age int) error {
  var user *User
  var err error

  user, err = FindUser(username)
  if err != nil {
      return err
  }

  if err = SetUserAge(user, age); err != nil {
      return err
  }

  return nil
}

func main() {
    if err := FindAndSetUserAge("bob@example.com", 21); err != nil {
        fmt.Println("failed finding or updating user: %s", err)
        return
    }

    fmt.Println("successfully updated user's age")
}
~~~

Now, what happens if one of our database operations fails with some `malformed request` error?

Our error check in the `main` function should catch that and print something like this:

~~~{.bash caption=">_"}
failed finding or updating user: malformed request
~~~

But which of the two database operations produced the error? Unfortunately, we don't have enough information in our error log to know if it came from `FindUser` or `SetUserAge`.

Go 1.13 adds a simple way we can get the information we need.

### Errors Are Better Wrapped

In the snippet below, we add `fmt.Errorf` with a `%w` verb to "wrap" the errors as they "bubble up" through our other function calls. This adds the appropriate context we need so that we can deduce which of those database operations failed in our previous example.

Here's our updated program:

~~~{.go caption="main.go"}
package main

import (
    "errors"
    "fmt"

    "example.com/fake/users/db"
)

func FindUser(username string) (*db.User, error) {
    u, err := db.Find(username)
    if err != nil {
        return nil, fmt.Errorf("FindUser: failed executing db query: %w", err)
    }
    return u, nil
}

func SetUserAge(u *db.User, age int) error {
    if err := db.SetAge(u, age); err != nil {
      return fmt.Errorf("SetUserAge: failed executing db update: %w", err)
    }
}

func FindAndSetUserAge(username string, age int) error {
  var user *User
  var err error

  user, err = FindUser(username)
  if err != nil {
      return fmt.Errorf("FindAndSetUserAge: %w", err)
  }

  if err = SetUserAge(user, age); err != nil {
      return fmt.Errorf("FindAndSetUserAge: %w", err)
  }

  return nil
}

func main() {
    if err := FindAndSetUserAge("bob@example.com", 21); err != nil {
        fmt.Println("failed finding or updating user: %s", err)
        return
    }

    fmt.Println("successfully updated user's age")
}
~~~

If we re-run our program and encounter the same error again, our log might print the following:

~~~{.bash caption=">_"}
failed finding or updating user: FindAndSetUserAge: SetUserAge: failed executing db update: malformed request
~~~

Now our message contains enough context so we can see that the problem originated in the `db.SetUserAge` function. Phew! That definitely saved us some time debugging!

Wrapping errors with meaningful messages (especially including the function name) gives us similar information as we might expect from printing a stack-trace in a language like Java.

#### When to Wrap

Generally, it's a good idea to wrap an error every time you "bubble" it up - i.e. every time you receive the error from a function and want to continue returning it back up the function chain.

There are some exceptions to the rule, however, where wrapping an error may not be appropriate.

Since wrapping the error always preserves the original error messages, sometimes exposing those underlying issues might be a security, privacy, or even UX concern. In those cases, it could be worth handling the error and returning a new one, rather than wrapping it. This could be the case if you're writing an open-source library or a REST API where we don't want the underlying error message to be returned to the 3rd-party user.

{% include cta/cta1.html %}

## Conclusion

That's a wrap! In summary, here's the gist of what was covered here:

* Errors in Go are just lightweight pieces of data that implement the `Error` `interface`
* Predefined errors will improve signaling, allowing us to check which error occurred
* Wrap errors to add enough context to trace through function calls (similar to a stack trace)

I hope you found this guide to effective error handling useful. If you'd like to learn more, I've attached some related articles I found interesting during my own journey to robust error handling in Go.

## References

* [Error handling and Go](https://go.dev/blog/error-handling-and-go)
* [Go 1.13 Errors](https://go.dev/blog/go1.13-errors)
* [Go By Example: Errors](https://gobyexample.com/errors)
* [Go By Example: Panic](https://gobyexample.com/errors)
* [Golang Error Handling Definitive Guide](https://gabrieltanner.org/blog/golang-error-handling-definitive-guide)

{% include cta/embedded-newsletter.html %}
