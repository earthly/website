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

## Introduction

In my tutorial series on building an Activity Tracker, I build up a client and server communicating over grpc and then added REST endpoints to it using the gRPC gateway protoc plugin.

The plugins like grpc gateway and openapi helped make me very productive but my `protoc` call grew from a simple invocation to a multi-line script. Which is what brought buf to my attention. `buf` is a suite of tools the simplify dealing with protocal buffers all wrapped up in a nice three letter tool.

So before I role this service out and start activity tracking at scale, I'm going to take my existing implementation and see how I can use `buf lint`, `buf generate` and `buf breaking` to improve things.

## `buf lint`

After [installing buf(), I ran `buf mod init` in my `activity-log` path, which created a default `buf.yaml` file. The gRPC service I had defined for my activity service looks like this:

```
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
```

Running `buf lint` against I got a number of great suggestions:

```
api/v1/activity.proto:10:5:"api.v1.Activity" is used as the request or response type for multiple RPCs.
api/v1/activity.proto:10:16:RPC request type "Activity" should be named "InsertRequest" or "ActivityLogServiceInsertRequest".
api/v1/activity.proto:11:5:"api.v1.Activity" is used as the request or response type for multiple RPCs.
api/v1/activity.proto:11:44:RPC response type "Activity" should be named "RetrieveResponse" or "ActivityLogServiceRetrieveResponse".
api/v1/activity.proto:12:36:RPC response type "Activities" should be named "ListResponse" or "ActivityLogServiceListResponse".
``` 

This is a great catch by `buf lint`. APIs change over time, and by sharing the `Activity` type across multiple RPC definitions, I'm essentially coupling them together forever.

Or as buf's guide states:

> One of the single most important rules to enforce in modern Protobuf development is to have a unique request and response message for every RPC. Separate RPCs should not have their request and response parameters controlled by the same Protobuf message, and if you share a Protobuf message between multiple RPCs, this results in multiple RPCs being affected when fields on this Protobuf message change. Even in straightforward cases, best practice is to always have a wrapper message for your RPC request and response types. 

So I wrap up my `Activity` into proper `Request` and `Response` messages:
```

message InsertRequest {
    Activity activity = 1;
}

message RetrieveResponse {
    Activity activity = 1;
}
```

And update my service to use them:
```
service ActivityLogService {
    rpc Insert(InsertRequest) returns (InsertResponse) {}
    rpc Retrieve(RetrieveRequest) returns (RetrieveResponse) {}
    rpc List(ListRequest) returns (ListResponse) {}
}
```

And with that, I am passing all the `buf lint` rules. Later, I'll add `buf lint` to the CI process using Earthly, but for now, I'd like to move on to breaking change detection.

## `buf breaking`

As my activity service evolves – as I add new features and role out new versions of it – something I need to keep in mind is backwards compatibility. It's not possible to instantly upgrade a gRPC service and all its clients. Instead I want to make sure that I don't introduce any breaking changes. That way, a new version of the service can receive and handle messages from a client using an earlier version of the protobuf definition. 

`buf breaking` is here to help me find breaking changes. In fact, it can show that the changes I just made above are breaking changes:

```
api/v1/activity.proto:10:16:RPC "Insert" on service "Activity_Log" changed request type from "api.v1.Activity" to "api.v1.InsertRequest".
api/v1/activity.proto:11:44:RPC "Retrieve" on service "Activity_Log" changed response type from "api.v1.Activity" to "api.v1.RetrieveResponse".
api/v1/activity.proto:12:36:RPC "List" on service "Activity_Log" changed response type from "api.v1.Activities" to "api.v1.ListResponse".
```

Those breaking changes I'm not too worried about, because my service is not yet running anywhere, but going forward I do want to prevent the introduction of any break changes. To do that I'm going to introduce `buf lint` and `buf breaking` into my CI process, but first I need to tackle code generation.

## `buf generate`

When I first started switching the activity tracker over to gRPC the protoc call look liked this:

```
 protoc activity-log/api/v1/*.proto \
    --go_out=. \
    --go_opt=paths=source_relative \
    --proto_path=.
```

But as I added a grpc-gateway, and a openapi spec and rest endpoints it got a little out of control.

```
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
```

Moving this to buf generate is really nice. I create a `buf.gen.yaml` file and start listing and configuring plugins.

```
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
```

Because of the nested nature of yaml, I find this much easier to understand than a lengthly protoc call. Then instead of `protoc` I just call `buf generate` and all the generated code is produced.

## Earthly CI Changes

In order to ensure my build process is repeatable, I've wrapped up all the build steps into an `Earthfile` (see previous discussion here). So I don't actually call `buf lint`, `buf breaking` or `buf generate` in CI or locally. Instead I call `earthly +proto` after changing it like this:

```
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
+   RUN buf generate 
    SAVE ARTIFACT ./api AS LOCAL ./api 
```

And with that, I have a smaller, more declarative protocol buffer generation process and `buf lint` and `buf breaking` help me avoid some gRPC footguns. I'm just scratching the surface on `buf`, most of the steps above are highly configurable and their schema registry and remote generation feature look very cool. But for now, I think it's been an improvement.  



Like:
- Tour on top menu
- start / finish structure

$ buf lint

$ buf breaking --against ../../.git#branch=main,subdir=start/petapis

It's very cool how this tool is git aware. So many dev tools only deal with active source, when there is a richer source in git.

This is cool:
https://buf.build/googleapis/googleapis/docs/main/google.cloud.bigquery.connection.v1



```
So Buf uses its own internal compiler under the hood most of the time —you can check out the Internal Compiler docs for more details and compatible behavior guarantees, but it's an essential part of our roadmap to improve protobuf.
Since it is not using protoc to generate (which I believe is a requirement for managed mode), it can't accurately provide a protoc version, so we register the compiler version as unknown as of release v1.0.0-rc9
```