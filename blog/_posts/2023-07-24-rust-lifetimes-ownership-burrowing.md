---
title: "Rust Lifetimes: A Complete Guide to Ownership and Borrowing"
categories:
  - Tutorials
toc: true
author: Enoch Chejieh
editor: Mustapha Ahmad Ayodeji

internal-links:
 - guide to ownership and borrowing
 - rust lifetimes
 - ownership and borrowing
 - rust guide
excerpt: |
    This article provides a comprehensive guide to Rust lifetimes, explaining ownership and borrowing in the language. It covers the basics of lifetimes, borrowing and references, as well as advanced topics like lifetime subtyping and higher-ranked trait bounds.
last_modified_at: 2023-08-28
---
**This article explains Rust lifetimes, a key feature for ensuring memory safety. Earthly simplifies your build process with its robust tools. [Check it out](/).**

As a software developer, you're probably familiar with common memory-related bugs, such as [buffer overflows](https://en.wikipedia.org/wiki/Buffer_overflow), [use-after-free errors](https://encyclopedia.kaspersky.com/glossary/use-after-free/), and [data races](https://web.mit.edu/rust-lang_v1.25/arch/amd64_ubuntu1404/share/doc/rust/html/nomicon/races.html). These issues can cause a wide range of problems, including crashes, data corruption, and even security vulnerabilities.

Rust is a programming language that uses [ownership and borrowing](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html) to address memory management issues while prioritizing both performance and memory safety. The approach is based on the concept of [lifetimes](https://doc.rust-lang.org/rust-by-example/scope/lifetime.html), where the lifetime system tracks the lifespan of every value, ensuring that references do not outlive their intended lifetime and preventing issues, such as dangling pointers/references and memory leaks.

Unfortunately, Rust's lifetimes can be difficult to understand, but they're essential to Rust's design, and they enable you to write secure and high-performing code while avoiding common memory-related problems found in other languages. In this article, you'll learn all about lifetimes and the concepts of ownership, borrowing, and resource management in Rust.

## Borrowing and References in Rust

Rust's ownership system is a notable and distinctive feature that revolves around the concepts of ownership and borrowing, which allows developers to manage resources efficiently and safely. It's designed to prevent memory leaks, data races, and other common problems that occur in other programming languages.
Ownership refers to the idea that every value in Rust has a distinct owner. The owner is responsible for value deallocation when it goes out of scope. Rust enforces this ownership model to ensure that memory deallocation occurs automatically and reliably. By structuring ownership in this way, Rust eliminates explicit memory deallocation calls and prevents memory leaks at compile time.
In comparison, borrowing refers to borrowing a reference to a resource from its owner. References are a way to access a resource without taking ownership of it, which makes it possible to share the resource between different parts of the program.

To demonstrate how borrowing works, take a look at the following example:

~~~{.rust caption="how_borrowing_works.rs"}
fn main() {
  let a = 5;
  let b = &a;
  println!("{}", b); 
}
~~~

This is what your output should look like:

~~~{ caption="Output"}
5
~~~

In this example, `b` borrows from the value of `a`, the `&` symbol acts as a way to create a reference of `a` in memory that can be pointed to retrieve its value, and it makes use of an immutable reference to do so (more on this next).

### Immutable and Mutable References

There are two types of references in Rust: immutable and mutable.

Immutable references allow read-only access to a resource. Immutable references are created using the `&` symbol and can be created multiple times, which means that multiple parts of the program can access the same resource at the same time.

Say you have a vector of integers, and you want to print each element in the vector. You can create an immutable reference to the vector using the following code:

~~~{.rust caption="immutable_references.rs"}
fn main()
   let vec = vec![10, 11];
   for i in &vec {
      println!("{}", i);
   }
}
~~~

Your output would look like this:

~~~{ caption="Output"}
10 
11
~~~

In comparison, mutable references are created using the [`&mut`](https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html#mutable-references) symbol and allow read and write access to a resource. However, there can only be one mutable reference to a resource at any given time. This ensures that only one part of the program can modify the resource at a time, which prevents data races.

For example, suppose you have a mutable vector of integers, and you want to modify its first element. In that case, you can create a mutable reference to the vector using the following code:

~~~{.rust caption="mutable_references.rs"}
fn main() {
   let mut vec = vec![10, 11];
   let first = &mut vec[0];
   *first = 6;
   println!("{:?}", vec);
}
~~~

Here's the output:

~~~{ caption="Output"}
[6, 11]
~~~

In this example, you create a mutable reference to the first element of the vector using the `&mut` symbol. Then you modify the first element by dereferencing the reference using the `*` operator and set its value to `6`.

### Rules for Borrowing

While borrowing is a powerful feature in Rust, it comes with a set of rules that must be followed to ensure memory safety and avoid data races. These rules include the following:

1. Each resource can only have one mutable reference or any number of immutable references at a time.
2. References must always be valid, which means that the resource being referenced must remain in scope for the entire lifetime of the reference.
3. A mutable reference cannot exist at the same time as any other reference, mutable or immutable.

The Rust compiler enforces these rules at compile time, ensuring that your code is safe from data races and other memory-related bugs.

When you follow these rules, you'll be able to write safer and more efficient code that takes advantage of Rust's ownership system.

## Lifetimes

![Lifetimes]({{site.images}}{{page.slug}}/lifetimes.png)\

Lifetimes are a way of tracking the scope of a reference to an object in memory. In Rust, every value has one owner, and when the owner goes out of scope, the value is dropped, and its memory is freed. Lifetimes allow Rust to ensure that a reference to an object remains valid for as long as it's needed.

In Rust, lifetimes are denoted using the `'a` syntax, where the `'a` is a placeholder for the actual lifetime. The lifetime can be defined as a generic parameter in a [function](https://web.mit.edu/rust-lang_v1.25/arch/amd64_ubuntu1404/share/doc/rust/html/book/first-edition/functions.html), [struct](https://web.mit.edu/rust-lang_v1.25/arch/amd64_ubuntu1404/share/doc/rust/html/book/first-edition/structs.html), or [trait](https://web.mit.edu/rust-lang_v1.25/arch/amd64_ubuntu1404/share/doc/rust/html/book/first-edition/traits.html) using angle brackets. The following is an example:

~~~{.rust caption="basic_lifetime_example.rs"}
struct Path<'a> {
    point_x: &'a i32,
    point_y: &'a i32,
}

fn main() {
    let p_x = 3200;
    let p_y = (p_x / 2) as i32;
    let maze = Path { point_x: &p_x, point_y: &p_y };
    println!("x = {}, y = {}", maze.point_x, maze.point_y);
}
~~~

Your output would look like this:

~~~{ caption="Output"}
x = 3200, y = 1600
~~~

Here, a `struct Path` is defined with two fields: `point_x` and `point_y`, which references an `i32` type. The `i32` value (or type) represents a signed integer from the number -2147483648 to 2147483647. The lifetime `'a` specifies that the reference must live at least as long as the instance of the struct.

Now, take a look at this example which is similar to the code above but results in an error:

~~~{.rust caption="basic_lifetime_example.rs"}
    …
fn main() {
    let p_x = 3200;
    let p_y = {
        let temp = 42;
        &temp
    };
    let maze = Path { point_x: &p_x, point_y: p_y };
    println!("x = {}, y = {}", maze.point_x, maze.point_y);
}
~~~

Can you see the error? Your output will look like this:

~~~{ caption="Output"}
|
|     let p_y = {
|         --- borrow later stored here
|         let temp = 42;
|         &temp
|         ^^^^^ borrowed value does not live long enough
|     };
|     - `temp` dropped here while still borrowed
~~~

In this example, the compiler detects an error when the lifetime reference of `temp` goes out of scope. This error prevents the further use of `p_y` in the program because the value of `temp` has already been dropped. The issue arises because `p_y` is assigned a borrowed reference, `&temp`, which cannot exist outside the scope of `p_y`. This error occurs due to the mismatched lifetimes.

Take a look at a modified version of the previous code snippet:

~~~{.rust caption="basic_lifetime_example.rs"}
    …

fn main() {
    let p_x = 3200;
    let temp;
    let p_y = {
        temp = 42;
        &temp
    };
    let maze = Path { point_x: &p_x, point_y: p_y };
    println!("x = {}, y = {}", maze.point_x, maze.point_y);
}
~~~

As you can see, this approach works because `temp` and `p_y` have the same lifetime, allowing the `temp` variable to exist for the duration of the program. This means that the reference to `temp`, assigned to `p_y`, remains valid and can be used throughout the program.

### Lifetime Elision

Rust's [lifetime elision](https://doc.rust-lang.org/nomicon/lifetime-elision.html) rules allow the compiler to infer lifetimes in specific situations, which can reduce the amount of boilerplate code that is needed. The rules are based on the following three-lifetime elision principles:

1. Each parameter that is a reference gets its lifetime parameter. In other words, a function with one parameter of type `&T` would have a single lifetime parameter, such as `fn foo<'a>(x: &'a T)`.
2. If there is exactly one input lifetime parameter (*ie,* `&self`, `&mut self`, or `&`), that lifetime is assigned to all output lifetime parameters.
3. If there are multiple input lifetime parameters but one of them is `&self` or `&mut self`, the lifetime of `&self` or `&mut self` is assigned to all output lifetime parameters.

By following these rules, the Rust compiler can automatically infer the correct lifetimes in many cases, reducing the amount of lifetime annotation needed in the code.

> It's important to note that these rules are not exhaustive, and there may be cases where manual lifetime annotation is still required.

Here's an example of how the lifetime elision rules work:

~~~{.rust caption="lifetimes_elision.rs"}
#[derive(Debug)]
struct Num {
    x: i32,
}

impl Num {
    fn compare<'a>(&'a self, other: &'a Self) -> &'a Self {
        if self.x > other.x {
            self
        } else {
            other
        }
    }
}

fn main() {
    let num = Num { x: 3 };
    let other_num = &num;
    println!("{:?}", num.compare(other_num));
}
~~~

Here's the output:

~~~{ caption="Output"}
Num { x: 3 }
~~~

In this example, there is a struct (*, i.e.,* `Num`) that contains a single field called `x`. There's also an implementation block for `Num` that defines a method comparison. The compare method takes a reference to `self` and a reference to another `Num` instance (*i.e.,* `other`) and returns a reference to the `Num` instance with the higher `x` value.

The `compare` method above uses the third rule of the lifetime elision rules stated earlier. Applying these rules to the compare method:

- The input lifetimes are `&'a self` and `&'a Self`. Since one of them is &self, the lifetime of self ('a) is assigned to the output lifetime.
- The return type &'a Self uses the same lifetime 'a.
Therefore, the code benefits from lifetime elision by avoiding the need to explicitly annotate the lifetimes, making it more concise and readable.

Take a look at another similar example below:

~~~{.rust caption="lifetimes_elision.rs"}
impl Num {
    fn compare(&self, other: &Self) -> &Self {
        if self.x > other.x {
            self
        } else {
            other
        }
    }
}

fn main() {
    let num = Num { x: 3 };
    let other_num = &num;
    println!("{:?}", num.compare(other_num));
}
~~~

Notice the lifetime elisions removed from your `compare` function.

The code above results in the following error:

~~~{ caption="Output"}
| fn compare(&self, other: &Self) -> &Self {
| -----     -----
| |
| this parameter and the return type are declared with different lifetimes
...
| other
| ^^^^^ ...but data from `other` is returned here
error: aborting due to previous error
~~~

This error occurs because Rust fails to guarantee the lifetimes of `self` and `other` references in the `compare` method, which then results in a lifetime mismatch error from the compiler.

The key to understanding the lifetime elisions here is the lifetime parameter `'a` on the `compare` method. This parameter indicates that both the `self` and `other` references need to have the same lifetime `'a`. This is important because it allows the Rust compiler to automatically infer the lifetimes of these references rather than require explicit annotations.

### Lifetime Bounds and Constraints

Lifetime bounds and constraints are a way to limit the lifetime of a reference to a particular scope. This can be useful in situations where you need to ensure that a reference lives long enough to be used in a particular context but not longer than necessary.

#### Lifetime Bounds

A lifetime bound is a way to specify the minimum lifetime that a reference must have to be used in a particular context. For example, if you have a function that takes a reference to a value and returns a reference to that same value, you can use a lifetime bound to ensure that the returned reference is valid as long as the input reference.

Here's an example:

~~~{.rust caption="lifetime_bounds.rs"}
use std::fmt::Display;

#[derive(Debug)]
struct Movie<'a, T> {
    title: &'a str,
    rating: T,
}

impl<'a, T: 'a + Display + PartialOrd> Movie<'a, T> {
    fn new(title: &'a str, rating: T) -> Self {
        Movie {
            title,
            rating,
        }
    }
}

fn main() {
    let movie = Movie::new("The Shawshank Redemption", 9.3);
    println!("{:#?}", movie);
}
~~~

Your output would look like this:

~~~{ caption="Output"}
Movie {
     title: "The Shawshank Redemption",
     rating: 9.3,
}
~~~

Here, the `Movie` struct has two fields, and the `new` function takes two parameters: `title` and `rating`. Both of these need to have the same lifetime. The type `T` is a generic type that must implement both the `Display` and `PartialOrd` traits. Additionally, type `T` must have a lifetime long enough to persist in the program. This ensures that any type used to represent a rating satisfies the requirements `'a + Display + PartialOrd`.

The `'a` represents a sufficiently long lifetime, the `Display` trait ensures that the value being passed is printable, and the [`PartialOrd`](https://doc.rust-lang.org/std/cmp/trait.PartialOrd.html) trait ensures that the type should be able to be compared partially using operators like `<`, `>`, `>=`, or`<=`. Failing to meet these requirements would result in compile-time errors.

In the `main` function, a new `Movie` object is created with the title "The Shawshank Redemption" and a `rating` of `9.3`. Finally, the`printing` macro is used to print the `Movie` object using the `{:?}`  formatter.

Try changing the rating type value in the `Movie` instance being created in your main function:

~~~{.rust caption="lifetime_bounds.rs"}
fn main() {
    let movie = Movie::new("The Shawshank Redemption", [9.8]);
    println!("{:#?}", movie);
}
~~~

Notice the errors:

~~~{ caption="Output"}
| let movie = Movie::new("The Shawshank Redemption", 
&String::from("9.8"));
| ^|
| creates a temporary which is freed while still in use
| println!("{:#?}", movie);
| ----- borrow later used here
~~~

This creates a [dangling reference](https://en.wikipedia.org/wiki/Dangling_pointer) error; A dangling reference error occurs when a temporary value that is not assigned to any variable is borrowed as a reference to nothing and used. In this example, you are passing a borrowed `String` reference into the `new` function, which it's lifetime only lives as long as the `new` function and not the `Movie` instance itself, so even though the `String` type implements both bounds `Display` and `PartialOrd` it still fails due to this reason.

Now try the same example but assign the borrowed `String` reference to a variable.

~~~{.rust caption="lifetime_bounds.rs"}
fn main() {
  let string_ref = &String::from("9.8");
  let movie = Movie::new("The Shawshank Redemption", string_ref);
  println!("{:#?}", movie);
}
~~~

No errors! This is because the value now has a longer lifetime being assigned to a variable, so it can live as long as the current scope.

#### Lifetime Constraints

Lifetime constraints are similar to lifetime bounds, but they specify an upper bound on the lifetime of a reference instead of a lower bound. This can be useful in situations where you need to ensure that a reference does not live longer than necessary to avoid creating memory leaks.

Here's an example:

~~~{.rust caption="lifetime_constraints.rs"}
// Declare the Movie struct with a title and a rating
#[derive(Debug)]
struct Movie<'a> {
    title: &'a str,
    rating: u8,
}

// Declare the Reviewer struct with reference to a Movie and a name
#[derive(Debug)]
struct Reviewer<'a, 'b: 'a> {
    movie: &'a Movie<'b>,
    name: &'a str,
}

impl<'a, 'b> Reviewer<'a, 'b> {
    // Create a new review
    fn new(name: &'a str, movie: &'a Movie) -> Self {
        Reviewer { movie: movie, name: name }
    }
}

fn main() {
    // Create a movie instance
    let movie = Movie {
        title: "The Rust Movie",
        rating: 8,
    };


    // Print the review information
    println!("{:?}", Reviewer::print_review("Alice", &movie));
}
~~~

Notice the `new` function located in the implementation of the `Reviewer` struct? it takes in two(2) parameters, `name` and `movie.` The name is a `&str` string slice type, while the `movie` is a `Movie` struct. see the lifetime parameters defined on the Reviewer struct and its implementation. This defines and lets the compiler know the lifetimes it's working with at compile time.

The `Reviewer` struct `new` function parameters specify those lifetimes parameters as part of its arguments, which says that the `name` and `movie` parameters should have the same lifetimes in the function.

Now run your code.

~~~{ caption="Output"}
|
| fn new(name: &'a str, movie: &'a Movie) -> Self {
| --------- help: add explicit lifetime `'b` to the type of `movie`: \
`&'a Movie<'b>`
| Reviewer { movie: movie, name: name }
| ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ lifetime `'b` required
~~~

This code fails at compile time; why?

Notice the `Reviewer` struct defined in the code:

~~~{.rust caption="lifetime_constraints.rs"}
#[derive(Debug)]
struct Reviewer<'a, 'b: 'a> {
    movie: &'a Movie<'b>,
    name: &'a str,
}
~~~

It defines two lifetime parameters of `'a` and the other `'b`, which is a subtype of `'a`; more on Rust lifetime subtyping will be discussed further later in the article. This means that `'b` should outlive `'a` or at least as long as `'a` is valid, `'b` will also be valid at compile time. This makes the lifetime parameter `'b` an upper bound lifetime and `'a` a lower bound lifetime.

This creates a lifetime constraint on the field `movie` on the `Reviewer` struct.

The Reviewer struct has two(2) fields, `movie` and `name`. The `movie` field specifies the `'a` and `'b` lifetime parameters where `'a` specifies the lifetimes both field `movie` and `name` should have, while `'b` specifies that lifetimes the `Movie` struct possess must live as long or longer than the `Reviewer` struct.

This is useful to prevent the `Movie` instance passed to the new function from being dropped and leading to a dangling reference error.

Now to modify the `new` function a bit so the code stops throwing errors:

~~~{.rust caption="lifetime_constraints.rs"}
impl<'a, 'b> Reviewer<'a, 'b> {
    // Create a new review
    fn new(name: &'a str, movie: &'b Movie) -> Self {
         Reviewer {
             movie, 
             name
         }
    }
}
~~~

Here is the output:

~~~{ caption="Output"}
Reviewer { movie: Movie { title: "The Rust Movie", 
rating: 8 }, name: "Alice" }
~~~

Great! Now it works.

In this modification, the `name` reference has the lifetime `'a`, while the movie reference has the lifetime 'b. The lifetimes assigned to `name` and `movie` are independent and not necessarily the same and are not directly tied together in this case.

### Static Lifetime

The `'static` lifetime is a special lifetime that represents the entire duration of the program. Any reference with a `'static` lifetime can be used anywhere without worrying about its scope. Here's an example:

~~~{.rust caption="static_lifetime.rs"}
const SECRET_PHRASE: &'static str = "Hello, world!";
~~~

Here, a constant variable is created called `SECRET_PHRASE` with a `'static` lifetime, which means that it can be used anywhere in the program.

## Rust Lifetime Examples

To help solidify your understanding of the Rust lifetimes, explore practical examples where lifetimes are commonly used.

### Function Signatures With Lifetimes

[Function signatures](https://doc.rust-lang.org/book/ch10-01-syntax.html?highlight=generic) in Rust are one of the most common places you'll encounter lifetimes. In Rust, it's important to specify the lifetime of references passed as function arguments because the compiler needs to know how long a reference remains valid in order to ensure memory safety.

Take a look at an example:

~~~{.rust caption="function_signatures_with_lifetimes.rs"}
fn shortest_route<'a>(a: &'a i32, b: &'a i32) -> &'a i32 {
    if a > b {
        b
    } else {
        a
    }
}

fn main () {
  let a = 300000;
  let b = 100000;
  println!("{}km", shortest_route(&a, &b));
}
~~~

Here's the output:

~~~{ caption="Output"}
100000km
~~~

Here, a function called `shortest_route` is created that takes two signed integers (*ie* `&i32`) as arguments and returns the shortest route between the two distances. The `<'a>` syntax specifies that the lifetime `'a` is a generic lifetime parameter. This means that the function can take any two signed integer values with the same lifetime, and the return value has the same lifetime as the input slices.

### Structs With Lifetimes

Lifetimes are often used when defining [structs](https://doc.rust-lang.org/book/ch05-01-defining-structs.html) in Rust, particularly when a struct contains references to other values. Consider the following example:

~~~{.rust caption="structs_with_lifetimes.rs"}
struct ImportantExcerpt<'a> {
    part: &'a str,
}

impl<'a> ImportantExcerpt<'a> {
    fn new(part: &'a str) -> ImportantExcerpt<'a> {
        ImportantExcerpt { part }
    }

    fn announce_and_return_part(&self, announcement: &str) -> \
    &str {
        println!("Attention please: {}", announcement);
        self.part
    }
}

fn main() { 
  let novel = String::from("Call me Ishmael. Some years ago..."); 
  let first_sentence = \
  novel.split('.').next().expect("Could not find a '.'"); 
  let i = ImportantExcerpt::new(first_sentence); 
  println!("{}", i.announce_and_return_part("Hello, world!"));
}
~~~

Your output would be:

~~~{ caption="Output"}
Attention please: Hello, world!
Call me Ishmael
~~~

In this example, a struct `ImportantExcerpt` is created and contains a reference to a string slice. The lifetime `'a` is used to specify that the reference to the string slice must live at least as long as the struct instance. The `impl` block defines methods for the struct, including a constructor `new` and a method `announce_and_return_part` that returns the referenced string slice.

Here's another example using this same code above, but this code could lead to errors by just changing the values passed to the struct in the `main` function:

~~~{.rust caption="structs_with_lifetimes.rs"}
fn main() { 
  let novel = String::from("Call me Ishmael. Some years ago..."); 
  let first_sentence = \
  novel.split('.').next().expect("Could not find a '.'"); 
  let i = ImportantExcerpt::new(&first_sentence.to_string()); 
  println!("{}", i.announce_and_return_part("Hello, world!"));
}
~~~

The key difference between the two main functions is how the `ImportantExcerpt` struct references data. In the first function, it holds a reference to a string slice `(&str)`, while in the second function, it holds a reference to a String created using the `to_string()` method. This distinction has implications for the lifetime of the referenced data.

If the `ImportantExcerpt` struct were to hold a reference to a `String` with a shorter lifetime than the struct itself, it would result in a dangling reference error. However, Rust's compile-time checks prevent this error from occurring, which is shown below:

~~~{ caption="Output"}

|   let i = ImportantExcerpt::new(&first_sentence.to_string()); 
   |                                  ^^^^^^^^^^^^^^^^^^^^^^^^^^ - temporary value is freed at the end of this statement
   |                                  |
   |                                  creates a temporary which is freed while still in use
|   println!("{}", i.announce_and_return_part("Hello, world!"));
   |                  - borrow later used here
~~~

### Lifetimes in Trait Implementations

[Trait implementations](https://web.mit.edu/rust-lang_v1.25/arch/amd64_ubuntu1404/share/doc/rust/html/book/first-edition/traits.html) can also use lifetimes when dealing with references. Here's an example:

~~~{.rust caption="slifetimes_in_trait.rs"}
trait Summary<'a> {
    fn summarize(&'a self) -> String;
}

struct NewsArticle<'a> {
    headline: &'a str,
    location: &'a str,
    author: &'a str,
    content: &'a str,
}

impl<'a> Summary<'a> for NewsArticle<'a> {
    fn summarize(&'a self) -> String {
        format!("{} by {} ({})", self.headline, self.author, self.location)
    }
}

fn main() {
    let article = NewsArticle {
        headline: "A brand new world",
        location: "New York",
        author: "John Doe",
        content: "This is the content of the article",
    };

    println!("{}", article.summarize());
}
~~~

And here's the output:

~~~{ caption="Output"}
A brand new world by John Doe (New York)
~~~

In this code block, the `Summary` trait has a lifetime parameter `'a` that is used to define the lifetime of the reference in the `summarize` method. The `NewsArticle` struct also has a lifetime parameter `'a` that is used to define the lifetime of its fields. The implementation of the summary trait for the `NewsArticle` struct specifies that the `&self` reference has the same lifetime as the lifetime of the fields in the `NewsArticle` struct.

By using lifetimes in trait implementations, you can ensure that the lifetimes of references are properly managed and avoid any potential memory safety issues.

## Advanced Topics

![Advanced]({{site.images}}{{page.slug}}/level.png)\

In addition to the core concepts of Rust lifetimes, there are some advanced topics worth exploring. They include Lifetime Subtyping and Higher-Ranked trait bounds.

### Lifetime Subtyping

[Lifetime subtyping](https://doc.rust-lang.org/nomicon/subtyping.html) is a concept that allows lifetimes to be compared and ordered based on their relationship to one another. This can be useful when working with functions or data structures that require multiple lifetimes or when defining traits with lifetime constraints.

For example, imagine a function that takes two references with different lifetimes and returns a reference with a lifetime that is a sub-lifetime of both inputs. To demonstrate lifetime subtyping, this relationship can be expressed using the `'a` and `'b` lifetime parameters:

~~~{.rust caption="lifetime_subtyping.rs"}
fn lifetime_subtyping<'a, 'b: 'a>(x: &'a str, y: &'b str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

fn main() {
    let string1 = String::from("abcd");
    let string2 = "xyz";
    let result = lifetime_subtyping(string1.as_str(), string2);
    println!("The longest string is {}", result);
}
~~~

This is what your output would look like:

~~~{ caption="Output"}
The longest string is abcd
~~~

In this example, the returned reference has a lifetime of `'b`, which is a sub-lifetime of `'a`. This will ensure the `'b` lifetime reference outlives `'a`.

### Higher-Ranked Trait Bounds

[Higher-ranked trait bounds](https://doc.rust-lang.org/nomicon/hrtb.html) are a type of trait bound that allows a function or data structure to specify requirements on lifetimes that are not directly related to the input or output lifetimes. This can be useful when working with complex data structures or algorithms that require more fine-grained control over memory usage.

Consider the following example:

~~~{.rust caption="higher_rank_trait_bounds.rs"}
// Define a trait with a method that takes a closure with a \
// reference parameter.
trait RefProcessor {
    fn process_refs<F>(&self, f: F)
    where
        F: Fn(&i32);
}

// Implement the RefProcessor trait for a Vec<i32>.
impl RefProcessor for Vec<i32> {
    fn process_refs<F>(&self, f: F)
    where
        F: Fn(&i32),
    {
        for item in self {
            f(item);
        }
    }
}

// A function that takes a type implementing RefProcessor and a closure \
// with a generic lifetime.
fn process_all_items<T>(ref_processor: &T, \
closure: impl for<'a> Fn(&'a i32))
where
    T: RefProcessor,
{
    ref_processor.process_refs(closure);
}

fn main() {
    let numbers = vec![1, 2, 3, 4, 5];

    // Pass a closure that prints the square of each item.
    process_all_items(&numbers, |x| println!("{}", x * x));
}
~~~

Your output would look like this:

~~~{ caption="Output"}
1
4
9
16
25
~~~

Here, a trait called `RefProcessor` is defined with a method called `process_refs` that takes a closure with a reference parameter. The trait is implemented for the `Vec<i32>` type, and a function called `process_all_items` is created that accepts a type implementing `RefProcessor` and a closure with a generic lifetime. The higher-ranked trait bound is specified as `impl for<'a> Fn(&'a i32)` for the closure, indicating that the closure can work with references of any lifetime.

### Associated Types and Lifetimes

[Associated types and lifetimes](https://rust-lang.github.io/rfcs/1598-generic_associated_types.html#summary) can be used to enforce complex relationships between data structures and their associated lifetimes. Associated types are a way of associating a type with a trait, while lifetimes can be used to specify the scope in which a reference remains valid.

For example, imagine a trait that defines a method for iterating over a data structure. You might want to associate the type of the iterator with the trait while also specifying a lifetime for the reference to the data structure:

~~~{.rust caption="associated_types_and_lifetimes.rs"}
trait Iter<'a> {
    type Item;
    type Iter: Iterator<Item = Self::Item> + 'a;

    fn iter(&'a self) -> Self::Iter;
}
~~~

~~~{.rust caption="associated_types_and_lifetimes.rs"}
// using the Iter<'a> trait

struct List<T> {
    head: Link<T>,
}

type Link<T> = Option<Box<Node<T>>>;

struct Node<T> {
    elem: T,
    next: Link<T>,
}

impl<T> List<T> {
    fn new() -> Self {
        List { head: None }
    }
}

impl<'a, T: 'a> Iter<'a> for List<T> {
    type Item = &'a T;
    type Iter = ListIter<'a, T>;

    // Returns an iterator over the list.
    fn iter(&'a self) -> Self::Iter {
        ListIter { next: self.head.as_ref().map(|node| &**node) }
    }
}

struct ListIter<'a, T> {
    next: Option<&'a Node<T>>,
}

impl<'a, T> Iterator for ListIter<'a, T> {
    type Item = &'a T;

   // Returns a reference to the current item and moves the iterator \
   // to the next item.
    fn next(&mut self) -> Option<Self::Item> {
        match self.next {
            Some(node) => {
                self.next = node.next.as_ref().map(|node| &**node);
                Some(&node.elem)
            }
            None => None,
        }
    }
}

fn main() {
    let mut list = List::new();
    list.head = Some(Box::new(Node { elem: 1, next: None }));
    list.head = Some(Box::new(Node { elem: 2, next: list.head }));
    list.head = Some(Box::new(Node { elem: 3, next: list.head }));
    list.head = Some(Box::new(Node { elem: 4, next: list.head }));
    list.head = Some(Box::new(Node { elem: 5, next: list.head }));

    for i in list.iter() {
        println!("{}", i);
    }
}
~~~

Here's the output:

~~~{ caption="Output"}
5
4
3
2
1
~~~

In this example, the trait created is used to create an iterable list of nodes where the `type` keyword is used to define two associated types: `Item`, which represents the type of item returned by the iterator, and `Iter`, which represents the type of iterator itself. A lifetime parameter `'a` is also specified, which is used to ensure that the reference to the data structure remains valid for as long as the iterator is being used.

## Conclusion

Although Rust's approach to memory management through ownership and borrowing and its use of lifetimes to track references and prevent memory leaks can be challenging to understand, with practice and experience, you can master these concepts and become a proficient Rust developer.

In this article, you learned all about the basics of Rust lifetimes, including borrowing and references, lifetime syntax, and annotations. You also explored advanced topics, such as lifetime subtyping, higher-ranked trait bounds, and associated types and lifetimes. All the code samples for this tutorial are available in [this GitHub repo](https://github.com/ECJ222/rust-lifetimes).

With the information and examples provided here, you should have a solid understanding of Rust's lifetimes and their importance in writing safe and efficient code. If you want to keep learning, try exploring the [official Rust documentation and community resources](https://www.rust-lang.org/learn).

{% include_html cta/bottom-cta.html %}