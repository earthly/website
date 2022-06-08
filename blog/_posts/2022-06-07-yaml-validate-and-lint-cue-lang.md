---
title: "YAML Validate with CUE Lang"
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - cue lang
 - yaml lint
 - yaml validate
---

I've [complained about using YAML](/blog/intercal-yaml-and-other-horrible-programming-languages/) when a programming language would is what's need before. But actually, when you've got configuring to do, YAML is pretty useful: It's so much nicer to read and write than the XML a had to write back in the early days of Java development. But one advantage XML seemly had of YAML is that XML schema were commonly used and so I wouldn't get errors like the one I got today on this very blog:

~~~{.bash caption=">_"}
Error parsing yaml file:
map values are not allowed here
  in "/Users/adam/sandbox/earthly-website/blog/authors.yml", line 2, column 8 
~~~

You see the blog is expecting a certain format of config, and I've violoated that expectation. The blog wants a string, and I've given it a map. If only we had XML Schema for YAML or even better a static type system for configuration.

It turns out such things do exist, there is [JSON Schema](https://json-schema.org/), [Dhall](https://dhall-lang.org/), and [Cuelang](https://cuelang.org/)[^1]. I'll save covering Dhall, and JSON Schema for another day. Today I'm going to show you how to use Cuelang, which is both an extension of YAML and command line tool, to validate your YAML. And I"m going to attempt to use it to prevent future problems with this blog's `authors.yml` file.

[^1]: I'll be referring to Cue as Cuelang in this article, and the command line tool as `cue`. Cue is a bit hard to search for in google, so perhaps I can start the trend of following GoLang's naming convention.

## Start Validating

Ok, so the authors of this blog are stored in a yaml file aptly named `authors.yaml` and it looks like this:

~~~{.yml caption="authors.yml"}
Corey:
    name    : "Corey Larson"
    bio     : "Eats, runs, and codes. Dad. Engineer. Progressive. LDS. Disneyland fanatic."
    avatar  : "/assets/images/authors/coreylarson.jpg"
Alex:
    name    : "Alex Couture-Beil"
    bio     : "Alex enjoys writing code, growing vegetables, and the great outdoors."
Vlad:
    name    : "Vlad A. Ionescu"
    bio     : " Founder of Earthly. Founder of ShiftLeft. Ex Google. Ex VMware. Co-author RabbitMQ Erlang Client."
    avatar  : "/assets/images/authors/vladaionescu.jpg"
~~~

All I want to do is find out before my blog starts if this file contains anything that will cause a runtime error. You know, catching problems without running the blog and hitting a code path that reads these values. It won't be an earth shattering improvement to the blog, but it will remove a little papercut of a problem.

To start with I'll create a description of what my author type looks like in a file called `authors-type.cue`:

~~~{.yml caption="authors-type.cue"}
#Author : {
    name   : string
    bio    : string 
    avatar : string
}
~~~

Types in Cuelang start with `#` and look like a struct or class definition. Here I'm saying an `#Author` type has a name, bio and an avatar, all of which are strings.

Next I need to tell `cue` that my yaml file, as the root level, is going to be a map with string keys, and `#Author` values. Doing so is pretty simple:

~~~{.yml caption="authors-type.cue"}
[string] : #Author
~~~

Then I can use the `cue` command-line tool to validate my author file, but first let's install it.

<div class="notice--info">

### Installing Cue

To install Cuelang, run `brew install cue-lang/tap/cue` on a mac, or download a release directly from [GitHub](https://github.com/cue-lang/cue/releases).

</div>

## YAML Validate

Now that I have the `cue` command installed I can vet my `authors.yml` like this:

~~~{.bash caption=">_"}
$ cue vet authors-type.cue authors.yml
~~~

~~~{.bash caption="Output"}
Alex.avatar: incomplete value string:
    ./authors-type.cue:6:14
~~~

As you can see, I'm missing an avatar value for Alex. I'll add that:

~~~{.diff caption="authors.yml"}
Alex:
    name    : "Alex Couture-Beil"
    bio     : "Alex enjoys writing code, growing vegetables, and the great outdoors."
+    avatar  : "/assets/images/authors/alexcouturebeil.jpg"
~~~

And now everything passes.

~~~{.bash caption=">_"}
$ cue vet authors-type.cue authors.yml
~~~

That's a small win for Cue, but it shows how static typing can be valuable.

<div class="notice--big--primary">

## What Did I Learn?

Cuelang can be used to specify a schema for a plain YAML file. You can put your types in a seperate file and run `cue vet types.cue plain.yml` and start benefiting from static types right away.

To specify a Type, the convention is to with a `#` like this:

~~~{.bash caption=">_"}
#Point: {
    x: number
    y: number
}
~~~

</div>

## Optional Fields

The `authors.yml` snippet I've shown so far is a bit simplified. I also have links optionally attached authors. It looks like this:

~~~{.yml caption="authors.yml"}
Adam:
    name    : "Adam Gordon Bell"
    bio     : "Spreading the word about Earthly. Host of CoRecursive podcast. Physical Embodiment of Cunningham's Law"
    avatar  : "/assets/images/authors/adamgordonbell.png"
    links:
        - label: ""
          icon: "fab fa-fw fa-twitter-square" 
          url: "https://twitter.com/adamgordonbell"
        - label: ""
          icon: "fas fa-fw fa-envelope-square"
          url: "mailto:adam+website@earthly.dev"
~~~

That is not described in our cue type, so now validation fails:

~~~{.bash caption=">_"}
$ cue vet authors-type.cue authors.yml
~~~

~~~{.bash caption="Output"}
Adam: field not allowed: links:
    ./authors-type.cue:3:11
    ./authors-type.cue:9:12
    ./authors2.yml:17:6
~~~

So to add links to my `#Author` type I first create a type of links:

~~~{.yml caption="authors-type.cue"}
#Link : {
    label: string
    icon: string
    url: string
}
~~~

Then I add it to `#Authors` as optional (using `?` marks it as optional):

~~~{.yml caption="authors-type.cue"}
#Author : {
    name   : string
    bio    : string 
    avatar : string
    links?: [...#Link]
}

~~~

Then running vet finds no errors.

~~~{.bash caption=">_"}
$ cue vet authors-type.cue authors.yml
~~~

I found it a little strange at first: `cue vet` complains when I add properties to a field but Cuelang Types are by default `closed`, and don't allow for extending. But that's just a default, if I want to skip adding links to my type I can easily mark the type as open (using `...`) and get around the errors.

~~~{.yml caption="authors-type.cue"}
#Author : {
    name   : string
    bio    : string 
    avatar : string
    ... //Type is open
}

[string] : #Author
~~~

It's also possible to define links as optional but leave its type unspecified:

~~~{.yml caption="authors-type.cue"}
#Author : {
    name   : string
    bio    : string 
    avatar : string
    links?: [...]
}
~~~

This would be less open then the full open solution, but less constrained than the full typed solution.

By adding these types, but leaving ways to leave the types open, Cuelang is behaving a bit like TypeScript. It improves upon YAML, but it tries to meet YAML where its at, and provides some escape hatches like open types.

The other way Cuelang is like TypeScript is that it does things with the type systems that are a little unusual. Which brings me to constraints.

<div class="notice--big--primary">

## What Did I Learn?

- Optional fields can be specified be ending their name with `?`. For example `tip?: number` would be an optional value.
- Lists can be be specified without a type `list: [...]` or with a type `strings: [...string]`.
- Types are closed by default. Adding new elements to them is a type error.
- Types can be opened by ending the definition with `...`.

Putting that all together you can write something like this:

~~~{.yml caption=""}
#MyOpenType: {
  tip?: number
  list: [...]
  strings: [...strings]
  ...
}
~~~

To specify a Type, the convention is to with a `#` like this:

~~~{.bash caption=">_"}
#Point: {
    x: number
    y: number
}
~~~

</div>

## Constraints

The layout on this blog has a limited space for bios. If an author's bio is longer than 250 characters then it will still fit, but it won't look great.

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/8210.png --alt {{  }} %}
<figcaption>No one should have to read about me in latin.</figcaption>

I can ensure that never happens like this:

~~~{.yml caption="authors-type.cue"}
#Author : {
    name   : string
    bio    : string 
    bio   : =~ "^.{1,250}$" //Max 250 length regex
    avatar : string
    links?: [...#Link]
}
~~~

What I've done here is add a constraint to the `#Author` type using a regex. You can constrain the type of strings using a regex! That is pretty cool and any regex can be attached to any string type. Granted, a regex is a bit of an odd way to verify a string length. Let fix that.

CueLang has a standard library which can be used for creating constraints. If I import the strings module, I can ensure the number of unicode runes in my string bio never gets over two fifty like this:

~~~{.yml caption="authors-type.cue"}
import "strings"

#Author : {
    name   : string
    bio    : string 
    bio   : strings.MaxRunes(250)
}
~~~

And get errors like this:

~~~{.bash caption=">_"}
$ cue vet authors-type.cue authors.yml
~~~

~~~{.bash caption=""}
Adam.bio: invalid value 
"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla eu dolor nec nisi scelerisque semper..." 
(does not satisfy strings.MaxRunes(250)):
~~~

The Cuelang standard library has [many other](https://pkg.go.dev/cuelang.org/go@v0.4.3/pkg) functions for constraining types. I beleive that any function that returns a bool can be used for this purpose and you can write your own functions in Golang. In this way constraints in CueLang are like [Refinement Types](https://en.wikipedia.org/wiki/Refinement_type).

The number of potential invariants you could enforce in this way is immense. I could parse the links to ensure they are valid links. I could enforce that `avatar` string always ended in `.png` and so on. However, I think for this simple author list this is enough validation.

<div class="notice--big--primary">

## What I Learned

Cuelang lets you constrain your values by adding constraints to the types. There are built in constraints that let enforce ranges and ensure strings match or don't match regular expressions like this:

~~~{.bash caption=">_"}
#Person: {
    age:   >=0 & <=100
    phone:  =~ "[0-9]+" 

}
~~~

And you can also import constraints from the [standard library](https://pkg.go.dev/cuelang.org/go/pkg@v0.4.3):

~~~{.yml caption=""}
import "list"

#Author : {
    parents   : list.isSortedStrings()
    pets      : list.MaxItems(3)
}
~~~

</div>

## Packages and Imports

The `author.yaml` file I've been using as an example came with [our blog theme](https://github.com/mmistakes/minimal-mistakes/blob/master/test/_data/authors.yml) and it's pretty simple to understand what each field is for. But we could do better than this right? If instead of using YAML for config, the theme used CueLang directly, then they could have shipped it with the author type we specified above and the configuration would be typed and validated without any effort on my part.

That might work something like this. The minimal mistakes theme could put this cue file up on github:

~~~{.bash caption="github.com/mmistakes/minimal-mistakes/blog"}
package blog

import "strings"

#Link : {
    label: string
    icon: string
    url: string
}

#Author : {
    name   : string
    bio    : string 
    bio   : strings.MaxRunes(250)
    avatar : string
    links?: [...#Link]
}

~~~

Then I could convert my YAML file to cue:

~~~{.bash caption=">_"}
$ cue import authors.yaml
~~~

Which would give me something like this:

~~~{.json caption="authors.cue"}

Corey: {
 name:   "Corey Larson"
 bio:    "Eats, runs, and codes. Dad. Engineer. Progressive. LDS. Disneyland fanatic."
 avatar: "/assets/images/authors/coreylarson.jpg"
}
Alex:  {
 name:   "Alex Couture-Beil"
 bio:    "Alex enjoys writing code, growing vegetables, and the great outdoors."
 avatar: "/assets/images/authors/vladaionescu.jpg"
}
Vlad: {
 name:   "Vlad A. Ionescu"
 bio:    " Founder of Earthly. Founder of ShiftLeft. Ex Google. Ex VMware. Co-author RabbitMQ Erlang Client."
 avatar: "/assets/images/authors/vladaionescu.jpg"
}
Adam:  {
 name:   "Adam Gordon Bell"
 bio:    "Spreading the word about Earthly. Host of CoRecursive podcast. Physical Embodiment of Cunningham's Law"
 avatar: "/assets/images/authors/adamgordonbell.png"
 links: [
  {
   label: ""
   icon:  "fab fa-fw fa-twitter-square"
   url:   "https://twitter.com/adamgordonbell"
  }, {
   label: ""
   icon:  "fas fa-fw fa-envelope-square"
   url:   "mailto:adam+website@earthly.dev"
  }, {
   label: ""
   icon:  "fas fa-fw fa-link"
   url:   "https://corecursive.com"
  },
 ]
}
~~~

And then I can import blog.#Authors type and use it to annotate my CUE like so:

~~~{.json caption="authors.cue"}
import (
 "github.com/mmistakes/minimal-mistakes/blog"
)

Corey: blog.#Author & {
 name:   "Corey Larson"
 bio:    "Eats, runs, and codes. Dad. Engineer. Progressive. LDS. Disneyland fanatic."
 avatar: "/assets/images/authors/coreylarson.jpg"
}
Alex: blog.#Author & {
 name:   "Alex Couture-Beil"
 bio:    "Alex enjoys writing code, growing vegetables, and the great outdoors."
 avatar: "/assets/images/authors/vladaionescu.jpg"
}
Vlad: blog.#Author & {
 name:   "Vlad A. Ionescu"
 bio:    " Founder of Earthly. Founder of ShiftLeft. Ex Google. Ex VMware. Co-author RabbitMQ Erlang Client."
 avatar: "/assets/images/authors/vladaionescu.jpg"
}
Adam: blog.#Author & {
 name:   "Adam Gordon Bell"
 bio:    "Spreading the word about Earthly. Host of CoRecursive podcast. Physical Embodiment of Cunningham's Law"
 avatar: "/assets/images/authors/adamgordonbell.png"
 links: [
  {
   label: ""
   icon:  "fab fa-fw fa-twitter-square"
   url:   "https://twitter.com/adamgordonbell"
  }, {
   label: ""
   icon:  "fas fa-fw fa-envelope-square"
   url:   "mailto:adam+website@earthly.dev"
  }, {
   label: ""
   icon:  "fas fa-fw fa-link"
   url:   "https://corecursive.com"
  },
 ]
}
~~~

And I can now run `cue vet` without need for specifying the schema, or having to create the types myself:

~~~{.bash caption=">_"}
$ cue vet authors.cue
~~~

And I can be sure all my config data is structured properly.

Once you start to import types for configuration you need to write, especially for config heavy areas like Kubernetes, you can start to see why something like CueLang or its competitor Dhall can make a lot of sense.

(A great post the expands on this idea is [How CUE wins](https://blog.cedriccharly.com/post/20210523-how-cue-wins/) which makes a great case for why something like CUE is needed desperately needed.)

There is one problem though...

<div class="notice--big--primary">

## What Did I Learn?

Cue supports packages with the `package` keyword. You can split cue files up into packages. 

~~~{.yml caption="https://lib.io/lib1/lib1.cue"}
package lib1

#MyString : string
#MyNumber : number
~~~

Packages can be imported from the web.

~~~{.yml caption="myfile.cue"}
import "lib.io/lib1/lib1.cue"

n1 : lib1.#MyNumber
s1 : lib1.#MyString
~~~

It all works very much like golang packages.

</div>

## Back To YAML

Having type checking for YAML sounds great. And CueLang has lots more features for improving configuration. But I have a problem. I want types and constraints for my blog config, but how much incentive do the Jekyll theme authors have to provide them? Not much because not many Jekyll users are using Cue and that won't change because the types.  It's the chicken and the egg problem of type annotations.

TypeScript solved this with [DefinitelyTyped](https://github.com/DefinitelyTyped/DefinitelyTyped), a giant community driven efforts to source types for various JavaScript libraries. CueLang doesn't yet have a similar concept.

## Generating YAML

Another problem is that ideally I'd like my programming language to be able to read cue files directly. Only Golang supports this.

Nevertheless, much like TypeScript, as a suffiecently motivated users i can do an end run around these concerns, just the way I have here, by writing my own types and then using the cue cli tool to turn my cue back to yaml. ( And this is all I can really do with Jekyll since Jekyll is written in Ruby and has no support for cue so I need to convert back to YAML before running the blog. )

`cue` does support this:

~~~{.bash caption=">_"}
$ cue eval authors.cue > authors.yaml 
~~~

And so if I keep my types in `authors-type.cue` and my values in `authors.cue` and then generate `authors.yaml` in source using `cue eval` then I can ensure my YAML is always correct. I'll have to keep a cue copy of my config and YAML version and really I think that is too much to ask. 

I do look forward to the day when types and constraints spread throughout the configuration land but what I'm going to do for now is just keep my types in a `authors-type.cue` file and keep the authors list in yaml, validating things using the `cue vet {{types.cue}} {{file.yaml}}` approach. That way I still get some type checks but don't have to maintain two files.

<div class="notice--big--primary">

## What Did I Learn?

- Only Golang can read cue files. 😢
- `cue` can generate yaml or json with `cue eval` though. 😊
- But then I have to hold onto my config in two formats, or use `cue vet`. 😕
- But if more people use Cuelang, support will grow over time. 🤞

</div>

## Conclusion

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/3180.png --alt {{  }} %}

That is a hopefully breezy introduction to the very basics of Cuelang. There is much more to learn but if you remember that it's a configuration format that uses types and constraints and packages to improve on YAML, then you've got the jist of it. After that you just have to draw the rest of the damn owl.

To that end [cuetorials.com](cuetorials.com) and [bitfieldconsulting](https://bitfieldconsulting.com/golang/cuelang-exciting) had the best online tutorials I was able to find.

(Just remember not to use configuration when a [programming language](/blog/intercal-yaml-and-other-horrible-programming-languages/) is what you need.)

And also if you are the type of person who thinks validating YAML is a worthly goal, you might also be the type of person who gets excited about new ways to make building software easier. If that is you, take a look at Earthly.

{% include cta/cta1.html %}
