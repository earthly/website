---
title: "Put Your Best Title Here"
categories:
  - Articles
toc: true
author: Adam
internal-links:
 - just an example
---

Some years ago, when I worked in a physical office, I was having trouble with a new report I was developing. The fairly complex SQL that generated the report would sometimes be missing a single row and then if a ran things again the row would be back.

The SQL looked something like this:
``` sql

INSERT INTO Report
SELECT name FROM input1 
ORDER BY val;
 
SELECT * FROM Report;
one
two
three -- yep

INSERT INTO Report
SELECT name FROM input2 
ORDER BY val;

SELECT * FROM Report;
one
two
three
four 
five 
six -- yep

SELECT top 3 * FROM Report;
one
two
four -- wait, what?

```

I was going to spend the morning tracking this down. That was my standup update for that day. But when I gave it I caught a look from my teammate Isabella (not her real name). The look helped me solve the problem. We'll get to the solution in a moment but what I really want to talk about is that look --  I am always on the look out for this look.

## The Wait-What? Look

<div class="align-right">
 {% picture grid {{site.pimages}}{{page.slug}}/confused1.png  --picture --img width="260px" --alt {{ Confused Women }} %}
<figcaption>"I've traced it to a bug in the SMTP protocal"</figcaption>
</div>

I once saw someone go up to post office box and confidently empty their lunch garbadge into it - like it was a food court garbage pale. I think I made the look then - I could feel my lips pull to one side and my eyes narrow in confusion. Am I seeing this wrong? 

I've seen this look, usually is very fleeting, in so many daily stand ups since then. When you see it don't less it pass by unremarked, this facial expression is gold. It easy to thrash on a problem and forget to question some simple assumption and this face is a sign you've missed something important.

Are daily standups valuable?  Sometimes they are and sometimes they are not.  If you are blocked on something then telling the team is great, but really you shouldn't wait for the next standup to share that. There are also all kinds of social reasons why a standup is healthy. I work from my home office and have for many years and a video stand-up is a great way to actually chat screen to screen, with my teammates. I'm not sure that 'what I did yesterday and what I'm doing today part' is always as valuable as made out to be, especially if its just a status report, but the actual off-topic parts of standup. The part where I complain about how difficult it is to get a permit for building my deck and where Alex explains about foraging for mushrooms - those parts I think are really valuable just for my sanity.

<div class="align-left">
 {% picture grid {{site.pimages}}{{page.slug}}/confused2.png  --picture --img width="260px" --alt {{ Confused Women }} %}
<figcaption>"I'm inserting 'foo' but retrieving 'disk is full'"</figcaption>
</div>

When I first started working remote, zoom didn't exist and google hangouts didn't exist. Skype was around but we couldn't use it for our standups. I think there were too many people involved.  So we used a conference call bridge.  I would phone in every day and pace around my apartment as I gave my update and listened to others. 

Now I attend standups via zoom and I sometimes miss that I can't pace around during anymore, but its worth it to see people faces.  If I can see you face it feels like a deeper conversation than with just audio, but also I can keep my eye out for that look.

## The That-Is-Not-Quite-Right Effect

I don't understand how our brains work, but I think we are always running a simulation of things so we can predict what is going to happen next. My neighbourgh is out watering grass right now -- I can see him out my office window. If his hose wasn't actually on, I'm not sure I would notice I'm not paying that much attention. But if he casually jumped from the ground to the second story roof of his house, it would become the center of my attention. It would trigger some that-is-not-quite-right effect and I would uncounsously make that confused face.

That is why a standup can be valuable, in person or screen to screen. You can give your update when you are stuck, and you can watch for that failed-simulation face. Then ask them what they are thinking. Chances are they know where you missed a step or have a false assumption or at the very least you've violated their intuition about the problem and unpacking feeling is a good idea.

## Non-verbal Communication

<div class="align-right">
 {% picture grid {{site.pimages}}{{page.slug}}/confused3.png  --picture --img width="260px" --alt {{ Confused Women }} %}
<figcaption>"All users were created on a Thursday in 1970"</figcaption>
</div>
I've heard many times before that 70% of communication is non-verbal. This doesn't seem right to me. I am probably bad at non-verbal queues but I am getting way less than 70% of my communication from facial expressions and body langauge. This whole confused-face could be replaced with chin-scratching emoji. However, when I do get a verbal signal its incredibly valuable. It's a low big rate signal, but the bits are incredbily valuable.  I don't think you can easily replicate this signal async communication. One reason is that these non-verbal queues represent thoughts not words. Someone can hear your update and think to themselves "That doesn't sound right" but they may not be comfortable enough or care enough to say it out loud. Or it could just be a fleeting though before they start their update - you have to catch these expressions and you can't do it without seeing the person.  

People find zoom meetings fatiguing and I get that, but sometimes audio just won't do. Whenever I talk to someone who works remotely and doesn't use video it surprizes me. If you're not seeing your team mates faces when you describe a problem you are missing out on important information.  Maybe not all the time, but when that information is valuable -- man is it valuable.


## The SQL Solution

<div class="align-left">
 {% picture grid {{site.pimages}}{{page.slug}}/confused4.png  --picture --img width="260px" --alt {{ Confused Women }} %}
<figcaption>"the max message size in \nthe queue is now 2 gb"</figcaption>
</div>

So about the SQL. I got `the look` from Isabella because a select statement, especially one like I was describing should be determinstic. Isabella's spidey sense was telling her either I was wrong about results changing or I was doing something really wrong with SQL.  It turned out to be the latter.  

You see I was inserting records in order, but then selecting them out without an explicit order. Also my simple recounting of the report's logic (and my code snippet above) was missing an important wrinkle -- an important detail I had forgotten about. Sometimes there were duplicate keys and they needed to be deleted from the report table. Guess what happens when you insert things in-order into a table with deleted rows? Its implementation specific but probably the invisible spaces left by the deleted rows will be filled in by the inserted data, undoing the ordering. So my row wasn't missing, it was just wasn't ordered properly.  Add in an order by clause and the mystery is solved[^1].

### Writing Article Checklist

- [x] Write Outline
- [x] Write Draft
- [ ] Fix Grammarly Errors
- [ ] Read out loud
- [ ] Write 5 or more titles and pick the best on
- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
- [ ] Run mark down linter (`earthly +blog-lint-apply`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `earthly --build-arg NAME=2020-09-10-better-builds.md +link-opportunity` and find 1-5 places to incorporate links to other articles
- [ ] Raise PR