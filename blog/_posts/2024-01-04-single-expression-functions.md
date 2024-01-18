---
title: "Rust, Ruby, and the Art of Implicit Returns"
categories:
  - Articles
toc: true
author: Adam
sidebar:
  nav: "thoughts"
internal-links:
 - expressions
 - if-expressions
excerpt: |
    This article explores the concept of implicit returns, if-expressions, match-expressions, and single-expression functions in programming languages like Rust, Ruby, Kotlin, and Scala, highlighting how they can enhance code readability and conciseness. The author demonstrates the use of these expression-based concepts and encourages readers to embrace the power of expressions in their code.
---
**This article delves into the specific aspects of expression-based programming. Earthly's compatibility expression based and statement based programming languages. [Learn more about Earthly](https://cloud.earthly.dev/login).**

If you are familiar with C-style programming languages, and ever touch Rust, Ruby, Kotlin, Scala, or even Julia there are some syntax and concepts that could initially appear confusing, unfamiliar, or unnecessary. I'm talking about implicit returns, if-expressions, match-expressions, and single-expression functions.

These expression-based concepts can significantly enhance code readability, clarity, and conciseness. If they aren't in your language today, they might be at some point.

For me personally, this transition to these expression forms feels like the change from `List<String> myList = new ArrayList<String>();` style in C# and Java to `var myList = new ArrayList<String>();`. At first, it seemed wrong because I had years of doing things one way, but once familiarity was built it seemed natural and correct.

But let me just show you some code. They all follow from a simple concept and fit together really nicely. And then you can decide for yourself what you think.

Lets start with expressions.

## From Statements to Values

In programming languages, you've got expressions and you've got statements. I'm going to cycle through some different programming languages in this article, but lets start with Rust:

~~~{.rust caption="Expressions (in Rust)"}
x + 10
add(x, y) 
~~~

~~~{.rust caption="Statements (in Rust)"}
let y = x + 10;
let z = add(x, y);
println!("Hello, Rust!");
~~~

You get the idea. Expressions evaluate to a value and statements are instructions that perform some action. They don't evaluate to a value.

## Implicit Returns

In C-like languages, you can return the value of an expression using the return keyword. There can be early returns, but usually you are returning in the last executed statement of the function.

~~~{.java caption="function in Java returning int"}
int sum(int p1, int p2) {
    return p1 + p2;
}
~~~

You can't return statements, that just doesn't make sense.

~~~{.java caption="Error: unexpected return value in Java"}
void printSum(int p1, int p2) {
    return System.out.println(p1 + p2);
}
~~~

This may seem obvious and contrived but I'm going somewhere. Note that if a function has a return type then the last executed line in any branch must return a value of that type. The return keyword itself is often redundant. So you can omit the return and get an implicit return.

Here is Ruby:

~~~{.ruby caption="Explicit Return (Ruby)"}
def add_numbers_explicit_return(a, b)
  return a + b
end
~~~

~~~{.ruby caption="Implicit Return (Ruby)"}
def add_numbers_implicit_return(a, b)
  a + b
end
~~~

Ruby is not exactly a C-like language. Instead of braces it uses a keyword like `def` to start a block of code and `end` to end things, but nevertheless, early returns work the same as in other languages that support it.

When you have branching this works as well, you just have implicit returns per branch:

~~~{.ruby caption="Implicit Return With Branches (Ruby)"}
def check_number(number)
  if number > 0
    "Positive"
  elsif number < 0
    "Negative"
  else
    "Zero"
  end
end

~~~

If you aren't used to this, you might not like it at first. You want things to be explicit but I think once you get used to it's very easy to read.

You never have to have an explicit return statement unless you need to return early. And often with implicit returns you just write in a style that avoids early returns.

So this c:

~~~{.c caption="Early Returns in C"}
const char* check_number(int number) {
    if (number > 0) {
        return "Positive";
    }
    if (number < 0) {
        return "Negative";
    }
    return "Zero";
}
~~~

Becomes this Rust:

~~~{.rust caption="Implicit Returns in Rust"}
fn check_number(number: i32) -> &'static str {
    if number > 0 {
        "Positive"
    } else if number < 0 {
        "Negative"
    } else {
        "Zero"
    }
}
~~~

Or this Kotlin[^1]:

~~~{.kotlin caption="Implicit Returns in Kotlin"}
fun checkNumber(number: Int): String =
  if (number > 0) {
      "Positive"
  } else if (number < 0) {
      "Negative"
  } else {
      "Zero"
  }
~~~

This reads better to my eyes. No reading redundant information. Each branch returns a value directly. No early exiting to trace. But let's keep going.

## If Expressions

Once you have this idea that expressions return something, and you don't need returns because its implicit you have code like this in Scala:

~~~{.scala caption="exclaiming in Scala"}
def checkNumber(number: Int): String = {
  if (number > 0) {
    "Positive"
  } else if (number < 0) {
    "Negative"
  } else {
    "Zero"
  }
}

def exclaimNumber(number: Int): String = {
  val s = checkNumber(number)
  s + "!"
}
~~~

That example is super contrived, but notice what happens if I inline `checkNumber` into `exclaimNumber`. All the sudden I need to declare a mutable string before my if.

~~~{.scala caption="inlined exclaiming in Scala"}
def exclaimNumber(number: Int): String = {
  var s = ""
  if (number > 0) {
    s = "Positive"
  } else if (number < 0) {
    s = "Negative"
  } else {
    s = "Zero"
  }
  s + "!"
}
~~~

Yuck, you need to transform your `if` so that each branch is a assignment statement and not a implicitly returned expression.

But, light-bulb moment: in the `if` above from our `checkNumber` each branch was implicitly returning an expression. So then isn't the `if` really an expression itself? Can't we then assign it to variable.

~~~{.scala caption="if expression in Scala"}
def exclaimNumber(number: Int): String = {
  val s = if (number > 0) {
      "Positive"
  } else if (number < 0) {
      "Negative"
  } else {
      "Zero"
  }
  s+"!" 
}
~~~

And there you have `if` expressions. Turns out a special syntax isn't need for ternary operators if you can treat your `if`s as expressions. They are things that return values so lets treat them as such.

I love this kind of stuff, the if/else control flow I already knew can work as a expression and simplify code without needing any new syntax, it just follows how assignment already works.

Some people prefer ternary operators, but I honestly hope that it's just inertia and that simple readability that falls out of this expression focus continues to spread. ( But, I understand that readability is highly subjective and somewhat about familiarity so I'm not holding my breath. )

These if expressions of course work in all the languages we touched on so far.

~~~{.rust caption="if expression in Rust"}
fn exclaim_number(number: i32) -> String {
    let s = if number > 0 {
        "Positive"
    } else if number < 0 {
        "Negative"
    } else {
        "Zero"
    };
    format!("{}!", s)
}
~~~

~~~{.ruby caption="if expression in Ruby"}
def exclaim_number(number)
  s = if number > 0
        "Positive"
      elsif number < 0
        "Negative"
      else
        "Zero"
      end
  "#{s}!"
end
~~~

A natural question you might have after this is what about other control flow? Can a switch be an expression? Yes it can!

~~~{.rust caption="match expression in Rust"}
fn describe_number(number: i32) -> String {
    let description = match number {
        n if n > 0 => "Positive",
        n if n < 0 => "Negative",
        _ => "Zero"
    };

    format!("{}!", description)
}

~~~

But now, lets push thinking in expressions a bit further.

## Block Expressions & Single Expression Functions

Ok, here is where I feel like I'm going to start losing people. Like not conceptually, but aesthetically. I love how this simple idea can keep improving code. But I'll admit my sense of whether something is an improvement or not might diverge with others at this point. But lets do it.

Ok so these are expressions:

~~~{.scala}
4
4+3
getError(x,y,z)
~~~

But so is this:

~~~{.scala caption="Block Expression"}
{
  val x = 3
  val y = 4
  x + y
}
~~~

That block expression can we used like any other expression. It can go in an if expression:

~~~{.scala caption="Scala standard if block"}
z = if (x)
{
  val x = 3
  val y = 4
  x + y
} else {
  5
}
~~~

But it can also be assigned to a variable.

~~~{.scala caption="Block expression assignment in Scala"}
val result = {
  val x = 3
  val y = 4
  x + y
}
~~~

~~~{.rust caption="Block expression assignment in Rust"}
let result = {
    let x = 3;
    let y = 4;
    x + y 
};
~~~

If fact, once you notice that a block can be an expression, then a function declaration starts to seem like just assigning an expression to function signature:

~~~{.scala }
def x(): // <- Function Signature = ...
{        // <- Block Expression Start
  val a = 3
  val b = 4
  a + b
}     // <- Block Expression End
~~~

And then you might be thinking well, ok, I can assign a block expression to a function signature then why can't I assign any expression to a function signature? Well you can if your languages supports single expression functions:

Ruby does:

~~~{.Ruby caption="single expression functions in Ruby"}
def double(x) = x * 2

def is_even?(num) = num.even?

def fahrenheit_to_celsius(fahrenheit) = (fahrenheit - 32) * 5.0 / 9.0
~~~

Kotlin and Scala do:

~~~{.scala caption="single expression functions in Scala And Kotlin"}
def double(x: Int): Int = x * 2
def isEven(num: Int): Boolean = num % 2 == 0
def fahrenheitToCelsius(fahrenheit: Double): Double = (fahrenheit - 32) * 5.0 / 9.0
// s/def/fun/ for Kotlin version
~~~

I find this approach to be both beautiful and concise, as well as highly readable. Some people do not though. Let's talk about that next.

### Ifs and Blocks

Note the similarity between the single-line and block definitions in function expressions, and the analogous distinction between single-statement and block-statement `if` constructs.

~~~
if (condition) doSomething()
~~~

~~~
if (condition) {
    doSomething()
    doSomethingElse()
}
~~~

The single expression function is a mirror of single statement `if` form. The single statement `if` of course is not liked by all. The complaint is that once you need to add a second statement you need to add braces and that is error prone and therefore we should never use this form.

Rust in fact, does not support the dropping of braces in an if. Even a one-line if statement needs braces.

~~~{.rust caption="single line if expression in Rust"}
let result = if condition { value_if_true } else { value_if_false };
~~~

Rust also does not have a single expression function declaration. On our bus to expression town, this is where Rust pulls the rope and gets off because in Rust you always need the braces.

~~~{.rust caption="Rust needs the braces"}
fn double(x: i32) -> i32 {
    x * 2
}

fn is_even(num: i32) -> bool {
    num % 2 == 0
}

fn fahrenheit_to_celsius(fahrenheit: f64) -> f64 {
    (fahrenheit - 32.0) * 5.0 / 9.0
}
~~~

There is a certain practically to Rust saying: "nah, function defs always look this one way".

But Ruby, Kotlin, Scala, and others by mirroring the assignment syntax can push on, because a single expression functions can of course be combined with an `if` expression or any other expression.

So that this:

~~~{.scala caption="Explicit Return Scala"}
def max(x : int, y : int){
  if (x > y){
    return x
  } else {
    return y
  }
}
~~~

Becomes the concise:

~~~{.scala caption="Single Expression Scala"}
def max(x : int, y : int) = if (x > y) x else y
~~~

Or we can take this early return style:

~~~{.kotlin caption="Early Return Kotlin"}
fun categorizeTemperature(temp: Int): String {
    if (temp < 0) {
        return "Freezing"
    }
    if (temp < 15) {
        return "Cold"
    }
    if (temp < 25) {
        return "Mild"
    }
    return "Hot"
}
~~~

And change it to use an if expression and a single expression style.

~~~{.kotlin caption="Single Expression Function in Kotlin"}
fun categorizeTemperature(temp: Int): String = 
    if (temp < 0) "Freezing"
    else if (temp < 15) "Cold"
    else if (temp < 25) "Mild"
    else "Hot"
~~~

And then change that using Kotlin version of a switch ( the `when`):

~~~{.kotlin caption="Single Expression When in Kotlin"}
fun categorizeTemperature(temp: Int): String = 
    when {
        temp < 0 -> "Freezing"
        temp < 15 -> "Cold"
        temp < 25 -> "Mild"
        else -> "Hot"
    }
~~~

Or the Scala `match`:

~~~{.scala caption="Single Expression Function in Scala"}
def categorizeTemperature(temp: Int): String = temp match {
    case t if t < 0 => "Freezing"
    case t if t < 15 => "Cold"
    case t if t < 25 => "Mild"
    case _ => "Hot"
}
~~~

Practically speaking a single expression function that is a `if` or `match` or other control flow is probably pushing things a bit to far. The Rust approach of keeping braces works pretty well once the expression starts to have branching.

For instance, I think this Rust match expression code reads pretty well:

~~~{.Rust caption="Match expression in Rust"}
enum TrafficLight {
    Red,
    Yellow,
    Green,
}

fn action_for_light(light: TrafficLight) -> &'static str {
    match light {
        TrafficLight::Red => "Stop",
        TrafficLight::Yellow => "Caution",
        TrafficLight::Green => "Go",
    }
}
~~~

So maybe these ideas work best when used with care, and not pushed all the way to the extremes, but embraced whole-heartedly and thoughtfully like Rust does.

( Of course, there are languages that take expressions much further. Maybe that will be my next post. But I think we've covered enough for now. )

## When Less Code Speaks More

Isn't embracing expressions powerful? I encourage you to dive into these languages, experiment with the code, and see for yourself the elegance and clarity that they can bring.

It excites me that thinking carefully about some little distinctions in programming can lead to improved ergonomics and readability. I like the idea that you can start with C-type language, notice that the return keyword is often redundant, and pull on that thread until you can assign expressions directly to function signatures.

I love that programming language concepts can be well thought out, generative, and combinable. It makes me feel like I'm using a finely crafted tool where how everything fits together has been deeply thought out.

<!-- markdownlint-disable MD036 -->
 [^1]:
  *Update: 2024-01-04 - I found some problems with a couple Kotlin examples and so changed them to Scala. Kotlin is not my strong suit. It turns out it only supports implicit returns with single expression functions and not block functions.*
