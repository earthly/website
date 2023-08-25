---
title: "Avoiding Common Protobuf's Pitfalls with Buf"
categories:
  - Tutorials
toc: true
sidebar:
  nav: "activity-tracker"
author: Adam
internal-links:
 - buf
excerpt: |
    
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about avoiding common pitfalls with Protobuf using Buf. Earthly great build tool if you are using Protobufs. [Check us out](/).**

## Introduction

Welcome back! In my tutorial series on building an [Activity Tracker](/blog/golang-grpc-example/), I built up a client and server communicating over gRPC. I then added REST endpoints to it using [the gRPC-Gateway](https://github.com/grpc-ecosystem/grpc-gateway) `protoc` plugin.

The plugins like gRPC-gateway and OpenAPI helped make me productive, but my `protoc` call grew from a simple invocation to a multi-line script, which brought `buf` to my attention. `buf` is a suite of tools that simplify dealing with protocol buffers wrapped up in a nice three-letter command.

So before I roll this service out and start actively using it, I will take my existing implementation and see how I can use `buf lint`, `buf generate` and `buf breaking` to improve things.

## Background

The current [activity tracking code](https://github.com/adamgordonbell/cloudservices/tree/v5-grpc-gateway) and [final version](https://github.com/adamgordonbell/cloudservices/tree/v6-buf) are on GitHub but the main thing you need to know for this walk-though is that my gRPC service is defined like this:

~~~{.protobuf caption="activity-log/api/v1/activity.proto"}
service ActivityLogService {
    rpc Insert(Activity) returns (InsertResponse) {}
    rpc Retrieve(RetrieveRequest) returns (Activity) {}
    rpc List(ListRequest) returns (Activities) {}
}

message Activity {
    int32 id = 1;
    google.protobuf.Timestamp time = 2;
    string description = 3;
}

...
~~~

## `buf lint`

After [installing `buf`](https://docs.buf.build/installation), I ran `buf mod init` in my `activity-log` path, which created a default `buf.yaml` file. Then I ran `buf lint`.

~~~{.bash caption=">_"}
> buf lint
~~~

~~~{.bash .merge-code caption=""}
api/v1/activity.proto:10:5:
  "api.v1.Activity" is used as the request or response type for multiple RPCs.
api/v1/activity.proto:10:16:
  RPC request type "Activity" should be named "InsertRequest" or "ActivityLogServiceInsertRequest".
api/v1/activity.proto:11:5:
  "api.v1.Activity" is used as the request or response type for multiple RPCs.
api/v1/activity.proto:11:44:
  RPC response type "Activity" should be named "RetrieveResponse" or "ActivityLogServiceRetrieveResponse".
api/v1/activity.proto:12:36:
  RPC response type "Activities" should be named "ListResponse" or "ActivityLogServiceListResponse".
~~~

This is an excellent catch by `buf lint`. APIs change over time, and by sharing the `Activity` type across multiple RPC definitions, I'm essentially coupling them together forever.

Or as buf's guide states:

> One of the single most important rules to enforce in modern Protobuf development is to have a unique request and response message for every RPC. Separate RPCs should not have their request and response parameters controlled by the same Protobuf message, and if you share a Protobuf message between multiple RPCs, this results in multiple RPCs being affected when fields on this Protobuf message change. Even in straightforward cases, best practice is to always have a wrapper message for your RPC request and response types.

So I wrap up my `Activity` into proper `Request` and `Response` messages:

~~~{.protobuf caption="activity-log/api/v1/activity.proto"}
message InsertRequest {
    Activity activity = 1;
}

message RetrieveResponse {
    Activity activity = 1;
}
~~~

And update my service to use them:

~~~{.protobuf caption="activity-log/api/v1/activity.proto"}
service ActivityLogService {
    rpc Insert(InsertRequest) returns (InsertResponse) {}
    rpc Retrieve(RetrieveRequest) returns (RetrieveResponse) {}
    rpc List(ListRequest) returns (ListResponse) {}
}
~~~

And with that, I am passing all the `buf lint` rules. Later, I'll add `buf lint` to the CI process using Earthly, but for now, I'd like to move on to breaking change detection.

## `buf breaking`

As my activity service evolves – as I add new features and roll out new versions – I need all my changes to be backwards compatible. This is because it's impossible to upgrade a gRPC service and its clients instantly. So I need backwards compatibility to prevent downtime. That way, a new version of the service can receive and handle messages from a client using an earlier version of the protobuf definition.

`buf breaking` is here to help me find breaking changes. For example, it can show that the changes I just made above are breaking changes:

~~~{.bash caption=">_"}

> buf breaking --against "https://github.com/adamgordonbell/cloudservices.git#branch=main,subdir=activity-log" 
~~~

<figcaption>Using `buf breaking` to compare against main branch</figcaption>

~~~{.bash caption=""}
api/v1/activity.proto:10:16:
  RPC "Insert" on service "Activity_Log" changed request type from "api.v1.Activity" to "api.v1.InsertRequest".
api/v1/activity.proto:11:44:
  RPC "Retrieve" on service "Activity_Log" changed response type from "api.v1.Activity" to "api.v1.RetrieveResponse".
api/v1/activity.proto:12:36:
  RPC "List" on service "Activity_Log" changed response type from "api.v1.Activities" to "api.v1.ListResponse".
~~~

I'm not too worried about those breaking changes because my service is not yet running anywhere, but from now on, I want to prevent the introduction of any break changes. To do that, I'm going to introduce `buf lint` and `buf breaking` into my CI process, but first, I need to tackle code generation.

## `buf generate`

When I first started switching the activity tracker over to gRPC the protoc call look liked this:

~~~{.bash caption=">_"}
 protoc activity-log/api/v1/*.proto \
    --go_out=. \
    --go_opt=paths=source_relative \
    --proto_path=.
~~~

But as I added a grpc-gateway, and a OpenAPI spec and rest endpoints, it got a little out of control.

~~~{.bash caption=">_"}
protoc api/v1/*.proto \
            --go_out=. \
            --go_opt=paths=source_relative \
            --go-grpc_out=. \
            --go-grpc_opt=paths=source_relative \
            --grpc-gateway_out . \
            --grpc-gateway_opt logtostderr=true \
            --grpc-gateway_opt paths=source_relative \
            --grpc-gateway_opt generate_unbound_methods=true \
            --openapiv2_out . \
            --openapiv2_opt logtostderr=true \
            --openapiv2_opt generate_unbound_methods=true \
            --proto_path=.
~~~

Moving this to `buf` generate is simple: I create a `buf.gen.yaml` file and start listing and configuring plugins.

~~~{.yaml caption="buf.gen.yaml"}
version: v1
plugins:
 - name: go
   out: .
   opt: paths=source_relative
 - name: go-grpc
   out: .
   opt: paths=source_relative
 - name: grpc-gateway
   out: .
   opt:
     - logtostderr=true
     - paths=source_relative
     - generate_unbound_methods=true
 - name: openapiv2
   out: .
   opt:
    - logtostderr=true
    - generate_unbound_methods=true
~~~

Because of the nested nature of yaml, I find this much easier to understand than a lengthy `protoc` call. So then instead of `protoc` I call `buf generate`, and all the generated code is produced.

## Earthly CI Changes

In order to ensure my build process is repeatable, I've wrapped up all the build steps into an `Earthfile` (see [previous discussion](/blog/golang-grpc-example/#playing-nice-with-others)). So I don't call `buf lint`, `buf breaking` or `buf generate` in CI or locally. Instead I call `earthly +proto` after changing it like this:

~~~{.diff caption="/activity-log/Earthfile"}
proto:
    FROM +proto-deps
    WORKDIR /activity-log
    COPY go.mod go.sum ./ 
    COPY api ./api
-   RUN protoc api/v1/*.proto \
-           --go_out=. \
-           --go_opt=paths=source_relative \
-           --go-grpc_out=. \
-           --go-grpc_opt=paths=source_relative \
-           --grpc-gateway_out . \
-           --grpc-gateway_opt logtostderr=true \
-           --grpc-gateway_opt paths=source_relative \
-           --grpc-gateway_opt generate_unbound_methods=true \
-           --openapiv2_out . \
-           --openapiv2_opt logtostderr=true \
-           --openapiv2_opt generate_unbound_methods=true \
-           --proto_path=.
+    COPY buf.* .
+    RUN buf lint
+    RUN buf breaking --against "https://github.com/adamgordonbell/cloudservices.git#branch=buf,subdir=activity-log" 
+    RUN buf generate 
    SAVE ARTIFACT ./api AS LOCAL ./api 
~~~

And with that, I have a simpler, more declarative protocol buffer generation process, and `buf lint` and `buf breaking` help me avoid some gRPC foot-guns, and it's all wrapped up in a reusable build script, so no breaking change or lint violation will even make it into my main branch.

( So, hint hint, if you're looking for a smarter build process, give [Earthly](https://www.earthly.dev/) a go. )

And I'm just scratching the surface on `buf`, most of the steps above are highly configurable, and their schema registry and remote generation feature look very cool. But for now, I think it's been an improvement.

{% include_html cta/bottom-cta.html %}
