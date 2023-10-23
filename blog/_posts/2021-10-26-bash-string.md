---
title: "Bash String Manipulation"
categories:
  - Tutorials
toc: true
author: Adam
sidebar:
  nav: "bash"
internal-links:
 - bash strings
 - bash substring
topic: cli
bottomcta: false
last_modified_at: 2023-04-17
excerpt: |
    Learn how to manipulate strings in bash with this informative tutorial. From concatenating strings to replacing parts of a string, you'll discover useful techniques for working with text in bash scripts.
---

**We're [Earthly](https://earthly.dev/). We make building software simpler and, therefore, faster. This article is about bash – which has its quirks but is a tool we find ourselves often reaching for. If you are looking for an open-source tool to improve how you build software, then [check us out](/).**

<div class="narrow-code">
One thing that bash is excellent at is manipulating strings of text. If you're at the command line or writing a small script, then knowing some bash string idioms can be a lot of help.

So in this article, I'm going to go over techniques for working with strings in bash.

You can run any of the examples at the bash prompt:

~~~{.bash caption=">_"}
> echo "test"
test
~~~

Or you can put the same commands into a file with a bash shebang.

~~~{.bash }
#!/bin/bash

echo "test"
~~~

And then make it executable using `chmod` and run it at the command line:

~~~{.bash caption=">_"}
> chmod +x strings.sh
> ./strings.sh
test
~~~

</div>

## Background

If you need a review of the basics of bash scripting, check out [Understanding Bash](/blog/understanding-bash/). If not, know that everything covered will work in bash version 3.2 and greater. Much covered will also work in ZSH. That means everything here will work on macOS, Windows under WSL and WSL 2, and most Linux distributions. Of course, if you're on Alpine, or some minimal linux distribution, you will need to install bash first.

Let's start at the beginning.

## Bash Concatenate Strings

In bash, I can declare a variable like this:

~~~{.bash caption=">_"}
> one="1"
~~~

and then I can refer to it in a double-quoted string like this:

~~~{.bash caption=">_"}
> echo "$one"
1
~~~

Concatenating strings follows easily from this same pattern:

~~~{.bash caption="concat1"}
#!/bin/bash

one="1"
two="2"
three="$one$two"
echo "$three"
~~~

~~~{.output caption="running concat1"}

12
~~~

<div class="notice--info">

### Side Note: Globs and File Expansions

You can, in theory, refer to variables directly like this:

~~~{.bash}
echo $one
~~~

but if you do that, you might have unexpected things happen.

~~~{.bash caption="bad_expand.sh"}
#!/bin/bash

comment="/* begin comment block"
echo $comment
~~~

~~~{.ini caption="Output"}
/Applications /Library /System /Users /Volumes /bin /cores /dev /etc 
/home /opt /private /sbin /tmp /usr /var begin comment block
~~~

Without quotes, bash splits your string on whitespace and then does a pathname expansion on `/*`.

I'm going to use whitespace splitting later on, but for now remember: **You should always use double quotes, when echoing, if you want the literal value of a variable.**
</div>

### Another Concatenate Method +=

Another way to combine strings is using `+=`:

~~~{.bash caption="concat2.sh"}
#!/bin/bash

concat=""
concat+="1"
concat+="2"
echo "$concat"
~~~

~~~{.output caption="Output"}
12
~~~

Next, let's do string length.

## Bash String Length

The `"$var"` syntax is called variable expansion in bash and you can also write it as `"${var}"`. This expansion syntax allows you to do some powerful things. One of those things is getting the length of a string:

~~~{.bash caption=">_"}
> words="here are some words"
> echo "'$words' is ${#words} characters long
'here are some words' is 19 characters long
~~~

## Bash SubString

If I need to get a portion of an existing string, then the substring syntax of parameter expansion is here to help.

The format you use for this is `${string:position:length}`. Here are some examples.

### Bash First Character

You can get the first character of a string like this:

~~~{.bash caption=">_"}
> word="bash"
> echo "${word:0:1}"
b
~~~

Since I'm asking to start at position zero and return a string of length one, I can also shorten this a bit:

~~~{.bash caption=">_"}
> word="bash"
> echo "${word::1}"
b
~~~

However, this won't work in ZSH (where you must provide the 0):

~~~{.bash caption=">_"}
> word="zsh"
> echo "${word::1}"
zsh: closing brace expected
~~~

You can get the inverse of this string, the portion starting after the first character, using an alternate substring syntax `${string:position}` (Note the single colon and single parameter). It ends up looking like this:

~~~{.bash caption="index_strings.sh"}
#!/bin/bash

word="bash"
echo "Head: ${word:0:1}"
echo "Rest: ${word:1}"
~~~

~~~{.output caption="Output"}
Head: b
Rest: ash
~~~

This substring works by telling the parameter expansion to return a new string starting a position one, which drops the first character.

### Bash Last Character

To return the last character of a string in bash, I can use the same single-argument substring parameter expansion but use negative indexes, which will start from the end.

~~~{.bash caption="neg_index.sh"}
#!/bin/bash

word="bash" 
echo "${word:(-1)}"
echo "${word:(-2)}"
echo "${word:(-3)}"
~~~

~~~{.output caption="Output"}
h
sh
ash
~~~

To drop the last character, I can combine this with the string length expansion (`${#var}`):

~~~{.bash caption="combined.sh"}
#!/bin/bash

word="bash" 
echo "${word:0:${#word}-1}"
echo "${word:0:${#word}-2}"
echo "${word:0:${#word}-3}"
~~~

~~~{.output caption="Output"}
bas
ba
b
~~~

That is a bit long, though, so you could also use the pattern expansion for removing a regex from the end of a string (`${var%<<regex>>}`) and the regular expression for any single character (`?`):

~~~{.bash caption="question.sh"}
#!/bin/bash

word="bash" 
echo "${word%?}
echo "${word%??}
echo "${word%???}
~~~

~~~{.output caption="Output"}
bas
ba
b
~~~

This regex trim feature only removes the regex match if it finds one. If the regex doesn't match, it doesn't remove anything.

~~~{.bash caption=">_"}
> word="one"
> echo "${word%????}" # remove first four characters
one 
~~~

You can also use regular expressions to remove characters from the beginning of a string by using `#` like this:

~~~{.bash caption="question2.sh"}
#!/bin/bash

word="bash" 
echo "${word#?}
echo "${word#??}
echo "${word#???}
~~~

Running that I get characters dropped from the beginning of the string if they match the regex:

~~~{.output caption="Output"}
ash
sh
h
~~~

## Bash String Replace

Another common task I run into when working with strings in bash is replacing parts of an existing string.

Let's say I want to change the word `create` to `make` in this quote:

> When you don't create things, you become defined by your tastes rather than ability. Your tastes only narrow & exclude people. So create.
>
> Why The Lucky Stiff

There is a parameter expansion for string replacement:

~~~{.bash caption="replace.sh"}
#!/bin/bash

phrase="When you don't create things, you become defined by your tastes 
rather than ability. Your tastes only narrow & exclude people. So create."
echo "${phrase/create/make}"
~~~

~~~{.output caption="Output"}
When you don't make things, you become defined by your tastes 
rather than ability. Your tastes only narrow & exclude people. So create.
~~~

You can see that my script only replaced the first `create`.

To replace all, I can change it from `test/find/replace` to `/text//find/replace` (Note the double slash `//`):

~~~{.bash caption="replace2.sh"}
#!/bin/bash

phrase="When you don't create things, you become defined by your tastes 
rather than ability. Your tastes only narrow & exclude people. So create."
echo "${phrase//create/make}"
~~~

~~~{.output caption="Output"}
When you don't make things, you become defined by your tastes 
rather than ability. Your tastes only narrow & exclude people. So make.
~~~

You can do more complicated string placements using regular expressions. Like redact a phone number:

~~~{.bash caption="regex.sh"}
#!/bin/bash

number="Phone Number: 234-234-2343"
echo "${number//[0-9]/X}
~~~

~~~{.output caption="Output"}
Phone number: XXX-XXX-XXXX
~~~

If the substitution logic is complex, this regex replacement format can become hard to understand, and you may want to consider using regex match (below) or pulling in an outside tool like `sed`.

## Bash String Conditionals

You can compare strings for equality (`==`), inequality (`!=`), and ordering (`>` or `<`):

~~~{.bash caption="eq1.sh"}
if [[ "one" == "one" ]]; then
    echo "Strings are equal."
fi

if [[ "one" != "two" ]]; then
    echo "Strings are not equal."
fi

if [[ "aaa" < "bbb" ]]; then
    echo "aaa is smaller."
fi
~~~

~~~{.output caption="Output"}
Strings are equal.
Strings are not equal.
aaa is smaller.
~~~

You can also use `=` to compare strings to globs:

~~~{.bash caption="eq2.sh"}
#!/bin/bash
file="todo.gz"
if [[ "$file" = *.gz ]]; then
    echo "Found gzip file: $file"
fi
if [[ "$file" = todo.* ]]; then
    echo "Found file named todo: $file"
fi
~~~

~~~{.output caption="Output"}
Found gzip file: todo.gz
Found file named todo: todo.gz
~~~

(Note that in the above the glob is not quoted.)

You can see it matched in both cases. Glob patterns have their limits, though. And so when I need to confirm a string matches a specific format, I usually more right to regular expression match(`=~`).

### Bash String Regex Match

Here is how I would write a regex match for checking if a string starts with `aa`:

~~~{.bash caption="regex1.sh"}
#!/bin/bash
name="aardvark"
if [[ "$name" =~ ^aa ]]; then
    echo "Starts with aa: $name"
fi
~~~

~~~{.output caption="Output"}
Starts with aa: aardvark
~~~

And here using the regex match to find if the string contains a certain substring:

~~~{.bash caption="regex2.sh"}
#!/bin/bash
name="aardvark"
if [[ "$name" =~ dvark ]]; then
    echo "Contains dvark: $name"
fi
~~~

~~~{.output caption="Output"}
Contains dvark: aardvark
~~~

Unfortunately, this match operator does not support all of modern regular expression syntax: you can't use positive or negative look behind and the character classes are a little different then you would find in most modern programming languages. But it does support capture groups.

## Bash Split Strings

What if I want to use regexes to spit a string on pipes and pull out the values? This is possible using capture groups :

~~~{.bash caption="regex3.sh"}
if [[ "1|tom|1982" =~ (.*)\|(.*)\|(.*) ]]; 
then 
  echo "ID = ${BASH_REMATCH[1]}" ; 
  echo "Name = ${BASH_REMATCH[2]}" ; 
  echo "Year = ${BASH_REMATCH[3]}" ; 
else 
  echo "Not proper format"; 
fi
~~~

~~~{.output caption="Output"}
ID = 1
Name = tom
Year = 1982
~~~

Capture groups can be convenient for doing some light-weight string parsing in bash. However, there is a better method for splitting strings by a delimiter. It requires a little explanation, though.

### Internal Field Separator Split

By default, bash treats spaces as the delimiter between separate elements. This can lead to problems, though, and is one of the reasons I mentioned earlier for double quoting your variable assignments. However, this space delimiting can also be a helpful feature:

~~~{.bash caption="list.sh"}
list="foo bar baz"
for word in $list; do # <-- $list is not in double quotes
  echo "Word: $word"
done
~~~

~~~{.output caption="Output"}
Word: foo
Word: bar
Word: baz
~~~

If you wrap space-delimited items in brackets, you get an array.

You can access this array like this:

~~~{.bash caption="list2.sh"}
list="foo bar baz"
array=($list)
echo "Zeroth: ${array[0]}"  
echo "First: ${array[1]}"  
echo "Whole Array: ${array[*]}" 
~~~

~~~{.output caption="Output"}
Zeroth: foo
First: bar
Whole Array: foo bar baz
~~~

I can use this feature to split a string on a delimiter. All I need to do change the internal field separator (`IFS`), create my array, and then change it back.

~~~{.bash caption="ifs.sh"}
#!/bin/bash

text="1|tom|1982"

IFS='|' 
array=($text)
unset IFS;
~~~

And now I have an array split on my chosen delimiter:

~~~{.bash caption="ifs.sh continued"}
echo "ID = ${array[1]}" ; 
echo "Name = ${array[2]}" ; 
echo "Year = ${array[3]}" ; 
~~~

~~~{.output caption="Output"}
ID = 1
Name = tom
Year = 1982
~~~

## Reaching Outside of Bash

Many things are hard to do directly in pure bash but easy to do with the right supporting tools. For example, trimming the [whitespace](https://stackoverflow.com/a/3352015) from a string is verbose in pure bash, but its simple to do by piping to existing POSIX tools like `xargs`:

~~~{.bash caption=">_"}
> echo "   lol  " | xargs
lol
~~~

Bash regular expressions have some limitations but sed, grep, and [`awk`](/blog/awk-examples) make it easy to do whatever you need, and if you have to deal with JSON data [`jq`](/blog/jq-select) will make your life easier.

<div class="no_toc_section">

## Conclusion

</div>

I hope this overview of string manipulation in bash gave you enough details to cover most of your use cases.

Also, if you're the type of person who's not afraid to solve problems in bash then take a look at [Earthly](https://earthly.dev/). It's a great tool for creating repeatable builds in a approachable syntax.

{% include_html cta/bottom-cta.html %}

<div class="no_toc_section">

## Feedback

</div>

If you have any clever tricks for handling strings in bash, or spot any problems with my examples, let me know on Twitter [`@AdamGordonBell`](https://twitter.com/adamgordonbell):
<blockquote class="twitter-tweet"><p lang="en" dir="ltr">How many of these bash string parameter expansions idioms do you use? <a href="https://t.co/9UIuLPgELy">https://t.co/9UIuLPgELy</a></p>&mdash; Adam Gordon Bell 🤓 (@adamgordonbell) <a href="https://twitter.com/adamgordonbell/status/1453341378361049091?ref_src=twsrc%5Etfw">October 27, 2021</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
