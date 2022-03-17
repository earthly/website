---
title: "Running Containers on AWS Lambda"
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

## Intro

Most of the code I've had running on AWS's cloud has been in the form of docker containers, running in Kubernetes clusters. And from my perspective, AWS was invisible, all I needed to concern myself with was the intricacies of getting the yaml for kubectl apply right. The actual specifics of the cluster and how its configured was outside of my area of concern, unless something went wrong and then I could just ping some OPs expert to help me out.

But all that seems like overkill for many tasks, and the operational burden of maintaing kubernetes seems like overkill for so many cases.

What if I just want a simple container running in my AWS account, with some endpoints open to the world. What is the best way to get that in place? AWS offers a myriad of options for this. There is Amazon Elastic Container Service (ECS), Amazon Elastic Kubernetes Service (EKS), AWS App Runner and AWS Lightsail. Maybe there are more options? I'm not sure how anyone keeps up with the myriad of options AWS offers. But, an option with some nice properties is AWS Lambda.

## Containers on AWS Lambda

AWS lambda, in it's first revision, supported giving the lambda a zip file of code, that corresponded to their lambda API and that was about it. But it has some two nice scalability features. One, it could scale up to thousands of instances based on request load and two, it scaled down to zero when no requests were coming in. That aggressive scheduling, combined with a billing structure where you only for the time your lamda is running is what caused all the buzz around lambdas back in 2014

... news

But, I never really got interested in lambdas myself. I worked in Scala, which runs on the JVM, which has a slow warm up time and I also was really into containers as a great unit for shipping OS level dependencies into prod. 

But then in 2020, AWS added support for containers. This maybe naive of me, but this suddenly made more sense to me. If I could take my app, wrap it up in a container and have it running in AWS Lambda it was sort of like getting the horizonal scaling features that were hard to get right in kubernetes (`HPAScaleToZero`), but for free. And if your app has a slow start up time,with provisioned concurrency, you can always keep some instances running, never scaling back right to zero.

All of this to say, 8 years afters its launch, I'm starting to see what the hype is about. With that extended preamble, let me show you have I setup a lambda to run a container. 

What I'm going to make will be pretty simple, it will be a node.js the will take a url request and return the results. Basically a very simple proxy. 

## TypeScript Code

The first thing I'm going to do is create typescript file that will be the bulk of my lambda. Any programming langauge that can run inside a container will work though. The main trick is just conforming to the shape of input and output expected by a lambda.

For instance, when I make a request against the AWS API gateway that I'll be setting up shortly, like this:

```
curl ((URL))/endpoint/?url=bla
```

Then AWS Lamda will recieve the even like this:

``` json
{
  "queryStringParameters": {
    "url": "https://earthly.dev/blog/golang-monorepo/"
  }
}
```

And if I want to return a plain text 500 error from my lambda I need to return a JSON object like this:

``` yaml
{
 statusCode: 500,
  headers: {
    "content-type": "text/plain; charset=utf-8"
  },
  body: "Some error fetching the content"
}
```
With that in mind, my typescript code looks like this:

``` typescript
'use strict';

const axios = require("axios").default;

exports.handler = (event: { queryStringParameters: { url: string; }; }) => {
    if (!event.queryStringParameters || !event.queryStringParameters.url) {
        let response = {
            statusCode: 200,
            headers: {
                "content-type": "text/plain; charset=utf-8"
            },
            body: "Please provide a url as a query string parameter"
        };
        return (Promise.resolve(response));
    } else {
        const url = event.queryStringParameters.url;
        return call(url)
    }
};
```

Above we return an explanitory message in plain text if URL is missing and otherwise return the results of call.

Since this is running in a container, call could call out to other programs installed in the container – perhaps downloading the html, and running a html minimizer?  But, for tutorial purposes, all it does it download the html content and return it as text.

``` typescript
function call(url: string) {
    console.log("Getting:" + url);
    return axios
        .get(url)
        .then((response: { data: string }) => {
            console.log("Got content for:" + url );
            return {
                statusCode: 200,
                headers: {
                    "content-type": "text/plain; charset=utf-8"
                },
                body: response
            };
        })
        .catch((error: Error) => {
            return {
                statusCode: 500,
                headers: {
                    "content-type": "text/plain; charset=utf-8"
                },
                body: "Some error fetching the content"
            };
        });
}
```

I build this file with `tsc` into `built/app.js` and then the next thing I need to do is wrap this up into a docker container, for deployment to AWS Lambda.

``` Dockerfile
FROM public.ecr.aws/lambda/nodejs:12
COPY package*.json ./
COPY built/*.js ./
RUN npm install
CMD [ "app.handler" ]

```

I'm using Amazon's suggested base container for Node.js which is a redhat linux container with the AWS lambda runtime installed. Amazon provides a number of container bases, but you can also just install the [container base of your choosing](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html#images-create-from-alt).

## Testing Locally

With the app containerized, its easy to test it locally:

First I build it: 
```
curl --verbose -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{
  "queryStringParameters": {
    "url": "https://earthly.dev/blog/golang-monorepo/"
  }
}'
}
```

Then I can run it and make calls against it:

```
 docker run -p 9000:8080 733977735356.dkr.ecr.us-east-1.amazonaws.com/text-mode:latest

```

Note how I need to make my requests in the same fashion API Gateway will. My API will be responding to GET requests with a URL parameter, but to exercise it I post with a correctly formatted request body. 


After that I need to push my image to AWS ECR:

```
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin XXXXXXXXXXXXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com 

```