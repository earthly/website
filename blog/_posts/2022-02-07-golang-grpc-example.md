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


---

protoc


Rewrite this:
```
When you’re building public APIs or you’re creating a project where
you don’t control the clients, JSON makes sense because it’s accessible—both
for humans to read and computers to parse. But when you’re building private
APIs or building projects where you do control the clients, you can make use
of  a  mechanism  for  structuring  and  transmitting  data  that—compared  to
JSON—makes you more productive and helps you create services that are
faster, have more features, and have fewer bugs
```



# Explain about protobufs
# Aside about json verification and golang

## CLI protobufs

start up a sample endpoint
```
docker run -it --rm -p 9000:9000 -p 9001:9001 moul/grpcbin
```
Use grpc_cli
```
brew install grpc 
==> Downloading from https://pkg-containers.githubusercontent.com/ghcr1/blobs/sha256:909f83d52b2fe4d9c2c2185183940162a4b2e189103d6f65a92b14714ec3abd6?se=2022-01-31T14%3A55%3A00Z&sig=HXzdw0%2BAyFd8%2FOYG
######################################################################## 100.0%
==> Installing dependencies for grpc: abseil, protobuf and re2
==> Installing grpc dependency: abseil
==> Pouring abseil--20211102.0.monterey.bottle.tar.gz
🍺  /usr/local/Cellar/abseil/20211102.0: 586 files, 6.9MB
==> Installing grpc dependency: protobuf
==> Pouring protobuf--3.19.4.monterey.bottle.tar.gz
🍺  /usr/local/Cellar/protobuf/3.19.4: 270 files, 19.6MB
==> Installing grpc dependency: re2
==> Pouring re2--20211101.monterey.bottle.tar.gz
🍺  /usr/local/Cellar/re2/20211101: 15 files, 448.6KB
==> Installing grpc
```

https://github.com/grpc/grpc/blob/master/doc/command_line_tool.md

Only for unsecured:
```
grpc_cli ls localhost:9000  -l   

```

Or use `grpcurl`
```
brew install grpcurl
grpcurl -plaintext localhost:9000 list
addsvc.Add
grpc.gateway.examples.examplepb.ABitOfEverythingService
grpc.reflection.v1alpha.ServerReflection
grpcbin.GRPCBin
hello.HelloService

```

Make sure installed:
```
protoc --version
```

```
➜  cloudservices git:(grpc) protoc activity-log/api/v1/*.proto --go_out=.      
protoc-gen-go: program not found or is not executable
Please specify a program using absolute path or make sure the program is available in your PATH system variable
--go_out: protoc-gen-go: Plugin failed with status code 1.
```
See here:

https://grpc.io/docs/languages/go/quickstart/


```
$ go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.26
```

``` ~/.zshrc
export PATH="$PATH:$(go env GOPATH)/bin"
```

## generate things

```
protoc activity-log/api/v1/*.proto --go_out=. --go_opt=paths=source_relative --proto_path=.
```

## GRPC

here is how we generate it
```
$ go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.1
```

## Problem:
```
cannot use srv (variable of type *grpcServer) as api_v1.Activity_LogServer value in argument to api1.RegisterActivity_LogServer: missing method Insert
```
Solution: Adding UnImplemented
```
type grpcServer struct {
	api1.UnimplementedActivity_LogServer
	Activities *Activities
}
```

```

// UnimplementedActivity_LogServer must be embedded to have forward compatible implementations.
type UnimplementedActivity_LogServer struct {
}

func (UnimplementedActivity_LogServer) Insert(context.Context, *Activity) (*Activity, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Insert not implemented")
}
func (UnimplementedActivity_LogServer) Retrieve(context.Context, *RetrieveRequest) (*Activity, error) {
	return nil, status.Errorf(codes.Unimplemented, "method Retrieve not implemented")
}
func (UnimplementedActivity_LogServer) List(context.Context, *ListRequest) (*Activities, error) {
	return nil, status.Errorf(codes.Unimplemented, "method List not implemented")
}
func (UnimplementedActivity_LogServer) mustEmbedUnimplementedActivity_LogServer() {}
```

With this in place, I can make calls:
```
grpcurl -plaintext -d '{ "id": 10 }' localhost:8080 api.v1.Activity_Log/Retrieve
ERROR:
  Code: Unimplemented
  Message: method Retrieve not implemented
```

GRPC has an introspection feature, that can be used to list what end points are available, but if I try it at first it fails:

```
 grpcurl -plaintext localhost:8080 describe
Error: server does not support the reflection API
```
first you need to do this:
```
https://github.com/grpc/grpc-go/blob/master/Documentation/server-reflection-tutorial.md
```

```
 grpcurl -plaintext localhost:8080 describe
api.v1.Activity_Log is a service:
service Activity_Log {
  rpc Insert ( .api.v1.Activity ) returns ( .api.v1.Activity );
  rpc List ( .api.v1.ListRequest ) returns ( .api.v1.Activities );
  rpc Retrieve ( .api.v1.RetrieveRequest ) returns ( .api.v1.Activity );
}
grpc.reflection.v1alpha.ServerReflection is a service:
service ServerReflection {
  rpc ServerReflectionInfo ( stream .grpc.reflection.v1alpha.ServerReflectionRequest ) returns ( stream .grpc.reflection.v1alpha.ServerReflectionResponse );
}
```

`grpc_cli` which comes with grpc also works well for this
```
grpc_cli ls localhost:8080 -l
filename: activity-log/api/v1/activity.proto
package: api.v1;
service Activity_Log {
  rpc Insert(api.v1.Activity) returns (api.v1.Activity) {}
  rpc Retrieve(api.v1.RetrieveRequest) returns (api.v1.Activity) {}
  rpc List(api.v1.ListRequest) returns (api.v1.Activities) {}
}

filename: reflection/grpc_reflection_v1alpha/reflection.proto
package: grpc.reflection.v1alpha;
service ServerReflection {
  rpc ServerReflectionInfo(stream grpc.reflection.v1alpha.ServerReflectionRequest) returns (stream grpc.reflection.v1alpha.ServerReflectionResponse) {}
}
```

Now I just have to implement this interface:

```
// Activity_LogServer is the server API for Activity_Log service.
// All implementations must embed UnimplementedActivity_LogServer
// for forward compatibility
type Activity_LogServer interface {
	Insert(context.Context, *Activity) (*Activity, error)
	Retrieve(context.Context, *RetrieveRequest) (*Activity, error)
	List(context.Context, *ListRequest) (*Activities, error)
	mustEmbedUnimplementedActivity_LogServer()
}
```

not clear how `mustEmbedUnimplementedActivity_LogServer` works.



## Client

I was wondering how the client was going to work. How does the client code get generated, but actually its already been generated, and I can use it.

## Questions
 - when to use int, int32, uint64 ?
 - what about hte locks and the pointers and stuff


## Base stuff

This client here is helpful:
https://github.com/grpc/grpc-go/blob/master/examples/helloworld/greeter_client/main.go

First I have to connect to the client
```

```

Then I can write my insert like this:
```

```
and use it like this:
```
```

Problem:
````
go run cmd/client/main.go -get 3
Error: Insert failure: rpc error: code = Canceled desc = context canceled
exit status 1
```
Solution:
```
I had called defer cancel in my constructor.
```

Problem:
```
go run cmd/client/main.go -get 1
Error: Insert failure: rpc error: code = Canceled desc = grpc: the client connection is closing
exit status 1
```
Problem here was I closed the connection

# Error handling
By default your errors will only have a string description, but you
may want to include more information such as a status code or some other
arbitrary data.


We do this like this
NB: need code above this to not use status
```
old:
return nil, fmt.Errorf("Internal Error: %w", err)

new:
		return nil, status.Error(codes.NotFound, "id was not found")

```

then we can unwrap it like this:
```

```