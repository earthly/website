---
title: "SQL Errors and Video Cameras"
categories:
  - Articles
author: Adam
internal-links:
 - just an example
bottomcta: false
excerpt: |
    In this article, the author shares a personal experience of encountering a SQL error and how a non-verbal cue from a teammate helped them solve the problem. They discuss the value of non-verbal communication in remote work and the importance of using video cameras during meetings. The article also provides a solution to the SQL issue and highlights the significance of using an "order by" statement.
last_modified_at: 2023-07-19
---
**In this article, we delve into the subtleties of non-verbal teamwork. Just as you prize the exactness of SQL queries, you'll value Earthly's declarative syntax for its similar precision in build processes. [Discover how with Earthly](/).**

<div class="narrow-code">

Some years ago, when I worked in a physical office, I was having trouble with a new report I was developing. The reasonably complex SQL that generated the report would sometimes be missing a single row that would reappear if I reran things.

The SQL looked something like this:

``` sql
-- sort and insert first partition into repo
INSERT INTO Report
SELECT name FROM input1 
ORDER BY val;
 
SELECT * FROM Report;
one
two
three -- yep

-- sort and insert second partition into repo
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

I was going to spend the morning tracking this down. That was my daily stand-up update. But when I gave it, I caught a look from my teammate Isabella (not her real name). The look helped me solve the problem. We'll get to the solution in a moment, but I want to talk about that facial expression -- I am always on the lookout for it now.

## The Wait-What? Look

<div class="align-right">
 {% picture grid {{site.pimages}}{{page.slug}}/confused1.png --picture --img width="260px" --alt {{ Confused Women }} %}
<figcaption>"I've traced it to a bug in the SMTP protocol"</figcaption>
</div>

I once saw someone go up to a post-office box and confidently empty their lunch garbage into it - like it was a food court garbage bin. I made the facial expression then - I could feel my lips pull to one side and my eyes narrow in confusion. Am I seeing this correctly?

I've spotted this look in so many daily stand-ups since then. Usually, it's very fleeting, but I try not to let it pass by unremarked because unpacking it can save so much time. It easy to thrash on a problem and forget some simple assumption you've made. This face is a sign you've overlooked something important.

Are daily stand-ups valuable? Sometimes they are, and sometimes they aren't[^1]. If you're blocked on something, then telling the team is essential, but you shouldn't wait for the next stand-up to share that. There are also all kinds of social reasons why a stand-up is healthy. I work from my home office and have for many years, and a video stand-up is a great way to actually have some small talk, screen to screen, with my teammates. Some parts of a daily stand-up are just a status report, and I'm not sure that 'what I did yesterday and what I'm doing today part' is always valuable. But the actual off-topic parts of a stand-up -- the part where I complain about how difficult it is to get a permit for building my deck, and where Alex explains about foraging for mushrooms -- those parts help keep me sane and happy.

## That's Not Quite Right

<div class="align-left">
 {% picture grid {{site.pimages}}{{page.slug}}/confused2.png --picture --img width="260px" --alt {{ Confused Women }} %}
<figcaption>"I'm inserting 'foo' but retrieving 'disk is full'"</figcaption>
</div>

We are always simulating the world around us on some subconscious level. It helps us predict what is going to happen next. For example, my neighbor is out watering his grass right now -- I can see him out my office window. If his hose wasn't on, I'm not sure I would notice because I'm not paying that much attention. But if he casually jumped from the ground to the second-story roof of his house, it would become the center of my attention. It would trigger some that's-not-quite-right effect, and I would unconsciously make that confused face.

That is why a stand-up can be valuable, in person or screen to screen. You can give your update when you are stuck, and you can watch for that failed-simulation face. Then ask them what they are thinking. Chances are they know where you missed a step or where you have a false assumption. At the very least, you've violated their intuition about the problem, and unpacking that feeling is a good idea.

## Non-Verbal Communication Requires Cameras On

<div class="align-right">
 {% picture grid {{site.pimages}}{{page.slug}}/confused3.png --picture --img width="260px" --alt {{ Confused Women }} %}
<figcaption>"All users were created on a Thursday in 1970"</figcaption>
</div>
I've heard many times before that 70% of communication is non-verbal. This seems to oversell non-verbals or maybe I'm just not great at reading them. This whole confused-face signal could be replaced with chin-scratching emoji or a sign that said: "Wait, What?". But, when I do get a non-verbal signal, it can save me hours and days of time. I don't think you can easily replicate this signal with asynchronous communication. One reason is that these non-verbal cues often represent subtle feelings. Someone can hear your update and think to themselves, "That doesn't sound right", but they may not be comfortable enough or care enough to say it out loud. Or it's just fleeting thought before they start their own update. You have to catch these expressions, and you can't do it without seeing the person.

This doesn't mean that everyone should always be able to see everyone in every meeting. If you are joining a 50 person meeting with a single presenter and everyone has their camera off, then follow suit. If you are eating your lunch in a meeting, I don't need to see or hear you chew. But if you are seeking help or giving help or pairing on an issue with me, then I want to see your face. The examples and facial expressions here are extreme but even just seeing that I've gone too fast and lost you, or that you're starting to say something, can improve the fidelity of the conversation.

People find zoom meetings fatiguing, and I get that. The world contains too many meetings. But I'm shocked when I talk to someone on a remote team that never uses video. If you're not seeing your teammate's face when you describe a problem, who knows what you are missing[^2].

## The SQL Solution

<div class="align-left">
 {% picture grid {{site.pimages}}{{page.slug}}/confused4.png --picture --img width="260px" --alt {{ Confused Women }} %}
<figcaption>"the max message size in the queue<br/> is now 2 gigabytes"</figcaption>
</div>

So about the SQL. I got `the look` from Isabella because a select statement like I was describing should be deterministic. Isabella's spidey-sense told her either I was wrong about results changing or I was misusing SQL. It turned out to be the latter.  

You see, I was inserting records sorted and selecting them out without an explicit order. Also, my simple recounting of the report's logic (and my code snippet above) was missing a critical detail -- one I had forgotten about[^3]. Sometimes I had to delete duplicate keys from the report table. Guess what happens when you insert things in-order into a table with deleted rows? Its implementation-specific, but sometimes, the invisible spaces left by the deleted rows will be filled in by the inserted data, undoing the insertion order. My row wasn't missing. My data just wasn't sorted correctly. Once I added in an `order by` everything worked.

</div>
<!-- markdownlint-disable MD046 -->

[^1]: [Like everything](/blog/thought-leaders/), they work well in some contexts and not in others. If they aren't helpful, drop them and try something else.
[^2]: I've run this idea by people I know who work remotely and never turn their camera on. Not everyone is convinced, and I find that genuinely confusing. Maybe they have a lot of useless meetings? Perhaps the local culture is against cameras? Or maybe they always know what they are doing, and I never do?
[^3]: Here is a minimal reproduction in Postgres.
      <div class="narrow-code">

      I have some tables with summary data in it:
    

      ``` sql
      -- simplified tables
      CREATE TABLE Report (name varchar(13));
      CREATE TABLE input1(name varchar(13), val bigint);
      CREATE TABLE input2(name varchar(13), val bigint);

      -- which, per user, had summary data something like this
      INSERT INTO input1
      VALUES
          ('one', 1),
          ('two', 2),
          ('three', 3),
          ('three', 3);

      INSERT INTO input2
      VALUES
          ('four', 4),
          ('five', 5),
          ('six', 6);
      ```      
     
     I sort it and put it in the report table then remove any duplicates:

      ``` sql
      -- sort and insert first partition
      INSERT INTO Report
      SELECT name FROM input1 
      ORDER BY val;
      
      -- delete duplicate records 
      DELETE FROM Report where name in ( 
        select name
        from Report 
        group by name 
        having count(*) > 1
      );

      -- sort and insert second partition
      INSERT INTO Report
      SELECT name FROM input2 
      ORDER BY val;
      ```

      Then I return the N results as part of the report:

      ``` sql
      -- show Top N report
      SELECT * FROM Report limit 3;
      one
      two
      four
      ```

      The actual problem was more complex, involved abusing row_number() and was in SQL SERVER, but the solution is still the same: use an `order by`:

    ``` sql
      -- show Top N report
      SELECT * FROM Report Order By name limit 3;
      one
      two
      three
      ```      
      SQL makes no guarantees about tables being in insertion order. 
      <!-- markdownlint-enable MD046 -->
      </div>