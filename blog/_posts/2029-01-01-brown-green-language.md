---
title: "Brown Vs Green Programming Languages"
author: Adam
tags:
- news
categories:
  - Articles
author: Adam
---
## Introduction
The Stack Overflow Developer Survey[^1] results are a great source of information about developers and how we work.  A favorite question of mine is the **Dreaded Programming Languages** question which asks what langauge you are currently using that you no longer wish to keep using. This question is paired with the **Most Loved Programming Langauge** question which is a langauge you are currently using that you want to keep using.

The results are interesting because they current usage: if people are honest, there should be no I-heard-kotlin-is-cool effect, where people rank highly things they don't actually use because they heard it is the new hottness.  The inverse should also be true: People who put something on the **Dreaded** list are actually using it. They are not dreading c++ because they heard its complex, but because they have to work in a C++ codebase and feel a real pain.

<div class="notice--warning" markdown="1">
**The TOP 15 Dreaded Programming Languages:**

VBA, Objective-C, Perl, Assembly, C, PHP, Ruby, C++, Java, R, Haskell, Scala, HTML, Shell, and SQL. 
</div>


<div class="notice--success" markdown="1">
**The TOP 15 Loved Programming Languages:**

Rust, TypeScript, Python, Kotlin, Go, Julia, Dart, C#, Swift, JavaScript, SQL, Shell, HTML, Scala, and Haskell.
</div>


The great thing about lists like this is that everyone can see what they want in the list and use it to rationilze their own favorite tools.  With Scala on the dreaded list, I can tell myself that that is probably just data engineering / Spark people throwing off the numbers.  If you are a fan of static types or intepreted languages or OO or FP, you can cherry pick things from this list to support your view.  But there actually is a pattern in this list.  Can you see what it is?

## Code Written Before I was Hired Is the Worst

Old code is the worst.  Find me a file in a code base that has been under active development for more than 3 years and it will be hard to follow.  What started out as a simple rule will develop special cases, and performance optimzations and configuration options.  Real world code evolves to fits its niche and as it does so it becomes more complex and harder to quickly understand.  The reason for this is simple, but the only person who has extensively written about this that I know of is Joel Spolsky. 

> The reason that [ developers ] think the old code is a mess is because of a cardinal, fundamental law of programming: **It’s harder to read code than to write it.**

Let's call this Joel's Law. Joel's thinks a lot of a lot of things follow from this premise.  Why do most developers think the code they inherited is a mess and want to throw it out and start again? It's because writing something new is cognitively less demaning than starting from scratch. Why are many rewrites doomed to fail? Because on completion the rewritten version is going to be just as hard to read as the original version.

![Scott Adams Understood]({{site.images}}{{page.slug}}/dt140812.gif)

Its easy to build up an understanding of code as you write it, but its hard to build up an understanding of code by reading it.  If you return to code you wrote and think its garbadge it could be because you have grown as a developer but it also could be because you have just forgotten how it works and are intepreting the pain of reading as a code quality problem. PR Reviews are a read only activity and hard if you don't already have a working model of the code in your head.


<<tangent about types and tests>>

## Brown Languages

Another thing that follows from this is that languages that you have to read existing code in a lot will seem worse than and the langauges where you mainly write code : software maintenace is less fun than a greenfield rewrite.  I think this effect is actually stronger than the pros and cons of various languages in many cases, and I think this is actually what the survey question is measuring: dreaded langauges are likely to be those used in existing brown field projects and loved langauges are those being used in realiveily new projects.  Lets measure this. [^2]

The Tiobe index claims to measure the "the number of skilled engineers, courses and jobs worldwide" for programming languages. There are probably some problems with how they measure this, but its accurate enough for our purposes.  The top 20 programming languages on their list as of are: Java, C, C++, C#, Python, VB .Net, PHP, JavaScript, Pascal, Swift, Perl, Ruby, Assembly, R, VB, Objective-C, Go, MATLAB, SQL, Scratch.  Some of these top 20 are strange, Scratch is unlikely to have many engineers, and some notable items are missing, but with some slight normalization[^3] we can use this as our brown language list.


<div class="notice--warning">
**Brown Langauage:** A language that you are more likely to use in existing software maintanence (ie. brown field projects).
TIOBE 2017 Brown Languages: Java, C, C++, C#, Python, PHP, JavaScript, Swift, Perl, Ruby, Assembly, R, Objective-C, Go, SQL 
</div>

<div class="notice--success">
**Green Langauage:** A language that you are more likely to use in a new project (ie. green field projects).
TIOBE 2017 Green Languages: Rust, TypeScript, Kotlin, Julia, Dart, Scala, Haskell
</div>

There is obviously lots of nuance that a list green/ brown split misses - I expect that more green field projects start with Swift than with ObjectiveC, but its not a bad split. There are also more Brown langauges in this list than green, but there is also a lot more existing code out there than is built each years, so :shrug:.  

Now we can answer the question: Do people love and dread these languages or are they really just dreading legacy code, regardless of langauge.

## The Dreaded Brown

``` matplotlib
import matplotlib.pyplot as plt

labels = 'Brown', 'Green'
dreaded_sizes = [10, 2]
dreaded_total = 12
loved_sizes = [6, 7]
loved_total = 13
explode = (0.1, 0)
colors = ["burlywood", "green"]

# Graph one
fig = plt.figure()
ax1 = fig.add_axes([0, 0, .5, .5], aspect=1)
ax1.set_title('Dreaded Languages')
ax1.pie(dreaded_sizes, explode=explode, labels=labels, 
        autopct=lambda p: '{:.0f}'.format(p * dreaded_total / 100),
        shadow=True, 
        startangle=90, 
        colors=colors)
ax1.axis('equal') 

```
<figcaption>
Dreaded Langauges 83% Brown
</figcaption>
</div>

In the top 15 almost all are brown languages. 15 of the 22 langauges in our list are brown, so this is higher than we would expect by chance.  

## Dreaded Outliers?
Haskell and Scala are the only two green languages in the list.  Does this mean they are most dreaded for the qualities of the language alone or is this just noise?  I'm not sure. The people dreading Scala and Haskell are either working on an existing code base, in which case its a brown langauge to them, or they are working on a new project and its not going well. Probably its some of both. They aren't exactly new langauges so its very possible people are being asked to maintain codes bases long after the languages experts have left. Both langauges have a reputation for complexity: does that make the maintance burden particularly acute? It's probably just noise based on my somewhat arbitrary dividing line, but I'd love to hear from you if you are a dreaded outlier.

## The Loved Greens
``` matplotlib
import matplotlib.pyplot as plt

labels = 'Brown', 'Green'
dreaded_sizes = [10, 2]
loved_sizes = [6, 7]
explode = (0.1, 0)
colors = ["burlywood", "green"]
total = 12

fig = plt.figure()

# Graph two
ax2 = fig.add_axes([.5, .0, .5, .5], aspect=1)
ax2.set_title('Loved Languages')
ax2.pie(loved_sizes, explode=explode, labels=labels, 
        autopct=lambda p: '{:.0f}'.format(p * total / 100),
        shadow=True, 
        startangle=90, 
        colors=colors)
ax2.axis('equal') 

```
<figcaption>
Loved Langauges 54% Green
</figcaption>

In the top 15 loved langauges 54% are green. 15 of the 22 langauges in our list are brown, so this is much higher than we would expect by chance.  This seems to confirm my hypothesis: the languages people love are languages that are too new to have giant big ball of mud projects.  Rust and Kotlin are still in the honeymoon phase.  I think Kotlin and Rust are big step forward from Java and C++, but peoples love for working in Kotlin and Rust maybe have as much to do with not having to work in 20 year old code bases than that the code bases are written in Kotlin and Java.

## Scala And Haskell Again
Scala and Haskell are ...

## The Loved Outliers
The most interesting category of 
Python
Go
C#
Swift
JavaScript
SQL



## methodolgy explained


To Do:
 * check what happens if go back further in tiobe
 * find what SO questions were


## References
 * [How Tiobe is measured](https://www.tiobe.com/tiobe-index/programming-languages-definition/)
 * [2017 Tiobe Index](https://web.archive.org/web/20170317170815/https://www.tiobe.com/tiobe-index/)
 * [Stack Overflow]()
 * [Things You Should Never Do](https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/)

 [^1]: 2020 [Graphical](https://insights.stackoverflow.com/survey/2020) and [Raw](https://drive.google.com/file/d/1dfGerWeWkcyQ9GX9x20rdSGj7WtEpzBB/view) results.
 [^2]: I came up with this measurement criteria first, I'm not working backwards from data and explaining it, rather testing a hypothesis, although you'll have to take my work for it.