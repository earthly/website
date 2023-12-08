---
title: "Nix Turns 20. What the Hell Is It?"
categories:
  - Articles
toc: true
author: Josh
bottomcta: false
internal-links:
 - Nix
 - Docker
 - Package Manager
excerpt: |
    Learn what Nix is and how it can revolutionize software development with its unique approach to package management and operating system configuration. Discover how Nix brings the power of purely functional programming to build systems and ensures reproducibility and control over software dependencies.
last_modified_at: 2023-07-19
---
**This article examines Nix package management. Earthly provides consistent build environments that enhance complement reproducibility. [Learn more about Earthly](https://cloud.earthly.dev/login).**

I was at a bar with friends, and one of them mentioned that they'd heard that Nix is [turning 20 this month](https://discourse.nixos.org/t/nix-20th-anniversary-march-of-nix/24209).

"What exactly is Nix?" I asked.  

"It's a package manager, but like, different," they said.

Then someone else chimed in. "I thought it was a Linux distro, but like, different?"

I pulled out my phone and looked it up, "Says here it's a programming language for managing and building software?"

You may have come across some similar confusion when trying to understand what exactly [Nix](https://nixos.org/) is. If so, I've got answers.

## To the Experts

I've played around with Nix, and it is very cool, but I'm an engineer turned writer at heart, and it's been a while since I last used build tools day-in-day-out for production work. I wanted to hear from experienced Nix users to learn more about what Nix is and what value it delivers.

I spoke with a wide range of Nix users, from consultants, to hobbyists, to devs using Nix in production, and even a Nix contributor. From these discussions I learned that, though Nix can refer to many different technologies, there's a central idea that's at the core of everything.

## What Is Nix?

I started all my interviews by asking the users to define Nix in their own words.

Théophane Hufschmitt, a developer at [Tweag](https://www.tweag.io/team/) and a contributor to Nix, focused on Nix's ability to work as a build system

{% include quotes/what_is_nix/theophane_hufschmitt.html %}

I tend to describe it as a build system that pretends to be a package manager or the other way around. If you take Make, the grandfather of all build systems, Make has this nice interface where you just describe everything that you want to be built. You describe your dependencies, and then you build that…and it's nice; it's declarative.

Nix somewhat has this same idea, but at the package manager level, in that, rather than saying, well, I want to apt-get install this thing and apt-get install this [other] thing...Nix takes the declarative approach of saying, in a file, that this project depends on this package and this package, and we are gonna make them available for you somewhere. You don't have to know where they are or install them globally because that could be annoying for other things. Just declare what you depend on, and this won't change the outside environment or anything else.

{% include quotes/end.html %}

Jonathan Lorimer, former Lead Software Engineer at [Mercury](https://mercury.com/), and an avid user of Nix both personally and professionally, agrees with Hufschmitt, but finds the value best expressed in the _ideas_ Nix was built around.

{% include quotes/what_is_nix/jonathan_lorimer.html %}

Here's the key insight that Eelco Dolstra [^1] had in his PhD thesis: we're awful at labeling the software that we're using in the programming community. The insight that Nix has is that we need to be more precise about the way we label our software.

For example, if you were to install Postgres with Homebrew on Mac, you would do 'brew install postgres'. That doesn't tell you what version of Postgres you're getting, which can be very confusing...But even if it was tagged with a version, there are many different versions between Postgres 14 and 15, like 14.1, 14.2, etc. Do you know which C compiler it was compiled with? Do you know which version of GCC was used or which flags were enabled for that compilation process? Do you know which environment it was compiled on? Was it cross-compiled for Mac from Linux?

The entire value of Nix falls out of this one insight that software is so much more than just the name and version labels. It's the entire closure of dependencies that the software has.

{% include quotes/end.html %}

Andreas Herrmann leads the Scalable Build team at Tweag:

{% include quotes/what_is_nix/andreas_herrmann.html %}

I mean, something that's interesting about Nix is the foundations it's built on are very general. It's really taking this idea that building software is also just evaluation of code of some form, and applying this purely functional programming idea there. And it's essentially applying memory management discipline to software deployments. You have packages separated on the file system. You can trace back references between them, you can garbage collect them, you can make sure that this installation is never in an inconsistent state. That's a really cool feature.

{% include quotes/end.html %}

<!-- vale off -->
Daniel Firth, a Software Research Development Specialist at [Homotopic.Tech](https://homotopic.tech/), was the first person I spoke with to really hone in on the value of the Nix language.
<!-- vale on -->

{% include quotes/what_is_nix/daniel_firth.html %}

Nix is a purely functional, declarative programming language for expressing build products. It's a domain-specific language specifically for talking about the product of compilation.

So it's functional in that you can refer to functions as values, you can assign them to variables, you can pass them around. It's pure, in that the outputs are uniquely determined by the inputs, and there are no side effects. That's Nix.

{% include quotes/end.html %}

This language is what is used to define Nix packages, and the functional, pure nature of it is what guarantees reproducibility. And this extends to NixOS as well.

Firth continues:

{% include quotes/what_is_nix/daniel_firth.html %}

So we're looking at being able to take a value and inspect it, see what it is, see what's inside it. And in that sense, because it's a language for talking about build products, the operating system itself is the result of calling some pure function that builds the operating system. And so that conceptual simplicity just extends everywhere. So the operating system itself is just the result of calling a function, you can refer to it in the programming language, and you can pass it around and it can be the input to other functions, like deployment functions, or whatever you want. So as long as you can figure out what it is you've got, then you can figure out how to use it.

{% include quotes/end.html %}

This starts to give us an idea about how all these things, the package manager, the OS, and the language, are connected.

## The Nix Package Manager

So, a big part of what makes Nix exciting is its approach to building, labeling, and installing software. To get a better understanding of how this works, let's compare it to a popular package manager for Linux.

APT installs packages into system-wide directories such as `/usr/bin` and `/usr/lib`. It does this partly because these directories are already part of your `PATH` and so software in them is easily accessible. But this also means that, in most cases, multiple versions of the same package cannot coexist on the same system. It can also be difficult to manage dependencies and versions with APT, at least at the level Nix allows.

Nix, on the other hand, installs packages in `/nix/store/`, which is a dedicated directory for all Nix packages. Each package gets installed into a subdirectory. The name of the directory always starts with a cryptographic hash, for example `/nix/store/8wvqqiwk6lpy7j3q3rdbfb7g1ipifdvh-gcc-11.2.0`. The power is in what that hash represents. It's computed based on the inputs for the build: the source files, the compiler, what flags were passed in, and more. In this way, Nix not only knows what dependencies a package needs but also what dependencies those packages have and exactly which versions with which inputs were used to build them. You essential get the entire dependency tree, along with instructions about how to rebuild everything.

So Nix isn't just giving you the version of the package you want; it's giving you the entire history, bill of materials, and supply chain. This not only gives you a level of control over which packages you are using, but it also allows you to rebuild them with an accuracy that other package managers can't compete with.

There's a bit more too it, but I'll let the experts take over from here.

Lorimer:

{% include quotes/what_is_nix/jonathan_lorimer.html %}

So when you pull a package from Nix, what you're doing is you're saying, Okay, give me the instructions to build that. There's a step called evaluation, where it evaluates what the name of the software will eventually be, then what it does is it can check against the cache and say, "Does this software already exist?" Oh, it does? Just pull that down." [But if] it checks and it says, "Oh, no, it doesn't exist; this is a new piece of software that no one's built before", well, then your computer will go ahead and build it and then you'll have it.

{% include quotes/end.html %}

Hufschmitt:

{% include quotes/what_is_nix/theophane_hufschmitt.html %}

And so you can say 'I have GCC'. I don't know, I have no idea what's the recent version of GCC, but let's say 7.8 for this project and 7.9 for this project. That works. But it goes even a bit further in that you can say, well, this project depends on version 7.8, alright?' And this other project depends on GCC 7.8, but with this patch applied...it's nearly the same thing, but the inputs are slightly different because there's also this specific patch. So the path in which it's gonna be installed, it's gonna be slightly different. And so every single variation of the package that you could think about can be installed in a different place if you wanted to. But they are only going to be available in the environments in which you specify that they should be available.

{% include quotes/end.html %}

### Adding Packages

One barrier to entry for users looking to adopt Nix in the early days was that it simply didn't offer a lot of packages.

Hufschmitt:

{% include quotes/what_is_nix/theophane_hufschmitt.html %}

Nix used to be like, because it was a small niche, it was pretty hard to find packages on it, or at least up-to-date and well-maintained packages. But actually, that has changed over the past, I would say, five years.

One reason is that it's much easier now to update packages for Nix than it is with other package managers.

{% include quotes/end.html %}

The [nixpkgs](https://github.com/NixOS/nixpkgs) repo on GitHub has over 5000 contributors. The website <https://repology.org/> which "monitors a huge number of package repositories and other sources" lists Nix as the top package manager in several categories including number of packaged projects (over 80,000) and number of projects with up-to-date packages (over 50,000).

Herrmann:

{% include quotes/what_is_nix/andreas_herrmann.html %}

It's actually very easy to contribute packages to the Nix packages set. And it's also very easy to manage software that you depend on cleanly for the Nix packages set up on your own machine. So you don't even have to commit the package to the distribution, if you don't want to, you can still install it as a proper first-class package locally, on your own machine. Because it has these overlay mechanisms. The Nix packages, it's just a git repository on GitHub. So if you do want to contribute a new package, or make an update or something, it's just a PR, so it's super easy to do.

{% include quotes/end.html %}

Hufschmitt:

{% include quotes/what_is_nix/theophane_hufschmitt.html %}

If you've ever tried to modify a Debian package, it's really a huge pain. You have to find the source packages and modify things here and there. Repackage it, recompile it, and then get the binary package. Put that somewhere.

That's a lot of manual steps. With Nix, because at a certain level you are just declaratively building the source code, you can just take the original expression that describes how this thing is built. You tweak it a bit, and you rebuild it...Updating a package on Nix is essentially, like it's the happy path. It's like three lines per request that you make on the GitHub repository. Which is incredibly easy compared to most other package managers.

{% include quotes/end.html %}

Not only that, but being able to define Nix packages using the Nix language also has benefits.

Firth:

{% include quotes/what_is_nix/daniel_firth.html %}

Yeah, so [other package managers] all have their own bespoke package format. So Ubuntu and Debian use `.deb`. Fedora and Red Hat use RPM...but they're all bespoke; they're all supposed to be interpreted specifically by Ubuntu package manager or the Fedora package manager.

So you can't write programs, you can't write functions in those; they don't support that kind of ad hoc programming. Whereas with Nix, you can write programs which will produce derivation outputs. So you can start to condense the code. So you've got like 50 packages that you need to package, and they're all somewhat similar. In Ubuntu Fedora, I imagine, they'll probably be 50 files, 50 RPM files, to package each of them, and they'll be copies of each other. With Nix, since you can deduplicate code, you can write some helper functions that would deduplicate as much of that as possible and parameterize the rest so that you can reduce all of those 50 expressions. And each of them would be pointing at a different source, but they'd all have roughly similar build logic.

{% include quotes/end.html %}

## Nix With Other Tools

There's value to be had with just the Nix package manager, but a few of the people I talked to mentioned using Nix with other popular build tools.

### Nix With Bazel

At Tweag, they combine Nix with Bazel.

{% include quotes/what_is_nix/andreas_herrmann.html %}

The group I work in commonly uses the combination of Nix plus Bazel, and in that case, Nix fulfills two purposes. One is providing the developer environment. We use [Nix Shell](https://nixos.org/manual/nix/stable/command-ref/nix-shell.html), which is a feature of Nix where it can set up a shell environment with all the declared dependencies installed in the PATH, populated with those packages, and so on. We also use it to provision Bazel itself.

…so that's the outer layer. The inner layer is for the Bazel build itself, we want to provide system dependencies and toolchains, and these kinds of third-party dependencies into our project. In principle, Bazel has its own notion of providing third-party dependencies.

A more interesting example is using Nix to patch a GCC installation that is managed by Nix, and then importing that into the Bazel build as a C toolchain. Now I can use that to build my C++ targets in Bazel, and I can be sure that they use a specific compiler, namely the one that is provided by Nix.

If my colleague builds on their own laptop using the same source repository configuration, they're going to use the exact same GCC version installation.

{% include quotes/end.html %}

### Nix VS Docker

Nix can offer some similar benefits to Docker, but as Firth points out, there are fundamental differences to be aware of.

Daniel Firth:

{% include quotes/what_is_nix/daniel_firth.html %}

So the main difference with Docker is that Docker is imperative. It's not declarative. Obviously isn't. It's not a language really. All it says is execute the steps in order. And Docker will arbitrarily trust the internet. So if you make an Ubuntu image in Docker, and then you say, execute these apt install steps, it will go and contact the Ubuntu Package Manager. And it will trust the internet at that point. So there's no guarantee that if you try and build a Docker container using Docker today, that it will be the same Docker image that you build in a year. Whereas with Nix, the inputs completely determine the outputs, and all of the inputs are cryptographically hashed. And all of the outputs are cryptographically hashed. So it knows if there's a mismatch if someone has changed the source on the internet, for example, [or] a source has gone missing. There's no way it's going to accidentally introduce a source that you didn't intend to go into the image, whereas Docker will just pull whatever is there.

{% include quotes/end.html %}

My colleague, Adam Gordon Bell, worked on container security as a Software Engineer at Tenable. He sees Nix and Docker as two different ways of solving the same problem.

{% include quotes/what_is_nix/adam.html %}

Packaging things is hard on Linux because you have dynamic dependencies. Everything written in C probably loads in libc. And it gets worse from there. You have all kinds of dependencies that are loaded dynamically at runtime, some crypto library, P threads, et cetera. If everything was linked into a static fat binary, it would be easy to package a deploy things onto Linux machines, but that's not the case.

So one way to view Docker is as a hack around this issue. You can ship an application easily – You can package it up easily – If you put it inside of a box and inside that box, you put an entire Linux file system and all its dependencies.

A second solution is the one that Nix has, which is to rethink all this. When you build things just be very explicit about what the dependencies are. And when you link them, link them by hash that's made of all the inputs, and then you don't have collision problems. And you've solved the packaging problem for Linux. But it requires changing how you build programs.

{% include quotes/end.html %}

Nix can work with Docker in a couple of different ways.

Lorimer:

{% include quotes/what_is_nix/jonathan_lorimer.html %}

So an amazing use case for Nix is to use it to generate Docker images. Docker and Nix are generally seen as competitors, but I think Nix is actually a fundamental value add to Docker. You can leverage the more granular caching that Nix has, and just have a build-once Docker image.

Another great way to use it, if you don't want to rebuild Docker images, is you can use the default [Nix] Docker image that is pushed to Docker Hub; you can pull it down; it's very small and lightweight. And what you do is you get access to the Nix CLI in there. And then you can use that to run the software that is described and stored. So you're just using a container or using Docker for what it does best, which is provide a uniform interface for being run in different environments. So you can hook into Kubernetes, you can run a bunch of different isolated Docker images on the server, but you aren't using Docker to sudo apt-get your software which is completely nondeterministic. You're using Nix to describe your software. And now you get all these benefits because your Docker image is completely uniform. You'll never have to rebuild it.

{% include quotes/end.html %}

Herrmann:

{% include quotes/what_is_nix/andreas_herrmann.html %}

I think some interesting differences with Nix is one, the reproducibility side on Docker is a little trickier, right? If you have a pinned Docker image, that's not gonna change. But if you need to make a change to a Docker file and rebuild it, it depends, right? I mean, a Dockerfile doesn't have updates. Right? At that point to make that reproducible, you have to have an entire apt cache and it's very difficult. So that's a big difference. Where with Nix, if you make one incremental change, that's going to be the only thing that changes, the rest will stay the same.

Another is with Nix, you get more reuse and granularity. So with a Docker container, the images are layered linearly, right? They're stacked on top of each other. But you cannot so easily say, those two containers, they happen to share those files in common. So load them on top of each other, and, you know, avoid the duplication, it's usually not really possible. Whereas with Nix, you really get this granularity at the package level, where, since everything is installed in the Nix store in these dedicated paths that don't collide, if two of your packages use the same libc version, they can just point to the same Nix store path and reuse that bit. So that gives more reuse, more granularity.

And, I mean, it's also because you know exactly what each package depends on, you can generate quite minimal environments. So with Docker, images based on usual, like, more common Linux distributions, it can be hard to make a minimal Docker image that doesn't contain too much stuff that you don't actually need. Because, I mean, you can start from a really minimal image, but then maybe you're missing too many things. And then once you install something, it comes with its own predictive dependencies that come with it, and all of a sudden, you have too much stuff in the image again. You can do use Nix to generate Docker images. And they can be very minimal, really generate some really small. So Nix Packages comes with a set of tools called Docker tools. And you can either use regular pre-made Docker images as base images, you can even do some Ubuntu or Debian base image, or you can generate a new base image from Nix. And then really only install the things that you actually need in a container.

{% include quotes/end.html %}

## What About That OS?

Up to this point, we've focused mainly on the Nix Package manager and the Nix language, but many of the people I talked to were just as excited about NixOS.

Jeff Zellner is a Director of Engineering at [FireHydrant](https://firehydrant.com/). He doesn't use Nix for work, but runs NixOS at home:

{% include quotes/what_is_nix/jeff_zellner.html %}

Nix is just something that I got into six or seven years ago. One of my friends ran NixOS on his laptop, and he showed it to me. And I was like, wow, this is unbelievable, like this is, I don't know, it's like a holy grail of computing to just have that much kind of declarative configuration.

{% include quotes/end.html %}

NixOS is a Linux distribution built around the Nix Package manager. What that means is that, not only does it use Nix Package manager by default, but it takes the same concepts that make Nix Packages declarative and reproducible, and applies them to configuring your OS. You use the Nix language to define your configuration in a set of files, and Nix builds your system for you the same way, every time.

For Zellner, this repeatability was all he needed to switch:

{% include quotes/what_is_nix/jeff_zellner.html %}

I think it's really magical because I love breaking things. I don't even really do that much development anymore, but I just like the idea that I can apply the configuration to my machine, I can revert it, I could destroy my machine and rebuild it... I don't leverage any of the, like real package manager capabilities to do development. In fact, I don't even know how that works very well. I'm pretty much just focused on: I have this great monolithic, relatively monolithic, configuration file, and it makes my machine exactly how I want it, sets up my window manager, sets up my vim.rc, it sets up my terminal. Just everything is exactly configured, not just at, you know, a package layer, but deep down into the configuration of packages. And that's really powerful, I think.

I don't use it for development and like building a nice environment to deploy software. I feel like that's probably its superpower. I just don't use it that way. So in my mind, like Nix, particularly, NixOS is just like, if you're the kind of person that runs a tiling Window Manager, install Nix OS, and you'll never look back.

{% include quotes/end.html %}

Lorimer:

{% include quotes/what_is_nix/jonathan_lorimer.html %}

The package manager and the OS are so deeply ingrained because the whole point of an OS is to run software. So you can see why there's like a deep connection. But I actually think that using Nix to specify your configuration is a nice to have, but it doesn't get at this philosophical core that I think is just so beautiful. Now, I say this as someone who uses NixOS every day, I love it. The thing I hated about my Mac was it was always in a dirty state. From the moment I installed software. If I wanted to move Macs I had to reinstall everything. I never knew which version I was at. I never knew what I had to install. I stopped my Adobe subscription last year, and I haven't been able to get Adobe off my system. It's just been impossible. And so I've got this like Adobe cloud syncer using up tons of CPU in the background, and I just can't find a way to get rid of it.

So I was a lifetime Mac user. And then I had been meaning to try out Linux, because, you know, I'd done software development, and all of our servers were Linux. And so I figured, you know, it was important to understand the environment that our code is running in. Now, having converted, I'm surprised that any developer uses Mac. I think it makes sense to be closer to what you're deploying your code to.

So I did Arch Linux first, thinking that it would be a gateway into NixOS. But ironically, Arch Linux was the hardest thing I've ever done. It was extremely confusing. And I ended up totally breaking my system within a month, which obviously wasn't great, given that it was my main driver for work. And then I tried Nix OS and got it up and running really quickly. And you know, I've never looked back. I had none of the issues that I had with Arch. It's a way easier mental model, in my opinion. And so I would actually even recommend NixOS as a beginner Linux distro with the caveat that you need, like some programming experience to kind of work your way around Nix's peculiarities.

{% include quotes/end.html %}

Firth:

{% include quotes/what_is_nix/daniel_firth.html %}

I've been using Nix for five or six years. So initially, I just dived in with the operating system, installed NixOS on all of my machines. And some of those installations, I'm still running. I haven't changed them all since.

{% include quotes/end.html %}

## Learning Nix

Once you are able to wrap your head around what Nix is and how it can be useful, you've still got to learn how to use it.

Hufschmitt:

{% include quotes/what_is_nix/theophane_hufschmitt.html %}

<!-- vale off -->
So one of the big pushbacks is that the learning curve for Nix is pretty steep. We've actually invested quite a lot of effort in the past year to try and smoothen it as much as we could, which is still a huge work in progress. But both because it's a pretty big paradigm shift from the way people are used to working. And also because of like, accidental complexity in the way people tend to learn [Nix]. The documentation is not as good as it could be; the interface in a lot of places leaves a lot to be desired. There's a big, big investment that you need to make at the beginning to start using Nix.
<!-- vale on -->

In practice most companies that I've seen that were using Nix, there were a handful of people that understood it well enough, and were maintaining these Nix files for everyone. And the others were just using them without trying to understand them too much. So reaching that setup works generally extremely well. But that requires a few people to start investing, investing in it. I think in that regard. It's very similar to something like Kubernetes. Once you get used to the way it works you certainly don't want to go back to well, not manual deployment, there's a whole lot of things between manually deploying and going from Kubernetes. But like, it's, it's really powerful once you get how it works and get familiar with the tool. But as long as you're not familiar with it, it's a whole big foreign galaxy that makes no sense whatsoever.

{% include quotes/end.html %}

Herrmann:

{% include quotes/what_is_nix/andreas_herrmann.html %}

It's also a question of who has to learn how much, right? So in larger teams, often you have those who are dedicated to the build system and the infrastructure and so on, and they're going to have to do a deeper dive. They're gonna have to get a good understanding of the system to be able to configure and fix it and so on.

But then, you have those who are working on the product, and they use the build system and the environment as a tool, but they don't really configure it much themselves. They don't have to take as deep of a dive, and in particular, in the Nix plus Bazel setting, most of the time they won't really have to interact with Nix much.

{% include quotes/end.html %}

Firth:

{% include quotes/what_is_nix/daniel_firth.html %}

Yeah, the documentation for Nix is notoriously bad. Even comparatively with a lot of the other functional programming ecosystems. Most of the knowledge you will get either from reading the Nix packages GitHub repository directly or from word of mouth. There isn't really a full tutorial set for next year. I think some people have written ones very, very recently… but they historically haven't existed; you might have to ask somebody or know somebody or be able to read the code. And I just recommend that people just learn how to read the code. That's the only really reliable way you're going to get information about what some of these options are actually doing.

{% include quotes/end.html %}

## Conclusions

### Pure Functions

My main take away after spending some time learning about Nix is that it embraces the functional programming concept of a pure function. If I give a function a certain set of inputs, it will return the same result every time, no matter what. Nix is about building software the same way, whether it's your own software, someone else's software, or your entire OS: You declare all your inputs explicitly and it will be built the same way every time.

What I learned from talking to Nix users is that what really mattered to them, regardless of how they were using Nix, was its ability to bring purely functional programming concepts to computing areas that were previously off-limits.

From that single idea you get a whole [ecosystem](https://nixos.wiki/wiki/Nix_Ecosystem) of tools. We mainly covered the Nix language, the Nix Package Manager, and NixOS, but there's also a continuous build system called Hydra, nix shell, and a deployment and provisioning tool called NixOps. Probably, there's even more.

### Ok, Thanks. Now What?

If you're looking to experiment with Nix, the package manager seems to be the easiest to adopt. You don't need to learn how to write the Nix language to start using it, and installing it on Linux or Mac won't interfere with your current package manager set up. If you're someone who's constantly jumping from project to project and worried about conflicting dependencies or if you're constantly running into build issues related to package versions, it could be a solution.

Learning the Nix language seems like the biggest lift, especially if you don't already have a background in functional programming, but it also seems to offer the most reward (within the Nix ecosystem), as doing so makes working with other Nix tools much more intuitive.

If you're interested in learning more about Nix here are some resources I found helpful while writing this article.

- [The Nix wiki](https://nixos.wiki/wiki/Main_Page)

- [Nix Pills](https://nixos.org/guides/nix-pills/)

- [Nix Pkgs Repo](https://github.com/NixOS/nixpkgs)

- [Zero to Nix](https://zero-to-nix.com/) - "An unofficial, opinionated, gentle introduction to Nix" created by Determinate Systems. It's a great resource, though it does heavily favor that you use their [Determinate Nix Installer](https://zero-to-nix.com/concepts/nix-installer), which I didn't mess with.

- [This Graham Christensen talk](https://www.youtube.com/watch?v=pfIDYQ36X0k) about Nix and containers.

- Check out how [Shopify](https://shopify.engineering/shipit-presents-how-shopify-uses-nix) and [Replit](https://blog.replit.com/nix) have started using Nix.

{% include_html cta/bottom-cta.html %}

[^1]: Eelco Dolstra created Nix as part of his PhD Thesis in 2003.
