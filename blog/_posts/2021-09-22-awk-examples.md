---
title: "Understanding AWK"
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
- [ ] Run mark down linter (`earthly +blog-lint-apply`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `earthly --build-arg NAME=2020-09-10-better-builds.md +link-opportunity` and find 1-5 places to incorporate links to other articles
- [ ] Raise PR

## Intro

One of the comments I heard around the JQ article was the JQ was so complex just like AWK. I have a confession to make - I don't know how to use AWK. I hear it mentioned sometimes and occasionally I see a really cool blog post where someone uses AWK to takes a giant spark task or big data workflow and reduce its complexity to a one-line in AWK.

So in this article I will myself, and you, the basics of AWK.

## What is AWK
AWK is a record processing tool written by AWK in 1977. After the success of tools like SED and GREP that worked with lines of text they created AWK as an experiment into how text processing tools could be extended to deal with numbers. GREP lets you search for lines that match a regualr experssion, and SED lets you do replacements. AWK lets you do calculations. This will make sense soon enough.

## How to Install GAWK

> The biggest reason to learn AWK, IMO, is that it's on pretty much every single linux distribution. You might not have perl or python. You WILL have AWK. Only the most minimal of minimal linux systems will exclude it. Even busybox includes awk. That's how essential it's viewed.
>
> https://news.ycombinator.com/item?id=28441887

AWK is part of the POSIX Standard. This means its already on your macbook and you linux server. There are several versions of AWK and for the basics whatever AWK you have will do. 

``` bash
$ awk --version
  GNU Awk 5.1.0, API: 3.0 (GNU MPFR 4.1.0, GNU MP 6.2.1)
  Copyright (C) 1989, 1991-2020 Free Software Foundation.
```

If you are doing something more involved with AWK, choose GNU awk (gawk,) which I installed using homebrew (`brew install gawk`) and which can also be installed on windows (`choco install gawk`). It is probably already on your linux distribution. 


## AWK Big Data

To understand how AWK works we will grab a small slice of the [amazon product reviews dataset](https://s3.amazonaws.com/amazon-reviews-pds/tsv/index.txt). 

```
curl https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Books_v1_01.tsv.gz |  gunzip -c > bookreviews.tsv

```
That should give us a large file of Amazon book reviews that look like this:

```
marketplace	customer_id	review_id	product_id	product_parent	product_title	product_category	star_rating	helpful_votes	total_votes	vine	verified_purchase	review_headline	review_body	review_date
US	22480053	R28HBXXO1UEVJT	0843952016	34858117	The Rising	Books	5	0	0	N	N	Great Twist on Zombie Mythos	I've known about this one for a long time, but just finally got around to reading it for the first time. I enjoyed it a lot!  What I liked the most was how it took a tired premise and breathed new life into it by creating an entirely new twist on the zombie mythos. A definite must read!	2012-05-03
```

Each row in this file represents the record of one book review. We can view it as a record like this:
TODO: insert record here

<div class="notice--info">
**Side Note: A Taste of Things to Come**

Now that I understand AWK, I'm finding lots of uses for it. The above record output is made with AWK and to display the size of the downloaded file I started with this:
```
$ ls -lh bookreviews.tsv
-rw-r--r--  1 adam  staff   6.2G Sep 15 12:54 bookreviews.tsv
```
But a little bit of AWK let me clean this up:
```
ls -lh bookreviews.tsv | awk '{ print $NF " " $5 }'
bookreviews.tsv 6.2G
```
</div>

## AWK Print

By default AWK expects to receive its input on standard in and output its results to standard out. The simplest thing you can do in AWK is Print the line.

```
$ echo "one two three" | awk '{ print }'
one two three
```
Note the braces. The syntax will make sense after seeing a couple examples.

We can selectively choose columns (which AWK calls fields):
```
$ echo "one two three" | awk '{ print $1 }'
one
$ echo "one two three" | awk '{ print $2 }'
two
$ echo "one two three" | awk '{ print $3 }'
three
```
You may have been expecting the first colum to be $0 and not $1 but $0 is something different:
```
$ echo "one two three" | awk '{ print $0 }'
one two three
```
It is the entire line! Incidentally AWK refers to each line as a record and each column as a field. 

All of this also works across multiple lines:
```
$ echo "one two three\n four five six" | awk '{ print $1 }'
one
four
```

And we can print more than one column:

```
$ echo "one two three\n four five six" | awk '{ print $1 $2 }'
onetwo
fourfive
```
But we need to put in spaces explicitly:

```
$  echo "one two three\n four five six" | awk '{ print $1 " " $2 }'
one two
four five
```



## Book Data

I can use this knowledge to pull the fields I care about from the amazon dataset. Like the marketplace:
```
$ awk '{ print $1 }' bookreviews.tsv| head 
marketplace
US
US
US
US
US
US
US
US
US
```
Or the customer_id:
```
$ awk '{ print $2 }' bookreviews.tsv| head 
customer_id
22480053
44244451
20357422
13235208
26301786
27780192
13041546
51692331
23108524
```
However, when I try to pull out the title things do not go well:
```
$ awk '{ print $6 }' bookreviews.tsv| head 
product_title
The
Sticky
Black
Direction
Until
Unfinished
The
Good
Patterns
```

## Field Seperators

By Default, AWK assumes that the fields in a record are space delimited. We can change the field seperator to use tabs using the `awk -F` option:
```
$ awk -F '\t' '{ print $6 }' bookreviews.tsv| head 
product_title
The Rising
Sticky Faith Teen Curriculum with DVD: 10 Lessons to Nurture Faith Beyond High 
Black Passenger Yellow Cabs: Of Exile And Excess In Japan
Direction and Destiny in the Birth Chart
Until the Next Time
Unfinished Business
The Republican Brain: The Science of Why They Deny Science- and Reality
Good Food: 101 Cakes & Bakes
Patterns and Quilts (Mathzones)
```

AWK also has convience values for accessing last field in a row:

```
$ awk -F '\t' '{ print $NF }' bookreviews.tsv| head 
review_date
2012-05-03
2012-05-03
2012-05-03
2012-05-03
2012-05-03
2012-05-03
2012-05-03
2012-05-03
2012-05-03
```

And you can easily work backwards from the last position forward by subtracting from `NF`.
```
$ awk -F '\t' '{ print $NF "\t" $(NF-2)}' bookreviews.tsv| head 
review_date     review_headline
2012-05-03      Great Twist on Zombie Mythos
2012-05-03      Helpful and Practical
2012-05-03      Paul
2012-05-03      Direction and Destiny in the Birth Chart
2012-05-03      This was Okay
2012-05-03      Excellent read!!!
2012-05-03      A must read for science thinkers
2012-05-03      Chocoholic heaven
2012-05-03      Quilt Art Projects for Children
```

<div class="notice--info">
**What I've learned**

AWK creates a variable for each field in a record ($1, $2 ... $NF), based on the field separator which is whitespace by default.

</div>

<div class="notice--info">
**Side Note: NF and NR**

`$NF` seems like a unusual name for printing the last column
, right? but `NF` is actually a variable holding the *Number of Fields* in a record. We are just using its value as an index to refer to the last field. 

We can print the actual value like this:
```
awk -F '\t' '{ print NF }' bookreviews.tsv| head  
15
15
15
15
15
15
15
15
15
15
```

Another variable AWK offers up for use is `NR`, the *number of records* so far. This is helpful if I need to print line numbers.

```
awk -F '\t' '{ print NR " " $(NF-2) }' bookreviews.tsv| head  
1 review_headline
2 Great Twist on Zombie Mythos
3 Helpful and Practical
4 Paul
5 Direction and Destiny in the Birth Chart
6 This was Okay
7 Excellent read!!!
8 A must read for science thinkers
9 Chocoholic heaven
10 Quilt Art Projects for Children
```

</div>

### AWK Pattern Match With Regular Expressions

Everything we've done so far has applied to every line in our file but the real power of AWK comes from pattern matching. Instead of using `head` to restrict our output, lets focus in on a specific book title.

```
awk -F '\t' '/245449872/{ print NR " " $(NF-2) }' bookreviews.tsv | head 
```

### AWK Printf

If I add in the star rating I start to hit one of the common problems of printing tabular data, field length.

```
awk -F '\t' '{ print $NF "\t" $(NF-2) "\t" $8}' bookreviews.tsv| head 
review_date     review_headline star_rating
2012-05-03      Great Twist on Zombie Mythos    5
2012-05-03      Helpful and Practical   5
2012-05-03      Paul    3
2012-05-03      Direction and Destiny in the Birth Chart        5
2012-05-03      This was Okay   3
2012-05-03      Excellent read!!!       5
2012-05-03      A must read for science thinkers        4
2012-05-03      Chocoholic heaven       4
2012-05-03      Quilt Art Projects for Children 5
```

We can switch from `print` to `printf` to fix this. `printf` works like it does in c and uses a format string and then a list of values. So my `print $NF "\t" $(NF-2) "\t" $8` becomes `printf "%s \t %s \t %s, $NF, $(NF-2), $8`. I can add right padding and fix my layout by changing `%s` to `%-Ns` where `N` is my desired column width. Putting it all together and we get: 

```
$ awk -F '\t' '{ printf "%s \t %-40s \t %s \n", $NF, $(NF-2), $8}' bookreviews.tsv| head 
review_date      review_headline                                 star_rating 
2012-05-03       Great Twist on Zombie Mythos                    5 
2012-05-03       Helpful and Practical                           5 
2012-05-03       Paul                                            3 
2012-05-03       Direction and Destiny in the Birth Chart        5 
2012-05-03       This was Okay                                   3 
2012-05-03       Excellent read!!!                               5 
2012-05-03       A must read for science thinkers                4 
2012-05-03       Chocoholic heaven                               4 
2012-05-03       Quilt Art Projects for Children                 5 
```
