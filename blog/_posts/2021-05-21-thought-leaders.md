---
title: "Please Don't Listen to the Thought Leaders"
categories:
  - Articles
author: Adam
internal-links:
 - dont link to me
 - just an example
---
Here is a somewhat fictionalized personal story. The names of the people and the technology have been changed. 

## Raising Objections

I was a new engineering manager who's team was starting a new ambitous project at a SAAS company. The company had several hundred developers and the project was approved. A design document and development plan existed, a working prototype had been created, and several talented people were executing on the plan. All that was left to do from, my perspective, was to 'reach alignment.'

I'm not sure if reaching alignment is a universal term that I was previously unfamilar with or if its company specific but for this project it worked like this: The project was approved but there were all kinds of people vaguely horizontal to me in the organization who could 'raise objections' about it. 

Raising objections is you telling someone above me, my boss or my bosses boss or so on, that you have concerns about the projects success.  An easy way to report concerns can be a really good idea. If the SRE manager heard we were using bongoDB and had dealt with bongoDB data lose in the past then there is no better time to speak than at the beginning of the project. And because the CTO doesn't want to spend time mediating discussions about database preferences, or whatever the lastest concerns are, as an engineering manageer part of my job was to make sure there were no objections to be raised. 

## Seeking Alignment
Preventing the raising of objections is was called 'reaching alignment.' The idea is to find the people who might have concerns or advice, get feedback from them, and work with the developers on the team to adjust the plan based on that. It ends up feeling a lot like the episode of the office where Andy and Kevin must meet with the heads of every company in the the office park about the parking situation.


<div class="wide">
![Everybody has advice about how to build your project]({{site.images}}{{page.slug}}/4-families.png)
</div>


At its worse the conversations tended to go something like this:

### The Quality Person Meeting

> **Adam:** You've had a chance to read the design doc.  What are your thoughts.
>
> **Quality Person:** There is nothing in here about unit-test coverage and taking a look at your other services they are below the the 80% level we set as a H2 engineering goal. Can you add a unit-testing strategy to the plan and set a specific coverage goal? 

### The Data Person Meeting

> **Adam:** You've had a chance to read the design doc.  What are your thoughts?
>
> **Data Person:** We are currently migrating all data in Important-Project-A from springy search to beetleDB and it is a multi-year project. All new projects should follow this so the effort doesnt need to be repeated.
>DB
> **Adam:** We weren't going to use springy search just a relational database. So I think we should be good.
>
> **Data Person:** BeetleDB is relational db equivalent so I would recommend using that so that you can scale.

### The Micro-Services Person

> **Adam:** You've had a chance to read the design doc.  What are your thoughts?
>
> **Micro-Services Person:** I would recommend seperating the read side from write side. I think you should put them in serparte services so that they can be scaled independently. That was our number one secret to scaling when I was at warble: the finer grain the services, the easier they are to scale.

I think you get the idea. If we adapt to all the feedback and we will avoid the pitfalls of the recent past but also the scope of the project will drastically grow and the project will likely never get completed.  Its like a [second-system effect](https://en.wikipedia.org/wiki/Second-system_effect) but brought forward in time. 

## The Solution
<div class="align-right">
 {% picture grid {{site.pimages}}{{page.slug}}/hearnoevil.png  --picture --img width="200px" --alt {{ Hear No Evil }} %}
<figcaption>The solution sort of</figcaption>
</div>
Thankfully, not all the advice I received was bad.  One person in particular asked very pointed questions about the problems be solved and identified some potential blindspots in our plan.  They also offered some great advice for dealing with advice that didn't seem relevant to the projects success: Create a product roadmap and put those items at least a year off into the future "and as long as they don't seem relevant you can just keep pushing them into the future." Perversely this plan made everyone happy -- everyone's feedback is on the roadmap, now its all just a question of priorites. 

With that advice the project got off the ground. But there was something that always bothered me about this process and I had never been able to put my finger on until recently.

## Contingent Advice

> “All bad advice is alike but all good advice is unique to the problem at hand.”
― Leo Tolstoy misquoted

The problem with all the bad advice was that same: it was unrelated to the problem I was going to solve.  The unit-testing person will always be advocating for more unit tests.  The distributed database person will always want things to go into beetleDB (at least until they hear about floraDB). 

It is sort of like Minh's cooking advice from King of The Hill: She tastes something and then says "Add Nutmeg". When would nutmeg not be a good fit?  Doesn't all advice need to be contigent?


<div class="align-right">
 {% picture grid {{site.pimages}}{{page.slug}}/nutmeg.png  --picture --img width="400px" --alt {{ Add Nutmeg }} %}
<figcaption>The solution to every problem can't be the same</figcaption>
</div>

This is what I think of when I hear the term thought-leader - someone has a single solution that seems to fit every problem. Whatever problem you face the answer is test driven development or stream architectures or 'being truly agile' or so on.

I get frustrated by advice like that but is the advice actually wrong? Unit testing, streaming architectures, agile are all good things.  I don't write code in a test-driven style but I did try it out a bit when it was the hot thing and I learned things from the process.  All of the thought-leaders are trying to move the industry forward. Can we really say that people offering uncontigent advice are worse at giving advice then those with more nuanced and complicated advice? I think that, yes, we can say that and there's evidence from the from the field of decision-making to back me up.

## Decision-Making Research
{% picture content-wide {{site.pimages}}{{page.slug}}/fork.png  --picture --alt {{ Add Nutmeg }} %}

One way to think about advice is as a prediction.  Advocating for TDD can be viewed as a prediction that if you don't write tests before you write code then your project will be less well designed and will be harder to maintain. Stream-Process-All-Things simiarly is a prediction that if you approach a problem as one of streams you'll get a better result than if you didn't. Obviously not all advice is tied to specific and explicit predictions and many thought-leaders would object to the idea that just because they are always talking about a solution that is the most important solution in every case. But I do think its fair to say that if you consult at 100s of companies and the proposed solution is always a variation of "use the actor system to model concurrency" or "you need a stronger alliegence to SOLID principles" then its fair to say you beleive those solution would strongly increase disired outcomes.

## Tetlock's Hedgehogs
 {% picture content-wide {{site.pimages}}{{page.slug}}/hedgehog.png  --picture --img width="1200px" --alt {{ A hedgehog }} %}

It turns out that [Philip E. Tetlock](https://scholar.google.com/citations?user=CJjf6H0AAAAJ&hl=en) from the University of Pennsylvania who has been studing the judgement and decision making of experts for most of his career, has something to say about those types of predictions. And Tetlock is an expert on experts: his [Good Judgement Project](https://en.wikipedia.org/wiki/The_Good_Judgment_Project) was able to beat CIA analyts by 30% at predicting geo-polical events. And the intelligence officers had access to classified information.  

Tetlocks earlier work was the study of political experts. He solicted political advice and predictions from 284 experts between 1984 and 2004 and once enough time had passed to determine the accuracy of the predictions, he scored the results. Political pundrity is a bit different than tech thought-leadership but I think his findings have a lot to teach us.

What he found was experts could be split into two broad categories, the first of which he called Hedgehogs. A Hedgehog had one big idea like free market capitalism (or nordic model capitalism or demand-side economics) which they used as a lens to look at many issues. They applied this big idea to every situation which resulted in simple and uncontigent advice.  You always need more freedom, nutmeg and unit tests. Hedgehogs are "Confident forecasters".

## The Foxes
 {% picture content-wide {{site.pimages}}{{page.slug}}/foxes.png  --picture --img width="1200px" --alt {{ A Fox }} %}

When all the predictions were added up and scored Hedgehogs lost out to his second category: Foxes. Foxes were the opposite of hedgehogs. They had complicated advice and were skeptical of even their own predictions.  Tetlock also found that foxes were less likely to be famous, because contingent advice is harder to explain in a sound bite.

Hedgehogs with predictions about the Iraq war existed on both sides of the polical spectrum. They had theories based on an over-arching political philosophies but the best predictors of the Iraq war outcomes were foxes who had in-depth knowledge of the region, not big theories. 

### Ignore Universal Solutions
 {% picture content-wide {{site.pimages}}{{page.slug}}/tools.png  --picture --img width="1200px" --alt {{ A Tool Board }} %}

Tetlock's [talk](https://longnow.org/seminars/02007/jan/26/why-foxes-are-better-forecasters-than-hedgehogs/) on this is subtitled "Ignore Confident Forecasters" which I think is a great summary of his findings.  

Everywhere I look in software development I feel like I see 'confident forecasters'. We are a pretty new field, and yet everyone always seems so certain that they have the solution to whatever problem is at hand. I'd like to hear more people saying things like "in this specific context test-coverage seem like an important metric" or "StopLang is a great if you can afford the GC but if you can't than you should look at IronOre." A great tool is not a universal tool its a tool well suited to a specific problem.

So that is my message: The more universal a solution someone claims to have to whatever software engineering problem exists, and the more confident they are that it is a fully-generalized solution, the more you should question them. The more specific and contigent the advice - the more someone says 'it depends' or 'YourSQL works well in a read heavy context with the following constraints ...' the more likely they are to be leading you in the right direction. At least that's what I have found.

Here at Earthly, we've been doing a lot of customer development and a lot of writing.  When meeting with someone, or [writing down advice](/blog/unit-vs-integration) I try to keep in mind Tetlock's findings. I really think [repeatable builds](https://earthly.dev) are important but if it's my solution to every problem then I think I'm probably falling into the same trap. So this post is my reminder to myself: Don't be a ~~hedgehog~~ thought-leader. 
