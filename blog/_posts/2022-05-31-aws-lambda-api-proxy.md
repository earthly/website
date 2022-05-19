---
title: "AWS Lambda Rest API Backend In Golang"
categories:
  - Tutorials
toc: true
author: Adam
sidebar:
  nav: "lambdas"
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

Keywords:
- api proxy
- aws lambda http request example
- rails lambda

- Provisioned Concurrency
   - https://aws.amazon.com/lambda/pricing/#Provisioned_Concurrency_Pricing

- single provisioned concurrency would mean 0.0000041667 * 604800 * 4.25 in a month

aws lambda web application
aws lambda rest api
serverless api gateway
serverless backend
aws backend

---
Welcome back. The earlier post on containers in lambdas showed up on hacker news and got some fun questions about using Lambdas to scale out stateless webapps. Here is one question: 

> Is it possible to host an app like Django inside container on lambda? This could help the Django/postgres apps to scale horizontally easily. - https://news.ycombinator.com/item?id=31183109

The answer is Yes! There are frameworks and libraries out there to help do this in Javascript with Express, in Python with Django and with Ruby on Rails. 

Today, I'm going to show how to do it in GoLang with just the standard HTTP lib and gorrila Mux for setting up routing rules. At the end, we will have a containerized app that can be called like a norma HTTP app locally and work in AWS running in a Lambda.

<div class="notice--info">

### Side Note: Other Languages

* If you'd like to spin up a Rub on Rails App on Lambda, bla is here to help
* For Django projects, or anything using ASGI both [magnum](https://github.com/jordaneremieff/mangum) and [apig-wsgi](https://pypi.org/project/apig-wsgi/)
* For Node.js try ...

</div>

## What we need to do

Our goal is be able to write a normal golang http webservice that we can start-up and make requests against, but have it work as a lambda when running behind the AWS API Gateway. 

The challenge of this is that [as seen previously]() HTTP requests from API Gateway come as JSON documents like this:

~~~{.json caption="lambda input"}
{
  "queryStringParameters": {
    "url": "https://earthly.dev/blog/golang-monorepo/"
  }
}
~~~

And responses get returned like this:

~~~{.json caption="lambda output"}
{
 "statusCode" : 500,
  "headers" : {
    "content-type": "text/plain; charset=utf-8"
  },
  "body" : "Some error fetching the content"
}
~~~

So one challegens is that we want to match our routes and write handlers using `http.ResponseWriter` like this:

```
    http.HandleFunc("/my-route", func(w http.ResponseWriter, r *http.Request) {
        io.WriteString(w, "Hello")
    })
```

And somehow get them translated into the format that lambda requires. Thankfully, `AWS Lambda Go API Proxy` is here to do all the heaving lifting for us.

A simple hello-world looks like this:
```
package main

import (
    "io"
    "net/http"

    "github.com/aws/aws-lambda-go/lambda"
    "github.com/awslabs/aws-lambda-go-api-proxy/httpadapter"
)

func main() {
    http.HandleFunc("/my-route", func(w http.ResponseWriter, r *http.Request) {
        io.WriteString(w, "Hello")
    })

    lambda.Start(httpadapter.New(http.DefaultServeMux).ProxyWithContext)
}
```

I'm going port the Text-mode service to use this framework and if you want to skip ahead, the [code is here]().

> Lambda is Greek for CGI script https://news.ycombinator.com/item?id=31183176

Here is our orignal, non-lambda specific code:

```
func main() {
    app := textmode.NewApp()
    r := mux.NewRouter()

    r.HandleFunc("/text-mode", app.Handler)
    r.HandleFunc("/", HomeHandler)

    log.Println("Starting up on own")
    srv := &http.Server{
        Addr:    ":8080",
        Handler: r,
    }
    _ = srv.ListenAndServe()
}
```

The first thing I need to do is bring in bla

```
func main() {
    app := textmode.NewApp()
    r := mux.NewRouter()

    r.HandleFunc("/text-mode", app.Handler)
    r.HandleFunc("/", HomeHandler)

    log.Println("Starting up on own")
-   srv := &http.Server{
-       Addr:    ":8080",
-       Handler: r,
-   }
-   _ = srv.ListenAndServe()
+   adapter := gorillamux.NewV2(r)
+   lambda.Start(adapter.ProxyWithContext)
}
```

Deploy to lambda and test it out. (I'll cover the setup soon).

## Failure

But once this is deployed, I get 404s:

```
$ curl https://earthly-tools.com/text-mode
404 Not Found
```

To figure out what going on, I'm going to add more information to my 404 errors:

```
func main() {
    app := textmode.NewApp()
    r := mux.NewRouter()
+   r.NotFoundHandler = http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
+       log.Println("Not found", r.RequestURI)
+       http.Error(w, fmt.Sprintf("Not found: %s", r.RequestURI), http.StatusNotFound)
+    })

    log.Println("Starting up on own")
    adapter := gorillamux.NewV2(r)
    lambda.Start(adapter.ProxyWithContext)
}
```
And then I can see the problem:
```
$ curl https://earthly-tools.com/text-mode
Not found: /default/text-mode
```

The route my service is getting has `default` on the front of it. It's possible there is a some way to configure AWS API gateway to remove this, but it's pretty easy to deal with in service: I just create a prefix path for all my routes.

```
	s := r.PathPrefix("/default").Subrouter()
	s.HandleFunc("/text-mode", app.Handler)
	s.HandleFunc("/", HomeHandler)

```

And with and a bit of deployment magic, my services routing works in the Lambda. My problem now is that it doesn't work outside of Lambda, and I'll tackle that next, but first let me show you how I deployed it and got it configured in AWS.

## Deployment Shenanigans 

