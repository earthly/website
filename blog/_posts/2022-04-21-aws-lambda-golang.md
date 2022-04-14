---
title: "Put Your Best Title Here"
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
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links to other articles
- [ ] Add Earthly `CTA` at bottom `{% include cta/cta1.html %}`
- [ ] Raise PR

## Intro

Last time, I built a Node.js lambda running in a container. Running a container on AWS serverless framework worked out really well. Being in a container meant it was easy for me to test locally and that I could install OS level dependencies and shell out and call them. That is how I was able to run Lynx in my lambda and build [TextMode].

So Lambda good, containers good, but node.js I'm less certina about. I'm not a JavaScript developer and I found working with promises confusing. TypeScript helped a lot but I still found it a bit of a confusing process. 

So today's mission is to port that Node.js code to GoLang, running a container. I'll also using OS dependencies in my container and because TextMode is a very cacheable service, I'll be using S3 to cache the results as well.

Or, to put it into terms that is probably more interesting for you the reader: Read this article to learn how to build a golang lambda service, hook it up to a REST API endpoint and get and put data to S3 from it.

## The Goal:

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5800.png --alt {{  }} %}
<figcaption>Here is what we will make.</figcaption>
</div>

Here is the plan, when I make a call like this:

~~~{.bash caption=">_"}
curl  https://earthly-tools.com/text-mode?url=https://www.lipsum.com/
~~~

It will hit the 1) API gateway, 2)Call my GoLang lambda function handler. My golang code will 3) pull the site from the web and 4) clean it up to look like a text document and return it to the user. Last we will tackle 5) adding some caching into the mix.

But the end-result is already up and running at [https://earthly-tools.com/text-mode](https://earthly-tools.com/text-mode) and will return something like this:  
```
What is Lorem Ipsum?

   Lorem Ipsum is simply dummy text of the printing and typesetting
   industry. Lorem Ipsum has been the industry's standard dummy text ever
   since the 1500s, when an unknown printer took a galley of type and
   scrambled it to make a type specimen book. It has survived not only
   five centuries, but also the leap into electronic typesetting,
   remaining essentially unchanged. It was popularised in the 1960s with
   the release of Letraset sheets containing Lorem Ipsum passages, and
   more recently with desktop publishing software like Aldus PageMaker
   including versions of Lorem Ipsum.
   ...
```
And all in ~150 lines of go code. So lets start with that.

## Go Code V1

When my Go Lambda is called via the lambda runtime, it will get a JSON event describing the request it recieved:

```
{
  "queryStringParameters": {
    "url": "https://www.lipsum.com/"
  }
}
```

And I'll return an even describing the document I'd like returned.

```

```