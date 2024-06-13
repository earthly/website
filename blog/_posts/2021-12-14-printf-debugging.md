---
title: "Printf Debugging and Srinivasa Ramanujan"
categories:
  - articles
author: Adam
newsletter_side: false
bottomcta: false
sidebar:
  nav: "thoughts"
internal-links:
 - printf debugging
 - debuggers
 - debugging
excerpt: |
    Learn why many experienced software engineers prefer printf debugging over using debuggers, and how this approach can deepen your understanding of your code and make you a better developer. Discover the connection between printf debugging and the unconventional learning methods of mathematician Srinivasa Ramanujan.
last_modified_at: 2023-07-19
---
**This article teaches advanced debugging techniques. Earthly improves debugging with reproducible and parallel builds. [Check it out](https://cloud.earthly.dev/login).**

The Visual Studio debugger is fantastic. When I was a C# developer, I used it all the time.

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/4450.png --alt {{ Visual Studio Debug Session }} %}

A typical pattern was putting a breakpoint on a failing assert in a unit test and then just poking around. I would look at all values in the current scope and see if anything looked wrong. Then I could drag the execution point around in the unit test and step into and out of the code under test.  

I would do this pretty quickly without really thinking much about the problem at hand, and I could usually find my way to where the problem was. Of course, it might take me some time to find the problem, but often I could find it iteratively and a bit mindlessly by just using the debugger keyboard shortcuts to walk around the code.

<div class="align-left">
 {% picture {{site.pimages}}{{page.slug}}/5610.png --picture --img width="260px" --alt {{ The Debugger Keyboard shortcuts were my most used key }} %}
<figcaption>The Debugger's Keyboard</figcaption>
</div>

Finding problems like this seemed like a minor superpower. I would see other devs writing out assumptions about code, or talking through how it worked to a coworker, in an attempt to pinpoint an issue in their understanding. But I didn't need to do that, I could just debug through the code until I found the problem.[^1]

The strange thing though, is that many incredible developers don't use debuggers at all. And it's not like debuggers are a new technology that haven't made their way out into the world yet. Richard Stallman released GDB in 1986. That was 35 years ago! And yet many developers don't use debuggers and even warn against their over-use:

> The most effective debugging tool is still careful thought, coupled with judiciously placed print statements.
>
> Brian Kernighan, "Unix for Beginners"

I have a theory about this is, and to explain it, I need to talk about a famous mathematician.

## Srinivasa Ramanujan

<div class="align-right">
 {% picture {{site.pimages}}{{page.slug}}/9200.png --picture --img width="260px" --alt {{ Srinivasa Ramanujan }} %}
<figcaption>Srinivasa Ramanujan</figcaption>
</div>

Srinivasa Ramanujan was an Indian mathematician. He lacked formal training in mathematics but made many important contributions to the field. (Wikipedia says he contributed 3900 original results to mathematics). Ramanujan was discovered because he wrote letters to G. H. Hardy, a British mathematician, who brought him to Cambridge as his doctoral student.

However, long before Hardy discovered him, Ramanujan was obsessed with equations and numbers. He spent all his time working on math but had very little access to high-quality mathematics textbooks. However, he managed to get a book from his local library called "A Synopsis of Elementary Results in Pure and Applied Mathematics." It was a reference book and listed, in condensed form, many mathematical theorems, but it often skipped the explanations and proofs.

Ramanujan worked through this book and derived many of the proofs himself. Later, Hardy would lament that Ramanujan spent so much of his short life with only that book and no proper mathematical education to guide him. Ramanujan was a genius, and Hardy thought a traditional graduate math education could have taken him much further.

However, I've heard a different theory of his genius from Scott Young: This untraditional training didn't hurt Ramanujan. In fact, he had accidentally stumbled into one of the best learning methods possible for an obsessively motivated working mathematician - deriving proofs for theorems from first principles.

That is, rather than reading and trying to understand the proofs of prominent mathematicians, Ramanujan was practicing a much more complex skill: trying to derive the proofs himself. Doing that forced him to develop a deep understanding of pure mathematics, and it's that deep knowledge that gave Ramanujan the ability to make substantial contributions to mathematics.

But let's get back to debugging.

## `printf` Debugging

> I don't use debuggers at all. I don't like debuggers.
>
> I use printfs and ... and thinking
>
> I sit back and run through the code in my head and think about 'how could this have happened'
>
> [Mitchell Hashimoto](https://youtu.be/LA8KF9Fs2sk?t=3110)

So why do a lot of the best software engineers not use a debugger? Well, not using a debugger is harder. You have to think, think about how your program executes, think about under what circumstances that thing you are seeing could be true. What assumptions do you have? How might they be wrong?

You need to deepen your understanding of the code to debug it without a debugger. And doing so is a skill -- a skill that doesn't get as much practice in a world with time-traveling, edit-and-continue debuggers.

The secret to printf debugging isn't the printfs. I can use those just as mindlessly as a debugger. The secret is thinking, thinking through the execution of your program, and deepening your understanding of how your program works. Doing so gives you a better ability to simulate program execution in your head. You are debugging not just the program, but your understanding of the program.

Debugging problems with careful thought and the odd printf statement is like deriving the proofs from first principles yourself. It's hard and sometimes it may be beyond your ability. But, when you can do it, when you can find problems in your code via careful thought, it will help make you a better software engineer.

So I still reach for a debugger when a problem is too big to fit in my head or if I don't know the codebase well. But I try to remind myself to pause and spend some time thinking – I force myself to guess what conditions could have led to this problem – before I jump in and add a print statement or fire up a debugger.

[^1]: With Visual Studio's edit and continue features, I could even write in the new code and try running it in the same session. And now Visual studio has time travel debugging, so you can move backward and forward in execution whenever you like. It's a fantastic feat of engineering.

{% include_html cta/bottom-cta.html %}
