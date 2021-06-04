---
title: "Incident Management Metrics"
categories:
  - Tutorial
toc: true
author: Adam
internal-links:
 - mtbf
 - mttr
 - mtta
 - metrics
 - incident management
---
## Intro
At the first software as a service company I worked at, now know as opentext acquisition #0324, we released new software monthly and measured quality by counting bugs and by how many large clients seemed upset at us.  Occasionally when something went really wrong we would do a stability release and spend a month only fixing bugs.  Testing was not a part of our build process, but a part of our team. We had full-time testing people working diligently to test each bug or new feature as it was completed. 

## MTBF: Mean Time Between Failures
When software was being released on a fixed timeline, like a new release every month, counting bug per release may have been sufficent but if software is released many times per week or even many times per day counting software failures per release is no longer meaningful and so another way to measure is required.

Mean time between failures is a metric from the field of reliability engineering.  Calculating it is simple: it is some amount of time over the numbers of failures in that time period. If in the last 30 days you have 2 production incidents, then the mean time between failure is 15 days.

T = some time period 
F = the count of failures 
MTBF = T / F

## MTTR: Mean Time To Recovery
Something funny happens when you start releasing much more frequently. You may end up with a higher count of issues in production but resolving them will happen much faster. If each change is release seperatly simply recovering from an incident will often be as easy as hitting a roll-back button. 

If you are measuring MTBF your software may be getting much but your numbers will be getting worse. Enter mean time to recovery. Mean time to recovery is just what it sounds like you start a timer when the incident starts and stop it when production is healthly - even a simple rollback counts. Average this number across incidents and you have MTTR. You now have a metric that measure that captures the health of your incidence response process. 

Incident #1 = Reported 10:00 am
Incident #1 = Addressed 12:00 pm
Recovery Time = 2 hours

Incident #2 = Reported 10:00 am 
Incident #2 = Addressed  2 days later at 10:00 am 
Recovery Time = 48 hours

Mean Time To Recovery:
48 + 2 / 2 = 25 hours


## MTTR: Mean time To Resolve
Rolling back to address an incident is a great idea. If it fixes the issue its the quickest way to get things back in a good place.  But there are other types of incidents. Imagine your application deadlocks every once in a while and you have to restart it to unlock. You could have a really great mean time to recovery but you've never actually addressed the root cause. This is what MTTR measures, not the time to get the service back up and running but the time to resolve the root cause and ensure the problem never happens again.  

The never-happens-again part is hard to achieve but very important. If you are resolving the root cause of each incident then quality will increase over time.  

Incident #3 = Reported day 1
Incident #3 = Addressed day 1
Incident #3 = Root Cause Analysis day 2
Incident #3 = Root Cause Addressed day 31
Resolve Time = 30 days

## MTTA: Mean Time To Acknowledge
Here are two incidents that all of our metrics so far would handle the same. 

Incident #1 = 
Mean time to acknowledge
calculating

## Others
    - mean time to restore
    - mean time between maintenance

## Summary

- heading: ??
- calculating X
- Mean Time Between Failures
- Mean Time to Recovery 
    - time to recover
- MTTR: Mean time to resolve
    - mean time to resolution
- MTTA: Mean time to acknowledge
e
- Lead Time
- Cycle time


This post is in the future, and won't show up in the published site

## Image without figure

An image with the alt text hidden.

![some alt text]({{site.images}}{{page.slug}}/alex-draw.png)\

An image with alt text printed below.

![some alt text]({{site.images}}{{page.slug}}/alex-draw.png)

## Image with explicit figure

{% include imgf src="alex-draw.png" alt="handddrawn cartoon for a person talking to a computer server" caption="Alex likes to draw and add a caption" %}

## Image with implicit figure

![This is my alt text and my figure. The alt text is used as the default figure if not specified.]({{site.images}}{{page.slug}}/alex-draw.png)

## Image Wide

<div class="wide">
![This should be wide]({{site.images}}{{page.slug}}/alex-draw.png)
</div>

### graph using matplotlib

``` matplotlib
import matplotlib.pyplot as plt

plt.figure()
plt.plot([0,1,2,3,4], [1,2,3,4,5])
plt.title('This is an example figure')
```

### Code blocks (with syntax highlighting)

``` go
    syntax = "proto3";
    package simplekeyvalue;
    option go_package = "kvapi";
    
    // The key/value API contains two procedures for storing and retrieving data
    service KeyValue {
      rpc Set (SetRequest) returns (SetReply) {}
      rpc Get (GetRequest) returns (GetReply) {}
    }
```

### Raw code blocks

```
{% raw %}
{{ raw template code}}
{% endraw %}
```

<figcaption>Use `raw` and `endraw` for code that overlaps with the liquid templates</figcaption>

## Fensed code blocks

~~~ scala
object Main extends App {
  println("Hello, World!")
}
~~~

### Code with Captions

``` scala
object Main extends App {
  println("Hello, World!")
}
```

<figcaption>Main.scala</figcaption>

<div class="notice">
**Notice**

Markdown here

- one
- two

</div>

<div class="notice--info">
**ℹ️  Notice Info**

Markdown here

- one
- two

</div>

<div class="notice--warning">
**Warning**

Markdown here

- one
- two

</div>

<div class="notice--success">
**Success**

Markdown here
</div>

### More example Image layouts

![align center](/blog/assets/images/authors/coreylarson.jpg){.align-center}\

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Massa enim nec dui nunc mattis enim ut. Cursus euismod quis viverra nibh cras. Posuere ac ut consequat semper viverra nam libero. Lectus nulla at volutpat diam ut venenatis tellus in. Nunc eget lorem dolor sed viverra ipsum. Lectus arcu bibendum at varius vel pharetra vel turpis. Cursus sit amet dictum sit amet justo donec. Eget nullam non nisi est sit amet facilisis. Scelerisque felis imperdiet proin fermentum leo. Imperdiet proin fermentum leo vel orci porta non pulvinar neque. Nulla facilisi morbi tempus iaculis urna id. Diam maecenas sed enim ut sem. Porttitor leo a diam sollicitudin. Neque gravida in fermentum et sollicitudin ac orci. Aliquet risus feugiat in ante metus. Vitae et leo duis ut diam quam nulla porttitor massa.

![alighn right](/blog/assets/images/authors/coreylarson.jpg){.align-right}\

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Massa enim nec dui nunc mattis enim ut. Cursus euismod quis viverra nibh cras. Posuere ac ut consequat semper viverra nam libero. Lectus nulla at volutpat diam ut venenatis tellus in. Nunc eget lorem dolor sed viverra ipsum. Lectus arcu bibendum at varius vel pharetra vel turpis. Cursus sit amet dictum sit amet justo donec. Eget nullam non nisi est sit amet facilisis. Scelerisque felis imperdiet proin fermentum leo. Imperdiet proin fermentum leo vel orci porta non pulvinar neque. Nulla facilisi morbi tempus iaculis urna id. Diam maecenas sed enim ut sem. Porttitor leo a diam sollicitudin. Neque gravida in fermentum et sollicitudin ac orci. Aliquet risus feugiat in ante metus. Vitae et leo duis ut diam quam nulla porttitor massa.

![align left](/blog/assets/images/authors/coreylarson.jpg){.align-left}\

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Massa enim nec dui nunc mattis enim ut. Cursus euismod quis viverra nibh cras. Posuere ac ut consequat semper viverra nam libero. Lectus nulla at volutpat diam ut venenatis tellus in. Nunc eget lorem dolor sed viverra ipsum. Lectus arcu bibendum at varius vel pharetra vel turpis. Cursus sit amet dictum sit amet justo donec. Eget nullam non nisi est sit amet facilisis. Scelerisque felis imperdiet proin fermentum leo. Imperdiet proin fermentum leo vel orci porta non pulvinar neque. Nulla facilisi morbi tempus iaculis urna id. Diam maecenas sed enim ut sem. Porttitor leo a diam sollicitudin. Neque gravida in fermentum et sollicitudin ac orci. Aliquet risus feugiat in ante metus. Vitae et leo duis ut diam quam nulla porttitor massa.

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Massa enim nec dui nunc mattis enim ut. Cursus euismod quis viverra nibh cras. Posuere ac ut consequat semper viverra nam libero. Lectus nulla at volutpat diam ut venenatis tellus in. Nunc eget lorem dolor sed viverra ipsum. Lectus arcu bibendum at varius vel pharetra vel turpis. Cursus sit amet dictum sit amet justo donec. Eget nullam non nisi est sit amet facilisis. Scelerisque felis imperdiet proin fermentum leo. Imperdiet proin fermentum leo vel orci porta non pulvinar neque. Nulla facilisi morbi tempus iaculis urna id. Diam maecenas sed enim ut sem. Porttitor leo a diam sollicitudin. Neque gravida in fermentum et sollicitudin ac orci. Aliquet risus feugiat in ante metus. Vitae et leo duis ut diam quam nulla porttitor massa.
![pic with only 100px width]({{site.images}}{{page.slug}}/alex-draw.png){width=300px .align-right}\
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Massa enim nec dui nunc mattis enim ut. Cursus euismod quis viverra nibh cras. Posuere ac ut consequat semper viverra nam libero. Lectus nulla at volutpat diam ut venenatis tellus in. Nunc eget lorem dolor sed viverra ipsum. Lectus arcu bibendum at varius vel pharetra vel turpis. Cursus sit amet dictum sit amet justo donec. Eget nullam non nisi est sit amet facilisis. Scelerisque felis imperdiet proin fermentum leo. Imperdiet proin fermentum leo vel orci porta non pulvinar neque. Nulla facilisi morbi tempus iaculis urna id. Diam maecenas sed enim ut sem. Porttitor leo a diam sollicitudin. Neque gravida in fermentum et sollicitudin ac orci. Aliquet risus feugiat in ante metus. Vitae et leo duis ut diam quam nulla porttitor massa.

### More Example Usage

- [Theme Guide](https://mmistakes.github.io/minimal-mistakes/docs/quick-start-guide/)
- Sample [Rendered Posts](https://mmistakes.github.io/minimal-mistakes/year-archive/) and [Raw mardown](https://github.com/mmistakes/minimal-mistakes/tree/d6444412c63aea5e47241ef536509fb1bfef4830/docs/_posts)
- Markdown stuff (pandoc): [Graphs](https://laurentrdc.github.io/pandoc-plot/) and [markdown](https://pandoc.org/MANUAL.html#pandocs-markdown)
