---
title: "Grpc, AWS Lambdas and GoLang"
categories:
  - Tutorials
toc: true
author: Adam
sidebar:
  nav: "lambdas"
internal-links:
 - just an example
excerpt: |
    Learn how to combine GRPC, AWS Lambdas, and GoLang to create a powerful serverless architecture. Discover different approaches to proxying GRPC requests on Lambda and explore the limitations of running a GRPC service on an AWS Lambda.
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and faster with containerization. Earthly is a great tool that can streamline your build process. [Check it out](/).**

<!-- vale HouseStyle.Link = NO -->

Previously, I built some [GRPC things](/blog/golang-grpc-example), and some [AWS Lambda](/blog/aws-lambda-golang) things, but can both be combined together? That is can I set up a go service, that runs as lambda, and can respond to GRPC requests.

The answer is no, and I'll explain why in a second.

However, I can do things close to GRPC on lambda and some of them might be useful.

## GRPC Proxy on Lambda

One thing its easy to do is setup a web proxy that runs on lambda and gets requests via API GATEWAY and forwards them on.

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/9010.png --alt {{ Two of the possible ways a Lambda can proxy to GRPC }} %}
<figcaption>Two of the possible ways a Lambda can proxy to GRPC</figcaption>
</div>

This would enable making REST requests that ultimately are backed by a GRPC service that your AWS Lambda calls. That GRPC service would be running somewhere else and your lambda code would be proxying requests to it.

Another thing you can do is have your GRPC service also run the web proxy on another port and then it can call itself: Your service starts up listening for GRPC requests on one port, and on another it is called by the lambda runtime. When you get a request from the lambda runtime you use the GRPC proxy to call yourself on the gRPC port. It's a little strange but not uncommon in go-land.

These two approaches and one more approach are covered [here](/blog/golang-grpc-gateway), and porting them to a lambda runtime only requires the configuration of the AWS API gateway and wrapping your request handling with `aws-lambda-go-api-proxy`:

~~~{.go caption="main.go"}
package main

import (
 "log"
 "net/http"

 "github.com/aws/aws-lambda-go/lambda"
 "github.com/awslabs/aws-lambda-go-api-proxy/handlerfunc"
 "github.com/grpc-ecosystem/grpc-gateway/v2/runtime"
)

func main() {
 mux := runtime.NewServeMux()

  // Configure grpc-gateway
  ...
  //Start in Lambda wrapped special handler function 
 lambda.Start(handlerfunc.NewV2(func(w http.ResponseWriter, req *http.Request) {
  mux.ServeHTTP(w, req)
 }).ProxyWithContext)
}

~~~

This works, but regardless of which way you do it, neither of these actually results in the API gateway endpoint that can receive GRPC requests. We need another trick.

## GRPC Web

[This article](https://blog.gendocu.com/posts/grpc-web-on-aws/
) shows how to setup a GRPC service on AWS Lambda and talk to it using GRPCWeb.

The code is up here and its deployed as a lambda [here](https://t30z1m0w81.execute-api.us-east-1.amazonaws.com/). The fact that they have the lambda up and running and you can interact with it is very cool!

Unfortunately, though it can be called from JavaScript, tt's can't work as a lambda based GRPC service.

Here it is not working:

~~~{.bash caption=">_"}
$ grpcurl t30z1m0w81.execute-api.us-east-1.amazonaws.com:443 \
  gendocu.example.library_app.BookService.ListBooks

Error invoking method "gendocu.example.library_app.BookService.ListBooks": 
rpc error: 
code = Unknown desc = failed to query for service descriptor "gendocu.example.library_app.BookService":
HTTP status code 464; transport: missing content-type field
~~~

Or the raw error from BloomRPC:

~~~{.yaml caption="Output"}
{
  "error": "14 UNAVAILABLE: Trying to connect an http1.x server"
}
~~~

The whole problem is getting an HTTP/2 connection to the lambda. The integration between API Gateway and lambdas don't seem to support this.

However, this endpoint can be used to make GRPCWeb requests. GRPCWeb is a different wire protocol than GRPC and does work over HTTP/1.1 and is usable from a JavaScript http/1.1 based client.

## Why No HTTP 2?

HTTP/2 and AWS's API Gateway don't play well when it comes to lambdas. Although you can connect via HTTP/2, the API Gateway sticks to HTTP/1.1 for lambda calls which is a bummer for GRPC, as it's bound with HTTP/2. You'd need to switch to GRPC-Web to work over HTTP/1.1, but its client support is limited. 

A GRPC service on an AWS Lambda might not be feasible unless more GRPCWeb clients emerge, or you're okay with JavaScript or not using Lambdas. If you find a workaround, hit me up! In the meantime, if you're struggling with build automation in your serverless architecture, [Earthly](https://www.earthly.dev/) could make things easier. Check it out!

For more information on GRPC and GRPC Web, you can check out these resources:

- [Stack Overflow Question](https://stackoverflow.com/questions/67281831/)
- [GRPC Web Explained](https://grpc.io/blog/state-of-grpc-web/)
- [Envoy GRPC Bridge](https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/grpc_http1_bridge_filter)

{% include_html cta/bottom-cta.html %}
