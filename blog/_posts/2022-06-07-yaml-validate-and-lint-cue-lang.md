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

```




## See Also:
 * 