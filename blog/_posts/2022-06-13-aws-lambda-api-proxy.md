---
title: "AWS Lambda Rest API Backend In Golang"
categories:
  - Tutorials
toc: true
author: Adam
sidebar:
  nav: "lambdas"
excerpt: |
    Learn how to run a full REST HTTP API in a single AWS Lambda using Golang. Discover the advantages of this approach and how to handle routing and requests using the AWS Lambda Go API Proxy.
last_modified_at: 2024-04-13
---
**This article explains the creation of Lambda-based REST APIs. Earthly streamlines the CI pipeline for GoLang developers using AWS Lambda functions. [Learn more about Earthly](https://cloud.earthly.dev/login).**

Welcome back to a series on AWS Lambdas. Today I'll be running a full REST HTTP API in a single lambda. Also, I'll discuss why you might want to do so – there are some exciting advantages to this approach.

## Background

An earlier post on [containers in lambdas](/blog/aws-lambda-docker/) showed up on hacker news and got some fun questions about using Lambdas to scale-out stateless web apps. Here is one question:

> Is it possible to host an app like Django inside container on lambda? This could help the Django/postgres apps to scale horizontally easily. [^1]

[^1]: [source](https://news.ycombinator.com/item?id=31183109)

I can't see why this wouldn't work. But before digging in myself I asked around online.

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Is anyone hosting a full CRUD type app with routing and persisting as an AWS Lambda? <br><br>And if so, how is that going?</p>&mdash; Adam Gordon Bell 🤓 (@adamgordonbell) <a href="https://twitter.com/adamgordonbell/status/1527268246533165056?ref_src=twsrc%5Etfw">May 19, 2022</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

The resounding answer I got was Yes! There are frameworks and libraries to help run serverless backends in single lambdas. It's possible in JavaScript with Express, Python with Django, Ruby on Rails and probably more.

The low cost was one of the most stated reasons for using this approach:

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">Keep going! I think it&#39;s a promising architecture for mid-size applications and could be really cheap</p>&mdash; Nomad  (@nomad_ok) <a href="https://twitter.com/nomad_ok/status/1527426967720673293?ref_src=twsrc%5Etfw">May 19, 2022</a></blockquote> <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

<figcaption>With pricing at 20 cents per million requests and no minimum usage, running an HTTP service on a lambda is a low-cost solution.</figcaption>

So today, I will show how to do it in GoLang with just the standard HTTP lib and Gorilla Mux for setting up routing rules. We will have a containerized app that can be called like a standard HTTP app locally and still work in AWS, running in a Lambda.

<div class="notice--info">

### Side Note: Other Languages

- If you'd like to spin up a Ruby on Rails App on Lambda, [Lamby](https://lamby.custominktech.com/) is here to help
- For Django projects or anything using ASGI, both [magnum](https://github.com/jordaneremieff/mangum) and [apig-wsgi](https://pypi.org/project/apig-wsgi/)
- For Node.js, [`serverless-express`](https://github.com/vendia/serverless-express) seems to be a great option.

</div>

## What We Need To Do

Our goal is to be able to write a normal Golang HTTP web-service that we can start-up and make requests against but run it as a lambda when behind the AWS API Gateway.

The challenge of this is that, [as seen previously](/blog/aws-lambda-docker/), HTTP requests from API Gateway come as JSON documents like this:

~~~{.json caption="lambda input"}
{
  "queryStringParameters": {
    "url": "https://earthly.dev/blog/golang-monorepo/"
  }
}
~~~

<figcaption>Example AWS Lambda HTTP Request</figcaption>

And responses need to get returned like this:

~~~{.json caption="lambda output"}
{
 "statusCode" : 500,
  "headers" : {
    "content-type": "text/plain; charset=utf-8"
  },
  "body" : "Some error fetching the content"
}
~~~

<figcaption>Example AWS Lambda HTTP Response</figcaption>

This is not how HTTP services send and receive. I want to match use `http.ResponseWriter` like this:

~~~{.go caption="main.go"}
    http.HandleFunc("/my-route", func(w http.ResponseWriter, r *http.Request) {
        io.WriteString(w, "Hello")
    })
~~~

And somehow have that translated into the lambda message format. Thankfully, `AWS Lambda Go API Proxy` is here to help.

A simple hello-world looks like this:

~~~{.go caption="main.go"}
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
~~~

It proxies the requests and responses, converts them to the proper format, and communicates with the Lambda runtime. I'm going port the [Text-mode service](/blog/text-mode/) to use this framework, and if you want to skip ahead, the [code is on GitHub](https://github.com/earthly/cloud-services-example/tree/aws-lambda-2).

> Lambda is Greek for CGI script [^3]

[^3]: [source](https://news.ycombinator.com/item?id=31183176)

Here is our original, non-lambda specific code:

~~~{.go caption="main.go"}
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
~~~

The first thing I need to do is bring in `aws-lambda-go-api-proxy`:

~~~{.diff caption="main.go"}
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
~~~

I then deploy to Lambda and test it out. (I'll cover the how of AWS setup soon).

## Failure

But once this is deployed, I get 404s:

~~~{.bash caption=">_"}
$ curl https://earthly-tools.com/text-mode
404 Not Found
~~~

To figure out what going on, I need to add more information to my 404 errors:

~~~{.diff caption="main.go"}
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
~~~

And then I can see the problem:

~~~{.bash caption=">_"}
$ curl https://earthly-tools.com/text-mode
Not found: /default/text-mode
~~~

The route my service is getting is prefixed with `default`. However, I can work around this by creating a prefix path for all my routes.

(It's possible there is a some way to configure AWS API gateway to remove this, but I didn't find it.)

~~~{.go caption="main.go"}
 s := r.PathPrefix("/default").Subrouter()
 s.HandleFunc("/text-mode", app.Handler)
 s.HandleFunc("/", HomeHandler)
~~~

And with a bit of deployment magic, my service's routing works in the Lambda.

~~~{.bash caption=">_"}
$ curl https://earthly-tools.com/text-mode | head -n 15
~~~

~~~{.merge-code}
Earthly.dev Presents:                                                                                              

  _____                 _       
 |_   _|   ___  __  __ | |_     
   | |    / _ \ \ \/ / | __|    
   | |   |  __/  >  <  | |_     
   |_|    \___| /_/\_\  \__|    
                                
  __  __               _        
 |  \/  |   ___     __| |   ___ 
 | |\/| |  / _ \   / _` |  / _ \
 | |  | | | (_) | | (_| | |  __/
 |_|  |_|  \___/   \__,_|  \___|
~~~

However, my next problem is getting this to work outside a Lambda. But first, let me show you how I deployed it and configured it in AWS.

## Deployment Shenanigans

To deploy a container as a lambda in AWS follow the steps from [my previous guide] and you should end up with a lambda that is backed by an image sitting in Elastic Container Registry (ECR) and can be updated with an Earthfile target (or equivalent bash script) like this:

~~~{.docker caption="Earthfile"}
deploy:
    FROM amazon/aws-cli
    ARG AWS_PROFILE=earthly-dev
    RUN --mount=type=secret,target=/root/.aws/config,id=+secrets/config \
        --mount=type=secret,target=/root/.aws/credentials,id=+secrets/credentials \
        --no-cache \
        aws lambda update-function-code \
            --region us-east-1 \
            --function-name lambda-api \
            --image-uri 459018586415.dkr.ecr.us-east-1.amazonaws.com/lambda-api:latest
~~~

<figcaption>Update Lambda Function</figcaption>

So the big difference from the previous solution on the AWS side is how API Gateway is configured. Instead of binding to a specific API gateway route, I want to bind to all routes and handle the routing in go. To do this, I set up a route of the form `{term+}` where term can be anything, and map it to my Lambda.

<div>
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/1340.png --alt {{ AWS API Gateway Route }} %}
<figcaption>API Gateway Route</figcaption>
</div>

And that is the only change needed.

(According to AWS Docs, It's also possible to map the existing `$default` route to Lambda and achieve the same results. Unfortunately, I had trouble getting that to work.)

<div class="notice notice--big">

### Alternate Ending: Lambda Function URL

AWS Lambdas have a new feature called 'Function URLs', one-off URLs for each function. They work very much like setting up API Gateway and routing all paths to a single lambda, but they can be set up in a single step.

<div>
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/2100.png %}
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/2050.png %}
<figcaption>Function URLs can be created under Lambda Configuration.</figcaption>
</div>

Function URLs work wonderfully, and nothing extra is appended onto the route, so to use them, you don't need to assume `default` will be part of the route.

~~~{.bash caption=""}
$ curl https://e5esd6waj5xra75atmg3t3iooq0pwxnp.lambda-url.us-east-1.on.aws/default/text-mode | head -n 15
Earthly.dev Presents:                                                                                              

  _____                 _       
 |_   _|   ___  __  __ | |_     
   | |    / _ \ \ \/ / | __|    
   | |   |  __/  >  <  | |_     
   |_|    \___| /_/\_\  \__|    

  __  __               _        
 |  \/  |   ___     __| |   ___ 
 | |\/| |  / _ \   / _` |  / _ \
 | |  | | | (_) | | (_| | |  __/
 |_|  |_|  \___/   \__,_|  \___|
~~~

Unfortunately, function URLS don't support custom domain names, so I need to discard it and stick with API Gateway.
</div>

<div class="notice notice--big">

### Alternate Ending: Fargate?

One downside of Lambdas can be the cold startup time:

> An entire backend on a single lambda would have high cold start times that I would recommend just using fargate if you would rather use containers.
> Otherwise I suggest using API Gateway & a lambda per route. [^2]

To speed things up, you can instead run your container on Fargate. The startup time is fine for my use case, so I'll stay in a Lambda and experiment with Lambda's provisioned concurrency if I need to decrease startup time.

</div>

[^2]: [source](https://dev.to/garretharp/comment/1ohci)

## Local Host

Ok, back to the go code.

The existing solution works as part of a Lambda but converting that `aws-lambda-go-api-proxy` means it doesn't work for me locally like a normal web service container.

~~~{.bash caption=">_"}
$ curl localhost:8080/default/text-mode
404 page not found
~~~

That is because I'm still running the lambda runtime locally, which expects JSON events. You can use this locally, as seen in [this article](/blog/aws-lambda-docker/), but it's a bit cumbersome.

To correct this, I need to modify the image (`public.ecr.aws/lambda/go:latest`) that I'm running. So, I create a second image with an updated entrypoint, in my [Earthfile](https://github.com/earthly/cloud-services-example/blob/aws-lambda-2/lambda-api/Earthfile):

~~~{.docker caption="Earthfile"}
local-image:
    FROM +docker
    ENV AWS_LAMBDA_RUNTIME_API=
    ENTRYPOINT [ "/var/task/lambda" ]
    SAVE IMAGE lambda-api:latest
~~~

I've also blanked out the `AWS_LAMBDA_RUNTIME_API` value, which allows me to detect when I'm running in a lambda like so:

~~~{.diff caption="main.go"}
func main() {
    app := textmode.NewApp()
    r := mux.NewRouter()
    s := r.PathPrefix("/default").Subrouter()
    s.HandleFunc("/text-mode", app.Handler)
    s.HandleFunc("/", HomeHandler)
    r.Use(loggingMiddleware)

+   if runtime_api, _ := os.LookupEnv("AWS_LAMBDA_RUNTIME_API"); runtime_api != "" {
        log.Println("Starting up in Lambda Runtime")
        adapter := gorillamux.NewV2(r)
        lambda.Start(adapter.ProxyWithContext)
+   } else {
+       log.Println("Starting up on own")
+       srv := &http.Server{
+           Addr:    ":8080",
+           Handler: r,
+       }
+       _ = srv.ListenAndServe()
+   }
}
~~~

And with that, I can run the HTTP service with its own routing locally, and in a lambda.

~~~{.bash caption=">_"}
$ docker run \
        -d \
        -v /Users/adam/.aws/config:/root/.aws/config:ro \
        -v /Users/adam/.aws/credentials:/root/.aws/credentials:ro \
        -p 8080:8080 lambda-api:latest
 d0a7b4ded42fa6458a52336c78c151d209e5c567734d70b17a342f231e8ee2b7

$ curl localhost:8080/default/text-mode | head -n 15
~~~

~~~{.merge-code}
Earthly.dev Presents:                                                                                              

  _____                 _       
 |_   _|   ___  __  __ | |_     
   | |    / _ \ \ \/ / | __|    
   | |   |  __/  >  <  | |_     
   |_|    \___| /_/\_\  \__|    
                                
  __  __               _        
 |  \/  |   ___     __| |   ___ 
 | |\/| |  / _ \   / _` |  / _ \
 | |  | | | (_) | | (_| | |  __/
 |_|  |_|  \___/   \__,_|  \___|
~~~

The complete source code is [on GitHub](https://github.com/earthly/cloud-services-example/tree/aws-lambda-2/lambda-api) , and the code for previous versions. This solution should work for any HTTP service in go, whether written using gorrilaMux, the standard lib, or whatever HTTP framework you prefer.

I think this can be a powerful model for deploying stateless HTTP services without getting too intertwined and locked into AWS-specific features. It's just a container and a proxy lib. Everything else works just like you are used to.

{% include_html cta/bottom-cta.html %}
