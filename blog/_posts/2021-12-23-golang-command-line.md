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

[Last time] I built a REST service for storing activities. Now I'm going to try to figure out how to build a command line client for it.

First I create a new folder for my client:
```
$ go mod init github.com/adamgordonbell/cloudservices/activityclient
```

I want my CLI to work something like this:
```
$ activity --add "lifted weights"
Added as 0
$ activity --list
ID:0  lifted weights  date
```
Or I can get specific activities:
```
$ activity --get 0
ID:0  lifted weights  date
```

The actual backend doesn't support `list` yet so we will skip that one for now.

## Command Line Flags

I'm going to start with the command line flags before I worry about talking to backend. For now, know we have a JSON client called `activitiesClient`.


Parsing command-line args is pretty simple, thanks to the `flag` package:

````
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

info box
I could just use `go run` but I'm going instead compile with 
`go build -o build/activityclient cmd/client/main.go` and use `activityclient`. Everything is in github.


I'm exiting 1, as this case will also be hit for any options the program doesn't understand -- which gives a helpful reminder of usage.

```
$ ./activityclient --unknown --flags
Usage of activityclient:
  -add
        Add activity
  -get
        Get activity
exit status 1
```

Now lets do Add. First thing I need to do is validate my input:

```
	case *add:
		if len(os.Args) != 3 {
			println(`Usage: --add "message"`)
			os.Exit(1)
		}
```

So that if I forget an arg, I get informed:
```
$ ./activityclient --add      
Usage: --add "message"
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
./activityclient --add "overhead press: 70lbs"
Error: Post "http://localhost:8080/": dial tcp [::1]:8080: connect: connection refused
```

With that in place ( and the json client, which I'll cover next) it's easy to add items:
```
$ go build -o build/activityclient cmd/client/main.go
$  ./activityclient --add "overhead press: 70lbs"
Added: {Time:2021-12-20 14:40:23.264457 -0500 EST m=+0.000422247 Description:overhead press: 70lbs ID:0} as 0
```

Get is very similar. 

## Get

Get will work like this:

```
$ ./activityclient --get 0                      
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
./activityclient --get one
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



## Mire stuff
IO reader
 -