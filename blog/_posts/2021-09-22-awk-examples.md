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

<p>
One of the comments I heard around the JQ article was the JQ was so complex just like awk. I have a confession to make - I don't know how to use awk. I hear it mentioned sometimes and occasionally I see a cool blog post where someone uses awk to takes a giant spark task or big data workflow and reduce its complexity to a one-line in awk.
</p>

So in this article I will myself, and you, the basics of Awk.

## What Is Awk

Awk is a record processing tool written by Aho, Kernighan, and Weinberger in 1977. It's name is an acronym of their names. 

They created it following the success of the line processing tools `sed` and `grep`. Awk was originally an experiment into how text processing tools could be extended to deal with numbers. If grep lets you search for lines, and sed lets you do replacements in lines then awk was designed to let you do calculations on lines. It will be clear what that means once I take us through some examples. 

## How to Install GAWK

> The biggest reason to learn AWK, IMO, is that it's on pretty much every single linux distribution. You might not have perl or python. You WILL have AWK. Only the most minimal of minimal linux systems will exclude it. Even busybox includes awk. That's how essential it's viewed.
>
> [cogman10](https://news.ycombinator.com/item?id=28447825)

Awk is part of the Portable Operating System Interface (POSIX). This means its already on your MacBook and your Linux server. There are several versions of Awk and for the basics whatever Awk you have will do. 

If you can run this, you can do the rest of this tutorial:

``` bash
$ awk --version
``` 
```
  GNU Awk 5.1.0, API: 3.0 (GNU MPFR 4.1.0, GNU MP 6.2.1)
  Copyright (C) 1989, 1991-2020 Free Software Foundation.
```

If you are doing something more involved with Awk, take the time to instal  GNU Awk (`gawk`). I did this using homebrew (`brew install gawk`). Windows users can use chocolatey (`choco install gawk`). It is already on your Linux distribution. 

## Awk Print

By default Awk expects to receive its input on standard in and output its results to standard out. The simplest thing you can do in Awk is print a line of input.

``` bash
$ echo "one two three" | awk '{ print }'
one two three
```
Note the braces. This syntax will start to make sense after you see a couple examples.

We can selectively choose columns (which Awk calls fields):
``` bash
$ echo "one two three" | awk '{ print $1 }'
one
$ echo "one two three" | awk '{ print $2 }'
two
$ echo "one two three" | awk '{ print $3 }'
three
```
You may have been expecting the first column to be `$0` and not `$1` but `$0` is something different:
``` bash
$ echo "one two three" | awk '{ print $0 }'
``` 
``` ini
one two three
```
It is the entire line! Incidentally Awk refers to each line as a record and each column as a field. 

I can do this across multiple lines:
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

And I can print more than one column:

``` bash
$ echo "
 one two three
 four five six" \
| awk '{ print $1, $2 }'
```
``` ini
one two
four five
```

Awk also includes `$NF` for access the last column:

``` bash
$ echo "
 one two three
 four five six" \
| awk '{ print $NF }'
```
``` ini
two
five
```


<div class="notice--big--primary">

<!-- markdownlint-disable MD036 -->
**What I've learned: Awk Field Variables**

Awk creates a variable for each field (row) in a record (line) (`$1`, `$2` ... `$NF`). `$0` refers to the whole record.

You can print out fields like this:
``` bash
awk '{ print $1, $2, $7 }'
```
</div>

## AWK Sample Data

> awk exists so that guy can rag on any data processing tool made after the year 1990 to get votes from people who can’t really remember any of its syntax
>
> “I processed 500 Petabytes with awk on a single server once I don’t see why this is needed”
>
> [BufferUnderpants on /r/programming](https://www.reddit.com/r/programming/comments/pank18/comment/ha6hzg0/?utm_source=reddit&utm_medium=web2x&context=3)

To move beyond simple printing, I need some sample data. I'm going to use the book portion of the [amazon product reviews dataset](https://s3.amazonaws.com/amazon-reviews-pds/tsv/index.txt).

> This dataset contains product reviews and metadata from Amazon, including 142.8 million reviews spanning May 1996 - July 2014.
>
> Amazon Review Data Set

You can grab the book portion of it like this:
``` bash
$ curl https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Books_v1_00.tsv.gz | /
  gunzip -c >> / 
  bookreviews.tsv
```
Repeat this for each of the three book files (`v1_00`, `v1_01`, `v1_02`) if you want to follow along with the full dataset.

<div class="notice--warning">

**❗ Disk Space Warning**

The above file is over 6 gigs unzipped. If you grab all three you will be up to 15 gigs. If you don't have much space you can play along by just grabbing the first ten thousand rows of the first file. 

``` bash
$ curl https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Books_v1_00.tsv.gz \
  | gunzip -c \
  | head -n 10000 \
  > bookreviews.tsv
```
</div>

## The Book Data

Once you've grabbed that data, you should have Amazon book review data that looks like this:

``` ini
marketplace	customer_id	review_id	product_id	product_parent	product_title	product_category	star_rating	helpful_votes	total_votes	vine	verified_purchase	review_headline	review_body	review_date
US	22480053	R28HBXXO1UEVJT	0843952016	34858117	The Rising	Books	5	0	0	N	N	Great Twist on Zombie Mythos	I've known about this one for a long time, but just finally got around to reading it for the first time. I enjoyed it a lot!  What I liked the most was how it took a tired premise and breathed new life into it by creating an entirely new twist on the zombie mythos. A definite must read!	2012-05-03
```

Each row in this file represents the record of one book review. The row is laid out like this:
``` ini
DATA COLUMNS:
01  marketplace       - 2 letter country code of the marketplace where the review was written.
02  customer_id       - Random identifier that can be used to aggregate reviews written by a single author.
03  review_id         - The unique ID of the review.
04  product_id        - The unique Product ID the review pertains to. 
05  product_parent    - Random identifier that can be used to aggregate reviews for the same product.
06  product_title     - Title of the product.
07  product_category  - Broad product category that can be used to group reviews 
08  star_rating       - The 1-5 star rating of the review.
09  helpful_votes     - Number of helpful votes.
10  total_votes       - Number of total votes the review received.
11  vine              - Review was written as part of the Vine program.
12  verified_purchase - The review is on a verified purchase.
13  review_headline   - The title of the review.
14  review_body       - The review text.
15  review_date       - The date the review was written.
```

## Printing Book Data

I can now test out my field printing skills on a bigger file. I can start by printing fields that I care about, like the marketplace:
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
However, when I try to print out the title things do not go well:
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

To fix this, I need to configure my field separators.

## Field Separators


By default, Awk assumes that the fields in a record are space delimited. We can change the field separator to use tabs using the `awk -F` option:

``` bash
$ awk -F '\t' '{ print $6 }' bookreviews.tsv | head 
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

<div class="notice--big--primary">

**What I've learned: Awk Field Separators**

Awk assumes that the fields in a record are space delimited.

You can change this using the `-F` option like this
``` bash
awk -F '\t' '{ print $6 }'
```
</div>


I can also work backwards from the last position forward by subtracting from `NF`.
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

### Awk Pattern Match With Regular Expressions

Everything I've done so far has applied to every line in our file but the real power of Awk comes from pattern matching. And you can give Awk a pattern to match each line on like this:
``` bash
$ echo "aa
        bb
        cc" | awk '/bb/'
bb
```
This lets you use Awk like you would use `grep`. You can combine this with the field access and printing we've done so far:
``` bash
$ echo "aa 10
        bb 20
        cc 30" | awk '/bb/{ print $2 }'
20
```

Using this knowledge, I can easily grab reviews by book title and print the book title(`$6`) and review score(`$8`). 

The reviews I'm going to focus in on today, are for the book 'The Hunger Games'. I'm choosing it because: its a series, it's likely to have many reviews, and I recall that I liked the movie and am wondering if I should read the series.  

``` bash
$ awk -F '\t' '/Hunger Games/{ print $6, $8  }' bookreviews.tsv | head
```
``` ini
The Hunger Games (Book 1) 5
The Hunger Games Trilogy Boxed Set 5
The Hunger Games Trilogy: The Hunger Games / Catching Fire / Mockingjay 5
Catching Fire |Hunger Games|2 4
The Hunger Games (Book 1) 5
Catching Fire |Hunger Games|2 5
The Hunger Games Trilogy: The Hunger Games / Catching Fire / Mockingjay 5
Blackout 3
The Hunger Games Trilogy: The Hunger Games / Catching Fire / Mockingjay 4
Tabula Rasa 3
```
I should be able to do some interesting data analysis on these reviews, but first there is a problem. I'm clearly getting reviews from more than one book here. `/Hunger Games/` is matching anywhere in the line and I'm getting all kinds of Hunger Game books. 

I'm even getting books that mention "Hunger Games" in the review text:

``` bash
$ awk -F '\t' '/Hunger Games/{ print $6 }' bookreviews.tsv | sort | uniq    
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

I can fix this by using the `product_id` field to pattern match on:
``` bash
awk -F '\t' '$4 == "0439023483"{ print $6 }' bookreviews.tsv | sort |  uniq 
The Hunger Games (The Hunger Games, Book 1)
```

I'd like to calculate the average review score for hunger games in my dataset but first lets take a look at the review_date (`$15`), the review_headline (`$13`) and the star_rating (`$8`) of our Hunger Games reviews, to get a feel for the data:

``` bash
$ awk -F '\t' '$4 == "0439023483{ print $15 "\t" $13 "\t" $8}' bookreviews.tsv | head 
```
``` ini
015-08-19      Five Stars      5
2015-08-17      Five Stars      5
2015-07-23      Great read      5
2015-07-05      Awesome 5
2015-06-28      Epic start to an epic series    5
2015-06-21      Five Stars      5
2015-04-19      Five Stars      5
2015-04-12      i lile the book 3
2015-03-28      What a Great Read, i could not out it down   5
2015-03-28      Five Stars      5
```

Look at those star ratings. Yes, the book is getting a lot of 5 star reviews but more importantly, the layout of my text table look horrible: the width of the review titles are breaking the layout.

To fix this I need to switch from using `print` to using `printf`.

<div class="notice--big--primary">

**What I've learned: Awk Pattern Matching**

I've learned that an awk action, like `{ print $4}`, can be preceded by a pattern, like `/regex/`. Without the pattern, the action runs on all lines.

You can use a plain regular expression for the pattern. In which case it matches anywhere in the line, like `grep`:
``` bash 
$ awk '/hello/{ print "This line contains hello", $0}'
```
Or you can match within a specific field:
``` bash
$ awk '$4~/hello/{ print "This field contains hello", $4}'
```
Or you can exact match a field:
``` bash
$ awk '$4 == "hello"{ print "This field is hello:", $4}'
```
</div>

### AWK Printf

`printf` works like it does in the C and uses a format string and then a list of values. 

So my `print $15 "\t" $13 "\t" $8` 
becomes `printf "%s \t %s \t %s, $15, $13, $8`. 

From there I can add right padding and fix my layout by changing `%s` to `%-Ns` where `N` is my desired column width:


``` bash
$ awk -F '\t' '$4 == "0439023483"{ printf "%s \t %-20s \t %s \n", $15, $13, $8}' bookreviews.tsv| head 
```
``` ini
2015-08-19       Five Stars              5 
2015-08-17       Five Stars              5 
2015-07-23       Great read              5 
2015-07-05       Awesome                 5 
2015-06-28       Epic start to an epic series    5 
2015-06-21       Five Stars              5 
2015-04-19       Five Stars              5 
2015-04-12       i lile the book         3 
2015-03-28       What a Great Read, i could not out it down   5 
2015-03-28       Five Stars              5 
```
This is pretty close to what I'd like. Some of the titles are just to long. I can shorten them up with `substr($13,1,20)`.

Putting it all together and I get:

``` bash
$ awk -F '\t' '$4 == "0439023483"{ printf "%s \t %-20s \t %s \n", $15, substr($13,1,20), $8}' bookreviews.tsv| head
```
``` ini
2015-08-19       Five Stars              5 
2015-08-17       Five Stars              5 
2015-07-23       Great read              5 
2015-07-05       Awesome                 5 
2015-06-28       Epic start to an epi    5 
2015-06-21       Five Stars              5 
2015-04-19       Five Stars              5 
2015-04-12       i lile the book         3 
2015-03-28       What a Great Read, i    5 
2015-03-28       Five Stars              5 
```

Alright, I think at this point I'm ready to move on to doing some calculations. 


<div class="notice--big--primary">

**What I've learned: Printf and Built-ins**

If you need print out a table, Awk lets you use `printf` and built-ins like `substr` to format your output.

It ends up looking something like this:
``` bash
$ awk '{ printf "%s \t %-5s", $1, substr($2,1,5)}'
```

`printf` works much like c's `printf` and for the built-ins included head to an Awk reference document.
</div>

## Awk `END` Actions

I want to calculate the average rating for book reviews in this data set. To do that I need to use a variable. Variables are easy in Awk. No declaration, just use them.

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
`BEGIN` also exists and runs an action at the beginning before any lines have been processed.

``` bash
 $ awk -F '\t' '
BEGIN { print "Calculating Average ..." } 
      { total = total + $8 }
END   { print "Average book review:", total/NR, "stars" }
' bookreviews.tsv 
```
``` ini
Calculating Average ...
Average book review is 4.24361 stars
```
<div class="notice--big--primary">

**What I've learned: Awk's `BEGIN`, `END` and Variables**

Awk provides two special patterns, `BEGIN` and `END`. The actions in these blocks are run before any lines are processed and after all the lines have be processed. This is how you would initialize data, print headers and footer or do any start up or tear down stuff in Awk.

It ends up looking like this:
``` bash
$ awk '
BEGIN { print "start up" }
      { print "line match" }
END   { print "tear down" }'
```

You can also easily use variables in Awk. No declaration is needed.
``` bash
awk -F '{ total = total + $8 }'
```

</div>

### Fun Awk one-liners

Before we leave the world of one liners behind here are some I've used before. Most of the times I've had to reach for Awk involves a command line tools returning a whitespace delimited table that I'd like to customize or further process.

Like printing files with a human readable size:
``` bash
$ ls -lh | awk '{ print $5,"\t", $9 }'  
```
``` ini
7.8M     The_AWK_Programming_Language.pdf
6.2G     bookreviews.tsv
```

Or getting the containerID of running docker containers:

``` awk
docker ps -a |  awk '{ print $1 }'
```
``` ini
CONTAINER
08488f220f76
3b7fc673649f
```
We can combine those with a regex to focus in on a line we care about. Here I stop postgres, regardless of its name.
```
docker stop "$(docker ps -a |  awk '/postgres/{ print $1 }')"
```
And so on. You get the idea.

## AWK Scripting Examples

> If you pick your constraints you can make a particular envelope of uses easy and ones you don't care about hard.
> AWK's choice to be a per line processor, with optional sections for processing before all lines and after all lines is self-limiting but it defines a useful envelope of use.
>
> [Michael Feathers](https://news.ycombinator.com/item?id=13455678)

In my mind, once an AWK program spans multiple lines its time to consider putting it into a file. 

<div class="notice--info">
**Side Note: Why Awk Scripting**

Once we move beyond one-liners a natural question is *why*. As in 'Why not use python? Isn't it good at this type of thing?' I have a couple answers for that.

First, Awk is great for writing programs that are, at their core, a glorified for loop over some input. If that is what you are doing, and the amount of control flow is limited, using Awk will be more concise than using python. 

Second, if you need to rewrite your Awk program in something else at some point so be it. It's not going to be more than 100 lines of code and the translation process will be straight forward. 

Third, why not? Learning a new tool can be fun. 
</div>

We've now crossed over from one-liners into AWK scripting. With AWK, this the transition is smooth. We can embed Awk into a bash script:

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

Or we can use a shebang (`#!`):
``` bash
$ cat average.awk
```
``` awk
#!/usr/bin/env -S gawk -f

BEGIN { FS = "\t" }
{ total = total + $8 }
END { print "Average book $6 review is", total/NR, "stars" } 
```
And run it like this
```
$ ./average.awk bookreviews.tsv
```

Or you can also pass it to awk directly using `-f`:
```
$ awk -f average.awk bookreviews.tsv
```

<div class="notice--info">
**Side Note: BEGIN FS**

If you do use a shebang or pass to Awk directly then it's easiest to set the file separator using `FS = "\t"` in the `BEGIN` action.
``` awk
BEGIN { FS = "\t" }
```
</div>

### Awk Average Example

At this point, I should be ready to start calculating review scores for The Hunger Games :

``` bash
exec awk -F '\t' '
$4 == "0439023483"{ title=$6; count = count + 1; total = total + $8 }
END { print "The Average book review for", title, "is", total/count, "stars" }  
' $1
```

Now that I'm in a file, I can format this out a bit better so its easier to read:
``` awk
$4 == "0439023483" { 
  title=$6
  count = count + 1; 
  total = total + $8 
}
END { 
  printf "Book: %-5s\n", title
  printf "Average Rating: %.2f\n", total/count 
}  
```
Either way, I get this output:
``` ini
Book: The Hunger Games (The Hunger Games, Book 1)
Average Rating: 4.67%       
```

<div class="notice--big--primary">

**What I've learned: Calling Awk from a file**

Once you are beyond a single line, it makes sense to put your Awk script into a file. 

You can then call you program using using the `-f`option

``` bash
awk -f file.awk input
```

Using a shebang :
``` bash
#!/usr/bin/env -S gawk -f
```
or by using a bash `exec` command:
``` bash
exec awk -F '\t' 'print $0' $1
```
</div>

### Awk Arrays
The next thing I'd like to do is compare the reviews across the hunger game trilogy. I'd like to know if the series stays strong, or its a single great book that was stretched out into a trilogy. 

Which book was the best and which was the worst? If the reviews decline quickly then that is not a good sign. Let's find out.

If I were going to calculate the averages in Python, I would loop over the list of reviews and use a dictionary to track the total stars and total reviews for each.

In Awk I can do the same:
``` awk
BEGIN { FS = "\t" }
$6~/\(The Hunger Games(, Book 1)?\)$/ { 
  title[$6]=$6
  count[$6]= count[$6] + 1
  total[$6]= total[$6] + $8
}
END { 
    for (i in count) {
        printf "---------------------------------------\n"
        printf "%s\n", title[i]
        printf "---------------------------------------\n"
        printf "Ave: %.2f\t Count: %s \n\n", total[i]/count[i], count[i]  
    }
}
```
``` bash
$ awk -f hungergames.awk bookreviews.tsv
```
``` ini
---------------------------------------
The Hunger Games (The Hunger Games, Book 1)
---------------------------------------
Ave: 4.55        Count: 1497 

---------------------------------------
Mockingjay (The Hunger Games)
---------------------------------------
Ave: 3.77        Count: 3801 

---------------------------------------
Catching Fire (The Hunger Games)
---------------------------------------
Ave: 4.52        Count: 2205 

---------------------------------------

```
And look at that, the first book in the series was the most popular. And the last book, Mocking Jay was much less popular. That isn't a good sign.

<!-- <div class="notice--info">
**Side Note: RegEx**

There are many editions of the hunger games books. This regex from above `\(The Hunger Games(, Book 1)?\)$/` let me narrow the results down to the most popular edition of the three books. 
</div> -->

Let me look at another trilogy to see if this gradual decrease in rankings is common or Hunger Games specific:

``` awk
BEGIN { FS = "\t" }
$6~/\(The Lord of the Rings, Book .\)$/ {  # <-- changed this line
  title[$6]=$6
  count[$6]= count[$6] + 1
  total[$6]= total[$6] + $8
}
END { 
    for (i in title) {
        printf "---------------------------------------\n"
        printf "%s\n", title[i]
        printf "---------------------------------------\n"
        printf "Ave: %.2f\t Count: %s \n\n", total[i]/count[i], count[i]  
    }
}
```
``` ini
---------------------------------------
The Return of the King (The Lord of the Rings, Book 3)
---------------------------------------
Ave: 4.79        Count: 38 

---------------------------------------
The Two Towers (The Lord of the Rings, Book 2)
---------------------------------------
Ave: 4.64        Count: 56 

---------------------------------------
The Fellowship of the Ring (The Lord of the Rings, Book 1)
---------------------------------------
Ave: 4.60        Count: 93  
```

Lord of the Rings has a different pattern. The books are all in a pretty tight range. The number of reviews is also much smaller so it's hard to say for sure that "The Return Of the King" is the best book but it certainly looks that way. 

<div class="notice--big--primary">

**What I've learned: Awk Associative Arrays**

Awk has associative arrays built it. These use a string as the index and function very much like Python dictionaries. 

``` awk
arr["key1"] = "one"
arr["key2"] = "two"
arr["key3"] = "three"
```
There is also a for loop construct for iterating over them:
``` awk
for (i in arr){
    print $i, arr[i]
}
```
``` bash
key1 one
key2 two
key3 three
```

Not bad for a langauge written in 1977!
</div>

### AWK If Else

The thing I hate about amazon reviews is that every book review I look at is somehow rated between 3.5 and 4.5 stars. Let's rescale things in terms of the average. Maybe if we normalize the reviews it will be easier to judge how good or bad 3.77 for MockingJay is. 

First I need to track the global average like this
``` awk
{
    # Global Average
    g_count = g_count + 1
    g_total = g_total + $8 
}
```
Then all I need to do is add some if statements to my `END` pattern:
```
END { 
    g_score = g_total/g_count 
    for (i in count) {
        score = total[i]/count[i]
        printf "%-30s\t", substr(title[i],1,30)
        if (score - g_score > .5)
            printf "👍👍👍" 
        else if (score - g_score > .25)
            printf "👍👍" 
        else if (score - g_score > 0)
            printf "👍" 
        else if (g_score - score  > 1)
            printf "👎👎👎" 
        else if (g_score - score  > .5)
            printf "👎👎" 
        else if (g_score - score  > 0)
            printf "👎"
        printf "\n"
    }
}
```
The values for partitioning are just a guess, but it make it easier for me to understand the rankings:
```
The Hunger Games (The Hunger G  👍
Catching Fire: The Official Il  👍👍👍
Mockingjay (The Hunger Games)   👎👎

The Two Towers (The Lord of th  👍👍
The Fellowship of the Ring (Th  👍👍
The Return of the King (The Lo  👍👍👍
```

It looks like MockingJay, at least on Amazon, in this dataset, was not well received. 

We can easily modify this to give let us query this adhoc:
``` awk
exec gawk -F '\t' '
{
    # Global Average
    g_count = g_count + 1
    g_total = g_total + $8 
    PROCINFO["sorted_in"] = "@val_num_asc"
}
$6~/^.*'+"$1"+'.*$/ { # <-- Take match as input
  title[$6]=$6
  count[$6]= count[$6] + 1
  total[$6]= total[$6] + $8
}
END { 
    PROCINFO["sorted_in"] = "@val_num_desc"
    g_score = g_total/g_count 
    for (i in count) {
        score = total[i]/count[i]
        printf "%-50s\t", substr(title[i],1,50)
        if (score - g_score > .4)
            printf "👍👍👍" 
        else if (score - g_score > .25)
            printf "👍👍" 
        else if (score - g_score > 0)
            printf "👍" 
        else if (g_score - score  > 1)
            printf "👎👎👎" 
        else if (g_score - score  > .5)
            printf "👎👎" 
        else if (g_score - score  > 0)
            printf "👎"
        printf "\n"
    }
}
' bookreviews.tsv | head -n 1
```

And then run it like this:
```
$ ./average "Left Hand of Darkness"
The Left Hand of Darkness (Ace Science Fiction)         👎
./average "Neuromancer"          
Neuromancer                                             👎👎
./average "The Lifecycle of Software Objects"
The Lifecycle of Software Objects                       👎
```
These are all great books so I'm starting to question the taste of Amazon reviewers. 

There is one more thing I'd like to test though: how do the most popular books rate? Maybe popular books get lots of reviews and that pushes them below the overall average?
<div class="notice--big--primary">

**What I've learned: Awk If Else**

Awk has branching using `if` and `else` statments. It works exactly like you might expect it to:

``` bash
echo "1\n 2\n 3\n 4\n 5\n 6" | awk '{
        if (NR % 2) 
            print "odd"
        else
            print $0
        }'
```
``` ini 
odd
2
odd
4
odd
6
```
</div>

## Awk Sort by Values

Awk ( specifically gawk) allows you easily configure your iteration order using a magic variable called `PROCINFO["sorted_in"]`. This means that if I change our program to sort by value and drop the filtering then I will be able to see the top reviewed books:

``` awk
exec gawk -F '\t' '
{
    # Global Average
    g_count = g_count + 1
    g_total = g_total + $8 
    title[$6]=$6
    count[$6]= count[$6] + 1
    total[$6]= total[$6] + $8
}
END { 
    PROCINFO["sorted_in"] = "@val_num_desc" # <-- Print in value order
    g_score = g_total/g_count 
    for (i in count) {
        score = total[i]/count[i]
        printf "%-50s\t", substr(title[i],1,50)
        if (score - g_score > .4)
            printf "👍👍👍" 
        else if (score - g_score > .25)
            printf "👍👍" 
        else if (score - g_score > 0)
            printf "👍" 
        else if (g_score - score  > 1)
            printf "👎👎👎" 
        else if (g_score - score  > .5)
            printf "👎👎" 
        else if (g_score - score  > 0)
            printf "👎"
        printf "\n"
    }
}
' bookreviews.tsv 

```
Running it:
``` bash
$ ./top_books | head
```
```
667539744       Harry Potter And The Sorcerer's Stone                 👍👍
600633062       Fifty Shades of Grey                                  👎👎
245449872       The Hunger Games (The Hunger Games, Book 1)           👍
669379389       The Hobbit                                            👍
745538746       Twilight                                              👎
340399706       Jesus Calling: Enjoying Peace in His Presence         👍👍👍
259796199       Unbroken: A World War II Story of Survival, Resili    👍👍👍
736723180       The Shack: Where Tragedy Confronts Eternity           👎
941986263       Divergent                                             👍
93816562        Gone Girl                                             👎👎
```

It looks like about half (6 /10) of the most reviewed books were more popular than average. This tell me that the low reviews on MockingJay can't be blamed on its popularity.  So, I think I'll have to take a pass on the series or at the very least that book.

### Conclusion
> A good programmer uses the most powerful tool to do a job. A great programmer uses the least powerful tool that does the job." I believe this, and I always try to find the combination of simple and lightweight tools which does the job at hand correctly.
>
> [vyuh](https://news.ycombinator.com/item?id=28445692
https://news.ycombinator.com/item?id=28445692)

Awk just keeps going. It has more built-in variables and built-in functions. It has range patterns and substition rules you can use to modify content and more.

If you want to learn more Awk, [The Awk Programming Language]() is the definitive book. It covers the language in depth but also covers how to biuld a small programming language in Awk, how to build a database in Awk and some other fun projects. It's really an introduction to building things with scripting langauges.

I hope this introduction gave you enough AWK for 90% of your use-cases though. If you come up with any clever Awk tricks yourself or if you have strong opinions on whether I should read the Hunger Games Trilogy, please reach out me.
