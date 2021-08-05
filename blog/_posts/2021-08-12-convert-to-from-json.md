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
json to csv
 csv to json
 xml to json
 json to xml
 yaml to json
 json to yaml
 json to html
 html to json
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

## Convert CSV to Json Command Line

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



https://github.com/archan937/gawkjsonv.sh