---
title: "The Slow March of Progress in Programming Language Tooling"
categories:
  - Articles
author: Adam
sidebar:
  nav: "thoughts"
excerpt: Discover how programming language tooling has evolved over time and why newer languages like Go and Rust have gained popularity due to their comprehensive tooling and developer experience. Learn about innovations such as batteries-included standard libraries, third-party package repositories, documentation support, cross-platform development, package managers, and code formatters that have improved the usability of programming languages.
---
The 2022 Stack Overflow developer survey is out!

And what's fascinating to me is which popular programming languages are either loved or dreaded.[^1]

<div class="notice--success notice--big">

### The Popular And Loved Programming Languages (2022)

Rust, Typescript, Python, Go, C#, Kotlin, JavaScript
</div>

<div class="notice--warning notice--big">

### The Popular And Dreaded Programming Languages (2022)

Ruby, C++, Java, PHP, C
</div>

[^1]: What is included here are languages with more than 4200 stack overflow survey responses. I dropped HTML and SQL because they aren't pacmac-complete. And I also dropped Bash and Powershell because their scripting usage makes them less relevant to today's topic. See the full results [on Stack Overflow](https://survey.stackoverflow.co/2022/#technology-most-loved-dreaded-and-wanted).

Last time the developer survey came out, I wrote a post about [Green VS Brown languages](/blog/brown-green-language). In it, I said that when people like a new programming language, they judge it from a biased perspective because new things get used for new development, whereas the older things get used in older projects, which are less exciting. But that misses something big: **Language tooling is getting better**[^2].

[^2]: Language syntax and semantics also gets better over time as well. But its harder to talk about because people have strong opinions. Syntactic sugar is good, or its bad. Operator overloading is good or its bad. Borrow checking is good or unneeded with state of the art GCs. Innovation is happening here, but my favorite example of innovation might be your example that we've strayed to far from god (Or K&R).

## Raising the Stakes - Go vs Rust

{% picture content-wide {{site.pimages}}{{page.slug}}/3870.png --alt {{ Go and Rust Together }} %}
<figcaption>"Let's be friends"</figcaption>

The internet is full of fights about Go vs. Rust. But I think the fascinating thing is how similar their developer tooling experience is. They both have a modern, batteries-included take on development that is very different from many of the languages in the DREAD list. You don't need to wonder what the best tool to use for testing, fuzzing, packaging, or linting is. All of these things are standardized and included. And I think this is one reason they are both at the top of the `Loved` list.

That is, a big difference between working in Go or Rust vs. some of the languages on the dreaded list has nothing to do with the specifics of the language syntax. Instead, the difference is the tooling and supporting ecosystem.

## Tooling Is the New Syntax

My thesis is that the tooling and developer experience for programming languages is improving over time, but mainly in new languages. It goes like this: Tooling innovation happens, new languages adopt and standardize on it, and end up incrementally better than existing languages. If you add up enough of these increments, the older languages, which may have pioneered some of these innovations, seem painful and antiquated.

It will make more sense once I give some examples. So here is a partial list of programming language innovations that aren't the language's syntax or semantics.

## Batteries-Included Standard Library

> I'm not sure whether it's a blessing or a curse, but expansive standard libraries [are a big improvement]. It's possible to get a lot done with PHP, Python, and Go without needing to install any third-party library. They come with json, http client and server, and even database access for the most part.
>
> Amir Saeid

### Standard Library History

A standard library is a library of common things that comes with the language. C has `libc`, and C++ has `libcpp`, but both feel very minimal compared to the common conception of a batteries-included standard library.

The history is a little unclear to me, but it seems like Python (1991) was the first language to take the stance of really having an extensive standard library. Java 1.0 (1996) also came with an extensive standard library (The Java Class Library), and many other languages would follow suit.

It's hard to overstate the benefits of getting simple things done without implementing foundational stuff yourself or having to reach for third-party dependencies.

### Standard Library State of the Art: GoLang

Most modern languages (that aren't JavaScript) now ship with extensive standard libraries. In particular, though, Go puts special emphasis on its standard library. It promises backward compatibility, performance, and well-thought-out implementations. Because of this, Go developers lean on the standard library more than many other communities and generally hold it in high regard.

## Third-Party Package Repositories

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/9160.png --alt {{ CPAN }} %}

### Third Party Packages: History

Around the time more extensive standard libraries became a thing, the world-wide-web was also taking off, and the internet proved to be pretty good at fostering collaboration.

Eventually, you outstrip even the most inclusive of standard libraries and have to build something yourself. Or do you? Perl popularized the idea of a global collection of packages with CPAN; since then, nothing has been the same. I think it's fair to say that people who used and contributed to CPAN knew it was a game-changer.

CPAN was launched in 1995 (based on CTAN), and by its height in 2003, it had established a new way for people to get things done with software. That is gluing together third-party components. So much of modern development now follows this model.

It's hard to find a commonly used programming language created after 2003 that didn't come with a third-party package repository of some sort. CPAN moved the line so that from then forward, a "real" programming language needed to have a strategy for third-party package management.

<div class="notice notice--big">
## Side Note: Backporting.

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/8470.png --alt {{ Backporting }} %}

Ok, so you might wonder, if CPAN made Perl better and every language moving forward embraced package managers for third-party code, why didn't languages predating this add on package managers after the fact?

Well, they did, but it doesn't seem obvious how to get agreement in a language community after a certain point. I'm not sure why this is, but maybe people don't like change?

This is going to be a running theme. Once the idioms and patterns of a programming language, and a language community, have been established its hard to go back and add things on. At least I think this is why Javascript has NPM, Rust has crates but C++ has [dds, cpm, conan, pacm, spakc, buckaroo, hunter and vcpkg](https://stackoverflow.com/questions/27866965/does-c-have-a-package-manager-like-npm-pip-gem-etc). You know what is better than one universally agreed upon package manager? Not eight of them!

One counter point on backporting here though is standard libraries. C++ added its standard library rather late in the game, by successfully bringing parts of STL under its roof. So existing languages can adopt tooling innovations, its just a bigger lift.

</div>

So after CPAN, a great standard library that does most of the things you need to do, augmented with a third-party package repository that is simple to use and straight forward to contribute to became the table stakes for a language.

## Documentation Support

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/6680.png --alt {{ Javadoc }} %}

### Documentation: History

Once you have third-party packages, you need an easy way to document them. Javadoc and it's generated documentation was the first version of this I encountered. It made it much easier to find what I was looking for in the Java Class Library because I could just click around in the Javadocs on the web. Then you can combine Javadoc with IDE integration and it becomes simple to work with code you've never seen before. Exploratory coding becomes possible.

### Documentation: State of the Art

Java with Javadocs is no longer the state of the art. Go has [`godoc`](https://pkg.go.dev/), Julia has [`Documenter.jl`](https://github.com/JuliaDocs/Documenter.jl) and even [hackage](https://hackage.haskell.org/) has pretty good package docs. But the state of the art seems to be Rust with [docs.rs](https://docs.rs/).

## Write Once, Run Most Places ™

> [One improvement I've seen has been] J2EE and the standardization of web servers have unlocked the computing foundation on which our civilization depends today.
> Java and the JVM pioneered that but I don't think they are being adequately credited for it. Once Java became a thing, the platform you develop on stopped being relevant with regards to the platform you deploy on. It's obvious knowledge today, but 20 years ago, this was revolutionary.
>
> Cédric Beust

### Run Anywhere: History

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/7310.png --alt {{ Java ME on Nokia Phones }} %}

Java and the JVM really pushed the line for cross platform development. No longer did your developer environment need to match your production environment. With the JVM, you could compile things down to JARs and run it anywhere that had a Java Virtual Machine installed.

Virtualization and then containerization have made this far more common, but the Java was the first major programming language to enable this type of run anywhere workflow.

### Run Anywhere: State of the Art

There are of course downsides to the Java approach. One of which is the slow start-up time of JIT code and another is the limitation of not being able to easily call something that isn't written in Java. GraalVM claims these problems have been overcome but the current trend seems to be ahead-of-time cross-compiling. Both Rust and Go make this fairly simple, assuming you don't have any c or `libc` dependencies.

But the state of the art appears to be Zig, which can easily cross compile not just Zig programs but also anything that would normally be build with Clang or GCC.

## Package Managers

<div class="align-right">
 {% picture grid {{site.pimages}}{{page.slug}}/7910.png --picture --img width="400px" --alt {{ Add Nutmeg }} %}
</div>

### Package Manager: History

Languages have compilers, and they have lots of flags that you call them with, but this quickly becomes a pain. So things like Make and Autotools came to exist. Now introduce a third-party package ecosystem, and things get even more complex. So you get stuff like Maven and `pip`. Then you have issues like multiple versions of the compiler or runtime and different programs require different versions of packages and in Python you end up with things like `pipenv` and `virtualenv` and something called `conda` that I don't even understand.

All this complexity makes it hard for new users to get up to speed. So new languages try to simplify things by bringing all this management under one roof.

> I would say that package management and LSP have been the two biggest game changers in my personal experience of programming languages.
>
> Ganesh Sittampalam

Much like how the batteries-included standard library expanded the definition of a language, modern package managers have raised expectations substantially. The upside of this expansion is the ease of onboarding and improved developer experience. The downside is that packaging, vendoring, and build software is not free. The language authors must pour many engineering hours into these tools to solve these problems.

### Package Manager: State of the Art

>I think one main advantage that cargo has is that it came with the language. Retro active build tools often lack integration into the platform as a whole
>
> Robert Masen

This package manager area is fast-moving. If you invest a lot of engineering hours, you can improve your language onboarding and day to day usage experience substantially. And so the stakes here keep growing. The `cargo` and `rustup` documentation for Rust are almost as extensive as the rust book, and that doesn't include all the cargo plugins.

Can you easily switch compiler versions in your language? Can you quickly run tests? Can you easily do code coverage, and performance testing? Vendor code? Generate documentation? Lint code? Fix the code lints? All of these used to be stand-alone tools in various language ecosystems and now they come with Rust out of the box. And it's a similar story for Go. I assume other newer languages will try to match or exceed this level of tooling.

## Code Formatters

## Case Study: `gofmt`

Code formatters existed before `gofmt`, just as third-party software packages existed before `CPAN`, but making something a standard for a community profoundly changes things. For example, no language that was created before Go is likely to achieve the near 100% style conformance that Go has because the existing languages have to deal with existing code, whereas `gofmt` enforces a single style and has no knobs to tweak. Languages that follow Go can learn this lesson. And so Rust (`rustfmt`) and Zig (`zig fmt`) have embraced a strong default code style and an accompanying code formatter, and have gained an edge in developer experience because of this.

## So Much More

There are so many other things that I could list in this essay. Some things, like runtime improvements, seem close to direct language improvements. Others like IDEs, LSPs, fuzzing support, and refactoring tools seem closer to developer tools and could have gone on this list. But you have to stop somewhere.

(Tell me what I missed and/or got wrong, and I'll do an update.)

<div class="notice--info">
### The Things That Didn't Spread

There are also the things that language creators were sure would change the world, but yet never gained wider adoption, or only became a fundamental expectation in one particular niche.

Certainly, Jupyter notebooks and REPLs are essential in some domains but unknown in others. Even more niche are Smalltalk's image-based approach to state and Mathematica / Wolfram language's language-integrated-data.
</div>

## Conclusion

The tooling that enables developers to get work done is a massive part of what makes a language useable. Tooling is also a changing landscape where standards keep rising.

It goes like this:

When a new developer tooling innovation is discovered, newer programming languages get a chance to bake that innovation into their language tooling. Doing so gives them an incremental advantage, and these increments add up over time to a better developer experience.

So newer languages have one clear, well thought out way to do something, and older languages will have either many contradictory ways, or no ways at all, to do the same thing. And this makes older languages feel old.

{% include_html cta/bottom-cta.html %}
