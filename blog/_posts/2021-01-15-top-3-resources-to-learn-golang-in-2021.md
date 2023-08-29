---
title: Top 3 Resources For Learning GoLang
categories:
  - Articles
author: Adam
internal-links:
   - golang
excerpt: |
    Looking to learn GoLang? Check out this article for the top 3 resources recommended by an experienced developer. From interactive tours to in-depth explanations, these resources will help you get started and build familiarity with the language. Plus, there are bonus resources and recommendations for further learning. Don't miss out on this valuable guide!
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and faster using containerization. If you're learning Golang, Earthly can be a useful tool for streamlining your build process. [Check us out](/).**

## Why Learn Go

<blockquote class="twitter-tweet" data-width="550">
<p lang="en" dir="ltr">If I were a system administrator looking to learn a new programming language it would be Go.<br><br>So many of our tools including Kubernetes, Prometheus, and Terraform are written, and extended, in Go that it's almost a requirement next to learning Bash. <a href="https://t.co/OfZmGo4uP5">https://t.co/OfZmGo4uP5</a></p>— Kelsey Hightower (@kelseyhightower) <a href="https://twitter.com/kelseyhightower/status/1336097427586129920?ref_src=twsrc%5Etfw">December 7, 2020</a>
</blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

I know I am a bit late to the game here, with Go being over 10 years old, but the main reason I am learning Go is that it's the language used here at Earthly.

Why should you learn Go though? &nbsp;The big reason is that the cloud world seems to be running on Go. [Kubernetes](/blog/building-on-kubernetes-ingress), Docker, CockroachDB, Prometheus, etcd, Traefik, Istio, InfluxDB, and many more are written in Go.

## Who This List Is For

> "Before you learn Go, learn some C" -- [Alex Couture-Beil](https://github.com/alexcb)

This list is for experienced developers who want to learn Go. This is the list I am using to learn.

I've been a developer for over a decade and I've learned a lot of languages over that time. It's something I really enjoy. &nbsp; If you are learning go just like I am, here are the top 3 resources I found in 2021 for learning it.

The list is shorter than I expected it to be, coming from Scala. I'm pretty certain some of Go's success is due to that simplicity.

## #1 A Tour of Go

![Screenshot of tour of go]({{site.images}}{{page.slug}}/pN9WHj_jvb.png)\

> "Honestly, for me I had a background in C, so simply going through various tutorials like [https://tour.golang.org/list](https://tour.golang.org/list) is how I learned."
>
> — Alex Couture-Beil

The first resource to recommend is the [Go Tour](https://tour.golang.org). Titled "A Tour of Go", it is an interactive exercise that takes you through learning the major features of Go. &nbsp; It includes some exercises, although maybe not quite enough for my taste.

It's great because it gets you running and then writing code very quickly. &nbsp;You don't need Go installed or even a text editor to start working through this tour and that low barrier to entry is really nice.

## #2 Go by Example

![Go By Example Screenshot]({{site.images}}{{page.slug}}/D1dOytb5di.png)\

> "I found that hitting gobyexample.com when I needed practical examples helped a ton"
> — [Corey Larson](https://twitter.com/dchw)

After reading the tour, you're probably ready to start playing around. If you have a side project, perhaps try reimplementing it in Go. If you'd like a more structured approach start with [Codewars](https://www.codewars.com/) or [Exercism](https://exercism.io/tracks/go).

Either way, writing, and running some actual code is a great way to build up familiarity. &nbsp;As you do this G[o by Example](https://gobyexample.com/) is a great reference. Personally, I hadn't written a C style for loop in a long time and I'm not sure if I had ever used the `continue` keyword before. The side by side examples provided really helped cement things.

## #3 Effective Go

![Effective Go Screenshot]({{site.images}}{{page.slug}}/Od6ESpAy3U.png)\

Effective Go is next up. &nbsp;This document written by the language authors and explains a lot of the idioms of the language. &nbsp;It is dense but very informative. &nbsp;If you use a language enough, the syntax and semantics of it become second nature but I'm not there yet and for me, its very helpful to grasp the reasons behind some features. &nbsp;This backstory gives me a hook that helps strengthen my understanding.

Here is an example. &nbsp;As I was going through "The Tour" I was surprised when semi-colons appeared. All the examples had been devoid of semicolons and then all of a sudden they appeared in for loops and then nowhere else.

Effective Go explains that, like in JavaScript, the Go lexer automatically inserts semicolons using a simple rule.

> if the newline comes after a token that could end a statement, insert a semicolon - [Effective Go](https://golang.org/doc/effective_go.html#blank)

I hadn't seen semicolons yet because I hadn't seen multiple statements on a single line. Learning this rule made thee syntax feel less magical and more internally consistent.

That is just one example of something I learned from reading this document. &nbsp;For someone who is an experience programmer, but a Go newbie, Effective Go is a treasure trove of insights.

## Start Coding

<blockquote class="twitter-tweet" data-width="550">
<p lang="en" dir="ltr">4 strategies for learning a new programming language:<br><br>1. Use it in a fun side project<br>2. Use it in a fun side project<br>3. Use it in a fun side project<br>4. Use it in a fun side project</p>— Adam Gordon Bell 🤓 (@adamgordonbell) <a href="https://twitter.com/adamgordonbell/status/1335613480641159170?ref_src=twsrc%5Etfw">December 6, 2020</a>
</blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

At this point, if you haven't started building something using the language you probably should, but first make sure you read [How To Write Go Code](https://golang.org/doc/code.html) to learn how to organize your projects and invoke the compiler.

## Bonus Resources

When I was looking for learning recommendations from my coworkers and on [reddit](https://www.reddit.com/r/programming/) there were a lot of great links shared. Here are some of the things on my future learning list.

## Bonus #1 Go - The Complete Developers Guide

> "[Go - The Complete Developers Guide] is a very approachable solid introduction to Golang." - Eric Vallee

I'm a big fan of seeing people work. Seeing how people interact with their text editors, how they work with the compiler, and think about solving problems. If you have someone available to pair program with, this is a great way to go. &nbsp;If you don't have that access then video courses are great.

[Go - The Complete Developers Guide](https://www.udemy.com/course/go-the-complete-developers-guide) is by Stephen Grider and covers everything from setting up VS Code to channels and goroutines. &nbsp;I've not taken the course, but I am a fan of Stephen.

<blockquote class="twitter-tweet" data-width="550">
<p lang="en" dir="ltr">A lot of people ask me what language they should learn.<br><br>&gt;&gt; Golang (Go)!!<br><br>100% the best language out to learn &amp; build stuff.<br><br>Here are <a href="https://twitter.com/udemy?ref_src=twsrc%5Etfw">@udemy</a> courses by the amazing <a href="https://twitter.com/Todd_McLeod?ref_src=twsrc%5Etfw">@Todd_McLeod</a> with discount codes.<br><br>Buy &amp; take the learn to code Go &amp; web programming ASAP<a href="https://t.co/kpW2rxmxiZ">https://t.co/kpW2rxmxiZ</a></p>— MARCUS 🏴‍☠️ 🇳🇬 🇺🇸 (@marcusjcarey) <a href="https://twitter.com/marcusjcarey/status/1273086021312425991?ref_src=twsrc%5Etfw">June 17, 2020</a>
</blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Go Courses by [Todd Mcleod](https://www.udemy.com/user/toddmcleod/) are also highly recommended by people online.

### A Bit About Udemy

At my previous employer, I had an all-you-can-eat Udemy package and I used it quite a bit. &nbsp;What I found was the quality of content on Udemy varies widely. &nbsp;Some courses are just not good. Some have good parts, but are padded out with extra or outdated content. If you are going to buy an Udemy course, see what is recommended by others or see if there is a previous author you like.

The Stephen Grider course its on my todo list specifically because I did Stephen's [Docker and Kubernetes course](https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/) in the past and enjoyed it. &nbsp;I like his approach to teaching, which involves having you typing out and running code as you go.

## Bonus #2: Distributed Services with Go

![Distributed Services With Go Book]({{site.images}}{{page.slug}}/images.jpeg)\

> "For me the main motivator for learning go was that it was kinda like Erlang with regards to goroutines / message-passing concurrency model, but with none of the performance drawbacks." [Vlad A. Ionescu](https://twitter.com/VladAIonescu)

Everything covered so far fits into the beginner and language intro category. &nbsp;But I mentioned at the beginning my interest in go was related to all the great cloud and distributed computing happening in Go. &nbsp;That is what got me interested in [Distributed Services with Go](https://pragprog.com/titles/tjgo/distributed-services-with-go/) by Travis Jeffery.

> "Go has become the most popular language for building distributed services as shown by projects like Docker, etcd, Vault, CockroachDB, Prometheus, and Kubernetes. Despite the number of prominent projects such as these, however, there's no resource that teaches you why or how you can extend these projects or build your own." - Distributed Services with Go

At the time of writing the book is only in beta and I have only read the free 1st chapter but it looks like exactly the type of book I need.

## Bonus 3 to N: More Resources

### Web Resources

- [Go Lang Bootcamp](http://www.golangbootcamp.com/book/intro#cid1)
- [Learn Go with Tests](https://github.com/quii/learn-go-with-tests)

### YouTube Talks

- [Go Concurrency Patterns by Rob Pike](https://www.youtube.com/watch?v=f6kdp27TYZs)
- [Golang University 101 Playlist](https://www.youtube.com/watch?v=rFejpH_tAHM&list=PLEcwzBXTPUE9V1o8mZdC9tNnRZaTgI-1P)
- [Golang University 201 - Intermediate Playlist](https://www.youtube.com/watch?v=yeetIgNeIkc&list=PLEcwzBXTPUE_5m_JaMXmGEFgduH8EsuTs)
- [Golang University 301 - Advanced Playlist](https://www.youtube.com/watch?v=YHRO5WQGh0k&list=PLEcwzBXTPUE8KvXRFmmfPEUmKoy9LfmAf)

### Lists of Resources

- [A List of Go Resources](https://golangresources.com/)
- [A List of Go Advocates](https://docs.google.com/document/d/1Zb9GCWPKeEJ4Dyn2TkT-O3wJ8AFc-IMxZzTugNCjr-8/edit)
- [Resources for new Go Programmers](https://dave.cheney.net/resources-for-new-go-programmers)

### Go Books

Here are some great resources for further learning:

- [Concurrency in Go: Tools and Techniques for Developers](https://www.goodreads.com/en/book/show/30413199-concurrency-in-go)
- [The Go Programming Language](https://www.goodreads.com/book/show/25080953-the-go-programming-language)
- [Head First Go](https://www.goodreads.com/book/show/36800891-head-first-go)

Take advantage of them to deepen your understanding of Go. And if you're diving into Go, you might want to check out [Earthly](https://www.earthly.dev/) for efficient and consistent build automation. It could be a valuable tool in your Go development toolbox.
