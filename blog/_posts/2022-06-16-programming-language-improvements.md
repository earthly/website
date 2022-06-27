---
title: "The Slow (but Steady) March of Progress in Programming Languages"
categories:
  - Articles
author: Adam

---
<!-- vale off -->
The Stack Overflow developer survey is out!

Last time it was out, I said this thing about dreaded vs loved languages, and Today I'd like to explain why parts of that were wrong, or maybe too simple. But first, here is the exciting part of the data. The 'Popular' languages that are loved, and those that are dreaded.[^1]

<div class="notice--warning notice--big">

### The Popular And Dreaded Programming Languages (2022)

Ruby, C++, Java, PHP, C
</div>

<div class="notice--warning notice--big">

### The Popular And Loved Programming Languages (2022)

Rust, Typescript, Python, Go, C# Kotlin, JavaScript
</div>

[^1]: What is included here are languages with more than 4200 stack overflow survey responses. I dropped HTML and SQL because they aren't pacmac-complete. And I also dropped Bash and Powershell because their scripting usage makes them less relevant to today's topic. See the full results [here](https://survey.stackoverflow.co/2022/#technology-most-loved-dreaded-and-wanted)

## Green Vs Brown Languages Revisited

So I wrote this post about [Green VS Brown languages](/blog/brown-green-language) and the point of the article was that when people like a new language, they are judging it from a biased perspective because the new language is used for new development whereas the older languages tend to used in existing projects, which often less exciting.

Or put another way, as languages get used, they accumulate code bases and people have to maintain those code bases and that maintenance works biases peoples opinions against the language.

I still stand by that. You can't know how good a language is until you've encountered a [Big Ball Of Mud](http://www.laputan.org/mud/mud.html) written in it. Ruby was so amazing, but then fast forward 2 decades and people are dealing with giant Rails monolith, and Ruby seems way less hot.

I still think all this is true, but it is a simplification because it ignores the fact that languages actually get better.

## Rising Stakes

The stack overflow survey measures what languages people use and whether they like them or not. This is the Dreaded vs Loved Ranking and I still think that new languages have an advantage in that framing. But also a new programming language can place higher because its better.

Think of it as a foot race. C++ had a amazing 12 second sprint time in 1984, and continued to improve. This year it finished in 10.1 seconds. But meanwhile Rust has a 9.7 second time, and being above 10 doesn't even put you in the top 10 anymore.

Ruby is better today for greenfield projects then it was 20 years ago. But the competition has improved as well. You can't just be better than Java 1.0 and Perl and expect a medal this year.

So, lets talk about language innovation.

## Language Innovation

One possible way to think about language innovation is to subdivide it into categories.

(which I'm going to call the language and the ecosystem)

One Category one is the code, the syntax and semantics of the language. Perl is one of the most dreaded programming languages in the 2022 list but at some point the flexibility of Perl for writing text processing scripts was a big innovation.

The same with Ruby. I assume that people who were writing verbose code in Java saw Ruby and all the sudden didn't need to declare types, and didn't need to worry about marking things as private or public and writing getters and setters and anonymous inner classes and got excited. I mean it turns out that all this flexibility had other downsides, but lets ignore that for now.

So, all of these syntax and semantics improvements go in category one. Borrow checkers, actors, syntactic sugar, type systems: all category one.

So what exists after this? What can be better about a programming language that is not the programming language?

## Tooling Is The New Syntax

My second category I'll call tooling, although its more than that. And it's what I'd like to talk about today. Category one, that langauage's syntax and semantics is hard to talk about, because it just descends into fight. Syntactic sugar is good, or its bad. Operator overloading is good or its bad. Innovation is happening here, but my favorite example of innovation might be your example that we've strayed to far from god (Or K&R).

This second category though is about the developer experience of the language and its both easier to talk about and has profound effects on how work gets done. It's my thesis that these category two factors, although they aren't programming language features in the traditional sense, they tend to dominate.

That's a big claim, but it will make more sense once I give some examples. So here is what I have so far. Here is my list of programming language innovation that aren't the language.

## Batteries Included Standard Library

### History

A standard library is a library of common things that come with the language and are ideally written in the language itself. C has libc, and C++ has libcpp but both these feel very minimal compared to the common conception of a batteries included standard library.

The history is a little unclear to me, but it seems like Python (1991) was the first language to take the stance of really having an extensive standard library. Java 1.0 (1996) also came with an extensive standard library (The Java Class Library) and many other languages would follow suite.

The benefits of being able to do what you want to do without having to roll it yourself or pull in a third party dependencies are hard to overstate.

> I'm not sure whether it's a blessing or a curse, but expansive standard libraries [are a big improvement]. It's possible to get a lot done with PHP, Python, and Go without needing to install any third party library. They come with json, http client and server, and even database access for the most part.
>
> Amir Saeid

### State of the Art: GoLang

Most modern languages (that aren't JavaScript) now ship with extensive standard libraries. In particular though, Go puts special emphasis on its standard library. It promises backwards compatibilty, performance and well-thought out implementations. Because of this, go developers tend to lean on the standard library more than many other communities and generally hold it in high regard.

## Third Party Package Repository

### History

Around the time bigger standard libraries became a thing the world-wide-web was also taking off and internet proved to be pretty good at fostering collaboration.

Eventually you outstrip even the most inclusive of standard libraries and have to build something yourself. Or do you? Perl popularized the idea of a global collection of packages with CPAN and nothing has been the same since. I think its fair to say that people who used and contributed to CPAN knew that it was a game changer.

CPAN was launched in 1995 (based on CTAN) and by its height in 2003 it had established a new way for people to get things done with software. That is glueing together 3rd party componenets. So much of modern development now follow this model.

It's hard to find a commonly used programming language created after 2003 that didn't come with a third party package repository of some sort. New table stakes had been set.

<div class="notice notice--big">
Side Note: Back porting.

Ok, so you might wonder, if CPAN made Perl better and every language moving forward embraced a package managers for third party code then why didn't languages predating this just add on package managers after the fact?

Well, they did, but it seems like its hard to get agreement in language community after a certain point. I'm not sure why this is but maybe people just don't like change?

This is going to be a running theme. Once the idioms and patterns of a programming language, and a language community, have been established its hard to go back and add things on. At least I think this is why Javascript has NPM, Rust has crates but C++ has dds, cpm, conan pacm, spakc, buckaroo, hunter and vcpkg (<https://stackoverflow.com/questions/27866965/does-c-have-a-package-manager-like-npm-pip-gem-etc>) and yet nobody is using any of those. You know what is better than one universally agreed upon package manager? Not eight of them!

One counter point here though is standard libraries. C++ added its standard library rather late in the game, by successfully bring parts of STL under its roof.

</div>

So, a great standard library that does most of the things you need to do, augmented with a third party package repositoy that is simple to use and straight forward to contribute to. That is now table stakes for a language.

## Documentation Support

## History

Once you have third party packages, you need an easy way's to document them. Javadoc and the related generated documentation was the first version of this I encountered and it made it much easier to find what I was looking for by clicking around in the javadocs on the web.

Combine something like that with IDE integration and it becomes simple to work with code you've never seen before. Exploratory coding becomes possible.

People use Doxygen to back port this to language without built in support.

## State of the Art

Even Java with Java Docs is now behind the standard. Go has [godoc](https://pkg.go.dev/), Julia has [Documenter.jl](https://github.com/JuliaDocs/Documenter.jl) and even [hackage](https://hackage.haskell.org/) has pretty good package docs. But the state of the art seems to be Rust with [docs.rs](https://docs.rs/).

## Write Once, Run Most Places ™

> [One improvement I've seen has been] J2EE and the standardization of web servers have unlocked the computing foundation on which our civilization depends today.
> Java and the JVM pioneered that but I don't think they are being adequately credited for it. Once Java became a thing, the platform you develop on stopped being relevant with regards to the platform you deploy on. It's obvious knowledge today, but 20 years ago, this was revolutionary.
>
> Cédric Beust

### History

Java and the JVM really pushed the line for cross platform development. No more did your developer environment need to match your production environment. With the JVM you could compile things down to JARs and run it anywhere with a Java Virtual Machine installed.

Containerization, and virtualization before it, have made this far more common, but the JVM was a big deal.

### State of the Art

There are of course downsides to the Java approach. One of which is the slow start-up time of JIT code and another is the limitation of not being able to easily call something that isn't written in Java.

The current state of the art for running everywhere seems to be ahead-of-time cross-compiled native executables. Both Rust and Go make this fairly easy assuming you don't have any c or libc dependendcies.

But the state of the art appears to be Zig, which can easily cross compile not just Zig programs but also anything that would normally be build with Clang or GCC.

## Package Managers

### History

> If you're going to invent/create a new language, what is the minimum in tooling that any early adopter developer would expect? Early adopters tend to have a lower bar to try new things, but I still find myself wanting at least syntax highlighting and single-command compile/build for all files as a minimum, and grouchy when I have to stare at all the code in one colour like some barbarian.
>
> Nogginly

Languages have compilers, and they have lots of flags that you call them with, but this quickly becomes a pain. So things like Make and autotools come to exist. Introduce a third party ecosystem and things get even more complex. So you get things like Maven and `pip`. Then you have issues like multiple version of the compiler / or runtime and different programs require different versions of packages and in Python you end up with things like `pipenv` and `virtualenv` and something called `conda` that I don't even understand.

All this complexity makes it hard for new users to get up to speed and so new try to simplify this by bringing all this management under one roof.

> I would say that package management and LSP have been the two biggest game changers in my personal experience of programming languages.
>
> Ganesh Sittampalam

Much like the expanded standard library added all this stuff into a tool that ships with the language can really improve the developer experience. The cost is that these are not trivial problems to solve. There are a lot of engineering hours that need to be poured to solve these problems.

### State of The Art

This package manager tool area seems like the current fasting moving area in language. If you can invest a lot engineering hours into this area, you can really make the onboarding experience that much better. The stakes here keep growing. It seems like the cargo and rustup documetation for Rust are almost as big as the rust book and this effort shows. Can you easily switch compiler versions in your language? Can you easily run tests? Can you easily do code coverage, performance testing? Vendor code? Generate documentation? Lint code? Fix code lints? All of these used to be things that were stand alone tools or functions in various language ecosystem now come with Rust out of the Box. And its a similar story for Go and I assume other newer languages will follow a similar path.

>I think one main advantage that cargo has is that it came with the language. Retro active build tools often lack integration into the platform as a whole
>
> Freemasen

In the previous [Red vs Green](/blog/brown-green-language) article much discussion broke out on hacker news about whether Rust or Go syntax would be considered great or horrible in the future. The differences between the languages approaches the syntax and semantics couldn't be more different. But I think the interesting thing is actually how similar they are in a batteries included approach to developer experience. You don't need to wonder that best tool to use for testing, or fuzzing or packaging or linting. All these things are standardized.

## Case Study: `gofmt`

It feels strange to call this area package managers because the surface area is so wide. `cargo` does a lot more than just manage packages. The `go` binary at least calls itself `a tool for managing go source code` and that seems more accurate because with modules, and testing and code generation it's more like an all-in-one developer tooling ecosystem in a single tool.

`gofmt` is an interesting example of a new approach to tooling.

Code formatters existed before `gofmt` just as third party software packages exited before cpan but making something a standard for a community changes things in a profound way.

I previously undertook an effort at a medium sized software company where many programming languages were used to get each language to adopt a code formatter and the process did not go smoothly.

The main objection was that their exists no code formatter that will do as good of a job as someone's specific style of laying out my code. Although that was usually stated in a different way. like "I'll quit before I let a code be laid out like that!" And of course the things objected to in the style were never the same. The thing you hated, someone else on some other team liked.

What wasn't appriecated was the uniformity has value all on its own. And you might not agreed, but in a team environment that value is greater than the value produced by your very specific ascii art approach to coding. Everyone hates the code formatter, but for different reasons and that's ok. Formatting has become a non-issue and that is more important.

So anyways, Go took a stand on this. Code is formatted by gofmt, which has no knobs to tweak, and you need to accept this. And this idea spread, but it can't spread as well backwards into communities who significantly predate go, because they have lots of code that doesn't necessarily conform to any particular encoded style. I really like `scalafmt` and think everyone should use it, but that is not a universal opinion in the scala world. And similarly for `Clang-format` or whatever tool is popular for code formatting in Java land. No language existing before Go is likely to achieve the 100% style conformance that go has.

But newer languages can and so they end up with more uniform communities. Every supportive tool, whether it be unit testing library, or code formatter or code linter, if it get popular enough will become standardized in some new languague and that standardization and investment into smoothing out the developer experience will give that new language an edge at adoption.

## So Much More

There are so many other things that could be listed in this essay. Somethings, like improvements in runtimes, seem close to language improvements and so I've skipped them. Others like IDEs, LSPs, fuzzing, and refactoring tools seem closer to developer tools and certainly could have gone on this list. But you have to stop somewhere.

(Tell me what I missed and / or got wrong and I'll do an update.)

### The Things That Weren't

There is also the things that language creators were certain would become the new table stakes but never gained wider adoption, or only made sense in one particular niche. These include Smalltalk's image based approach to state and matlab / Wolfram language's integrated data. Certainly jupyter notebooks and REPLs are considered essential in some domains and not used at all in others.

The point is though, that so much language innovation is not about the language itself.

## Conclusion

So going back to the original list of dreaded and loved languages, how much does the number of these table stakes affordances the programming languages have indicate its popularity?

Top 5 loved = Rust, Typescript, Python, Go, C#, Kotlin

Top 5 dreaded = Ruby, C++, Java, PHP, C

To me, at least it seems like the top of the list, if you ignore the programming language itself completely, that the top of the list has more developer experience affordances than the bottom.

The tooling that enables developers to get work done and helps teams ship features are a huge deal. And I didn't mention Community – because its such a large and amorphous concept – but a thriving community where best practices and idioms are communicated and spread may in fact be the most essential non-languages factor. But that is a whole different essay.

{% include cta/cta1.html %}
