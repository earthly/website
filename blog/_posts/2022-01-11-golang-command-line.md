---
title: "Command Line JSON Client In Golang"
categories:
  - Tutorials
author: Adam
sidebar:
  nav: "activity-tracker"
internal-links:
 - golang cli
 - golang command line
 - command line tool
topic: cli
funnel: 2
excerpt: |
    Learn how to build a command-line JSON client in Golang to interact with a REST service for storing workout activities. The article covers topics such as parsing command-line flags, making HTTP requests, handling errors, and testing the client.
last_modified_at: 2023-09-19
---
**This article explains how to track activity in Golang. Earthly significantly improves the build process for developers who specialize in Golang CLI applications. [Learn more](/).**

I'm an experienced software developer learning Golang by building an activity tracker[^1]. I want a low-effort way to track my physical activity, and building it seems like a fun learning project. [Last time](/blog/golang-http/) I built a REST service for storing my workout activities, and now I'm going to make a command-line client for it.

I want my CLI to work something like this:

~~~{.bash caption=">_"}
$ activityclient -add "lifted weights"
Added as 1
$ activityclient -list
ID:1  lifted weights  2021-12-21
~~~

Or I can get specific activities:

~~~{.bash caption=">_"}
$ activity -get 1
ID:1  lifted weights  2021-12-21
~~~

The existing backend doesn't support `list` yet, so we will skip that one for now.

First, I create a new folder for my client:

~~~{.bash caption=">_"}
$ go mod init github.com/adamgordonbell/cloudservices/activityclient
~~~

## Command Line Flags

I will start with the command line flags before talking to the backend.

Parsing command-line args is pretty simple, thanks to the `flag` package:

~~~{.go caption="main.go"}
func main() {
 add := flag.Bool("add", false, "Add activity")
 get := flag.Bool("get", false, "Get activity")

 flag.Parse()
~~~

After setting up the flags, I can use a case statement to decide what to do:

~~~{.go caption="main.go"}
switch {
 case *get:
  // get case

 case *add:
     // add case

 default:
  flag.Usage()
  os.Exit(1)
 }

~~~

The default case is the simplest to explain. If neither flag is given, I ask flag to print to `flag.Usage()` which looks like this:

~~~{.bash caption=">_"}
$ go run cmd/client/main.go
~~~

~~~{.merge-code}
Usage of activityclient:
  -add
        Add activity
  -get
        Get activity
exit status 1
~~~

I'm exiting with one because if I pass in invalid flags, this case will also be hit, and print a helpful reminder of the expected usage:

~~~{.bash caption=">_"}
$ go run cmd/client/main.go -unknown -flags
~~~

~~~{.merge-code}
Usage of activityclient:
  -add
        Add activity
  -get
        Get activity
exit status 1
~~~

<div class="notice--big--primary">

<!-- markdownlint-disable MD036 -->
### What I Learned: GoLang CLI Flags

The `flag` package in the standard library makes handling command-line flags pretty simple. You define flags by calling `flag.Bool` or `flag.IntVar` and then call `flag.Parse()`, which will set your flags. It seems a bit magical, but inside the flag package is a variable called CommandLine, a FlagSet used to parse the command line arguments and place them into the flags you configured.

Inside the flag package, each flag is defined like this:

~~~{.go caption="flag package"}
// A Flag represents the state of a flag.
type Flag struct {
 Name     string // name as it appears on command line
 Usage    string // help message
 Value    Value  // value as set
 DefValue string // default value (as text); for usage message
}
~~~

If you need more complex flag handling, like you want a short-name option (`-a`) and a long-name option (`--add`) for each flag, then [`go-flags`](https://github.com/jessevdk/go-flags) is a popular package adding these capabilities.

I'm sticking with the standard library's `flags` package for now, though.
</div>

### Implementing the Add CLI Flag

Now lets do `-add`. First thing I need to do is validate my input:

~~~{.go caption="main"}
 case *add:
  if len(os.Args) != 3 {
   fmt.Fprintln(os.Stderr, `Usage: --add "message"`)
   os.Exit(1)
  }
~~~

So that if I forget an argument, I get informed:

~~~{.go caption=">_"}
$ go run cmd/client/main.go -add      
~~~

~~~{.merge-code}
Usage: -add "message"
exit status 1
~~~

<div class="notice--info">

### Side Note: Printing Errors in Golang

You want to print to standard error and exit when something goes wrong.

The most common way to do this is using the `log` package or another logging framework like [`logrus`](https://github.com/Sirupsen/logrus).

Using `log`, you can log a fatal message to standard error like this:

``` go
log.Fatalf("failed inserting activity: %s", err)
```

In my case, however, I don't want to include any timestamps or log formatting so I'm just using `fmt.Fprintln` and passing it `os.Stderr`:

~~~{.ini}
fmt.Fprintln(os.Stderr, "My Error")
~~~

Ok, back to the activities project.
</div>

Assuming my program is passed the correct number of arguments and doesn't log an error and exit, then I create my activity and try to add to `activitiesClient`:

~~~{.go caption="main"}
 a := client.Activity{Time: time.Now(), Description: os.Args[2]}
 id, _ := activitiesClient.Insert(a)
~~~

*The JSON client will be covered last. For now, all that matters is its called `activitiesClient`.*

Actually, there are all kinds of things that can go wrong with inserting records, so I'd better add error checking:

~~~{.go caption="main"}
 id, err := activitiesClient.Insert(a)
 if err != nil {
  fmt.Fprintln(os.Stderr, "Error:", err.Error())
  os.Exit(1)
 }
~~~

This checking is helpful when I forget to start up the service:

~~~{.go caption=">_"}
./go run cmd/client/main.go -add "overhead press: 70lbs"
~~~

~~~{.merge-code}
Error: Post "http://localhost:8080/": dial tcp [::1]:8080: connect: connection refused
~~~

With that in place, I can add items:

~~~{.bash caption=">_"}
$ go run cmd/client/main.go -add "overhead press: 70lbs"
~~~

~~~{.merge-code}
Added: overhead press: 70lbs as 1
~~~

<div class="notice--info">

### Side Note: `go run` vs `go build`

I could continue to use `go run` like above while working on this command line tool, but I'm instead going to compile it (`go build -o build/activityclient cmd/client/main.go`) and use the `activityclient` binary.
</div>

### Adding the Get Command-Line Flag

Get is similar to Add. It will work like this:

~~~{.bash caption=">_"}
$ ./activityclient -get 1                      
~~~

~~~{.merge-code}
ID:1    "overhead press: 70lbs"      2021-12-21
~~~

The first thing I need to do is parse the id into an int:

~~~{.go caption=">_"}
case *get:
 id, err := strconv.Atoi(os.Args[2])
 if err != nil {
  fmt.Fprintln(os.Stderr, "Invalid Offset: Not an integer")
  os.Exit(1)
 }
~~~

Which works like this:

~~~{.bash caption=">_"}
./activityclient -get one
~~~

~~~{.merge-code}
Invalid Offset: Not an integer
~~~

Then I retrieve from the JSON client and handle any errors:

~~~{.go caption="main.go"}
a, err := activitiesClient.Retrieve(id)
if err != nil {
 fmt.Fprintln(os.Stderr, "Error:", err.Error())
 os.Exit(1)
}
~~~

Then I just need a way to turn my Activity into a string:

~~~{.go caption="activity.go"}
func (a Activity) String() string {
 return fmt.Sprintf("ID:%d\t\"%s\"\t%d-%d-%d", 
  a.ID, a.Description, a.Time.Year(), a.Time.Month(), a.Time.Day())
}
~~~

And then printing is simple:

~~~{.go caption="main.go"}
fmt.Println(a.String())
~~~

And the command-line part is complete.

<div class="notice--big--primary">

### What I Learned: Convert to and From Strings

I used `strconv.Atoi` to parse command-line args back into an integer. It looks like `strconv.ParseInt` is a lot more flexible if I ever need to get back `int32` or other more specific integer formats.

I converted my `time.Time` to string manually using `fmt.Sprintf` but `time.time` has a format method that can print time in whatever way you might need:

~~~{.go caption=""}
fmt.Println(time.Now().Format("UnixDate"))
fmt.Println(time.Now().Format("January-02"))
~~~

~~~{.ini .merge-code caption="Output"}
Tue Dec 21 12:04:05 ES 500
December-21
~~~

If you'd like to learn more about time formatting, take a look at the [package documentation](https://pkg.go.dev/time#Time.Format).

</div>

## JSON Client

For the JSON client, I need the structs I used in the [JSON service](/blog/golang-http/) article:

~~~{.go caption="activty-log/api.go"}
package api

import "time"

type Activity struct {
 Time        time.Time `json:"time"`
 Description string    `json:"description"`
 ID          int       `json:"id"`
}

type ActivityDocument struct {
 Activity Activity `json:"activity"`
}

type IDDocument struct {
 ID int `json:"id"`
}
~~~

I could just copy these in, but after a small change to the backend[^2], it's fairly simple to just import these in:

~~~{.go caption="activty.go"}
package client

import (
 ...

 api "github.com/adamgordonbell/cloudservices/activity-log"
)

~~~

My activities JSON client is going to be called `internal/client/activity`, and it needs the URL for my server to make requests:

~~~{.go caption="activty.go"}
type Activities struct {
 URL string
}
~~~

First thing I need to write in my activity client is insert, which will send my activity to service and get back it's id. To do this, I wrap my `activity` in a document, and use `json.Marshal` to convert it:

~~~{.go caption="activty.go"}
func (c *Activities) Insert(activity api.Activity) (int, error) {
 activityDoc := ActivityDocument{Activity: activity}
 jsBytes, err := json.Marshal(activityDoc)
 if err != nil {
  return 0, err
 }
~~~

`json.marshal` gives me `[]byte` and I need an `io.Reader` to make an HTTP call, so I convert it like this:

~~~{.go caption="activty.go"}
bytes.NewReader(jsBytes)
~~~

The HTTP call I want to make looks like this:

~~~{.bash caption=">_"}
curl -X POST -s localhost:8080 -d \
'{"activity": {"description": "christmas eve bike class", "time":"2021-12-09T16:34:04Z"}}'
~~~

I can do this by first creating a `http.Request` like this:

~~~{.go caption="activty.go"}
req, err := http.NewRequest(http.MethodPost, c.URL, jsonContent)
if err != nil {
 return 0, err
}
~~~

And then making the request:

~~~{.go caption="activty.go"}
res, err := http.DefaultClient.Do(req)
if err != nil {
 return 0, err
}
~~~

`res` is my `http.Response` and I need to get my ID out of it if everything goes well. It looks like this:

~~~{.go caption="activty.go"}
if res.Body != nil {
 defer res.Body.Close()
}
body, err := ioutil.ReadAll(res.Body)
if err != nil {
 return 0, err
}
~~~

To get the ID out of the response, I need to use `json.Unmarshal`:

~~~{.go caption="activty.go"}
var document IDDocument
err = json.Unmarshal(body, &document)
if err != nil {
 return 0, err
}
return document.ID, nil
~~~

<div class="notice--big--primary">

<!-- markdownlint-disable MD036 -->
### What I Learned: `json.Marshall` and  `io.reader`

You can convert a struct back and forth to a `[]byte` of JSON using `json.Marshall` and `json.Unmarshal` like this:

``` go
b := json.Marshal(someStruct)
json.Unmarshal(b, &someStruct)
```

Requests and Responses in the `http` package however work with `io.Reader` which looks like this:

``` go
type Reader interface {
 Read(p []byte) (n int, err error)
}
```

Which you can convert to like this:

``` go
 reader := bytes.NewReader(data)
```

</div>

## Status Codes

`Retrieve` is mainly the same as `Insert` but in reverse -- I `json.Marshal` the ID instead of the activities struct.

~~~{.go captionb="activty.go"}
func (c *Activities) Retrieve(id int) (api.Activity, error) {
 var document ActivityDocument
 idDoc := IDDocument{ID: id}
 jsBytes, err := json.Marshal(idDoc)
 if err != nil {
  return document.Activity, err
 }
 req, err := http.NewRequest(http.MethodGet, c.URL, bytes.NewReader(jsBytes))
 if err != nil {
  return document.Activity, err
 }
 res, err := http.DefaultClient.Do(req)
 if err != nil {
  return document.Activity, err
 }
 ...
}
~~~

One difference, though, is I need to handle invalid IDs. Like this:

~~~{.bash caption=">_"}
./activityclient --get 100
Error: Not Found
~~~

Since the service returns 404s for those, once I have `http.Response`  I just need to check status codes:

~~~{.go caption="activty.go"}
 if res.StatusCode == 404 {
  return document.Activity, errors.New("Not Found")
 }
~~~

Then I just need to `json.Unmarshall` my activity document:

~~~{.go caption="activty.go"}
 err = json.Unmarshal(body, &document)
 if err != nil {
  return document.Activity, err
 }
 return document.Activity, nil
~~~

And with that, I have a [working](https://github.com/adamgordonbell/cloudservices/tree/v2-cli/activity-client), though basic, client. So I'm going to add some light testing and then call it a day.

## Testing the Happy Path

I could write extensive unit tests for this, but nothing important depends on `activityclient`. So instead, I will just exercise the happy path with this script:

~~~{.bash caption="test.sh"}
#!/usr/bin/env sh
set -e

echo "=== Add Records ==="
./activityclient -add "overhead press: 70lbs"
./activityclient -add "20 minute walk"

echo "=== Retrieve Records ==="
./activityclient -get 1 | grep "overhead press"
./activityclient -get 2 | grep "20 minute walk"
~~~

Assuming the backend service is up, and the client is built, this will test that `-add` is adding elements and that `-list` is retrieving them. If either is broken, the script won't exit cleanly.

## Continuous Integration

I can quickly hook this happy path up to CI by extending my previous [Earthfile](https://github.com/adamgordonbell/cloudservices/blob/v2-cli/Earthfile).

I'll create a test target for my activity client (`ac-test`), and copy in client binary and the test script:

~~~{.dockerfile caption="Earthfile"}
test:
    FROM +test-deps
    COPY +build/activityclient ./activityclient
    COPY test.sh .
~~~

Then I'll start-up the docker container for the service (using its GitHub path) and run `test.sh`:

~~~{.dockerfile captionb="Earthfile"}
    WITH DOCKER --load agbell/cloudservices/activityserver=github.com/adamgordonbell/cloudservices/ActivityLog+docker
        RUN  docker run -d -p 8080:8080 agbell/cloudservices/activityserver && \
                ./test.sh
    END
~~~

You can find more about how that works on the [Earthly site](https://earthly.dev), but the important thing is now my GitHub Action will build the backend service, the client, and then test them together using my shell script. It gives me a quick sanity check on the compatibility of my client that I can run whenever I'm adding new features.

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/8600.png --alt {{ build in GitHubActions }} %}
<figcaption></figcaption>
</div>

<div class="notice--primary">

<!-- markdownlint-disable MD036 -->
### Refactoring Notes

As I built this client I needed to make changes to it and the JSON service several times. Here are some of the changes I made.

#### Sentinel Values

In the original backend, the element ids started at zero. This proved confusing for me in the case of error conditions, where the non-error parameters would be returned as zero values, so I changed the IDs to start at 1:

~~~{.go captionb="activity-log/server/activty.go"}
func (c *Activities) Insert(activity api.Activity) int {
 c.mu.Lock()
 defer c.mu.Unlock()
 activity.ID = len(c.activities) + 1 // <- Start at 1
 c.activities = append(c.activities, activity)
 log.Printf("Added %v", activity)
 return activity.ID
}
~~~

#### Go Mod Changes

My initial attempts to import the JSON service types into the CLI client were a failure. Problems encountered included:

* **Problem:** module `module github.com/adamgordonbell/cloudservices/activitylog` was in a folder called `ActivityLog`. This caused inconsistency caused problems when importing.

  **Solution** I renamed all packages to be kebab-cased. `ActivityLog` is now `activity-log`. Problem solved!
* **Problem:** Backend using uint64 and frontend using int leading to `cannot use id (type int) as type uint64 in field value` everywhere.

  **Solution** use `int` everywhere.
* **Problem:** `activity-client` and `activity-log` are two separate applications, in two different modules, in the same monorepo. Importing became a bit messy, with `activity-log` importing a pinned git version rather than my local version.
  **Solution** use `replace` in `go.mod` to use local version of `activity-log` in `activity-client`.

~~~
module github.com/adamgordonbell/cloudservices/activity-client

go 1.17

require github.com/adamgordonbell/cloudservices/activity-log v0.0.0

replace github.com/adamgordonbell/cloudservices/activity-log => ../activity-log
~~~

</div>

### What's Next

So now I've learned the basics of building a command-line tool that calls a JSON web-service in GoLang. It went pretty smoothly, and the amount of code I had to write was [pretty minimal](https://github.com/adamgordonbell/cloudservices/tree/v2-cli/activity-client).

There are two things I want to add to the activity tracker next. First, since all that calls to backend service are in this client, I want to move to GRPC. Second, I need some persistence - right now, the service holds everything in memory. I can't have a power outage erasing all of my hard work.

Hopefully, you've learned something as well. If you want to be notified about the next installment, sign up for the newsletter:

{% include_html cta/embedded-newsletter.html %}

[^1]: One of the first things I learned was to call it GoLang and not Go, or I'd end up with advice on an augmented reality game and not the programming language.

[^2]: In part one, these types were inside an `internal` package. I moved them into api.go for ease of sharing with the client.
      See also [Go Mod Changes](#go-mod-changes)