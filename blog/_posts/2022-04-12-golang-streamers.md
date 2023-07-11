---
title: "Watch People Doing the Thing"
categories:
  - Articles
author: Adam
internal-links:
 - live coding
excerpt: |
    Learn how to absorb tacit knowledge and improve your programming skills by watching experienced developers code in real-time. Discover a list of popular streamers and YouTubers who share their expertise in various programming languages, including Golang, and gain valuable insights from their live coding sessions.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about watching experienced developers code in real-time to absorb tacit knowledge and improve programming skills. Earthly is a powerful build tool that can be used to streamline the development and deployment process, making it a valuable tool for developers who want to improve their programming skills by watching experienced developers code in real-time. [Check us out](/).**

I've learned so much from watching other people code. It's never a thing I'm specifically trying to learn. It's more like someone is walking me through a problem, and they do something I didn't know could be done. Maybe they just have a low friction way to exploratory test some set of services, where I could only test things by deploying to staging, or they use some shortcut I didn't know about, and I have to ask them how they did that.

It's silly, but one improvement I learned from code pairing years ago was while debugging something with print lines. I added a `fmt.Print("here")` and then a `fmt.Print("also here")` and eventually a`fmt.Print("Do we get to here as well?")` before someone said "Use numbers". Now I'm always starting with `fmt.Print("1")`, `fmt.Print("2")`, and so on, and it makes my print-line debugging a tiny bit more productive. [^1]

To be able to professionally develop software, you need to learn the tech stack and learn how to get work done. But, to get to the next level – to become an expert – you have to accumulate thousands of tiny pieces of [tacit knowledge](<https://commoncog.com/blog/the-tacit-knowledge-series/>) that may not be written down anywhere.

>Tacit knowledge — as opposed to formal knowledge — is knowledge that is difficult to express or extract, and thus more difficult to transfer to others by means of writing it down or verbalizing it. This can include personal wisdom, experience, insight, and intuition. - [Wikipedia](https://en.wikipedia.org/wiki/Tacit_knowledge)

## 10,000 Hours?

Remember ["Deliberate practice"](https://en.wikipedia.org/wiki/Practice_(learning_method)#Deliberate_practice)? It's the idea that you can get good at chess or the violin or leet code problems via grinding out the required, properly structured practice. The ideas behind Deliberate practice are correct but hard to apply past the intermediate level in many fields because they require three things:

> First, it demands that the practice be conducted in a field with well-established training techniques.
>
> Second, it demands that practice be guided in the initial stages by a teacher or coach. This is somewhat linked to the first principle — that the practice occurs in a domain with established training methods mean that a teacher may use known pedagogical techniques to improve student performance.
>
> Third, and last, deliberate practice nearly always involves building or modifying previously acquired skills by focusing on particular aspects of those skills and working to improve them specifically. - [source](https://commoncog.com/blog/the-problems-with-deliberate-practice/)

So, it's easy to go to a Bootcamp and get up to speed on a language, but the stages past that have increasingly limited pedagogical resources and so are way harder to achieve.

Thankfully, there is [a newer school of thought](https://commoncog.com/blog/the-problems-with-deliberate-practice/) suggesting that if you aren't an aspiring chess master or concert violinist, and if you passed the early levels of skill acquisition then there is still a method of learning available to you. You need to find a way to absorb the tacit knowledge of your field. The argument from common cog, translated into the developer domain, is this:

You learn more practical intermediate skills from pairing with experienced developers (tacit knowledge) than you will learn from drilling on LeetCode problems (deliberate practice).

The problem is that code pairing doesn't scale the way the LeetCode problems do. ( Secondary concern: if you need to be good at LeetCode problems to get the job, it doesn't matter how useful they are. It's just a hurdle you need to overcome. )

## Enter Twitch

Code pairing isn't the only way to learn tacit knowledge. According to [Accelerated Expertise](https://www.amazon.ca/Accelerated-Expertise-Training-Proficiency-Complex/dp/184872652X), what you need is a way to observe experts building software[^2]. Enter YouTube and twitch streamers.

> People with expertise in thing X can now film themselves doing thing X, and clued-in practitioners can watch these experts do thing X and become really good themselves. - [The YouTube Revolution in Knowledge Transfer](https://medium.com/@samo.burja/the-youtube-revolution-in-knowledge-transfer-cb701f82096a)

You should read the common-cog series on [tacit knowledge](https://commoncog.com/blog/the-tacit-knowledge-series/). But seriously, coding streams are a minor revolution in transferring tacit knowledge. People said building a web browser from scratch was impossible but you can now watch ~80 hours of video of Andreas Kling building [a web browser from scratch](https://www.youtube.com/watch?v=4U8T6Abcv9Q&list=PLMOpZvQB55be0Nfytz9q2KC_drvoKtkpS). The implied wisdom behind building a web browser has now been made a lot more widely distributed.

So in my quest to master the tacit knowledge in a particular subfield, I've been looking for streamers and YouTubers who are building in Golang. Here is what I've got so far:

## GoLang / Cloud Native Streamers

### Robert S. Muhlestein (`rwxrob`)

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/2990.png --alt {{ YouTube Golang streamer rwxrob }} %}
<figcaption>rwxrob has been building software for a long time. He uses his stream to teach server-side programming, mainly using Golang.</figcaption>
</div>

> I'm a 54 year-old polyglot, mentor, Ashtangi, sk8ter, musician, writer, coder, hacker, gamer, traveler, dancer, art-lover, and full-time Kubernetes infrastructure engineer for a big corp.

- Online at: [YouTube](https://www.youtube.com/channel/UCs2Kaw3Soa63cJq3H0VA7og), [Twitch](https://www.twitch.tv/rwxrob)
- Notable Content: [Coding a Web server in go](https://www.youtube.com/watch?v=5RJ4sxoX9O4), [Beginner Dev Fundamentals](https://www.youtube.com/watch?v=UkE2KMsVzjQ&list=PLrK9UeDMcQLre1yPasCnuKvWvyXKzmKhW)

### Matt Layher

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/3320.png --alt {{ Go and Rust twitch and YouTube user Matt Layher }} %}
<figcaption></figcaption>
</div>

> Software Engineer. Go, Rust, Linux, networking, and open source software. On and ever upward.

- Online at: [YouTube](https://www.youtube.com/watch?v=QXg9Ds1Ldqs), [Twitch](https://www.twitch.tv/mdlayher/videos)
- Notable Content: [streaming work on an IPV6 router in GoLang](https://www.youtube.com/playlist?list=PLwYCB5_B6y--zGWkhATjfsYTFZOveHyQF)

### Michael Stapelberg

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/3850.png --alt {{ YouTube streamer and i3 creator Michael Stapelberg }} %}
<figcaption></figcaption>
</div>

> I wrote the Linux tiling window manager i3, the code search engine Debian Code Search and the netsplit-free, distributed IRC network RobustIRC. I used to be a Debian Developer, but these days I have effectively retired, aside from keeping services running.

- Online at: [YouTube](https://www.youtube.com/c/MichaelStapelberg), [Twitch](https://www.twitch.tv/stapelberg)
- Notable Content: [Working on GoCrazy (something like a unikernel for raspberry pis)](https://www.youtube.com/playlist?list=PLxMVx8p-A48CkZCPmuo7mIcjn6TK2ndQo)

### Jordan Lewis (Large Data Bank)

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/7360.png --alt {{ cockroachDB developer and twitch streamer Jordan Lewis }} %}
<figcaption>Jordan Lewis hacks on the SQL layer of cockroachDB in his stream. He also has great video and audio quality.</figcaption>
</div>

> I'm Jordan Lewis, Director of Engineering at Cockroach Labs and a Brooklyn townie. I used to work at Knewton, and before that I got my B.S. in Computer Science from UChicago.

- Online at: [YouTube](https://www.youtube.com/c/largedatabank/), [Twitch](https://www.twitch.tv/large__data__bank)
- Notable Content: [Lots of hacking on CockroachDB](https://www.youtube.com/playlist?list=PLusTLTHkFrR240f5qGJhywJuLDSxCBm_n)

### Mark Mandel

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/0330.png --alt {{ twitch live coding user Mark Mandel }} %}
<figcaption>Mark Mandel is building a game server on Kubernetes called [Agones](https://agones.dev/site/)</figcaption>
</div>
> I like writing code in just about any language that comes along. I built a career writing ColdFusion, but these days tend to focus more on Clojure and Go, and a little bit of Haskell.
>
> I have been at Google as a Developer Advocate for the Google Cloud Platform, for the past couple of years, which included moving from Australia over to California, USA.

- Online at: [YouTube](https://www.youtube.com/channel/UCviD9easAslHLWQ5RH1GCzg), [Twitch](https://www.twitch.tv/markmandel/)
- Notable Content: [Scaling a game server on K8s](https://www.youtube.com/playlist?list=PLqqp1QEhKwa5aNivDIE4SS21ehE9Zt0VZ)

### Nic Jackson

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/1690.png --alt {{ screen share of streamer Nic Jackson's micro service work }} %}
<figcaption>Nic Jackson's microservices videos come highly recommended.</figcaption>
</div>

> Developer advocate working for @hashicorp. Interested in Go microservices. Author of Building Microservices in Go and Service Mesh Patterns.

- Online at: [YouTube](https://www.youtube.com/channel/UC2V1SxXFUa5YxVJvTsrCgyg), [Twitter](https://twitter.com/sheriffjackson)
- Notable Content: [Building Microservices with Go](https://www.youtube.com/playlist?list=PLmD8u-IFdreyh6EUfevBcbiuCKzFk0EW_)

### Filippo Valsorda

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/3950.png --alt {{ Crypto Streamer Filippo Valsorda working on AGE }} %}
<figcaption>Filippo Valsorda explains cryptography solutions on twitch as he builds [AGE](https://github.com/FiloSottile/age)</figcaption>
</div>
> Cryptogopher. Go security lead.

- Online at: [YouTube](https://www.youtube.com/channel/UCYamvEaHbjh2wAf47FilxiQ), [Twitch](https://www.twitch.tv/filosottile)
- Notable Content: [Cryptography tool AGE streaming](https://www.youtube.com/playlist?list=PLwiyx1dc3P2K2zh9WA_ES7tTIZM_8Q62Z), [CryptoPals Solutions in GoLang](https://www.youtube.com/playlist?list=PLwiyx1dc3P2KoKsYdbZQutKvozOPjDilr)

### Ashley Jeffs (Jeffail)

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5420.png --alt {{ Ashley Jeffs' live streams his work on Benthos, a boring stream processor }} %}
<figcaption>Ashley Jeffs' live streams his work on Benthos, a boring stream processor.</figcaption>
</div>

> I'm Ashley Jeffs, a Software Engineer based in Reading, UK. I'm the maintainer of the Benthos stream processor and a few other popular Go projects.
>
> I basically share everything that I do either as code on Github, video talks on YouTube, or incoherent rambling on Twitter.

- Online at: [YouTube](https://www.youtube.com/channel/UCjIYEhBrw3GQwpRWe1asufg), [Twitter](https://twitter.com/Jeffail)
- Notable Content: [Build Benthos, an ETL tool](https://www.youtube.com/playlist?list=PL9hWaP-BQh2ovI1iwEKxzNFF8dVAZgHCA)

### `justforfunc`

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/6460.png --alt {{ Francesc Campoy shares screen }} %}
</div>

> I'm Francesc Campoy and I decided I want to code more often,
and to make it even better I'll be showing what I build, or at least
what I try to build, on this series of videos.

- Online at: [YouTube](https://www.youtube.com/channel/UC_BzFbxG2za3bp5NRRRXJSw), [Twitch](https://twitch.com/justforfunclive)
- Notable Content: [Advent Of Code](https://www.youtube.com/playlist?list=PL64wiCrrxh4KAal63TpN0eiPvCTNBRHi6)

### Jeff Lindsay (`progrium`)

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5070.png --alt {{ Earthly Docker contributor Jeff Lindsay }} %}
<figcaption>Earthly Docker contributor Jeff Lindsay</figcaption>
</div>

> Hello, I'm Jeff Lindsay. I'm an independent creator/programmer/entrepreneur/dreamer who, among other things, has somehow been at the forefront of cloud and developer tooling for the last 15 years. I work to make the world more generative and creative, and the world of computing more user extensible and re-combinable.
>
> For the last few years I've been working on a project called Tractor, a tool for quickly making software systems. I'll be using Tractor to build all other tools for my creative projects. I will also be sharing these creator tools, and how they're made, with the world.

- Online at: [YouTube](https://www.youtube.com/c/progrium), [Twitch](https://www.twitch.tv/progrium), [GitHub](https://github.com/progrium)
- Notable Content: [Workbench, Stream Archive](https://www.youtube.com/playlist?list=PLw1XoTpvjkthy0anlRJz5KrsxSTqmBxu6)

### GoLang Cafe

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/3150.png --alt {{ GoLang Cafe's YouTube videos are halfway between a tutorial and a live stream }} %}
<figcaption>GoLang Cafe's YouTube videos are halfway between a tutorial and a live stream</figcaption>
</div>
- Online at: [YouTube](https://www.youtube.com/c/GolangCafe)
- Notable Content: [Advent Of Code](https://www.youtube.com/playlist?list=PLLf6iaZKV_xvc13jISDXyKwPZJ2qz58zL), [Mastering The Standard Library](https://www.youtube.com/playlist?list=PLLf6iaZKV_xsp2EKR7cgRZFW5u9yVuzBi)

### Donald Feury

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/3480.png --alt {{ Donald Feury streams development }} %}
</div>
> Appalachian Boi making videos about development, linux, and games.

- Online at: [YouTube](https://www.youtube.com/c/DonaldFeury)
- Notable Content: [GoLang Concurrency](https://www.youtube.com/watch?v=GWK8Vox2MmY&list=PLSxcR40jNIvj8TzjNGNn8dwpgf7N0R4mp&index=1)

## Other Great Live Coders

I assume that the knowledge you can learn from watching live streamers is proportional to how closely their work matches your work. If you work in PHP on windows, using PhpStorm, you may not learn many low-level workflow tips from watching a Linux developer writing C in vim. But the high-level lessons about how to design a solution or how to decompose a problem, those skills can transfer across domains.

So here are some streamers worth watching regardless of your tech-stack.

### Casey Muratori (Hand Made Hero)

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/9160.png --alt {{ Casey Muratori stream }} %}
<figcaption>
Casey has been building a game from scratch on Twitch for years now. 600+ episodes are up on YouTube. He is a passionate presenter with lots to teach.</figcaption>
</div>

> <http://handmadehero.org> is a project designed to capture and teach the process of coding a complete, professional-quality game from scratch.

- Online at: [YouTube](https://youtube.com/c/MollyRocket), [Twitch](https://twitch.tv/handmade_hero)

### Andreas Kling (Serenity OS)

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/9600.png --alt {{ SerenityOS Stream }} %}
<figcaption>Andreas Kling and the SerenityOS community are building an operating system from scratch and live streaming a lot of it.</figcaption>
</div>
> I'm currently working on SerenityOS, a from-scratch operating system that tries to make Unix fun again.
>
> I've been writing C++ for many years at companies both big and small. There's a pretty good chance you're reading this in a browser that's slightly faster because of me.

- Online at: [YouTube](https://www.youtube.com/channel/UC3ts8coMP645hZw9JSD3pqQ)
- Notable Content: [OS from Scratch](https://www.youtube.com/playlist?list=PLMOpZvQB55bczV5_3DxTLDm37v_F6iCKA), [Web Browser from scratch](https://www.youtube.com/watch?v=4U8T6Abcv9Q&list=PLMOpZvQB55be0Nfytz9q2KC_drvoKtkpS)

### Andrew Kelly (Zig Creator)

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/0150.png --alt {{ Andrew Kelly stream compiler work }} %}
<figcaption>Andrew Kelly often streams Zig compiler hacking.</figcaption>
</div>
> I am an open-source contributor, best known for creating the Zig Programming Language. I am employed by the Zig Software Foundation. Open-source software, game dev, music production, and other curiosities.

- Online at: [Vimeo](https://vimeo.com/andrewrk), [Twitter](https://twitter.com/andy_kelley)

## Send Me Your Tacit Knowledge

So that is a wrap-up of online streamers I am aware of. I tried to focus on Golang people who are streaming their work. Many people create great presentations and tutorials, which are more time-efficient to consume. But, you want to watch an expert at work, not them giving a presentation for tacit knowledge.

I'm sure there are many great streamers that I've missed. Who am I missing? Let me know.

## Implicit CI Know-How

What does this all have to do with Earthly? Isn't Earthly a build tool?

Great question. Earthly is a great piece of engineering, but what makes Earthly exciting is that it encapsulates some previously tacit knowledge of the Earthly team directly into a build tool. Values like [Versatility, Approachability](/blog/platform-values/) and making CI developer-centric.

Also, I just wanted to write up a list of great online programming streamers and explain why they are a valuable resource. But while you are here, take a moment to check out Earthly.

{% include_html cta/bottom-cta.html %}

[^1]: This example is not great, but it's hard to communicate examples of tacit knowledge easily. It's subjective and not formally expressed by definition.

[^2]: You also need a method for extracting and absorbing this knowledge. See [NDM](https://commoncog.com/blog/how-to-learn-tacit-knowledge/) for that. Or for a first approximation: emulate what the experts do.