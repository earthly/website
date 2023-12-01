---
title: "Approachability in Programming Languages"
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - approachability in programming languages
 - rust in programming languages
 - future is rust
last_modified_at: 2023-09-08
---

**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster. If you want rust builds in CI as fast as local development then [check us out](https://earthly.dev/).**

I see something like this on reddit/r/rust quite a bit:

> I've been learning Rust for the past 3 months and now comparing it with my experience of learning C++, I think it's a lot more difficult. There are so many rules that you need to understand to efficiently program in Rust, including(but not limited to): ownership, the borrow checker, cargo, lifetimes, traits, generics, closures, unsafe Rust, etc.

<https://www.reddit.com/r/rust/comments/xryi2n/opinion_rust_has_the_largest_learning_curve_for_a/>

Many programming languages are designed to be approachable, easy to get up to speed with. This has historically given them an edge in adoption because they are quite literally easier for beginners to adopt.

Python, for instance, was a successor to ABC, a language designed explicitly for teaching purposes. Most people today start with one of those shallow learning curve languages and then struggle when they try a language with a steeper learning curve.

Why is that? Well, language design is about trade-offs. If a shallow learning curve is the number one goal then things like expressiveness, rigor, performance, and maintainability can suffer.

Languages that take a different approach, Rust, Kotlin, Ocaml …, get a lot of newcomers struggling to learn their language. It can be intimidating and demotivating how slow things go. And that is just going through the beginner parts of learning. The trickier part is the intermediate stage, where you want to build things on your own.

That situation, the steep learning curve problem, has now gotten a lot easier, thanks to LLMs. Rust, Haskell, and everything this side of INTERCAL are now easier to learn. That's my conjecture, at least. But let me explain.

## The Intermediate Material Problem

Imagine you've chosen Rust for your next big project - you're ambitious and ready to build a ray tracer. You're drawn to Rust's promises of speed and safety, and you've successfully navigated through the basics with some tutorials and books. But as soon as you start on your ray tracer, you hit a formidable wall. This is where the 'Intermediate Material Problem' kicks in, and it hits hard with Rust. The leap from basic Rust tutorials to implementing complex graphics rendering is immense. You find yourself wrestling with Rust's ownership rules, deciphering compiler errors, and trying to understand how to efficiently manage memory. It's not just about coding anymore; it's about thinking in Rust, and that's a steep curve to climb.

The frustration is real – you know what you want to build, but the path from here to there feels like navigating a maze with no map. This stage, transitioning from a Rust beginner to a confident developer capable of building a raycaster, is a journey filled with challenges and learning curves that many Rust enthusiasts face.

This 'Intermediate Material Problem' isn't unique to Rust; it's a shared experience across many complex programming languages. Years ago, based on HN hype I decided to learn Haskell. After working through several books, I felt ready to tackle some real projects. But I quickly encountered barriers. I often hit walls, unable to understand what I was missing or why specific approaches wouldn't work. It felt like many people had cut their way through this confusing middle jungle, but each person had to find their own way. Stack Overflow was helpful but slow, and various Slack communities I joined helped for quicker debugging pointers, but it was a slow go.

Usually, this is what people mean when they talk of a steep learning curve. It's not getting started with tutorials. It's what happens when you leave the tutorials behind, build your own thing, and hit problems.

## Using LLMs as an Intermediate Coding Buddy

The problem with stack overflow, mailing lists, forums, and Reddit for getting past the intermediate hump is the speed of feedback is so slow. But what if you could ask a question on the subReddit for your programming language and instantly get answers? What if Stack Overflow instantly answered every question instead of closing it as off-topic? The speed of DMing your buddy with the experience of a niche community. At the intermediate level, this is possible with ChatGPT. If you are stuck on some error in building your ray tracer, just ask ChatGPT. If you aren't sure of the right approach, write up your thoughts like it's a Reddit post and ask GPT4 or shell GPT. Sure, you can occasionally hit the limits of its knowledge and get non-helpful answers, but at the intermediate stage, much of what you are asking is not at the limits of knowledge, and the LLMs will know it better than you do. You just need some direction. You don't know what you don't know. You need to find out the likely problems and solutions are. ChatGPT can give you those real quick.

Many people don't see the utility of using ChatGPT in this way, and that surprises me. [Terrence Tao](https://chat.openai.com/share/53aab67e-6974-413c-9e60-6366e41d8414), the highly awarded mathemetician and professor of mathematics at the University of California, Los Angeles, used ChatGPT to [help him with math](https://mathstodon.xyz/@tao/110601051375142142) and reported that it was helpful as a collaborator.

If it can help him navigate the solution space around Diaconis-Graham inequalities, it can help you understand a lifetime compiler error in Rust.

Here are some [personal examples](http://bla/) of [what I'm talking about](http://bka/).

## Learning Suffers Without Struggle?

The realistic concern for this approach is not whether the LLM is helpful enough to get you through this intermediate zone but whether it harms learning. I have an issue and ask ChatGPT, which suggests some things to try, one of which is the solution. But I worry that I wouldn't have gotten that far without it. Is ChatGPT just causing an atrophy of my skills? If my goal is to get good, then is an LLM's assistance hurting my progress?

Contrary to the often-held belief that the best learning comes from grappling with problems alone, research suggests that guided learning can be more impactful, especially in complex fields like programming. The educational psychologist [John Sweller](https://www.sciencedirect.com/topics/psychology/cognitive-load-theory) showed that being walked through a solution by someone else is often the best way to learn something. Better than figuring it out yourself. Large Language Models, by offering instant, contextual, and conversational assistance, excel at this. When an intermediate learner encounters a baffling error or a gap in their knowledge, questioning ChatGPT can provide a well-structured explanation or a step-by-step breakdown of the problem. This is not merely about providing answers; it's about unveiling the underlying logic and process, illuminating the 'why' and 'how' behind the solution.

![Image]({{site.images}}{{page.slug}}/image.png)\

There is this educational concept called the "Zone of Proximal Development". It's the area beyond your current skills where you need some assistance to progress. LLMs can serve as a bridge into this zone, offering assistance to get you past limits on what you can do yourself.

This is called a scaffolded learning experience. The intermediate gap can be closed: Try to build something beyond your abilities, hit gaps, and get help from an LLM. You will be able to do more than you can without them, and if education research is correct, what you can accomplish without them will be expanded by this process. You're not cheating. You're learning.

Try something hard, and lean on an LLM. You will be learning the tools and techniques via collaboration that allow you to get beyond your current boundaries. You will be building up confidence in a new area.

## The Future Is Rusty

This brings me back to Rust vs Python: Yes, if you are learning a programming language for the first time, then learn Python, but if there is something you bounced off of in the past, as I did with building Haskell web services back in the day, well, try again, tackle something hard and use the LLMs to help you along the way. Steep learning curves are now a lot less steep. Try something, hit a barrier, get help, backtrack a bit to make sure you understand, and then charge ahead. Push out into the Proximal Development Zone!

Back to Terence Tao: He is now also using [ChatGPT to teach himself the lean programming language](https://twitter.com/8teAPi/status/1713867160886599920) and using that to formalize some of his proofs.

If the most brilliant mathematician of our time is using ChatGPT to help him with proofs and programming, you have no excuse.

Build something with Rust. Build something with Ocaml. Build something with Elixir. The intermediate problem is over. Your coding buddy can boost you over hurdles and pretty soon you'll be jumping them on your own. LLMs are only getting better. Therefore, programming languages can be more expressive and rigorous, with steeper learning curves, and we can still learn them. **The world can be more rusty**.

(Coincidentally, if you are working in Rust, check out this example of Earthly taking Rust builds from [13 minutes to 3 minutes](http://fsdf/).

{% include_html cta/bottom-cta.html %}
