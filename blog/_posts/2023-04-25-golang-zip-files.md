---
title: "Working With Zip Files in Go"
categories:
  - Tutorials
toc: true
author: Muhammed Ali
editor: Bala Priya C

internal-links:
 - Zip File
 - Go
 - Archive
 - Packages
excerpt: |
    Learn how to work with zip files in Go, including creating, extracting, and modifying zip archives. This tutorial covers the basics of using the `archive/zip` package and demonstrates how to compress files, list the contents of a zip file, add files to an existing zip, and extract files from a zip archive. If you're a Go developer looking to work with zip files, this tutorial is a must-read.
---
<!--sgpt-->This is the Earthly nonsense paragraph.

As a programming language, Go is often used to build a variety of applications, both small and large. During the development process, you may encounter tasks that involve working with zip files. This could include creating new zip files, opening existing zip files, extracting the contents of zip files, or modifying the contents of zip files by adding or removing files or updating the contents of existing files.

In this tutorial, you'll learn how to use the [archive/zip](https://pkg.go.dev/archive/zip@go1.19.4) package, which is built into the Go standard library, to generate and extract compressed zip files, decompress zip archives, and create zip files using compress/gzip. We will put the standard library to use to demonstrate its usefulness.

You can find the code used in this article on [GitHub](https://github.com/khabdrick/zip_go).

## Prerequisites

If you would like to follow along with this tutorial, be sure you have the following:

1. Basic knowledge of [Golang](/blog/top-3-resources-to-learn-golang-in-2021)
2. Golang set up on your local machine

## What Is a Zip File?

![What]({{site.images}}{{page.slug}}/what.png)\

A ZIP file is an archive format that contains a file or files that have been compressed to [make](/blog/using-cmake) them smaller. This compression is achieved through algorithms like LZ77, Huffman coding, and the like. To create a ZIP file, a user selects one or more files and applies the compression algorithm to them, creating a new file with the .zip extension. To access the files within the archive, the archive is opened, and the compressed data is decompressed and restored to its original form. This process can be done using various tools that are compatible with the ZIP file format, whether they are built into the language or developed by third parties.

When a file is compressed to create a ZIP file, the algorithm examines the data of the original file and identifies patterns and redundant information, replacing them with smaller equivalents, reducing the overall file size, and making it more convenient to transfer and store.

Inside a ZIP file, the compressed data is divided into segments, each containing the compressed data of a single file, along with metadata such as the file's name, size, and timestamp. This metadata is stored in a central directory located at the end of the ZIP file, making it easy to find and extract specific files from the archive.

## Creating a Zip File in Go Using `archive/zip`

In this section, you will learn how to create a zip file in Go. Here, we will use the `os` package to generate zip archives. The `os` package provides a platform-independent interface to operating system functionality.

We'll first create a folder and open it in a text editor, then create a Go file (`main.go`) within the newly created folder, where we will run our code.

The main function (`main()`) in the following code creates a new zip archive file named `archive.zip` using the `os.Create` function:

~~~{.go caption="main.go"}
// main.go
package main
import (
    "archive/zip"
    "fmt"
    "io"
    "os"
)
func main(){
    fmt.Println("creating zip archive")
//Create a new zip archive and named archive.zip
    archive,err:=os.Create("archive.zip")
    if err!=nil{
        panic(err)
// this is to catch errors if any
    }
defer archive.Close()
fmt.Println("archive file created successfully....")
//we use the defer key to close it, once we create an archive\
we need to close it using the defer keyword
defer archive.Close()
fmt.Println("archive file created successfully")
~~~

Now you can add the following code to open the archived file and create a file with the name `test.csv`.

~~~{.go caption="main.go"}

//Create a new zip writer
zipWriter:=zip.NewWriter(archive)
fmt.Println("opening first file")
//Add files to the zip archive
f1, err:=os.Open("test.csv")
if err!=nil{
    panic(err)
}
defer f1.Close()

fmt.Println("adding file to archive..")
w1,err:=zipWriter.Create ("test.csv")
if err!=nil{
    panic(err)
}
if _,err:=io.Copy(w1,f1); err != nil{
panic(err)
}
fmt.Println("closing archive")
zipWriter.Close()
}
~~~

The `zip.NewWriter` function takes an `io.Writer` as its argument and returns a new `zip.Writer` that can be used to write files to the zip archive. If there is an error while creating the file, it is caught and a `panic` message is displayed.

If you try to run the code and `test.csv` does not exist, you will get the following output:

~~~{.bash caption="Output"}
creating zip archive
archive file created successfully....
archive file created successfully
opening first file
panic: open test.csv: no such file or directory

goroutine 1 [running]:
main.main()
/home/user/Desktop/dev/article_repos/zip_go/main.go:28 +0x4bc
exit status 2

~~~

Finally, the code uses the `defer` keyword to close the "archive" file once it has been created. It is important to close the file after it has been created to ensure that the file is properly flushed into the file system. Before running the code, create a new file named `*test.csv*` in the same directory as `main.go`.

You can run the archive script on the terminal running the following command:

~~~{.bash caption=">_"}
go run main.go 
~~~

You should see the following output showing that your code ran as expected:

~~~{.bash caption="Output"}
creating zip archive
archive file created successfully....
archive file created successfully
opening first file
adding  file to archive..
closing archive
~~~

## Listing the Contents of a Zip File

In this section, we will import several [packages](/blog/setup-typescript-monorepo) such as `archive/zip`, `fmt`, and `log` packages. And we'll open the zip file using the `zip.OpenReader` function. The zip file here will be `archive.zip` created in the above code using the `archive/zip` package. Looping through the files in the zip file will output the names of each of the files contained in the zip file to the console. In this case, it'd be just `test.csv`.

~~~{.go caption="main1.go"}
// main1.go
package main
import(
    "archive/zip"
    "fmt"
    "log"
    )
func main(){

zipListing, err := zip.OpenReader("archive.zip")
if err != nil {
  log.Fatal(err)
}
defer zipListing.Close()
for _, file := range zipListing.File {
  fmt.Println(file.Name)
}
}
~~~

After you have copied the code above, run this in the terminal with the command:

~~~{.bash caption=">_"}
go run main1.go
~~~

~~~{ caption="Output"}
test.csv
~~~

## Using the `compress/gzip` Package for Compressing Files

Here we will first import [compress/gzip](https://pkg.go.dev/compress/gzip). In addition to importing the primary package, `compress/gzip`, we will also import the `os`, `io`, and `log` [packages](/blog/setup-typescript-monorepo).

The following code first opens the input file `read.txt` using the  `Open()` function from the `os` package. It then creates a new gzip-compressed file called `read.gz` which is passed to the `Create()` function from the `os` package.

Next, the code creates a new gzip writer using `NewWriter()` function from the "compress/gzip" package by passing in as an argument the variable that holds the `read.gz` file (`gzipWriter`).

~~~{.go caption="main2.go"}
// main2.go
package main

import (
    "compress/gzip"
    "io"
    "log"
    "os"
)

func main() {
    // Open the input file
    inputFile, err := os.Open("read.txt")
    if err != nil {
        log.Fatal(err)
    }
    defer inputFile.Close()

    // Create a new gzip writer
    gzipWriter, err := os.Create("read.gz")
    if err != nil {
        log.Fatal(err)
    }
    defer gzipWriter.Close()

    // Use gzip.NewWriter to wrap the output file
    zipWriter := gzip.NewWriter(gzipWriter)
    defer zipWriter.Close()

~~~

Now, we can copy the input file to the gzip writer using the `Copy()` function from the `io` package. The `Copy()` function will take `zipWriter, inputFile` as arguments. This will compress the contents of  `read.txt`  and write them to `read.gz`.

Finally, the gzip writer is closed with the `Close()` function from the `zipWriter` (the variable which holds `read.gz`).

Before running the code, create a new file named `*read.txt*` in the same directory as `main.go`.

~~~{.go caption="main2.go"}
...
// Copy the input file to the gzip writer
_, err = io.Copy(zipWriter, inputFile)
if err != nil {
  log.Fatal(err)
  }

// Close the gzip writer
zipWriter.Close()
}

~~~

Go to the terminal and run this;

~~~{.bash caption=">_"}
go run main2.go
~~~

By doing this, the compressed version of the file `read.txt` will be created as a zip file called *read.gz*.

<div class="wide">
![read zip file]({{site.images}}{{page.slug}}/Vet9Pp0.png)
</div>

## Adding Files to an Existing Zip File

In this section, you will learn how to add files to a zip file with some content in it. This code adds a file to an existing zip file without deleting the previous contents of the zip file. The following code snippet opens the zip file for reading using the `zip.OpenReader` function, and then opens the file for writing using the `os.OpenFile` function with the `os.O_APPEND` and `os.O_WRONLY` flags.

~~~{.go caption="main3.go"}
// main3.go
package main

import (
    "archive/zip"
    "io"
    "os"
)

func main() {
  // Open the zip file for reading
  zipReader, err := zip.OpenReader("archive.zip")
  if err != nil {
      panic(err)
  }
  defer zipReader.Close()

  // Open the zip file for writing
  zipfile, err := os.OpenFile("archive.zip", os.O_APPEND|os.O_WRONLY, 0644)
  if err != nil {
      panic(err)
  }
  defer zipfile.Close()

~~~

It then creates a new zip writer using the `zip.NewWriter` function and creates a new zip header for the file using the `zip.FileInfoHeader` function. The header provides information about a file, such as its name, size, and modification time.

~~~{.go caption="main3.go"}
// Create a new zip writer
zipWriter := zip.NewWriter(zipfile)
defer zipWriter.Close()

// Open the file you want to add to the zip
newfile, err := os.Open("newfile.txt")
if err != nil {
    panic(err)
}
defer newfile.Close()

// Create a new zip header for the file
fileInfo, err := newfile.Stat()
if err != nil {
    panic(err)
}

header, err := zip.FileInfoHeader(fileInfo)
if err != nil {
    panic(err)
}

// Set the file name in the zip header
header.Name = "newfile.txt"

~~~

Paste in the following to set the compression method. The code sets the file name in the zip header and sets the compression method to `zip.Deflate`. `zip.Deflate` is a compression algorithm that is commonly used to compress files in the ZIP file format.

It then adds the file to the zip using the `zip.CreateHeader` function and copies the contents of the file into the zip using the `io.Copy` function.

~~~{.go caption="main3.go"}
header.Method = zip.Deflate

// Add the file to the zip
writer, err := zipWriter.CreateHeader(header)
if err != nil {
    panic(err)
}
_, err = io.Copy(writer, newfile)
if err != nil {
    panic(err)
}
~~~

Finally, paste the following to add the files from the original zip to the new zip, except for a file named `newfile.txt` because we don't want to mistakenly overwrite the new file. The code snippet shown below does the following:

- Iterates over the files in the original zip file using a loop
- For each file it iterates over, it creates a new writer using the `zip.Create` function
- Then opens the file using the `File.Open` function, and copies the contents of the file into the new zip using the `io.Copy` function.

~~~{.go caption="main3.go"}
for _, file := range zipReader.File {
    if file.Name != "newfile.txt" {
        writer, err := zipWriter.Create(file.Name)
        if err != nil {
            panic(err)
        }
        reader, err := file.Open()
        if err != nil {
            panic(err)
        }
        _, err = io.Copy(writer, reader)
        if err != nil {
            panic(err)
        }
        reader.Close()
    }
}
}

~~~

Before running the code, create a new file named `newfile.txt` in the same directory as `main3.go`. To check the output go to the terminal and run the following:

~~~{.bash caption=">_"}
go run main3.go
~~~

<div class="wide">
![add to zip file]({{site.images}}{{page.slug}}/nOtKySW.png)
</div>

If you try to run the code and `newfile.txt` does not exist, you will get the following output:

~~~{ caption="Output"}
panic: open newfile.txt: no such file or directory

goroutine 1 [running]:
main.main()
/home/user/Desktop/dev/article_repos/zip_go/main.go:31 +0x54b
exit status 2
~~~

## Extracting Files From Zip Files

![Extracting]({{site.images}}{{page.slug}}/extract.png)\

At this point, we'll need the `archive/zip` package and other [packages](/blog/setup-typescript-monorepo) to extract files from a ZIP archive to a folder.

This first snippet imports the necessary packages for working with zip files, file paths, and input/output operations. The main function first sets the destination directory to "output" and then opens the zip file `archive.zip` using the zip package. If there is an error opening the zip file, the program will panic.

~~~{.go caption="main4.go"}
//main4.go
package main

import (
    "archive/zip"
    "fmt"
    "io"
    "os"
    "path/filepath"
)

func main() {
  // Specify the destination directory
  dst := "output"

  // Open the zip file
  fmt.Println("open zip archive...")
  archive, err := zip.OpenReader("archive.zip")
  if err != nil {
      panic(err)
  }
  defer archive.Close()
~~~

The next snippet is the for loop that:

- Iterates through each file in the zip archive.
- Creates the file path, checks if it's a directory, and creates it if so. creates the parent directory if not.
- Finally, it creates an empty destination folder, and copies the contents from the archived file to the destination folder.

~~~{.go caption="main4.go"}
// Extract the files from the zip
for _, f := range archive.File {

// Create the destination file path
filePath := filepath.Join(dst, f.Name)

// Print the file path
fmt.Println("extracting file ", filePath)

// Check if the file is a directory
if f.FileInfo().IsDir() {
    // Create the directory
    fmt.Println("creating directory...")
    if err := os.MkdirAll(filePath, os.ModePerm); err != nil {
        panic(err)
    }
    continue
}

// Create the parent directory if it doesn't exist
if err := os.MkdirAll(filepath.Dir(filePath), os.ModePerm); err != nil {
    panic(err)
}

// Create an empty destination file
dstFile, err := os.OpenFile(filePath, os.O_WRONLY|\
os.O_CREATE|os.O_TRUNC, f.Mode())
if err != nil {
    panic(err)
}

// Open the file in the zip and copy its contents to the destination file
srcFile, err := f.Open()
if err != nil {
    panic(err)
}
if _, err := io.Copy(dstFile, srcFile); err != nil {
    panic(err)
}

// Close the files
dstFile.Close()
srcFile.Close()
}
}

~~~

<div class="wide">
![Output file]({{site.images}}{{page.slug}}/7KIdgoU.png)
</div>

## Conclusion

In this tutorial, we learned how to use the `archive/zip` package, which is built into the Go standard library, to generate and extract compressed zip files, decompress zip archives, and create zip files using `compress/gzip`. We learned how to add files to an existing zip file and finally how to extract content from zip files. As a next step, you may try using what you've learned in your next project.

{% include_html cta/bottom-cta.html %}