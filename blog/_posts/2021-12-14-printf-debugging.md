---
title: "Printf Debugging and Srinivasa Ramanujan"
categories:
  - Articles
author: Adam
newsletter_side: false
sidebar:
  nav: "thoughts"
internal-links:
 - printf debugging
 - debuggers
 - debugging
excerpt: |
    Learn why many experienced software engineers prefer printf debugging over using debuggers, and how this approach can deepen your understanding of your code and make you a better developer. Discover the connection between printf debugging and the unconventional learning methods of mathematician Srinivasa Ramanujan.
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and faster using containerization. Earthly is a powerful build tool that would complement any printf debugging process. [Check it out](/).**

The Visual Studio debugger is fantastic. When I was a C# developer, I used it all the time.

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/4450.png --alt {{ Visual Studio Debug Session }} %}
</div>

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
<!--sgpt-->
Many proficient software engineers choose not to use a debugger, because it forces them to deeply understand their code. Thinking about how the code executes and questioning assumptions are key to this method, known as 'printf' debugging. This approach encourages you to derive solutions from first principles and improves your ability to mentally simulate program execution. 

While using a debugger might be necessary for unfamiliar or complex problems, always aim to understand your code thoroughly. Before jumping into using a debugger or adding a print statement, take time to contemplate the potential causes of the issue you're facing. 

As you work on honing your debugging skills and strive to understand your code better, you might also want to level up your build process. For that, give [Earthly](https://www.earthly.dev/) a look. It could be a valuable tool in your software development toolkit.

{% include_html cta/bottom-cta.html %}
[^1]: With Visual Studio's edit and continue features, I could even write in the new code and try running it in the same session. And now Visual studio has time travel debugging, so you can move backward and forward in execution whenever you like. It's a fantastic feat of engineering.