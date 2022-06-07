---
title: "YAML Validate and Lint with CUE Lang"
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - cue lang
 - yaml lint
 - yaml validate
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
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links to other articles
- [ ] Add Earthly `CTA` at bottom `{% include cta/cta1.html %}`
- [ ] Raise PR

YAML is useful as a configuration langauge. It's so much nicer to read and write than XML, but also it so many quirks. Did you know that a boolean value in YAML has 22 valid values? Well, its true. Here is the regex for determining if a value is a boolean in YAML:

```
 y|Y|yes|Yes|YES|n|N|no|No|NO
|true|True|TRUE|false|False|FALSE
|on|On|ON|off|Off|OFF
```
<figcaption>Is YAML typing too flexible? ON. Can we improve on it? True</figcaption>

So today I'm going to show you how to use CUE, which is both an extension of YAML and command line tool, to validate your YAML.

## Beginning

Authors are this blog are stored in a yaml file aptly named authors.yaml. It looks like this:

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

To validate this I could use JSON Schema or probably a variatey of other tools, but Cue Langauge does have some nice properties. To start with I will create a description of what my author type looks like.

```
#Author : {
    name   : string
    bio    : string 
    avatar : string
}
```

Types in Cue start with '#' and describe the shape and the datatypes of the data. Here I am saying an author Type has a name, bio and an avatar. All of which are strings.

Next I need to tell cue that my yaml file is going to be a map with string keys, and `#Author` values. Doing so is pretty simple:

```
[string] : #Author
```

Then I can use the cue commandline tool to validate my author file.

<div class="notice">

### Install CUE

To install cuelang, run `brew install cue-lang/tap/cue` on a mac, or download a release directly from [GitHub](https://github.com/cue-lang/cue/releases).

</div>

## Cue Vet

Now that I have the cue command install I can vet my authors.yml like this:
```
$ cue vet authors-template.cue authors.yml
```
```
Alex.avatar: incomplete value string:
    ./authors-template.cue:6:14
```

As you can see I'm missing an avatar picture path for Alex. I'll add that. 
```
Alex:
    name    : "Alex Couture-Beil"
    bio     : "Alex enjoys writing code, growing vegetables, and the great outdoors."
+    avatar  : "/assets/images/authors/alexcouturebeil.jpg"
```

And now everything passes.

## What did I learn?
Use vet bla bla bla


## Optional Fields

I also want to optionally let blog writers define some links to where else they can be found online. It will work like this:

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

And it will look like this:
...

The problem is this is not described in our cue type:

```
Adam: field not allowed: links:
    ./authors-template.cue:3:11
    ./authors-template.cue:9:12
    ./authors2.yml:17:6
```

First I create a type of links:
```
#Link : {
    label: string
    icon: string
    url: string
}
```
Then I add it to `#Authors` as optional:
```
#Author : {
    name   : string
    bio    : string 
    avatar : string
    links?: [...#Link]
}

```
Then running vet finds no errors. 

I found it a little strange at first that CUELang flags errors when you add properties to a field – YAML extends JSON, and in Javascript, everything is a prototype and you need to add things to things ...

CueLang Types are by default closed, and don't allow this addition but that's just a default. If I wanted to skip adding links to my type I could easily mark the type as open and get around the errors.

```
#Author : {
    name   : string
    bio    : string 
    avatar : string
    ... //Type is open
}

[string] : #Author
```

It's also possible to define links as optional but not its type:

```
#Author : {
    name   : string
    bio    : string 
    avatar : string
    links?: [...]
}
```

This would be less open then the full open solution, but less constrained than the full typed solution.

In this way, CueLang is a big like TypeScript, it wants to improve upon YAML, but in doing so it tries to meet YAML where its at, and expects to have occasionaly use of escape hatches like open types.

The other way CueLang is like TypeScript is that it does things with the type system that are not seen often seen outside of academic PL papers. Which brings us to constraints.

## Constraints

The layout on our blog has a limited space for bios. If an author's bio is longer than 250 characters then that's going to be a problem. I can ensure that never happens like this:

```
#Author : {
    name   : string
    bio    : string 
    bio   : =~ "^.{1,250}$" //Max 250 length regex
    avatar : string
    links?: [...#Link]
}
```
What I've done here is add a constraint to the Author Type, which is specified with a regex. The regex is a bit of an odd way to verify a string length. But thankfully CueLang has other ways to do it.


If I import from the CueLang standard Library I can run functions in my types like this:

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
lad.bio: invalid value " Founder of Earthly. Founder of ShiftLeft. Ex Google. Ex VMware. Co-author RabbitMQ Erlang Client." (does not satisfy strings.MaxRunes(250)):
```

The CueLang standard library has [many other](https://pkg.go.dev/cuelang.org/go@v0.4.3/pkg) functions for constraining YAML Types in fact any function that returns a bool can be used for this purpose. In this way constraints in CueLang are much like [Refinement Types](https://en.wikipedia.org/wiki/Refinement_type) .

I could use them to continue validating my types – Links could be parsed with a regex to ensure they are of proper format; `avatar` could be checked to make sure it ends in `.png` – however, I think for this simple author list this is enough validation.


## What I learned

constraints and stuff

## Packages and Imports

The author.yaml file I've been using as an example came with [our blog theme](https://github.com/mmistakes/minimal-mistakes/blob/master/test/_data/authors.yml) and I think it's pretty easy to understand what each field is for. But we could do better than this right? If instead of using YAML for config the theme used CueLang, they could have shipped it with the author type we specified above and the configuration would be typed and validated.

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

And I can now run `cue vet` without need for specifying the schema:
```
$ cue vet authors.cue
```
And I can be sure all my config data is structured properly. The imports and packages don't seem to be extensively explained inthe Cue documentation but if you assume they work like go imports and modules you won't be led astray. 

Once you start to import types for configuration you need to write, especially for config heavy areas like Kuberenetes, you can start to see why something like CueLang or its competitor Dhall can make a lot of sense.

There is one problem though. 


## Back To YAML

Having type checking for YAML sounds great. And CueLang ( and competitor Dhall) have lots more features to make configuration easier to work with but they havea problem. It's the chicken and the egg problem or the two sided marketplace. I want types and constraints for my blog config, but what incentive do the Jekyll theme authors have to provide them? No one is Cue and no one will use it because the types don't exist for the things they need to configure. 

TypeScript solved this with [DefinitelyTyped](https://github.com/DefinitelyTyped/DefinitelyTyped), a giant community driven efforts to source types for variosu javascript libraries. CueLang as far as I know doesn't have a similar concept.

Another problem is that ideally I'd like my programming langauge to be able to read files cue files directly and so far with CUE I can only read cue configuration files from golang.

Nevertheless, much like TypeScript, as a suffiecently motivated users i can do an end run around these concerns, just the way I have here, by writing my own types and then using the cue cli tool to my cue back to yaml. And this is all I can really do with Jekyll since its written in Ruby and has no support for cue. I need to convert back to YAML before running the blog.

```
$ cue eval authors.cue > authors.yaml 
```

And so if I keep both `authors.cue` and `authors.yaml` in source, and treat `authors.cue` as the source of truth and always run `cue eval` after I make changes then I can ensure my YAMl is always correct.  I do look forward to the day when types and constraints spread throughout the configuration land but probably what I'm going to do is just keep my types in a `cue` file and keep the authors list in yaml, validating things using the `cue vet {{types.cue}} {{file.yaml}}` approach.

## What did I learn?
 - optional parameters
 - open vs closed types

## 

## See Also:
 * https://cuelang.org/
 * https://cuetorials.com/

