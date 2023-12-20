---
title: "The Power of Single-Expression Functions"
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - just an example
---

In my mind, there a bunch of concepts related together in programming languages syntax that all work together to make code more readable and understandable and concise. But sometimes I see people who haven't worked with these ideas, and they find the whole thing confusing and decreasing readability, because it strays from the c family standard way of doing things.

I think though, that it is all just an issue of familarity and that once you get used to these ideas then you will want them in your language. They are implicit returns, if expressions and single expression functions.

But lets start with expressions:

## Expressions

In programming languages, you've got expressions and you've got statements. I'm going to cycle through some different programming languages in this article, but lets start with Rust:

Expressions:
```
x + 10
add(x, y) 
```

Statements:
```
let y = x + 10;
let z = add(x, y);
println!("Hello, Rust!");
```

You get the idea. Expressions evaluate to a value and statements are instructions that perform some action. They don't evaluate to a value.

## Implicit Returns

In C-like languages, you can return the value of an expression using the return keyword. There can be early returns, but usually you are returning in the last executed statement of the function.

```
int functionName(int p1, int p2) {
    return p1 + p2;
}
```

You can return statements, that just doesn't make sense.

```
int functionName(int p1, int parameter2) {
    int a; 
    return a = p1 + p2; //What??!
}
```

This may seem obvious but I'm going somewhere. Note that this often makes the return statement redundant. If a function has a return type then the last executed line in any branch must return a value of that type. So you can omit the return and get an implicit return.

Here is Ruby:
```
def add_numbers_explicit_return(a, b)
  return a + b
end

def add_numbers_implicit_return(a, b)
  a + b
end
```

Ruby is not exactly a C-like langauge. Instead of braces it uses a keyword like `def` to start a block of code and `end` to end things, but nevertheless, early returns work the same in it as in other languages that support it.

When you have branching this works as well, you just have implicit returns per branch:

```
def check_number(number)
  if number > 0
    "Positive"
  elsif number < 0
    "Negative"
  else
    "Zero"
  end
end

```
If you aren't used to this, you might not like it at first. You want things to be explicit but I think once you get used to it's very easy to read. 

You never have to have an explicit return statement unless you need to return early. And often with implicit returns you just write in a style that avoids early returns. 

So this c:

```const char* check_number(int number) {
    if (number > 0) {
        return "Positive";
    }
    if (number < 0) {
        return "Negative";
    }
    return "Zero";
}
```

Becomes this Rust:
```
fn check_number(number: i32) -> &'static str {
    if number > 0 {
        "Positive"
    } else if number < 0 {
        "Negative"
    } else {
        "Zero"
    }
}
```

Or this Kotlin:
```
fun checkNumber(number: Int): String {
  if (number > 0) {
      "Positive"
  } else if (number < 0) {
      "Negative"
  } else {
      "Zero"
  }
}
```

>> Side bar

For me personally, this transition to implicit returns felt like the change from `List<String> myList = new ArrayList<String>();` style in C# and Java to `var myList = new ArrayList<String>();`. At first it seemed wrong after years of doing things one way, but once I realized I was just typing and reading redundant information, it became natural.

I realize that readability is something that is hard to quatify and generally what's readable is what familar but I want to say that to once you are used to this implicit return stlye its as if not more readable then an early return style.

<< Side Bar

# If Expressions

Ok, once you have this idea that expressions return something, and you don't need returns because its implicit you have code like this in Kotlin:

```
fun checkNumber(number: Int): String {
  if (number > 0) {
      "Positive"
  } else if (number < 0) {
      "Negative"
  } else {
      "Zero"
  }
}

fun exclaimNumber(number: Int): String {
  s = checkNumber(number)
  return s+"!" 
}
```

That example is super contrived, but notice what happens if I inline `checkNumber` into `exclaimNumber`. All the sudden I need to declare a mutable string before my if.

```
fun checkNumber(number: Int): String {
  
}

fun exclaimNumber(number: Int): String {
  s = ""
  if (number > 0) {
      s = "Positive"
  } else if (number < 0) {
      s = "Negative"
  } else {
      s= "Zero"
  }
  return s+"!" 
}
```

Yuck, you need to transform your if so that each branch is a assignment statement and not a implicitly returned expression.

But, lightbulb moment, if the if above from our `checkNumber` had each branch implicitly returning an expression, then isn't the if really an expression itself?

```
fun exclaimNumber(number: Int): String {
  s = if (number > 0) {
      "Positive"
  } else if (number < 0) {
      "Negative"
  } else {
      "Zero"
  }
  return s+"!" 
}
```

And there you have if expressions. Turns out a special syntax isn't need for ternary operators if you can treat your if's as expressions. They are things that return values so lets treat them as such. 

I love this kind of stuff, the if/else control flow I already knew can work as a expression and simplify code without needing any new syntax, it just follows how assignment already works.

Some people don't like this and prefer ternary operators, but I honestly think and hope that it's just inertia and that simple readability that falls out of this expression focus continues to spread. ( But, I understand that readablity is highly subject and somewhat about familarity so I'm not holding my breath. )

These if expressions of course work in all the langauges we touched on so far.

Rust:
```
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
```
Ruby:
```
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

```

A natural question you might have after this is what about other control flow? Can a while be an expression? Can a switch case be an expression? Yes, yes, and yes! 

Here is a Rust match.

```
fn describe_number(number: i32) -> String {
    let description = match number {
        n if n > 0 => "Positive",
        n if n < 0 => "Negative",
        _ => "Zero"
    };

    format!("{}!", description)
}

```

But now, lets push thinking in expressions a bit further.

## Block Expressions & Single Expression Functions

Ok, here is where I feel like I'm going to start losing people. Like not conceptually, but aesthetically. I love how this simple idea can keep improving code. But I'll admit my sense of whether something is an improvement or not might diverge with others at this point. But lets do it.

Ok so these are expressions:
```
4
4+3
getError(x,y,z)
```
But so is this:
```
{
  val x = 3
  val y = 4
  x + y
}
```

That block statement can we used like any other expression. If can go in an if expression:
```
z = if (x)
{
  val x = 3
  val y = 4
  x + y
} else {
  5
}
```

It can be assigned to a variable. 

Scala
```
val result = {
  val x = 3
  val y = 4
  x + y
}
```

Rust:
```
let result = {
    let x = 3;
    let y = 4;
    x + y 
};
```

If fact, once you notice that a block can be an expression, then function declaration seems like just assigning an expression to function signature:

```
def x():
{
  val x = 3
  val y = 4
  x + y
}
```

And then you might be thinking well, ok, I can assign a block expression to a function signature then why can I assign any expression to a function signature and you can if your languages supports single expression functions:

Ruby does:
```
def double(x) = x * 2

def is_even?(num) = num.even?

def fahrenheit_to_celsius(fahrenheit) = (fahrenheit - 32) * 5.0 / 9.0
```

Kotlin and Scala do:
```
// Scala ( s/def/fun/ for Kotlin)
def double(x: Int): Int = x * 2
def isEven(num: Int): Boolean = num % 2 == 0
def fahrenheitToCelsius(fahrenheit: Double): Double = (fahrenheit - 32) * 5.0 / 9.0

```

I find this approach to be both beautiful and concise, as well as highly readable. It's interesting to note the similarity between the single-line and block definitions in function expressions, and the analogous distinction between single-statement and block-statement if constructs.

```
if (condition) doSomething()
```

```
if (condition) {
    doSomething()
    doSomethingElse()
}
```

The single expression function is a mirror of single statement if form. The single statement if of course is not liked by all. The complaint is that once you need to add a second statement you need to add braces and that is just exhausting work, error prone and therefore we should never use this form. 

Rust in fact, does not support the dropping of braces in an if and also does not have a single expression function declartion. On our bus to expression town, this is where Rust pulls the rope and gets off because in Rust you always need the braces.


```
fn double(x: i32) -> i32 {
    x * 2
}

fn is_even(num: i32) -> bool {
    num % 2 == 0
}

fn fahrenheit_to_celsius(fahrenheit: f64) -> f64 {
    (fahrenheit - 32.0) * 5.0 / 9.0
}
```
There is probably a certain practically to Rust saying, nah, function defs always look this one way.

But Ruby/Kotlin/ Scala with their mirroring the assignment syntax can push on because a single expression functions can of course be combined with an if expression or any other expression.

So that this:

```
def max(x : int, y : int){
  if (a > b){
    return a
  } else {
    return b
  }
}
```

Becomes the concise:

```
def max(x : int, y : int) = if (a > b) a else b
```

Or we can take this early return style:
```
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
```

And change it to use an if

```
fun categorizeTemperature(temp: Int): String = 
    if (temp < 0) "Freezing"
    else if (temp < 15) "Cold"
    else if (temp < 25) "Mild"
    else "Hot"
```
And then change that using Kotlin version of a switch, the when:

```
fun categorizeTemperature(temp: Int): String = 
    when {
        temp < 0 -> "Freezing"
        temp < 15 -> "Cold"
        temp < 25 -> "Mild"
        else -> "Hot"
    }
```
Or the Scala match:
```
def categorizeTemperature(temp: Int): String = temp match {
    case t if t < 0 => "Freezing"
    case t if t < 15 => "Cold"
    case t if t < 25 => "Mild"
    case _ => "Hot"
}
```

Practially speaking a single expression function that is a if or match or other control flow is probably pushing things a bit to far. The Rust approach of keeping braces works pretty well once the expression starts to allow branching. 

I think this Rust match expression code reads pretty well:

```
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
```
And this Kotlin if doesn't seem more verbose for having braces around it:
```
fun categorizeTemperature(temp: Int): String {
    if (temp < 0) "Freezing"
    else if (temp < 15) "Cold"
    else if (temp < 25) "Mild"
    else "Hot"
}
```

But isn't embracing expressions powerful! I wanted to show how these ideas all come together. It gets me excited that thinking carefully about some little distinctions in programming, expressions vs statments and what information can be inferred, can lead to such improved ergonomics and readability.

Of course, all these ideas are imports from fp land. But I like the idea that you can start with c type language and notice that the return keyword is often redundant and pull on that thread until you can assign expressions directly to function signatures.

I love that concepts in programming languages can be so well thought out and geneartive and recombinable. It makes me feel like I'm using a finely crafted tool where the how of how everything fits together has been deeply thought out.

Basically I'm just trying to write down something I find exciting about in programming languages and hopefully some people find it exciting too.

I get though that people disagree with me. My opinions here are – I'm sure – actively considered suspect by some core Earthly devs ( Hey Alex). But as they say, even though this is literally the Earthly corporate blog, opinions expressed are mine, and not those of my employer.
