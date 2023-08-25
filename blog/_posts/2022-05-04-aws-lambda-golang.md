---
title: "AWS Lambda Golang With S3"
categories:
  - Tutorials
toc: true
author: Adam
sidebar:
  nav: "lambdas"
internal-links:
 - s3
 - aws lambda
excerpt: |
    
---
**We're [Earthly](https://earthly.dev/). We simplify and speed up software builds with containerization. Whatever you're building, Earthly is a handy tool to complement your workflow. [Check it out](/).**

## Intro

Last time, I built a [Node.js lambda function](/blog/aws-lambda-docker/) running in a container. Running a container as a serverless application worked out great: it meant it was simple to test locally and that I could install and use OS-level dependencies in a serverless function. That is how I was able to run Lynx in my Lambda and build [TextMode](/blog/text-mode).

So Lambda's and containers combined seemed like a good solution, but node.js I'm less sure about. I'm not a JavaScript developer, and I chose Node.js merely because of the existence of the [Mozilla Readability](https://github.com/mozilla/readability) library. However, since then, I've found it has been ported to Golang, and I hope that the Golang version will be faster and easier for me to understand.

So today's mission is to port that Node.js code to Golang, running in a container. I'll also be using OS dependencies in my container, and because TextMode is a very cacheable service, I'm going to use S3 to cache the results as well.

**So, please read this article to learn how to build a Golang Lambda service in a container, hook it up to a REST API end-point, and push and pull data from S3.**

## The Goal

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5800.png --alt {{ Diagram of AWS Lambda request flow }} %}
<figcaption>Here is what we will make.</figcaption>
</div>

Here is the plan when I make a call like this:

~~~{.bash caption=">_"}
curl  https://earthly-tools.com/text-mode?url=https://www.lipsum.com/
~~~

It will *1)* hit the API gateway, *2)* call my GoLang lambda function handler. My code will then *3)* pull the site from the web and *4)* clean it up to look like a text document and return it to the user. Last we will tackle *5)* adding some caching into the mix.

But the end result is already up and running at [https://earthly-tools.com/text-mode](https://earthly-tools.com/text-mode) and will return something like this:  

~~~{.txt caption="curl result"}
What is Lorem Ipsum?

   Lorem Ipsum is simply dummy text of the printing and typesetting
   industry. Lorem Ipsum has been the industry's standard dummy text ever
   since the 1500s, when an unknown printer took a galley of type and
   scrambled it to make a type specimen book. It has survived not only
   five centuries, but also the leap into electronic typesetting,
   remaining essentially unchanged. It was popularised in the 1960s with
   the release of Letraset sheets containing Lorem Ipsum passages, and
   more recently with desktop publishing software like Aldus PageMaker
   including versions of Lorem Ipsum.
   ...
~~~

And all in ~150 lines of Go code. So let's do it.

## The AWS Serverless REST API

When my Go Lambda is called via the lambda runtime, it will get a JSON event describing the request it recieved:

~~~{.json caption="sameple input"}
{
  "queryStringParameters": {
    "url": "https://www.lipsum.com/"
  }
}
~~~

And, I'll return an event describing the document I'd like produced.

~~~{.json caption="sample output"}
{
  statusCode: 200,
  headers: {
    "content-type": "text/plain; charset=utf-8"
  },
  body: "What is Lorem Ipsum?\n\n ..."
}
~~~

The whole thing has the feel of an old-fashion [CGI Interface](https://en.wikipedia.org/wiki/Common_Gateway_Interface).

I represent the input JSON in Golang like this:

~~~{.go caption="input types"}
type Event struct {
 QueryStringParameters QueryStringParameters `json:"queryStringParameters"`
}
type QueryStringParameters struct {
 Url string `json:"url"`
}

~~~

And output like so:

~~~{.go caption="output types"}
type Response struct {
 StatusCode int               `json:"statusCode"`
 Body       string            `json:"body"`
 Headers    map[string]string `json:"headers"`
}
~~~

And, with those in place, I can write my lambda handler code.

## The Golang Lambda Function

First I'll add the needed dependencies:

~~~{.bash caption=">_"}
$ go get github.com/aws/aws-lambda-go/lambda # Add lambda dependency
$ go get github.com/go-shiori/go-readability # Add readability dependency
~~~

Then I can wire everything up:

~~~{.go caption="handler code"}
func (app App) HandleLambdaEvent(event Event) (Response, error) {
 // ToDo: Check Cache
 return process(event.QueryStringParameters.Url)
 //ToDo: Store to Cache
}

func process(url string) (Response, error) {
 article, err := readability.FromURL(url, 30*time.Second)
 if err != nil {
  log.Printf("Error: failed to parse (422) %v: %v", url, err)
  return Response{StatusCode: 422}, err
 }
 cmd := exec.Command("lynx", "--stdin", "--dump", "--nolist", "--assume_charset=utf8")
 cmd.Stdin = strings.NewReader(article.Content)
 out, err := cmd.CombinedOutput()
 if err != nil {
  log.Printf("Error: failed to lynx %v: %v", url, err)
  return Response{StatusCode: 500}, err
 }
 body := article.Title + "\n\n" + string(out)
 return Response{Body: body, StatusCode: 200, Headers: headersTXT}, nil
}

func main() {
 lambda.Start(app.HandleLambdaEvent)
}
~~~

Here `HandleLambdaEvent` does nothing but delegate to `process`, which uses readability to grab the url and then pipes the returned html through lynx. This is the bulk of the work of our service, everything else is just packaging and bookkeeping.

So, let's package it up in a container and test it out with the lambda runtime.

## Containerization

There are two ways to create a container for running in AWS lambda. One is to start with your preferred base container and then copy in and properly set up the AWS Lambda runtime. The second is to use an Amazon-provided container and put your code where the runtime expects it. I'm going to do the latter.

I'm using an Earthfile, so my container image creation code looks like this:

~~~{.dockerfile caption="Earthfile"}
VERSION 0.6
FROM golang:1.17-stretch

deps:
    WORKDIR /lambda
    COPY ./go.mod ./
    RUN go mod download

build:
    FROM +deps
    COPY . .
    RUN go build -o lambda main.go
    SAVE ARTIFACT /lambda/lambda /lambda

docker:
    FROM public.ecr.aws/lambda/go:latest
    RUN yum install lynx -y
    COPY +build/lambda* /var/task/
    ENV _LAMBDA_SERVER_PORT=8080
    CMD [ "lambda" ]
    SAVE IMAGE --push 459018586415.dkr.ecr.us-east-1.amazonaws.com/text-mode-go:latest
~~~

I grab my dependencies in `deps`, build my executable in `build` and in `docker` things get a bit more exciting. First, I copy my executable into AWS's lambda go image and into `/var/task`, which is the default place the runtime will look for it. ( In theory, it's possible to change `/var/task`  with `LAMBDA_TASK_ROOT`, but I found that to only work in local development and be ignored when running in AWS.) After that, I set the `CMD` and `SAVE` my image with a tag assigned to my Amazon ECR registry and build and push the image using `earthly --push +docker`.

It's possible to do all this in a [dockerfile](https://docs.aws.amazon.com/lambda/latest/dg/go-image.html) as well.

With that done, it's possible to test the code and the AWS Lambda runtime locally.

## AWS Lambda Local Development

Since our lambda is now wrapped up in a container, with the lambda runtime its very possible to test it out locally.

~~~{.bash caption=">_"}
$ # Start it up
$ docker run \
        -p 9000:8080 459018586415.dkr.ecr.us-east-1.amazonaws.com/text-mode-go:latest
# Test it out
$ curl --verbose \
      -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations \
    -d '{
    "queryStringParameters": {
      "url": "https://www.lipsum.com/"
    }
  }'
~~~

~~~{.merge-code .caption="Output"}

What is Lorem Ipsum?

   Lorem Ipsum is simply dummy text of the printing and typesetting
   industry. Lorem Ipsum has been the industry's standard dummy text ever
   since the 1500s, when an unknown printer took a galley of type and
   scrambled it to make a type specimen book. It has survived not only
   five centuries, but also the leap into electronic typesetting,
   remaining essentially unchanged. It was popularised in the 1960s with
   the release of Letraset sheets containing Lorem Ipsum passages, and
   more recently with desktop publishing software like Aldus PageMaker
   including versions of Lorem Ipsum.
   ...
~~~

For steps on how to construct the Lambda in AWS and hook it up to and API endpoint, see the [Node.js lambda article](https://earthly.dev/blog/aws-lambda-docker/#elastic-container-registry)

## Using AWS S3 Object Expiration

This service is a bit slow, especially for huge pages. But, the text results I am retrieving are very cacheable. So, why head back to the web each time `https://www.lipsum.com/` is requested when I can just cache the result for future usage.

Amazon S3 has Object expiration settings, so its easy to set up a bucket as a text file cache.

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5520.png --alt {{ S3 Object Expiration Settings }} %}
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5620.png --alt {{ S3 day to expiration rules }} %}
<figcaption>S3 Expiration Settings make for a simple disk-based cache</figcaption>
</div>

## AWS S3 Put Object

To write and read from S3 first I need to import some code and start up an S3 session:

~~~{.diff caption="main.go"}
import (
  ...
  "github.com/aws/aws-lambda-go/lambda"
+ "github.com/aws/aws-sdk-go/aws/session"
+ "github.com/aws/aws-sdk-go/service/s3"
+ readability "github.com/go-shiori/go-readability"
)

+ type App struct {
+  S3         *s3.S3
+ }

func main() {
+ sess, err := session.NewSession(&aws.Config{
+  Region: aws.String("us-east-1")},
+ )
+ if err != nil {
+  log.Fatalf("failed to create AWS session, %v", err)
+ }
+ s3 := s3.New(sess)
+ app := App{S3: s3}

 lambda.Start(app.HandleLambdaEvent)
}
~~~

Then I need a way to put data into the correct bucket:

~~~{.go caption="main.go"}
func (app App) put(url string, result string) error {
 input := &s3.PutObjectInput{
  Body:   strings.NewReader(result),
  Bucket: aws.String("text-mode"),
  Key:    aws.String(url),
 }
 r, err := app.S3.PutObject(input)
 if err != nil {
  return fmt.Errorf("failed to store result: %w", err)
 }
 log.Printf("Stored result: %v", r)
 return nil
}
~~~

I'm creating a PutObjectInput, where the key is the input url and the value is the result of my process step.

Let's do an S3 get:

~~~{.go caption="main.go"}
func (app App) get(url string) (string, error) {
 req := &s3.GetObjectInput{
  Bucket: aws.String("text-mode"),
  Key:    aws.String(url),
 }
 r, err := app.S3.GetObject(req)
 if err != nil {
  return "", fmt.Errorf("failed to get result: %w", err)
 }
 defer r.Body.Close()
 buf := new(bytes.Buffer)
 _, err = buf.ReadFrom(r.Body)
 if err != nil {
  return "", fmt.Errorf("failed to get S3 result: %w", err)
 }
 return buf.String(), nil
}
~~~

This works fine, except because we are just passing the error up to the caller its going to be hard to tell the key not existing from any other errors.

The Amazon SDK represents its errors with this interface:

~~~{.go caption="package awserr"}
type Error interface {
 // Satisfy the generic error interface.
 error

 // Returns the short phrase depicting the classification of the error.
 Code() string

 // Returns the error details message.
 Message() string

 // Returns the original error if one was set. Nil is returned if not set.
 OrigErr() error
}
~~~

And their types are denoted using the constant stored in `Code()`. The possible values for s3 are in package `s3` in `errors.go`

~~~{.go caption="errors.go"}
 // ErrCodeNoSuchBucket for service response error code
 // "NoSuchBucket".
 //
 // The specified bucket does not exist.
 ErrCodeNoSuchBucket = "NoSuchBucket"

 // ErrCodeNoSuchKey for service response error code
 // "NoSuchKey".
 //
 // The specified key does not exist.
 ErrCodeNoSuchKey = "NoSuchKey"
 ...
~~~

And so I can use this information determine if the key is there and return a sentinel error value for that. All other problems are non-recoverable.

~~~{.diff caption="func get"}
+var errNoKey = errors.New(s3.ErrCodeNoSuchKey)
+
func (app App) get(url string) (string, error) {
 req := &s3.GetObjectInput{
  Bucket: aws.String("text-mode"),
  Key:    aws.String(url),
 }
 r, err := app.S3.GetObject(req)
 if err != nil {
-   return "", fmt.Errorf("failed to get result: %w", err)
+   if s3Err, ok := err.(awserr.Error); ok && s3Err.Code() == s3.ErrCodeNoSuchKey {
+      return "", errNoKey
+   } else {
+      return "", fmt.Errorf("failed to get result: %w", err)
+   }
 }
 defer r.Body.Close()
 buf := new(bytes.Buffer)
 _, err = buf.ReadFrom(r.Body)
 if err != nil {
  return "", fmt.Errorf("failed to get S3 result: %w", err)
 }
 return buf.String(), nil
}
~~~

And then I can use these from my lambda helper.

~~~{.go caption=""}
func (app App) HandleLambdaEvent(event Event) (Response, error) {
 log.Println("Received event: ", event)

 result, err := app.get(event.QueryStringParameters.Url)
 if errors.Is(err, errNoKey) {
  log.Println("No cache value found")
  resp, err := process(event.QueryStringParameters.Url)
  if err != nil {
   return resp, err
  }
  log.Println("Caching value")
  err = app.put(event.QueryStringParameters.Url, resp.Body)
  return resp, err
 } else if err != nil {
  return Response{StatusCode: 500}, err
 }
 return Response{Body: result, StatusCode: 200, Headers: headersTXT}, nil
}
~~~

## Accessing S3 Locally

Now, if I test this locally, in its docker container, I hit a new problem:

~~~{.json caption=""}
{
  "errorMessage":"failed to get result: NoCredentialProviders: no valid providers in chain. Deprecated.\n\tFor verbose messaging see aws.Config.CredentialsChainVerboseErrors",
  "errorType":"wrapError"
}                                
~~~

My Lambda is running under a specific role with specific permissions when running in AWS. But here, locally inside a container, it doesn't know who it is. I can fix this for local testing by giving my program access to my `.aws/config` and `.aws/credentials`.

<div class="notice--warning">
### ❗ Careful With Secrets

Whenever you are working with secrets and building docker images, its important to ensure you aren't capturing the secrets in an image layer or log file. You don't want your secrets to end up contained an image and then be pushed to the registry.

</div>

The simplest safe way to access these files at runtime in the container is a read-only volume mount. This will ensure they are accessible to the running process but they will not be contained in the image at rest.

~~~{.bash caption=">_"}
 docker run \
        -v /Users/user/.aws/config:/root/.aws/config:ro \
        -v /Users/user/.aws/credentials:/root/.aws/credentials:ro \
        -p 9000:8080 459018586415.dkr.ecr.us-east-1.amazonaws.com/text-mode-go:latest
~~~

And with that change, I can read and write to S3 when running locally.

## Deploy

With all that working locally, I can deploy things:

~~~{.bash caption=">_"}
$ earthly --push +docker
$ aws lambda update-function-code \
            --region us-east-1 \
            --function-name text-mode-go \
            --image-uri 459018586415.dkr.ecr.us-east-1.amazonaws.com/text-mode-go:latest
~~~

## Speed Test

Now that I'm caching and using a compiled language, things should be faster. Lets check it out. I'll temporarily keep [the original node.js](/blog/text-mode/) code and the new code up, so that I can compare them.

~~~{.bash caption=">_"}
$ # Node.js 
$ time curl https://earthly-tools.com/text-mode-2?url=https://en.wikipedia.org/wiki/Software_engineering
...
curl   0.02s user 0.01s system 0% cpu 8.905 total
~~~

After running it a couple times, to make sure it was warm, the time averaged out at 3.8 seconds.

To test the go solution without caching, I'll use the aws cli to clear the cache bucket every second.

~~~{.bash caption=">_"}
watch -n 1 'aws s3 rm s3://text-mode/ --recursive'
~~~

And then test it:

~~~{.bash caption=">_"}
$ # GoLang
$ time curl https://earthly-tools.com/text-mode?url=https://en.wikipedia.org/wiki/Software_engineering
...
~~~

Then to test with caching, I just stop deleting stuff. The end result, making sure each lambda is warmed up, and average across several call, is this:

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/4310.png --alt {{ Graph of speeds }} %}
<figcaption>Porting to Golang was a performance win.</figcaption>
</div>

It's surprising to me how much faster the Golang version is. Lynx and the readability lib do the majority of the work. Perhaps the native readability lib is just a lot faster but I'm not sure without digging in further.  

## Conclusion

So there you go, containerized serverless Golang. We built a program in Go that has some OS level dependencies (lynx), we've wrapped it up into a container, ran it in an AWS Lambda, and then also used S3 get and puts for caching. And the whole up to a REST end point. You can [test it out](https://earthly-tools.com/text-mode) or use it for your own purposes and the complete source code is on [github](https://github.com/adamgordonbell/cloudservices/tree/aws-lambda-1).

And if you liked how I put together this project, take a look at [Earthly](/).

{% include_html cta/bottom-cta.html %}
