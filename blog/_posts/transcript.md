# transcript

[00:00:00] **Adam:** So welcome Benji to the inaugural earthly video interview. Thank you for joining me. I'm wondering if you could tell everybody who you are and, and what you do.

[00:00:12] **Benjy:** Sure. First, thanks for having me on. It's really great to, to be here. My name's Benji. I am a software engineer. Have been working as a software engineer for over 25 years now. Today, in my most recent role, I am the CEO and co-founder of Tool Chain, which is a company in the build system space.

[00:00:31] **Benjy:** And it's built around an open source build system called Pants, which I am one of the co-creators of, and one of the current maintainers of. So that's what I'm best known for.

[00:00:42] **Adam:** I'm wondering if you can take me back, you know, two, two year days at Google

## A Builds were slow, no one cared

[00:00:47] **Benjy:** So we're going back in the midst of time to the late nineties when I graduated from university and started my first jobs out out of college and as a, as a very junior software engineer and, You know, when you are very junior, you sort of accept things as given to you.

[00:01:05] **Benjy:** And so I worked at a company that just had a big old c plus plus code base using a big old make file, and things were very slow and took forever, and there was just a perception that this was almost part of the mystique of software engineering. Like things are supposed to be hard and slow and flaky and broken and require huge amounts of.

[00:01:25] **Benjy:** You know, by late nineties standards, so what was that like half a gig or something? And that's just how it is. And you accept that and you don't really think anything of it. And people who may be familiar with that famous sex k c d comic of engineers rolling around the office, playing with lightsabers using the excuse of their codes, compiling.

[00:01:43] **Benjy:** That was basically life like, I'm going to go have lunch because my code's compiling. . Then I worked for another smaller company that the, the scale problems were this company was smaller. The scale problems were not quite so noticeable, but nonetheless, there was no strong tooling or strong processes, and that just seemed to be how it was in most places in the industry.

## B Google cared about builds

[00:02:05] **Benjy:** And I moved to the us. I ended up working at Google and. was very taken. This was the early two thousands with Google also had a big make file that was very slow and and builds were clunky. But the really interesting thing there that stayed with me to this day was the attitude was so different.

[00:02:29] **Benjy:** The attitude was not, this is the fact that this is slow and broken and hard and messy is part of the mystique. The attitude there was no, we should fix. This should be fast and easy and fun. And software engineering is a discipline, and we have it within our power to improve our own discipline. We can come up with good practices and we can build tools that not just support those practices, but enforce them.

[00:02:56] **Benjy:** And so that was where I think my present day interest in this space really began was with that observation that. Oh, actually, unlike many, most, I think pretty much all other professionals that don't have it within their power to create their own tools. Or if you work in sales and you want better sales tools, you have to find a software engineer to do it for you.

[00:03:16] **Benjy:** But we are software engineers and the tools that we use are themselves made outta software. And so we have it in our power to fix this. And Google was where I first encountered that attitude of, it's not like things are great, but we aspire for them to be much, much better than they are, and we do not accept.

[00:03:33] **Benjy:** The mystique argument for why things are bad.

[00:03:35] **Adam:** Why do you. . Google had that attitude and, and also like, so what did they.

[00:03:41] **Benjy:** So at the time there was just a big old make file that took a really long time to establish its state. You start, you'd fire it up and it would pass the make file, and then it would have to stat many, many, many thousands of files on your, at the time spinning disc. And so, it, it was just very, very slow to even start up, to get to the point where it could figure out what work needed, what compilation work needed to be done, let alone doing that compilation work or running tests or whatever.

[00:04:12] **Benjy:** And Google was, I think, very, even, even in those early days, very, very ambitious. So I think that was part of it. A lot of people looking f projecting into the future and saying, well what? What happens when we're 10 times the number of engineers and our code base is a hundred times as big? This isn't even working well now it's not gonna work.

[00:04:30] **Benjy:** Then I think there was also a strong sense of Google of organizational, the tooling and the code base architecture must promote organizational unity. Many organizations solve this problem by fragment. They're code base along team lines and just saying the right, you know, the, the every piece of the organization, every piece of functionality, every system, every service, every product will just have its own code base and they will not interact.

[00:04:57] **Benjy:** And Google was, for various philosophical reasons, very against this. And I think with hindsight, justifiably so. And in particular, , they recognized quite early that it is very hard to share code across fragmented code bases. How, how? Like, how do you even do that? Particularly in that they were using c plus plus very heavily at the time.

[00:05:24] **Benjy:** And so there are no, you, you can't sort of publish a built artifact like a jar file or a, or a wheel and say, consume this at some version. Right. You, you have to actually consume code at source. And so

[00:05:39] **Adam:** Yeah. Even package management right now in c plus plus isn't very mature, right? I, I

[00:05:44] **Benjy:** right. And it's, it's a hard problem in general because of the version hell problem, which I think very early Google was recognized as being a huge problem and was why cross code, code-based packaging was not a thing.

[00:06:00] **Benjy:** So, , I think just a lot of ambition, a lot of smart people who had good intuitions about the problem space was why

[00:06:09] **Benjy:** they Google in particular really focused on, on this problem. I'm sure they weren't the only ones. Un undoubtedly, for example, Microsoft have excellent processes and tooling in this space. I, I'm not familiar with them cause I've never worked there, but I'm certain they do. But anywhere where you have. , a big ambitious team full of smart people who've been around the block.

[00:06:31] **Benjy:** They will recognize this problem and solve it. I think that's another thing is there were a lot of people at Google for whom this was not their first rodeo, so there were plenty of people at the time, Google was hiring a lot of new grads who like me, years previously. just accepted things at face value, but they also hired enough people who had enough experience to know that they could start seeing patterns from previous jobs, repeat themselves and say, Nope, not this time, not gonna fall for this, this time.

[00:07:01] **Adam:** Those feedback cycles can kill you. So what do they.

[00:07:06] **Benjy:** I mean, keep in mind, this is almost 20 years ago, and so my memory's a little hazy, but the first step was, To use dependency information provided in, in so-called build files to constrain the problem and say, well, I'm actually only working on this file, so really the only bits I care about are this file and all of its transitive dependencies, which may maybe.

[00:07:35] **Benjy:** no small amount of code, but it's still significantly smaller than the entire code basin. So the very first observation there was, if we know something about the dependencies at whatever level can be at the directory level, at the file level, package module, whatever the unit is, relevant unit is in your language or in your code base.

[00:07:54] **Benjy:** But if you can constrain the, even if you're still using. , say a generated make file, but you can constrain it to just the parts of the code base that are relevant and you can use dependency information to cut out huge sways of the code base. You can limit the scope of the problem. And that was the very first thing was we should not be looking at the entire code base.

[00:08:17] **Benjy:** Every time you want to do some operation. We should only be looking at the relevant parts. And so instead of statting, you know, 50,000 files, maybe you only have to stat 500.

[00:08:29] **Adam:** So it's like generating make files for each directory off of a dependency list,

[00:08:34] **Adam:** maybe. 

[00:08:35] **Benjy:** or less, it's more generating make files on the fly based on the code you're working on. And its transitive dependencies.

[00:08:44] **Adam:** So you start with the dependency list you generate on the fly and like call it and you're off.

[00:08:49] **Benjy:** Yeah.

[00:08:51] **Adam:** And then what, 

[00:08:52] **Benjy:** Well, they kept working on this. So I think people may be familiar with the open source project, basil, which is a, an open source variant of the, their internal system which is called Blaze. I'm very unclear on why the name is different, and I'm not a hundred percent clear on the relationship between the one they use internally and the one they open source.

[00:09:12] **Benjy:** I don't believe they're the same, but they share deep design principles. I dunno how much the code 

[00:09:18] **Adam:** And all the letters. I, I think, I think

[00:09:20] **Benjy:** and all the lessons. Yes, no, definitely a strong anagram game there. But they were building slowly towards Blaze, which you know, came on. Over the next, like, bits and pieces of it came online over the next few years.

[00:09:35] **Benjy:** There was, Google is not using gi. they were using per force. Per force allow, unlike GI allows you to check out only parts of the code base. So it's a very, very different model than what maybe many people are familiar with with Git.

[00:09:51] **Benjy:** And so one thing they could do, given all this dependency information from these build files which you know, had to be written anyway, was. Actually, I don't even need all those files that are not relevant to the work I'm doing. Don't even need to be on disk, locally on my machine. They had they developed something called Source Affairs.

[00:10:13] **Benjy:** It was just essentially a file system overlay that let you see reference any version of any source file as a file and eventually, Object Fs, which allowed you to, essentially the object files you were building were, was stored on some network file system. And it was sort of accessible over the network.

[00:10:33] **Benjy:** So a lot of bits and pieces, very clever ones that came online over the next few years and culminated in the sort of more modern build experience that people may be familiar with from tools like basil and pants.

[00:10:47] **Adam:** , like what did. Local build times go from to, or do you remember an impactful experience,

[00:10:53] **Benjy:** I very much remember it getting a lot better very quickly every time some new thing was launched, but of course Russ never sleeps. And so on the other hand, offsetting this was, the company was growing, so Like even if you don't hire any new engineer, But you, your team size is at the steady state.

[00:11:11] **Benjy:** Your code base is still growing because we all write a hell of a lot more lines of code than we ever delete. And even though I think we all know that deleting code is the greatest pleasure possible, the greatest source of satisfaction to any software engineer, but we, we don't spend enough of our time deleting code and we spend a lot of it writing code.

[00:11:29] **Benjy:** And so your code base just grows naturally. But then if you're also hiring like crazy, your code base grows super linearly with time and so, offsetting, all those gains were the added drag of just more and more and more code, and more complexity and more dependencies. And so there were added features around which dependencies were allowed to exist.

[00:11:53] **Benjy:** Sort of is, you know, which libraries were allowed to depend on which other libraries and things like that. There were features around ownership of libraries. So if you, you couldn't submit a. Patch that touched certain files unless the owners of those files had code, reviewed your code and allowed it.

[00:12:13] **Benjy:** And every directory had like an owner's file in it to say, you know, these are the people who must review the code changes in this directory. And so they were able to distribute the knowledge of who knows what about which bits of code in some sensible way, but. . So, so there's always this tug of war between the tooling keeps getting better, but the situation keeps getting more complicated.

[00:12:36] **Benjy:** But I do think the, the big legacy there and as far as I know, still holds to this day and, and imagine at what size and scale they are now. I have not worked there in 13 years, so I really can only imagine it the attitude of. , we want one code base, essentially. I mean, obviously they have many other smaller code base, but one central repo.

[00:13:06] **Benjy:** The, the bulk of our employees collaborate on the, the unity of that thing is what promotes the unity of purpose and organization of the entire. And so instead of, we want our engineering organization to be structured as a, a loose collection of warring tribes. We have one organization, one engineering team, even if it's giant.

[00:13:30] **Benjy:** And obviously it's broken into many, many, many teams and subteams and sub subteams and so on. But the fact that we all share this common infrastructure and this common code base gives the organization even at scale a common sense of purpose. And that I think was very, very valuable. Years later, I came across.

[00:13:48] **Benjy:** A, something called I think it's Conway's Principal and this is, 

[00:13:53] **Adam:** Law. 

[00:13:54] **Benjy:** yeah, and this is not Conway. This is Conway, who was a software engineering person. And it's not a Game of Life, Conway. And he and I think the principle was that basically a system.

[00:14:08] **Benjy:** a system designed by an organization. Its internal structure will recapitulate the structure of the organization. And I think the, the the, the, the ultimate example being that if you a n teams build a compiler, then it'll be an N Pass compiler. And, and I think that's kind of true. in reverse as well.

[00:14:28] **Benjy:** So if you have your organization organized around a code base that is fragmented, then the organization will become fragmented, and that may not be what you want.

[00:14:39] **Adam:** And I'm sure the, the fans of more of a, a bottom up structure would say, That basically Google must be very top, top-down oriented to have a top-down structure in, in a large monorepo. And maybe there's advantages to T teams going their own way. I, I don't know. How do you feel about that?

[00:15:03] **Benjy:** I think there are definitely advantages and disadvantages to both, and you have to pick your poison. I would say at the very least, my , you know, essentially my life's work with pants and so on, is to make sure that you're making that decision based on what you truly want your organization to look like.

[00:15:24] **Benjy:** Derived from organizational principles and not because the tooling forced me to, because there was no other way to make my code base. So I would say at the very least, don't make the tooling or lack of it. Your reason for doing this, I would say personally having experienced both, having experienced some, you know, more bottom up teams going their own way versus pretty top down organizations, I prefer that.

[00:15:52] **Benjy:** I prefer the, I think a, a, a corporation, an organization. , an organization like a decisions, priorities, funding, resources flow top down, right? This isn't a case where wisdom of crowds is what applies. This is a case where smart management downwards is how companies succeed.

[00:16:17] **Adam:** A company is a, an authoritarian top town organization.

[00:16:21] **Benjy:** it, it is. And I've seen the chaos that ensues when you.

[00:16:25] **Benjy:** Do that. And so I'm not saying there aren't organizations out there that have not done the, the alternative successfully. I'm absolutely sure there are, but again, at least let that be a decision that is not forced on you because it is the only co base architecture that you have available to you.

[00:16:42] **Adam:** Now you said organizations. With chaos. I don't know if that's supposed to be a hint, it's transition to a Twitter story or, or,

[00:16:51] **Benjy:** I mean, when I went to Twitter, I definitely experienced a very different organizational structure in terms of that. That was a company that had, at the time, I can't remember exactly how many engines. , say a hundred or 200 or something like that, but many, many more repos than there were engineers on the team.

[00:17:13] **Benjy:** Every little library, every little project was its own repo. And there was just a lot of difficulty in sharing code. And interestingly, Twitter did in fact, over the course of the me 2010. Completely changed their coa. They merged all of those by the time they actually did this work, I think they had around 2000 small repos and they merged them all basically into one. And you know, obviously they needed the tooling for that. And there was a lot of discipline involved and there was it involved a lot of changes into how they operated, but I, as far as I know, they've not looked back from that. So I, you know, and I was not involved in any of that. That all happened after I left.

[00:17:51] **Benjy:** And so, I, when I was at Twitter, I observed this fragmentation, and independently they moved away. They chose to move away from it, and so I think that's pretty instructive.

[00:18:03] **Adam:** Instructive that the, or like the imposing the structure and finding a way to fit everything together, like leads to success, that some sort of organizational principles are easier to maintain when everybody. Knows where

[00:18:17] **Benjy:** mean, I, I'll give like the classic example of this. And this gets into sort of monorepo theory and why and I am pretty, personally, pretty opinionated about mono repos, although pants is, is fairly agnostic to it. The I go and make a change in some library. If the code is all in a monorepo, then it is very easy for me to find all the downstream consumers of my change.

[00:18:45] **Benjy:** And it's very easy for me to run their tests, and it's very, very easy for me to make sure that I haven't broken my coworker. code through my change. But if my change just lives in some separate repo and no repo has in its metadata, who consumes it. So you have no rigorous way of knowing that your changes are just being fired out into the void.

[00:19:06] **Benjy:** And someone will pick them up at some later date when they upgrade to whatever the latest version of your, of this library we're talking about is. And your changes may affect them. some, you know, really difficult way, like a a in a way that is hard for them to resolve. Now they may only do that upgrade weeks or months later, by which time maybe you've moved on.

[00:19:29] **Benjy:** And so now there are no, there is no context to your change anymore. And so consuming code written internally, consuming first party code through published versions as if it's third party code, where when I make changes, I am under. obligation to reason about the impact of my changes downstream from me, because that's impossible to do is really leads to a lot of problems.

[00:19:58] **Benjy:** I mean, I've seen this over and over again. 

[00:20:01] **Adam:** I wanna push back against that cuz to take the other side of it, you know, if I'm making an eternal library, I could publish it. I don't know, like in the Java world, like there's some sort of Maven version. . So, so that's a thing. Obviously it would be better to change everything at once, but like in the real, maybe the real world is the wrong term.

[00:20:20] **Adam:** If there's a network call in the middle you can't really change everything all at once anyways, because they're not all gonna roll out at once. Like if I, if I make an API change and then I, I changed the callers of the api, but I can't actually instantly switch all the services over.

[00:20:36] **Benjy:** No, that's very true. So, With regard to your first example, yes, you can publish a library. If, if we're in JVM land, you can just publish something at some ma coordinates and you're essentially having the rest of your own company treat your code the same way they would treat third party code.

[00:20:55] **Benjy:** Consume it by downloading it at this coordinate. But here's the problem. When someone upgrades, . So there's a couple of big problems with this. One is someone might upgrade, need to upgrade to a later version of your library because of a bug fix that's available there, or some new feature or something. And then they also pick up all those other changes.

[00:21:17] **Benjy:** And so now you've potentially. , you know, you've made a bunch of changes that may or may not break them, and there's, it's really hard to know. But the other really complicated problem, and this was very explicitly why Google did not go down this path in the early two thousands, was the famous diamond problem, right?

[00:21:35] **Benjy:** Where you end up re depending on two conflicting versions of the same. So I depend on A and B. A and B both depend on different versions of.

[00:21:47] **Benjy:** One version of C can be present. So now now we've sort of, this is the, the famous Jar Hill problem. We've now extended Jar Hill from third party code to also first party code.

[00:21:59] **Benjy:** And so, and it's bad enough in the first party realm, and it is very, it is a very, very hard problem to solve. The algorithms that attempt to solve it, a conne. It may actually be impossible, right? There may not be a version of that third library that is compatible with both A and B, but even if there is finding, it may be intractable.

[00:22:20] **Benjy:** The algorithms that solve this are all that the s solve, the algorithms that solve this optimally, at least are all NP complete. There are.

[00:22:28] **Benjy:** heuristics that, that do a pretty good job. Like you know, PIP does this for Python with a bunch of algorithms. And Google a few years ago published something called Pub Grub, which is for the Dark Package Manager, which is a general purpose algorithm for solving heuristic, for solving these problems.

[00:22:43] **Benjy:** But nonetheless, this is a hard problem. And so that's kind of where I would say doing it through publishing gets tricky. Certainly you cannot. avoid the problem of how do you roll out like, like you said, if there's a network call in the middle, then you can't avoid reasoning about how things roll out.

[00:23:03] **Benjy:** So I think what we're talking about more is compatibility at the linker level.

[00:23:08] **Adam:** Yeah, that makes sense. It seems like, I mean, maybe nobody wants to go down this road, but like a linker that could link multiple versions of things and link them in the right spots. Oh, it

[00:23:19] **Benjy:** That is something we kind of toyed with back in the day of. Well JVM for example, has you know, the concept of shading where you can rewrite the class names and, you know, could you just shade everything, like, essentially hide every library behind some anonymized name and then selectively. De-anonymize them, you know, when you have to reference because you have to also rewrite all the links and references to the code.

[00:23:45] **Benjy:** And so it's, that is an interesting approach. I think Rust does this basically, if I'm not mistaken. I am not sure on that. Don't, don't fact check me on this, but I, I, I think Rust will actually allow this, because it name angles, but you then can't pass objects across those boundaries. your APIs may need to do.

[00:24:07] **Adam:** Oh.

[00:24:07] **Benjy:** They're not of the same type in, in JVM land anymore. Once you shade

[00:24:12] **Adam:** Makes sense that yeah, they wouldn't be because Yeah. Okay. We, we've tangented it off, but like, so tell me like when at Twitter you like, like what's the build story at Twitter? Because I know pants has its birth there.

[00:24:28] **Benjy:** Twitter, I met John Soros, who is now my co-founder at Toolchain, and he had also been at Google, although we didn't know each other there, and he had the same observation I did about, wow, there's a lot of cobas here and the tooling is haphazard and there isn't any uniform way of building anything at.

[00:24:51] **Benjy:** and he had already started hacking on that problem using python scripts to generate ant XML files. Andt being the sort of jvm, the, the, the standard JVM built system at the time. And so that's where the name pants came from. It was an sort of contraction of python ants cuz you were using Python to generate ants.

[00:25:14] **Benjy:** None of that remained for very long, but the name stuck around, the name stuck around, you know, a decade after the contraction no longer meant anything real in the world. But

[00:25:23] **Adam:** I recall a event is that it was like a lot of xml,

[00:25:26] **Benjy:** there's a lot of xml. I think it, I think Ant was created in like the year 2000 ish, right? When XML was at the height of its popularity.

[00:25:35] **Benjy:** And so it was very, and XML and, and Java were also very sort of intertwined in the public imagination. And so, yeah, and xml and it was a lot of xml. So at Twitter, John had started hacking on this problem. I was using pants just purely as a user because he had written this, this thing. I started using it.

[00:25:57] **Benjy:** I needed it to do some stuff and reached out to him and, Started hacking on it. And that's where I got really fascinated with this problem. Like I said, at Google, I had seen it in action, but I hadn't actually contributed to it. I was just a user at Twitter. I started actually hacking on the thing and seeing what I could get it to do.

[00:26:19] **Benjy:** And then I just kept kind of hacking on it. And after I left Twitter and went to work at Foursquare, I quickly noticed that Foursquare had the exact same problem.

[00:26:30] **Benjy:** They had this big scholar code base, but using sbt, it wasn't scaling the solution at the time when I am not joking, was to give. , all of the engineers are stick of ram and a screwdriver. And so say, just upgrade your laptops and you can do that for a while. Right? But you can't do it forever. And that's when I realized, wait, I, I, I think I have a solution here.

[00:26:54] **Benjy:** And so reached out to Twitter and said like, how about if we just hack on this together and like open source it? And, and you know, we, we've both got big scholar co bases and so that's what happened. We. That was Pence, what we now call Pan V one to distinguish it from the current version of the system,

[00:27:14] **Adam:** How come you never like went to Google and said, why don't you open this? And

[00:27:20] **Benjy:** Oh, open source Light Blaze.

[00:27:22] **Adam:** yeah.

[00:27:23] **Benjy:** Oh God. First of all, they did eventually, but only like several years later. And even then it was really designed for c plus plus. and had JVM support, but I didn't, you know, we knew, oh, even if they do that, it is a complicated system to adopt. It is, you know, it's really designed for one code base and you can use it on other code bases, but it is not at all trivial to do.

[00:27:47] **Benjy:** And at the time we would've had to develop scholar support for it. Whereas we had this thing that kind of worked so, and was built around like a somewhat similar model. Conceptual model. At any rate. So also like who do you talk to at Google? Even at that time Google was such a behemoth. You know, I could just email Twitter peop folks I knew at Twitter and say, can you open source this?

[00:28:13] **Benjy:** And I figured they'd say yes, and they immediately did. Whereas at Google, I mean, can you imagine the bureaucracy you would have to go through?

[00:28:20] **Adam:** It's funny because like. because you have this story, right? And, and others do. I I think that Facebook's build tool has a similar backstory. The, yeah. And what about, I don't know about the AWS build tool. It might be, be similar.

[00:28:39] **Benjy:** So I think Buck outta Facebook also has like blaze in its lineage. AWS stuff is very different. They have an extremely different philosophy.

[00:28:47] **Benjy:** Around building, and so I'm not well placed to talk about it, but I believe their stuff is very, very different.

[00:28:54] **Adam:** and then like to plug Earthly, like, like Vlad who, who started Earthly, he, he had this like a similar story, but years later, leaving Google I mean, basil existed at this time, but he didn't feel like it could be used if you weren't Google. So he's like, well, what can I ? What can I 

[00:29:11] **Adam:** build? 

[00:29:11] **Benjy:** Pretty much it was designed for Google, for a giant c plus plus code base that had more or less the shape of Google's. You can use it for other things, but it's hard to do. It's hard to adopt. And we didn't feel like that was even possible. Like the idea that we could get Googled open source something we did not seem very likely at the time.

[00:29:32] **Benjy:** So that's kind of how Pan View one came to be as really there were only a handful of companies sort of scholarly using companies. early 2010s vintage using it. That was back when it seemed like Scarlet would be the next big thing and didn't quite go in that direction. So we hacked on it for a few years and you know, still also had a lot of problems.

[00:29:51] **Benjy:** Everything is a work in progress, but the, we learned a lot from it that informed the current iteration of pants, which is focused, I mean sports, many languages, but is really focused on Python because. That, you know, while everyone was looking at Skylar waiting to see if it would take off, Python actually took off.

[00:30:11] **Adam:** I mean, why does this matter so much to you? Why did you, why did you decide after leaving four Square that this is my next thing?

[00:30:19] **Benjy:** Cuz scratching your own itch is the greatest satisfaction there is. I, I love working in Python. . There were no there. There, just the Python ecosystem did not have any tooling that was really designed for big, scalable repos. Everything was sort of implicitly and sometimes explicitly assumes that your Python code base is small and produces one thing.

[00:30:44] **Benjy:** but I was used to, I want a Python monorepo. I want like, you know, I want to build a big Python code base that produces dozens of things, like many microservices and many whatever cloud functions, docker images, whatever it is you're building. I want to be able to have tooling to be really effective in that space.

[00:31:03] **Benjy:** And I, when I say me, I sort of figured. It's not just me. More and more businesses are, you know, used to be that Python was just a fancy scripting language and now people were building entire businesses out of Python and, but without the tooling. So what was the equivalent tooling for a company that was building around Python and first of all, many, many companies were now actually building their mainline code bases out of Python.

[00:31:31] **Benjy:** But even those that weren't had big data science code base. predominantly using Python because one of the reasons Python became so popular was that it is the language of choice for data science, machine learning, ai because of its good integration with all the numerical libraries. And so what, what are all those teams supposed to use?

[00:31:51] **Benjy:** And that was a problem that we were really fascinated in solving. And that's where, you know, we sort of had. ongoing project that we didn't use any of the code of really that was what we now rec on to be Pan V one. We've essentially in 2018 to 2020 rebuilt pretty much from scratch and named it Pan V two because we're pretty bad at naming things.

[00:32:15] **Benjy:** And it was a pandemic. And, you know, we already had a domain on a little bit of brand recognition, so we said Vine, Penns, Vito, it is. And that one is the p in now has come full circle, except now it. That the implementation is Python, it's that the language we're targeting is Python, 

[00:32:31] **Adam:** oh yeah. Cause it was python ants because you were generating with Python, but now

[00:32:35] **Benjy:** generally Python and files to build scar with, or Java. And now pants itself is written partly in Python, but the, the core part, the core engine is written in rust. And. , the but the target language was now Python. And so we, we reclaimed at least the p part of the name because people expect the, the Python community expects its tools to start with a letter P

[00:32:59] **Adam:** So it worked out all right.

[00:33:01] **Benjy:** well, no.

[00:33:01] **Benjy:** Good. Yeah. So, That is kind of where pants is now. It's been a long journey through Scarla, through couple of, you know, several companies. But now, if you look at the project today, it is supports, like I said, many languages, but a, it is the only system that has Python, very deeply Python support, deeply baked into its design.

[00:33:24] **Benjy:** So it's, it's caching mechanisms and it's There are many optimizations in it to support working very effectively with Python at scale like no other system has. So Basil has Python rules. In fact, I think there are several sets of them, but Basil is not really designed for this. . And we also, you know, a big part of if you build a system that you want loads of people to use, you want it to be easy to adopt.

[00:33:45] **Benjy:** And so rather than rely on handwriting those laborious build files path relies a lot on static analysis of your files. So we essentially learn the fine grain structure and dependencies of your, of your code base. And that allows us to do things like handle cycles and hair walls and all the sort of weird.

[00:34:04] **Benjy:** unpleasant, real world dependency situation. So if you want to adopt pants, you do not need to first refactory your code base or write 10,000 lines of build files. You can just kind of set it up and, and, and run with it. Yeah, that's going right.

[00:34:21] **Adam:** I guess like, I mean, it's very clear to me what a c plus plus build is. It's not as clear to me what a python build.

[00:34:31] **Benjy:** So I use the word build in the most general sense, which is everything that happens in between when you hit Save and your editor and when you have something that is ready to be deployed. And so in many cases, yes. So for C plus plus or Go or Russ, that would include compilation. And for Python it would not, although it will, should today include type checking.

[00:34:50] **Benjy:** I mean, if you are writing Python and you are not using a type checker, you are missing out on some on, on a. Fabulous tool for keeping your code base bug free. So, and that is essentially a compilation like step, but obviously the big one in that build, in the large sense, a really important step there is running tests.

[00:35:10] **Benjy:** but also formatting and running security checks and resolving third party dependencies and running code generators and basically everything that allows you to go from and, and the actual act of packaging because unlike some other languages, Python does not have a, an in a great intrinsic story for how you deploy code.

[00:35:28] **Benjy:** And so we've had to invent some of those primitives, like Pex, which is a format for, it's short for Python executable, which is a self-contained executable file that contains all of your code and all of its third party dependencies. So you, you can just deploy by copying that file into a Docker image or, or directly onto a server.

[00:35:47] **Benjy:** So a lot of the, the, those sort of concepts had to be invented. or, or formalized by us. So Python has a build, it just doesn't have a compiler or at least not a build time compiler. But again, if you're not using but, but again, if you're using type checking, which you really should be, then that is essentially a compilation step of sorts.

[00:36:08] **Adam:** Hey, I am a big fan of types. I feel like Python. I assume that people are going through their Python code bases trying to write down the types of discovering, oh my God, these are really hairy types. What have I done? But

[00:36:21] **Benjy:** Oh my God. I will never not write, I will never use un type checked Python again. If I can help it like, like type annotated python is the way to go.

[00:36:33] **Adam:** Why is Python. Why did this happen? Like why is Python grown in pro?

[00:36:40] **Benjy:** I think Python is so interesting. I mean, there, I'm sure people have written books about it. I'm sure there will be many books written about it. But I believe it was originally designed by Guido Van Raso as a teaching language, which I think where some of the like sort of semantic meaning of white space of, of indentation comes in.

[00:36:58] **Benjy:** I think it was intended to just make it readable. , and yet now it is this heavy duty industrial language that trillions of dollars of, of value are built on. How did that happen? And you think it's a fascinating topic that, a better historian than I should write, but I think it has a lot to do with the fact that it, it is at a relative sweet spot of.

[00:37:24] **Benjy:** o on, on the sort of ease, ease of use versus power scale. Like it is relatively easy to write a learn and, and be productive in Python, but it has a lot of great language features. I think it is used a lot where performance is not CPU bound. So and in the, so, you know, when, if I'm like writing a web app or something and everything is network bound then sure, like, use Python.

[00:37:56] **Benjy:** Why not? The, the fact that everything's running under the gill and is being compiled on the fly, et cetera, is not a huge deal. Or, or you know, the garbage collector is, is doing its thing like, it, it's sort of fine. And then the other big thing is, obviously I'd mentioned that Python has become incredibly popular is, is essentially the language of choice for data science.

[00:38:16] **Benjy:** And I think that is because it is well integrated, it, it is very easy to use. It makes it much easier to use some underlying numerical computation libraries. And that is because Python has a good story around native code bind. . And so it's relatively easy to put Python rappers around a bunch of complicated native libraries.

[00:38:37] **Benjy:** And so when you had specific things that were CPU bound, like a numerical computation, you could just slap a Python facade on that and get the best of both worlds. So, I don't know. By, I mean, python's fun. I love it. I, I also should say I really like rust and want to learn more. . A big pence, as I mentioned, is written in a combination of rust and python.

[00:38:59] **Benjy:** They interoperate really well and we've gotten a lot of mileage out of that. And I would say a really good place to be is I'm writing in Python, but when I have performance critical sections I write them in rust. It's not a bad place to be.

[00:39:14] **Adam:** Is it. To, I know it's easy to, to, to bring in c code from Python. Similar for rust, I guess.

[00:39:23] **Benjy:** There are layer, there are these layers that make it relatively straightforward to do. Yeah. I mean, I think the big challenge with Python in that, and, and as in everything is, as I mentioned, I think probably because of its origins as a teaching language, and then as a small scale language that was mostly used for ad hoc scripting.

[00:39:41] **Benjy:** It doesn't have, it has a lot of tooling in the small, but not a lot of tooling in the large, which is what pants aims to provide in terms of orchestrating and managing a code base that has a lot of moving parts and a lot of shared code, but also built a lot of different binaries and so on. And just to give one example like probably, you know, one of the most famous bits of Python out there is Jen.

[00:40:09] **Benjy:** which is an excellent framework that we use a lot internally, and many of pence using teams are using it to work with Jango Code. Jango basically assumes that you have just one server, right? Jango, you can write jano microservices in your repo. , you have to do a lot of hoop jumping that you have to sort of write your own hoops to jump through because Jango itself, at least the versions I'm familiar with, doesn't really provide anything, provides the concept of multiple apps, like little bits of functionality.

[00:40:42] **Benjy:** But in the end, you compose 'em all together into one server and there isn't really a story for like multiple servers and how they interoperate and so on. And so you have to invent that. And so, yeah, I mean, Python just sort of grew up. It came from the streets, so to speak. I mean, and it looks the way it does because it wasn't designed by committee.

[00:41:02] **Benjy:** Right. And Java looks like it does because it was designed by committee. And there's strengths and and weaknesses to both approaches. And you have to pick your poison,

[00:41:11] **Adam:** What's the, there's the clip about, there's the languages that the people complain about and the languages that no one uses. 

[00:41:18] **Adam:** It's like the 

[00:41:19] **Adam:** So one reason, you know, I wanted to to talk to you was, especially I guess, you know, I'm trying to put together these, these interviews for Earthly, and I feel like we both, I assume, really care a lot about developer productivity and builds and Yeah.

[00:41:42] **Adam:** I'm curious why you, why, I mean, assuming that you think this is an important area, like why you think.

[00:41:49] **Benjy:** I think there's that phrase like the shoemaker's children go barefoot. I think we have just done way too much of that historically for various reasons. I think. I mean, that saying is a saying for a reason. I guess it must be common across professions that you pay less attention to your own needs, to using your skills to solve your own problems than you do those of other people.

[00:42:10] **Benjy:** I think if you worked at, you know, a Google or Facebook or Amazon or wherever, you maybe didn't want to, it wasn't cool to work on this problem because the, you were solving an internal problem. You wanted to work on search or ads or Gmail or whatever the cool thing was to work on. You didn't want to. So you, you have to be really fascinated by the problem to want to it.

[00:42:33] **Benjy:** You know, so I think the, the solutions to that were understaffed because, and, and, and underemphasized. Because if, you know, if you're at a company, you as an engineer want to work on the company's external facing, like the thing they sell, the thing that makes them company big and famous, and not the internal tooling, but also the company itself.

[00:42:53] **Benjy:** It's always very easy. incur technical debt and just say, well, we'll solve the, you know, build time problem tomorrow, because today, you know, G is crashing. So I think I, I, I, look, I, I see this problem space that is just not been given enough attention. And then, you know, and I had this experience. Of seeing a company, namely Google, paying attention to it and, and how might, what dividends that can yield.

[00:43:26] **Benjy:** And I imagine it's the same for the folks at Earthly and I think there's some similar trajectories there, right?

[00:43:32] **Adam:** Yeah.

[00:43:33] **Benjy:** Lad and others.

[00:43:34] **Adam:** Yeah, definitely. Like, you know, I feel like feedback, like the, the rate of feedback and the consistency of feedback that you get is, is like so important and, but like we don't take it seriously as developers. Like I've been on projects where like, yeah, the build takes a while and then it fails. 30% of the time. And so , and so you like, yeah, I'm gonna take my Friday and fix it. But then I don't know, like I'm measured on actually shipping features and not messing around with the build. So practically I'll just hit rerun or there's some tests that don't always work and whatever. I'll, I'll comment them out.

[00:44:13] **Adam:** Or like, as you said, it's an underinvested in area, but when you work in an environment, I think you get used to it, right? If there's that tax, like you were. You know, oh, the compile is slow, like big deal. That's just, you know, that's just how it is and everybody in the company deals with that. So whatever.

[00:44:30] **Adam:** Right? But then when you work and you get this quick feedback, right it's just you can get stuff done so fast. And I think like in the python world with the notebooks, right? I think the success of notebooks and like the data science people building things that way, it's just that there's immediate feedback and you're kind of.

[00:44:49] **Adam:** you know, like a, like a re or something. I, I don't know. I feel like it, it's such an important problem to, to give people ways to re, you know, what's happening, I guess.

[00:44:59] **Benjy:** Yeah. I think an example of how much work there is to do in this space is the fact that earthly and pants are so different in their approaches, and yet both like. on a complimentary, but really fill in like these needs, the, these similar-ish, like different enough that these two systems make sense independently, but, but needs in the same space.

[00:45:26] **Benjy:** So like there's, there's, there's so much open space here to fill with good technology that two systems with radically different architectures and radically different approaches can. Both very useful in their own right and also complimentary. And so it's not like, oh, this is just like a, a little bit of, of a gap here.

[00:45:48] **Benjy:** And like it's very obvious what the architecture is that will solve this. And so someone should just build that and then we'll be done. It's like, no, this is a big wide open fieldware pants and earthly and others are still pathfinding in this space and there's room for a hell of a lot of innovation.

[00:46:03] **Benjy:** The. we are working on and you are working on, and loads of other people are working on and still more, that hasn't even begun yet.

[00:46:10] **Adam:** Yeah, that's interesting. I've never thought of it that way, but it's a very good point, right? It's like if we were just getting small incremental gains in builds, then we would both be doing the same thing, but we. , you're coming from the bottom. We're coming from the top and, and we're both seeing like large improvements that people are excited about, which implies there's just a lot of waste, just like so much

[00:46:30] **Benjy:** That, yeah. and I think, you know, really interesting there are just really interesting technology challenges here. When I think about sort of what, how Earthly does what it does, like looking Yeah. Like chipping away from the top down. How can I make this slowly more, you know, break things up incrementally and, and, and provide a ton of organizational rigor that way.

[00:46:53] **Benjy:** And we are sort of coming, like you said, from the bottom up of like, how can we use static analysis to like, look at thousands of little tiny bits of work and sort of cash them and and unifying them and bring them together. Really different approaches. Both really, I think both useful and challenging and also frankly, fascinating.

[00:47:15] **Benjy:** I mean, I won't lie like the, probably the main reason I'm working on this is that I find the problem absolutely fascinating and it's scratching my own itch. So I'd worked at Google, I'd worked at Twitter, I'd worked at Foursquare, and when I was looking for my next thing to work on, I was fairly confident.

[00:47:27] **Benjy:** I. done with consumer internet for a while. Like I'd spent most of my career working on it, and I really wanted to work on this problem, partly because it was scratching my own itch, which I think, you know, as engineers, as I said, we don't do enough really.

[00:47:43] **Adam:** Yeah. And once, like, there's a lot of enablement that could potentially happen here. Like you talked about Scala fa famously not so fast with with the builds, right? I mean, who's to say what would happen? You know, there's more type checking you can do when you're more efficient at building things and you're doing less rework.

[00:48:06] **Benjy:** a hundred percent. Yeah. It's I remember once when I was at Four Square, Martin Osky came to visit and a lot of people complained about the compiler speed, and he's said, . I work at a research lab at a university. You're in the industry. This is a problem industry should solve. And it's like, you know, that is actually a really fair point.

[00:48:25] **Benjy:** We were like, why'd you keep piling new features on this language? You know, the compiler can't keep up. And he's like, that's my job. Your job is to make the compiler faster or pay, pay to make it faster. I was like, yep, that's actually a really good point. So here we are. I like doing exactly that. Not just for scholar specifically, but more in general, you know, and

[00:48:43] **Benjy:** It's a really fun, it's a really fun problem to be working on.

[00:48:46] **Adam:** Yeah, definitely. So where should people go to check out pants and everything. You're up.

[00:48:52] **Benjy:** Oh yeah. So pants build.one word pants build.org is the main pants website. And there's two really useful things there. One is documentation, obviously how to get started, what it all means, how it works. And then the other is links to how to get in touch with us on Slack or email usually. The best place to come and ask questions and say, hi is Slack.

[00:49:15] **Adam:** Well, this has been a lot of fun. I've learned a lot of stuff. Yeah. Thanks, Benji

[00:49:19] **Benjy:** Oh, you're welcome. I had a great time. Thanks for having me on.

