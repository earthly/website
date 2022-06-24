---
title: "The slow (but steady) march of progress in programming languages"
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - just an example
---
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

The Stack Overflow developer survey is out! 

Last time it was out, I said this thing about it, and Today I'd like to explain why parts of that were wrong, or maybe too simple.

## Green VS Brown languages Revisited

I wrote this post about Green VS Brown languages and the point of the article was that when people like a new langauge, they are judging it from a biased perspective because the new langauge is used for new development, green field development, whereas the older langauges tend to used in existing projects  - brown field projects. 

That is, as lanaguages get used, they accumluate code bases and people have to maintain those code bases and maintenace sucks. 


I still stand by that. People like writing new code, and don't like maintaining old code. So langauges start green, only used in a green field development, but if successful, eventually become brown. 

Another way to say this I guess is that you can't know how good a langauge is until you've encountered a [Big Ball Of Mud](http://www.laputan.org/mud/mud.html) written in it. Ruby was so amazing, but then fast forward 2 decades and people are dealing with giant Rails monolothis, and Ruby seems way less hot. And Ruby is a better langauage today then it was then, and still people like it less.

I still think all this is true, but it is a simplification because it ignores the fact that langauges actaully get better.

## Rising Stakes

So the stack overflow survey measures what langauges people use and whether they like them or not. This is the Dreaded vs Loved Ranking and I still think that new langauges have an advantage in that framing. But also a new programming langauge can place higher because its better. 

It makes sense if you think of it as a foot race. C++ had a amazing 12 second sprint time in 1984, and continued to improve so that this year it finished in 10.1 seconds. But Rust has a 9.7 second time, and being above 10 doesn't even put you in the top 10 anymore.

Ruby is better for greenfield projects then it was 20 years ago, but the table stakes are different. You can't just be better than Java 1.0 and Perl and expect a medal this year.

So, lets talk about langauge innovation.


## Language Innovation

One possible way to think about language innovation is to subdivide it into categories. One Category one is the code, the syntax and semantics of the language. Perl is one of the most dreaded programming languages in the 2022 list but at some point the flexibilty of Perl for writing text processing scripts was a big innovation.

The same with Ruby. I assume that people who were writing very verbose code in Java saw Ruby and all the sudden didn't need to declare types, and didn't need to worry about marking things as private or public and writing getters and setters and annonomous innner classes and got very excited. I mean it turns out that all this flexibility had other downsides, but lets ignore that for now. 

So, all of these syntax and semantics improvements go in category one. Borrow checkers, actors, syntaxic sugar, type systems: all category one.

So what exists after this? What can be better about a programming langauge that is not the programming langauge? 


## Tooling is The New Syntax

My second category I'll call tooling, although its more than that. And it's what I'd like to talk about today. Category one, that langauage's syntax and semantics is hard to talk about, because it just descends into fight. Syntaxtic sugar is good, or its bad. Operator overloading is good or its bad. Innvoation is happening here, but my favorite example of innovation might your example that we've strayed to far from god (Or K&R).


This second category though is about the developer experience of the language and its both easier to talk about and has profound effects on how work gets done. It's my thesis that these category two factors, although they aren't programming language features in the traditional sense, they tend to dominate.

That's a big claim, but it will make more sense once I give some examples. So here is what I have so far. Here is my list of programming language innovation that aren't the language.

## Batteries Included Standard Library

### History

A standard library is a library of common things that come with the langauge and are ideally written in the language itself. C has libc, and C++ has libcpp but both these feel very minimal compared to the common conception of a batteries included standard library.

The history is a little unclear to me, but it seems like Python (1991) was the first language to take the stance of really having an extensive standard library. Java 1.0 (1996) also came with an extensive standard library (The Java Class Library) and many other languages would follow suite.

The benefits of being able to do what you want to do without having to roll it yourself or pull in a third party dependencies are hard to overstate.

> I'm not sure whether it's a blessing or a curse, but expansive standard libraries [are a big improvement]. It's possible to get a lot done with PHP, Python, and Go without needing to install any third party library. They come with json, http client and server, and even database access for the most part.
>
> Amir Saeid

### State of the Art: GoLang

Most modern languages (that aren't JavaScript) now ship with extensive standard libraries. Go though puts special emphasis on its standard library. It promises backwards compatibilty, performance and well-thought out implementations. Because of this, go developers tend to lean on the standard library more than many other communities and generally hold it in high regard.

## Third Party Package Repository

### History

Around the time bigger standard libraries became a thing the world wide web was also taking off and internet proved to be pretty good at fostering collaboration.

Eventually you outstrip even the most inclusive of standard libraries and have to build something yourself. Or do you? Perl popularized the idea of a global collection of packages with CPAN and nothing has been the same since. I think its fair to say that people who used and contributed to CPAN knew that it was a game changer.

CPAN was launched in 1995 (based on CTAN) and by its height in 2003 it had established a new way for people to get things done with software. That is glueing together 3rd party componenets. So much of modern development now follow this model.

It's hard to find a commonly used programming language created after 2003 that didn't come with a third party package repository of some sort. New table stakes had been set.

<div class="notice notice--big">
Side Note: Back porting.

Ok, so you might wonder, if CPAN made Perl better and every language moving forward embraced a package managers for third party code then why didn't languages predating this just add on package managers after the fact?

Well, they did, but it seems like its hard to get agreement in language community after a certain point. I'm not sure why this is but maybe people just don't like change? 

This is going to be a running theme. Once the idioms and patterns of programming langauge, and a langauge community, have been established its hard to go back and add things on. At least I think this is why Javascript has NPM, Rust has crates but C++ has dds, cpm, conan pacm, spakc, buckaroo, hunter and vcpkg (https://stackoverflow.com/questions/27866965/does-c-have-a-package-manager-like-npm-pip-gem-etc) and yet nobody is using any of those. You know what is better than one universally agreed upon package manager? Not That!

One counter point here though is standard libraries. C++ added its standard library rather late in the game, by successfully bring parts of STL under its roof.

</div>

So, a great standard library that does most of the things you need to do, augemented with a third party package repositoy that is simple to use and straight forward to contribute to. That is now table stakes for a language.

## Community

### History

I'm not totally sure what to say about this one. But a community where people can ask questions and other answer them and relationship are built is important.

### State of the art

- I'm not sure? Julia?

## Single file Deployment / Write Once Run Someplaces

## History
Java with the JVM really set the bar here. With tthe JVM you could compile things down to JARs and run it anywhere where a Java Virtual Machine existed. There is a second phase that followed this with containerization, where docker containers, run c and friends mean you can ship whatever you want to production. 

Newer ahed of time compiled languages push this line even more. Go And Rust and Zig make it easy to ship a single native executable. No runtime installation neccary (although dynamic linking issues can come up with both Rust and Go)
...

## State of The Art?
- Go? Rust Zig?


## Doc Strings, and so on

## History
Once you have thrid party packages you need easy way's to document them. Javadoc and the related generated code was the first version of this I encourntered and it made it much easier to find what I was looking for by clicking around in the javadocs on the web. 

Combine something like javadocs with IDE integration and it becomes easy to work with code you've need seen before. Exploratory coding becomes possible. 

People use Doxygen to back port this to langauge without built in support. 

## State of the Art

Even Java with Java Docs is now behind the standard. Langauges like GoLang, with X and Rust with docs.rs ship autogenerated docs for third party libs whereever they can.

This is the new standard and table stakes.


## IDEs and LSPs

I'm super not sure about adding this one, since what an IDE is and whether its neccary is a hot button issue. Biut 
## History
 ... Turbo pacsla or something

## State of the Art

This has got to be Intellij and Kotlin 


## Future Table Stakes

If these items have all become table stakes for future languages then are there things happening now, that will also reach this level of table stakes.

Here are a couple ideas:
* single file native deployment
* easy cross-compiles  (exists to varying levels of ease in Zig, golang, Rust)
* Built in Fuzzers (exists in Golang)
* Built in performance testing (exists in Golang, Rust)

## Conclusion

So going back to the original list of dreaded and loved lanagues, how much does the number of these table stakes affordances the programmming langue have indicate its popularity?

Top 5 loved = Rust, TypeScript, Python, Kotlin, Go
Top 5 dreaded = VBA, Objective-C, Perl, Assembly, C,

So defintely in this case it seems like the top and bottom of the loved / dreaded list correlate with the number of the affordances that the languages have.

