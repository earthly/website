---
title: "The Power of Single-Expression Functions"
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - just an example
---
Langauages: Scala, Kotlin, Ruby, Rust and f#

In my mind, there a bunch of concepts related together in programming languages syntax that all work together to make code more readable and understandable and consise. But sometimes I see people who haven't worked with these ideas, and they find the whole thing confusing and decreasing readability, because it strays from the c family standard way of doing things.

I think though, that it is all just an issue of familarity and that once you get used to these ideas then you will want them in your language. They are implicit returns, if expressions and single expression functions.

But lets start with expressions:

## Expressions

In programming languages, you've got expressions and you've got statements. An expressions.

... examples


## Implicit Returns

In programming langauges that are old, you can return the value of an expression in the last statement of a function. ( fucntion / method  / proc / whatever ). Let's ignore early returns for now.

```
def x():
  return x
```

You can return statements, that just doesnt' make sense.

```
def x():
  return x = y + z //???
```

Note that this often makes the return statement redundant. If a function has return types and the last executed line in any branch must return those values. So you can omit the return and get an implicit return:

```
def x():
  x + y
```

When you have branching this works as well, you just have implicit returns per branch:

```
def x():
  if(bla):
    x
  else:
    y
```
If you aren't used to this, you might not like it at first. You want things to be explicit but I think once you get used to it's very easy to read. 

You almost never have an explicit return statement. That only happens if you need an early return and at least in some languages with impliciti returns early returns are a bit frowned upon. That's probably just style.

>> Side bar

For me personally, this transition to implicit returns (and the other changes coming) felt like the change from `List<String> myList = new ArrayList<String>();` style in C# and Java to `var myList = new ArrayList<String>();`. At first it seemed wrong and problematic after years of doing things one way, but once I realized I was just typing and reading redundant information, it became natural.

<< Side Bar

# If Expressions

Ok, once you have this idea that expressions return something, and you don't need returns because its implicit you have code like this:

```
def x():
  if(bla):
    x
  else:
    y

def y():
  z = x()
  z++
  ...
```

But what if you need to do all these in one function. That is you need to setup the values of x and then do something with them. Then you need to transform your if so that each branch is a assignment statement and not a implicitly returned expression.

```
val z = Int
if(bla):
    z = x
  else:
    z = y
z++
```

But, lightbulb moment, if the if above from our `x()` had each branch implicitly returning an expression, then isn't it really an expression itself? Supporting this is how we get if expressions:

```
val z = if(bla):
    z = x
  else:
    z = y
z++
```
And there you have if expressions. Turns out a special syntax isn't need for ternary operators if you can treat your if's as expressions. They are things that return values.

All this is great right? Some people don't like this and prefer explicit returns, early returns and ternary operators to all this, but I honestly think and hope that it's just inheria and that simple readability that falls out of this expression focus continues to spread. 

( A natural question you might have after this is what about other control flow? Can a while be an expression? Can a switch case be an expression? Yes, yes, and yes! But I"m not covering that, I want to more onward)

## Single Expression Functions

Ok, here is where I feel like I'm going to start losing people. Like not conceptually, but aesthetically. Because thinking in expressions can take you further and I love how this simple idea can keep improving code. But I'll admit my sense of whether something is an improvement or not might diverge with others at this point. But lets do it.

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

It can be assigned to a variable:

```
val result = {
  val x = 3
  val y = 4
  x + y
}
```

If fact, once you notice that a block can be an expression, then function declarion seems like just assigning an expression to signature:

```
def x():
{
  val x = 3
  val y = 4
  x + y
}
```

And then you might be thinking well why can I assign any expression to a function signature and you can! These are single expression functions


```
def x() = 5

def double(x : int) = x * x
```

How beatiful and how cool is that. And it works for any expressions. We can take this:

```
def max(x : int, y : int){
  if (a > b){
    return a
  } else {
    return b
  }
}
```
and express the idea more clearly, in a way that I find more readable:

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

And change it to this:
```
fun categorizeTemperature(temp: Int): String = 
    if (temp < 0) "Freezing"
    else if (temp < 15) "Cold"
    else if (temp < 25) "Mild"
    else "Hot"
```

Practially speaking a single expression function that is a if expression is probably not that common, but I wanted to show how these ideas all come together. And it gets me so excited that thinking carefully about some little distinction in programming lead to such nice ergonomics and improved readability. Of course, all these ideas are imports from fp land. But I like the idea that you can start with c type language and notice that returns are often redundant when you last statement is an expression and then go to control from being expression and then to actual function just being statments that assign expression to a signature. Of course, all that gloss over some of hte fine details, a function declartion might not actually be a statement that assigns an expression to a statement in any of the langauges shown, Scala, Kotlin, Rust or Ruby, but it certainly feels to me like fucntion declarations are statementy and I love that concepts in these lanagues are so geneartive and recombinatable. It makes me feel like I'm using a finely crafted tool where the how everything fits together has been deeply thought out. 

People disagree with me though. My opinions here are actively consider wrong and the opposite of progress by some core Earthly devs ( Hey Alex). But as they say, even though this is literally the Earthly corporate blog, opinions expressed are mine, and not those of my employer.


## Need to add
- problems with single expression functions
- 


https://chat.openai.com/c/0954b0da-6e7a-4fe5-8e75-eca0696c5182

https://chat.openai.com/c/e1883c40-b1d9-40fc-97f6-b59dfac18fa0
