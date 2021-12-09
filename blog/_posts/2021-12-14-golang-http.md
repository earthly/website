---
title: "Building a Golang JSON HTTP Server"
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - golang json
 - golang http
---

- [ ] Fix Grammarly Errors

If you want to build a simple JSON HTTP web service that runs natively on a linux server, then Go (often called GoLang) is a great language to choose.

At least this is what I've been told. My coworkers are big fans and report that it has a small memory footprint, a shallow learning curve and a great standard library.

So in this article I'm going to give it a try and I have a simple project in mind that I can use as an example, an activity tracker. You see, I'm out of shape and I'd like to start tracking my activity levels. It will be a bit of a toy application but I'm hoping it will be enough to encourage me to starting adding more activity to sedentary winter habits.

( Maybe I should actually exercise as a first step instead, but coding this up seems like more fun.)

I want my end result to be beautiful and easy to use but to start with I just need an simple API of inserting and retrieving records.

Inserting I want to look something like this:

``` bash
> curl -X POST localhost:8080 -d \
'{"activity": {"description": "christmas eve bike class", "time":"2021-12-24T12:42:31Z"}}'
```

And I want to be able to retrieve previous activities by their auto-generated Id:

``` bash
> curl -X GET localhost:8080 -d '{"id": 1}'
{"activity": {"description": "christmas eve class", time:"2021-12-24T12:42:31Z", "id":1}}
```

## Build a Simple GoLang HTTP Server

The first step towards building my web server is using `"net/http"` to start listening on a port.

~~~{.go caption="main.go"}
package main

import (
 "net/http"
)

func main() {
 srv := &http.Server{
  Addr: ":8080",
 }
 srv.ListenAndServe()
}
~~~

I can then run it like this:

~~~{.bash caption=">_"}
> go run main.go   
~~~

And verify that it is serving HTTP `GET` requests:

~~~{.bash caption=">_"}
>  curl -X GET localhost:8080
404 page not found
~~~

Posts work equally as well as GETs:

~~~{.bash caption=">_"}
> curl -X POST localhost:8080
404 page not found
~~~

### Building HTTP Handlers in GoLang

404s may be the appropriate response to a query about my activity levels but to return something informative for these `GET` and `POST` requests, I'll need to write handlers for them:

~~~{.go caption="main.go"}
func handleGet(w http.ResponseWriter, req *http.Request) {
 fmt.Fprintf(w, "get\n")
}

func handlePost(w http.ResponseWriter, req *http.Request) {
 fmt.Fprintf(w, "post\n")
}
~~~

And then import `github.com/gorilla/mux` and update our main function to route to these handlers:

~~~{.go caption="main.go"}
func main() {
 r := mux.NewRouter()
 r.HandleFunc("/", handlePost).Methods("POST")
 r.HandleFunc("/", handleGet).Methods("GET")

 srv := &http.Server{
  Addr:    ":8080",
  Handler: r,
 }
 srv.ListenAndServe()
}
~~~

<div class="notice--info">
ℹ️ **Gorilla web toolkit**

The [Gorilla web toolkit](https://www.gorillatoolkit.org/) is a collection of packages for working web protocols. `github.com/gorilla/mux` is a HTTP request multiplexer, basically a router, and is just a bit more flexible than the standard library's router.
</div>

Running this version, I can see that my handlers are working:

~~~{.bash caption=">_"}
> curl -X GET -s localhost:8080
get
> curl -X POST -s localhost:8080
post
~~~

## Testing HTTP `GET` and `POST`

I'm a big fan of integration tests and though our service isn't exactly doing much it does seem like this would be an easy time to write some end to end tests.

If fact, by combining a `curl` request with [ripgrep](https://github.com/BurntSushi/ripgrep)'s `-q` flag -- which will fail when no matches are found -- I can quickly write a shell script to test my end-points:

~~~{.bash caption="test.sh"}
#!/usr/bin/env sh

set -e

echo "=== Test GET ==="
curl -X GET -s localhost:8080 | rg -q "get" 

echo "=== Test POST ==="
curl -X POST -s localhost:8080 | rg -q "post"

echo "Success"
~~~

And I can also use [Earthly](https://earthly.dev/) to write a small build script that puts this service into a container, and tests it's end points. This may seem like overkill, but I'm going to build on this test case as we go.

~~~{.dockerfile caption="Earthfile"}
test:
    FROM +test-deps
    COPY test.sh .
    WITH DOCKER --load agbell/cloudservices/webserver=+docker
        RUN  docker run -d -p 8080:8080 agbell/cloudservices/webserver && \
                ./test.sh
    END
~~~

<figcaption>Test my containerized service</figcaption>

What I've built up so far is on [GitHub](https://github.com/adamgordonbell/cloudservices/tree/main/WebServer) but it doesn't do much. For my activity tracker to be useful it's going to need to understand and store activities.

So let's move on to my activity data structures.

## In-Memory Service Data

The way I am going represent activities in Golang is to create a new package for my server ( in `internal/server` ) and in it create an `activity.go` with an `Activity` struct:

~~~{.go caption="internal/server/activity.go"}

package server

import (
 "fmt"
 "sync"
 "time"
)

type Activity struct {
 Time        time.Time 
 Description string
 Id          uint64    
}
~~~

I need a way to store my activity results. For now I'm just going to keep them in memory, in a slice.  

~~~{.go caption="internal/server/activity.go"}
type Activities struct {
 activities []Activity
}
~~~

If the service is stops or crashes I'll lose all my activity data, but on the plus side I can simply use the slice offset as my auto-incrementing Id.

Doing that, I can write an insert function like this:

~~~{.go caption="internal/server/activity.go"}

func (c *Activities) Insert(activity Activity) uint64 {
 activity.Id = uint64(len(c.activities))
 c.activities = append(c.activities, activity)
 return activity.Id
}
~~~

And retrieve is super simple as well:

~~~{.go caption="internal/server/activity.go"}

func (c *Activities) Retrieve(id uint64) (Activity, error) {
 if id >= uint64(len(c.activities)) {
  return Activity{}, ErrIdNotFound
 }
 return c.activities[id], nil
}
~~~

If I get an invalid Id I just return an `ErrIdNotFound` error:

~~~{.go caption="internal/server/activity.go"}

var ErrIdNotFound = fmt.Errorf("Id not found")
~~~

Now I just need to hook this up to the HTTP server and do the JSON serialization.

### Updating The HTTP Server and Routing

At this point I think it makes sense to take my HTTP server code out of main and move it to it's own file. I also am going to create a struct for my `httpServer` and give it an 'Activities` field to hold onto its state.

~~~{.go caption="internal/server/http.go"}
package server

import (
 "net/http"

 "github.com/gorilla/mux"
)

type httpServer struct {
 Activities *Activities
}

func NewHTTPServer(addr string) *http.Server {
 server := &httpServer{
  Activities: &Activities{},
 }
 r := mux.NewRouter()
 r.HandleFunc("/", server.handlePost).Methods("POST")
 r.HandleFunc("/", server.handleGet).Methods("GET")
 return &http.Server{
  Addr:    addr,
  Handler: r,
 }
}
~~~

## JSON Encoding And Decoding in GoLang

I also need my server to understand the JSON formats of my API. So to represent `{"id": 1}` I will create this struct:

~~~{.go caption="internal/server/http.go"}
type IdDocument struct {
 Id uint64 `json:"id"`
}
~~~

<figcaption>
*The struct field tag `json:"id"` will be used by `encoding/json` to decode and encode IdDocument back and forth from Golang to JSON.*
</figcaption>

Similarly to represent a JSON activity like `{"activity": {"description": "christmas eve class", time:"2021-12-24T12:42:31Z", "id":1}}`, I need an `ActivityDocument`:

~~~{.go caption="internal/server/http.go"}
type ActivityDocument struct {
 Activity Activity `json:"activity"`
}
~~~

And finally, I need to head back to my Activity service to add field tags for `Activity` like so:

~~~{.go caption="internal/server/activity.go"}
type Activity struct {
 Time        time.Time `json:"time"`
 Description []byte    `json:"description"`
 Id          uint64    `json:"id"`
}
~~~

Now I can add the insert handler:

~~~{.go caption="internal/server/http.go"}

func (s *httpServer) handlePost(w http.ResponseWriter, r *http.Request) {
 var req ActivityDocument
 err := json.NewDecoder(r.Body).Decode(&req)
 if err != nil {
  http.Error(w, err.Error(), http.StatusBadRequest)
  return
 }
  ...
}
~~~

I use `json.NewDecoder` to decode the body of the request sent to the service and if it doesn't decode, I write `http.StatusBadRequest`  to the `ResponseWriter`, which is a 400 Response.

It works like this:

```
> curl -X POST localhost:8080 -d \
'{"this":"is","all":"wrong"}'
//todo show result
```

But if it's a valid response I can add it to my activities list and return the Id using `IdDocument`:

~~~{.go caption="internal/server/http.go"}

func (s *httpServer) handlePost(w http.ResponseWriter, r *http.Request) {
  ...
 id := s.Activities.Insert(req.Activity)
 res := IdDocument{Id: id}
 json.NewEncoder(w).Encode(res)
}

~~~

We now have half our API working!

``` bash
> curl -X POST localhost:8080 -d \
'{"activity": {"description": "christmas eve class", time:"2021-12-24T12:42:31Z"}}'
{"id":0}
```

### Get by ID JSON Decoding

For the `GET` request, I want to accept an Id via the `IdDocument` and return a 400 if I get something else:

~~~{.go caption="internal/server/http.go"}
func (s *httpServer) handleGet(w http.ResponseWriter, r *http.Request) {
  var req IdDocument
 err := json.NewDecoder(r.Body).Decode(&req)
 if err != nil {
  http.Error(w, err.Error(), http.StatusBadRequest)
  return
 }
  ...
~~~

Then I retrieve my activity and assuming it exists, I write it to the `ResponseWriter` as an `ActivityDocument` :

~~~{.go caption="internal/server/http.go"}
activity, err := s.Activities.Retrieve(req.Id)
 if err == ErrIdNotFound {
  http.Error(w, err.Error(), http.StatusNotFound)
  return
 }

 res := ActivityDocument{Activity: activity}
 json.NewEncoder(w).Encode(res)

~~~

Then I just update `main.go` to call this server:

~~~{.go caption="cmd/server/main.go"}
func main() {
 println("Starting on http://localhost:8080")
 srv := server.NewHTTPServer(":8080")
 srv.ListenAndServe()
}

~~~

And my original API, that was just a wish is now a reality:

```
curl -X POST localhost:8080 -d \
'{"activity": {"description": "christmas eve bike class", "time":"2021-12-09T16:34:04Z"}}'
{"id":1}
> curl -X GET localhost:8080 -d '{"id": 1}' 
{"activity":{"time":"2021-12-09T16:34:04Z","description":"christmas eve bike class","id":15}
```

the whole thing, including some edge cases I left out is on [GitHub](https://github.com/adamgordonbell/cloudservices/tree/main/ActivityLog).

If fact, I can now update my shell script `test.sh` to exercise these endpoints.

## End to End Testing

First I can add in some test data:

~~~{.bash caption="test.sh"}
#!/usr/bin/env sh
set -e

echo "=== Insert Test Data ==="

curl -X POST localhost:8080 -d \
'{"activity": {"description": "christmas eve bike class", "time":"2021-12-09T16:34:04Z"}}'

curl -X POST localhost:8080 -d \
'{"activity": {"description": "cross country skiing is horrible and cold", "time":"2021-12-09T16:56:12Z"}}'

curl -X POST localhost:8080 -d \
'{"activity": {"description": "sledding with nephew", "time":"2021-12-09T16:56:23Z"}}'

~~~

Then I can get test that I can get them back:

~~~{.bash caption="test.sh"}
echo "=== Test Descriptions ==="

curl -X GET localhost:8080 -d '{"id": 0}' | rg -q 'christmas eve bike class'
curl -X GET localhost:8080 -d '{"id": 1}' | rg -q 'cross country skiing'
curl -X GET localhost:8080 -d '{"id": 2}' | rg -q 'sledding'
~~~

And since that is just testing the descriptions I should also check that `id` and `time` are being stored and retrieved:

~~~{.bash caption="test.sh"}
echo "=== Test Other Fields ==="
curl -X GET localhost:8080 -d '{"id": 0}' | rg -q '2021-12-09T16:34:04Z'
curl -X GET localhost:8080 -d '{"id": 1}' | rg -q '"id":1'
~~~

And now, since I wrote that `Earthfile` that starts up the service and runs `test.sh` against it, it's simple to use GitHub Actions to test every commit!

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/1010.png --alt {{ GitHub Actions }} %}
<figcaption>Passing End to End tests on [GitHub](https://github.com/adamgordonbell/cloudservices/tree/main/ActivityLog)</figcaption>
</div>


## That is a Wrap

There we go. I have a working service and I put it up on [GitHub](https://github.com/adamgordonbell/cloudservices/tree/main/ActivityLog) with a working CI process. It doesn't persist it's data, it doesn't allow me to access my activity log in any other way than by id, and it doesn't have a UI, but I'm starting to get the feel for how web services are built in Go, which was really the point.

As an activity tracker, what I have so far is pretty weak. But as a learning lesson, I've found it valuable.

Now I just have to start being active! Maybe another coding project will help.

{% include cta/cta1.html %}

<!-- Errors:
`illegal base64 data at input byte 9`
`invalid character 't' looking for beginning of object key string`

Improvements:
- how to validate the input and make things required? -->
