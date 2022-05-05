---
title: "Staff VS Line"
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

Let's talk about a career in tech but not the usual boring stuff about salary or whether you should work for FANG. Instead I want to talk about how where you fit in a specific organization influences what that job is like and what skills and strengths you'll develop as a software engineer.

Imagine a simplified world there is only enterprise software and there are only two broad types of software jobs.

( What is enterprise software? It's boring software for large corporations. My story is going to apply to other areas as well, but bear with me here. )

Ok, so only enterprise software exists and so you can work at two types of companies. First you could work at that a large company, where you might build and maintain their internal billing software. Or you could work outside the large company selling software and development services to them.

More specifically, you can either work at Duke Energy (a large utility company) or at Thoughtworks. And in both cases, by some coincidence of made of anedotes, you'll be writing billing software for utility companies.

These jobs may sound similar. Some even argue that an internal dev team and external consulting team are the same job:

> If you are a dev team within a bigger, non-tech company, you are basically an in-house agency with one client. 
>
> The Coding Career Handbook

After all, at both Thought Works and Duke Energy you'll be working inside a utility company, you'll be working to understand the gaps that the current system has, and coming up with and implementing a solution for them. **But there are actually big differences between these jobs: One is a line position and the other is a staff position.**

## Line and Staff

The division of employees into line and staff comes from the military. A line officer can fight on the front line. They directly contribute to the core mission of the branch of the armed forces they are in. On the other hand, a staff officer contributes only in a supporting role. They are doctors, IT people and administrators. 

The term spread from the military to business schools, where it became a useful way to group staff into categories:

> Staff and line are names given to different types of functions in organizations. A "line function" is one that directly advances an organization in its core work. This always includes production and sales, and sometimes marketing.[1] A "staff function" supports the organization with specialized advisory and support functions. For example, human resources, accounting, public relations and the legal department are generally considered to be staff functions.[2] Both terms originated in the military. 
>
> - https://en.wikipedia.org/wiki/Staff_and_line

What I find interesting about this distiction is that Staff and line roles are very different. They have different paces and they have different career trajectories. Understanding the difference, and which will fit you best is an important guiding principle.


Back to our example, the dev team at Duke Electric is a staff developer position. The billing software supports Duke Electric, the electricity is the product not that billing software. However, for the team at Thought Works, even if working on very similar billing software at a similarly sized region utility company (Dominion Energy maybe), the stakes are different. 

Someone at Thoughtworks sold Dominion Energy on the idea that Thoughtworks could do a great job on the billing software and Thoughtworks is probably charging a lot for their services. And if things go well, they will get follow up business and maybe make a whitepaper and try to get into more regional utilities ( Florida Power & Light here we come!). In other words, if you work on the team deployed into Duke and endanger the project timeline you might end up on the 'the bench' which is a half-step away from a lay-off.

Other the other hand, if someone in billing complains about you and you work on the internal dev team at Duke, you boss will deflect that and life will go on. Market pressures don't apply to internal teams and that can be both a good and a bad thing. One is not better than the other, they are just different. Each has career advantages and disadvantges. And I'll get to that shortly but first let me beat this distinction to death.


<div class="notice">
### Profit Center vs Cost Center

A similar concept I've heard used a lot is Profit Center vs Cost Center. This phrasing I found less clear because it's never totally clear what is a profit center and what is a cost center and everyone wants to be a profit center. However, if you find that profit vs costs easier to understand, go with that.

I personally like that Staff vs Line is role specific. An Agile coach embedded in the dev team of a highly profitable product is still in a supporting role ( unless the company is actually selling burn-down charts and platitudes) and therefore a Staff position.
</div>

## More Examples

- You maintain logistics software in a dev team at Walmart **Staff**
- You work on logistics software that your company sells to Target and other Walmart competitors **Line**
- In house ERP Dev: You are the expert at customizing the ERP software from SAP in a dev team at a large accounting firm. **Staff**.
- ERP software company: You add new stuff to SAP, at SAP. **Line**
- You are a in-house recruiter, at a software company. **Staff**
- You are a recruiter at a recruiting company. **Line**
- You work in PR at Google. **Staff**
- You work in PR at a PR firm. **Line**
- You're a doctor on a miltary base. **Staff**
- You're a doctor at medical hospital. **Line**

<div class="notice">
## Something about devops

Side Note: Things get murky
Things aren't quite as clear the miltary, where its everyone knows if they have the type of job where someone might shoot at them or not. There are more gradations of roles, but if you make a product your organization makes money from, you are line employee and the farther away you get from that the more of a staff employee you are. For instance, if you work at a software company, but on maintaining the hand-rolled internal ticketing system, you are probably staff.

Is devops, taking something that was traditionally staff (ops) and realizing that it can be supportive enough that it becomes a strategic advantage. 

What are SRE, Platform Engineering, and Solutions architects in this world? I think it depends on the org. A platform engineering team certainly is in a supporting role in the org, but if the company produces software as its main product, then the roles will feel like line roles. That's why its important to look at the org chart.
</div>

## The Org Chart

The easiest way to tell if you are line or staff is to look at the org chart of your business. If your role makes up the largest fraction of the org chart, you are line. There will always be less doctors than soldiers in the army and less IT people than accountants at the accounting firm.

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5600.png --alt {{  }} %}
<figcaption></figcaption>
</div>

## Being a Line Software Developer

Being a dev at a software producing company is well covered. [Michael Lynch's](https://mtlynch.io/why-i-quit-google/) story about the pluses and minues of working at google is great coverage of the good and bad side: "I was surrounded by the best engineers in the world, using the most advanced development tools in the world, and eating the free-est food in the world."


- You'll get great at software development
- You'll work with a lot of great developers
- You'll specialize and become great in your speciality.
- Competition for advancement will be fierce

The advantages of working at a non-tech company, of being a staff developer are less well covered. But advantages do exist.

## Advantages to Staff

### Corporate Ladder Climbing

If most of the teams in the org chart are filled with people like you then its going to be hard to climb the ranks of the organization. I once managed tweleve people as a engineering manager and my boss, a director, managed around that many managers himself, the pattern continuing up to the CTO. If you envision being part of the C-suite yourself someday, competeing with 12^N people below the CTO is a tough way to do it.

Meanwhile, my friend building software at a Utility Company in on a team of 6, and his boss reports to the executive level. His boss goes on vacation and he is giving status updates to the COO.

This ladder climbing disparity is acatually how I learned of the staff vs line breakdown. In the one business class I took in university the teacher pointed out trying to become a partner at Goldman Sachs was a fools errand, but their are great (staff) positions in finance at thousands of publically traded companies where becoming the Chief Finance Officer is very possible.

### Business Focus

At a tech company, especially a large one, you will specialize. You may become an expert in a particular subsystem or a particular layer of stack. In a staff role, at a non-tech company, you will likely have a much larger but shallower scope. You may build talk to the stakeholders to understand their requirements, and make changes to the frontend and keep the database up and maybe spend time getting familar with the intracaies of the business your company operates in. You will learn more about the industry you operate in.

If understanding how business operate is interesting to you this could be a great fit.

<div class="notice">
Retiring to a staff role is a common pattern I've seen. You used to work at Hooli on their data backends, but now you work at a Utility company who has a much smaller version of the same challenges. You get to be the expert who can solve real business problems with your database experticne and also work at a company where tenure's are in the decades and planning is done over simlar timelines. ( Finnaly you get off the sprint treadmill and you'll have so many opportunties to start sentenses with "When I was at Hooli ..." ).

</div>

### Different Values and Pace

The line of business a company is in and the type of people it employees effect what it values and what it's expectations are. A tech company where the average age is 28 years old will have different values than an accounting firm where the average age is 47 years. If you value working with people who've been working at the job for decades more than you value a kombucha keg, a slower moving industry might be a better fit for you. A developer at a utility company will get paid less than a [unicorn startup](https://twitter.com/fast), but most utility compaines expect you to work their for decades. They might have unions and pension funds, and they are generally aware that any investment they make in you can be recouped over decades rather than years. For some people, that is a great trade to make.

<div class="notice">
Note: My Expericne 
Culturally the tech companies I've worked at have all assumed that good employees want to do a good job. Employees are empowered and valued. I really don't think this is the case everywhere. My one role as a staff developer was at a place where I felt their was an implicit assumption that people disliked their work and needed to be strongly directed. 
</div>

## The Staff Role Is Under Discussed

I work at Earthly, a venture funded developer tools company. Our company mainly employs software developers, our customers are software developers, and our product is a product for building software. I love it but it can feel a little insular and inward facing at times.

My few friends who work at non-software producing company live in such a different world and its a world I never see discussed. In fact, if you hang out online with other developers, it feels like these roles don't even exist. But they do exist and they can be great. 

If you've worked at both, let me know what you think? What are advantages and disadvantages? 





Extras:
- union
- staff vs staff engineer
( This is not in the sense of the seniory role called Staff engineer, different concept – you should pretend that term does not exist for now. )
- 