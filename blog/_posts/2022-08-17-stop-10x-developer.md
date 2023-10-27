---
title: "Stop saying 10x developer"
categories:
  - Articles
author: Adam
bottomcta: false
internal-links:
 - 10x developer
 - 10x engineer
excerpt: |
    In this article, the concept of the "10x developer" is dissected and examined. The author explores whether such developers truly exist and discusses the importance of skills being a limiting factor in order for them to have a significant impact. The article also suggests using more specific terms, such as "expert" or "specialist," instead of the vague "10x developer" label.
last_modified_at: 2023-07-19
---
**We're [Earthly](https://earthly.dev/). We make building software faster and more efficient. Whether you're a "10x developer" or working to improve your skills, our tool might just give you the efficiency boost you need. [Check us out](/).**

Here is part of a rather infamous Twitter thread:

> 10x engineers rarely look at help documentation of classes or methods.
> Given a product feature, they can write that entire feature in one or two sittings of 4 to 6 hours with a caffeinated drink without distraction.

It goes on:

> 10x engineers hate meetings. They think it is a waste of time, and obvious things are being discussed.

And on:

> Most of the 10x engineers are full-stack engineers. [But] I have rarely seen them doing UI work.[^1]

[^1]: [Source](https://twitter.com/skirani/status/1149302828420067328)

Shekhar Kirani treats talented engineers like a rare dog breed he's learned to spot. This is obviously wrong, but the subject of the 10x engineer won't go away. **So let's dissect this concept a little bit, see when it makes sense, when it doesn't, and maybe arrive at a better way to frame things.**

## Definitions

The 10x developer concept came out of research by [Tom Demarco](https://www.gwern.net/docs/cs/algorithm/2001-demarco-peopleware-whymeasureperformance.pdf). He tested more than 600 developers at completing coding exercises and found some were ten times faster than others (under the conditions of the research).

> A 10x developer is a professional who is 10 times more productive than other developers with an equal level of expertise in the field. That is to say, a 10x developer completes 10 times more tasks and writes 10 times better code than any other competent member of their team working in the same conditions.
> [Who Is a 10x Developer and How to Become One?](https://www.actitime.com/productivity/10x-developer)

A frequent discussion point online is whether 10x Developers can really exist. After all, it's not 1984 any more and maybe the playing field has now been levelled. So let's tackle that first.

## The 95x Developer

> You will never see two 10x engineers in the same place. This is because it would trigger a productivity singularity.
>
> [Xanda Schofield](https://twitter.com/XandaSchofield/status/1150106315647119360)

Development skills vary and can be improved. I don't think anyone argues that point. But are people really 10x better at tasks than non-incompetent colleagues? Yes and in fact 10x is too small a number.

Let's look at an extreme but still instructive example: LeetCode. Leetcode problems make it very easy to show that developer skills vary by orders of magnitude. (Demarco's original research used a problem set called 'Coding War Games', so Leetcode puzzles are in the spirit of his research.)

Contest competitors on Leetcode have scores that translate into the probability they can complete a problem. Specifically, "In practice, if you meet a problem whose rating is equal to your rating, you are expected to solve it in half of your contests."[^2] You see, LeetCode uses ELO rankings, which are directly convertible to a success multiplier. LeetCode does not share problem ratings, but user `zerotrac` has calculated and shared implied problem scores on [github](https://github.com/zerotrac/leetcode_problem_rating/blob/main/ratings.txt)

[^2]: [source](https://leetcode.com/discuss/study-guide/1965086/How-to-practice-for-2200%2B-rating-in-LC)

Using this and a [probability table](https://www.318chess.com/elo.html), I can tell you that the Leetcode problem [Count Ways to Make Array With Product](https://leetcode.com/problems/count-ways-to-make-array-with-product/) problem can be solved by 95% of users with a ranking of 3000 but only by about 1% of users with rankings of 1700.

If you were to imagine a Jira board made up of 2500 difficulty problems, and if work practices conformed strictly to Leetcode rules, then a 3000 ranked player would be as effective as 95 1700-rating users working individually. They would be a 95X developer. So certainly, if a 95x developer can exist in LeetCode, then a 10x Developer can exist in any domain where the ceiling on difficulty is high enough.

But how much day-to-day work has sufficient difficulty to let a skilled developer shine?

## Doctor House, 10x Doctor

> 10x engineers do not know what sunlight is because they have never seen it.
>
> They also hang from the roofs of caves, their leather wings enfolding their self assembled Compute as they code through the dark night of the soul...  
> [Paul Sweeney](https://twitter.com/PaulSweeney/status/1150366063303057408)

Variation in skills isn't unique to software development. If 10x developers exist, then 10x doctors and mechanics exist as well. But, for a skill to materially impact a team or an organization, it must be a limiting factor.

If House, the misanthropic medical genius from the show 'House' worked at a walk-in clinic, handing out flu shots and antibiotics, he wouldn't be more effective than a mediocre doctor.[^3] Similarly, if your team's problems aren't occasionally [combinatorial graph coverage problems](https://leetcode.com/problems/minimum-weighted-subgraph-with-the-required-paths/submissions/), then is a Leetcode champ going to move the needle? If a 10x developer is supposed to get 10x the work done, then you need some challenging problems to throw at them.

[^3]: Also, why do 'geniuses' need to be jerks? Both Shekhar Kirani and the House writers need talented people to be deficient in other ways. Where is the genius who's friendly and brings banana bread in to work for everyone?

(Personal opinion: A developer who is a 10x communicator is what many a team needs.)

So developers can be far more effective than other developers. But this doesn't necessarily translate into getting much more work done unless the work at hand benefits from those increased skills and is a team bottleneck. Time and skill are not interchangeable quantities. But there is an even bigger problem with the idea of a 10x developer: Skills are not unipolar.

<!-- vale HouseStyle.OxfordComma = NO -->
You can't measure developer skill on a single axis like Leetcode scores or like pole vaulting, where you can either clear a bar at a certain height or not. Software development is a varied field: people doing firmware development have different skillsets than people building game engines, who have different skillsets than frontend JavaScript developers. And even within those roles, Software Development, like most fields, is not like a single event track-and-field contest. It's made up of many different components: System design, testing, debugging and more. It's more like the multi-skill [modern pentathlon](https://www.cbc.ca/sports/olympics/summer/modern-pentathlon/instant-expert-modern-pentathlon-1.3694080).
<!-- vale HouseStyle.OxfordComma = YES -->

<div class="wide">
{% picture {{site.pimages}}{{page.slug}}/header.jpg --alt {{ The modern pentathlon is an Olympic sport consisting of fencing, freestyle swimming, equestrian show jumping, pistol shooting, and pull request reviewing. }} %}
<figcaption>The modern pentathlon is an Olympic sport consisting of fencing, freestyle swimming, equestrian show jumping, pistol shooting, and pull request reviewing.<figcaption>
</div>

## On the Extremes of Software Development

The 10X meme is both too extreme, by implying that Fabrice Bellard[^4] could kick out simple crud tasks at 10X the speed I do, and not extreme enough, suggesting that I could build `ffmpeg` and `qemu` the same as Fabrice if I was just given more time.

[^4]: [Fabrice](https://bellard.org/) has created so many [amazing pieces](https://smartbear.com/blog/fabrice-bellard-portrait-of-a-super-productive-pro/) of software.

And also, the 10x meme, and how it's often used, implies that skills are interchangeable. Should a great database internals expert be able to build a great micro-services architecture?

So what term should you use instead of 10x developer? Try expert. As in 'John is a video encoding expert'. Or specialist: 'What I learned working with a postgres internals specialist'. Or if you want to sound like an MBA, use talent: 'I really need some exceptional compiler-backend talent to help with the incremental-compilation design'.

I guess what I'm saying is: terminology matters and we can do better than `10x`. We can be specific. Skills are not homogeneous, and people can quickly [improve their craft](https://danluu.com/p95-skill/) as long as we don't treat talent like some mythical quality.

{% include_html cta/bottom-cta.html %}
