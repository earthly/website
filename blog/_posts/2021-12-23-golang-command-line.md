---
title: "Put Your Best Title Here"
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - just an example
---

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

## Start

I'm an experience software developer learning GoLang by building an activity tracker. Incidentally, one of the first things I learned was to call it GoLang and not Go or I just end up with advice on an augmented reality and not the programming langauge. 

I want an easy way to track all my physical activity in hopes it will encourage me to be more active. [Last time](/blog/golang-http/) I built a REST service for storing my workout activities and now I'm going to build a command line client for it.

I want my CLI to work something like this:

~~~{.bash caption=">_"}
$ activityclient -add "lifted weights"
Added as 0
$ activityclient -list
ID:0  lifted weights  2021-12-21
~~~

Or I can get specific activities:

~~~{.bash caption=">_"}
$ activity -get 0
ID:0  lifted weights  2021-12-21
~~~

The existing backend doesn't support `list` yet so we will skip that one for now.

First I create a new folder for my client:

~~~{.bash caption=">_"}
$ go mod init github.com/adamgordonbell/cloudservices/activityclient
~~~

## Command Line Flags

I'm going to start with the command line flags before I worry about talking to backend. 

Parsing command-line args is pretty simple, thanks to the `flag` package:

~~~{.go caption="main.go"}
func main() {
	add := flag.Bool("add", false, "Add activity")
	get := flag.Bool("get", false, "Get activity")

	flag.Parse()
~~~

After setting up the flags, I can just use a case statement to decide what to do:

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

~~~{.ini }
Usage of activityclient:
  -add
        Add activity
  -get
        Get activity
exit status 1
~~~

I'm exiting 1, as this case will also be hit for any options the program doesn't understand -- which gives a helpful reminder of usage:

~~~{.bash caption=">_"}
$ go run cmd/client/main.go -unknown -flags
~~~

~~~{.ini }
Usage of activityclient:
  -add
        Add activity
  -get
        Get activity
exit status 1
~~~

<div class="notice--big--primary">

<!-- markdownlint-disable MD036 -->
**What I Learned: GoLang CLI Flags**

The `flag` package in the standard library makes handling command line flags pretty simple. You just define flags by calling `flag.Bool` or `flag.IntVar` and then call `flag.Parse()` and your flags will be set. It seems a bit magical but inside the `flag` package is a variable called `CommandLine`, which is a `FlagSet` and used to parse the command line arguments and place them into the flags you configured.

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

If you need more complex flag handling, like you want a shortname option (`-a`) and a long name option (`--add`) for each flag, then [`go-flags`](https://github.com/jessevdk/go-flags) is a popular package adding these capabilities.

I'm sticking with `flags` for now though.
</div>

### Adding the Add CLI Flag

Now lets do `-add`. First thing I need to do is validate my input:

~~~{.go caption="main"}
	case *add:
		if len(os.Args) != 3 {
			println(`Usage: -add "message"`)
			os.Exit(1)
		}
~~~

So that if I forget an arg, I get informed:

~~~{.go caption=">_"}
$ go run cmd/client/main.go -add      
~~~

~~~{.ini}
Usage: -add "message"
exit status 1
~~~


After that, if the argument count is correct, I just to create my activity and try to add to `activitiesClient`:


~~~{.go caption="main"}
	a := client.Activity{Time: time.Now(), Description: os.Args[2]}
	id, _ := activitiesClient.Insert(a)
~~~

*The JSON client will be covered last. For now, all that matters is its called `activitiesClient`.*

Actually, there are all kinds of things that can go wrong with inserting records, so I'd better add error checking:

~~~{.go caption="main"}
	id, err := activitiesClient.Insert(a)
	if err != nil {
		println("Error:", err.Error())
		os.Exit(1)
	}
~~~

This is helpful when I forget to start up the service:

~~~{.go caption=">_"}
./go run cmd/client/main.go -add "overhead press: 70lbs"
~~~

~~~{.ini}
Error: Post "http://localhost:8080/": dial tcp [::1]:8080: connect: connection refused
~~~

With that in place, it's easy to add items:

~~~{.bash caption=">_"}
$ go run cmd/client/main.go -add "overhead press: 70lbs"
~~~

~~~{.ini}
Added: overhead press: 70lbs as 0
~~~

<div class="notice--info">

ℹ️ **`go run` and `go build`**

I could continue to use `go run` like above while working on the CLI tool but I'm going instead compile it (`go build -o build/activityclient cmd/client/main.go`) and use the `activityclient` binary.
</div>

### Adding the Get Command Line Flag

Get is similar to Add. It will work like this:

~~~{.bash caption=">_"}
$ ./activityclient -get 0                      
~~~

~~~{.ini}
ID:0    "overhead press: 70lbs"      2021-12-21
~~~

The first thing I need to do is parse the id into an int:

~~~{.go caption=">_"}
case *get:
	id, err := strconv.Atoi(os.Args[2])
	if err != nil {
		println("Invalid Offset: Not an integer")
		os.Exit(1)
	}
~~~

Which works like this:

~~~{.bash caption=">_"}
./activityclient -get one
~~~

~~~{.ini}
Invalid Offset: Not an integer
~~~

Then I retrieve from the JSON client and handle any errors:

~~~{.go caption="main.go"}
a, err := activitiesClient.Retrieve(id)
if err != nil {
	println("Error:", err.Error())
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

<!-- markdownlint-disable MD036 -->
**What I Learned: Convert to and From Strings **

I used `strconv.Atoi` to parse command-line args back into a integer. It looks like `strconv.ParseInt` is a lot more flexibile, if I ever need to get back `int32` or other more specific integer formats.

I converted my `time.Time` to string manually using `fmt.Sprintf` but `time.time` has a format method that can print time in whatever way you might need:

~~~{.go caption=""}
fmt.Println(time.Now().Format("UnixDate"))
fmt.Println(time.Now().Format("January-02"))
~~~

~~~{.output caption="Output"}
Tue Dec 21 12:04:05 ES 500
December-21
~~~

If you'd like to learn more about time formatting, take a look at the [package documentation](https://pkg.go.dev/time#Time.Format).

</div>

## JSON Client

For the JSON client, I need the structs I used in the [JSON service](/blog/golang-http/) article. I'll just copy pasta them in:

~~~{.go caption="activty.go"}
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

My activities JSON client is going to be called `internal/client/activity` and it needs the URL for my server in order to make requests:

~~~{.go caption="activty.go"}
type Activities struct {
	URL string
}
~~~

First thing I need to write in my activity client is insert. I wrap my `activity` in a document and use json.Marshal to convert it:

~~~{.go caption="activty.go"}
func (c *Activities) Insert(activity Activity) (int, error) {
	activityDoc := ActivityDocument{Activity: activity}
	bytes, err := json.Marshal(activityDoc)
	if err != nil {
		return -1, err
	}
~~~

`json.marshal` gives me `[]byte` and I need a `io.Reader` to make an HTTP call, so I convert it like this:

~~~{.go caption="activty.go"}
strings.NewReader(string(bytes))
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
	return -1, err
}
~~~

And then making the request:

~~~{.go caption="activty.go"}
res, err := http.DefaultClient.Do(req)
if err != nil {
	return -1, err
}
~~~

`res` is my `http.Response` and I need to get my ID out of it if everything went well. It looks like this:

~~~{.go caption="activty.go"}
if res.Body != nil {
	defer res.Body.Close()
}
body, err := ioutil.ReadAll(res.Body)
if err != nil {
	return -1, err
}
~~~

To get the ID out of the response, I need to use `json.Unmarshal`:

~~~{.go caption="activty.go"}
var document IDDocument
err = json.Unmarshal(body, &document)
if err != nil {
	return -1, err
}
return document.ID, nil
~~~

<div class="notice--big--primary">

<!-- markdownlint-disable MD036 -->
**What I Learned: `json.Marshall` and  `io.reader` **

You can convert a struct back and forth to a `[]byte` of JSON using `json.Marshall` and `json.Unmarshal` like this:

``` go
byte := json.Marshal(someStruct)
json.Unmarshal(bytes, &someStruct)
```

Requests and Responses in the http package however work with `io.Reader` which looks like this:

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

`Retrieve` is mainly the same as `Insert` but in reverse -- I json.Marshal the ID and json.Unmarshal the activities struct. 

~~~{.go caption="activty.go"}
func (c *Activities) Retrieve(id int) (Activity, error) {
	...
	return document.Activity, nil
}
~~~

One differences though is we need to handle invalid IDs. Like this:

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

And with that I have a working client, though basic client. I'm going to add some light testing and then call it a day.

## Testing the Happy Path

I could write extensive unit tests for this, but important depends on `activityclient`. So instead I will just exercise the happy path with this script:

~~~{.bash caption="test.sh"}
#!/usr/bin/env sh
set -e

echo "=== Add Records ==="
./activityclient -add "overhead press: 70lbs"
./activityclient -add "20 minute walk"

echo "=== Retrieve Records ==="
./activityclient -get 0 | grep "overhead press"
./activityclient -get 1 | grep "20 minute walk"
~~~

Assuming the back-end service is up, and the client is built, this will test that `-add` is adding elements and that `-list` is retriveing them. If either is broken, the script won't exit cleanly.

## Continuous Integration

I can even hook this happy path up to CI fairly easily by extending my previous [Earthfile](https://github.com/adamgordonbell/cloudservices/blob/main/ActivityClient/Earthfile).

I'll create a `test` target for the client, and copy in client binary and the test script:

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

You can find more about how that works on the main [Earthly site](https://earthly.dev), but the important thing is now my GitHub Action will build the back-end service, the client, and then test them together using my shell script. It gives me a quick sanity check on the compatibility of my client that I can run on each new feature.

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/8600.png --alt {{  }} %}
<figcaption></figcaption>
</div>


### What's Next

There are two things I want to add to activity tracker next. First, I want to move to GRPC. Second, I need some sort of persistence - right now the service holds everything in memory.  

If you want to be notified about the next installment, sign up for the newsletter:

{% include cta/embedded-newsletter.html %}


## More stuff
JS MArshal and unMarshal
IO reader
 -