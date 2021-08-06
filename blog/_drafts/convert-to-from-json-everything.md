---
title: "Json Convert"
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
- [ ] Run mark down linter (`earthly +blog-lint-apply`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `earthly --build-arg NAME=2020-09-10-better-builds.md +link-opportunity` and find 1-5 places to incorporate links to other articles
- [ ] Raise PR

https://github.com/johnkerl/miller
https://elv.sh/learn/unique-semantics.html


## Keywords
 xml to json -> dasel
 json to xml 
 yaml to json -> dasel
 json to yaml -> dasel
 json to html 
 html to json -> tidy?
 xsd to json schema
xml scheme to json schema
 docx to json 
 xslx to json
 json to excel
bson to json
json to bson
 json to pdf
 pdf to json
 wsdl to json 
Also mention:
- dump 
- conversion
- tool
- convert
- command line
- windows
- linux

## Convert XML to JSON
To convert from an XML document to JSON there are a couple tools to choose from. `xq` which comes with [`yq`](https://github.com/kislyuk/yq) is the most actively supported.  

Install
```
pip3 install yq
```

In the XML standard ordering of elements is defined and duplicate elements are supported. Neither of these is true of JSON so if you plan to convert back at some point be aware that you may lose ordering and duplicate values.

```
cat sample01.xml
<note>
<to>Tove</to>
<from>Jani</from>
<heading>Reminder</heading>
<body>Don't forget me this weekend!</body>
</note> 
```
<figcaption>A sample xml document</figcaption>

`xq` is a wrapper around `jq` that converts to XML. To use `xq` as a conversion tool just call it as `xq .`:

``` json
$ xq . < sample.xml
{
  "note": {
    "to": "Tove",
    "from": "Jani",
    "heading": "Reminder",
    "body": "Don't forget me this weekend!"
  }
}
```

## Convert JSON to XML
➜  downloads git:(master) ./jsontoxml-cli-darwin-amd64 < /Users/adam/sandbox/earthly-website/blog/assets/other/convert-to-from-json/simple.json
<root><element><color>red</color><id>1</id><value>#f00</value></element><element><color>green</color><id>2</id><value>#0f0</value></element><element><color>blue</color><id>3</id><value>#00f</value></element></root>


https://github.com/chrismalek/jsontoxml-cli

##  html to json -> tidy?

install pup
```
brew install pup
```

curl https://earthly.dev/blog/ | pup '.archive__item-title' > test2.html

Ideas:
what can you do by taking everything to JSON?
Can you do CSS style selectors on json and then back to other formats?

Articles:
https://kevinmarsh.com/2014/11/12/web-scraping-with-pup-and-jq.html
https://datascienceworkshops.com/blog/seven-command-line-tools-for-data-science/
https://www.reddit.com/r/commandline/comments/cq5n4c/jq_for_htmlxml/
