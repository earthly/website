---
title: "The Two Types of Readable Code"
categories:
  - Articles
toc: true
author: Adam
sidebar:
  nav: "thoughts"
---
There is a joke about readability that goes something like this:

```
f(x,y) -> Clear and straightforward - the hallmark of practical programming.
f x y -> Acceptable in shell scripting, but a bit odd.
(f x y) -> Impossibly enigmatic. Approach with caution!
```

I assume this joke was written by Lisp programmers upset that they lose so many programmers just because s-expressions can look odd to the uninitiated. But there is some truth to this. Readability does have a lot to do with familiarity and if you are familiar with syntax that looks a certain way, then anything else can look foriegn.

But can we talk about readability outside of familiarity? I think we can. [Last time](/blog/showboaters) I mentioned that expert readability and begginer approachablity can sometimes be conflict and today I wanted to unpack that.

Readability of programming languages can vary, influenced by factors such as syntax complexity, standard library design, and the presence of advanced programming constructs. **These factors all effect beginners and language experts differently and that's what I want to share. There are two types of Readability.**

Let's define readability like this:

| Category                      | Description                                                                                                                                 |
|-------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| Newcomers Readability         | How quickly you can get up to speed reading a programming language. Related to how familiar you are with the syntax and concepts used. |
| Experienced Readability       | How quickly someone experienced in the language can understand a piece of code.                                |

So, with these definitions you can't dismiss `(f x y)` style as less readable just because you aren't familiar with it. What matters is how readable it is for experience LISPer. 

Somethings help both beginner and expert readbality but other things trade one off against the other. 

Let's start with the first.

## Structure

This may sound obvious but comptures don't really need structure, like function calls and modules and objects and so on. They just need on instruction after another to run. 

In 2004ish, at my first software developer job I got introduced to a large DBASE program that had no structure at all below the file level. Each file was just start executing at the top and well that's about it. 100s of files that looked like this.

```
CLEAR
DO WHILE .T.
    @ 0,0 CLEAR TO 0,79
    @ 0,0 SAY "Main Menu"
    @ 1,0 SAY "1. View Records"
    @ 2,0 SAY "2. Add Record"
    @ 3,0 SAY "3. Exit"
    @ 5,0 SAY "Select an option: "
    ACCEPT "> " TO nChoice
    CLEAR

    IF nChoice = 1
        DO viewrec.prg
    ELSE IF nChoice = 2
        DO addrec.prg
    ELSE IF nChoice = 3
        EXIT
    ELSE
        @ 8,0 SAY "Invalid option, please try again."
        WAIT
    ENDIF
ENDDO

```

Because that experience its pretty clear to me that being able to break things down into functions or procedures or whatever is super valuable. If some init fucntion is 150 lines long and does three distinct things, encapsulating those three things into seperate functions that init calls is a big win. I think this is uncontroversial though like any good idea it can be taken three steps to far.  

There are other types of structure though. 

### ASCII Art and You

If structure helps scanning and improves readability for all then code comments and whitespace another obvious way we can highlight structure. Here are two version of some code:

~~~
x = 6 // picked by random dice role
stop-word = "salad" // see pre-training data 
exponents = 10**6 // max solution space
~~~

~~~
x = 6                   // picked by random dice role
stop-word = "salad"     // see pre-training data 
exponents = 10**6       // max solution space
~~~

For me, those lined up comments make a list of declarations more readable. They show that we are in some sort of setup section, and that the lines are related to each other.

Another obvious but somtimes missed way to provide structure is just simple line breaks. 

```
package main

import (
    "fmt"
    "slices"
)

func main() {

    strs := []string{"c", "a", "b"}
    slices.Sort(strs)
    fmt.Println("Strings:", strs)

    ints := []int{7, 2, 4}
    slices.Sort(ints)
    fmt.Println("Ints:   ", ints)
}
```

The blank line, much like a paragraph break in writing helps group related things and break up unrelated.

Jimmy Koppel makes a [pretty good argument](https://www.pathsensitive.com/2023/12/should-you-split-that-file.html) that structure should be taken further. We should using code comments and whitespace to provide structure in large files and that this aids readability by reducing cognitive load.

You see this often in CSS:

```
/*******************************
             Types
*******************************/

/*-------------------
       Animated
--------------------*/


/* Horizontal */
.ui.animated.button .visible.content,
.ui.animated.button .hidden.content {
  transition: right @animationDuration @animationEasing 0s;
}
...

/* Vertical */
.ui.vertical.animated.button .visible.content,
.ui.vertical.animated.button .hidden.content {
  transition: top @animationDuration @animationEasing, transform @animationDuration @animationEasing;
}
...

/*-------------------
       Inverted
--------------------*/

.ui.inverted.button {
  box-shadow: 0px 0px 0px @invertedBorderSize @white inset !important;
  background: transparent none;
  color: @white;
  text-shadow: none !important;
}

```

All of that, reminds me of the regions that were common with C# code and I did find that they aided readability in large files.

```
#region MyRegion

your code here

#EndRegion
```
Todo: insert picture

All of this, of course, can be over used and abused. ( Your 4000 line C# class file is probably easier to understand with regions but maybe it shouldn't be 4000 lines. ) But still, well used, adding structure to code with whitespace and comments only helps readabilty when things start to get hairy. 


## Less To Go Wrong

Another way to improve readbility is to strictly just have less that can go wrong. A for each can't have a off by one error, so if I replace a for i loop with a for each, I no longer have to worry about my indexes being off.

Even if somewhere that for each has an implementation that may use indexes, I can just assume it works correctly and move my thinking to a higher level. You can only hold so many things in working memory at a time, so off loading some of this helps.

~~~{.go caption="Code Report: Count Max"}
func maximumCount(nums []int) int {
    var pos, neg int = 0, 0
    for _, e := range nums {
        if e > 0 {
            pos++
        } else if e < 0 {
            neg++
        }
    }
+    return max(pos,neg)
-    if pos > neg {
-        return pos
-    } else {
-        return neg-    }
}
~~~
<figcaption>Having a `max` to call is handy. It communicates intent for the reader, improving readability in a small way.[^1]</figcaption>

The neat thing about max, is that using it doesn't hurt begineer readability. Everyone knows what it means to get the maximum of two numbers. But if we keep building up helpful standard libraries and langauge features, we quickly start adding to the number of things a beginner has to learn.

```
let numbers = [1, 2, 3, 4]

//Original 
var sum1 = 0
for number in numbers {
    sum1 += number
}

//Improved
let sum2 = numbers.reduce(0, +)

```

Reduce is super handy and this is where readability of an expert can really grow I think. If you're going to spend years working in a programming langauge, learning the idioms is a small cost to pay to improve day to day readability, because you are using higher level concepts.

filter and map also benefit expert readablity.


```
const numbers = [1, 2, 3, 4, 5, 6];
let evensSquares1 = [];
for (let i = 0; i < numbers.length; i++) {
    if (numbers[i] % 2 === 0) {
        evensSquares1.push(numbers[i] * numbers[i]);
    }
}

const evensSquares2 = numbers.filter(number => number % 2 === 0)
                             .map(number => number * number);
```

Flatmap is super useful:
```
val sentences = List("Hello world", "Functional programming in Scala")

val splitSentences = sentences.map(_.split(" "))
val words1 = splitSentences.flatten()

val words2 = sentences.flatMap(_.split(" "))
```

While simplifications like using `reduce` or `filter` and `map` chains indeed elevate the level of abstraction and reduce error-prone boilerplate, they also encapsulate complexity that might not be immediately apparent to beginners. Each of these higher-order functions embodies a concept that, while straightforward for an experienced developer, adds to the list of things a newcomer must learn and understand before they can fully appreciate the readability improvements these abstractions offer.

I guess what I'm saying is higher order functions are valuable for the expert but a barrier for the newcomers. And its not just higher-order functions. They are one class of a concept, you can learn, that can let you write code at a very slightly higher level. You can elide over some of the details.

Other concepts do the same thing, like pattern matching, like Sum types, like Gererics, like polymorphic traits.

All these things, if they are used to more consisely express the concept at hand ( and not for showboating) can improve expert readability at the cost of beginner readability.

| Readability Enhancers    | Definition                                                                                     | Effects on Beginners                         | Effects on Experts                           |
|--------------------------|------------------------------------------------------------------------------------------------|---------------------------------------------|---------------------------------------------|
| Structural Enhancements  | Use of functions, whitespace, comments and even comment headings to visually structure code.                        | Makes code more navigable and understandable; helps in grouping related logic. | Aids in quick navigation and understanding of code structure; reduces cognitive load. |
| Simplification Techniques| Utilizing constructs that reduce error likelihood and leveraging built-in functions for common tasks. | Simplifies understanding of code by reducing complexity; minimizes common errors. May harm readability depending on specific familiarity. | Streamlines code, making it easier to read and maintain; promotes use of concise, expressive constructs. |
| Advanced Language Features | Employing higher-order functions, pattern matching, and other expressive language features.   | Increases complexity and learning curve due to more concepts to grasp. | Enhances expressiveness and conciseness; allows for more sophisticated abstractions and clearer intent. |

So which column do you care the most about? What trade off to choose?

Earlier I showed refactoring some go code to call `max`. But actually go doesn't have a way to get the max of some ints in the standard libraray. So I'd have to implement the max function myself, which takes away some of the benefit and I assume Rob Pike would rather I just use the if x > y else logic that I started with. That's because, in my view, go chooses beginner readablity over expert readablity. If you've not programminged in go yet, well there are very few concepts you aren't already familar with. And that is a legit choice to choose beginner readablity and simplicity. Clearly go has been wildly successful at gain adoption in the 'cloud native', network services world.

Rust, makes the opposite choice. And not because of the borrow checker vs Go GC, but because of the trait system, the sum types, the structural pattern matching, the const generics, the procedural macros and so on. Also a totally legit choice to choose to be a more complex expert tool.

Myself, I think expert readablity is more important. In the future I hope we are building up more higher level concepts that allow us to write better code.

It's crucial, however, to acknowledge the balance that must be struck. Complex features can make the initial learning curve steeper for beginners. Higher-order functions, pattern matching, and other sophisticated constructs are additional layers to learn, which can be daunting for those new to programming or a particular language.

But expert readabiity matters. There will always be a need for simple languages but we should be optimizing for experienced users being able to understand code quickly because it precicley communicates it's intent and to do that we need to be able to have building blocks larger than ifs and for loops.
