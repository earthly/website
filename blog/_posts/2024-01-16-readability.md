---
title: "Put Your Best Title Here"
categories:
  - Articles
toc: true
author: Adam
sidebar:
  nav: "thoughts"
internal-links:
 - just an example
---

Thesis: Article: Adding new features removes boilerplate and helps with readabilty for experienced users.

There is a joke about readability that can't find, but I goes something like this:

f(x,y) -> Clear and straightforward - the hallmark of practical programming.
f x y -> Acceptable in shell scripting, but a bit odd.
(f x y) -> Impossibly enigmatic. Approach with caution!

I assume this joke was written by Lisp programmers upset that they loose so many programmers just to unfamilarity with reading s-expressions. But there is some truth to this right. Readability does have a lot to do with familarity and if you are familar with syntax that looks a certain way, then anything else can look foriegn.

But can we talk about readability outside of familarity? I think we can. Let's define readability like this:

Newcomers Readability: How quickly you can get up to speed reading a programming language. Related to how familar it is to what you know and also how many things it has.

Experienced Readability: How easy it is for someone experienced in the language to understand a piece of code by glancing at it. 

This means that you can't dismiss `(f x y)` style as less readable just because you aren't familar with it. Familarty with syntax is super unpleasant at first, but builds quickly. 

Ok, so what effects experienced readabilty. I think there is time to read a piece of code and understand what it does, and they related time to spot any problems.

So I think actually these two have pretty similar experienced readablity:

def max(x : int, y : int) = if (x > y) x else y

def max(x : int, y : int){
  if (x > y) { 
    return x;
    } else {
    return y;
    {
}

Because you read it quickly. An expericned developer can read an if statement as single block practically. The long version, from the perspective of the short version has a lot more boiler plate, brackets and returns, but you get used to reading those pretty quickly and you end up reading that the if statement of this size as a whole.

Maybe boilerplate even helps readiability. Soem may say that semicolons on the end of each statement are part of the pattern that let them quickly skim code. It might be stricthly speaking redundant but that aids readabilty in the same way redudancy in spoken langauge aids understanding. 


## consie != readabile
I think this is why concisness is not readability. 

This code:


```
x = 6 // picked by randon dice role
configuration = "salad" // important word 
```
has less characters then this:

```
x = 6                   // picked by random dice role
configuration = "salad" // important word 
```

But, while I'm not totally sure I want full ascii comments, but those lined up comments are nice and more readabilt for me. They show that we are in some sort of setup vars section.


I also think python does a good job, with significant whitespace. I think that makes writing a parser harder, but the redundancy removed by having the indents specify the rules is pretty nice. 

( One thing I miss with python thoough, is having brackets as little handles, being able to collapse to brackets, or mouse over a bracket and see the matching on the other side light up.  So what are those afforadances? They are redundancy that in some small way is helping me, although perhaps an IDE could over this affordes regarless of python by ataching them somewhere. )

## concise == readabilty

This :
```
if( x > 7){
  y' = 5
} elseif (x > 5) {
  y' = 4
} else {
  y = 3
}
```
vs 

```
y = if( x > 7){
  5
} elseif (x > 5) {
  4 
} else {
  3
}
```

There are some redudancies there, and because of that its possible to have errors. I guess I'm saying the boilerplate parts of code you do learn to skim over, but the result is that those parts can have bugs. Beter not to have them.

# cognitive load

Ok, so adding concepts, sytanic concepts to a language can make it harder to learn. It becomes less accessible and has more cognitive load for new users. But hopefully, it introduces more concise and expressive ways to do things, and this means the cognitive load for an experienced user is decreased. They have in their long term memory how if expressions work, and can read an if expressoin faster than if statements. 

There is a point about vim somewhere here. Vim is not accessible, but the concepts it has, the vim verbs, nouns and text objects are very powerful. They have a high weight to power ratio.

An important question is can the curve be flattened. When you add a feature to an language how much complexity does it bring? Is the language's core philosophy and design consistent with the addition of this feature? 

Is it make sense with the langauge or is the lanauge just a hodge podge of features. 

Here is some Java:

```
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
public class LambdaHelloWorld {
    public static void main(String[] args) {
        Greeter greeter = () -> System.out.println("Hello, world!");
        greeter.greet(); // Outputs: Hello, world!
    }
}

```


## Missteps - Perl 6

# Improvements constexp vs tempates

```
template<int radius>
struct CircleArea {
    static const double value;
};

template<int radius>
const double CircleArea<radius>::value = radius * radius * 3.14159;


int main() {
    const double area = CircleArea<5>::value; // Circle area for radius 5
    // ... use 'area' as needed ...
}

```

to: 
```
constexpr double square(double x) {
    return x * x;
}

constexpr double PI = 3.14159;
constexpr double circleArea(double radius) {
    return PI * square(radius); // Computed at compile time if radius is constant
}

constexpr double radius = 5.0;
constexpr double area = circleArea(radius); 
```

More Ideas:
Generics in Go
i++?
operator overloading?
val in c#, type inference in general

Misfeatures:

Python stuff:

https://chat.openai.com/c/4bb48ac2-3fc0-4e99-9710-c64220736baf


Go slices?
