---
title: "Understanding AWK"
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - just an example
---
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
