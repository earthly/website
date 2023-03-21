---
title: "Nix Turns 20, but What is It?"
categories:
  - Article
toc: true
author: Josh

internal-links:
 - just an example
---

I talked to Nix users across the spectrum, from hobbyists, to experts, to maintainers, trying to better understand what Nix is and what people user it for. I was hoping to come to single conclusion, a single thing that Nix is, but the truth Nix is many things to many people. The one thing everyone I talked to was excited about was Nix's ability to manage system packages in a way that was


There's a website with a graph of package managers and some info about how nix is the best or has the most or some shit.
Yet Nick's package is, is, uh, the fourth biggest GitHub repository


## What is Nix

It's a configuration language designed specifically for package management. It’s functional and not a general purpose language.
NixOS which takes this idea of a configuratoin language and repeatable software builds and applies describing a Linux instillation.

ChatGPT:

Nix is a purely functional package manager and system configuration tool that allows users to install and manage software packages, and to configure their system in a reliable, reproducible, and declarative way. Unlike traditional package managers, Nix treats packages as immutable and builds them from source code, ensuring that they are reproducible across different systems and platforms.

Ok, but what can I actually do with Nix?

Nix is also a powerful system configuration tool that allows users to define and manage their entire system configuration in a declarative way, using the Nix expression language. This means that users can specify their desired system configuration in a text file, and Nix will take care of installing the necessary packages and configuring the system accordingly.

Nix has several unique features that set it apart from other package managers and configuration tools. For example:

    Nix allows users to install multiple versions of the same package side-by-side, without conflicts or dependencies.
    Nix can build packages from source code in a sandboxed environment, ensuring that packages are built in a reproducible and secure way.
    Nix can create isolated environments, called "Nix environments", that contain a specific set of packages and dependencies, allowing users to easily switch between different software configurations.
    Nix can manage system configurations in a declarative way, using the Nix expression language, making it easy to version control and reproduce system configurations across different systems and platforms.

Overall, Nix is a powerful tool for managing software packages and system configurations in a reliable, reproducible, and declarative way, making it a popular choice for developers, system administrators, and other power users.





### Writing Article Checklist

- [ ] Write Outline
- [ ] Write Draft
- [ ] Fix Grammarly Errors
- [ ] Read out loud
- [ ] Write 5 or more titles and pick the best on
- [ ] First two paragraphs: What's it about? Why listen to you?
- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links to other articles
- [ ] Add Earthly `CTA` at bottom `{% include cta/cta1.html %}`
- [ ] Raise PR

Andreas Herrmann - Tweag
Théophane Hufschmitt - Tweag (contributor to Nix)



Functional and Repeatable


Category: Using Nix Nex Next

Quotes:
The group I work in most commonly, we use the combination of nex plus basil, and in that case, nex, uh, fulfills two purposes. Uh, one is NEX provides the developer environment. . Um, so there we use, uh, N'S Shell, um, which is a feature of N'S where it can sort of set up a shell environment with all the declared dependencies installed in the path, populated with those packages and so on…Um, and in fact, we also use that to provision basil itself.

NEXT And then once you change directory into it, um, it will automatically load a shell environment that's defined by this dot NRC file, um, the first time you have to explicitly allow it for, you know, security concerns. Uh, once you do it remembers that and, um, you can use that to automatically load an next show.

so that's sort of the outer layer. Um, and then the inner layer is where, uh, for the basal build itself, we want to provide system dependencies and tool chains, um, and these kinds of third party dependencies into our project. Um, and in principle, basil has its own notion of providing third party depend.

Um, and of course a more interesting example then is, uh, use nix to patch a g ccc uh, installation that is managed by Nix. , um, and then import that into the basil build as a C tool chain. And now I can use, uh, that to build my cc plus plus targets in basil and I can be sure that they use a specific compiler, namely that one that is provided by.

And if my colleague builds on their own laptop using the same source repository configuration, they're going to use the exact same GCC version installation. 



Category: The Old Way
quotes:
So many of the software packages that you might want to install, you would quickly bump into all kinds of, uh, computability issues. Um, and then trying to install all those things in sort of a separate profile turned out to be really difficult to maintain. I mean, it used this, there is this. I don't know if this is still around, but at the time, this was a popular tool.

It was called Modules, uh, no, lovely unambiguous name,  Implement implemented in Pearl. Uh, and this was a way of switching between profiles of software installations on a cluster so that you could say, oh, right now I need HDFS version X, and in the next project I'm gonna use Version Y. And you can switch between those profiles.

But it relied on just handwritten configurations or all those packages, and essentially just relied on the authors of those package configurations, getting it right, and making sure that they passed all the right flags to all the builds and everything, which is of course very brittle. Yeah. Um, and then after I had Nicks available, all of a sudden I could do things that were previously completely impossible, for example, In one set of simulations that I had, there was a little bit of complicated logic around finding the right sets of parameters and so on.

in the system administration world, um, traditional system administration is tends to be very, uh, low level imperative style where you have your file system, which is when giant mutable, uh, data structure.

and you can install packages by mutating it in some places, uninstall packages by mutating it in what you hope is exactly the reverse of the installation process. Um, and yeah, and when you re a comment, you make assumptions about the state of the Global five system because you expect that all the files that you need will be there at the right magical places.

And. , I mean, that, that works in practice. That's how we've been doing computing for, uh, more than 30 years. And, and it works fairly okay. But then Nick tried the other approach, uh, inspired by functional programming, by saying, well, let's just resign in terms of, um, we want to have. Access values, which are things which probably live somewhere on the disc, but we don't care where.

We just want to get some kind of, um, pointer, some something that tells us how we acc, how we can access it, but without having to bother about where it's placed and just make it so that, uh, whenever we were want to run a comment, these comments get all the informations about where to find what it depends.

that's also enables quite a lot of things because now you can say, well, I have this, I don't know. I want to build this program. I know it depends. G c c, this is this version of G c C, this version of lip through this version of lip bar.

Um, but uh, I don't need to install them globally on my system. I just have a nix file that says, oh, I depend on that, that and that. And then NS will take care of putting them somewhere I don't care about where I just know they will be somewhere and like,  enriching my current environment so that the compiler, so that, well, first I, when I type GCC on the common line, uh, the shell knows where to find jcc, and then G CCC knows where to find my dependencies.




category : Learning Nix
Quotes: 
It's, um, it's also a question of who. Has to learn how much, right? Yeah. Yeah. Um, so in larger teams, often you have those who are dedicated to the build system and the infrastructure and so on, and they're going to have to do a deeper dive. They're gonna have to get a good understanding of the system to be able to, uh, configure and fix it and so on.

Um, but then, uh, you have those who are working on the product, um, and they use the build system and the environment as a tool, but they don't really configure it much themselves. Um, They don't have to take as deep of a dime. Um, and in particular in the n plus basil setting, most of the time they won't really have to interact with NS much.


Category: Community
quotes:
I eventually got the, uh, the second official maintainer of NS after Elco. Um, and a few months later, uh, which is a few months before now, uh, I've started with a bunch of other people, uh, a proper team around the maintenance of ns, which is originally called the next team.



Category: How Nix Works

quotes:
I tend to describe it as, uh, a build system, uh, that pretends to be a package manager or the other way around, uh, in that, If you take, uh, make right the text, make the, the grandfather of all build systems, um, make has this nice, um, um, interface where you just like describe everything that you want to be built.

You describe your dependencies, um, and then you build that. Um, and that's cool. Cause if you say, well, I have. Final compilation step, which depends on this, this, and this. You just declare that and then when you run, make, it's gonna like know what has to be compiled and do that. And if you clo you like, you push your project to uh, get ripple, someone else pulls in, just trends make and all the intermediate artifacts will be rebuilt.

>>>

Um, and so if you like, you can say I have gcc. I don't know, I, I have no idea what's the recent version of gccs, but let's say 7.8 okay for this project and 7.9 for this project. That works. But it goes even a bit further in that you can say, well, this project depends on version 7.8. Alright? And this other project depends on GCC 7.8, but with this patch applied, Oh yeah.

Yeah. And, and you can do that and Mix will see that. Well, this gcc, like this is like Van GCC 7.8. I can, um, like. Yeah, I, I know I have all the inputs for the build. I, I can just like computer part based on that. Uh, like in practice it's using cryptographic hashes, uh, behind the scenes for that and put it somewhere that depends on this whole set of inputs.

And then this other, this other thing which has G C C with that patch, it's nearly the same thing, but the inputs are slightly different because there's also this specific patch. So the path in which it's gonna be installed, it's gonna be slightly different. And so every single variation of the package that you could think about can be installed in, uh, will be installed in a different place if you wanted to.

Category: Don’t Use Nix

Quotes:
Yeah. So there are, there's two kind of downsides I would say, which are, um, the biggest downsides are like, not so much theoretical downsides. Some theoretical downside that you can think of because it adds a bit more indirection, it can be slightly less performing.

But that's, these are in practice, very minor. The main downside is more, are more practical based on two things. Uh, the first one is that, um, well that's not how computers generally work or how, how like, uh, operating systems and distributions generally work. So they don't expect this kind of things and.

The system or the user or both? Don't expect it. Both. Both? Both. Both. Okay. Yeah, we can talk out to you about the, the user a bit later, but for the system, uh, yeah, that's not how it generally works. And fairly often you have to walk around packages, which for example, uh, won't, would, uh, would hardcode some path, uh, in.

because with the traditional way, you know that you're gonna have, uh, I don't know, uh, slash bean slash bash available. Uh, well that one is not exactly true, but most of the time you will have it available. So you can just rent slash b slash slash bash something. And that in a, in a pure niche system, that's not gonna work cuz you won't have a slash bin slash back slash bash, for example.

