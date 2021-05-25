---
title: "Please Don't Listen to the Thought Leaders"
categories:
  - Articles
toc: true
author: Adam
internal-links:
 - dont link to me
 - just an example
---

Here is a somewhat fictionalized personal story.  I was a new engineering manager starting a new ambitous project at a SAAS company. The company had several hundred developers. 

A design document and development plan existed, a working prototype has been created, and several talented people were executing on the plan. All that was left to do was to 'reach alignment'. I'm not sure if reaching alignment is a universal term that I was unfamilar with but for me and this project it worked like this: The project was approved but there were all kinds of people vaguely horizontal to me in the organization who could 'raise objections'. 

Raising objections is telling someone above me, my boss or my bosses boss or so on, that you have concerns about the projects success.  An easy way to report concerns can be a really good idea. If the SRE manager heard we were using bongoDB and had PTSD from dealing with bongoDB data lose in the past then there is no better time to speak than at the beginning of the project.  And because the CTO doesn't want to spend time mediating discussions about database preferences, or whatever the lastest concerns are, as an engineering manageer part of my job was to meet with people ahead of time and make sure that they won't 'raise objections'.  The idea is to find the people who might have concerns or advice, get feedback from them, and work with the developers on the team to adjust the plan based on that.  It It ends up feeling a lot like the [Five Familes] https://i.redd.it/5wisw98zpn5z.png episode of the office.

This is where it gets tricky. At its worse, conversations tend to go something like this:

---
Adam: You've had a chance to read the design doc.  What are your thoughts.
Person1: There is nothing in here about unit-test coverage and taking a look at my dashboard your other services are below the the 80% level we set as a H2 goal. Can you add a unit-testing strategy to the plan and set a specific coverage goal? 
---
---
Adam: You've had a chance to read the design doc.  What are your thoughts?
Person2: We are currently migrating all data in important-project-A from springy search to beetle db and it is a multi-year project. All new projects should follow this so the effort doesnt need to be repeated.
Adam: We weren't going to use springy search just a relational database. So I think we should be good.
Person2: Beetle db is relational db equivalent so I would recommend using that so that you can scale.
---
---
Adam: You've had a chance to read the design doc.  What are your thoughts?
Person2: I would recommend seperating the read side from write side. I think you should put them in serparte services so that they can be scaled independtly. That was our number one secret to scaling when I was at warble: the finer grain the services, the easier they are to scale.
---

You get the idea. Adapt to all the feedback and I will avoid the pitfalls of the recent past but also the scope of the project will drastically grow and the project will likely never get completed.  Its like a [second-system effect](https://en.wikipedia.org/wiki/Second-system_effect) but brought forward in time. Thankfully, not all the advice I received was bad.  One person in particular asked very pointed questions about the problems be solved and identified some potential blindspots in our plan.  They also offered some great advice for dealing with others concerns that, after consideration, didn't seem relevant: Create a product roadmap and put those items at least a year off into the future "and if they don't seem relevant then you can just adjust the roadmap again." With that advice the project got off the ground. But there was something that always bothered me about the feedback I got during this process that I had never been able to put my finger on until recently.

## Contingent Advice

The problem with all the bad advice was that same: it was unrelated to the problem I was going to solve.  The unit-testing person will always be advocating for more unit tests.  The distributed database person will always want things to go into bettleDB. It is sort of like Minh Souphanousinphone's cooking advice from King of The Hill, which is to taste something and then say "Add Nutmeg". I want to ask her: Are there conditions underwhich you wouldn't want to add nutmeg.  When would nutmeg not be a good fit?  Doesn't all advice need to be contigent?

This is literally what I think of when I hear the term thought-leader - someone has a single solution that seems to fit every problem. Whatever problem you face the answer is test driven development or stream architectures or 'being truly agile' or so on.

But id that actually wrong? Unit testing, streaming architectures, agile are all good things.  I don't write code in a test-driven style but I did try it out a bit when it was the hot thing and I learned things from the process.  All of the thought-leaders are trying to move the industry forward. Can we really say that people offering uncontigent advice are worse at giving advice then those with more nuanced and complicated advice? I think that, yes, we can say thay and There's evidence from the from the field of decision-making to back me up.

## Tetlock's Hedgehogs

One way to think about advice and feedback is as a prediction.  Advocating for TDD can be viewed as a prediction that if you don't write tests before you write code then your project will be less well designed and will be harder to maintain. Stream-Process-All-Things simiarly is a prediction that if you approach a problem as one of streams you'll get a better result than if you didn't. Obviously not all advice is tied to specific and explicit predictions and many thought-leaders would object to the idea that just because they are always talking about a problem that is the most important problem in every case. But I do think its fair to say that if you consult at 100s of companies and the proposed solution is always a variation of "use the actor system to model concurrency" or "stricter alliegence to SOLID principles" then its fair to say you beleive .... <<TODO>>  

It turns out that [Philip E. Tetlock]() from the University of Pennsylvania has been studing the judgement and decision making of experts for most of his career. Famously his [Good Judgement Project] was able to beat CIA analyts by 30% at predicting geo-polical events. And the intelligence officers had access to classified information.  

Tetlocks earlier work was the study of political experts. He solicted political advice and predictions from 284 experts between 1984 and 2004 and once enough time had passed to determine the accuracy of the predictions, he scored the results. Political pundrity is a bit different then thought-leadership but I think what his data showed has some lessons to teach us.

What he found was experts could be split into two broad categories which he called hedgehogs and foxes. Foxes know lots of little things and Hedgehogs know one big thing.  

A Hedgehog had one big idea like free market captilism (or marxism) will win out in the end. They applied this big idea to every situation which resulted in simple and uncontigent advice.  You always need more freedom, nutmeg and unit tests. Hedgehogs are "Confident forecasters".

When all the predictions were added up and scored Hedgehogs lost out to his second category: Foxes. Foxes were the opposite of hedgehogs. They had complicated advice and were skeptical of even their own predictions.  

Hedgehogs with predictions about the Iraq war existed on both sides of the polical spectrum. They had theories based on an over-arching political philosophies but the best predictors of the Iraq war outcomes were foxes who had indepth knowledge of the region, not big theories. 

Tetlock's talk on this is subtitled "Ignore confident forecasters" which I think is a great summary of his findings.  Everywhere I look in software development I feel like I see 'confident forecasters'. We are a pretty new  field, and yet everyone always seems so confident that the latest thing is a solution to whatever problem is at hand. I'd like to hear more people saying "It's complicated" or "in this specific context test-coverage seem like an important metric" 

So that is my message: Thought-leaders are Hedgehogs, and the more universal a solution someone claims to have to whatever software engineering problem exists, and the more confident they are that it is a universal solution, the more you should distrust them. The more specific and contigent the advice - the more someone says 'it depends' or 'its complicated'  or 'X works well in a read heavy context with the following constraints ...' the more likely they are to be leading you in the right direction.

Here at Earthly, we've been doing a lot of customer development and a lot of writing.  When meeting with someone, or [writing down advice](/blog/unit-vs-integration) I try to keep in mind Tetlock's findings. I really think [repeatable builds](https://earthly.dev) are important but if it's my solution to every problem then I think I'm probably falling into the same trap.  
