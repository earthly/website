---
title: "Stop using Pie-Charts: Use These Alternative Bar Charts Instead -- A Practical Guide to Generating Easy-to-Read Plots Using Matplotlib and Python"
categories:
  - Tutorials
internal-links:
 - python
 - matplotlib
 - pandas

author: Alex
---
## What's Wrong With Pie Charts

Humans have a hard time comparing areas. Try it for yourself: **Which slice is the largest? Which is the smallest?**

<div class="wide">
{% picture content-nocrop {{site.pimages}}{{page.slug}}/pie-chart.png --picture --alt {{ Can you rank the slices from largest to smallest? }} %}
<figcaption>Can you rank the slices from largest to smallest?</figcaption>
</div>

Instead, if we plot the exact data points in a linear dimension; it's trivial:

<div class="wide">
{% picture content-nocrop {{site.pimages}}{{page.slug}}/horizontal-lollipop-chart.png --picture --alt {{ largest to smallest values in ascending order }} %}
<figcaption>Using a horizontal lollipop bar plot ranks values in ascending order</figcaption>
</div>

### Stevens' Power Law

In 1957 psychologist Stanley Smith Stevens published a body of work which went on to be named the [Stevens' Power Law](https://en.wikipedia.org/wiki/Stevens%27s_power_law).
The law describes how people perceive intensities of various stimuli relative to other stimuli.
It showed that people, on average, tend to perceive an actual 100% growth in area as being approximately 60% bigger.

### Cleveland and McGill

In 1984, Cleveland and McGill published [experimental results](http://euclid.psych.yorku.ca/www/psy6135/papers/ClevelandMcGill1984.pdf) evaluating various data visualization types.
They too showed that interrupting linear-based data visualizations was less error-prone when compared to visualizations that used angles or area.

### Still Think You Are Above Average and Can Read a Pie-Chart?

Then consider picking up a copy of [illusion](https://boardgamegeek.com/boardgame/244995/illusion). It's a card game where players
must rank cards based on the visible area of a particular color. On your turn you must either a) draw and place a new card in the correct order,
or b) claim that the current order of ranked cards is incorrect. If you claim the order is incorrect, you flip all the cards to reveal the actual area, and
if it's incorrect the previous player must take all the cards; however, if you are incorrect and *it is in ascending order*, then you take all the cards.

## What Do You Call the Day After Two Non-Stop Days of Rain?

Monday.

In this section, we will switch from using randomly-generated data to using precipitation data, which was previously described in ["Plotting Precipitation with Python, Pandas and Matplotlib"](/blog/plotting-rainfall-data-with-python-and-matplotlib); in particular Victoria BC's daily precipitation for 2020. Let's See if it actually rains more on the weekend.

<div class="wide">
{% picture content-nocrop {{site.pimages}}{{page.slug}}/rainfall-by-day-of-week-pie-chart-is-hard-to-read.png --picture --alt {{ amount of rain by day of week as a pie chart }} %}
<figcaption>Distribution of precipitation by day of week: Saturday does look smaller than others, however the second ranked day is not clear</figcaption>
</div>

### Let's Try That Again

Here's the same data plotted horizontally:

<div class="wide">
{% picture content-nocrop {{site.pimages}}{{page.slug}}/rainfall-by-day-of-week.png --picture --alt {{ amount of rain by day of week as a dot chart }} %}
<figcaption>Distribution of precipitation by day of week: Avoid Fridays!</figcaption>
</div>

Interestingly Saturdays and Sundays were significantly[^1] drier than most weekdays; whereas Fridays appear to be downright ugly.

### Plotting Distributions Using Box and Whisker Plots

I Wonder why Fridays received so much more precipitation compared to other days? Maybe we had a single Friday that poured rain. Rather than look at the total precipitation, let's look at a distribution of precipitation. We will use a box and whisker plot (also known as simply a box plot).

<div class="wide">
{% picture content-nocrop {{site.pimages}}{{page.slug}}/rainfall-by-day-of-week-box-and-whisker-with-outliers.png --picture --alt {{ amount of rain by day of week as a dot chart }} %}
<figcaption>Box and whisker plot of precipitation by day of week</figcaption>
</div>

Percentiles are at the core of a box and whisker plot. The plot is comprised of four parts: 1) a rectangular box displays the lower and upper quartiles (the 25th and 75th percentiles), 2) a vertical line drawn inside the rectangular box, which represents the median value (the 50th percentile), 3) whiskers which extend on beyond the rectangle to display the minimum and maximum values, and optionally 4) outliers which are displayed as points which were rejected while calculating the percentiles.

It turns out that the heaviest day of rain in 2020 occurred on a Monday! Whereas Fridays contained five days of heavy rain, which contributed
to the large total precipitation value displayed in a previous plot.

It's possible to reduce (or completely disable) outlier detection, by setting a very large [`whis`](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.boxplot.html) value; however doing presents a simplified version of the story:

<div class="wide">
{% picture content-nocrop {{site.pimages}}{{page.slug}}/rainfall-by-day-of-week-box-and-whisker.png --picture --alt {{ amount of rain by day of week as a dot chart }} %}
<figcaption>Box and whisker plot without omitting outliers</figcaption>
</div>

### Plotting the Number of Wet Days in a Year

If you have the option of staying inside, does 50mm vs 80mm of precipitation really matter? Instead, let's plot the number of days in a year where it rained.

<div class="wide">
{% picture content-nocrop {{site.pimages}}{{page.slug}}/number-of-wet-days-by-day-of-week.png --picture --alt {{ number of days that experienced precipitation }} %}
<figcaption>Day of week distribution of rainy days</figcaption>
</div>

One rebuttal to using pie charts, I've heard is "well how do I show the values sum to 100%?", if it's not clear by your text, you can just add this to a title, or figure description.

*If you absolutely want to show an area-based chart, consider using a 10x10 [waffle chart](https://github.com/gyli/PyWaffle), but keep in mind that humans have a hard time perceiving changes in area. The 10x10 suggestion allows users to treat each box as a percentage point, which they can count if they want.*

## Generating Horizontal Charts Using Python and Matplotlib

The following section provides some sample python and matplotlib code to help you get started.

### Random Data

First, let's generate some random data. In particular the data will be positive
values randomly distributed along a log-normal curve. Alternatively the absolute
value of a Gaussian curve could have been used.

```python
import matplotlib.pyplot as plt
import random

phonetics = [
    "alpha","bravo","charlie","delta","echo","foxtrot","golf","hotel",
    "india","juliet","kilo","lima","mike","november","oscar","papa",
    "quebec","romeo","sierra","tango","uniform","victor","whiskey",
    "x-ray","yankee","zulu"]

def get_random_data(num_data=5, mu=1, sigma=0.1):
    if not (0 < num_data <= len(phonetics)):
        raise ValueError(num_data)
    data = [random.lognormvariate(mu, sigma) for _ in range(num_data)]
    labels = list(phonetics[:len(data)])
    return data, labels

```

Calling `print(get_random_data(5))`, will result in a tuple containing a list of 5 random values, along with a list of 5 labels:

```
(
  [2.3830, 2.3067, 2.7829, 2.8205, 2.7673],
  ['alpha', 'bravo', 'charlie', 'delta', 'echo']
)
```

### Generating a Horizontal Plot

The following will save the plot to the current directory under `horizontal-bar-chart.png`.

```python
import matplotlib.pyplot as plt

def plot_horizontal_bar(data, labels, output_path, xlabel=None, title=None):
    fig = plt.figure(figsize=(10.0, 5.0), dpi=100)
    ax = fig.add_axes([0,0,1,1])
    ax.barh(labels, data, height=0.1)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    fig.savefig(output_path, bbox_inches='tight')

data, labels = get_random_data()
plot_horizontal_bar(data, labels, 'horizontal-bar-chart.png',
    xlabel='x unit', title='five random normal values')
```

### Generating a Horizontal Lollipop Plot

The following will generate a lollipop chart (also known as a dot chart):

```python
def plot_horizontal_lollipop(data, labels, output_path, xlabel=None, title=None):
    fig = plt.figure(figsize=(10.0, 3.0), dpi=100)
    ax = fig.add_axes([0,0,1,1])
    ax.set_title(title)

    ax.hlines(labels, xmin=[0]*len(data), xmax=data, alpha=0.4, lw=2, linestyle='dotted', zorder=1)
    ax.scatter(data, labels, zorder=2)

    ax.set_xlim([0,max(data)*1.1])
    ax.set_xlabel(xlabel)
    fig.savefig(output_path, bbox_inches='tight')

data, labels = get_random_data()
plot_horizontal_lollipop(data, labels, 'horizontal-lollipop-chart.png',
    xlabel='x unit', title='five random normal values')
```

### Generating the Plots Used in This Article

If you would like to try generating the above graphs, all the code (and data) can be found under
[github.com/earthly/example-plotting-precipitation](https://github.com/earthly/example-dont-use-pie-charts).

In particular, the code for generating the randomized bar charts and lollipop charts are under
[plotrandom.py](https://github.com/earthly/example-dont-use-pie-charts/blob/main/dontusepiecharts/plotrandom.py),
and the code for precipitation charts under
[plotprecipitation.py](https://github.com/earthly/example-dont-use-pie-charts/blob/main/dontusepiecharts/plotprecipitation.py).

The code provides a minimal set of functions which wrap the matplotlib functions stored under [plot.py](https://github.com/earthly/example-dont-use-pie-charts/blob/main/dontusepiecharts/plot.py) which shows how to sort, reverse, and convert the values into percentages -- perhaps it will be valuable the next time you want to quickly plot some data.

Even the code to generate the [Pac-Man pie-chart](https://github.com/earthly/example-dont-use-pie-charts/blob/main/dontusepiecharts/pacman.py) is included, but please don't use it
(for real data).

{% include cta/cta1.html %}

[^1]: "significantly" is being used in the literary sense -- I didn't perform a significance test.
