---
title: "Using Rust Generics to Write Flexible and Reusable Code"
categories:
  - Tutorials
toc: true
author: Enoch Chejieh
editor: Ubaydah Abdulwasiu

internal-links:
 - using rust generics
 - write flexible and reusable code
 - write code
 - rust generics
 - flexible and reusable code
---

**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster by using containerization. If you're interested in a different approach to building and packaging software, then [check us out](/).**

Rust's use of generics enables developers to write flexible and reusable code. Generics allow functions, structs, and enums to be defined without specifying the type of data they will operate on. This means that a single implementation can work with various types of data, making the code more versatile. Additionally, generics provide better type safety and reduce the likelihood of errors.

Generics were first introduced in the [Meta Language (ML) programming language](https://en.wikipedia.org/wiki/ML_(programming_language)) in the 1970s and have since become a common feature in many modern languages, such as Java, C#, and C++. Rust adopted generics from its inception in 2010, which enables developers to write code that works with any data type rather than being limited to a single type. This flexibility makes code more extensible and reusable because it can accommodate various data types without rewriting.

In this guide, you'll learn about the basics of generics in Rust, particularly generic functions, structs, and enums. Additionally, you'll learn about more advanced topics, including traits, generic lifetimes, phantom types, and type-level programming.

**Please note:** Make sure you wrap all your codes in a `main` function so that you don't get any errors.

## Using Generics in Rust

One powerful way to use generics is to create generic functions that can work with multiple types of parameters. These functions use placeholders for the types they operate on, called type parameters.

### Generic Functions

Generic functions operate on different types of data using placeholders for the data types they work with. These placeholders are called type parameters.

To define a generic function in Rust, you use angle brackets (`<` and `>`) to specify a type parameter, like this:

~~~{.rust caption="main.rs"}
fn print_type<T>(_arg: T) { 
    println!("Type is {}", std::any::type_name::<T>()); 
}
~~~

In this example, a function named `print_type` is defined so that it accepts a single argument, `T`. The `<T>` syntax indicates to Rust that `T` is a type parameter. The function then uses `std::any::type_name` to print the type's name.

You can call this function with any type:

~~~{.rust caption="main.rs"}
fn main() {
   print_type("hello"); // Type is &str 
   print_type(42); // Type is i32
   print_type(vec![1, 2, 3]); // Type is Vec<i32>
}
~~~

Here's the output:

~~~{ caption="Output"}
Type is &str
Type is i32
Type is alloc::vec::Vec<i32>
~~~

You can use this function to print the variable type at runtime, which can help with debugging or introspection.

### Generic Structs

A generic struct is a data structure that holds the values of different types. It works similarly to a generic function, using type parameters to allow flexibility in the values it can store.

To define a generic struct in Rust, you use the same syntax you use for a generic function:

~~~{.rust caption="main.rs"}
struct Circle<T> { 
      diameter: T, 
      height: T,
 }
~~~

Great, now a struct is defined and called `Circle` and has two fields: `diameter` and `height`, both of type `T`. Again, the `<T>` syntax is used to specify that `T` is a type parameter.

You can create instances of this struct with any type. It's useful when you want to define a data structure that can hold values of any type, such as a container or collection:

~~~{.rust caption="main.rs"}
fn main() {
  let object1 = Circle { diameter: 1, height: 2 }; 
  // diameter and height are both i32
  let object2 = Circle { diameter: 3.14, height: 2.71 }; 
  // diameter and height are both f64
  let object3 = Circle { diameter: "hello", height: "world" }; 
  // diameter and height are both &str
}
~~~

Great! Now you can use these instances with appropriate typings anywhere you need to within your code.

### Generic Enums

A generic enum is similar to a generic struct, but it allows multiple types with different variants. Each variant can have its own set of associated data of different types. To define a generic enum in Rust, you use the same syntax as for a generic function or struct. Here's an example:

~~~{.rust caption="main.rs"}
enum Result<T, E> { 
   Ok(T), 
   Err(E), 
}

fn main() {
  let result1: Result<i32, &str> = Result::Ok(42); 
  // Ok variant with i32
  let result2: Result<i32, &str> = Result::Err("error"); 
  // Err variant with &str
}
~~~

An enum called `Result` is defined above with two variants: `Ok` and `Err`. `Ok` takes a value of type `T`, while `Err` takes a value of type `E`. The `<T, E>` syntax specifies that both `T` and `E` are type parameters.

You can use this enum to represent the result of an operation that may either succeed (`Ok`) or fail (`Err`). The `T` type parameter represents the successful result, while the `E` type parameter represents the error:

This enum is useful when you want to handle errors in a type-safe way without resorting to error codes or exceptions.

### Traits and Generics

Traits in Rust are similar to interfaces in other languages, defining a set of methods that a type must implement. Traits can be used with generics to add constraints to the types a generic function, struct, or enum can operate on. They define a set of methods a type must implement to be considered compatible with the trait.

Here's an example:

~~~{.rust caption="main.rs"}
trait Printable {
    fn print(&self);
}
~~~

In this example, a trait called `printable` is created with a single method called `print`.

~~~{.rust caption="main.rs"}
struct Point<T: Printable, U: Printable> {
    x: T,
    y: U,
}
~~~

The trait is used to create a struct called `Point`, which takes two generic type parameters (*ie* `T` and `U`) that must implement `Printable`.

~~~{.rust caption="main.rs"}

impl<T: Printable, U: Printable> Point<T, U> {
    fn print(&self) {
        self.x.print();
        self.y.print();
    }
}

impl Printable for i32 {
    fn print(&self) {
        println!("i32: {}", self);
    }
}

impl Printable for &str {
    fn print(&self) {
        println!("&str: {}", self);
    }
}
~~~

Inside the `impl` block for `Point`, the `print` method is used to call the `print` methods on both the `x` and `y` fields. Finally, an instance of `Point` is created with an `i32` and a `&str` type that calls `print` based on the implementations of `Printable` on both types.

This allows printing values of `x` and `y` using their respective `Printable` implementations.

~~~{.rust caption="main.rs"}
fn main() {
  let p = Point { x: 42, y: "hello" };
  p.print();
}
~~~

Here's the output:

~~~{ caption="Output"}
i32: 42 &str: hello
~~~

This example demonstrates how traits can be used to constrain the types that a generic function or struct can work with while still allowing flexibility for a wide range of types.

## Advanced Topics

In addition to the basics of generics in Rust, several advanced topics are worth exploring. These include generic lifetimes, phantom types, and type-level programming.

### Generic Lifetimes

Lifetimes in Rust specify how long a variable's reference can remain active. This ensures that the reference remains valid for as long as it's being used.

Generic lifetimes allow a reference's lifetime to be parameterized by a generic type. This enables more flexible and expressive code that handles references of varying lifetimes. The following is an example:

~~~{.rust caption="main.rs"}
struct Foo<'a, T> {
    data: &'a T,
}

fn main() {
    let x = 42;
    let foo = Foo { data: &x };
    println!("{}", foo.data);
}
~~~

Output:

~~~{ caption="Output"}
42
~~~

In this code, a struct called `Foo` takes a lifetime parameter `'a` and a generic type parameter `T`. The `data` field is a reference to a value of type `T` with lifetime `'a`.

Inside the `main` function, an instance of `Foo` is created with a reference to `x`. Since `x` is a local variable, its lifetime is limited to the scope of the `main` function. By specifying the lifetime parameter `'a` in the definition of `Foo` ensures that the reference to `x` does not outlive its lifetime.

### Phantom Types

Phantom types don't have values and instead are used to enforce constraints on other types at compile time. They're often used in Rust for [drop-checking](https://doc.rust-lang.org/nomicon/dropck.html) and ensuring that certain types are used only in certain contexts or providing additional safety guarantees.

Here's an example of a phantom type:

~~~{.rust caption="main.rs"}
struct Secret<T> {
    data: String,
    phantom: std::marker::PhantomData<T>,
}

fn main() {
    let s = Secret::<String> {
        data: "secret data".to_string(),
        phantom: std::marker::PhantomData,
    };
    println!("{:?}", s.phantom);
}
~~~

In this example, a struct called `Secret` takes two fields: `data` and `phantom`, in which `data` is a `String` type, and `phantom` is a `PhatomData<T>` type. The `PhatomData<T>` type doesn't ‌ hold any data; by defining the `struct` with a type parameter `T` that must be a `String`, the Rust compiler can verify that any instance of the struct dropped at compile time includes one or more fields with a type of `String`.

Inside the main function, an instance of `Secret` is created with reference to the `String` type, which means that the `PhantomData` type field to be created in the struct would be a non-existent `String` type used at compile time and the data field of a `String` type. This is useful for [drop-checking](https://doc.rust-lang.org/nomicon/dropck.html).

### Type-Level Programming

Rust allows type-level computations through generic types and traits. With Rust's type system, you can use various type-level programming techniques, which involve using types and type-level computations to encode information in the type system. This can be used to ensure that certain properties hold for values of a certain type or to enforce constraints at compile time.

Type-level programming can be used for various purposes, from encoding protocols and data formats to ensuring that certain operations are performed in a specific order. The following is an example:

~~~{.rust caption="main.rs"}
trait Add<Rhs> {
    type Output;

    fn add(self, rhs: Rhs) -> Self::Output;
}

impl Add<u32> for u32 {
    type Output = u32;

    fn add(self, rhs: u32) -> Self::Output {
        self + rhs
    }
}
~~~

In this example, a trait called `Add` has a single associated type called `Output` and defines an implementation of `Add` for `u32`, which simply returns `u32`.

~~~{.rust caption="main.rs"}
impl<T, Rhs> Add<Rhs> for Option<T>
where
    T: Add<Rhs>,
    <T as Add<Rhs>>::Output: Clone,
{
    type Output = Option<<T as Add<Rhs>>::Output>;

    fn add(self, rhs: Rhs) -> Self::Output {
        match self {
            Some(x) => Some(x.add(rhs)),
            None => None,
        }
    }
}
~~~

An implementation of `Add` for `Option<T>` is also created, where `T` implements `Add<Rhs>` and `Output` is cloneable. Inside the `add` method, a pattern-matching match expression is used to handle the case where `self` is `Some` and adds the value of `rhs` to `x`. Otherwise, it returns `None`.

~~~{.rust caption="main.rs"}
fn main() {
    let x: Option<u32> = Some(42);
    let y: Option<u32> = None;
    let z = x.add(10);
    let w = y.add(10);
    println!("{:?} {:?}", z, w);
}
~~~

Here's the output:

~~~{ caption="Output"}
Some(52) None
~~~

Finally, two instances of `Option<u32>` are created and used to add 10 to each of them. When both results are printed, the result for `x` is `Some(52)` (because 42 + 10 = 52), while the result for `y` is `None` (because `None` does not have a value to `add`).

Type-level programming can be used for various purposes, including compile-time checks, optimizations, and even the creation of new types.

## Considerations When Using Generics

![Using]({{site.images}}{{page.slug}}/using.png)\

While generics can be a powerful tool for creating flexible and reusable code, there are some considerations to consider when using them.

### Strike a Balance between Generics and Concrete Types

One of the challenges of generics is finding the right balance between abstraction and concrete types. Too much abstraction can make your code difficult to understand and maintain, while too little can lead to code duplication and reduced flexibility.

When designing a generic function or type, it's imperative to consider the use cases and potential variations of the types involved. If only a few possible variations exist, using concrete types instead of generics is better. However, if there are a lot of possible or unknown variations, generics can provide valuable abstractions.

#### Code Readability and Maintainability

While generics can make your code more abstract and flexible, they can also make it harder to read and understand. Writing clear and concise documentation and using meaningful names for generic type parameters is important when using generics.

It's also important to consider the readability and maintainability of generic code. As with any code, it's important to follow best practices for formatting, commenting, and structuring it.

#### Performance Considerations

You need to know that generics can affect program performance. In some cases, generic code may be slower than concrete types. This is due to the additional indirection and type-checking required. Rust's type system is designed to minimize generic runtime overhead, and in many cases, generic code can be just as fast as concrete code.

When designing code that uses generics, it's critical to consider ‌performance implications. It's also important to test the code thoroughly to ensure it meets the required performance criteria.

## Conclusion

Generics are a powerful feature in Rust that helps create flexible and reusable code. By abstracting types, generics can make writing code that works with a wide range of input types easier without sacrificing performance or readability.

In this article, you learned about the basics of generics in Rust, including generic functions, structs, enums, and traits. You also learned about more advanced topics, including generic lifetimes, phantom types, and type-level programming.

You can learn more about Rust and generics by visiting the official [Rust documentation](https://doc.rust-lang.org/book/ch10-00-generics.html). Additionally, on the Rust website, you can find several Rust community resources, forums, and blogs that discuss Rust and its features, including generics, in more detail.

{% include_html cta/bottom-cta.html %}
