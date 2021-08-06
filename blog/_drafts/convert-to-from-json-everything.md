---
title: "Json Convert"
categories:
  - Tutorials
toc: true
author: Aniket Bhattacharyea

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

## Keywords
json to csv -> dasel
 csv to json -> dasel
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


## Convert JSON to CSV via the Command Line
The easiest way to convert JSON to CSV is using JSONV. Here is a simple JSON file. Lets do a JSON to CSV conversion.

``` json
[
	{
        "id"   : 1,    
		"color": "red",
		"value": "#f00"
	},
	{
        "id"   : 2,  
		"color": "green",
		"value": "#0f0"
	},
	{
        "id"   : 3,  
		"color": "blue",
		"value": "#00f"

	}
]
```
<figcaption>sample.json</figcaption>

To convert we will use `jsonv` and pipe it our json file. It also takes a list of columns to include and by default outputs the csv file to standard out. We redirect this output to a file.
```
cat simple.json | jsonv id,color,value > simple.csv
```
This gives us a simple CSV file:

```
$ cat simple.csv
1,"red","#f00"
2,"green","#0f0"
3,"blue","#00f"
4,"cyan","#0ff"
5,"magenta","#f0f"
6,"yellow","#ff0"
7,"black","#000"
```
jsonv handles more complex examples as well. Under the hood it uses gnuawk (`gawk`). It can be installed like this:
```
$ curl -Ls https://raw.github.com/archan937/jsonv.sh/master/install.sh | bash
```
gawk can be installed like using brew (`brew install gawk`) or your package manager of choice. `jsonv` has no option for adding headings to the resulting file. For my own one of usage this has never been a problem as its easy to add in the heading row manually. However if you need an automated way to add the heading then `JQ` can do an excellant job of this.

```
cat simple.json| jq -r '(map(keys) | add | unique) as $cols | map(. as $row | $cols | map($row[.])) as $rows | $cols, $rows[] | @csv' 
"color","id","value"
"red",1,"#f00"
"green",2,"#0f0"
"blue",3,"#00f"
```
The other advantage of this JQ approach is that you don't need to specify the columns you need. The down side is to specify the ordering with JQ a different approach is needed. Understanding the JQ solution is beyond the scope of this article. 

## Convert CSV to JSON Command Line

Converting from CSV to Json is very simple with the right conversion tool and `csvtojson` is just that tool. It requires a header line in the CSV file for determining the keys of the resulting JSON document. 

```
$ cat sample.csv
ID, color, value
1,"red","#f00"
2,"green","#0f0"
3,"blue","#00f"
```

To convert just sent csvtojson results over standard in:
```
csvtojson < sample.csv
[
{"ID":"1","color":"red","value":"#f00"},
{"ID":"2","color":"green","value":"#0f0"},
{"ID":"3","color":"blue","value":"#00f"}
]
```

Install it via npm:
```
npm i --save csvtojson

```

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
what can you do taking everything to JSON?
Can you do CSS style selectors on json?

Articles:
https://kevinmarsh.com/2014/11/12/web-scraping-with-pup-and-jq.html
https://datascienceworkshops.com/blog/seven-command-line-tools-for-data-science/
https://www.reddit.com/r/commandline/comments/cq5n4c/jq_for_htmlxml/
