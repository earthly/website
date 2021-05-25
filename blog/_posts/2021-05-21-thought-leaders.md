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

You get the idea. Adapt to all the feedback and I will avoid the pitfalls of the recent past but also the scope of the project will drastically grow and the project will likely never get completed.  Its a [second-system effect](https://en.wikipedia.org/wiki/Second-system_effect) but brought forward into the first version. Thankfully, not all advice I received was bad.  One person in particular asked very pointed questions about the problems be solved and identified some potential blindspots in our plan.  They also offered some great advice for dealing with others concerns that, after consideration, didn't seem relevant: Create a product roadmap and put those items at least a year off into the future "and iff they don't seem relevant then you can just adjust the roadmap again." With that advice the project got off the ground. But there was something that always bothered me about the feedback I got during this process that I had never been able to put my finger on until recently.

## Contingent Advice

The problem with all the bad advice was that same: it was unrelated to the problem I was going to solve.  The unit testing person will always be advocating for more unit tests.  The distributed database person will always want things to go into bettleDB. It is sort of like Minh Souphanousinphone's cooking advice from King of The Hill, which is to taste something and then say "Add Nutmeg". I want to ask her: Are there conditions underwhich you wouldn't want to add nutmeg.  When would nutmeg not be a good fit?  Doesn't all advice need to be contigent?

This is literally what I think of when I hear the term industry thought-leader - someone with a single solution that seems to fit every problem. At least the unit testing person and the streaming person had hopefully seen a problem come up in the context of this company and were now spreading the word about their favorite solution.  In the worse case, a thought leaders context is everything, they have a solution and whatever problem you face the answer is test driven development or stream architectures or 'being truly agile' or so on.

But it that actually wrong? Unit testing, streaming architectures, and, in the early years, agile were all good things.  They helped moved the industry forward so can we really say that people offering uncontigent advice are worse at giving advice then those with more nuanced and complicated adivce? It turns that, yes we can say that.

## Tetlock's Hedgehogs

One way to think about advice and feedback is as a prediction.  TDD can be viewed as a prediction that if you don't write tests before you write code then your project will be less well designed and will be harder to maintain. Stream-Process-All-Things simiarly is a prediction that if you approach a problem as one of streams you'll get a better result than if you didn't. And so on.

It turns out that [Philip E. Tetlock]() from the University of Pennsylvania has been studing prediction and judgement of experts for most of his career. Famously his [Good Judgement Project] was able to beat by 30% CIA intelligence offers at predicting geo-polical events. And the intelligence officers had access to classified information.  

Tetlocks earlier work was the study of political experts. He solicted advice from 284 experts between 1984 and 2004 and scored there results. What he found was experts could be split into two broad categories which he called hedgehogs and foxes. Foxes know lots of little things and Hedgehogs know one big thing.  

Hedgehog had one big idea like free market captilism (or marxism) will win out and solve all problems. They applied this big idea to every situation which resulted in simple and uncontigent advice.  You always need more freedom, nutmeg and unit tests. Hedgehogs are "Confident forecasters".

Foxes are the opposite. They have complicated advice and are skeptical of even their own predictions.  Hedgehogs with predictions about the Iraq war existed on both sides of the polical spectrum. they had theories based on an over-arching political philosophies but the best predictors were foxes with  indepth knowledge of the region. 

When all the predictions were added up and scored Hedgehogs lost to Foxes. Tetlock's talk on this is subtitled "Ignore confident forecasters" which I think is a great summary of his findings.  

So that is my message: Thought-leaders are Hedgehogs, and the more universal a solution someone claims to have to whatever software engineering problem exists, and the more confident they are that it is a universal solution, the more you should distrust them. The more specific and contigent the advice - the more someone says 'it depends' or 'its complicated' the more likely they are to be leading you in the right direction.

Here at Earthly, we've been doing a lot of customer development and a lot of writing.  When meeting with someone, or [writing down advice](/blog/unit-vs-integration) I try to keep in mind Tetlock's findings. I really think [repeatable builds](https://earthly.dev) are important but if it's my solution to every problem then I'm probably wrong.  
