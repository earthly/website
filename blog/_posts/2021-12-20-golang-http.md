---
title: "Building a Golang JSON HTTP Server"
categories:
  - Tutorials
toc: true
newsletter_side: false
author: Adam
sidebar:
  nav: "activity-tracker"
internal-links:
 - golang json
 - golang http
excerpt: |
    Learn how to build a JSON HTTP server using Golang in this tutorial. Discover the basics of creating a Golang web service, handling HTTP requests, and working with JSON data.
last_modified_at: 2023-09-19
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and faster using containerization. Earthly can streamline your Golang build process, making your HTTP server projects a breeze. [Give it a go](/).**

If you want to build a simple JSON HTTP web service that runs natively on a Linux server, then Golang is a great choice. At least this is what I've been told, my coworkers are big fans and report having a small memory footprint, a shallow learning curve, and an excellent standard library.

So in this article, I'm going to give it a try with a simple project I've been wanting to build: an activity tracker. You see, I'm a bit out of shape, and I'd like to start tracking my activity levels. It will be a bit of a toy application, but I'm hoping it will encourage me to start adding more activity to sedentary winter habits.

( Maybe I should exercise as a first step instead, but coding this up seems more fun.)

I want my end result to be beautiful and easy to use, but to start with, I just need an API to insert and retrieve records.

I want inserting to look something like this:

~~~{.bash caption=">_"}
> curl -iX POST localhost:8080 -d \
'{"activity": {"description": "christmas eve bike class", 
"time":"2021-12-24T12:42:31Z"}}'
~~~

~~~{.merge-code}
HTTP/1.1 200 OK
{"id":1}
~~~

And I want to be able to retrieve previous activities by their auto-generated Id:

~~~{.bash caption=">_"}
> curl -X GET localhost:8080 -d '{"id": 1}'
~~~

~~~{.merge-code}
{"activity": {"description": "christmas eve class", 
time:"2021-12-24T12:42:31Z", "id":1}}
~~~

## Build a Simple GoLang HTTP Server

The first step towards building my web server is using `"net/http"` to listen on a port.

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
>  curl -iX GET localhost:8080
~~~

~~~{.merge-code}
HTTP/1.1 404 Not Found
Content-Length: 19

404 page not found
~~~

Posts work equally as well as GETs:

~~~{.bash caption=">_"}
> curl -iX POST localhost:8080
~~~

~~~{.merge-code}
HTTP/1.1 404 Not Found
Content-Length: 19

404 page not found
~~~

### Building HTTP Handlers in GoLang

404s may be the appropriate response to a query about my activity levels, but to return something informative for these `GET` and `POST` requests, I'll need to write handlers for them:

~~~{.go captionb="main.go"}
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

### Gorilla Web Toolkit

The [Gorilla web toolkit](https://www.gorillatoolkit.org/) is a collection of packages for working web protocols. `github.com/gorilla/mux` is an HTTP request multiplexer, basically a router, and is just a bit more flexible than the standard library's router.
</div>

Running this version, I can see that my handlers are working:

~~~{.bash caption=">_"}
> curl -X GET -s localhost:8080
~~~

~~~{.merge-code}
HTTP/1.1 200 OK
get
~~~

~~~{.bash caption=">_"}
> curl -X POST -s localhost:8080
~~~

~~~{.merge-code}
HTTP/1.1 200 OK
post
~~~

## Testing HTTP `GET` and `POST`

I'm a big fan of integration tests, and though our service isn't exactly doing much, it seems like this would be an easy time to write some end-to-end tests.

In fact, by combining a `curl` request with [ripgrep](https://github.com/BurntSushi/ripgrep)'s `-q` flag -- which will fail when no matches are found -- I can quickly write a shell script to test my end-points:

~~~{.bash caption="test.sh"}
#!/usr/bin/env sh

set -e

echo "=== Test GET ==="
curl -X GET -s localhost:8080 | rg -q "get" 

echo "=== Test POST ==="
curl -X POST -s localhost:8080 | rg -q "post"

echo "Success"
~~~

And I can also use [Earthly](https://earthly.dev/) to write a small build script that puts this service into a container and tests it's endpoints. Doing so may seem like overkill, but I'm going to build on this test case as we go.

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

What I've built up so far is on [GitHub](https://github.com/adamgordonbell/cloudservices/tree/v1-http-server/WebServer), but it doesn't do much. For my activity tracker to be useful, it will need to understand and store activities.

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
 ID          uint64    
}
~~~

I need a way to store my activity results. For now I'm just going to keep them in memory, in a slice.  

~~~{.go caption="internal/server/activity.go"}
type Activities struct {
 activities []Activity
}
~~~

If the service stops or crashes, I'll lose all my activity data, but I can use the slice offset as my auto-incrementing ID.

Doing that, I can write an insert function like this:

~~~{.go captionb="internal/server/activity.go"}
func (c *Activities) Insert(activity Activity) uint64 {
 activity.ID = uint64(len(c.activities))
 c.activities = append(c.activities, activity)
 return activity.ID
}
~~~

And retrieve is super simple as well:

~~~{.go captionb="internal/server/activity.go"}
func (c *Activities) Retrieve(id uint64) (Activity, error) {
 if id >= uint64(len(c.activities)) {
  return Activity{}, ErrIDNotFound
 }
 return c.activities[id], nil
}
~~~

If I get an invalid ID I just return an `ErrIDNotFound` error:

~~~{.go captionb="internal/server/activity.go"}
var ErrIDNotFound = fmt.Errorf("ID not found")
~~~

Now I just need to hook this up to the HTTP server and serialize the JSON.

### Updating The HTTP Server and Routing

At this point, it makes sense to take my HTTP server code out of main and move it to its own file. I will also create a struct for my `httpServer` and give it an 'Activities` field to hold onto its state.

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
type IDDocument struct {
 ID uint64 `json:"id"`
}
~~~

<figcaption>
*I use the struct field tag `json:"id"` to tell `encoding/json` how to decode and encode IDDocument back and forth from Golang to JSON.*
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
 Description string    `json:"description"`
 ID          uint64    `json:"id"`
}
~~~

Now I can add the insert handler:

~~~{.go captionb="internal/server/http.go"}
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

I use `json.NewDecoder` to decode the body of the request sent to the service, and if it doesn't decode, I write `http.StatusBadRequest`  to the `ResponseWriter`, which is a 400 Response.

It works like this:

~~~{.bash caption=">_"}
> curl -iX POST localhost:8080 -d "Not Valid"
~~~

~~~{.merge-code}
HTTP/1.1 400 Bad Request
invalid character 'N' looking for beginning of value
~~~

But if it's a valid response I can add it to my activities list and return the ID using `IDDocument`:

~~~{.go captionb="internal/server/http.go"}
func (s *httpServer) handlePost(w http.ResponseWriter, r *http.Request) {
  ...
 id := s.Activities.Insert(req.Activity)
 res := IDDocument{ID: id}
 json.NewEncoder(w).Encode(res)
}

~~~

We now have half our API working!

~~~{.bash caption=">_"}
> curl -X POST localhost:8080 -d \
'{"activity": {"description": "christmas eve class",
 time:"2021-12-24T12:42:31Z"}}'
~~~

~~~{.merge-code}
{"id":0}
~~~

### Get by ID JSON Decoding

For the `GET` request, I want to accept an ID via the `IDDocument` and return a 400 if I get something else:

~~~{.go captionb="internal/server/http.go"}
func (s *httpServer) handleGet(w http.ResponseWriter, r *http.Request) {
  var req IDDocument
 err := json.NewDecoder(r.Body).Decode(&req)
 if err != nil {
  http.Error(w, err.Error(), http.StatusBadRequest)
  return
 }
  ...
~~~

Then I retrieve my activity and assuming it exists, I write it to the `ResponseWriter` as an `ActivityDocument` :

~~~{.go captionb="internal/server/http.go"}
activity, err := s.Activities.Retrieve(req.ID)
 if err == ErrIDNotFound {
  http.Error(w, err.Error(), http.StatusNotFound)
  return
 }

 res := ActivityDocument{Activity: activity}
 json.NewEncoder(w).Encode(res)

~~~

Then I just update `main.go` to call this server:

~~~{.go caption="cmd/server/main.go"}
func main() {
 println("Starting listening on port 8080")
 srv := server.NewHTTPServer(":8080")
 srv.ListenAndServe()
}

~~~

And my original API, which was just a wish is now a reality:

~~~{.bash caption=">_"}
curl -X POST localhost:8080 -d \
'{"activity": {"description": "christmas eve bike class",
 "time":"2021-12-09T16:34:04Z"}}'
~~~

~~~{.merge-code}
{"id":1}
~~~

~~~{.bash captionw=">_"}
> curl -X GET localhost:8080 -d '{"id": 1}' 
~~~

~~~{.merge-code}
{"activity":{"time":"2021-12-09T16:34:04Z","description":"christmas eve bike 
class","id":15}
~~~

the whole thing, including some edge cases I left out is on [GitHub](https://github.com/adamgordonbell/cloudservices/tree/v1-http-server/ActivityLog).

If fact, I can now update my shell script `test.sh` to exercise these endpoints.

## End To End Testing

First, I can add in some test data:

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

curl -X GET localhost:8080 -d '{"id": 0}' | grep -q 'christmas eve bike class'
curl -X GET localhost:8080 -d '{"id": 1}' | grep -q 'cross country skiing'
curl -X GET localhost:8080 -d '{"id": 2}' | grep -q 'sledding'
~~~

And now, since I wrote that `Earthfile` that starts up the service and runs `test.sh` against it, it's simple to use GitHub Actions to test every commit!

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/1010.png --alt {{ GitHub Actions }} %}
<figcaption>Passing End to End tests on [GitHub](https://github.com/adamgordonbell/cloudservices/tree/v1-http-server/ActivityLog)</figcaption>
</div>

## That's a Wrap

There we go. I have a working service that I've put up on [GitHub](https://github.com/adamgordonbell/cloudservices/tree/v1-http-server/ActivityLog) with an active CI process. It doesn't persist its data, it doesn't allow me to access my activity log in any other way than by id, and it doesn't have a UI, but I'm starting to get a feel for how web services are built in Golang, which was the point.

As an activity tracker, what I have so far is pretty weak. But as a learning lesson, I've found it valuable.

Now I just have to start being active! Maybe building a command line client for this service will help.

{% include_html cta/bottom-cta.html %}

## Appendix

### Linting

In the first version of this example I used `Id` everywhere instead of `ID`, which is incorrect capitalization (per `go lint` and [Alex](/blog/authors/Alex/)). To prevent further style issues like this as I continue building this application I'm linting my code going forward using [`golangci-lint`](https://golangci-lint.run/) which with the [right configuration](https://github.com/adamgordonbell/cloudservices/blob/v1-http-server/ActivityLog/.golangci.yml) calls several go linters, including `go lint`.

### Errors

I hit a number of errors building this. If you hit them, here are the solutions.

| Error      | Solution |
| ----------- | ----------- |
| illegal base64 data at input byte      | I was using `[]byte` for my json Description. If you do this then base64 encoded data is expected. Switching to `string` fixed this.         |
| invalid character 't' looking for beginning of object key string   |  I was sending invalid JSON to my service. I needed to validate my input and found I wasn't quoting a string. |

### What's Next

Next up, I'm building a command-line client for this service to make it more user-friendly. I've got other features brewing in my mind, but I'll save that for later. Tossed around a few other improvements like using `gojsonschema` for better JSON validation and `net/http/httptest` for testing.

Speaking of Golang projects, you might want to check out [Earthly](https://www.earthly.dev/) for efficient, reproducible builds. It could be a valuable tool to streamline your development process.

If you want to be notified about the next installment, sign up for the newsletter:

{% include_html cta/embedded-newsletter.html %}
