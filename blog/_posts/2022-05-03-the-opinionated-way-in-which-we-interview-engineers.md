---
title: "The (Opinionated) Way We Interview Engineers"
categories:
  - Articles
toc: true
author: Vlad
published: true
bottomcta: false
excerpt: |
    
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. As an engineer, using Earthly can help you optimize your build process and manage complex software projects more efficiently. [Check us out](/).**

Interviewing engineers is an impossible task. You have to use a few hours to figure out if a person will be a good employee for several years to come. No process will ever be perfect and the various approaches out there each come with their pros and cons.

I always found an interesting correlation between the interviewing standards and the quality of people I've had the pleasure of working with. When the interviewing process severely lacked proper challenges, surprise! the staff was also of lower quality.

I've heard some people complain about "the whiteboard interview" as being outdated (which, I agree in many ways, it is). However, replacing that with just a chat about previous experience + behavioral questions alone is far worse: you can learn some things about a person's personality, but you won't know jack about how they will perform as an engineer.

Across my career so far I've worked in both big and small companies, across industries ranging from Telco (EE - TMobile & Orange in UK), to Cloud infrastructure (RabbitMQ), to Virtualization (VMware), to Ads and Search (Google), and finally to founding two of my own companies in Security ([ShiftLeft](https://shiftleft.io)) and Developer Tooling ([Earthly](https://earthly.dev)). I have been interviewed ~20 times throughout my career and have interviewed others hundreds of times.

There are many facets of a "good interviewing process". What is important to you will vary greatly depending on the company culture and the vertical that your business is addressing. Here is a non-exhaustive list of things to measure:

- Verifying the level of experience
- Testing problem-solving skills
- Testing domain-specific knowledge
- Testing solid understanding of CS fundamentals
- Checking general culture-fit
- Ensuring potential for growth
- Ensuring experience in similar role-specific situations
- Ensuring remote work culture
- Ticking every checkbox in the job spec requirements
- Company-side overhead (interviewers' time, general cost)
- Deciding without burdening the candidate with a lot of work
- Meantime to decision from start to finish

None of these different facets are unimportant. However, as you tune the interviewing process, you will focus on a few specific ones primarily, thus making inevitable trade-offs, depending on what makes sense for you strategically.

In addition, no format is perfect. Perhaps the ideal test of a candidate's fitness is trying out the candidate as an employee for a few months and then deciding. In the real world, that has the disadvantage of extremely high overhead for both the company and the candidate, not to mention the high latency of the decision-making process. What if the candidate doesn't work out? Well, you've wasted several months.

On the other side of the spectrum, making an offer based only on 15 minutes of meeting someone would be the opposite extreme case, where there is low effort and low latency, but the fit will almost always be inferior.

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/1000.png --alt {{ Interview process time vs accuracy }} %}
</div>

The interview is a trade-off between effort, latency (time spent with the candidate), and the accuracy of the process.

As the interviewer (or the founder or manager designing the interview process), your task is to create the setup yielding high accuracy and recall, yet low overhead of process and low latency to reaching a decision.

Here is how we at [Earthly Technologies](https://earthly.dev), have thought about this and tuned our process to optimize for the things that matter to us. I should preface this by saying that this is probably not a perfect system (no interviewing process is). Also, this is tuned for our needs (early-stage startup), which might differ from the needs of a later-stage company or a tech giant. We look for some specific things: strong problem-solvers with a solid technical background, fit for being nimble and adaptable, fit for working in small teams, can wear many hats, and can improvise when needed to. These specific attributes are essential for us, but might not be important to every company. We're constantly learning and improving and I'd love to [hear your thoughts](https://twitter.com/VladAIonescu) if they are different from ours.

### Things We Avoid in Our Process

Before going how our interviewing works, I'll first share what we do NOT do. These are things that might seem good ideas (or were good ideas sometime in the past), but we think they are not helping in our case.

**Avoid pure algorithm & data structure / TopCoder / LeetCode style challenges** - We generally don't agree with this kind of testing because it's easy for someone to train specifically for this kind of challenge and get ahead via prep (and the prep doesn't necessarily improve real-world skills - they only improve interview performance). Unless what the candidate has to do at work involves coming up with innovative algorithms, involving heavy data structure theory and all that, this will not test real-world fit. It might test problem-solving skills, but because there is a clear way in which the candidate can train for this, then this ends up being a noisy criteria. Challenges in this category are sometimes called "whiteboard interview" challenges. Some people don't like "whiteboard interviews" for the reasons mentioned here, though I don't think the whiteboard itself is the issue - the whiteboard is just the medium in this equation.

**Avoid challenges that require getting the program right** (possibly compiling and running it) - we try to avoid focusing on absolute correctness in an interview. It is far more critical to check that the reasoning is sound or the process or getting to the correct reasoning is good, not that every detail of the solution is correct. Focusing too much on the details will have two unwanted consequences: 1. the candidate will focus too much on syntax, code structure, and code design, and not enough on solving the actual challenge; and 2. it will introduce noise in the testing process as under pressure some candidates will get the details wrong.

**Avoid testing knowledge primarily**. While every interview process will have experience expectations, we limit it to simple questions like "have you worked with gRPC", or "how many years of Go experience do you have". We generally don't try to catch our candidates on knowledge gaps. I've worked with some wickedly smart people, who either had a focused level of experience, and thus there were entire areas of engineering they didn't have the opportunity to dabble with, or who have simply never encountered a specific technique, feature, situation, or method, in their day-to-day. If we simply tried to test everyone that they meet a minimum knowledge bar, all we would have done was to ensure that everyone is at the very least mediocre. This is not a good test for finding world-class talent. (Note that for some more specialized roles, like Security Researcher, or Operations Engineer, there is some amount of knowledge testing too. But it should not be the primary criteria).

Usually, we **try to avoid take-home exercises**. While we think that take-home exercises are more accurate than live interviews, the downside of take-home exercises is that they take time and oftentimes smart people are busy. The biggest problem with take-home exercises is high rates of process drop-outs. And because it's the smart people that tend to be busier, you're "weeding out" the right candidates unintentionally. But if someone does strongly prefer doing a take-home exercise, we generally limit it to 8 hours of effort. This is to limit the candidate's time investment (thus keeping drop-out rate in check), but also to limit the process latency (thus to stay competitive and be able to make an offer as early as possible - ideally before the candidate has even had the chance to start the process with another company). At the end of the take-home exercise, we ask the candidate to present their exercise in front of an internal audience. This often uncovers the thinking behind some of the design choices - which sometimes is more important than the exercise itself.

### Our General Principles

Our process focuses on the idea that you're encountering novel problems to solve every day in engineering. Almost every function you write, every system you design, and every platform you operate in production will have unique aspects that you've never seen before. Unless you are a good problem solver, no amount of knowledge or experience will help you solve completely new challenges.

Engineering is all about finding solutions to unique situations. Therefore, you're better off with people who can intuitively find any solution rather than those who know some answers but cannot derive more. People with excellent problem-solving skills will also have a high degree of knowledge as a side-effect of their experience. However, the reverse is not true.

Or like [Albert Einstein liked to say](https://quoteinvestigator.com/2013/01/01/einstein-imagination/)... "imagination is more important than knowledge".

For this reason, **we test primarily on pure problem-solving skills** (see later in this article on the specifics of **how** we test for this), and generally take the candidate's word for it when it comes to level of expertise with a topic or technology.

In some specific roles, we do test some knowledge too, but this is primarily a safety check - e.g. the candidate might have to operate independently in an area where another expert can't verify their work, so we better make sure that they are indeed an expert in that area; otherwise, there may be catastrophic consequences that get uncovered much too late.

#### The *Spark*

Besides problem-solving testing, we also look for **some unique spark**. This notion of *spark* can get subjective, although it has to be, as you can never devise a genuinely objective process that selects geniuses consistently. World-class talent is extremely diverse - the reason someone ends up being of world-class caliber is very different from one person to another. But at a high-level, we're looking for something remarkable in some unique way that is useful to the company. By this definition, the interview process should have enough slack in it, to give the candidate the freedom and opportunity to be able to showcase unique, remarkable capabilities. (See later open-ended questions)

Here are some examples of *sparks*:

- **Unusually fast career growth** - (e.g. raising to team lead, people manager really fast, or owning a really important piece of the infrastructure or of the product despite relatively low experience). Generally, we found this specific indicator to be one of the most accurate ones for finding world-class talent.
- **Unusual creativity in devising a solution to an open-ended problem** (as long as the solution really does make sense and is not just [weird](https://earthly.dev/blog/dont-be-weird/))
- **Was involved with the early team of a world-class product** (commercial or open-source)
- Is the **author of a popular (or quickly growing) open-source project**, or the **author of a truly unique and useful project** (even if it did not end up being popular)
- Was **consistently involved in cross-functional effort coordination** in particularly gnarly organizational setup - e.g. has a flair for navigating political waters.
- **Have reinvented themselves** - e.g. were in a position where they had to start from scratch, and they rose up really fast. The most common example is having navigated a career switch, yet their skill level is comparable to a CS major's.
- **They are a unicorn** - i.e. they are the rare individual who is highly skilled in more than one domain or sub-domain (e.g. frontend and backend, or UX design and frontend engineering, they are strong in both operations and in backend engineering). These candidates are the best especially when you want them to own more the two areas, or to be a key cross-functional collaborator across two teams.
- **They are a true generalist** - they have worked in so many unique sub-domains of computer engineering that they have developed a special flair for handling new problems. It's oftentimes very difficult to study those domains one-by-one in depth in advance, so these people have generally developed unique skills for tackling situations they have never seen before - because their diverse experience have forced them to.
- **They are a wildcard** - this is kind of like a generalist unicorn. No matter what the task is, they end up being good at it. These people are some of the rarest to find, but they are **extremely** valuable. Usually, the only problem with this person is convincing them why they should work for you when they can start their own company. Good founders are in this category.
- **Their content has gone viral** - this can sometimes be noisy, but smart people sometimes have written really good content that other smart people find useful. The one challenge with this category is that you might have higher than usual competition in convincing them to join your cause, as they may have become popular in the process.
- **Unusually passionate but consistent references** - sometimes some people's work ends up being relatively private to the companies they worked for. However, their former colleagues would have had a lasting impression. Because the candidate gives references, it's best to discount one-offs and maybe even two-offs. But if all references are stellar, this would be considered a *spark*.

- **Nothing** - sometimes it's important to recognize that your actual skill as a recruiter is finding the hidden gems – the diamonds in the rough. There will be people out there that haven't had a chance to showcase their true colors. Finding a *spark* isn't necessarily a strict criteria, especially when it comes to lesser experienced candidates who haven't yet had the chance to prove themselves. However, a very experienced candidate with no spark can turn into a red flag, since you would assume that there would have been many opportunities during their career in which they could have proven unique talent.

Most *sparks* will generally be visible during resume review and/or the first "get-to-know-each-other" interview. But note, the above isn't an exhaustive list - anything unique, difficult to attain, remarkable and useful to the company can qualify.

A counter-example of a *spark* is someone coming from a reputable company, known for high-quality engineering. Ex-Google, ex-HashiCorp. The fact that they simply worked there isn't enough. A pedigree can definitely be a significant positive, but it takes key contributions within that company to really be a *spark*.

Also, **don't get star-struck**. Just seeing a *spark* isn't a guaranteed fit. Keep your eyes open and assess the candidate in all other ways too. A *spark* should never give the candidate an automatic offer. You still have to run through the rest of the process to 1. validate the spark really exists, 2. confirm that the problem-solving skills are adequate, and 3. to make sure they are not an absolute jerk or cowboy who doesn't play well in a team.

#### Culture Fit

This brings us to the third large category of things we test for: **culture-fit**. The only thing worse than an incompetent person is a capable asshole. This can fall into two categories: the kind that is just unpleasant or difficult to work with and the downright toxic kind. Neither is great, and the cost can vary from case to case, from the mere time wasted looking for the right person and having to start over to the much more severe long-term influence the behavior might have upon the behavior of others. It's best to catch culture misfit early and nip it in the bud as the cost in extreme cases can be immeasurable.

Never. Compromise. On. Culture. Fit.
It's not worth it.

There is no specific interview format or test for the culture-fit. It's much more of a (somewhat subjective) feeling when interacting with the candidate throughout the entire process. Everyone is friendly during the interviews, so it is hard to tell. But as you develop experience in reading people, you'll discover that you can tell sooner and sooner of specific character traits. I don't know if there is a set of tricks you can use here that are easy to describe as some kind of recipe. The way I've learned this is by doing a lot of interviews, and then getting to work long-term with the people I hired. If there was any character trait that I would discover only later, I would look back at any sign I might have seen during interviews that could have indicated that character trait. And if I couldn't identify anything, I would think about what kind of questions I could have asked to identify that kind of character trait. You also have to be careful not to over-fit or over-generalize too - you have to be level-headed and objective to the extent possible. Try to avoid [common human biases](https://www.psychologytoday.com/us/blog/thoughts-thinking/201809/12-common-biases-affect-how-we-make-everyday-decisions). I wish I could describe more specifically how this works for me, but all I can think of is just: do this consistently and mindfully, and over time, you'll notice a sensible difference in the way you assess people at first glance.

Another fascinating thing about human behavior is that the most minor habits, quirks, or behaviors that you notice in the short interactions of the interview process will represent the habits, quirks, and behaviors of the person long-term. If some trait is common for a person, there will be a higher chance of exhibiting that trait even in short interactions. Some random examples: "not answering the phone and then only responding after a full 24 hours", "mixing up something over email", "writing inconsistently (e.g. frequent errors or misspellings)", "being late - especially if it happens more than once" etc. What does this all mean? Well - that's for you to decide. Is that important for the role you're hiring for? Oftentimes, no. Occasionally, yes. I wouldn't terminate the process for missing a comma in an email - but if there is something you have a bad feeling about, and it's important for the role, it might be a good idea to find a way to keep an eye on, or double-click into the issue, if you can. (e.g. ask for code samples, if code quality and consistency is the worry)

### Red Flags

Although we don't try to "catch" candidates on something specific (remember, we're looking for a unique star, not ensuring that the candidate is simply above mediocre), there are a few cases in which we would outright disqualify the candidate because the risk of toxicity is too high. Here are some examples:

**Lying**. This often goes without saying. Trust is fundamental in a team. Lying of any kind destroys that foundation, and there is no good way to make the relationship productive. I've noticed this once when a candidate tried to give me the impression that they had worked for Google, only to discover through reference checking that they had worked together, but only on a specific project, and they were part of a different company. It was a nicely crafted half-truth, but still a very serious lie.

**Complaining about a former employer** - even if they didn't have a good experience with someone, good, ethical people will present the situation objectively, leaving the listener to draw conclusions. Toxic people will outright accuse others passionately in an interview context.

**Generally, a bad personality or a bad attitude** - this can mean many things. As this is in the red flag category, it has to be something very obviously bad: getting angry, being disrespectful or abusive towards the interviewer, or getting in an unreasonable argument.

**Not answering a question** or **avoiding admitting that they don't know something**. This one is not very obvious, but I've noticed that smart people are extremely honest and open about what they don't know. When someone tries to deflect (and sometimes some candidates get **very** skilled in deflecting elegantly so that you wouldn't notice), something could be wrong.

I had this candidate once, let's call him John, interviewing for a security researcher position at ShiftLeft. After talking to John for an hour, he seemed really intelligent, and he seemed to know his security stuff really well however after spending 5 minutes with my cofounder (Chetan), he pulled me to the side and told me, "This guy is full of sh**!". I was bewildered at first, but I went back into the room and tried to challenge John about some specific security scenarios. At first, he tried to steer the conversation back to his past projects and interesting war stories from the trenches, but as I pressed more about a real answer, I realized that he was clueless, even on some of the more basic stuff. John was so charismatic that he gave the impression of a more skilled candidate than I had thought at first glance. Chetan was able to identify the question evasiveness much more quickly than I was.

On another occasion, I spoke to someone, let's call her Jill, about a similar role, and as I was trying to challenge her on some security scenarios, it seemed that she was trying to evade the questions. People will come up with all kinds of excuses for not being straight with you. In this case, Jill came up with the highly intellectually-sounding "I couldn't readily quote a paper on that off the top of my head", but really she was trying to say "I don't know how to approach this", but tried to sound smarter about it. Maybe this wouldn't be an outright red flag - but something to keep an eye out on if it is consistent.

Sometimes you can tell how smart someone is by how honest they are about not knowing something. Some world-class people I've had the pleasure to work with were dead-honest and blunt about not knowing how to do something. The not-so-great candidates either tried to improvise really badly, tried to evade the question or tried to cover it up somehow.

**Not being able to talk about past contributions in detail**. Sometimes this could be another case of resume lying. You'll have to assess yourself if this was something too long ago that they truly no longer remember, or simply that they have lied about that contribution. In my experimentation so far, somehow, the people who were in the "did not remember" category still didn't pass the technical interviews. Not sure whether that tells us something conclusively.

### The Process Itself

Our interviewing process itself consists of the following:

1. Interview with the recruiter (this step is optional, in case of a referral)
2. Resume review with the hiring manager (given that we're a small organization currently, the hiring manager is usually me)
3. Get to know each other with the hiring manager
4. 3 x technical interviews - pure problem solving
5. 1 x technical interview - architecture
6. Reference checking (3 x references, of which at least one should be from a former manager)
7. Offer

#### 1. Interview With the Recruiter

This is the only step in the process that is outsourced. We use external recruiters, and so we rely on them to make a rough selection through their search and their own interview with the candidate. Really good recruiters will give you decent confidence that the candidates are worth your time. You're going for something between 10-50%. If confidence is too high, volume might suffer. If confidence is too low, then you're wasting time with interviews that keep rejecting people that were not fit enough in the first place.

It is extremely important to give feedback to the recruiter on every single submission so that they can adjust the criteria. Unless the candidate is spot-on, I usually list 3 pros and 3 cons of the candidate. Steps 2 and 3 will help you devise that feedback.

For technical roles, you'll need to work extra hard at this step for diversity. Pushing the recruiter to give you diverse candidates is key at this stage.

#### 2. Resume Review

This is where you're looking for a general fit for the role. Look for

- Ballpark level of experience (number of years total, number of years of a specific key technology, numbers of years of experience delivering to production).
- Coverage of the key technologies. Don't go for the perfect match, though. Smart people can learn on the job, so missing a few is usually not a problem.
- Avoid job-hopping - staying for very little time in multiple companies.
- A mix of big and small companies. A mix is the best of everything - you develop different skills in each kind of organization. If you have to compromise, just know that going from big-company-only to a small company is the hardest. You can probably make all the other cases work, but big to small requires a special kind of mentality (e.g. needs to be able to own things and make decisions independently).
- Signs of leadership, if any - even if you're hiring an IC, leadership is a sign of the employer entrusting them with something important (because they did things right), or they stepped up themselves (which shows initiative and ambition)
- General resume presentation - grossly inconsistent layout or riddled with typos is a [bad sign](https://blog.alinelerner.com/lessons-from-a-years-worth-of-hiring-data/). Developers need to be very detail-oriented and write consistent code to play nicely in a team.
- Signs of the *spark* - if any at this stage.

#### 3. Get To Know Each Other With The Hiring Manager

This is where I spend a significant amount of time talking about what we do. If you're an early-stage startup like us, it's possible that they've never heard about you. You need to tell them why what you're building is exciting. It has an impact, and it's challenging, it makes a difference to your users. Plug customers, plug investors, plug employees. Create credibility for yourself - this is a pitch. Only remember that smart engineers prefer the less flashy kind of marketing - so remember to also be humble and factual. Also, remember that the smartest people are primarily motivated by environments in which they can learn more.

The other part of this interview is assessing the following:

- Talking about the general experience, while deep diving occasionally into interesting projects along the way.
- Getting a general feel of what it would be like to work with the candidate.
- Understanding in more detail the coverage of the key technologies.
- Look for the *spark*, or if identified during the previous step, double-click into it. Verify it.
- Assess culture-fit.
- Check that they are passionate about what you do.
- I usually like to ask an impossible question here - something that I wouldn't really expect anyone to have a complete answer. If they do, then it was clearly knowledge-based, so the answer is somewhat discounted. The more interesting thing happens 99% of the time, when they don't know the answer, but their behavior sometimes tells me something about their mode of working. Most smart people will end up with "I don't know" - but hopefully after identifying a few key concerns (why the answer is very difficult). Some junior people will naively give me an incorrect answer, because they failed to see the real concerns. A bad answer to this is usually improvising a complicated answer, while failing to identify the real issue behind the question.

At this stage, I also like to ask "what are you looking for in your next role?". This is to get some understanding of the motivation criteria that drives them as a person. This might either help you argue why the company is a good fit for them, or sometimes uncover key blockers. At one point, I had someone realize that they didn't want to work for another developer tools company. I asked them to sleep over it and give me an indication the next day, and sure enough they decided to pursue something else in the end. Was this a loss? I call this a win for the process - if they had doubts, they would have fallen through the cracks later on anyway. We just saved so much time in not interviewing a candidate that doesn't want to work for us.

Especially if you are an early-stage company and nobody knows about you, you should leave ample time for questions / challenges. Make sure it's a two-way process. You're getting to know them, but they are also getting to know you.

#### 4. Problem Solving Technical Interviews

In many ways, this part is the "meat" of the whole process. Also, this part is particularly hard because you also have to properly train others on how to do this interview. It's best that the process does not rely on a single person's perspective. You reduce risk by introducing multiple points of view.

There are a few kinds of problem-solving challenges that we like to give, but they have one specific thing in common: **the person being interviewed has never worked in that area** before. The key here is to use exercises that require the person to think from first principles about something. So when we typically start the interview, one of the first questions we ask is "have you worked in area X of software engineering before?" If the answer is yes, then we switch to a different exercise. Sometimes the exercise is esoteric enough that it doesn't require the pre-qualification question at all.

A common criticism of this kind of interview is that it doesn't match what the person will work after being hired, especially when the question is from a **really** obscure sub-domain. But remember, the reason we focus on problem-solving primarily (and not on the knowledge of applying some standard technique) is that we want to hire people who do well in new situations. So in a way we **are** creating a similar work situation - in that we make sure that the problem being presented is truly new to them. And a good way to give them a unique problem is for it to be from an obscure sub-domain.

If we instead focused on more mundane subjects -- e.g. "how does a hash-map work" -- then we would be introducing noise in the process, because whoever has worked extensively with the implementation of a hash map (or who has trained specifically on CS fundamentals) would have a significant advantage at this interview (but wouldn't necessarily be strictly better at problem-solving).

Types of good problem-solving challenges:

- **Peeling onion** - the idea that the interview question shouldn't have large leaps of intuition. Large leaps introduce noise in the process, because nervous, but smart people might just not get the idea. Instead, you want to gradually make the problem harder and harder as the candidate progresses through it. You mainly want to verify that the candidate's thinking is sound, and that they iterate towards the right solution gradually, not that they come up with a brilliant solution right off the bat. A good way to come up with a "peeling onion" problem is to think of a hard problem and then try to break it down into easier parts. Then start the interview with the easier parts, leaving the harder parts (connecting the easier parts together) at the end. Yet another way of coming up with a good "peeling onion" might be to think of a hard problem, but then change the rules in some way (e.g. think only of base cases) to make the problem easier, and start the interview with the easy versions of that problem, and then gradually turn the problem into the hardest version.
- **Real-world problem** - another category of good interview problems is a tough challenge that you've encountered in your day-to-day that can be reduced to a 1-hour interview question. The nice thing about this type that you can probably also describe the real-world motivation behind the feature from when you worked on it, which helps with setting a context grounded in reality. Just remember - the candidate must have never also encountered the same problem before. In this area, I like to give a specific time-series-related challenge - so I first make sure that the candidate hasn't worked extensively with data streaming, data pipelines and definitely not with timeseries data.
- **Open-ended** - a completely distinct category of problems is one where we talk about a very open-ended challenge. An example would be: "create an algorithm that automatically generates a maze". And there are no rules. The candidate can choose their own rules: 2D, 3D, single-solution, multi-solution, graph, bitmap. It can be anything. The only rule is that the maze has to be "cool" in some way, and the candidate can choose anything for the cool-factor. This kind of exercise is mainly meant to allow the candidate enough freedom to showcase unique abilities, while also introducing a creative element. It's another way to encourage the *spark* to come to light. One disadvantage of this kind of open-ended exercise, however, is that the responses will vary wildly and so calibration is a bit harder.

Speaking of calibration, as you, or a colleague of yours gives out a certain problem for the first time, it may be hard to assess at first what exactly to expect. For example, the problem may be way too easy or way too hard. It's hard for you to compare yourself with the candidate, because you've been thinking about the challenge for the past week. To counter for this, we recommend that a problem is taken through multiple interviews before relying on it completely. It's ok in a panel of 3 interviewers if one of them is in calibration mode.

When it comes to figuring out a solution, the medium should be either:

- A whiteboard (if in-person)
- A shared Google Doc
- A virtual whiteboard (though this can be clunky to use oftentimes)

It's best to avoid online code editors, or interviewing systems that run the code. These kinds of systems take away from the challenge by moving focus onto the correctness, style, and syntax of the code. For world-class talent, we think that it's better when the focus is simply problem-solving.

Separately, an important factor that helps with reducing noise in the process is scheduling the interviews on separate days. If the interview is in-person, this will probably not make sense due to the repeated commute. But if this is a remote interview, then allowing the candidate to rest properly will help eliminate cases where due to pressure and the difficulty of the challenges, the candidate simply gets tired and doesn't do well after the second interview of the day.

#### 5. Architecture Technical Interview

Another step in the interviewing process is the architecture technical interview. In this interview, there is some problem-solving, in the context of cloud infrastructure. This type of interview is mainly given to cloud / backend / operations engineers, so it might not apply to everyone.

An example of a challenge for this stage might be: "tell me how you would design Slack from scratch". It's very open-ended and the conversation can take the two of you in many directions. It may be helpful for you to guide the conversation towards specific aspects or challenges gradually, to still have some sense of structure. As with the regular problem-solving tasks, this challenge also requires calibration - over time you'll be able to compare roughly the level of thinking depending on the seniority of the candidate.

The principles of the problem-solving interview still apply here, but there will be some inescapable overlap with past experience (e.g. load balancers are a similar concept applicable to any company; or common infrastructure like Redis, SQL, or JWT tokens). That is generally ok, as long as the challenge itself doesn't overlap completely (for example, don't ask about designing Slack if the person that comes from an instant messaging company).

#### 6. Reference Checks

Another step in our process is reference checking. It's relatively rare that references will cause you to change your mind (<5% of the time), but when they do, there is a really good reason and will save you a lot of hassle.

In reference checks, you're looking for

- Basic checking of the role, responsibility, and length of tenure of the candidate with the company - to ensure that the candidate did not blatantly lie somehow in the resume
- The smallest sign of any negative feedback. Keep in mind that references are provided by the candidate - so it's bound to be very biased. In fact you can outright discount the extremely positive feedback for this reason - maybe they owe the candidate a favor, or they're a close friend of theirs. However, when there's the smallest sign of any kind of negativity, try to double-click as much as you can. In fact throughout the reference check you should ask "what can the candidate do better" in multiple ways, just in case one of the ways unlocks more information.

A key question I like to ask is how would they rate the professional performance of the candidate on a scale of 1 to 10. If anyone is under 7, something is really off. But even if they are above 7, it's still an opportunity to ask yet again what could the candidate do to be a 10? (yet another way of asking "what can the candidate improve"). If the candidate is a perfect 10, again, don't get too excited - the reference check is highly biased. Keep checking the other two references before you call this a *spark*.

Another good question to ask is "all things aside, would you hire/work with the candidate again if given the opportunity?". If the answer is "no", again, something is really off.

#### 7. Offer

The offer stage is one of the most important ones. You are now convinced that the candidate is worthy, so now the focus is on actually getting them onboard.

The qualification criteria is that they passed all previous interviews (unanimous "yes"s) and all references came back with 7+ rating. Ideally, there is a *spark* identified along the way - but not absolutely necessary if they did really well otherwise. Some people argue that a "strong yes" can cancel a single "no" - this is something you'll have to decide whether it makes sense for you. In the past, wherever we hired anyone with a "no", it **never** worked out. Some of these cases were me personally trying to advocate and change somebody's answer from a "no" to a "yes". Although I was successful in doing that, it ended up being a disaster. Lesson learned for me. Don't do this - don't influence the outcome. You're hurting the process.

Separately, I cannot stress how important it is that your process is efficient enough that you get to this point in less than two weeks. Maybe even a single week, if possible. For us, usually, the bottleneck is the candidate's schedule, not our own process. An efficient process allows you to be the first company to make the offer (sometimes that helps with being the **only** company to make an offer) and thus have an unfair advantage.

### Conclusion

Hopefully, the way we interview candidates has helped you in some meaningful way to improve your own interviewing process. In summary, we:

- Avoid a Top Coder / LeetCode style interview.
- Look for the *spark*: evidence of truly unique capabilities.
- Look for generalist, or adaptable people who can be decathletes, not just really good sprinters.
- Never compromise on culture-fit.
- Focus on problem-solving testing as the meat of the interviewing process. We do this by giving problems from areas they have never worked in before, and ask them to think about them from scratch.
- Take reference checks seriously.
- Keep our end-to-end process fast

If you'd like to try out our process first-hand, from the receiving end, well [we are hiring](https://earthly.dev/hiring)!

If you think our practices can be improved, [let me know](https://twitter.com/VladAIonescu)! This process has been built with the experience we've collected so far. But we are constantly evolving it, and in all likelihood, it will never be perfect. What practices have worked for you?

If you liked this article, you might also like [my past writings on Engineering Management principles](https://vladaionescu.com/my-version-of-44-engineering-management-lessons-88f6c50568a2).

{% include_html cta/bottom-cta.html %}
