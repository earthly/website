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

## Draft.dev Article Checklist

- [ ] Add in Author page
- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
  - Would any images look better `wide` or without the `figcaption`?
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links
- [ ] Add Earthly `CTA` at bottom `{% include cta/cta1.html %}`

## Start

[Last time](/blog/golang-http/) I built a REST service for storing activities. Now I'm going to try to figure out how to build a command line client for it.

First I create a new folder for my client:
```
$ go mod init github.com/adamgordonbell/cloudservices/activityclient
```

I want my CLI to work something like this:
```
$ activity -add "lifted weights"
Added as 0
$ activity -list
ID:0  lifted weights  date
```
Or I can get specific activities:
```
$ activity -get 0
ID:0  lifted weights  date
```

The actual backend doesn't support `list` yet so we will skip that one for now.

## Command Line Flags

I'm going to start with the command line flags before I worry about talking to backend. For now, know we have a JSON client called `activitiesClient`.


Parsing command-line args is pretty simple, thanks to the `flag` package:

```
func main() {
	add := flag.Bool("add", false, "Add activity")
	get := flag.Bool("get", false, "Get activity")

	flag.Parse()

```

After setting up the flags, I can just use a case statement to decide what to do:

```
switch {
	case *get:
		// get case

	case *add:
 	   // add case

	default:
		flag.Usage()
		os.Exit(1)
	}

```
The default case is the simplest to explain. If neither flag is given, I ask flag to print to `flag.Usage()` which looks like this:

```
$ go run cmd/client/main.go
Usage of activityclient:
  -add
        Add activity
  -get
        Get activity
exit status 1
```

<div class="notice--info">

ℹ️ **`go run` and `go build`**

I could continue to use `go run` like above while working on the CLI tool but I'm going instead compile it (`go build -o build/activityclient cmd/client/main.go`) and use `activityclient`.
</div>


I'm exiting 1, as this case will also be hit for any options the program doesn't understand -- which gives a helpful reminder of usage:

```
$ ./activityclient -unknown -flags
Usage of activityclient:
  -add
        Add activity
  -get
        Get activity
exit status 1
```

Now lets do `-add`. First thing I need to do is validate my input:

```
	case *add:
		if len(os.Args) != 3 {
			println(`Usage: -add "message"`)
			os.Exit(1)
		}
```

So that if I forget an arg, I get informed:
```
$ ./activityclient -add      
Usage: -add "message"
exit status 1
```

After that, if the argument count is correct, I just to create my actvity and try to add it:

```
	a := client.Activity{Time: time.Now(), Description: os.Args[2]}
	id, _ := activitiesClient.Insert(a)
```

Actually, there are all kinds of things that can go wrong inserting records, so I'd better add error checking:

```
	id, err := activitiesClient.Insert(a)
	if err != nil {
		println("Error:", err.Error())
		os.Exit(1)
	}
```
This is helpful when I forget to start up the service:
```
./activityclient -add "overhead press: 70lbs"
Error: Post "http://localhost:8080/": dial tcp [::1]:8080: connect: connection refused
```

With that in place ( and the json client, which I'll cover last) it's easy to add items:
```
$ go build -o build/activityclient cmd/client/main.go
$  ./activityclient -add "overhead press: 70lbs"
Added: {Time:2021-12-20 14:40:23.264457 -0500 EST m=+0.000422247 Description:overhead press: 70lbs ID:0} as 0
```

## Get

Get is very similar to Add. It will work like this:

```
$ ./activityclient -get 0                      
{Time:2021-12-20 14:59:51.723453 -0500 EST Description:overhead press: 70lbs ID:0}
```

The first thing I need to do is parse the id into an int:

```
case *get:
	id, err := strconv.Atoi(os.Args[2])
	if err != nil {
		println("Invalid Offset: Not an integer")
		os.Exit(1)
	}
```
Which works like this:
```
./activityclient -get one
Invalid Offset: Not an integer
```

Then I retrieve from the JSON client and handle any errors:
```
a, err := activitiesClient.Retrieve(id)
if err != nil {
	println("Error:", err.Error())
	os.Exit(1)
}
```
Then I print activity:
```
fmt.Printf("Added: %+v as %d\n", a, id)
```

And the command-line part is complete. 

## JSON Client

For the JSON client, I need the structs I used in the [JSON service](/blog/golang-http/) article. I'll just copy pasta them in:

```
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

```
My activities JSON client is going to be called `internal/client/activity` and it needs the URL for my server in order to make requests:

```
type Activities struct {
	URL string
}
```

First thing I need to write in my activity client is insert. I wrap my `activity` in an document and use json.Marshal to convert it:

```
func (c *Activities) Insert(activity Activity) (int, error) {
	activityDoc := ActivityDocument{Activity: activity}
	bytes, err := json.Marshal(activityDoc)
	if err != nil {
		return -1, err
	}

```

`json.marshal` gives me `[]byte` and I need a `io.Reader` to make an HTTP call, so I convert it like this:

```
strings.NewReader(string(bytes))
```
The HTTP call I want to make looks like this:

```
curl -X POST -s localhost:8080 -d \
'{"activity": {"description": "christmas eve bike class", "time":"2021-12-09T16:34:04Z"}}'
```

I can do this by first creating a request:

```
req, err := http.NewRequest(http.MethodPost, c.URL, jsonContent)
	if err != nil {
		return -1, err
	}
```
And then making the request:

```
res, err := http.DefaultClient.Do(req)
	if err != nil {
		return -1, err
	}
```
`res` is my `http.Response` and I need to get my ID out of it if everything went well. It looks like this:

```
if res.Body != nil {
	defer res.Body.Close()
}
body, err := ioutil.ReadAll(res.Body)
if err != nil {
	return -1, err
}
```
To get the ID out of the response, I need to use `json.Unmarshal`:

```
var document IDDocument
	err = json.Unmarshal(body, &document)
	if err != nil {
		return -1, err
	}
	return document.ID, nil
```

// what I learned

## Status Codes

`Retrieve` is mainly the same as `Insert` but in reverse -- I json.Marshal the ID and json.Unmarshal the activities struct. 

```
func (c *Activities) Retrieve(id int) (Activity, error) {
	...
	return document.Activity, nil
}
```

One differences though is we need to handle invalid IDs. Like this:

```
./activityclient --get 100
Error: Not Found
```

Since the service returns 404s for those, once I have `http.Response`  I just need to status codes:

```
	if res.StatusCode == 404 {
		return document.Activity, errors.New("Not Found")
	}
```

And with that I have a working client. I'm going to add some light testing and then call it a day.

## Test the Happy Path

I could write extensive unit tests for this, but nothing turns on my implementation so instead I will just exercise the happy path with this script:

```
#!/usr/bin/env sh
set -e

echo "=== Add Records ==="
./activityclient -add "overhead press: 70lbs"
./activityclient -add "20 minute walk"

echo "=== Retrieve Records ==="
./activityclient -get 0 | grep "overhead press"
./activityclient -get 1 | grep "20 minute walk"
```

Assuming the back-end service is up, and the client is built this will test that `-add` is adding elements and that `-list` is retrieveing them. If either break, the script won't exit cleanly.

## Continuous Integration

I can even hook this happy path up to CI fairly easily by extending my previous [Earthfile](https://github.com/adamgordonbell/cloudservices/blob/main/ActivityClient/Earthfile). 

I'll create a `test` target for the client, and copy in client binary and the test script:
```
test:
    FROM +test-deps
    COPY +build/activityclient ./activityclient
    COPY test.sh .
```

Then I'll start-up the docker container for the service (using its GitHub path) and run `test.sh`:
```
    WITH DOCKER --load agbell/cloudservices/activityserver=github.com/adamgordonbell/cloudservices/ActivityLog+docker
        RUN  docker run -d -p 8080:8080 agbell/cloudservices/activityserver && \
                ./test.sh
    END
```
You can find more about how that work on the main earthly site, but the important for my purpose is now my GitHub Action will build the back-end service, the client and then test them together using my shell script. It gives me a quick sanity check on the compatiblity of my client.

// insert picture


### What's Next

There are two things I want to add to activity tracker next. First, I want to move to GRPC. Second is I need some sort of persistence - right now everything is held in memory.  

If you want to be notified about the next installment, sign up for the newsletter:

{% include cta/embedded-newsletter.html %}


## More stuff
JS MArshal and unMarshal
IO reader
 -