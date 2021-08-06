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

## Converting to Comma-Separated Values
The details behind Comma-separated values (CSV) file parsing and conversion is trickier than it may seem at first glance. The idea is simple: you have a fixed number of fields per row and each is field is serpated by a comma.

```
1997,Ford,E350\n
```
If you need to use commas in the format, then the fields must be delimited with `"`:
```
1997,Ford,E350,"Super, luxurious truck"\n
```
You can use this same trick to delimit a line break and use double double-quotes to add use delimiters
```
1997,Ford,E350,"Go get one ""now""\n
they are going fast"\n
```

Things get more complex from there and even the (RFC standard)[https://datatracker.ietf.org/doc/html/rfc4180] does not specify all the edge cases. From this we can conclude one thing: Although the format seems simple, you probably want to use an existing tool if you are converting json to CSV because the edge cases are a bit more involved then you might think.

Wikipedia puts it this way:

> The CSV file format is not fully standardized. Separating fields with commas is the foundation, but commas in the data or embedded line breaks have to be handled specially. Some implementations disallow such content while others surround the field with quotation marks, which yet again creates the need for escaping these if they are present in the data.

With that in mind, lets review some tools for converting from JSON to CSV at the command line.

## Convert JSON to CSV via the Command Line
The simplest way to do this JSON to CSV conversion is with `dasel`. `dasel` is a tool for DAta SELection. Think of it as a `jq` that supports selection on formats besides just JSON. 

It's easy to install (`brew install dasel`) and it works great as a format converter.

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

```
dasel -r json -w csv < sample.json 
color,id,value
red,1,#f00
green,2,#0f0
blue,3,#00f
```
`dasel` handles newlines and comma values as well. 

#todo example

dasel -r json -w csv "{"name,,,":"lines\n\nlines"}"

Install 

## Convert JSON to CSV via the Command Line using JQ

If you don't want to install `dasel` or if you just love `JQ`  (`brew install jq`) then this solution may work well for you. Before I discovered `dasel` this was the main approach I used.

```
cat simple.json| jq -r '(map(keys) | add | unique) as $cols | map(. as $row | $cols | map($row[.])) as $rows | $cols, $rows[] | @csv' 
"color","id","value"
"red",1,"#f00"
"green",2,"#0f0"
"blue",3,"#00f"
```


## Convert JSON to CSV via the Command Line and Choose Ordering Column

The down side to the previous two approaches is that the order of the columns not preserved and it's not simple to specify which columns to include. Both `jq` and `dazel` support a query langauge which is capable of handling such rules but the `jsonv` tool is an easy way to accomplish this without learning a query langauge. 

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
gawk can be installed like using brew (`brew install gawk`) or your package manager of choice.

## Convert CSV to JSON at The Command Line 
For converting CSV to JSON we can use `daser` again. The read (`-r`) and write (`-w`) options mean its easy to convert from any of its supported file formats (JSON, YAML, TOML, XML and CSV).

We can get our original JSON document back from CSV like this:
``` bash
$ cat sample.csv
ID, color, value
1,"red","#f00"
2,"green","#0f0"
3,"blue","#00f"
```

``` json
$ dasel -r csv -w json < sample.csv
{
  "ID": "1",
  "color": "red",
  "value": "#f00"
}
{
  "ID": "2",
  "color": "green",
  "value": "#0f0"
}
{
  "ID": "3",
  "color": "blue",
  "value": "#00f"
}
```


## Convert CSV to JSON Command Line with `csvtojson`
Another option is to grab the npm tool `csvtojson` (`npm i --save csvtojson`). To convert just sent csvtojson results over standard in:
```
csvtojson < sample.csv
[
{"ID":"1","color":"red","value":"#f00"},
{"ID":"2","color":"green","value":"#0f0"},
{"ID":"3","color":"blue","value":"#00f"}
]
```

## Conclusion

You now have the knowledge and the tools you need to convert JSON to CSV and CSV to JSON. [`jq`](https://stedolan.github.io/jq/), [`dasel`](https://github.com/TomWright/dasel), [`csvtojson`](https://www.npmjs.com/package/csvtojson) and [`jsonv`](https://github.com/archan937/jsonv.sh) are handy command line tools. 

{% include cta/cta1.html %}