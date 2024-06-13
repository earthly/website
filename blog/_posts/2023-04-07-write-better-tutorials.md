---
title: "How to Write a Tutorial About How to Read a CSV in Golang"
toc: true
author: Josh
topcta: false
bottomcta: false
internal-links:
 - just an example
excerpt: |
    Learn how to write effective technical tutorials by providing context, being patient, and running code. This article explores the common pitfalls of tutorial writing and offers advice on how to improve your tutorials.
last_modified_at: 2023-07-19
categories:
  - writing
---

We've been running the Earthly blog for [over a year](/blog/write-for-us-anniversary) now, and in that time we've worked with dozens of talented writers on nearly a hundred programming tutorials.

Many times developers would come to us with great ideas, but not much writing experience. In those cases we are happy to help them work through multiple drafts of an article. After a while, we started to notice that we were giving the same notes over and over again, so I thought I'd write a bit about tutorial writing, why it can be so challenging, and what advice we've learned to give to writers to help them improve.

One of the things that makes tutorials effective is that you get to learn by doing, so at the end we'll take the slightly meta approach of writing a short tutorial using some of the things we've learned about writing tutorials. Let's try to resist making jokes about recursion or Inception. This only goes one level deep. It's a box inside a slightly bigger box and that's the end of it.

## Types of Technical Writing

We tend to encounter three types of written technical resources as software developers:

### 1. Official Docs

I'm not talking about the Getting Started tutorials on the home page. I'm talking about the raw documentation. These are usually designed as a reference, or manual. They are sometimes dry and dense, though they don't need to be. Documentation is extremely useful, but it's more concerned with accurately and succinctly recording information. **Documentation doesn't attempt to teach you.** It says, here is the information, do with it what you will.

### 2. Procedures

This is usually just a checklists of instructions for what to do in certain situations. You'll sometimes see these at companies disguised as "Internal Documentation" or "SOPs".

a. SSH into the server.
b. Check the logs for errors.
c. If you find errors, fix them.
d. If you can't find any errors follow this broken link.
c. WARNING This document is out of date.

Procedures are **helpful for users who already understand the system**, but just need to remember how to achieve a complicated multi-step outcome. Things like updating dependencies, restoring database backups, or clearing out old logs often benefit from having a procedure written down, but should still be done by someone who knows the system and can improvise if something goes wrong. Rocket launches have procedures. Hopefully no one uses them to try to learn about rocket launches for the first time.

### 3. Tutorials

This is what we're here for. Tutorials teach you something. A great tutorial offers some technical information, similar to the docs, and often walks you towards a desired outcome, like a procedure, but tutorials need to be more than the sum of those parts. Tutorials need to not only consider *what* we are learning, but the *ways in which people learn*. That's what separates them from documentation and procedures and why they can be so hard to write well.

## Showing Is Not Teaching

When I was a kid my parents would make me load the dishwasher after dinner. I hated it. I'd try to race through the task, cramming dishes and pots and cups in, smashing them to fit at any angle. Inevitable my father would come around. Usually a quiet, patient man, he'd be overcome with frustration.

"No no no. I told you a thousand times."

He'd pull everything out and redo it himself with me standing there watching in silence. When he was done, he'd point down triumphantly at his work and say, "You see? You do it like that!"

But I was 7, and unsure about why you couldn't just throw all the dirty dishes away and get new ones. So when I looked down at what my dad had done all I saw was a pile of dishes that, to me, looked exactly like the pile I had created before he redid it. And this would just happen over and over - me doing it wrong, him making me stand there and watch him do it again - until finally he stopped asking me to load the dishwasher all together.

When I first started learning to code I had versions of this with other devs who were senior to me. Some of them where jerks about it, but most where kind, thoughtful people who were trying to help. They'd run through a complicated idea that made total sense to them and then say, "See? Like that." But I wouldn't see, because it all happened too fast. There was too much going on. I had no idea what was important and what wasn't.

And then later, when I became the one trying to train juniors, I would do the exact same thing! The problem was that I knew the material so well, I had no clue what wasn't clear, what needed time to understand.

This form of "teaching" we all thought we were doing where we point and say "See, like this." is not very effective, but it's probably the most common way that we expect people to learn in a professional setting. This is half the problem with most onboarding and corporate trainings, and *it's where most tutorial writing falls short*.

### Too Much Too Fast

Moving too quickly through material can happen in several different ways when writing a tutorial, but the most prominent is the dreaded giant code block. It's basically a meme at this point. The writer introduces the topic and then says, "Now just copy and paste this code, which will train an AI to train 2 more AIs." Followed by a huge chunk of code dozens of lines long. Then they say something like, "Run this and it should work."

More commonly, writers will attempt to follow the code block with a line by line explanation. "Line 1 does this, lines 2-4 do this, line 5 does this" etc. This approach at least has good intentions, but it's usually impossible to follow.

When we first our Write With Us program and authors would do this, we would tell them to break the code up into smaller chunks, and then explain those as they go. This would work to make the code in the tutorial more digestible, but the articles still remained difficult to follow. It was still missing something.

## What Many Tutorials Are Missing

Breaking complicated ideas down is really helpful for learning, but in a tutorial, it's not enough. Once we realized that, we started to be more nuanced in how we provided feedback to writers. In the end we often ended up giving some version of these three comments.

### This Needs Context

So many tutorials don't explain *why*? Why do I need to do it like this? Why is this useful? Why not do it another way? And if they do explain why, they do it once, in the intro, and never again. Context often needs to be repeated. Context frames things for the learner. It helps them connect what they don't know yet with things they do know. When you're learning something new you often feel afloat, and context is what gives you solid ground to walk on.

### Think About Your Audience

Another way to patience and empathy. You need to think about not just who your audience is, but what they may be thinking and feeling while reading what you are writing. People who are learning new things often feel at least a little bit overwhelmed, intimidated, stupid etc. They will have questions or require clarification where an expert will not. They will require that some ideas are repeated or explained slowly. A writer is going to have to make a lot of decisions about what to spend time on. Understanding your audience is the only way you can make those decisions with any type of confidence.

### Run the Code Often

You'd be amazed how often tutorials do not run code and display the output. Show me the maniac who writes 100 lines of code without running it a dozen times along the way.

Running the code as you go doesn't just give your reader a sense of progression, it also gives them small milestones to hold onto as they read. Even if they are not coding along themselves, they can start to see how little parts of the code work, and understand how they will build up to a larger solution.

Also, running code that errors out can be extremely valuable. Understanding why things don't work is a great way to move toward understanding why they do.

## Example Time

Ok, all of this is great in theory, but what does it look like in practice?

Let's look at a solid example of what I'm talking about. Let's write a tutorial. Better yet, let's write the same tutorial three times. We'll start out writing it in a way that mostly ignores the comments above. We'll use one large code block, give little context, ignore our audience, and we won't run the code. Slowly we'll rework it over two more drafts, improving it along the way.

For this exercise I've chosen a relatively simple topic to write about: How to Read a CSV in Golang. This way we can write it three times without it getting too long. We aren't going to do anything flashy. We are just going to slowly implement the ideas above and see what it get's us. Also, I'm going to skip the introduction and the conclusion so we can just focus on the meat of the tutorial.

### Before We Start Writing

Before we get started we need to ask ourselves, who is our audience? This questions seems deceptively simple. You may say, "People who want to know how to read a CSV in Golang." Yes, that's part of it. But we need to be more specific. With tutorials I usually ask versions of the following questions:

1. How experienced of a developer is the reader?
2. What knowledge can I assume they already have?

With these questions in mind I'm going to make the following assumptions about my audience when writing about how to read a CSV file in Go.

1. They are familiar with Go and its syntax.
2. They have some experience coding, but may not be an expert.
3. They may not have any experience reading or writing directly to a file of any kind.
4. They *do* already know what a CSV file is. (This assumption is mostly just to keep the examples short. If I was writing a full tutorial about reading from a CSV I would include at least some explication about what they are and how they work.)

### First Draft

For this first attempt, we'll do very little work to help our reader understand.

<div class="notice--info">

To read from a CSV file you use the `encoding/csv` package. You use the `Read()` function to read one line at a time. Or, you can use the `ReadAll()` function to read all the lines at once.

~~~{.go}
package main

import (
    "encoding/csv"
    "fmt"
    "os"
)

func main() {
    file, err := os.Open("test.csv")
    if err != nil {
        fmt.Println(err)
    }
    reader := csv.NewReader(file)
    
  record, _ := reader.Read()

    records, _ := reader.ReadAll()

    fmt.Println(record)
    fmt.Println(records)
}

~~~

This code first imports the `csv` module as well as the `os` module. It then opens a file. After that we create a new reader. Then it reads a line using the `Read()` function. Then it reads the rest of the lines using the `ReadAll()` function.

</div>

If you are an experienced developer who already knows how reading from a CSV works, then this is probably fine. You don't even really need to read the text, you can just look at the code since it's not that complicated. But if that's the case, you don't need a tutorial. You can just reference the docs. For people who do need a tutorial, who need help deepening their understanding beyond what the docs can provide, this gives them nothing new.

This is the tutorial equivalent of standing in front of the dishwasher and saying "See?".

This version of our tutorial lacks patience. It tries to speed through the information. It has no empathy, it doesn't consider its audience and what they may need. It gives no example of what to expect when running the code.

At first, when we would get tutorials like this from writers we'd give a note similar to: "Try breaking the code up into smaller chunks and explain them as you go. Try adding some context along the way." Basically this was a very not direct or clear way of us saying, "Rewrite this so it teaches something, instead of just showing it."

Usually, the writer would rewrite it and return something like our next draft.

## Second Draft

For draft two, let's try to be a bit more patient. We'll take time to walk through the important parts of the code and break it down step by step.

<div class="notice--info">

In order to read from a csv file in Go, we first need to import the `encoding/csv`, the `fmt` and the `os` packages.

~~~{.go}
package main

import (
    "encoding/csv"
    "fmt"
    "os"
)
~~~

We start by opening the file.

~~~{.go}
func main() {
    
    file, err := os.Open("test.csv")
    if err != nil {
        fmt.Println(err)
    }

~~~

Next we create a reader and pass in the file. This will allow us to read lines from the csv.

~~~{.go}
    reader := csv.NewReader(file)
~~~

Finally, we can use the `Read()` function to read one line at a time. We can use the `ReadAll()` function to read all the lines at once.

~~~{.go}
    record, _ := reader.Read()

    records, _ := reader.ReadAll()

    fmt.Println(record)
    fmt.Println(records)

~~~

</div>

This is a little better, at least we get walked through each line a bit more thoroughly, but you see what we've done? We still have the same basic problem we've just done it several times instead of once.

We're still just showing code with a quick explanation of what it does. It's easier to follow, but there's little context, not much new beyond what the docs offer, and we never run the code.

## Third Draft

We going to keep the similar structure we set up before, where the code is broken up into smaller chunks, but we are going to make some new changes.

1. I'm going to use an actual CSV file that we can run code against.
2. I'll try to anticipate questions along the way and attempt to answer them.
3. Provide context for *why* the code is the way it is.

<div class="notice--info">

In order to learn how to read from a csv, we'll first need a csv. I'll be using this [list of movie data](https://gist.github.com/tiangechen/b68782efa49a16edaf07dc2cdaa855ea) made public by github user tiangechen. I just copied it all into a file called `movies.csv`.

Go has its own built in standard library for dealing with CSV data. It's not very robust, but it's got everything we need to get started using CSV files in our Go code.

Let's start by importing the `encoding/csv` package. We will also import `os` because we will need it to open and close the file, and `fmt` so we can print some values to the terminal.

~~~{.go}
import (
    "encoding/csv"
    "fmt"
    "os"
)
~~~

To get started, we need to open the `csv` file so that we can use it in our code. This is easy with the `os` package.

~~~{.go}
file, err := os.Open("movies.csv")
if err != nil {
    fmt.Println(err)
}

~~~

`os.Open` isn't unique to CSV files. You can use it to open any type of file in Go. It's also worth noting that `os.Open()` doesn't read the data in the `movies.csv`, it just allows us to now work with the file in our Go code.

To read the data we first need to pass the file to the `csv.NewReader()` function. This function is unique to CSV files. It knows what they are and how to read data from them.

~~~{.go}
reader := csv.NewReader(file)
~~~

This returns a [`Reader` struct](https://pkg.go.dev/encoding/csv#Reader) that has some functions attached to it that will allow us to read from the file in a couple different ways.

Let's start by reading all of the lines from the file at once.

~~~{.go}
allLines, err := reader.ReadAll()

if err != nil {
    fmt.Println("Error reading CSV:", err)
    return
}

fmt.Println(allLines)
~~~

If you run this code, and you're using the same dataset as me, your output will look like this:

~~~
[[Film Genre Lead Studio Audience score % Profitability Rotten Tomatoes % Worldwide Gross Year] [Youth in Revolt Comedy The Weinstein Company 52 1.09 68 $19.62  2010] [You Will Meet a Tall Dark Stranger Comedy Independent 35 1.211818182 43 $26.66  2010] [When in Rome Comedy Disney 44 0 15 $43.04  2010] [What Happens in Vegas Comedy Fox 72 6.267647029 28 $219.37  2008] ....
~~~

Actually, there's way more, but for the sake of brevity, I've only included the first few lines. A couple of things to notice here. First, how is the data structured? When it was in the csv file, each row was separated by a new line and rows themselves were broken up into columns with commas. But now the data has been translated into Go and Go doesn't have a `csv` type, so it needs to convert the data into something it understands. In this case, a [slice](https://go.dev/blog/slices-intro). Actually, a slice of slices, where each slice in the larger slice represents a line in the csv.

From here we can treat the data like any slice. For example, we can loop through it and print one line at a time to the console. Remember that each line is also a slice, so I've imported the `string` package so I can join each line of data into a simple string. This isn't necessary, I just thought it looked a little better when it printed to the console.

~~~{.go}
for _, line := range allLines {
      str := strings.Join(line[:], ",")
    fmt.Println(str)
}
~~~

~~~
Film,Genre,Lead Studio,Audience score %,Profitability,Rotten Tomatoes %,Worldwide Gross,Year
Youth in Revolt,Comedy,The Weinstein Company,52,1.09,68,$19.62 ,2010
You Will Meet a Tall Dark Stranger,Comedy,Independent,35,1.211818182,43,$26.66 ,2010
....
~~~

Or we can get the average Audience Score for all the movies. Remember, we're dealing slices of `strings`, so we'll need to convert any number values to an `int` if we want to do any math.

~~~{.go}
    for _, movie := range movies {
        i, err := strconv.Atoi(movie[3]) // index of audience score
        if err != nil {
            fmt.Println("Error converting string to int:", err)
            return
        }

        sum += i
    }
    avg := sum / len(movies)
    fmt.Println(avg)
~~~

Run this and... Oh no! It's broken.

~~~
Error converting string to int: strconv.Atoi: parsing "Audience score %": invalid syntax
~~~

No worries, we can fix this. First, let's talk about headers.

### Headers and Reading One Line at a Time

You may have noticed that the first line in our `movies.csv` is different than the rest. It's not a line of movie data, it's a line of headers or labels for each column of data. Not all csv files have this, but when they do, we may want to deal with this header line separate from the rest of the lines.

The header row in `movies.csv` is what's breaking our code when we try to calculate the average audience score. Specifically, this line is breaking.

~~~{.go}
    i, err := strconv.Atoi(movie[3]) // index of audience score
~~~

`strconv.Atoi()` is a function that takes a string and converts it into an int. So "3" (string) becomes `3` (int). That works for all the rows of data because all of those rows contain a string representation of a number at index 3. The header row, on the other hand, contains the string "Audience score %" at index 3. It's the label for the column of data.

We need to find a way to deal with this header row before we try to calculate the average. One way we could do that is to just remove the first element in our slice of all the lines. But this is a good opportunity to talk about the `Read()` function.

`Read()` reads one record at a time. Each time you call `Read()`, it gets the next line in the file.

~~~{.go}
    fmt.Println(reader.Read())
    fmt.Println(reader.Read())
    fmt.Println(reader.Read())
~~~

~~~
[Film Genre Lead Studio Audience score % Profitability Rotten Tomatoes % Worldwide Gross Year] <nil>
[Youth in Revolt Comedy The Weinstein Company 52 1.09 68 $19.62  2010] <nil>
[You Will Meet a Tall Dark Stranger Comedy Independent 35 1.211818182 43 $26.66  2010] <nil>
~~~

Here we called `Read()` three times and so got the first three lines. `ReadAll()` loads all the lines in the csv file into memory at once. For really large files, that can get costly. `Read()` loads each line one at a time, so if you don't need the entire file, it can save on memory. This can be usefully when you don't want or need to read the entire file. Say you have a file with millions of lines and you only want the first 10. You could write a loop that ran 10 times and called `Read()` each time. Or if you wanted to only read lines in a file until you found a certain record, `Read()` would also be the way go.

Another way `Read()` is useful is when dealing with Headers.

We can first grab the header with `Read()`. It's the first line, so we can do it right away. Then we can load the rest of the data using `ReadAll()`, since we want' all the movie data to help us calculate the average audience score.

~~~{.go}
    headers, err := reader.Read()
    movies, err := reader.ReadAll()
~~~

This illustrates something important about `ReadAll()`, which is that it reads all the lines in the file **that haven't been read yet**. So if we print the results, you'll see that `headers` is a single slice with all the header values. Separately, `movies` will be a slice of slices containing all the movie data, but not the header data, because we already read that line and saved it to the `headers` variable.  

~~~{.go}
    fmt.Println(headers)
    fmt.Println("--------------")
    fmt.Println(movies)
~~~

~~~
[Film Genre Lead Studio Audience score % Profitability Rotten Tomatoes % Worldwide Gross Year]
--------------
[[Youth in Revolt Comedy The Weinstein Company 52 1.09 68 $19.62  2010] [You Will Meet a Tall Dark Stranger Comedy Independent 35 1.211818182 43 $26.66  2010] [When in Rome Comedy Disney 44 0 15 $43.04  2010] [What Happens in Vegas Comedy Fox 72 6.267647029 28 $219.37  2008]...
~~~

Now we can finally get back to calculating our average audience score.

~~~{.go}
    for _, movie := range movies {
        i, err := strconv.Atoi(movie[3]) // index of audience score
        if err != nil {
            fmt.Println("Error converting string to int:", err)
            return
        }
        sum += i
    }
    avg := sum / len(movies)
    fmt.Println(avg)
~~~

~~~
63
~~~

</div>

This is starting to feel a lot better. We've slowed down our tutorial quite a bit and taken time to answer questions that might come up, like: "What does the data look like after we've read it from the csv file?", or "Why would I need to use `Read` instead of `ReadAll`?" In doing so we've talked about header rows, what they are, and how you might deal with them. We've introduced the idea that you can use `Read` and `ReadAll` together. We've added context by mentioning real world applications for what we are learning, and we ran the code several times and watched it break.

Is this the perfect CSV tutorial? No. But I hope it helped illustrate how context, patience, and running code can help you write tutorials that teach instead of just show.

## Conclusion

You can think about writing a tutorial in a similar way to building an API. There are patterns that you can follow to make it easier to write and easier to use, but those patterns are never going to cover every use case. You'll need to make decisions along the way, alter, and even break patterns in some cases to achieve the desired outcome.

<!--vale off-->
There's a lot more to writing a great tutorial than just Patience, running code, and providing context. We didn't cover everything. Structuring your tutorial in a logical way and learning how to write great introductions and conclusions, for example, could be articles on their own. So could choosing your audience, finding your writing voice, or learning how to write and rework multiple drafts.
<!--vale on-->

But I think these are three of the biggest pieces of advice we find ourselves given writers over and over again. I hope you'll find them useful next time you write a technical tutorial.

{% include_html cta/bottom-cta.html %}
