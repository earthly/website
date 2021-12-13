---
title: "Green Vs. Brown Programming Languages"
author: Adam
categories:
  - Articles
author: Adam
sidebar:
  nav: "thoughts"
toc: true
featured: true
excerpt: "I've noticed something interesting about the types of programming languages people like. It's something that doesn't seem to come up in various discussions of programming language preferences."
---
## The Data

The Stack Overflow Developer Survey[^1] results are a great source of information about how developers work. I was looking at the 2020 results for some ideas on what programming languages we should add to our [documentation](https://docs.earthly.dev/basics/part-1-a-simple-earthfile) on containerized builds, and I noticed something interesting about the types of programming languages people like. It's something that doesn't seem to come up in various discussions of programming language preferences.

The survey results have rankings for **The Most Dreaded Programming Languages** and **The Most Loved Programming Language**. Both rankings come from this question:

> Which programming, scripting, and markup languages have you done
extensive development work in over the past year, and which do you want to work
in over the next year? (If you both worked with the language and want to continue
to do so, please check both boxes in that row.)

A dreaded language is one you work with extensively in the current year but don't want to continue to use. A loved language you use extensively and wish to continue using. The results are interesting because they reflect the opinions of people who are using the languages extensively. There should be no I-heard-X-is-cool effect, where people rank highly things they don't use because they heard it is the new hotness. The inverse should also be true: People who put something on the **Dreaded** list are using it. They are not dreading a language because they heard it was complex, but because they have to work it and feel real pain.

<div class="notice--warning notice--big">
**The TOP 15 Dreaded Programming Languages:**

VBA, Objective-C, Perl, Assembly, C, PHP, Ruby, C++, Java, R, Haskell, Scala, HTML, Shell, and SQL.
</div>

<div class="notice--success notice--big">
**The TOP 15 Loved Programming Languages:**

Rust, TypeScript, Python, Kotlin, Go, Julia, Dart, C#, Swift, JavaScript, SQL, Shell, HTML, Scala, and Haskell.
</div>

There is a pattern in this list. Can you see what it is?

## Code Written Before I Joined Is the Worst

Old code is the worst. Find me a file in a codebase that has been under active development for more than three years, and it will be hard to follow. What starts as a straightforward file access layer develops special cases and performance optimizations and various branches controlled by configuration options. Real-world code evolves to fits its niche, and as it does so, it becomes more complex and harder to understand. The reason for this is simple, and I first heard about it from Joel Spolsky.

> The reason that [ developers ] think the old code is a mess is because of a cardinal, fundamental law of programming: **It's harder to read code than to write it.**
>
> Joel Spolsky - [Things you should never do](https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/)

Let's call this Joel's Law. A lot of things follow from this premise. Why do most developers think the code they inherited is a mess and want to throw it out and start again? It's because writing something new is cognitively less demanding than the hard work of understanding an existing codebase, at least initially. Why are many rewrites doomed to fail? Because much of what makes the code seem messy are vital little improvements that accreted over time. Without some plan for simplifying them, you will end up back where you started.  

![Scott Adams Understood]({{site.images}}{{page.slug}}/dt140812.gif)

It's easy to understand code as you are writing it. You are executing it and refining it as you go. But it's hard to understand code just by reading it after the fact. If you return to old code you wrote and find it hard to follow, it could be because you have grown as a developer and would write it better today. But its also possible that the code is inherently complex, and you are interpreting the pain of understanding that complexity as a code quality problem. Could this be why growing PR backlogs are a persistent problem? PR Reviews are a read-only activity, and they are hard to do well if you don't already have a working model of the code in your head.

## This is Why You Dread It

If much real-world code is unfairly considered a mess, could programming languages also be unfairly judged? If you build new things in Go but have to maintain a sprawling 20-year-old C++ codebase, can you rank them fairly? I think this is actually what the survey question is measuring: dreaded languages are likely to be used in existing brown-field projects. Loved languages are more often used in new green-field projects. Let's test this.[^2]

## Measuring Brown vs. Green Languages

The TIOBE index claims to measure "the number of skilled engineers, courses, and jobs worldwide" for programming languages. There are probably some problems with how they measure this, but it's accurate enough for our purposes. We use the July 2016 TIOBE [index]( https://web.archive.org/web/20160801213334/https://www.tiobe.com/tiobe-index/), the oldest available in way back machine, as a proxy for a language having accumulated lots of code to maintain. If something was big in 2016, it's more likely people are maintaining code written in it than if it wasn't popular in 2016.

The top 20 programming languages on their list as of July 2016 are Java, C, C++, Python, C#, PHP, JavaScript, VB.NET, Perl, Assembly, Ruby, Pascal, Swift, Objective-C, MATLAB, R, SQL, COBOL, and Groovy. We can use this as our list of languages more likely to be used in maintenance work. Let's call them brown languages. Languages not in the top 20 in 2016 are more likely to be used in new projects. We will refer to these as green languages.

![Out of 22 Languages in the combined dreaded/loved list, 63% are Brown]({{site.images}}{{page.slug}}/graph1.svg)
<!-- ```
import matplotlib.pyplot as plt

labels = 'Brown', 'Green'
dreaded_sizes = [10, 2]
overall_languages = [14, 8]
overall_total = 22
dreaded_total = 12
loved_sizes = [6, 7]
loved_total = 13
explode = (0.1, 0)
colors = ["burlywood", "green"]

fig, ax1 = plt.subplots()
ax1.set_title('Green Vs Brown')
ax1.pie(overall_languages, explode=explode, labels=labels, 
        autopct=lambda p: '{:.0f}'.format(p * overall_total / 100),
        shadow=True, 
        startangle=90, 
        colors=colors)
ax1.axis('equal') 

``` -->

<figcaption>
Out of 22 Languages in the combined dreaded/loved list, 63% are Brown
</figcaption>

<div class="notice--warning notice--big">
**Brown Language:** A language that you are more likely to use in existing software maintenance. These projects are often called brown-field projects.

Java, C, C++, C#, Python, PHP, JavaScript, Swift, Perl, Ruby, Assembly, R, Objective-C, SQL
</div>

<div class="notice--success notice--big">
**Green Language:** A language that you are more likely to use in a new green-field project.

Go, Rust, TypeScript, Kotlin, Julia, Dart, Scala, and Haskell
</div>

TIOBE and StackOverflow have different ideas of what a programming language is. To overcome this, we have to normalize the two lists by removing HTML/CSS, Shell Scripts, and VBA.[^3]

<div class="notice--info">
**Removed Language:** Not measured the same by TIOBE and StackOverflow

VBA, Shell, HTML/CSS
</div>

There are many nuances that a simple green / brown split misses - I expect that more green-field projects start with Swift than with Objective-C, but it does seem sufficient to capture what we need. There are far more brown languages in this list than green, but that is what I would expect given that year-on-year turn-over in programming languages is relatively low.  

Now we can answer the question: Do people love and dread the languages they state or are they just dreading legacy code? Or to put it another way: If Java and Ruby appeared today, without piles of old rails apps and old enterprise Java applications to maintain, would they still be dreaded or would they be more likely to show up on the loved list?

## The Dreaded Brown Programming Languages

![Dreaded Languages: 83% Brown]({{site.images}}{{page.slug}}/graph2.svg)

<!-- ```
import matplotlib.pyplot as plt

labels = 'Brown', 'Green'
dreaded_sizes = [10, 2]
overall_languages = [14, 8]
overall_total = 22
dreaded_total = 12
loved_sizes = [6, 7]
loved_total = 13
explode = (0.1, 0)
colors = ["burlywood", "green"]

# Graph one
fig, ax1 = plt.subplots()
ax1.set_title('Dreaded Languages')
ax1.pie(dreaded_sizes, explode=explode, labels=labels, 
        autopct=lambda p: '{:.0f}'.format(p * dreaded_total / 100),
        shadow=True, 
        startangle=90, 
        colors=colors)
ax1.axis('equal') 

```
<figcaption>
Dreaded Languages: 83% Brown
</figcaption> -->

The Top Dreaded languages are almost all are brown languages. 68% of the languages in our complete list are brown, while 83% of the dreaded languages are brown, which is higher than we would expect by chance.  

## The Loved Green Programming Languages

![Loved Languages 54% Green]({{site.images}}{{page.slug}}/graph3.svg)

<!-- ```
import matplotlib.pyplot as plt

labels = 'Brown', 'Green'
dreaded_sizes = [10, 2]
loved_sizes = [5, 8]
explode = (0.1, 0)
colors = ["burlywood", "green"]
total = 13

# Graph two
fig, ax2 = plt.subplots()
ax2.set_title('Loved Languages')
ax2.pie(loved_sizes, explode=explode, labels=labels, 
        autopct=lambda p: '{:.0f}'.format(p * total / 100),
        shadow=True, 
        startangle=90, 
        colors=colors)
ax2.axis('equal') 

```
<figcaption>
Loved Languages 54% Green
</figcaption> -->

In the top loved languages, 54% are green. Only 36% of the languages in our list are green, and every single green language showed up somewhere in the loved list.

> Another flaw in the human character is that everybody wants to build and nobody wants to do maintenance.
>
> ― Kurt Vonnegut

This probably isn't quite enough evidence to say for sure that having to use a language in a maintenance project causes dread, but it certainly looks like it is a factor. Many of the languages people love are too new or too historically unpopular to have many big big-ball-of-mud projects to maintain.  

In other words, Rust, Kotlin, and the other green languages may still be in a honeymoon phase. People's love for working with them may have as much to do with not working in 20-year-old codebases as it does with the particular languages.

## Overcoming Bias

 {% picture {{site.pimages}}{{page.slug}}/angel-devil-wide.png --picture class="wide" --alt {{ Angel and Devil from the Noun Project }} %}

Some newer or historically less popular programming languages might be better than older or more mainstream languages, but our ability to judge seems quite biased. In particular, developers are giving a halo to languages that are newer or were not used commonly in the past, and they are giving horns to languages that have been around longer. I think this is because nobody likes maintaining someone else's code. And also, because of Joel's Law: reading real-world is code hard. Building something new is fun, and new languages are used for that more often.

## The Lifecycle of Programming Language Hype

I originally started digging into these numbers to establish a ranking for what languages were most used and loved by software developers. I was going to use this to guide adding more examples to our [docs](https://docs.earthly.dev/) and our [build examples](https://github.com/earthly/earthly/tree/main/examples). What I came away with instead was the idea of a programming language life cycle: loved programming languages get used a lot, which leads to code maintenance, which causes people to dislike them, which leads to people looking for greener pastures and trying out a newer language. Popular frameworks probably follow this lifecycle as well.

<div class="wide">
 {% picture {{site.pimages}}{{page.slug}}/hype-wide.png --alt A graph showing hype decreasing overtime for a language %}
<figcaption>The lifecycle of programming language hype</figcaption>
</div>

I don't have data for this, but I distinctly remember Ruby being the hottest language back in 2007, and although it does have more competition today, Ruby is a better language now than it was then. Yet now it is dreaded. Part of the difference, it seems to me, is that now people have 14 years' worth of rails apps to maintain. That makes Ruby is a lot less fun than when it was all new projects. So watch out Rust and Kotlin and Julia and Go: you too will eventually lose your halo.[^4]

 [^1]: 2020 [Graphical](https://insights.stackoverflow.com/survey/2020) and [Raw](https://drive.google.com/file/d/1dfGerWeWkcyQ9GX9x20rdSGj7WtEpzBB/view) results.
 [^2]:
     I came up with the criteria first. I didn't hunt for data to back up my original idea.

     I did consider using language creation date to determine green vs. brown status, but some languages have been around for some time but only found usage relatively recently. 

     TIOBE is measured like [this](https://www.tiobe.com/tiobe-index/programming-languages-definition/) and their historical data is only available if you pay, so I am using the Wayback Machine.  
 [^3]: TIOBE doesn't include HTML/CSS because it doesn't consider them Turing complete and therefore not a programming language.  [Shell scripts](/blog/understanding-bash) are measured separately by TIOBE, and VBA is not in the list of languages measured at all, as far as I can see.

 [^4]: Not all brown languages are dreaded however: Python, C#, Swift, JavaScript, and SQL remain loved and I would love to hear if anyone has theories on why. Also [Scala](/blog/top-5-scala-blogs) and Haskell, two languages I have a soft spot for, are the only green languages on the dreaded list. Is this just noise or is there something else going on there?
