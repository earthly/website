---
title: "Understanding AWK"
categories:
  - Tutorials
toc: true
sidebar:
  nav: "bash"
author: Adam
internal-links:
 - awk
excerpt: |
    Learn the basics of Awk, a powerful text processing tool, in this informative article. Discover how to use Awk to manipulate and analyze data, calculate averages, and even score books based on reviews. Whether you're a beginner or an experienced programmer, this article will help you unlock the potential of Awk.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about understanding AWK, a powerful text processing tool used for manipulating and analyzing data. Earthly is a powerful build tool that can be used in conjunction with Bash scripting to streamline and automate the build process. [Check us out](/).**

<iframe width="560" height="315" src="https://www.youtube.com/embed/yJek26lyXZ0" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

## Background

I have a confession to make: I don't know how to use Awk. Or at least I didn't know how to use it before I started writing this article. I would hear people mention Awk and how often they used it, and I was pretty certain I was missing out on some minor superpower.

Like this little off hand comment by [Bryan Cantrill](https://www.youtube.com/watch?v=2wZ1pCpJUIM):

> I write three or four Awk programs a day. And these are one-liners. These super quick programs.

It turns out Awk is pretty simple. It has only a couple of conventions and only a small amount of syntax. As a result, it's straightforward to learn, and once you understand it, it will come in handy more often than you'd think.

So in this article, I will teach myself, and you, the basics of Awk. **If you read through the article and maybe even try an example or two, you should have no problem writing Awk scripts by the end of it.** And you probably don't even need to install anything because Awk is everywhere.

### The Plan

I will be using Awk to look at book reviews and pick my next book to read. I will start with short Awk one-liners and build towards a simple 33 line program that ranks books by the 19 million reviews on Amazon.com.

## What Is Awk

Awk is a record processing tool written by Aho, Kernighan, and Weinberger in 1977. Its name is an acronym of their names.

They created it following the success of the line processing tools `sed` and `grep`. Awk was initially an experiment by the authors into whether text processing tools could be extended to deal with numbers. If grep lets you search for lines, and sed lets you do replacements in lines then awk was designed to let you do calculations on lines. It will be clear what that means once I take us through some examples.

### How To Install `gawk`

> The biggest reason to learn Awk is that it's on pretty much every single linux distribution. You might not have perl or Python. You *will* have Awk. Only the most minimal of minimal linux systems will exclude it. Even busybox includes awk. That's how essential it's viewed.
>
> [cogman10](https://news.ycombinator.com/item?id=28447825)

Awk is part of the Portable Operating System Interface (POSIX). This means it's already on your MacBook and your Linux server. There are several versions of Awk, but for the basics, whatever Awk you have will do.

If you can run this, you can do the rest of this tutorial:

~~~{.bash caption=">_"}
$ awk --version
~~~

~~~{.bash .merge-code}
  GNU Awk 5.1.0, API: 3.0 (GNU MPFR 4.1.0, GNU MP 6.2.1)
  Copyright (C) 1989, 1991-2020 Free Software Foundation.
~~~

If you are doing something more involved with Awk, take the time to install GNU Awk (`gawk`). I did this using Homebrew (`brew install gawk`). Windows users can get gawk using chocolatey (`choco install gawk`). If you are on Linux, you already have it.

## Awk Print

By default, Awk expects to receive its input on standard in and output its results to standard out. Thus, the simplest thing you can do in Awk is print a line of input.

~~~{.bash caption=">_"}
$ echo "one two three" | awk '{ print }'
one two three
~~~

Note the braces. This syntax will start to make sense after you see a couple of examples.

You can selectively choose columns (which Awk calls fields):

~~~{.bash caption=">_"}
$ echo "one two three" | awk '{ print $1 }'
one
~~~

~~~{.bash .merge-code}
$ echo "one two three" | awk '{ print $2 }'
two
~~~

~~~{.bash .merge-code}
$ echo "one two three" | awk '{ print $3 }'
three
~~~

You may have been expecting the first column to be `$0` and not `$1`, but `$0` is something different:

~~~{.bash caption=">_"}
$ echo "one two three" | awk '{ print $0 }'
~~~

~~~{.bash .merge-code }
one two three
~~~

It is the entire line! Incidentally, Awk refers to each line as a record and each column as a field.

I can do this across multiple lines:

~~~{.bash caption=">_"}
$ echo "
 one two three
 four five six" \
 | awk '{ print $1 }'
~~~

~~~{.bash .merge-code}
one
four
~~~

And I can print more than one column:

~~~{.bash caption=">_"}
$ echo "
 one two three
 four five six" \
| awk '{ print $1, $2 }'
~~~

~~~{.bash .merge-code}
one two
four five
~~~

Awk also includes `$NF` for accessing the last column:

~~~{.bash caption=">_"}
$ echo "
 one two three
 four five six" \
| awk '{ print $NF }'
~~~

~~~{.bash .merge-code}
three
six
~~~

<div class="notice--big--primary">

### What I've learned: Awk Field Variables

Awk creates a variable for each field (column) in a record (line) (`$1`, `$2` ... `$NF`). `$0` refers to the whole record.

You can print out fields like this:

~~~{.bash caption=">_"}
$ awk '{ print $1, $2, $7 }'
~~~

</div>

## Awk Sample Data

To move beyond simple printing, I need some sample data. I will use the book portion of the [amazon product reviews dataset](https://s3.amazonaws.com/amazon-reviews-pds/tsv/index.txt) for the rest of this tutorial.

> This dataset contains product reviews and metadata from Amazon, including 142.8 million reviews spanning May 1996 - July 2014.
>
> Amazon Review Data Set

You can grab the book portion of it like this:

~~~{.bash caption=">_"}
$ curl https://s3.amazonaws.com/amazon-reviews-pds/tsv/ ↩
amazon_reviews_us_Books_v1_00.tsv.gz | /
  gunzip -c >> / 
  bookreviews.tsv
~~~

If you want to follow along with the entire dataset, repeat this for each of the three book files (`v1_00`, `v1_01`, `v1_02`).

<div class="notice--warning">

### ❗ Disk Space Warning

The above file is over six gigs unzipped. If you grab all three, you will be up to fifteen gigs of disk space. If you don't have much space, you can play along by grabbing the first ten thousand rows of the first file:

~~~{.bash caption=">_"}
$ curl https://s3.amazonaws.com/amazon-reviews-pds/tsv/ ↩
amazon_reviews_us_Books_v1_00.tsv.gz \
  | gunzip -c \
  | head -n 10000 \
  > bookreviews.tsv
~~~

</div>

### The Book Data

Once you've grabbed that data, you should have Amazon book review data that looks like this:

~~~{.bash }
marketplace customer_id review_id product_id product_parent product_title product_category star_rating helpful_votes total_votes vine verified_purchase review_headline review_body review_date
US 22480053 R28HBXXO1UEVJT 0843952016 34858117 The Rising Books 5 0 0 N N Great Twist on Zombie Mythos I've known about this one for a long time, but just finally got around to reading it for the first time. I enjoyed it a lot!  What I liked the most was how it took a tired premise and breathed new life into it by creating an entirely new twist on the zombie mythos. A definite must read! 2012-05-03
~~~

Each row in this file represents the record of one book review. Amazon lays out the fields like this:

~~~{.bash caption="Data Format"}
DATA COLUMNS:
01  marketplace       - 2 letter country code of the marketplace where the ↩
 review was written.
02  customer_id       - Random identifier that can be used to aggregate reviews↩
 written by a single author.
03  review_id         - The unique ID of the review.
04  product_id        - The unique Product ID the review pertains to. 
05  product_parent    - Random identifier that can be used to aggregate ↩ 
reviews for the same product.
06  product_title     - Title of the product.
07  product_category  - Broad product category that can be used to group ↩
reviews 
08  star_rating       - The 1-5 star rating of the review.
09  helpful_votes     - Number of helpful votes.
10  total_votes       - Number of total votes the review received.
11  vine              - Review was written as part of the Vine program.
12  verified_purchase - The review is on a verified purchase.
13  review_headline   - The title of the review.
14  review_body       - The review text.
15  review_date       - The date the review was written.
~~~

### Printing Book Data

I can now test out my field printing skills on a bigger file. I can start by printing fields that I care about, like the marketplace:

~~~{.bash caption=">_"}
$ awk '{ print $1 }' bookreviews.tsv | head 
~~~

~~~{.bash .merge-code}
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
~~~

Or the customer_id:

~~~{.bash caption=">_"}
$ awk '{ print $2 }' bookreviews.tsv | head 
~~~

~~~{.bash .merge-code}
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
~~~

However, when I try to print out the title, things do not go well:

~~~{.bash caption=">_"}
$ awk '{ print $6 }' bookreviews.tsv | head 
~~~

~~~{.bash .merge-code}
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
~~~

To fix this, I need to configure my field separators.

## Field Separators

By default, Awk assumes that the fields in a record are whitespace delimited[^1]. I can change the field separator to use tabs using the `awk -F` option:

~~~{.bash caption=">_"}
$ awk -F '\t' '{ print $6 }' bookreviews.tsv | head 
~~~

~~~{.bash .merge-code}
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
~~~

<div class="notice--big--primary">

### What I've learned: Awk Field Separators

Awk assumes that the fields in a record are whitespace delimited.

You can change this using the `-F` option like this

~~~{.bash caption=">_"}
$ awk -F '\t' '{ print $6 }'
~~~

</div>

I can also work backward from the last position forward by subtracting from `NF`.

~~~{.bash caption=">_"}
$ awk -F '\t' '{ print $NF "\t" $(NF-2)}' bookreviews.tsv | head 
~~~

~~~{.bash .merge-code}
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
~~~

<div class="notice--info">
**Side Note: NF and NR**

`$NF` seems like an unusual name for printing the last column, right?
But actually, `NF` is a variable holding the *Number of Fields* in a record. So I'm just using its value as an index to refer to the last field.

I can print the actual value like this:

~~~{.bash caption=">_"}
$ awk -F '\t' '{ print NF }' bookreviews.tsv | head  
~~~

~~~{.bash .merge-code}
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
~~~

Another variable Awk offers up for use is `NR`, the *number of records* so far. `NR` is handy when I need to print line numbers:

~~~{.bash caption=">_"}
$ awk -F '\t' '{ print NR " " $(NF-2) }' bookreviews.tsv | head  
~~~

~~~{.bash .merge-code}
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
~~~

</div>

## Awk Pattern Match With Regular Expressions

Everything I've done so far has applied to every line in our file, but the real power of Awk comes from pattern matching. And you can give Awk a pattern to match each line on like this:

~~~{.bash caption=">_"}
$ echo "aa
        bb
        cc" | awk '/bb/'
bb
~~~

You could replace `grep` this way. You can also combine this with the field access and printing we've done so far:

~~~{.bash caption=">_"}
$ echo "aa 10
        bb 20
        cc 30" | awk '/bb/ { print $2 }'
20
~~~

Using this knowledge, I can easily grab reviews by book title and print the book title(`$6`) and review score(`$8`).

The reviews I'm going to focus on today are for the book 'The Hunger Games'. I'm choosing it because it's part of a series with many reviews and I recall liking the movie. So I'm wondering if I should read it.  

~~~{.bash caption=">_"}
$ awk -F '\t' '/Hunger Games/ { print $6, $8  }' bookreviews.tsv | head
~~~

~~~{.merge-code}
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
~~~

I should be able to pull valuable data from these reviews, but first there is a problem. I'm getting reviews from more than one book here. `/Hunger Games/` matches anywhere in the line and I'm getting all kinds of 'Hunger Games' books returned. I'm even getting books that mention "Hunger Games" in the review text:

~~~{.bash caption=">_"}
$ awk -F '\t' '/Hunger Games/ { print $6 }' bookreviews.tsv | sort | uniq    
~~~

~~~{.merge-code}
Birthmarked
Blood Red Road
Catching Fire (The Hunger Games)
Divergent
Enclave
Fire (Graceling Realm Books)
Futuretrack 5
Girl in the Arena
...
~~~

I can fix this by using the `product_id` field to pattern match on:

~~~{.bash caption=">_"}
$ awk -F '\t' '$4 == "0439023483" { print $6 }' bookreviews.tsv | sort |  uniq 
~~~

~~~{.merge-code}
The Hunger Games (The Hunger Games, Book 1)
~~~

I want to calculate the average review score for 'The Hunger Games', but first, let's take a look at the review_date (`$15`), the review_headline (`$13`), and the star_rating (`$8`) of our Hunger Games reviews, to get a feel for the data:

~~~{.bash caption=">_"}
$ awk -F '\t' '$4 == "0439023483" { print $15 "\t" $13 "\t" $8}' \
    bookreviews.tsv | head 
~~~

~~~{.merge-code}
2015-08-19      Five Stars      5
2015-08-17      Five Stars      5
2015-07-23      Great read      5
2015-07-05      Awesome 5
2015-06-28      Epic start to an epic series    5
2015-06-21      Five Stars      5
2015-04-19      Five Stars      5
2015-04-12      i lile the book 3
2015-03-28      What a Great Read, i could not out it down   5
2015-03-28      Five Stars      5
~~~

Look at those star ratings. Yes, the book is getting many 5-star reviews, but more importantly, the layout of my text table looks horrible: the width of the review titles is breaking the layout.

To fix this, I need to switch from using `print` to using `printf`.

<div class="notice--big--primary">

### What I've learned: Awk Pattern Matching

I've learned that an awk action, like `{ print $4}`, can be preceded by a pattern, like `/regex/`. Without the pattern, the action runs on all lines.

You can use a simple regular expression for the pattern. In which case it matches anywhere in the line, like `grep`:

~~~{.bash caption=">_"}
$ awk '/hello/ { print "This line contains hello", $0}'
~~~

Or you can match within a specific field:

~~~{.bash caption=">_"}
$ awk '$4~/hello/ { print "This field contains hello", $4}'
~~~

Or you can exact match a field:

~~~{.bash caption=">_"}
$ awk '$4 == "hello" { print "This field is hello:", $4}'
~~~

</div>

## Awk `printf`

`printf` works like it does in the C and uses a format string and a list of values. You can use `%s` to print the next string value.

So my `print $15 "\t" $13 "\t" $8`
becomes `printf "%s \t %s \t %s", $15, $13, $8`.

From there I can add right padding and fix my layout by changing `%s` to `%-Ns` where `N` is my desired column width:

~~~{.bash caption=">_"}
$ awk -F '\t' \
   '$4 == "0439023483" { printf "%s \t %-20s \t %s \n", $15, $13, $8}'  \
   bookreviews.tsv | head 
~~~

~~~{.merge-code}
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
~~~

This table is pretty close to what I'd want. However, some of the titles are just too long. I can shorten them to 20 characters with `substr($13,1,20)`.

Putting it all together and I get:

~~~{.bash caption=">_"}
$ awk -F '\t' \
 '$4 == "0439023483" { 
    printf "%s \t %-20s \t %s \n",$15,substr($13,1,20),$8
  }' \
 bookreviews.tsv | head
~~~

~~~{.merge-code}
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
~~~

Alright, I think at this point, I'm ready to move on to star calculations.

<div class="notice--big--primary">

### What I've Learned: `printf` and Built-ins

If you need to print out a table, Awk lets you use `printf` and built-ins like `substr` to format your output.

It ends up looking something like this:

~~~{.bash caption=">_"}
$ awk '{ printf "%s \t %-5s", $1, substr($2,1,5) }'
~~~

`printf` works much like C's `printf`. You can use `%s` to insert a string into the format string, and other flags let you the set width or precision. For more information on `printf` or other built-ins, you can consult an Awk reference document.
</div>

## Awk `BEGIN` and `END` Actions

I want to calculate the average rating for book reviews in this data set. To do that, I need to use a variable. However, I don't need to declare the variable or its type. I can just use it:

I can add up and print out a running total of review_stars (`$8`) like this:

~~~{.bash caption=">_"}
$ awk -F '\t' '{ total = total + $8; print total }' bookreviews.tsv | head 
~~~

~~~{.merge-code}
0
5
10
...
~~~

And to turn this into an average, I can use `NR` to get the total amount of records and `END` to run an action at the end of the processing.

~~~{.bash caption=">_"}
$ awk -F '\t' '
    { total = total + $8 }
END { print "Average book review:", total/NR, "stars" }
' bookreviews.tsv | head 
~~~

~~~{.merge-code}
Average book review is 4.24361 stars
~~~

I can also use `BEGIN` to run an action before Awk starts processing records.

~~~{.bash caption=">_"}
 $ awk -F '\t' '
BEGIN { print "Calculating Average ..." } 
      { total = total + $8 }
END   { print "Average book review:", total/NR, "stars" }
' bookreviews.tsv 
~~~

~~~{.merge-code}
Calculating Average ...
Average book review is 4.24361 stars
~~~

<div class="notice--big--primary">

### What I've learned: Awk's `BEGIN`, `END` and Variables

Awk provides two special patterns, `BEGIN` and `END`. You can use them to run actions before and after processing the records. For example, this is how you would initialize data, print headers and footer, or do any start-up or tear-down stuff in Awk.

It ends up looking like this:

~~~{.bash caption=">_"}
$ awk '
BEGIN { print "start up" }
      { print "line match" }
END   { print "tear down" }'
~~~

You can also easily use variables in Awk. No declaration is needed.

~~~{.bash caption=">_"}
$ awk -F '{ total = total + $8 }'
~~~

</div>

## Fun Awk One-Liners

Before we leave the world of one-liners behind, I reached out to my friends to ask when they use Awk day-to-day. Here are some of the examples I got back.  

Printing files with a human readable size:

~~~{.bash caption=">_"}
$ ls -lh | awk '{ print $5,"\t", $9 }'  
~~~

~~~{.merge-code}
7.8M     The_AWK_Programming_Language.pdf
6.2G     bookreviews.tsv
~~~

Getting the containerID of running docker containers:

~~~{.bash caption=">_"}
$ docker ps -a |  awk '{ print $1 }'
~~~

~~~{.merge-code}
CONTAINER
08488f220f76
3b7fc673649f
~~~

You can combine that last one with a regex to focus on a line you care about. Here I stop `postgres`, regardless of its tag name:

~~~{.bash caption=">_"}
$ docker stop "$(docker ps -a |  awk '/postgres/{ print $1 }')"
~~~

You get the idea. If you have a table of space-delimited text returned by some tool then Awk can easily slice and dice it.

## Awk Scripting Examples

> If you pick your constraints you can make a particular envelope of uses easy and ones you don't care about hard.
> Awk's choice to be a per line processor, with optional sections for processing before all lines and after all lines is self-limiting but it defines a useful envelope of use.
>
> [Michael Feathers](https://news.ycombinator.com/item?id=13455678)

In my mind, once an Awk program spans multiple lines, it's time to consider putting it into a file.

<div class="notice--info">
**Side Note: Why Awk Scripting**

Once we move beyond one-liners, a natural question is *why*. As in 'Why not use Python? Isn't it good at this type of thing?'

I have a couple of answers for that.

First, Awk is great for writing programs that are, at their core, a glorified for loop over some input. If that is what you are doing, and the control flow is limited, using Awk will be more concise than Python.

Second, if you need to rewrite your Awk program into Python at some point, so be it. It's not going to be more than 100 lines of code, and the translation process will be straightforward.  

Third, why not? Learning a new tool can be fun.
</div>

We've now crossed over from one-liners into Awk scripting. With Awk, the transition is smooth. I can now embed Awk into a bash script:

~~~{.bash caption=">_"}
$ cat average
~~~

~~~{.bash .merge-code}
exec awk -F '\t' '
    { total = total + $8 }
END { print "Average book review is", total/NR, "stars" } 
' $1
~~~

~~~{.bash caption=">_"}
$ average bookreviews.tsv
~~~

~~~{.merge-code}
Average book review is 4.2862 stars
~~~

Or I can use a shebang (`#!`):

~~~{.bash caption="average.awk"}
#!/usr/bin/env -S gawk -f

BEGIN { FS = "\t" }
{ total = total + $8 }
END { print "Average book $6 review is", total/NR, "stars" } 
~~~

And run it like this

~~~{.bash caption=">_"}
$ ./average.awk bookreviews.tsv
~~~

Or you can also pass it to awk directly using `-f`:

~~~{.bash caption=">_"}
$ awk -f average.awk bookreviews.tsv
~~~

<div class="notice--info">

### Side Note: BEGIN FS

If you use a shebang or pass to Awk directly, it's easiest to set the file separator using `FS = "\t"` in the `BEGIN` action.

~~~{.bash caption=">_"}
BEGIN { FS = "\t" }
~~~

</div>

## Awk Average Example

At this point, I should be ready to start calculating review scores for The Hunger Games:

~~~{.bash }
exec awk -F '\t' '
$4 == "0439023483" { title=$6; count = count + 1; total = total + $8 }
END { 
      print "The Average book review for", title, "is", total/count, "stars" 
    }  
' $1
~~~

Now that I'm in a file, I can format this out a bit better so its easier to read:

~~~{.awk caption="average.awk"}
$4 == "0439023483" { 
  title=$6
  count = count + 1; 
  total = total + $8 
}
END { 
  printf "Book: %-5s\n", title
  printf "Average Rating: %.2f\n", total/count 
}  
~~~

Either way, I get this output:

~~~
Book: The Hunger Games (The Hunger Games, Book 1)
Average Rating: 4.67%       
~~~

<div class="notice--big--primary">

### What I've learned: Calling Awk From a File

Once you are beyond a single line, it makes sense to put your Awk script into a file.

You can then call you program using the `-f`option

~~~{.bash caption=">_"}
$ awk -f file.awk input
~~~

Using a shebang :

~~~{.bash caption=">_"}
#!/usr/bin/env -S gawk -f
~~~

or by using a bash `exec` command:

~~~{.bash caption=">_"}
exec awk -F '\t' 'print $0' $1
~~~

</div>

## Awk Arrays

I'd like to know if the series stays strong or if it's a single great book that the author stretched out into a trilogy. If the reviews decline quickly, then that is not a good sign. I should be able to see which book was rated the best and which was the worst. Let's find out.

If I were going to calculate the averages in Python, I would loop over the list of reviews and use a dictionary to track the total stars and total reviews for each.

In Awk I can do the same:

~~~{.awk caption="hungergames.awk"}
BEGIN { FS = "\t" }
$6~/\(The Hunger Games(, Book 1)?\)$/ { 
  title[$6]=$6
  count[$6]= count[$6] + 1
  total[$6]= total[$6] + $8
}
END { 
    for (i in count) {
        printf "