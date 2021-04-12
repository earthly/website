---
title: "Green Vs Brown Programming Languages"
author: Adam
categories:
  - Articles
author: Adam
toc: true
---
## Part 1 - Data
The Stack Overflow Developer Survey[^1] results are a great source of information about developers and how we work.  A favorite statistic that comes from the survey is the **Dreaded Programming Languages** and the **Most Loved Programming Langauge** statistic. Both results come from this question:

> Which programming, scripting, and markup languages have you done
extensive development work in over the past year, and which do you want to work
in over the next year? (If you both worked with the language and want to continue
to do so, please check both boxes in that row.)

A dreaded langauge is one people work with extensively in the current year but don't want to continue to.  A loved language is one you'd like to continue to use.  The results are interesting because they reflect the opions of people who are using the langauge extensively at the time of the survey: there should be no I-heard-kotlin-is-cool effect, where people rank highly things they don't actually use because it is the new hottness.  The inverse should also be true: People who put something on the **Dreaded** list are actually using it. They are not dreading C++ because they heard its complex, but because they have to work in a C++ codebase and feel a real pain.

<div class="notice--warning" markdown="1">
**The TOP 15 Dreaded Programming Languages:**

VBA, Objective-C, Perl, Assembly, C, PHP, Ruby, C++, Java, R, Haskell, Scala, HTML, Shell, and SQL. 
</div>


<div class="notice--success" markdown="1">
**The TOP 15 Loved Programming Languages:**

Rust, TypeScript, Python, Kotlin, Go, Julia, Dart, C#, Swift, JavaScript, SQL, Shell, HTML, Scala, and Haskell.
</div>


The great thing about lists like this is that everyone can see what they want in the list and use it to rationilze their own favorites.  With Scala on the dreaded list, I can tell myself that that is probably just data engineering / Spark people throwing off the numbers.  If you are a fan of static types or intepreted languages or OO or FP, you can cherry pick things from this list to support your view.  But there actually is a pattern in this list.  Can you see what it is?

### Code Written Before I was Hired Is the Worst

Old code is the worst.  Find me a file in a code base that has been under active development for more than 3 years and it will be hard to follow.  What started out as a simple rule will develop special cases, and performance optimzations and configuration options.  Real world code evolves to fits its niche and as it does so it becomes more complex and harder to quickly understand.  The reason for this is simple, but the only person who has extensively written about this that I know of is Joel Spolsky. 

> The reason that [ developers ] think the old code is a mess is because of a cardinal, fundamental law of programming: **It’s harder to read code than to write it.**

Let's call this Joel's Law. Joel's thinks a lot of a lot of things follow from this premise.  Why do most developers think the code they inherited is a mess and want to throw it out and start again? It's because writing something new is cognitively less demaning than starting from scratch. Why are many rewrites doomed to fail? Becasuse all the cruft that makes the code messy are actually important little improvements accreted overtime and without some plan for simplifying them you are back where you started.  

![Scott Adams Understood]({{site.images}}{{page.slug}}/dt140812.gif)

Its easy to build up an understanding of code as you write it, but its hard to build up an understanding of code by reading it.  If you return to code you wrote and think its garbadge it could be because you have grown as a developer but it also could be because you have just forgotten how it works and you are intepreting the pain of reading as a code quality problem. Could this be why growing PR backlogs are a persistent problem.  PR Reviews are a read only activity and they are really hard to do well if you don't already have a working model of the code in your head.


### Measuring Brown Languages

Another thing that follows from this is that languages that you have to read and maintain existing code in will seem worse than and the langauges where you mainly write new code : software maintenace is less fun than a greenfield rewrite.  My hypothesis is this effect is actually stronger than the pros and cons of various languages in many cases. I think this is actually what the survey question is measuring: dreaded langauges are likely to be those used in existing brown field projects and loved langauges are those being used in realiveily new projects.  Let's test this.[^2]

The Tiobe index claims to measure the "the number of skilled engineers, courses and jobs worldwide" for programming languages. There are probably some problems with how they measure this, but its accurate enough for our purposes.  We use the July 2016 TIObe index, the oldest available in way back machine, as a proxy for a language having accumulated lots of code to maintain.  If something was big in 2016 its more likely people now are maintaining code written in it than if it wasn't popular in 2016. 

The top 20 programming languages on their list as of July 2016 are: Java, C, C++, Python, C#, PHP, JavaScript, VB .Net, Perl, Assembly, Ruby, Pascal, Swift, Objective-C, MATLAB, R, SQL, COBOL, Groovy.  We can use this as our brown language list. If a language is in the top 20 in 2016, we call it a brown langauge.  If it wasn't we call it a green langauge. 


``` matplotlib
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
fig = plt.figure()
ax1 = fig.add_axes([0, 0, .5, .5], aspect=1)
ax1.set_title('Green Vs Brown')
ax1.pie(overall_languages, explode=explode, labels=labels, 
        autopct=lambda p: '{:.0f}'.format(p * overall_total / 100),
        shadow=True, 
        startangle=90, 
        colors=colors)
ax1.axis('equal') 

```

<figcaption>
Out of 22 Languages in the dreaded/loved list 63% are Brown
</figcaption>

<div class="notice--warning">
**Brown Langauage:** A language that you are more likely to use in existing software maintanence (ie. brown field projects).

Java, C, C++, C#, Python, PHP, JavaScript, Swift, Perl, Ruby, Assembly, R, Objective-C,  SQL 
</div>

<div class="notice--success">
**Green Langauage:** A language that you are more likely to use in a new project (ie. green field projects).

Go, Rust, TypeScript, Kotlin, Julia, Dart, Scala, Haskell, 
</div>


TIOBE and StackOverflow have different ideas of what a programming lanugage is so we have to normalize the two lists a bit by removing HTML/CSS, Shell Scrips and VBA.[^3] 

<div class="notice--info">
**Removed Langauage:** Not measured the same by TIOBE and StackOverflow

VBA, Shell, HTML/CSS
</div>

There is obviously lots of nuances that a simple green/ brown split misses - I expect that more green field projects start with Swift than with ObjectiveC, but its not a bad split. There are far more brown langauges in this list than green, but that is what I would expect given that turn-over in programming languages is realively low.  

Now we can answer the question: Do people love and dread the languages they state in that stackoverflow survy or they really just dreading legacy code, regardless of langauge? Or put another way: If Java and Ruby appeared today, without piles of old rails apps and old enterprise java applications to maintain, would they still appear as highly in these lists?

### The Dreaded Brown Languages

``` matplotlib
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

The top 15 Dreaded languages, minus HTML and CSS, are almost all are brown languages. 15 of the 22 langauges in our list are brown, so this is higher than we would expect by chance.  

### The Loved Greens
``` matplotlib
import matplotlib.pyplot as plt

labels = 'Brown', 'Green'
dreaded_sizes = [10, 2]
loved_sizes = [5, 8]
explode = (0.1, 0)
colors = ["burlywood", "green"]
total = 13

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

In the top 15 loved langauges 54% are green. 15 of the 22 langauges in our list are brown, so this is much higher than we would expect by chance.  This seems to confirm my hypothesis: the languages people love are languages that are too new or too historically unpopular to have giant big ball of mud projects to maintain.  Rust, Kotlin and the rest may still be in the honeymoon phase with many people.  I think Kotlin and Rust are big step forward from Java and C++, but peoples love for working for them may have as much to do with not having to work in 20 year old code bases than that the code bases are written in those particular languages.

### Conclusion
![Angel and Devil by Gan Khoon Lay from the Noun Project]({{site.images}}{{page.slug}}/angel_devil.png)

> Another flaw in the human character is that everybody wants to build and nobody wants to do maintenance.
>
> ― Kurt Vonnegut

So some newer or historically less popular programming langauges might be better than older or more mainstream langauges but our ability to judge that seems like it is quite biased.  In particular, it seems like when deciding if they like a programmign language, software engineers in the stackoverflow survey are giving a halo to languages they have used in a green field project and giving horns to languages where they had to do mainteance work and the reason for this is Joel's Law: reading real world is code hard because it has accumulated special conditions and optimzations for corner cases and so on. Building something new is more fun, and new languages are more likely to be used to build something new.

## Part 2 - Overcoming Bias

The lesson for me here is that I should trust my personal opinion of programming languages less.  This is quite difficult because, well, they are my personal opinions and who else do I trust more?  One group of people I could look to is those who have already adopted a language.  A lot of these green languages are not actually that new.  No one at your company might be using Rust or Typescript, but people at other companies are so talk to them and ask them how maintaining the code going? In particular I'd want to talk, not to the person who ported the code to Typescript, but the javascript developer who came in after that guy left. What does he think of Typescript?

#### Brownfield a Green Language
When I'm learning a new language, and going through tutorial or building a small project all the code is small and understandable and that makes learning easier. But after I have the fundementals under my belt, I could go out into the world and find a large project using the language and try to contribute. This will let me feel what its like to be thrown into an unfamilar codebase. So instead of building something trivial using Haskell Tutorials, I could try to contribute to Pandoc.  Instead of building my own commandline tools in Rust, I could try to help out the Firecracker project.  I think these experiences would give a better feeling for what working with that langauge will be like once the honeymoon effect wears off. 

#### Greenfield a Brown Language
Sarah works somewhere where her time is half keeping an old C++ codebase going and half working on new things that are all written in Go and because of this she loathes C++ and loves Go.  One thing she could try is building something new and fun and small in C++. This should make it easier to notice how much of her loathing is specific to that code base.  

## Part 3 - The Outliers

### Dreaded Outliers
Haskell and Scala are the only two green languages in the dreaded list.  Does this mean they are most dreaded for the qualities of the language alone or are they in the wrong category and this just noise?  I'm not sure. The people dreading Scala and Haskell are either working on an existing code base, in which case its a brown langauge to them, or they are working on a new project and its not going well. Probably its some of both.  Both langauges have a reputation for complexity: does that make the maintance burden particularly acute? It's probably just noise based on my somewhat arbitrary dividing line, but I'd love to hear from you if you are working in these languages but want to leave them behind.

Other ideas:
* people who use these languagse are early adopters, so on to the next thing
* FP 

### The Loved Outliers
The most interesting category is languages that are brown but loved: C#, Python, Swift, SQL and JavaScript.  These langauages aren't new: developers using them are probably not in a honeymoon period - they have had to maintain code for the long term, yet they love the language and want to keep working with it.  C# and Python stand out in this list, they are both quite high on the Loved list and high in the TIOBE rank.  Do Python and C# developers have some secret of code maintanance that Java and Ruby develoeprs never learned? I'm not sure. Maybe the users on these languages just don't see a better option for their skillset out their? If you are a windows developer, C# is where it is at.  If you love iOS developement than you are going to continue using Swift  - better options don't really exist.   



https://www.goodreads.com/quotes/276615-another-flaw-in-the-human-character-is-that-everybody-wants


To Do:
 * check what happens if go back further in tiobe
 * find what SO questions were
 * tangent about tests and types


## References
 * [How Tiobe is measured](https://www.tiobe.com/tiobe-index/programming-languages-definition/)
 * [2017 Tiobe Index](https://web.archive.org/web/20170317170815/https://www.tiobe.com/tiobe-index/)
 * [Stack Overflow]()
 * [Things You Should Never Do](https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/)

 [^1]: 2020 [Graphical](https://insights.stackoverflow.com/survey/2020) and [Raw](https://drive.google.com/file/d/1dfGerWeWkcyQ9GX9x20rdSGj7WtEpzBB/view) results.
 [^2]: I came up with this measurement criteria first, I'm not working backwards from data and explaining it, rather testing a hypothesis, although you'll have to take my work for it.
 [^3]: TIOBE doesn't include HTML/CSS because it doesn't consider them turning complete and therefore not a programming language.  Shell scripts are measured seperately by TIOBE and VBA is not in the list of languages measured at all as far as I can see.

 https://web.archive.org/web/20160801213334/https://www.tiobe.com/tiobe-index/
