---
title: "Put Your Best Title Here"
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

So I wrote this post about Green VS Brown langauges and the point of hte aritlce was that when people like a new langauge, they might be judging it from a biased perspective because the new langauge they use for new development whereas older langauges tend to be more often used in existing projects. 

That is as lanaguages get used, they accumluate code bases and people have to maintain those code bases and generally people like writing new code so much more than maintaining old code. So langauge start green, only used in a green field development, but if successful eventaully become brown, primarly used in maintanance.

So its easier to compare peoples feelings on two brown langauges, or two green languages. Ruby was so amazing, but then fast forward 2 decades and people are dealing with giant Rails monolothis that nobody understands and ruby seeems way less hot. Even though Ruby is a better langauage today then it was then, people like it far less.

Ok, I stil think all this is true, but it is a simplification and the biggest peicee of critisim I got on the article was that you know what Adam, this ignores the fact that langauges actaully get better. 

Maybe ruby is better for greenfield projects then it was 20 years ago, but also the table stakes are different. It was competing against old Java and perl then and now there are so many competitors.

Its like say Ruby could get a Gold 1890 track and field with a time of X, and not its at X+5 but you are ignore the fact that X+5 is no where near the level people are playing at now.

## Language innovation

So, lets talk about langauge innovation. I think it can be seperated into two things. Category one is the code, the systnax and semantics of the langauge. Not sure why I'm still on Ruby but I think it was very much a language innovation. People writing very verbose code in Java all the sudden didn't need to declare types, and didn't need to worry about marking things as private or public and writing getters and setters and annonomous innner classes. ( I mean it turns out that all this flexibility had other downsides, but lets ignore that for now. )

So what exists after this? What can be better about a programming langauge that is not the programming langauge? Well, that is my second category, which I don't have a great name for but I will call the tooling around a language.

Maybe this is the non-code developer experience of a programming language and its effect can be huge. It's my thesis that these category two factors, although they aren't programming language features in the traditional way, they tend to dominate.

If you took the C programming languages syntax and relaunched it as the Do lanaguge, with all of these modern acquitimontes added on, you might have a winner of a language on your hands. Additionally, most of these things seem hard to add on after the langauge and idioms have developed. This will make more sense and I go thru these. So lets do it.

## Batteries Included Standard Library

### History
A standard library is a library of common things that come with the langauge and are ideally written in the langauge itself. C has libc, and C++ has libcpp but both these feel very minimal compared to the common conception of a batteries included standard library. 

The history is a little unclear to me, but it seems like Python (1991) was the first langaue to really take the stance of really having an extensive standard library. Java 1.0 (1996) also came with an extensive standard library (The Java Class Library) and many languages would follwo suite.

The benefits of being able to do what you want to do without having to roll it yourself or pull in a thrid party dependencies are hard to overstate.

Is Javascript the exception that proves the rule?

((Amir quote))

### State of the Art
- go

## Third Party Package Repository

### History

Around the time bigger standard libraries became a thing the world wide web was also taking off and internet proved to be pretty good at fostering collaboration.

Eventually you outstrip even the most inclusive of standard libraries and have to build something yourself.  Or do you? Perl popularized the idea of a global collection of packages with CPAN and nothing has been the same since. I think its fair to say that people who used and contributed to CPAN knew that this was an important thing and didnt' want to work in langauges without it afterwards.


CPAN was launched in 1995 (based on CTAN) and by its height in 2003 it had established a new way for people to get things done with software. That is glueing together 3rd party componenets. So much of modern development now follow this model.

It's hard to find a commonly used programming langauge created after 2003 that didn't come with a third party package repository of some sort. New table stakes had been set.

Side Note: Back porting.

Ok, so you might wonder, if CPAN made perl better and every langauge moving forward embraced a package managers for thrid party code then why didn't languages predating this date just add on package managers?

This is going to be a running theme. It seems that once the idioms and patterns of lanague and a langauge community have been established its hard to go back and add certain things. I'm not sure that this has to be the case, but it does seem to be the current reality. Its just hard to get an agreement in a language community past a certain size, and so things fragement. At least I think this is why Javascript has NPM, Rust has crates but C++ has dds, cpm, conan pacm, spakc, buckaroo, hunter and vcpkg (https://stackoverflow.com/questions/27866965/does-c-have-a-package-manager-like-npm-pip-gem-etc). You know what is better than one universally agreed upon package manager? Not That!

One counter point here though is standard libraries. C++ added its standard library rather than in the game, by successfully bring parts of STL under its roof.

So, a great standard library that does most of the things you need to do, augemented with a third party package repositoy that is easy to use and contribute to. These things are game changes for languages and lead to a community growing up around the langauges.

### State of the Art?

- NPM?


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

If these items have all become table stakes for future langaes are there things happening now, that will also reach this level of table stakes. 

Here are a couple ideas:
* single file native deployment
* easy cross-compiles  (exists to varying levels of ease in Zig, golang, Rust)
* Built in Fuzzers (exists in Golang)
* Built in performance testing (exists in Golang, Rust)

## Conclusion

So going back to the original list of dreaded and not dreaded lanagues, how much does the number of these table stakes affordances the programmming langue have indicate its popularity?

Top 5 loved = Rust, TypeScript, Python, Kotlin, Go
Top 5 dreaded = VBA, Objective-C, Perl, Assembly, C,

So defintely in this case it seems like the top and bottom of the loved / dreaded list correlate with the number of the affordances that the languages have.

