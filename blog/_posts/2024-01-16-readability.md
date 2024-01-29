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

I assume this joke was written by Lisp programmers upset that they lose so many programmers just because s-expressions can look odd to the unintiated. But there is some truth to this. Readability does have a lot to do with familarity and if you are familar with syntax that looks a certain way, then anything else can look foriegn.

But can we talk about readability outside of familarity? I think we can. Let's define readability like this:

Newcomers Readability: How quickly you can get up to speed reading a programming language. Related to how familar it is to what you know and also how many things it has.

Experienced Readability: How easy it is for someone very experienced in the language to understand a piece of code by glancing at it. 

You can't dismiss `(f x y)` style as less readable just because you aren't familar with it. Building familarty with syntax is super unpleasant at first, but it builds quickly. 

Ok, so what affects experienced readabilty? It's the time to read a piece of code, understand what it does, and spot any problems.

I think these two have pretty similar experienced readabilty:

def max1(x : int, y : int) = if (x > y) x else y

def max2(x : int, y : int){
  if (x > y) { 
    return x;
    } else {
    return y;
    }
}

These are written in two different styles and `max1` has a lot fewer characters then `max2` but if you are experienced with the style I think both are eqaully readable because you read it quickly. You can read an if statement as single block. The long version, from the perspective of the short version has a lot more boiler plate, brackets and returns, but you get used to reading those pretty quickly and you end up reading that the if statement of this size as a whole.

Maybe boilerplate even helps readability? Some may say that semicolons on the end of each statement are part of the pattern that let them quickly skim code, seperating statements from control flow. The semi-colons might be strictly speaking redundant but it could help some in the way redudancy in spoken langauge aids understanding. 

## Less Characters is Not More Readable

Here is two version of some code:

```
x = 6 // picked by random dice role
stop-word = "salad" // see pre-training data 
exponents = 10**6 // max solution space
```

```
x = 6                   // picked by random dice role
stop-word = "salad"     // see pre-training data 
exponents = 10**6       // max solution space
```

Version two has more characters, they are whitespace characters, but still strictly more characters. And those lined up comments make a list of declarations more readable for me. They show that we are in some sort of setup section.

But sometimes consiseness really does aid readability.

This :
```
if( x > 7){
  y = 5
} elseif (x > 5) {
  y = 4
} else {
  y' = 3
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

There are some redudancies in the first, and because of that its possible to have errors. The boilerplate parts of code without if expressions you do learn to skim over, but those parts can have bugs and hence the error in the first version. The slightly shorter expression based could has less room for error.

# Cognitive Load

Ok, so adding concepts to a language can make it harder to learn. It becomes less accessible to people not familar with those concepts. It has more cognitive load for new users. But hopefully, the new concepts introduces more concise and expressive ways to do things, and this means the cognitive load for an experienced user is decreased. They have in their long term memory how if expressions work, and can read an if expression faster than if statements. 

An important question is when you add a feature to an language how much complexity does it bring? Is the language's core philosophy and design consistent with the addition of this feature? 

# Idea - Start here
Todo: up to here
Does it make sense within the langauge or is the language just a hodge-podge of features. 

Here is some Java. The Java I learned in university was Java 1.something and the concepts behind Java were simple. "In Java, everything is a object". I mean, you had classes and abstract classes and interfaces but really objects were what we were supposed to focus on. So you'd :

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
```


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



