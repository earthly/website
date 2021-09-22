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

## What Is AWK

AWK is a record processing tool written by AWK in 1977. After the success of tools like SED and GREP that worked with lines of text they created AWK as an experiment into how text processing tools could be extended to deal with numbers. GREP lets you search for lines that match a regualr experssion, and SED lets you do replacements. AWK lets you do calculations. This will make sense soon enough.

## How to Install GAWK

> The biggest reason to learn AWK, IMO, is that it's on pretty much every single linux distribution. You might not have perl or python. You WILL have AWK. Only the most minimal of minimal linux systems will exclude it. Even busybox includes awk. That's how essential it's viewed.
>
> https://news.ycombinator.com/item?id=28441887

AWK is part of the POSIX Standard. This means its already on your macbook and you linux server. There are several versions of AWK and for the basics whatever AWK you have will do. 

``` bash
$ awk --version
``` 
```
  GNU Awk 5.1.0, API: 3.0 (GNU MPFR 4.1.0, GNU MP 6.2.1)
  Copyright (C) 1989, 1991-2020 Free Software Foundation.
```

If you are doing something more involved with AWK, choose GNU awk (gawk,) which I installed using homebrew (`brew install gawk`) and which can also be installed on windows (`choco install gawk`). It is probably already on your linux distribution. 


## AWK Big Data

To understand how AWK works we will grab a small slice of the [amazon product reviews dataset](https://s3.amazonaws.com/amazon-reviews-pds/tsv/index.txt). 

``` bash
$ curl https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Books_v1_01.tsv.gz | /
  gunzip -c > / 
  bookreviews.tsv
```

<div class="notice--warning">

**❗ Disk Space Warning**

The above file is over 6 gigs unzipped. If you don't have much space you can play along by just grabbing the first ten thousand rows. 

```
$ curl https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Books_v1_01.tsv.gz \
  | gunzip -c \
  | head -n 10000 \
  > bookreviews.tsv
```

</div>

That should give us a large file of Amazon book reviews that look like this:

``` ini
marketplace	customer_id	review_id	product_id	product_parent	product_title	product_category	star_rating	helpful_votes	total_votes	vine	verified_purchase	review_headline	review_body	review_date
US	22480053	R28HBXXO1UEVJT	0843952016	34858117	The Rising	Books	5	0	0	N	N	Great Twist on Zombie Mythos	I've known about this one for a long time, but just finally got around to reading it for the first time. I enjoyed it a lot!  What I liked the most was how it took a tired premise and breathed new life into it by creating an entirely new twist on the zombie mythos. A definite must read!	2012-05-03
```

Each row in this file represents the record of one book review. We can view it as a record like this:
TODO: insert record here

## AWK Print

By default AWK expects to receive its input on standard in and output its results to standard out. The simplest thing you can do in AWK is Print the line.

``` bash
$ echo "one two three" | awk '{ print }'
one two three
```
Note the braces. The syntax will make sense after seeing a couple examples.

We can selectively choose columns (which AWK calls fields):
``` bash
$ echo "one two three" | awk '{ print $1 }'
one
$ echo "one two three" | awk '{ print $2 }'
two
$ echo "one two three" | awk '{ print $3 }'
three
```
You may have been expecting the first colum to be $0 and not $1 but $0 is something different:
``` bash
$ echo "one two three" | awk '{ print $0 }'
``` 
``` ini
one two three
```
It is the entire line! Incidentally AWK refers to each line as a record and each column as a field. 

All of this also works across multiple lines:
``` bash
$ echo "
 one two three
 four five six" \
 | awk '{ print $1 }'
```
``` ini
one
four
```

And we can print more than one column:

``` bash
$ echo "
 one two three
 four five six" \
| awk '{ print $1 $2 }'
```
``` ini
onetwo
fourfive
```

But we need to put in spaces explicitly:

``` bash
$ echo "
 one two three
 four five six" \
| awk '{ print $1 " " $2 }'
```
``` ini
one two
four five
```



## Book Data

I can use this knowledge to pull the fields I care about from the amazon dataset. Like the marketplace:
``` bash
$ awk '{ print $1 }' bookreviews.tsv| head 
```
``` ini
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
``` bash
$ awk '{ print $2 }' bookreviews.tsv| head 
```
``` ini
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
``` bash
$ awk '{ print $6 }' bookreviews.tsv| head 
```
``` ini
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

To fix this, I need to configure my field seperator.

## Field Seperators

By Default, AWK assumes that the fields in a record are space delimited. We can change the field seperator to use tabs using the `awk -F` option:

``` bash
$ awk -F '\t' '{ print $6 }' bookreviews.tsv| head 
```
``` ini
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

``` bash
$ awk -F '\t' '{ print $NF }' bookreviews.tsv| head 
```
``` ini
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
``` bash
$ awk -F '\t' '{ print $NF "\t" $(NF-2)}' bookreviews.tsv| head 
```
``` ini
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
, right? 
But `NF` is actually a variable holding the *Number of Fields* in a record. We are just using its value as an index to refer to the last field. 

We can print the actual value like this:
``` bash
awk -F '\t' '{ print NF }' bookreviews.tsv| head  
```
``` ini
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

``` bash
awk -F '\t' '{ print NR " " $(NF-2) }' bookreviews.tsv| head  
```
``` ini
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

Everything we've done so far has applied to every line in our file but the real power of AWK comes from pattern matching. You can give AWK a pattern to match each line on like this:
``` bash
$ echo "aa \n bb \n cc" | awk '/bb/'
bb
```
This lets you use AWK like you would use GREP and you can combine this with the field access and printing we've done so far:
``` bash
$ echo "aa 10\n bb 20 \n cc 30" | awk '/bb/{ print $2 }'
bb
```

Using this knowledge, I can easily grab reviews by product_id and print the book title ($6):

``` bash
$ awk -F '\t' '/0439023483/{ print $6  }' bookreviews.tsv | head
```
``` ini
The Hunger Games (The Hunger Games, Book 1)
The Hunger Games (The Hunger Games, Book 1)
The Hunger Games (The Hunger Games, Book 1)
The Hunger Games (The Hunger Games, Book 1)
The Hunger Games (The Hunger Games, Book 1)
The Hunger Games (The Hunger Games, Book 1)
The Hunger Games (The Hunger Games, Book 1)
The Hunger Games (The Hunger Games, Book 1)
The Hunger Games (The Hunger Games, Book 1)
The Hunger Games (The Hunger Games, Book 1)
The Hunger Games (The Hunger Games, Book 1)
The Hunger Games (The Hunger Games, Book 1)
The Hunger Games (The Hunger Games, Book 1)
```
<figcaption>
The amazon reviews dataset I'm using is from 2012. Hunger Games we really big then
</figcaption>

I should be able to do some interesting data analysis on these reviews, but first there is a problem. `/0439023483/` is matching any line with that number in it anywhere and I seem to be getting some false positives:

``` bash
$ awk -F '\t' '/0439023483/{ print $6 }' bookreviews.tsv | sort |  uniq      
```
``` ini
Birthmarked
Blood Red Road
Catching Fire (The Hunger Games)
Divergent
Enclave
Fire (Graceling Realm Books)
Futuretrack 5
Girl in the Arena
...
```
The problem is the file has a `product_parent` column and since I'm matching on the whole line I'm getting back all the related child products. 

It is sort of like this
``` bash
$ cat hunger-tree.table 
  title parent
  hunger_games none
  sequel hunger_games
  sequel_again hunger_games
$ awk '/hunger_games/' hunger-tree.table 
  hunger_games none
  sequel hunger_games
  sequel_again hunger_games
```

I can fix this by specifying a field to pattern match on:
``` bash
$ echo "key1 key2 value1\n key2 key3 value2 \n key5 key1 value3" | awk '$1/key2/{ print $2 }'
bb
```

I can fix this by using `$field == "value"` in my pattern

``` bash
$ awk '$1 =="hunger_games"{ print $1}'
hunger_games
```
I can see that it works with the amazon dataset as well:
``` bash
awk -F '\t' '$4 == "0439023483"{ print $6 }' bookreviews.tsv | sort |  uniq 
The Hunger Games (The Hunger Games, Book 1)
```

I'd like to calculate the average review score for hunger games in my dataset but first lets take a look at the review_date (`$15`), the review_headline (`$13`) and the star_rating (`$8`) of our Hunger Games reviews.

``` bash
$ awk -F '\t' '$4~0439023483{ print $15 "\t" $13 "\t" $8}' bookreviews.tsv | head 
```
``` ini
2012-05-02      Great story, great characters   5
2012-05-02      Great!  5
2012-05-02      " A Repeat Of The First Book"   2
2012-05-02      Great book, appropriate and satisfying ending   5
2012-05-02      Catching Fire   5
2012-05-02      Psychological Manipulation Inappropriate for Youths.    1
2012-05-02      A Ray of Light  5
2012-05-02      Easy and Entertaining Read      4
2012-05-02      The Hunger GAmes        5
2012-05-02      the game of life [no spoilers]  4
```

Look at those star ratings. Yes, the book is polarizing but more importantly, the layout of my text table look horrible: the width of the width of the review titles are breaking the layout.

To fix this I need to switch from using `print` to using `printf`.

### AWK Printf

`printf` works like it does in the C and uses a format string and then a list of values. 

So my `print $15 "\t" $13 "\t" $8` 
becomes `printf "%s \t %s \t %s, $15, $13, $8`. 

From there I can add right padding and fix my layout by changing `%s` to `%-Ns` where `N` is my desired column width. 

Putting it all together and we get: 

``` bash
$ awk -F '\t' '$4~0439023483{ printf "%s \t %-55s \t %s \n", $15, $13, $8}' bookreviews.tsv| head 
```
``` ini
2012-05-02       Great story, great characters                                   5 
2012-05-02       Great!                                                          5 
2012-05-02       " A Repeat Of The First Book"                                   2 
2012-05-02       Great book, appropriate and satisfying ending                   5 
2012-05-02       Catching Fire                                                   5 
2012-05-02       Psychological Manipulation Inappropriate for Youths.            1 
2012-05-02       A Ray of Light                                                  5 
2012-05-02       Easy and Entertaining Read                                      4 
2012-05-02       The Hunger GAmes                                                5 
2012-05-02       the game of life [no spoilers]                                  4 
```


## AWK END Actions

I want to calculate the average rating for book reviews in this data set. To do some I need to use a variable. Variables are easy in AWK. No declaration, just use them.

I can add up and print out a running total of review_stars (`$8`) like this
``` bash
$  awk -F '\t' '{ total = total + $8; print total }' bookreviews.tsv| head 
```
``` ini
0
5
10
...
```
And to turn this into an average, I can use `NR` to get the total amount of records and `END` to run an action at the end of the processing.

``` bash
 $ awk -F '\t' '
    { total = total + $8 }
END { print "Average book review:", total/NR, "stars" }
' bookreviews.tsv | head 
```
``` ini
Average book review is 4.24361 stars
```
### Fun AWK one-liners

Before we leave the world of one liners behind here are some fun ones.
....
...


## AWK Scripting Examples
In my mind, once an AWK program spans multiple lines its time to consider putting it into a file. We've now crossed over from one-liners to scripting and with AWK the transition is really smooth.

``` bash
$ cat average
```
``` ini
exec awk -F '\t' '
{ total = total + $8 }
END { print "Average book review is", total/NR, "stars" } 
' $1
```
``` bash
$ average bookreviews.tsv
```
``` ini
Average book review is 4.2862 stars
```

### Bringing It All Together
With the things I've covered so far, you should be able to do a lot with AWK. For example, I can get average review for hunger games:

``` bash
exec awk -F '\t' '
$4 == "0439023483"{ title=$6; count = count + 1; total = total + $8 }
END { print "The Average book review for", title, "is", total/count, "stars" }  
' $1
```

I can do this over multiple lines, so it reads a bit better:
``` awk
exec awk -F '\t' '
$4 == "0439023483"{ 
  title=$6
  count = count + 1; 
  total = total + $8 
}
END { 
  printf "Book: %-5s\n", title
  printf "Average Rating: %.2f\n", total/count 
  }  
' $1
```
Next:
- add a header
- if else
- gsub
- dictionary
- passing in parameters
- accessing the match 
