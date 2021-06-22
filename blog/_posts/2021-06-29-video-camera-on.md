---
title: "Put Your Best Title Here"
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
- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
- [ ] Run mark down linter (`earthly +blog-lint-apply`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `earthly --build-arg NAME=2020-09-10-better-builds.md +link-opportunity` and find 1-5 places to incorporate links to other articles
- [ ] Raise PR

## Draft.dev Article Checklist

- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
- [ ] Run mark down linter (`earthly +blog-lint-apply`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `earthly +link-opportunity` and find 1-5 places to incorporate links


## Outline
- story about werid expressions and stand ups
- working remote
- body language studies
- people as simulators 


I was having trouble with a new report I was developing. The fairly complex SQL that generated it would sometimes be missing a single row and then if a ran things again the row would be back.

The SQL looked something like this:
```
CREATE TABLE input1([name] varchar(13), [val] bigint);

INSERT INTO input1
VALUES
    ('one', 1),
    ('two', 2),
    ('three', 3);

CREATE TABLE input2 ([name] varchar(13), [val] bigint);

INSERT INTO input2
VALUES
    ('four', 4),
    ('five', 5),
    ('six', 6);

CREATE TABLE Report (
  [name] varchar(13)
);

INSERT INTO Report
SELECT
  name
FROM
  input1 
 ORDER BY val;
 
INSERT INTO Report
SELECT
name
FROM
  input2 
 ORDER BY val;

SELECT top 3 * FROM Report;
```
Usually this would output 

``
one
two
three
```
But occasionally it would output 

```
one
two
four
```


I was going to spend the morning tracking this down. That was my standup update for that day. But when I gave it I caught a look from someone else on the team. The look helped me solve the problem. We'll get to the solution in a moment but what I really want to talk about is that look --  I am always on the look out for this look.

 I once saw someone go up to post office box and confidently empty their lunch garbadge into it - like it was a food court garbage pale. I think I made the look then - I could feel my lips pull to one side and my eyes narrow in confusion. Am I seeing this wrong? 

I've seen this look, usually is very fleeting, in so many daily stand ups since then. When you see it don't less it pass by unremarked, this facial expression is gold.  

Are daily standups valuable?  Maybe. Sometimes they are and sometimes they are not.  If you are blocked on something then telling the team is great, but really you shouldn't wait for the next standup to share that. There are all kinds of social reasons why a standup is healthy. I work from my home office and have many years and a video stand-up is a great way to actually chat screen to screen, with my teammates. I'm not sure that 'what I did yesterday and what I'm doing today part is as a valuable as made out to be, but the actual off-topic parts of standup. The part where I complain about how difficult it is to get a permit for building a deck and where Alex explains about foraging for mushrooms - those parts I think are really valuable for a distributed team.

When I first started working remote, zoom didn't exist and google hangouts didn't exist. Skype was around but we couldn't use it for our standups. I think there were too many people involved.  So we used a conference call bridge.  I would phone in every day and pace around my apartment as I gave my update and listened to others. 

Now I attend standups via zoom and I sometimes miss that I can't pace around during anymore, but its worth it to see people faces.  See peoples faces it feels like a deeper conversation than with just audio but also I can keep my eye out for that look.

I don't understand how our brains work, but I think we are always running a simulation of things so we can predict what is going to happen next. My neighbourgh is out watering grass right now -- I can see him out my office window. If his hose wasn't actually on, I'm not sure I would notice I'm not paying that much attention. But if he casually jumped from the ground to the second story roof of his house, it would become the center of my attention. It would trigger some that-is-not-quite-right effect and I would uncounsously make that confused face.

That is why a standup can be valuable, in person or screen to screen. You can tell your update of your progress and you can watch for that failed simulation face. Then ask them what they are thinking. Chances are they know where you missed a step or have a false assumption or at the very least you've violated their intuition about the problem and unpacking feeling is a good idea.

I've heard many times before that 70% of communication is non-verbal. This doesn't seem right to me. I am probably bad at non-verbal queues but I am getting way less than 70% of my communication from facial expressions and body langauge. This whole confused-face could be replaced with chin-scratching emoji. However, when I do get a verbal signal its incredibly valuable and I don't think you can easily replicate it in async. One reason is that these non-verbal queues represent thoughts not words. Someone can hear your update and think to themselves "That doesn't sound right" but they may not be comfortable enough or care enough to say it out loud.

So about the SQL. I got the look because a select statement, especially one like I was describing should be determinstic. It should be determinstic that is if you are ordering everything. I was inserting records in order, but then selecting them out without an explicit order. 

Also my simple recounting of the report's logic (and my code snippet above) was missing an important wrinkle -- an important detail I had forgotten about.Sometimes there were duplicate keys and they needed to be deleted from the report table, so there was some logic like this:
```
delete top(1) from Report where name in 
(
  select name
from Report 
group by name 
having count(*) > 1
);
```

Guess what happens when you insert things in order into a table with deleted rows? Its implementation specific but probably invisible spaces left by the deleted rows will be filled in by the inserted data, undoing the ordering.


