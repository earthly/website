---
title: "Rust Macros: Practical Examples and Best Practices"
categories:
  - Tutorials
toc: true
author: Aniket Bhattacharyea
editor: Bala Priya C

internal-links:
 - Rust Macros
 - Metaprogramming
 - Macro
 - Programming
 - Efficient
excerpt: This article explores the power of macros in Rust, providing practical examples and best practices for using them effectively. Whether you're new to macros or looking to enhance your understanding, this article will help you harness the full potential of macros in your Rust projects.
---

**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article presents practical examples for using macros in Rust. If you're interested in a different approach to building and packaging software then [check us out](/).**

In Rust, macros are pieces of code that generate other Rust code using a technique commonly known as [metaprogramming](https://en.wikipedia.org/wiki/Metaprogramming). A macro is expanded during compilation, and the output of a macro is inserted into the source code of the program.

The most famous example of a macro is `println!`. Even though it looks like a function and is used like a function, it's actually expanded during compilation, and the `println!` call is replaced with a more complex implementation code.

In this article, you'll see some practical examples of macros and learn some tips and tricks on how to best use them.

## Rust Macros Basics

![Macros]({{site.images}}{{page.slug}}/macro.png)\

<div class="notice--info">
This tutorial assumes familiarity with the basics of Rust programming.
</div>

In Rust, there are two types of macros: declarative and procedural. Take a look at each:

### Declarative Macros

Declarative macros are the simplest type of macro and are defined with the `macro-rules!` macro. They look and behave similarly to a `match` expression.

A `match` expression takes as input an expression and matches it with a set of predefined patterns and runs the corresponding code. Similarly, a declarative macro takes as input a piece of Rust source code, matches the source code with a set of predefined structures and, on successful match, replaces the code with the code associated with the matched pattern.

The following example shows a declarative macro in action:

~~~{.rust caption="declarative_macro.rs"}
//declarative_macro.rs

macro_rules! greetings {
    ($x: expr) => {
        println!("Hello, {}", $x);
    };
}

fn main() {
    greetings!("Earthly"); // Prints "Hello, Earthly"
}
~~~

Here, the macro is named `greetings` and is defined with `macro_rules!`. In the body of the macro, there is only one pattern: `($x: expr) => { ... }`. This pattern matches any Rust expression (denoted by the `expr` type) and stores it in a variable `$x`. Upon matching the pattern, the `$x` placeholder is replaced by the value of `4x` (in this case, `"Earthly"`), and the output of the macro becomes `println!("Hello, {}", "Earthly");`.

The input code is replaced by this resulting code during compilation, which means the line `greetings!("Earthly");` is turned into `println!("Hello, {}", "Earthly");` during compilation.

It's possible to have multiple patterns just like a `match` expression:

~~~{.rust caption="declarative_macro.rs"}
//declarative_macro.rs

macro_rules! greetings {
    (struct $x: ident {}) => {
        println!("Hello from struct {}", stringify!($x));
    };
    ($x: expr) => {
        println!("Hello, {}", $x);
    };
}

fn main() {
    greetings!("Earthly"); // Prints "Hello, Earthly"
    greetings! {
        struct G {} // Prints "Hello from struct G"
    };
}
~~~

In this example, another arm has been added in the `greetings` macro, which matches the code of the form `struct X {}` and replaces it with `println!("Hello from struct {}", "X");`. The `ident` type is used to indicate that `$x` is an identifier (name of the struct). For any other code, the other arm is matched just like it was in the previous example.

In addition, it's also possible to match repeated expressions using a special syntax:

~~~{.rust caption="declarative_macro.rs"}
//declarative_macro.rs

macro_rules! add {
    ($a:expr)=>{
        $a
    };
    ($a:expr,$b:expr)=>{
        $a+$b
    };
    ($a:expr,$($b:tt)*)=>{
        $a+add!($($b)*)
    }
}
~~~

The `add!` macro has three arms: the first arm matches a single expression and returns the same expression. The second arm matches two comma-separated expressions and returns their sum. In the third arm, the first input is matched to `$a`. The next one (or more input) is matched to `$b`, where the `*` denotes that the pattern should match zero or more occurrences of whatever precedes the `*`.

In the macro body, `add!` is used recursively to add the inputs in `$b`. Here, the `*` denotes that the code should be generated for each part that matches the `$()*` in the arm. This means that the macro call `add(1,2,3)` is expanded to `add(1, add(2,3))`, which is further expanded to `add(1, add(2, add(3)))` and finally becomes `1+2+3`.

<div class="notice--info">
Here, the type of `$b` is `tt`, which represents a token tree.
</div>

You've already seen the `expr` and `ident` types. Following are a few other types that you can use:

* **`item`**: an item; for example, a function or a struct
* **`block`**: a block of statements and/or an expression within braces
* **`stmt`**: a statement
* **`pat`** a pattern
* **`expr`**: an expression
* **`ty`**: a type
* **`ident`**: an identifier
* **`path`**: a path (*eg* `::foo::bar`)
* **`meta`**: a meta item that goes inside `#[...]` and `#![...]` attributes
* **`tt`**: a single token tree
* **`vis`**: a possibly empty [visibility qualifier](https://doc.rust-lang.org/reference/visibility-and-privacy.html) (*eg* `pub`)

You can find a full list of types in [The Rust Reference documentation](https://doc.rust-lang.org/reference/macros-by-example.html#metavariables).

Declarative macros are simple to write and utilize, but their functionality is limited to pattern matching and code replacement based on the macro input. They lack the capability to perform complex operations on the code.

<div class="notice--big--primary">
Keep in mind that when declaring a macro, you can't write the exclamation mark (`!`) after the macro name, but it's necessary when calling the macro.
</div>

### Procedural Macros

Procedural macros are a big step up from declarative macros. Like their declarative cousins, they get access to Rust code, but procedural macros can operate on the code (similar to a function) and produce new code.

A procedural macro is defined similarly to a function, and it receives one or two `TokenStream` as inputs and produces another `TokenStream`, which is then inserted into the source code by the compiler. A `TokenStream` is an abstract sequence of tokens that makes up the source code of the program. This means that a procedural macro can operate on the [abstract syntax tree (AST)](https://en.wikipedia.org/wiki/Abstract_syntax_tree) of the Rust source code, making it more flexible and powerful.

There are three types of procedural macros:

1. [Custom derive macro](https://doc.rust-lang.org/reference/procedural-macros.html#derive-macros)
2. [Attribute-like macro](https://doc.rust-lang.org/reference/procedural-macros.html#attribute-macros)
3. [Function-like macro](https://doc.rust-lang.org/reference/procedural-macros.html#function-like-procedural-macros)

Every procedural macro must be defined in its own crate, which needs to be added as a dependency to any project where the macro is used. For instance, the following must be added to the `Cargo.toml` file of the project where a procedural macro is defined:

~~~{ caption="Cargo.toml"}
[lib]
proc-macro = true
~~~

The macro is defined as a function with the `#[proc_macro_derive]`, `#[proc_macro_attribute]`, or `#[proc_macro]` attribute, depending on whether it's a derive macro, attribute-like macro, or a function-like macro.

In this article, you'll get a simple overview of the three types of procedural macros. For a step-by-step tutorial on writing these macros, you can refer to the [Rust docs](https://doc.rust-lang.org/reference/procedural-macros.html).

#### Derive Macros

A derive macro lets you create new inputs for the [`derive` attribute](https://doc.rust-lang.org/reference/attributes/derive.html), which can operate on structs, unions, and enums to create new items. The following example shows a derive macro that implements the `MyTrait` trait:

~~~{.rust caption="lib.rs"}
//macro_demo/macro_demo_derive/src/lib.rs

use proc_macro::TokenStream;
use quote::quote;
use syn;

/*
Definition of MyTrait:

pub trait MyTrait {
    fn hello();
}
*/

#[proc_macro_derive(MyMacro)]
pub fn my_macro_derive(input: TokenStream) -> TokenStream {
    let syn::DeriveInput { ident, .. } = syn::parse_macro_input!{input};

    let gen = quote! {
        impl MyTrait for #ident {
            fn hello() {
                println!("Hello from {}", stringify!(#ident));
            }
        }
    };
    gen.into()
}
~~~

Following are a few important things to note:

* The `#[proc_macro_derive(MyMacro)]` attribute denotes that the following function is a derive macro whose name is `MyMacro`.
* The function receives its input as a `TokenStream`.
* The `syn` crate is used to parse the input as a `DeriveInput` and extract the identifier of the item.
* The identifier name is used with a `#` symbol, which replaces it with the value of `ident`, courtesy of the `quote` crate.
* The `quote` crate is used to generate a `TokenStream` from the output code.

The macro can be used as follows:

~~~{.rust caption="main.rs"}
//procedural_macro/src/main.rs

#[derive(MyMacro)]
struct MyStruct;

fn main() {
    MyStruct::hello();
}
~~~

#### Attribute-Like Macros

An attribute-like macro defines a new [outer attribute](https://doc.rust-lang.org/reference/attributes.html) that can be attached to items, such as function definitions and struct definitions.

An attribute macro is defined with the `#[proc_macro_attribute]` and receives two `TokenStream` arguments. The first argument contains the inputs passed to the attribute macro, and the second, `TokenStream`, contains the item that it will operate on.

In the following example, a macro named `trace` has been defined, which operates on a function definition (denoted by the `ItemFn` type from the `syn` crate). It prints the name of the function and the arguments passed to the attribute and replaces the function definition with itself:

~~~{.rust caption="lib.rs"}
//macro_demo/macro_demo_derive/src/lib.rs

use proc_macro::TokenStream;
use quote::quote;
use syn::{parse_macro_input, ItemFn};

#[proc_macro_attribute]
pub fn trace(_attr: TokenStream, item: TokenStream) -> TokenStream {
    let input = parse_macro_input!(item as ItemFn);
    println!("{} defined", input.sig.ident);
    println!("Args received: {}", _attr.to_string());
    TokenStream::from(quote!(#input))
}
~~~

The macro can be used, as seen here:

~~~{.rust caption="main.rs"}
//procedural_macro/src/main.rs

#[trace]
fn foo() {}
/* Output:
foo defined
Args received:
*/

#[trace(some_arg)]
fn bar() {}
/* Output:
bar defined
Args received: some_arg
*/

#[trace(some_arg1, some_arg2)]
fn baz() {}
/* Output:
baz defined
Args received: some_arg1, some_arg2
*/
~~~

This prints the output as denoted in the comments. Note that because the macro is expanded during compilation and has no visible output (it leaves the function definition as is), you'll only see this output during compilation.

#### Function-Like Macros

Function-like macros are procedural macros that are invoked with the macro invocation operator (`!`). These are defined with the `#[proc_macro]` attribute and receive one `TokenStream` input, which is the code passed to the invocation of the macro. The entire macro invocation is replaced with the output of the macro.

The following example defines a function-like macro that simply prints its inputs and then replaces the macro invocation with a function definition:

~~~{.rust caption="lib.rs"}
//macro_demo/macro_demo_derive/src/lib.rs

use proc_macro::TokenStream;

#[proc_macro]
pub fn print_and_replace(input: TokenStream) -> TokenStream {
    println!("Inputs: {}", input.to_string());
    "fn add(a:i32, b:i32) -> i32 { a+ b }".parse().unwrap()
}
~~~

And this is how it can be used:

~~~{.rust caption="main.rs"}
//procedural_macro/src/main.rs

fn main() {
    print_and_replace!(100); // Output: "Inputs: 100"
    add(1,2); // Not an error as the macro call brings 'add' into scope
}
~~~

## Macro Hygiene

In the context of macros, hygiene refers to whether the macro is influenced by the external code surrounding it or not. A hygienic macro works in all contexts and is uninfluenced by the code around the invocation site.

In general, declarative macros are partially hygienic. A declarative macro is hygienic for local variables and labels but not for anything else. Consider the following example:

~~~{.rust caption="lib.rs"}
macro_rules! foo {
    ($x: expr) => {
        a + $x
    }
}
fn main() {
    let a = 42;
    println!("{}", foo!(5));
}
~~~

After macro expansion, the previous code should transform into the following:

~~~{.rust caption="lib.rs"}
fn main() {
    let a = 42;
    println!("{}", a + 5);
}
~~~

However, this code doesn't compile because the macro is hygienic and the definition of `a` outside the macro cannot be used by the macro.

In contrast, the following is a scenario where the macro is unhygienic:

~~~{.rust caption="lib.rs"}
//// Definitions in the `my_macro` crate.
#[macro_export]
macro_rules! foo {
    () => { bar!() }
}

#[macro_export]
macro_rules! bar {
    () => { () }
}

//// Usage in another crate.
use my_macro::foo;

fn unit() {
    foo!();
}
~~~

This code won't compile because `my_macro::bar` isn't imported when `foo` is called. This is a situation where the surrounding code (or lack thereof) affects the macro. A solution is to use `$crate::bar`:

~~~{.rust caption="lib.rs"}
macro_rules! foo {
    () => { {% raw %}${% endraw %}crate::bar{% raw %}!{% endraw %}() }
}
~~~

Procedural macros are always unhygienic. They behave as if they were written inline in place of the macro invocation and are, therefore, affected by surrounding code.

## Practical Examples of Macros

Now that you know how macros can be defined and used, you're ready to look at some real-life examples of macros. The following examples are all taken from popular crates to give you a feel of macros in the wild. All the example codes have been significantly simplified to help you follow along with ease.

### Loop Unrolling

It's possible to use declarative macros to implement simple loop unrolling using recursion. The following `unroll_loop` macro can unroll loops of up to four iterations:

~~~{.rust caption="lib.rs"}
{% raw %}
macro_rules! unroll_loop {
    (0, |$i:ident| $s:stmt) => {};
    (1, |$i:ident| $s:stmt) => {{ let $i: usize = 0; $s; }};
    (2, |$i:ident| $s:stmt) => {{ unroll!(1, |$i| $s); let $i: usize = 1; \
    $s; }};
    (3, |$i:ident| $s:stmt) => {{ unroll!(2, |$i| $s); let $i: usize = 2; \
    $s; }};
    (4, |$i:ident| $s:stmt) => {{ unroll!(3, |$i| $s); let $i: usize = 3; \
    $s; }};
    // ...
}

fn main() {
    unroll_loop!(3, |i| println!("i: {}", i));
}
{% endraw %}
~~~

Since a declarative macro is restricted by pattern matching and is unable to perform operations on its input, the `unroll_loop` macro is limited in the sense that it's not possible to dynamically set up the recursion. You must explicitly write the cases for every integer that you want to use as the index of the loop. The solution to this is to use a procedural macro, but for obvious reasons, that's more complex.

Here's a real-life example in the [seq-macro](https://crates.io/crates/seq-macro/) crate:

~~~{.rust caption="lib.rs"}
seq!(N in 0..=10 {
    println!("{}", N);
});
~~~

### JSON Parsing and Serialization

The [Serde JSON](https://github.com/serde-rs/json) crate uses a declarative macro `json` to parse and serialize a JSON. The `json` macro provides a familiar interface for creating JSON objects:

~~~{.rust caption="lib.rs"}
let user = json!({
    "id": 1,
    "name": "John Doe",
    "age": 42
});

println!("Name of user: {}", user["name"]);
~~~

`json` is a declarative macro that looks like this:

~~~{.rust caption="lib.rs"}
#[macro_export(local_inner_macros)]
macro_rules! json {
    // Hide distracting implementation details from the generated rustdoc.
    ($($json:tt)+) => {
        json_internal!($($json)+)
    };
}
~~~

`json` matches zero or more expressions of type `tt` (*ie* token tree) and calls the `json_internal` macro. The use of `local_inner_macro` automatically exports the inner `json_internal` macro so that it doesn't need to be explicitly imported at the invocation site. This is an alternative to using `$crate`, as explained previously in the section about hygiene.

The `json_internal` macro is where the magic happens. It's similar to the `add` macro you saw previously because it implements a TT muncher that produces a `vec![]` of the elements:

~~~{.rust caption="lib.rs"}
macro_rules! json_internal {
    ///////////////////////////////////////////////////////////
    // TT muncher for parsing the inside of an array [...]. \
    Produces a vec![...]
    // of the elements.
    //
    // Must be invoked as: json_internal!(@array [] $($tt)*)
    ///////////////////////////////////////////////////////////

    // Done with trailing comma.
    (@array [$($elems:expr,)*]) => {
        json_internal_vec![$($elems,)*]
    };

    // Done without trailing comma.
    (@array [$($elems:expr),*]) => {
        json_internal_vec![$($elems),*]
    };

    // Next element is `null`.
    (@array [$($elems:expr,)*] null $($rest:tt)*) => {
        json_internal!(@array [$($elems,)* json_internal!(null)] $($rest)*)
    };

    // Next element is `true`.
    (@array [$($elems:expr,)*] true $($rest:tt)*) => {
        json_internal!(@array [$($elems,)* json_internal!(true)] $($rest)*)
    };

    ...
}
~~~

For more details, check out the [source code](https://docs.rs/serde_json/1.0.96/src/serde_json/macros.rs.html#53-58).

### Server Route Creation

The popular [Rocket framework](https://github.com/SergioBenitez/Rocket) uses attribute-like procedural macros to create server routes. There are several macros that correspond to HTTP verbs, such as `get`, `post`, and `put`. You can use them with a function definition to annotate the function to be invoked when an HTTP request is made to that route:

~~~{.rust caption="lib.rs"}
#[get("/hello")]
fn hello() -> String {
    "Hello, World!"
}
~~~

The macros are defined using another helper macro—a declarative macro named [`route_attribute`](https://github.com/SergioBenitez/Rocket/blob/9b0564ed27f90686b333337d9f6ed76484a84b27/core/codegen/src/lib.rs#L95):

~~~{.rust caption="lib.rs"}
macro_rules! route_attribute {
    ($name:ident => $method:expr) => (
        #[proc_macro_attribute]
        pub fn $name(args: TokenStream, input: TokenStream) -> TokenStream {
            emit!(attribute::route::route_attribute($method, args, input))
        }
    )
}
~~~

The actual attributes are then defined as follows:

~~~{.rust caption="lib.rs"}
route_attribute!(route => None);
route_attribute!(get => Method::Get);
route_attribute!(put => Method::Put);
route_attribute!(post => Method::Post);
route_attribute!(delete => Method::Delete);
route_attribute!(head => Method::Head);
route_attribute!(patch => Method::Patch);
route_attribute!(options => Method::Options);
~~~

As an example, after the `route_attribute` macro is expanded, the `get` macro is defined like this:

~~~{.rust caption="lib.rs"}
#[proc_macro_attribute]
pub fn get(args: TokenStream, input: TokenStream) -> TokenStream {
    emit!(attribute::route::route_attribute(Method::Get, args, input))
}
~~~

[`emit`](https://github.com/SergioBenitez/Rocket/blob/9b0564ed27f90686b333337d9f6ed76484a84b27/core/codegen/src/lib.rs#L77) itself is a declarative macro that generates the final output:

~~~{.rust caption="lib.rs"}
macro_rules! emit {
    ($tokens:expr) => ({
        use devise::ext::SpanDiagnosticExt;

        let mut tokens = $tokens;
        if std::env::var_os("ROCKET_CODEGEN_DEBUG").is_some() {
            let debug_tokens = proc_macro2::Span::call_site()
                .note("emitting Rocket code generation debug output")
                .note(tokens.to_string())
                .emit_as_item_tokens();

            tokens.extend(debug_tokens);
        }

        tokens.into()
    })
}
~~~

### Custom Code Parsing

The [SQLx macro](https://github.com/launchbadge/sqlx) uses a combination of declarative and procedural macros to parse and verify SQL queries during compilation, as shown here:

~~~{.rust caption="lib.rs"}
let usernames = sqlx::query!(
        "
SELECT username
FROM users
GROUP BY country
WHERE country = ?
        ",
        country
    )
    .fetch_all(&pool)
    .await?;
~~~

The `query` macro is a declarative macro [defined in this link](https://github.com/launchbadge/sqlx/blob/4f1ac1d6060ee73edf83c8365fafb12df44deecc/src/macros/mod.rs#L305):

~~~{.rust caption="lib.rs"}
macro_rules! query (
    ($query:expr) => ({
        $crate::sqlx_macros::expand_query!(source = $query)
    });
    ($query:expr, $($args:tt)*) => ({
        $crate::sqlx_macros::expand_query!(source = $query, \
        args = [$($args)*])
    })
);
~~~

The `expand_query` macro is a function-like procedural macro [defined in this link](https://github.com/launchbadge/sqlx/blob/4f1ac1d6060ee73edf83c8365fafb12df44deecc/sqlx-macros/src/lib.rs#L7):

~~~{.rust caption="lib.rs"}
pub fn expand_query(input: TokenStream) -> TokenStream {
    let input = syn::parse_macro_input!(input as query::QueryMacroInput);

    match query::expand_input(input, FOSS_DRIVERS) {
        Ok(ts) => ts.into(),
        Err(e) => {
            if let Some(parse_err) = e.downcast_ref::<syn::Error>() {
                parse_err.to_compile_error().into()
            } else {
                let msg = e.to_string();
                quote!(::std::compile_error!(#msg)).into()
            }
        }
    }
}
~~~

## Tips for Using Macros Efficiently

![Tips]({{site.images}}{{page.slug}}/tips.png)\

It's essential to know how to use macros efficiently. To that end, the following tips can help.

### Know When to Use Macros vs. Functions

Although macros and functions behave similarly, macros are more powerful because they can generate Rust code. However, due to the power of macros, they're more difficult to write, read, and maintain than functions.

In addition, macros expand during compilation, resulting in an increase in the binary's size and compilation time. Therefore, it's necessary to exercise restraint when employing macros and only use them when functions fail to provide the solution you need.

Here are a few scenarios where macros may be preferred over functions:

* Creating a domain-specific language (DSL) that extends the syntax of Rust.
* Moving computation and checks to compile-time. For example, validating an SQL query during compilation so that there's no need to perform the check at runtime, thus reducing runtime overhead.
* Writing repetitive or boilerplate code. For instance, you can use a derive macro to auto-implement a trait so that you don't have to manually implement it.

### Make Sure Macros Are Readable and Maintainable

Since macros operate on Rust code, if you're not careful, they can be difficult to read and maintain. This is especially true for procedural macros since they're more complex.

Generous documentation is your friend here. You can also try to keep your macros simple by extracting the macro logic to a separate function or macro. The following example from the [Rust documentation](https://doc.rust-lang.org/book/ch19-06-macros.html) shows this in action:

~~~{.rust caption="lib.rs"}
#[proc_macro_derive(HelloMacro)]
pub fn hello_macro_derive(input: TokenStream) -> TokenStream {
    // Construct a representation of Rust code as a syntax tree
    // that we can manipulate
    let ast = syn::parse(input).unwrap();

    // Build the trait implementation
    impl_hello_macro(&ast)
}
~~~

Here, the actual implementation is extracted inside `impl_hello_macro`. This keeps the actual macro lean and simple.

### Handle Errors in Macro

Since macros are inherently complex, it's a good idea to provide thorough error messages that clearly indicate what went wrong and, if possible, how to fix it. To do so, you can use `panic` in a procedural macro:

~~~{.rust caption="lib.rs"}
#[proc_macro]
pub fn foo(tokens: TokenStream) -> TokenStream {
    panic!("Boom")
}
~~~

Or you can use the [`compile_error`](https://doc.rust-lang.org/stable/std/macro.compile_error.html) macro, which raises a compiler error:

~~~{.rust caption="lib.rs"}
macro_rules! give_me_foo_or_bar {
    (foo) => {};
    (bar) => {};
    ($x:ident) => {
        compile_error!("This macro only accepts `foo` or `bar`");
    }
}

give_me_foo_or_bar!(neither); // Error: \
"This macro only accepts `foo` or `bar`"
~~~

You can also use the [`proc_macro_error`](https://docs.rs/proc-macro-error/latest/proc_macro_error/) crate that provides a powerful API for handling errors in macros.

### Test Your Macros

Like any other unit of code, a macro needs to be thoroughly tested. However, the usual ways of testing don't apply to macros since they're expanded at compile-time.

To test your macros, the [enums](https://crates.io/crates/trybuild) crate can be used. This crate provides a `compile_fail` that expects a Rust file to fail to compile and also checks that the correct error message is printed. Another `pass` function is provided, which ensures a given Rust file compiles successfully.

You can use the crate as shown here:

~~~{.rust caption="lib.rs"}
#[test]
fn test_macro() {
    let t = trybuild::TestCases::new();
    t.compile_fail("tests/my_macro.rs");
}
~~~

Here, assume that `my_macro.rs` invokes some macro in an invalid way. The `trybuild` crate ensures that the erroneous invocation does not compile. If you have a file named `tests/my_macro.stderr`, it checks that the error message produced during compilation matches the content of this file.

## Conclusion

Macros are one of the most powerful features offered in Rust. The ability to manipulate and generate Rust code is unmatched in terms of making code simple and reducing runtime complexity.

In this article, you learned about two types of macros, declarative, and procedural, and the basic syntax to use them. You also saw some real-life examples of macros, and learned some tips to make sure you're using macros as efficiently as possible. All the code in this article can be found in [GitHub repo](https://github.com/heraldofsolace/rust-macros-demo).

If you're looking for more information about Rust macros, check out the [Rust docs](https://doc.rust-lang.org/book/ch19-06-macros.html). In addition, the e-book [*The Little Book of Rust Macros*](https://danielkeep.github.io/tlborm/book/README.html) has a thorough explanation of macros, and [this GitHub repo](https://github.com/thepacketgeek/rust-macros-demo) contains some practical examples.

{% include_html cta/bottom-cta.html %}
