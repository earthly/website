---
title: "How To Work With CSV Files In Go"
categories:
  - Tutorials
toc: true
author: Muhammed Ali
editor: Bala Priya C

internal-links:
 - CSV
 - Go
 - Tabular Data
 - GoCSV
excerpt: |
    Learn how to work with CSV files in Go using the encoding/csv package and the goCSV library. This tutorial covers topics such as reading and appending CSV files, converting between CSV and JSON file formats, and provides code examples to help you get started. If you're a Go developer looking to manage CSV files in your projects, this article is a must-read.
---
**We're [Earthly](https://earthly.dev/). We simplify the software building process, making it fast and easy. If you're working with CSV files in Go, Earthly can help streamline your workflow. Why not [give it a look](/) for your next project?**

Tabular data is frequently stored in [CSV files](https://en.m.wikipedia.org/wiki/Comma-separated_values), a popular file format. In data processing and analysis projects, managing CSV files is a common task.

And to work with CSV files, a number of packages are available. In this tutorial, we will explore various techniques for managing CSV files using the Go programming language. We will cover topics such as reading and appending CSV files, converting between CSV and JSON file formats.

### Prerequisites

To follow along with this tutorial, be sure you have the following:

1. Basic knowledge of Golang

2. Golang is set up on your local machine

You can find the code used in this article on [GitHub](https://github.com/khabdrick/go-csv).

## What Is a CSV File?

A CSV (Comma Separated Values) file is a straightforward and popular file format. It is made up of data records, where each record corresponds to a single row in the table and where each field is delimited by a comma.

Typically, each line in a CSV file represents one record or row of data, with commas separating each field in that record. Column headers, which explain what information is stored in each column, are frequently found on the first line of a file. Additionally, they are simple to create, edit, and import into most database and spreadsheet programs using a text editor or spreadsheet program.

## Encoding/CSV and GoCSV for Reading CSV

![Reading]({{site.images}}{{page.slug}}/reading.png)\

Golang provides built-in packages such as [`encoding/csv`](https://pkg.go.dev/encoding/csv) and third-party packages such as [`Gocsv`](https://pkg.go.dev/github.com/gocarina/gocsv) for handling CSV data. In this section, we will discuss these two packages and discuss which one is better for handling CSV data in Golang.

### Using `Encoding/csv` To Work with CSV Files

[`encoding/CSV`](https://pkg.go.dev/encoding/csv) is a standard package in Golang's standard library that provides functionality for encoding and decoding CSV data. In this section, we'll use the `encoding/CSV` package to read and write CSV data.

We'll first create a folder and open it in a text editor, then create a Go file (`main.go`) within the newly created folder, where we will run our code. Also, create a CSV file named `data.csv`. You can as well and get the sample data from [GitHub](https://github.com/khabdrick/go-csv/blob/master/data.csv).

The code below demonstrates how to read data from a CSV file. And also how to write data to a new CSV file:

~~~{.go caption="main.go"}
//main.go
package main

import (
   "encoding/csv"
   "fmt"
   "os"
)

func main() {
   // Open the CSV file
   file, err := os.Open("data.csv")
   if err != nil {
       panic(err)
   }
   defer file.Close()
~~~

Here, we first open the file using the `os.Open()` function and assign it to the variable `file`. We check for any errors using an if statement and panic if there's an error. We use the `defer` keyword to ensure that the file is properly closed at the end of the program.

Next, we create a new `csv.Reader` object called `reader` and read the data from the opened file. We use `reader.FieldPerRecord=-1` to allow for a variable number of fields in each record. We then use `reader.ReadAll()` to read all the records from the file and assign them to the `data` variable. If there's any error while reading the file, the program will panic and stop.

We then loop through the data using a nested `for` loop to access each row and column of the CSV file. We print each column value to the console, followed by a comma separator and a newline:

~~~{.go caption="main.go"}
   // Read the CSV data
   reader := csv.NewReader(file)
   reader.FieldsPerRecord = -1 // Allow variable number of fields
   data, err := reader.ReadAll()
   if err != nil {
       panic(err)
   }

   // Print the CSV data
   for _, row := range data {
       for _, col := range row {
           fmt.Printf("%s,", col)
       }
       fmt.Println()
   }
~~~

The following part of this code creates a new CSV file named `data1.csv` and populates it with some data. It creates a new CSV file named `data1.csv` using the `os.Create()` function and assigns it to the variable `file2`. We check for any errors using an `if` statement and `panic` if there's an error.

~~~{ caption="Output"}
panic: nil

goroutine 1 [running]:
main.main()
        /home/muhammed/Desktop/dev/article_repos/go-csv/main.go:36 +0x675
exit status 2

~~~

Next, we create a new `csv.Writer` object called `writer` for writing data to the new file.

We use defer `writer.Flush()` to ensure that any buffered data is written to the file before it's closed. Next, we define the header and data values for the new CSV file as slices of strings (represents a collection of string values) and write the header values to the new file using the `writer.Write(header)` statement. We then loop through the data rows and write each row to the new CSV file using the `writer.Write(row)` statement.

Finally, we use the `defer` statement to close both the old and new CSV files.

~~~{.go caption="main.go"}
//main.go
   // Write the CSV data
   file2, err := os.Create("data1.csv")
   if err != nil {
       panic(err)
   }
   defer file2.Close()

   writer := csv.NewWriter(file2)
   defer writer.Flush()
// this defines the header value and data values for the new csv file
   headers := []string{"name", "age", "gender"}
   data1 := [][]string{
       {"Alice", "25", "Female"},
       {"Bob", "30", "Male"},
       {"Charlie", "35", "Male"},
   }

   writer.Write(headers)
   for _, row := range data1 {
       writer.Write(row)
   }
}
~~~

Now run main.go from your terminal:

~~~{.bash caption=">_"}
go run main.go
~~~

<div class="wide">
![CSV extraction]({{site.images}}{{page.slug}}/54tNaOw.png)
</div>

![CSV creation with Encoding/CSV]({{site.images}}{{page.slug}}/5tgyj8J.png)

### Using `goCSV` to Create a CSV File

In this section, we'll use a third-party package called [`goCSV`](https://pkg.go.dev/github.com/gocarina/gocsv) to easily handle CSV data in Golang. The `goCSV` package provides advanced functionality for handling CSV data, such as the automatic mapping of CSV data to struct fields.

To download GoCsv, run the following command in your terminal or command prompt:

~~~{.bash caption=">_"}
go mod init csv
go get github.com/gocarina/GoCsv
~~~

First, we import two packages: `os` for file handling and `github.com/gocarina/gocsv` for CSV marshaling and unmarshaling.

<div class="notice--info">

Marshaling is the process of converting Go data structures (such as structs, maps, and slices) to a serialized format, typically JSON, XML, or YAML while unmarshaling is the process of decoding data in serialized format into Go data structure.

</div>

We then define a struct called `Person` with three fields: `Name`, `Age`, and `Gender`. The `csv` tag on each field specifies the column name in the CSV file.

Next, we create a new CSV file called `data2.csv` using the `os.Create()` function and assign it to the `file` variable. We check if there was any error while creating the file and panic if an error is found. The `defer file.Close()` statement ensures that the file is closed at the end of the program, even if an error occurs.

We then create a slice of `Person` structs (a collection of struct values of the same type) called `people` and initialize it with three `Person` objects. We then marshal this slice of structs into a CSV format using the `gocsv.MarshalFile()` function, which takes a pointer to the slice of structs and the file object to write the CSV data to.

After successfully marshaling the data, we close the CSV file using the `defer` statement to ensure proper cleanup and then exit.

~~~{.go caption="main1.go"}
//main1.go
package main

import (
   "os"

   "github.com/gocarina/gocsv"
)

type Person struct {
   Name   string `csv:"name"`
   Age    int    `csv:"age"`
   Gender string `csv:"gender"`
}

func main() {
   file, err := os.Create("data2.csv")
   if err != nil {
       panic(err)
   }
   defer file.Close()

   people := []*Person{
       {"Alice", 25, "Female"},
       {"Bob", 30, "Male"},
       {"Charlie", 35, "Male"},
   }

   if err := gocsv.MarshalFile(&people, file); err != nil {
       panic(err)
   }
}
~~~

After copying the code to your text editor run this command below;

~~~{.bash caption=">_"}
go run main1.go
~~~

![Using gocsv]({{site.images}}{{page.slug}}/XjeaRTr.png)

The example code below reads a CSV file named `data2.csv` using the GoCsv library. We define a struct `Record` with two fields, `Name` and `Gender`, each with a corresponding CSV column specified using struct tags `csv:"name"` and `csv:"gender"`.

Next, we read the CSV file into a slice of `Record` structs using `gocsv.UnmarshalFile()`. If there's an error during this process, we also panic with the error message.

Finally, we print the contents of the CSV file to the console using a `for` loop and the `fmt.Printf()` function. We print the name and gender fields of each record in the CSV file.

~~~{.go caption="main2.go"}
//main2.go

package main

import (
   "fmt"
   "github.com/gocarina/gocsv"
   "os"
)

type Record struct {
   Name  string `csv:"name"`
   Gender string `csv:"gender"`
}

func main() {
   // Open the CSV file
   file, err := os.Open("data2.csv")
   if err != nil {
       panic(err)
   }
   defer file.Close()

   // Read the CSV file into a slice of Record structs
   var records []Record
   if err := gocsv.UnmarshalFile(file, &records); err != nil {
       panic(err)
   }

   // Print the records
   for _, record := range records {
       fmt.Printf("Name: %s, Gender: %s\n", record.Name, record.Gender)
   }
}
~~~

After copying the code to your text editor run this command below;

~~~{.bash caption=">_"}
go run main2.go
~~~

## Appending to a CSV File

Using the [`encoding/csv`](https://pkg.go.dev/encoding/csv) package, we will be appending using the code below to the `data1.csv` file created above.

First, the code opens the CSV file using the `os.OpenFile()` function with the `os.O_APPEND` flag, which allows appending data to the end of the file instead of overwriting it. If the file opening operation encounters an error, the code uses the `panic()` function to terminate the program immediately and print the error message.

Next, the code creates a CSV writer using the `csv.NewWriter()` function and assigns it to the `writer` variable. The `defer` keyword is used to ensure that the writer is flushed and the file is closed when the function exits, even if an error occurs before these operations.

Then, the code creates a new row of data to add to the CSV file as a slice of strings and writes this row to the CSV file using the `writer.Write()` function. If the write operation encounters an error, the code again uses the "panic" function to terminate the program immediately and print the error message.

~~~{.go caption="main3.go"}
//main3.go
package main

import (
   "encoding/csv"
   "os"
)

func main() {
   // Open the CSV file for appending
   file, err := os.OpenFile("data1.csv", os.O_APPEND|os.O_WRONLY, 0644)
   if err != nil {
       panic(err)
   }
   defer file.Close()

   // Create a CSV writer
   writer := csv.NewWriter(file)
   defer writer.Flush()

   // Write a new row to the CSV file
   row := []string{"David", "30", "Male"}
   err = writer.Write(row)
   if err != nil {
       panic(err)
   }
}
~~~

Go to the terminal and run this;

~~~{.bash caption=">_"}
go run main3.go
~~~

## Converting a JSON File To CSV

In this section, we will learn how to convert JSON data to CSV using Golang. It has a built-in support for JSON encoding and decoding, which makes it easy to work with JSON data. Additionally, we will be using a third-party package, [json2csv](https://github.com/yukithm/json2csv), to convert the JSON data to CSV format.

To get the package, run the following command:

~~~{.bash caption=">_"}
go get github.com/yukithm/json2csv
~~~

This example code below reads a JSON file named [`input.json`](https://github.com/khabdrick/go-csv/blob/master/input.json) and converts it to a CSV file named `output.csv`.

In the `main` function, we create a new buffer using the `bytes.Buffer` function. We then create a new CSV writer using the `json2csv.NewCSVWriter` function, which takes a buffer as its argument.

Next, we read the JSON data from a file using the `os.ReadFile` function. We use the `json.Unmarshal` function to unmarshal the JSON data into a slice of maps. The maps represent the rows of the CSV file, and the keys represent the columns.

<div class="notice--info">
### Maps and Slice of Maps in Golang

In Go, **maps** are a built-in data structure that associates data in key-value pairs. A map provides constant-time access to its elements, based on their keys. A slice provides a way to reference a subset of an array or map without getting the whole map.

A **slice of maps** in Go is a data structure that combines the features of slices and maps. It is a dynamic sequence of maps, where each map represents a collection of key-value pairs. In other words, it is a slice where each element is a map.
</div>

~~~{.go caption="main4.go"}
//main4.go
package main

import (
   "bytes"
   "encoding/json"
   "github.com/yukithm/json2csv"
   "log"
   "os"
)

func main() {
   b := &bytes.Buffer{}
   wr := json2csv.NewCSVWriter(b)
   j, _ := os.ReadFile("input.json")
   var x []map[string]interface{}

   // unMarshall json
   err := json.Unmarshal(j, &x)
   if err != nil {
       log.Fatal(err)
   }
~~~

In the next snippet, we will convert the JSON to CSV using the `JSON2CSV` function from the json2csv package. This function takes a slice of maps with string keys and `interface{}` values, which represents the JSON data, and returns a byte slice containing the CSV data. Next, the CSV data is written to a buffer using the `WriteCSV` method.

Finally, a helper function named `createFileAppendText` is called to create a file with the name "output.csv" and append the CSV data to it. This function takes the filename and text as arguments and returns an error if there is a problem opening the file or writing to it.

~~~{.go caption="main4.go"}
// convert json to CSV
   csv, err := json2csv.JSON2CSV(x)
   if err != nil {
       log.Fatal(err)
   }

   // CSV bytes convert & writing...
   err = wr.WriteCSV(csv)
   if err != nil {
       log.Fatal(err)
   }
   wr.Flush()
   got := b.String()

   //Following line prints CSV
   // create file and append if you want
   createFileAppendText("output.csv", got)
}
~~~

Now we will create the helper function `createFileAppendText` that handles the details of opening the "output.csv" file, writing to it, and closing it.

~~~{.go caption="main4.go"}
//
func createFileAppendText(filename string, text string) {
   f, err := os.OpenFile(filename, os.O_APPEND|os.O_WRONLY|\
   os.O_CREATE, 0600)
   if err != nil {
       panic(err)
   }

   defer f.Close()

   if _, err = f.WriteString(text); err != nil {
       panic(err)
   }
}
~~~

Go to the terminal and run this;

~~~{.bash caption=">_"}
go run main4.go
~~~

The output should look like this:

![Json to csv]({{site.images}}{{page.slug}}/jSkrisz.png)

## Converting a CSV File To JSON

In this section, we will delve into the process of converting a CSV file into a JSON file. The procedure that we are about to discuss assumes that the CSV file's structure is unknown to us, making it more challenging to convert the data into the desired JSON format.

To begin, we must first open the CSV file and create a CSV reader. This will enable us to access and extract information from the headers and data rows of the CSV file. We can accomplish this with the following code:

~~~{.go caption="main5.go"}
file, err := os.Open("data1.csv")
if err != nil {
   log.Fatal(err)
}
defer file.Close()

csvReader := csv.NewReader(file)
~~~

Next, we will read the headers from the CSV file. The headers are the first row in the CSV file and contain the names of the fields in the JSON objects. Here is the code to read the headers:

~~~{.go caption="main5.go"}
headers, err := csvReader.Read()
if err != nil {
   log.Fatal(err)
}
~~~

After reading the headers, we can start reading the data rows from the CSV file. For each data row, we will create a `map[string]interface{}` where the keys are the header names and the values are the row values. We will use `strconv.ParseFloat` and `strconv.ParseBool` to convert the row values to the appropriate types (float64 and bool, respectively).

Here is the code to read the data rows:

~~~{.go caption="main5.go"}
var data []map[string]interface{}
for {
   row, err := csvReader.Read()
   if err != nil {
       break
   }

   m := make(map[string]interface{})
   for i, val := range row {
       f, err := strconv.ParseFloat(val, 64)
       if err == nil {
           m[headers[i]] = f
           continue
       }

       b, err := strconv.ParseBool(val)
       if err == nil {
           m[headers[i]] = b
           continue
       }

       m[headers[i]] = val
   }

   data = append(data, m)
}

~~~

Finally, we will encode the data as a JSON array and write it to `stdout`. Here is the code to do this:

~~~{.go caption="main5.go"}
encoder := json.NewEncoder(os.Stdout)
if err := encoder.Encode(data); err != nil {
   log.Fatal(err)
}

~~~

All the code snippets working together should look like the following:

~~~{.go caption="main5.go"}
//main5.go
package main

import (
   "encoding/csv"
   "encoding/json"
   "log"
   "os"
   "strconv"
)

func main() {
   // Open the CSV file
   file, err := os.Open("data1.csv")
   if err != nil {
       log.Fatal(err)
   }
   defer file.Close()

   // Create the CSV reader
   csvReader := csv.NewReader(file)

   // Read the CSV headers
   headers, err := csvReader.Read()
   if err != nil {
       log.Fatal(err)
   }

   // Read the CSV data rows
   var data []map[string]interface{}
   for {
       row, err := csvReader.Read()
       if err != nil {
           break
       }

       // Convert the row values to the appropriate types
       m := make(map[string]interface{})
       for i, val := range row {
           f, err := strconv.ParseFloat(val, 64)
           if err == nil {
               m[headers[i]] = f
               continue
           }

           b, err := strconv.ParseBool(val)
           if err == nil {
               m[headers[i]] = b
               continue
           }

           m[headers[i]] = val
       }

       data = append(data, m)
   }

   // Encode the JSON data and write

~~~

Now run this:

~~~{.bash caption=">_"}
go run main5.go
~~~

Your output should look like the following:

~~~{.csv caption="data2.csv"}
[{"age":25,"gender":"Female","name":"Alice"},\
{"age":30,"gender":"Male","name":"Bob"},\
{"age":35,"gender":"Male","name":"Charlie"},\
{"age":30,"gender":"Male","name":"David"}]
~~~

## Conclusion

Handling CSV files in Go is simple using the encoding/csv package and libraries like goCSV. Whether reading, adding to, or converting CSV files, Go equips you with what you need. Use the code examples in this article to delve into the perks of CSV for data storage and analysis.

And if you're looking to further enhance your development processes, consider exploring [Earthly](https://www.earthly.dev/), a neat build automation tool that can streamline your builds and make them more efficient.

{% include_html cta/bottom-cta.html %}
