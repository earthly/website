---
title: "How to Convert from JSON to CSV at The Command Line"
author: Adam
internal-links:
 - csv
 - json to csv
 - csv to json
 - json
 - convertion tool
topic: cli
excerpt: |
    Learn how to convert JSON to CSV and vice versa at the command line using tools like `dasel`, `jq`, `jsonv`, and `csvtojson`. These handy command line tools make the conversion process easy and efficient, allowing you to handle edge cases and customize the output according to your needs. Whether you're a data engineer or just someone who loves working with the command line, this article provides the knowledge and tools you need to perform JSON to CSV conversion effortlessly.
last_modified_at: 2023-07-11
categories:
  - cli
---
**Explore the top JSON-CSV conversion tools in this article. If you like `jq` consider Earthly for streamlining your build processes with its containerized approach. [Check it out](https://cloud.earthly.dev/login).**

How do you convert JSON values to CSV and back at the command line? I've done this task on many occasions and been stung by the edge cases frequently enough that **it's time for me to share my favorite tools for this conversion process.** But first, some background.

## Background: You Probably Want a CSV Conversion Tool

The CSV format seems simple at first glance: You have a fixed number of fields per row and each field is separated by a comma.

``` bash
1997,Ford,E350\n
```

However, if you need to use commas in the value, then the fields must be delimited with `"`:

``` bash
1997,Ford,E350,"Super, luxurious truck"\n
```

You can use this same trick to delimit a line break, and use double double-quotes if you need to include `"` in your values or headings.

``` bash
1997,Ford,E350,"Go get one ""now""\n
they are going fast"\n
```

Things get more complex from there, and even the [CSV standard](https://datatracker.ietf.org/doc/html/rfc4180) does not specify how to handle all the edge cases and some formatting options are non-compatible. Wikipedia puts it this way:

> The CSV file format is not fully standardized. Separating fields with commas is the foundation, but commas in the data or embedded line breaks have to be handled specially. Some implementations disallow such content while others surround the field with quotation marks, which yet again creates the need for escaping these if they are present in the data.

So although it seems like CSV conversion can be done by hand in python, or your language of choice, using an existing tool that is known to handle the edges cases well it the way to go.

With that in mind, let's review some tools for converting from JSON to CSV at the command line.

## Convert JSON to CSV via the Command Line

The simplest way to do this JSON to CSV conversion is with `dasel`. `dasel` is a tool for DAta SELection. Think of it as a `jq` that supports selection on formats besides just JSON.

It's easy to install (`brew install dasel`), and it works great as a format converter.

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

<figcaption>simple.json</figcaption>

The conversion is easy:

``` bash
$ dasel -r json -w csv < sample.json 
color,id,value
red,1,#f00
green,2,#0f0
blue,3,#00f
```

<figcaption>converting with `dasel`</figcaption>

`dasel` handles newlines and values containing commas as well.

## Convert JSON to CSV via the Command Line Using JQ

If you don't want to install `dasel` or if you just love `jq`  (`brew install jq`) then this solution may work well for you. Before I discovered `dasel` this was the main approach I used:

``` bash
$ cat simple.json| jq -r '(map(keys) | add | unique) as $cols | map(. as $row | $cols | map($row[.])) as $rows | $cols, $rows[] | @csv' 
"color","id","value"
"red",1,"#f00"
"green",2,"#0f0"
"blue",3,"#00f"
```

<figcaption>Convert any JSON to CSV with JQ</figcaption>

A full explanation for how this works is beyond the scope of this article, but the idea is to use `(map(keys) | add | unique)` to get the column names and then gather the values for those columns into `$row` and use the `@csv` filter to convert the array of rows in a CSV format.

## Convert JSON to CSV via the Command Line and Choose Ordering Column

The downside to the previous two approaches is that you can't specify which columns to exclude nor their order. Both `jq` and `dazel` support a query language for customizing the output, but if you don't want to dive into CSS selectors, the `jsonv` tool is a great alternative.

To convert, we will use `jsonv` and pipe it our JSON file. Then, we will specify the columns to include, and we redirect its output to a file.

``` bash
cat simple.json | jsonv id,color,value > simple.csv
```

This gives us a simple CSV file:

``` bash
$ cat simple.csv
1,"red","#f00"
2,"green","#0f0"
3,"blue","#00f"
4,"cyan","#0ff"
5,"magenta","#f0f"
6,"yellow","#ff0"
7,"black","#000"
```

`jsonv` handles more complex examples as well. Under the hood, it uses `gnuawk` (`gawk`). You can install it using curl:

```
curl -Ls https://raw.github.com/archan937/jsonv.sh/master/install.sh | bash
```

You can install `gawk` using brew (`brew install gawk`) or your package manager of choice.

## Convert CSV to JSON at The Command Line

For converting CSV to JSON, we can use `dasel` again. The read (`-r`) and write (`-w`) options mean that it's easy to convert from any of its supported file formats (JSON, YAML, TOML, XML, and CSV).

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

Another option is to grab the npm tool `csvtojson` (`npm i --save csvtojson`). If you don't already have npm and Node.js installed then installing `dasel` is a simple solution. Once installed, you can convert to CSV by sending input to  `csvtojson` over standard in:

``` bash
csvtojson < sample.csv
[
{"ID":"1","color":"red","value":"#f00"},
{"ID":"2","color":"green","value":"#0f0"},
{"ID":"3","color":"blue","value":"#00f"}
]
```

## Conclusion

You now have the knowledge and the tools you need to convert JSON to CSV and CSV to JSON. [`jq`](https://stedolan.github.io/jq/), [`dasel`](https://github.com/TomWright/dasel), [`csvtojson`](https://www.npmjs.com/package/csvtojson) and [`jsonv`](https://github.com/archan937/jsonv.sh) are handy command line tools that can be used on Linux, MacOS and Windows under WSL 2.

Also, if you're the type of person who's not afraid to do things on the command line then you might like [Earthly](https://cloud.earthly.dev/login/):

{% include_html cta/bottom-cta.html %}
