---
title: "Experienced Readability"
categories:
  - Articles
toc: true
author: Adam
sidebar:
  nav: "thoughts"
---
There is a joke about readability that goes something like this:

f(x,y) -> Clear and straightforward - the hallmark of practical programming.
f x y -> Acceptable in shell scripting, but a bit odd.
(f x y) -> Impossibly enigmatic. Approach with caution!

I assume this joke was written by Lisp programmers upset that they lose so many programmers just because s-expressions can look odd to the uninitiated. But there is some truth to this. Readability does have a lot to do with familiarity and if you are familiar with syntax that looks a certain way, then anything else can look foriegn.

But can we talk about readability outside of familiarity? I think we can. [Last time] I mentioned that expert readability and begginer approachablity can sometimes be conflict and today I wanted to unpack that.

Let's define readability like this:

| Category                      | Description                                                                                                                                 |
|-------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| Newcomers Readability         | How quickly you can get up to speed reading a programming language. Related to how familiar you are with the syntax and concepts used. |
| Experienced Readability       | How quickly someone experienced in the language can understand a piece of code.                                |

So, with these definitions you can't dismiss `(f x y)` style as less readable just because you aren't familiar with it. What matters is how readable it is for experience LISPer. 

Somethings help both beginner and expert readbality but other things trade one off against the other. 

Let's start with the first.

## Structure

This may sound obvious but comptures dont 'really need structure, like function calls and modules and objects and so on. They just need on instruction after another to run. 

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

...

Something about reduce vs for each

or max vs manaul max




-----
Up To here

Ok, so what affects experienced readability? It's the time to read a piece of code, understand what it does, and spot any problems.

I think these two have pretty similar experienced readability:

```
def max1(x : int, y : int) = if (x > y) x else y

def max2(x : int, y : int){
  if (x > y) {
    return x;
    } else {
    return y;
    }
}
```

These are written in two different styles and `max1` has a lot fewer characters then `max2` but if you are experienced with the style both are equally readable. You read an if statement as single block. The long version, from the perspective of the short version has a lot more boiler plate, brackets and returns, but you get used to reading those pretty quickly and you end up reading it as a whole.

Maybe boilerplate and formatting even helps readability? The layout of version two may make it easier to scan. Some may even say that semicolons on the end of each statement are part of the pattern that let them quickly skim code, separating statements from control flow. The semi-colons might be strictly speaking redundant but it could help some in the way. Redundancy in spoken language aids understanding.

## ASCII Art and You

In structure helps scanning and improves experienced readability then code comments and whitespace are really where we can highlight structure. Here is two version of some code:

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

Version two has more characters. They are whitespace characters, but still strictly more characters. For me, those lined up comments make a list of declarations more readable. They show that we are in some sort of setup section, and the lines are more related.

Jimmy Koppel makes a [pretty good argument](https://www.pathsensitive.com/2023/12/should-you-split-that-file.html) that comments providing structure should be taken further. We should using code comments to provide structure in large files and that this aids readability by reducing cognitive load.

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
All of that, reminds me of the regions the were common with C# code and I did find that they aided readability.

```
#region MyRegion

your code here

#EndRegion
```
Todo: insert picture

Ok, so using comments and whitespace can help with expert readability. But also conciseness also helps with expert readability but at the cost of approachability.


Here is some code from my previous article:

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

    if pos < neg { //Bug 
        return pos
    } else {
        return neg
    }
}
~~~

What this does is fairly evident. It counts positive and negative numbers in a list and then returns the count of whichever is larger. I'm pretty sure even those who aren't familar with go can understand this code. But readability is not just about getting the gist of code, its also about easy it is to spot errors reading code. And there are a couple of places in this code where off by one errors can hide. 

Compare with this Scala code:

```
def maximumCount(nums : Array[Int]) : Int = 
  max(nums.count(_ < 0), nums.count(_ > 0))
```

Or this C# version:

```
def maximumCount(int[] nums) {
  return Math.Max(
    nums.Count(x => x < 0),
    nums.Count(x => x > 0)
  );
} 
```

There is just fewer places for bugs to hide in those versions. You not going to accidentally flip the sign and get min instead of max. (A bug in the go verision). And that drastically improves expert readablity. 

The slightly shorter expression based could has less room for error.



## Cognitive Load

Ok, so adding concepts to a language can make it harder to learn. It becomes less accessible to people not familiar with those concepts. It has more cognitive load for new users. But hopefully, the new concepts introduces more concise and expressive ways to do things, and this means the cognitive load for an experienced user is decreased. They have in their long term memory how if expressions work, and can read an if expression faster than if statements.

An important question is when you add a feature to an language how much complexity does it bring? Is the language's core philosophy and design consistent with the addition of this feature?

## Idea - Start Here

Todo: up to here
Does it make sense within the language or is the language just a hodge-podge of features.

Here is some Java. The Java I learned in university was Java 1.something and the concepts behind Java were simple. "In Java, everything is a object". I mean, you had classes and abstract classes and interfaces but really objects were what we were supposed to focus on. So you'd :

~~~
@FunctionalInterface
interface Greeter {
    void greet();
}

public class HelloWorld {
    public static void main(String[] args) {
        Greeter greeter = new Greeter() {
            @Override
            public void greet() {
                System.out.println("Hello, world!");
            }
        };
        greeter.greet(); // Outputs: Hello, world!
    }
}
~~~

public class LambdaHelloWorld {
    public static void main(String[] args) {
        Greeter greeter = () -> System.out.println("Hello, world!");
        greeter.greet(); // Outputs: Hello, world!
    }
}

~~~


## Missteps - Perl 6

# Improvements constexp vs tempates

~~~

template<int radius>
struct CircleArea {
    static const double value;
};

template<int radius>
const double CircleArea<radius>::value = radius *radius* 3.14159;

int main() {
    const double area = CircleArea<5>::value; // Circle area for radius 5
    // ... use 'area' as needed ...
}

~~~

to: 
~~~

constexpr double square(double x) {
    return x * x;
}

constexpr double PI = 3.14159;
constexpr double circleArea(double radius) {
    return PI * square(radius); // Computed at compile time if radius is constant
}

constexpr double radius = 5.0;
constexpr double area = circleArea(radius);

~~~

More Ideas:
Generics in Go
i++?
operator overloading?
val in c#, type inference in general

Misfeatures:

Python stuff:

https://chat.openai.com/c/4bb48ac2-3fc0-4e99-9710-c64220736baf

## Warts
Scala tuples
Go slices?
kotlin implict returns
other?

## The Hoang FActor

You can combine a bunch of stuff into a format that seems readable to those familar but some will refuse or maybe just not be able to climb the path to understanding that code.

Some people will just not make this jump, into prod code that combines a bunch of things.


Then, past this path, you have complex code uses a bunch of things together.

This can be for two reasons:
Expressivness Win
- The problem is complex, and the expressivness of the langauge is letting us susscintly explain the problem. So it takes a bit to get up to speed with what we are doing but once you do, you'll see how we are doing things falls out of the problem at hand.


Cleverness Masterbation / Larping as PL Researcher
- The problem at hand is normal and could be solved in 1000 lines of python, but with my cleverness and adding constraints (hey, lets solve the whole class of problems this one belongs to, and this solution is just a specific instance) to the problem I can solve it in a fun way using the langauge.

Thoughts on Cleverness:

So when people complain about the readablity of something and they aren't talking about action at a distance problems like come_from or monkey patching, too much global state then probably they are talking about verbosity or code that is too clever by half. The thing is, verbosity can be spotted without familiaryt, perhaps even better then with it. Because with time, you learn to ignore the boilerplate. But when the complaint is about overly clever code then everything is very murky. Maybe what you are looking at is an idea that is very well encapsulated in the expressiveness of the languauge. A solution with just ifs and elses would be so verbose as to be difficult to hold in your head, while using chunkier building blocks the idea is clear.  

But perhaps the complex code is the opposite. Maybe its a simple problem, expressed in a complex way, to entertain, to keep things interesting. Maybe shakespear if he made a cookbook would write them as sonnets. And sonnet fans would love it, but for the rest of us, we'd just be confused. A dram of milk and a peck of salt, a grain of isinglass might sound great, but struggling to get the recipe make.


## But its complex
Here why its confusing. If you know all the intricate features of a langauge, then of course given a solution you might reach for solving it using those things. And it might not be apparent that that makes new-comers struggle, it s jsut the obvisou way to structure the solution. It's the curse of knowledge. And so certainly some are just having new tools in the langauge nad want to use them, there is a crazy Scala version of this, there must have been crazy template version of this and every lanague that gets rich enough has people and groups that go through a maxmialist phase but this doesn't mean the things being used to build this maximilist vision are wrong. Just some constraint and empath is need. And from the other side, maybe don't just give up and say smething is werid because it has more expressivity or whatever then you are used to. The thing you think is werid is often not, its just foreigh. If you're going to spend your career doing this, it makes sense to keep learning. To use lanaguge that allow experts to cleanly solve problems. 

## Conclusion: I don't know
Ok, so what about the other side of features. Does something that move boilerplate make readablity worse when abused? 

Like here is some crazy list comprehensions...

And here is strange things you can do with if expressions.

But now here is also some crazy ifs

And some crazy while non-sense...


So, yeah, new syntax can make things denser and people can write horrible code in it. Is that worse then people writing horible code in other simpler constructus? I don't know.. 

Maybe more syntaxtic constructs means the very worse code can be worse indeed. One thing that I think is more revelant is when there are so many ways to do things that you can be experiecned in a langauge, but not in the style being used in something. It muddies the water that languages that support the most styles also seem to hav the most constructs. Scala here.

The problem in that case, is you become experienced enough to read a style of C++ or Scala but then another style yoy are still a beginniner. Frameworks make this worse, operatator overloading, which can be very handy, makes this worse.  
