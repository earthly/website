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
- [ ] Would any images look better `wide` or without the `figcaption`?
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links
- [ ] Add Earthly `CTA` at bottom `{% include cta/cta1.html %}`

## Intro

Most of the code I've had running on AWS's cloud has been in the form of docker containers, running in Kubernetes clusters. And from my perspective, AWS was invisible, all I needed to concern myself with was the intricacies of getting the yaml for kubectl apply right. The actual specifics of the cluster and how its configured was outside of my area of concern, unless something went wrong and then I could just ping some OPs expert to help me out.

But all that seems like overkill for many tasks, and the operational burden of maintaing kubernetes seems like overkill for so many cases.

What if I just want a simple container running in my AWS account, with some endpoints open to the world. What is the best way to get that in place? AWS offers a myriad of options for this. There is Amazon Elastic Container Service (ECS), Amazon Elastic Kubernetes Service (EKS), AWS App Runner and AWS Lightsail. Maybe there are more options? I'm not sure how anyone keeps up with the myriad of options AWS offers. But, an option with some nice properties is AWS Lambda.

## Containers on AWS Lambda

AWS lambda, in it's first revision, supported giving the lambda a zip file of code, that corresponded to their lambda API and that was about it. But it has some two nice scalability features. One, it could scale up to thousands of instances based on request load and two, it scaled down to zero when no requests were coming in. That aggressive scheduling, combined with a billing structure where you only for the time your lambda is running is what caused all the buzz around lambdas back in 2014

> AWS Lambda is a compute service that runs your code in response to events and automatically manages the compute resources for you, making it easy to build applications that respond quickly to new information. AWS Lambda starts running your code within milliseconds of an event such as an image upload, in-app activity, website click, or output from a connected device. You can also use AWS Lambda to create new back-end services where compute resources are automatically triggered based on custom requests.

But, I never got interested in lambdas myself. I worked in Scala, which runs on the JVM, which has a slow start-up time, and I also was into containers as a packaging unit and so although I heard people talk about lamda's I didn't really pay attention.

But then in 2020, AWS added support for containers. This maybe naive of me, but the tech stack suddenly made more sense to me. If I could take my app, wrap it up in a container, which I was doing already, and have it running in AWS Lambda then it was sort of like getting to deploy things into a giant Kuberenetes cluster in the sky. The horizonal scaling features that were hard to get right in kubernetes (`HPAScaleToZero`), came for free with lambdas and if your app has a slow start up time, with provisioned concurrency, you can always keep some instances running, never scaling back right to zero.

All of this to say, 8 years afters its launch, I'm starting to see what the hype is about. With that extended preamble, let me show you the set up for running a container in a lambda.

What I'm going to make will be pretty simple, it will be a small node.js app that will take a url, download it and return the results. Basically a very simple web proxy.

## TypeScript Lambda

The first thing I'm going to do is create typescript file that will be the bulk of my lambda. Any programming langauge that can run inside a container will work though. The main trick is just conforming to the shape of input and output expected by a lambda.

For instance, when I make a request against the AWS API gateway that I'll be setting up shortly, like this:

~~~{.bash caption=">_"}
curl ((URL))/endpoint/?url=bla
~~~

Then AWS Lamda will recieve the even like this:

~~~{.json caption="lambda input"}
{
  "queryStringParameters": {
    "url": "https://earthly.dev/blog/golang-monorepo/"
  }
}
~~~

And if I want to return a plain text 500 error from my lambda I need to return a JSON object like this:

~~~{.json caption="lambda output"}
{
 "statusCode" : 500,
  "headers" : {
    "content-type": "text/plain; charset=utf-8"
  },
  "body" : "Some error fetching the content"
}
~~~

With that in mind, my TypeScript code looks like this:

~~~{.ts caption="app.ts"}
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
~~~

I'm returning an explanitory message in plain text if URL is missing and otherwise I return the result of `call`.

Since this is running in a container, `call` could call out to other programs installed in the container – perhaps downloading the html, and running a html minimizer? But for tutorial purposes, all it does it download the html content and return it as text.

~~~{.ts caption="app.ts continued"}
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
~~~

I build this file with `tsc` into `built/app.js` and then I wrap it up into a docker container, for deployment to AWS Lambda.

~~~{.dockerfile caption="dockefile"}
FROM public.ecr.aws/lambda/nodejs:12
COPY package*.json ./
COPY built/*.js ./
RUN npm install
CMD [ "app.handler" ]

~~~

I'm using Amazon's suggested base container for Node.js which is a redhat linux container with the AWS lambda runtime installed. 

Using Amazon's images, the lambda runtime is already installed and everything is configured for it to start up. I can see this using `docker inspect`

~~~{.json caption="docker inspect"}
{
 ...
 "Env": [
    "LAMBDA_TASK_ROOT=/var/task",
    "LAMBDA_RUNTIME_DIR=/var/runtime"
       ],
 "WorkingDir": "/var/task",
 "Entrypoint": [
    "/lambda-entrypoint.sh"
    ],
 ...
}
~~~

Amazon provides a number of container bases, but you can also just install the [container base of your choosing](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html#images-create-from-alt).

Now, let's run something.

## Testing Lambdas Locally

With the app containerized, its easy to test it locally:

First I build it:

~~~{.bash caption=">_"}
$ docker build i  -t 733977735356.dkr.ecr.us-east-1.amazonaws.com/container-test .
~~~

Then I can run it.

~~~{.bash caption=">_"}
$ docker run -p 9000:8080 /
    733977735356.dkr.ecr.us-east-1.amazonaws.com/container-test:latest
~~~

And exercise it.

~~~{.bash caption=">_"}
$ curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{
  "queryStringParameters": {
    "url": "https://icanhazip.com/"
  }
}'
~~~

~~~{.bash caption="Output"}
{
    "statusCode":200,
    "headers":
        {
            "content-type":"text/plain; charset=utf-8"
        },
    "body":"76.6.XXX.XXX\n"
}
~~~

<div class="notice--info">
Note how I need to make my requests in the same fashion the API Gateway will. My API will be responding to GET requests with a URL parameter, but to exercise it I post with a correctly formatted request body.
</div>

### Elastic Container Registry

After that I need to push my image to AWS ECR.

First I create a repository:

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/4460.png --alt {{  Create Repo in ECR }} %}
<figcaption>Create Repo in ECR</figcaption>
</div>

Then I login and push to it.

~~~{.bash caption=">_"}
$ aws ecr get-login-password --region us-east-1 | \
    docker login --username AWS --password-stdin \
    XXXXXXXXXXXXXXXXXXX.dkr.ecr.us-east-1.amazonaws.com 

~~~

~~~{.bash caption="Output"}
 [733977735356.dkr.ecr.us-east-1.amazonaws.com/container-test]
6f55f8f6a022: Pushed 
ff595bbcde74: Pushed 
428b5d37bdb8: Pushed 
aa262ea90a60: Pushed 
b84abea626b7: Pushed 
c51ba664b438: Pushed 
2b9913d02f84: Pushed 
d589926497ff: Pushed 
00a4e675f0b7: Pushed 
3f1bccf018a1: Pushed 
latest: digest: sha256:f5578098c6677638e2 size: 2420
~~~

And then create the lambda, by selecting 'Create Function' and 'Container Image'.

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5170.png --alt {{  }} %}
</div>

Then I select my image.

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5200.png --alt {{  }} %}
<figcaption></figcaption>
</div>

And then create a trigger.

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5320.png --alt {{  }} %}
<figcaption></figcaption>
</div>

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5430.png --alt {{  }} %}
<figcaption></figcaption>
</div>

At this point, I'm all setup and I can start using my lambda.

## Calling My Endpoint

Then I can call it , via the provided API end point:
<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5520.png --alt {{  }} %}
<figcaption></figcaption>
</div>

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5650.png --alt {{  }} %}
<figcaption></figcaption>
</div>

~~~{.bash caption=">_"}
curl https://5f8lt8irs0.execute-api.us-east-1.amazonaws.com/default/container-test\?url\=https://icanhazip.com/
100.27.35.7
~~~

<div class="notice--info">
### Side Note: Home Path

If you are spawning processes and running things in a shell inside your container, inside your lambda be aware that the home directory, as of March, 2020 is not properly configured and you will get an error like this:

~~~{.bash caption=">_"}
ENOENT: no such file or directory, mkdir '/home/sbx_user1051/.fonts
~~~

See this error, but the easiest way to fix is just set `$HOME` to `/tmp` in the environmental variables section of lambda configuration.

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/7210.png --alt {{  }} %}
</div>

### Deploying Changes

One thing that caught me out with this solution is that, although I've deployed `:latest`, updating the latest image doesn't change whats running in the lambda. This because the lambda just uses the tag to look up the sha of a container and runs that.

I can easily deploy a new image using the aws cli though.

~~~{.bash caption=">_"}
 aws lambda update-function-code \
      --region us-east-1 \
      --function-name container-test \
      --image-uri 733977735356.dkr.ecr.us-east-1.amazonaws.com/container-test:latest
~~~

So there you go, I have containers working in lambdas. And this will work with any software stack that you can get inside a linux container.

## Continous Deployment

From where I'm at now, its not far to a full CI/CD solution.

First off I make my docker container inside an Earthfile.

~~~{.bash caption="Earthfile"}
FROM public.ecr.aws/lambda/nodejs:12

build:
    COPY package*.json readme.txt ./
    COPY built/*.js ./
    RUN npm install
    CMD [ "app.handler" ]
    SAVE IMAGE 733977735356.dkr.ecr.us-east-1.amazonaws.com/container-test:latest
~~~

Then, in the same Earthfile, I run my deploy steps.

~~~{.bash caption="Earthfile"}
deploy:
    LOCALLY
    RUN aws lambda update-function-code \
         --region us-east-1 \
         --function-name container-test \
         --image-uri 733977735356.dkr.ecr.us-east-1.amazonaws.com/container-test:latest

~~~

Then in my chosen CI, when something is merged into my main branch, I just run `earthly +build --push` and `earthly +deploy` and my function will be updated.

{% include cta/cta1.html %}
