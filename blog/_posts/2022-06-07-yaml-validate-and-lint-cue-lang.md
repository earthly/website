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

Todo:

- add 'what did I learn'


### Writing Article Checklist

- [ ] Fix Grammarly Errors
- [ ] Read out loud
- [ ] Write 5 or more titles and pick the best on
- [ ] First two paragraphs: What's it about? Why listen to you?
- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links to other articles
- [ ] Add Earthly `CTA` at bottom `{% include cta/cta1.html %}`
- [ ] Raise PR

I've complained about using YAML as when a programming language would do before.  But actually, when you've got configuring to do, YAML is pretty useful: It's so much nicer to read and write than the XML a had to write back in the early days of Java development. But one advantage XML seemly had of YAML is that XML schema were commonly used and so I wouldn't get errors like the one I got today on this very blog:
```
Error parsing yaml file:
map values are not allowed here
  in "/Users/adam/sandbox/earthly-website/blog/authors.yml", line 2, column 8 
```

You see the blog is expecting a certain format of config, and I've violoated that expectation. The blog wants a string, and I've given it a map. If only we had XML Schema for YAML or even better a static type system for configuration.

It turns out such things do exist, there is [JSON Schema](https://json-schema.org/), [Dhall](https://dhall-lang.org/), and [Cuelang](https://cuelang.org/)[^1]. I'll save covering Dhall, and JSON Schema for another day. Today I'm going to show you how to use Cuelang, which is both an extension of YAML and command line tool, to validate your YAML. And I"m going to attempt to use it to prevent future problems with this blogs `authors.yml` file.

[^1]: I'll be referring to Cue as Cuelang in this article, and the command line tool as `cue`. Cue is a bit hard to search for in google, so perhaps I can start the trend of following GoLang's naming convention.

## Beginning

The Authors are this blog are stored in a yaml file aptly named authors.yaml. It looks like this:

```
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
```

All I want to do is find out before my blog starts if this file contains anything that will cause a runtime error. You know, catching problems without running the blog and hitting a code path that reads these values. It won't be an earth shattering improvement to the blog, but it will remove a little papercut of a problem.

To start with I'll create a description of what my author type looks like in a file called `authors-type.cue`:

```
#Author : {
    name   : string
    bio    : string 
    avatar : string
}
```

Types in Cuelang start with '#' and look like a struct or class definition. Here I'm saying an `#Author` type has a name, bio and an avatar, all of which are strings.

Next I need to tell `cue` that my yaml file, as the root level, is going to be a map with string keys, and `#Author` values. Doing so is pretty simple:

```
[string] : #Author
```

Then I can use the `cue` command-line tool to validate my author file.

<div class="notice--info">

### Install CUE

To install Cuelang, run `brew install cue-lang/tap/cue` on a mac, or download a release directly from [GitHub](https://github.com/cue-lang/cue/releases).

</div>

## YAML Validate

Now that I have the `cue` command installed I can vet my `authors.yml` like this:
```
$ cue vet authors-type.cue authors.yml
```
```
Alex.avatar: incomplete value string:
    ./authors-type.cue:6:14
```

As you can see, I'm missing an avatar value for Alex. I'll add that: 
```
Alex:
    name    : "Alex Couture-Beil"
    bio     : "Alex enjoys writing code, growing vegetables, and the great outdoors."
+    avatar  : "/assets/images/authors/alexcouturebeil.jpg"
```

And now everything passes.

```
$ cue vet authors-type.cue authors.yml
```

<div class="notice--success notice--big">

## What did I learn?

Use vet bla bla bla
</div>


## Optional Fields

I also want to optionally attach links to authors in `authors.yaml`. It will look like this:

```
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
```
The problem is this is not described in our cue type, so now validation fails:

```
Adam: field not allowed: links:
    ./authors-type.cue:3:11
    ./authors-type.cue:9:12
    ./authors2.yml:17:6
```

To add links to my `#Author` type I first create a type of links:
```
#Link : {
    label: string
    icon: string
    url: string
}
```
Then I add it to `#Authors` as optional (using `?` marks it as optional):
```
#Author : {
    name   : string
    bio    : string 
    avatar : string
    links?: [...#Link]
}

```
Then running vet finds no errors. 

```
$ cue vet authors-type.cue authors.yml
```

I found it a little strange at first that CUELang complains when I add properties to a field but CueLang Types are by default closed, and don't allow  additional fields by default. But that's just a default, if I want to skip adding links to my type I could easily mark the type as open (using `...`) and get around the errors.

```
#Author : {
    name   : string
    bio    : string 
    avatar : string
    ... //Type is open
}

[string] : #Author
```

It's also possible to define links as optional but leave its type unspecified: 

```
#Author : {
    name   : string
    bio    : string 
    avatar : string
    links?: [...]
}
```

This would be less open then the full open solution, but less constrained than the full typed solution.

By adding these types, but leaving ways to leave the types open, CueLang is behaving a bit like TypeScript. It improves upon YAML, but it tries to meet YAML where its at, and provides some escape hatches like open types.

The other way CueLang is like TypeScript is that it does things with the type systems that are a little unusual. Which brings me to constraints.

## Constraints

The layout on this blog has a limited space for bios. If an author's bio is longer than 250 characters then that's going to be a problem. I can ensure that never happens like this:

```
#Author : {
    name   : string
    bio    : string 
    bio   : =~ "^.{1,250}$" //Max 250 length regex
    avatar : string
    links?: [...#Link]
}
```

What I've done here is add a constraint to the Author Type, which is specified with a regex. That is pretty simple way to constrain a type if you ask me. Any regex can be attached to any string type. Granted, a regex is a bit of an odd way to verify a string length. Let fix that.

CueLang has a standard library which can be used for creating constraints. If I import the strings function, I can check the number of unicode runes in my types like this:

```
import "strings"

#Author : {
    name   : string
    bio    : string 
    bio   : strings.MaxRunes(250)
}

```

And get errors like this:

```
Vlad.bio: invalid value " Founder of Earthly. Founder of ShiftLeft. Ex Google. Ex VMware. Co-author RabbitMQ Erlang Client." (does not satisfy strings.MaxRunes(250)):
```

The CueLang standard library has [many other](https://pkg.go.dev/cuelang.org/go@v0.4.3/pkg) functions for constraining types. I beleive that any function that returns a bool can be used for this purpose and you can write your own functions in Golang. In this way constraints in CueLang are like [Refinement Types](https://en.wikipedia.org/wiki/Refinement_type).

The invariants you can enforce in this way are limitless. I could parse the links to ensure they are valide links. I could validate `avatar` ended in `.png` and so on. However, I think for this simple author list this is enough validation.

<div class="notice--success notice--big">

## What I Learned

constraints and stuff
</div>

## Packages and Imports

The `author.yaml` file I've been using as an example came with [our blog theme](https://github.com/mmistakes/minimal-mistakes/blob/master/test/_data/authors.yml) and it's pretty simple to understand what each field is for. But we could do better than this right? If instead of using YAML for config the theme used CueLang directly, then they could have shipped it with the author type we specified above and the configuration would be typed and validated.

That might work something like this. The minimal mistakes theme could put this cue file up on github:

github.com/mmistakes/minimal-mistakes/blog
```
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

```

Then I could convert my YAML file to cue:
```
$ cue import authors.yaml
```

Which would give me something like this:
```

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
```

And then I can import blog.#Authors type and use it to annotate my CUE like so:

```
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
```

And I can now run `cue vet` without need for specifying the schema, or having to create the types myself:
```
$ cue vet authors.cue
```

And I can be sure all my config data is structured properly. 

Once you start to import types for configuration you need to write, especially for config heavy areas like Kuberenetes, you can start to see why something like CueLang or its competitor Dhall can make a lot of sense.

There is one problem though...

## Back To YAML

Having type checking for YAML sounds great. And CueLang has lots more features for improving configuration. But they have a problem. I want types and constraints for my blog config, but what incentive do the Jekyll theme authors have to provide them? Not many Jekyll users are using Cue and that won't change because the types don't exist for the things they need to configure. It's the chicken and the egg problem of Type annotations.

TypeScript solved this with [DefinitelyTyped](https://github.com/DefinitelyTyped/DefinitelyTyped), a giant community driven efforts to source types for variosu javascript libraries. CueLang doesn't yet have a similar concept.

Another problem is that ideally I'd like my programming langauge to be able to read cue files directly and so far with CUE I can only read cue configuration files from Golang.

Nevertheless, much like TypeScript, as a suffiecently motivated users i can do an end run around these concerns, just the way I have here, by writing my own types and then using the cue cli tool to my cue back to yaml. And this is all I can really do with Jekyll since Jekyll is written in Ruby and has no support for cue. I need to convert back to YAML before running the blog.

```
$ cue eval authors.cue > authors.yaml 
```

And so if I keep both `authors.cue` and `authors.yaml` in source, and treat `authors.cue` as the source of truth and always run `cue eval` after I make changes then I can ensure my YAML is always correct. I do look forward to the day when types and constraints spread throughout the configuration land but probably what I'm going to do for now is just keep my types in a `cue` file and keep the authors list in yaml, validating things using the `cue vet {{types.cue}} {{file.yaml}}` approach.

<div class="notice--success notice--big">

## What did I learn?
 - optional parameters
 - open vs closed types

</div>

## Conclusion

That is a breezy introduction to the very basics of Cuelang. There is much more to learn but if you remember that it's a configuration format that uses types and constraints and packages to improve on YAML, then you'll have the jist of it. After that you just have to draw the rest of the damn owl.

To that end [cuetorials.com](cuetorials.com) was the best online resource I was able to find and [How CUE wins](https://blog.cedriccharly.com/post/20210523-how-cue-wins/) makes a great case for why something like CUE is needed and is hopefully the future. 

(Just remember not to use configuration when a programming language is what you need.)

{% include cta/cta1.html %}