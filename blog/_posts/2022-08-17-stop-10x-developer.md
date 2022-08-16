---
title: "Stop using the term 10x developer"
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

Do 10x develoeprs exist? How can I hire a 10x developer? Things I learned from a 10x developer and quotes like this:

> 10x engineers hate meetings. They think it is a waste of time and obvious things are being discussed. They attend meetings because the manager has called for a "Staff meeting" to discuss the features and status.
> 
>

Can we stop talking like this? 

A 10x developer is defined like this:

> A 10x developer is a professional who is 10 times more productive than other developers with an equal level of expertise in the field. That is to say, a 10x developer completes 10 times more tasks and writes 10 times better code than any other competent member of their team working in the same conditions.
> [Who Is a 10x Developer and How to Become One?](https://www.actitime.com/productivity/10x-developer)

## They exist but not like that

Yes, 10x Developers, by some definition exist. Development skills obviously vary and can be improved. Whether you beleive that greatness is born, created or both you must recognize that skills aren't uniform and that people vary in their ability to successfully complete tasks. 

Those that question the existance of outsized skill perhaps question the 
10x. Can anyone really be 10x better at a task than anyone else? And this gets at the heart of the reason we should give up the term 10x. But yes, depending on how you meausre things the problem is that 10x is too small a number.

Let's look at an extreme example.

## Yep, Leet Code Time

If we want to compare developers we need a means to do so and Leet Code rankings are the best I can come up with.

( I'm really not saying leetcode problems is how we should judge developers. I'm just showing that 10x problem solving ability in a specific niche is not unreasonable. )

Contest competitors on Leetcode have scores and scores can be translated into the probability that that user could complete a problem. 

Specifically "In practice, if you meet a problem whose rating is equal to your rating, you are expected to solve it in half of your contests."[^1]

[^1]: [source](https://leetcode.com/discuss/study-guide/1965086/How-to-practice-for-2200%2B-rating-in-LC)

This is because LeetCode uses an ELO rankings, which are very easy to convert to a success multiplier. LeetCode does not share problem ratings, but user zerotrac calcuates them on a regular basis and shows them on [github](https://github.com/zerotrac/leetcode_problem_rating/blob/main/ratings.txt)

So using this, and a ELO to win [probablality table](https://www.318chess.com/elo.html) I can tell you that the leetcode problem [Count Ways to Make Array With Product](https://leetcode.com/problems/count-ways-to-make-array-with-product/) problem can be solved by 95% of users with a ranking of 3000 but only by about 1% of users with a rankings of 1700. 

If you were to imagine a Jira board made up purely of 2500 leet code difficulty problems, then (and we are probably stretching the math a little here) a 3000 ranked player would as effective as 95 1700 ratings users. A 95X developer.

So certainly a 10x Developer can exist. But really the way people talk about this mythical 10X developer helps highlight why its time to kill this term.

## The Reason I Can Clear The Bar

> Taking about 10x engineers, as if it's a specific dog breed, is pretty dumb.
>
> Yes, different engineers are differently effective. That's true in any walk of life.

> [Ron Minsky](https://twitter.com/yminsky/status/1150158104560115712)

Variation in skills isn't unique to software development. Also for a skill to materially impact a team or an organization in need to be a limiting factor. A developer who is a 10x communicator is what many a team needs. But one thing I don't like about the 10X developer terminology is it's emphasis on time. A 10x developer gets 10x more work done. I'm not sure this is true.

Another analogy:

<blockquote class="instagram-media" data-instgrm-captioned data-instgrm-permalink="https://www.instagram.com/p/CgFRxXdpp8_/?utm_source=ig_embed&amp;utm_campaign=loading" data-instgrm-version="14" style=" background:#FFF; border:0; border-radius:3px; box-shadow:0 0 1px 0 rgba(0,0,0,0.5),0 1px 10px 0 rgba(0,0,0,0.15); margin: 1px; max-width:540px; min-width:326px; padding:0; width:99.375%; width:-webkit-calc(100% - 2px); width:calc(100% - 2px);"><div style="padding:16px;"> <a href="https://www.instagram.com/p/CgFRxXdpp8_/?utm_source=ig_embed&amp;utm_campaign=loading" style=" background:#FFFFFF; line-height:0; padding:0 0; text-align:center; text-decoration:none; width:100%;" target="_blank"> <div style=" display: flex; flex-direction: row; align-items: center;"> <div style="background-color: #F4F4F4; border-radius: 50%; flex-grow: 0; height: 40px; margin-right: 14px; width: 40px;"></div> <div style="display: flex; flex-direction: column; flex-grow: 1; justify-content: center;"> <div style=" background-color: #F4F4F4; border-radius: 4px; flex-grow: 0; height: 14px; margin-bottom: 6px; width: 100px;"></div> <div style=" background-color: #F4F4F4; border-radius: 4px; flex-grow: 0; height: 14px; width: 60px;"></div></div></div><div style="padding: 19% 0;"></div> <div style="display:block; height:50px; margin:0 auto 12px; width:50px;"><svg width="50px" height="50px" viewBox="0 0 60 60" version="1.1" xmlns="https://www.w3.org/2000/svg" xmlns:xlink="https://www.w3.org/1999/xlink"><g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><g transform="translate(-511.000000, -20.000000)" fill="#000000"><g><path d="M556.869,30.41 C554.814,30.41 553.148,32.076 553.148,34.131 C553.148,36.186 554.814,37.852 556.869,37.852 C558.924,37.852 560.59,36.186 560.59,34.131 C560.59,32.076 558.924,30.41 556.869,30.41 M541,60.657 C535.114,60.657 530.342,55.887 530.342,50 C530.342,44.114 535.114,39.342 541,39.342 C546.887,39.342 551.658,44.114 551.658,50 C551.658,55.887 546.887,60.657 541,60.657 M541,33.886 C532.1,33.886 524.886,41.1 524.886,50 C524.886,58.899 532.1,66.113 541,66.113 C549.9,66.113 557.115,58.899 557.115,50 C557.115,41.1 549.9,33.886 541,33.886 M565.378,62.101 C565.244,65.022 564.756,66.606 564.346,67.663 C563.803,69.06 563.154,70.057 562.106,71.106 C561.058,72.155 560.06,72.803 558.662,73.347 C557.607,73.757 556.021,74.244 553.102,74.378 C549.944,74.521 548.997,74.552 541,74.552 C533.003,74.552 532.056,74.521 528.898,74.378 C525.979,74.244 524.393,73.757 523.338,73.347 C521.94,72.803 520.942,72.155 519.894,71.106 C518.846,70.057 518.197,69.06 517.654,67.663 C517.244,66.606 516.755,65.022 516.623,62.101 C516.479,58.943 516.448,57.996 516.448,50 C516.448,42.003 516.479,41.056 516.623,37.899 C516.755,34.978 517.244,33.391 517.654,32.338 C518.197,30.938 518.846,29.942 519.894,28.894 C520.942,27.846 521.94,27.196 523.338,26.654 C524.393,26.244 525.979,25.756 528.898,25.623 C532.057,25.479 533.004,25.448 541,25.448 C548.997,25.448 549.943,25.479 553.102,25.623 C556.021,25.756 557.607,26.244 558.662,26.654 C560.06,27.196 561.058,27.846 562.106,28.894 C563.154,29.942 563.803,30.938 564.346,32.338 C564.756,33.391 565.244,34.978 565.378,37.899 C565.522,41.056 565.552,42.003 565.552,50 C565.552,57.996 565.522,58.943 565.378,62.101 M570.82,37.631 C570.674,34.438 570.167,32.258 569.425,30.349 C568.659,28.377 567.633,26.702 565.965,25.035 C564.297,23.368 562.623,22.342 560.652,21.575 C558.743,20.834 556.562,20.326 553.369,20.18 C550.169,20.033 549.148,20 541,20 C532.853,20 531.831,20.033 528.631,20.18 C525.438,20.326 523.257,20.834 521.349,21.575 C519.376,22.342 517.703,23.368 516.035,25.035 C514.368,26.702 513.342,28.377 512.574,30.349 C511.834,32.258 511.326,34.438 511.181,37.631 C511.035,40.831 511,41.851 511,50 C511,58.147 511.035,59.17 511.181,62.369 C511.326,65.562 511.834,67.743 512.574,69.651 C513.342,71.625 514.368,73.296 516.035,74.965 C517.703,76.634 519.376,77.658 521.349,78.425 C523.257,79.167 525.438,79.673 528.631,79.82 C531.831,79.965 532.853,80.001 541,80.001 C549.148,80.001 550.169,79.965 553.369,79.82 C556.562,79.673 558.743,79.167 560.652,78.425 C562.623,77.658 564.297,76.634 565.965,74.965 C567.633,73.296 568.659,71.625 569.425,69.651 C570.167,67.743 570.674,65.562 570.82,62.369 C570.966,59.17 571,58.147 571,50 C571,41.851 570.966,40.831 570.82,37.631"></path></g></g></g></svg></div><div style="padding-top: 8px;"> <div style=" color:#3897f0; font-family:Arial,sans-serif; font-size:14px; font-style:normal; font-weight:550; line-height:18px;">View this post on Instagram</div></div><div style="padding: 12.5% 0;"></div> <div style="display: flex; flex-direction: row; margin-bottom: 14px; align-items: center;"><div> <div style="background-color: #F4F4F4; border-radius: 50%; height: 12.5px; width: 12.5px; transform: translateX(0px) translateY(7px);"></div> <div style="background-color: #F4F4F4; height: 12.5px; transform: rotate(-45deg) translateX(3px) translateY(1px); width: 12.5px; flex-grow: 0; margin-right: 14px; margin-left: 2px;"></div> <div style="background-color: #F4F4F4; border-radius: 50%; height: 12.5px; width: 12.5px; transform: translateX(9px) translateY(-18px);"></div></div><div style="margin-left: 8px;"> <div style=" background-color: #F4F4F4; border-radius: 50%; flex-grow: 0; height: 20px; width: 20px;"></div> <div style=" width: 0; height: 0; border-top: 2px solid transparent; border-left: 6px solid #f4f4f4; border-bottom: 2px solid transparent; transform: translateX(16px) translateY(-4px) rotate(30deg)"></div></div><div style="margin-left: auto;"> <div style=" width: 0px; border-top: 8px solid #F4F4F4; border-right: 8px solid transparent; transform: translateY(16px);"></div> <div style=" background-color: #F4F4F4; flex-grow: 0; height: 12px; width: 16px; transform: translateY(-4px);"></div> <div style=" width: 0; height: 0; border-top: 8px solid #F4F4F4; border-left: 8px solid transparent; transform: translateY(-4px) translateX(8px);"></div></div></div> <div style="display: flex; flex-direction: column; flex-grow: 1; justify-content: center; margin-bottom: 24px;"> <div style=" background-color: #F4F4F4; border-radius: 4px; flex-grow: 0; height: 14px; margin-bottom: 6px; width: 224px;"></div> <div style=" background-color: #F4F4F4; border-radius: 4px; flex-grow: 0; height: 14px; width: 144px;"></div></div></a><p style=" color:#c9c8cd; font-family:Arial,sans-serif; font-size:14px; line-height:17px; margin-bottom:0; margin-top:8px; overflow:hidden; padding:8px 0 7px; text-align:center; text-overflow:ellipsis; white-space:nowrap;"><a href="https://www.instagram.com/p/CgFRxXdpp8_/?utm_source=ig_embed&amp;utm_campaign=loading" style=" color:#c9c8cd; font-family:Arial,sans-serif; font-size:14px; font-style:normal; font-weight:normal; line-height:17px; text-decoration:none;" target="_blank"></p></div></blockquote> <script async src="//www.instagram.com/embed.js"></script>

Katie Nageotte, Olypmic champion pole vaulter can easily clear a bar 4 meters high. Her personal best is 4.95 meters ( which is over 16 feet high, American readers ).  I will never be able to clear a 4 meter bar. My time to clear a 4 meeter high bar is 1/0 seconds. So is she infinite times better at pole vaulting than me? 

Well, yes she is. But my point is it's not a useful way to measure varation in skills because I'm just as fast at her at clearing a 3 foot bar. Time and skill are not interchangable quantities. Skills aren't even neccarily interchangeable from one domain to another. In fact, the biggest problem with the 10x developer term is it implies developer skill can be measured on a single axis like leetcode problem or like pole vaulting, when everyone knows building software's closest track and field analogue is the multi-skill modern pentaholon.

<div class="wide">
{% picture {{site.pimages}}{{page.slug}}/8020.png --alt {{ The modern pentathlon is an Olympic sport consisting of fencing, freestyle swimming, equestrian show jumping, pistol shooting, and cross country running.  }} %}
<figcaption>The modern pentathlon is an Olympic sport consisting of fencing, freestyle swimming, equestrian show jumping, pistol shooting, and cross country running.<figcaption>
</div>


## On the Extremes of Software Development

The 10X mem is both too extreme, by implying that Fabrice Bellard could kick out simple crud tasks at 10X the speed I do, and not extreme enough, in that it implies that I could build `ffmpeg` and `qemu` the same as fabrice if I was just given more time.

So what term should you use instead of 10x developer? Try expert. As in 'John is a video encoding expert'.  Or specialist like:  'What I learned working with a postgres internals specialist'. Or if you really want to sound like an MBA use talent: 'I really need some exceptional compiler backend talent to help with the incremental complication design'.

I guess what I'm saying is be specific. Skills are not homogeneous and talented people don't have to be treated like a rare pokemon. Specificity leads to clear communication.



Links:
https://leetcode.com/discuss/study-guide/1965086/How-to-practice-for-2200%2B-rating-in-LC


https://www.318chess.com/elo.html

https://twitter.com/skirani/status/1149302828420067328?lang=en
