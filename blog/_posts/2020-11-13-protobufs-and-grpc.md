---
title: Using gRPC with Golang, Python, and Ruby
toc: true
categories:
  - Golang
  - Python
author: Alex
internal-links:
   - grpc
topic: python
funnel: 2
topcta: false
excerpt: |
    Learn how to use gRPC with Golang, Python, and Ruby to implement a key-value store microservice. This tutorial provides step-by-step instructions and code examples for each language, making it easy to understand and follow along.
last_modified_at: 2023-07-14
---
I was surprised to learn that Google protocol buffers (protobufs), were first introduced nearly two decades ago. They were used internally at google as early as 2001 and were open sourced 2008.

Following this success, in 2016 Google released gRPC. gRPC offered a way to define remote procedure calls using protobufs for serialization. Due to protobuf's binary serialization format, it offered a significant speed up compared to using JSON over HTTP. The use of proto files for a precise definition of a service's API. This was a big innovation.

gRPC is a great solution for communicating between internal microservices. There's [plenty](https://phenopackets-schema.readthedocs.io/en/latest/protobuf.html) [of](https://www.ionos.ca/digitalguide/websites/web-development/protocol-buffers-explained/) [articles](https://www.baeldung.com/google-protocol-buffer) and documentation that covers [protobufs](https://developers.google.com/protocol-buffers) and [gRPC](https://grpc.io/), but when I am considering a new technology, I learn best by seeing a working example. In this blog post I'm going build an example using Go, Python and Ruby.

## First Step: Implementing a gRPC Client using Go

Let's write an in-memory key/value micro-service in Go, and some clients in both Python and Ruby.

Our server will allow users to set and get data from a key/value store.

{% include imgf src="server.png" alt="hand drawn cartoon for a person talking to a computer server" caption="Interacting with the server" %}

First let's design our API in a proto file:

~~~{.protobuf caption="api.proto"}
    syntax = "proto3";
    package simplekeyvalue;
    option go_package = "/kvapi";
    
    // The key/value API contains two procedures for storing
    // and retrieving data
    
    service KeyValue {
      rpc Set (SetRequest) returns (SetReply) {}
      rpc Get (GetRequest) returns (GetReply) {}
    }
    
    // SetRequest contains a key and value to set
    message SetRequest {
      string key = 1;
      string value = 2;
    }
    
    // SetReply contains nothing
    message SetReply {
    }
    
    // GetRequest contains a key and value to set
    message GetRequest {
      string key = 1;
    }
    
    // GetReply contains the value
    message GetReply {
      string value = 1;
    }

~~~

Next we need to compile this proto file into Go code. On a Mac one might be tempted to run _brew install protobuf_, or if you're on Linux you might want to see if _apt-get install protoc_ will magically work, but rather than do that, we will use earthly to containerize these tools. This will allow you to share this code with other developers, and ensure everyone can compile proto files across multiple platforms using the same version to eliminate compatibility issues.

Here's what an Earthfile would look like for installing Google protobufs inside an Ubuntu image, and generating the protobuf code using the protoc-gen-go-grpc tool:

~~~{.dockerfile caption="Earthfile"}
    FROM ubuntu:20.10
    WORKDIR /defs
    
    RUN apt-get update && apt-get install -y wget unzip
    
    # setup protoc
    RUN wget -O protoc.zip
    https://github.com/protocolbuffers/protobuf/releases/download/v3.13.0/protoc-3.13.0-linux-x86_64.zip
    
    RUN unzip protoc.zip -d /usr/local/
    
    proto-go:
      RUN apt-get install -y golang git
      ENV GO111MODULE=on
      ENV PATH=$PATH:/root/go/bin
      RUN go get google.golang.org/protobuf/cmd/protoc-gen-go \
          google.golang.org/grpc/cmd/protoc-gen-go-grpc
      COPY api.proto /defs
      RUN mkdir /defs/go-api
      RUN protoc --proto_path=/defs --go_out=/defs/go-api \
          --go-grpc_out=/defs/go-api /defs/api.proto
      SAVE ARTIFACT ./go-api/kvapi AS LOCAL kvapi

~~~

This will then produce two go files under the `kvapi` directory: `api.pb.go` and `api\_grpc.pb.go` which contains the auto generated protobuf and grpc code respectively.

At this point, assuming that earth is already [installed](https://docs.earthly.dev/install), give it a try for yourself with code from our [example repository](https://github.com/earthly/example-grpc-key-value-store):

~~~{.bash caption=">_"}
    git clone https://github.com/earthly/example-grpc-key-value-store.git
    cd example-grpc-key-value-store/proto
    earth +proto-go
~~~

The next step is to write the server code that will implement the set and get methods:

~~~{.go caption="main.go"}
    package main
    
    import (
     "context"
     "fmt"
     "log"
     "net"
    
     "github.com/earthly/example-grpc-key-value-store/go-server/kvapi"
    
     "google.golang.org/grpc"
    )
    
    const (
     port = ":50051"
    )
    
    var errKeyNotFound = fmt.Errorf("key not found")
    
    // server is used to implement kvapi.KeyValueServer
    type server struct {
     kvapi.UnimplementedKeyValueServer
     data map[string]string
    }
    
    // Set stores a given value under a given key
    func (s *server) Set(ctx context.Context, in *kvapi.SetRequest) (*kvapi.SetReply, error) {
     key := in.GetKey()
     value := in.GetValue()
     log.Printf("serving set request for key %q and value %q", key, value)
    
     s.data[key] = value
    
     reply := &kvapi.SetReply{}
     return reply, nil
    }
    
    // Get returns a value associated with a key to the client
    func (s *server) Get(ctx context.Context, in *kvapi.GetRequest) (*kvapi.GetReply, error) {
     key := in.GetKey()
     log.Printf("serving get request for key %q", key)
    
     value, ok := s.data[key]
     if !ok {
      return nil, errKeyNotFound
     }
    
     reply := &kvapi.GetReply{
      Value: value,
     }
     return reply, nil
    }
    
    func main() {
     lis, err := net.Listen("tcp", port)
     if err != nil {
      log.Fatalf("failed to listen: %v", err)
     }
     log.Printf("Listening on %s", port)
     serverInstance := server{
      data: make(map[string]string),
     }
     s := grpc.NewServer()
     kvapi.RegisterKeyValueServer(s, &serverInstance)
     if err := s.Serve(lis); err != nil {
      log.Fatalf("failed to serve: %v", err)
     }
    }
~~~

Next we will compile the go code and save it as a docker image with the following Earthfile:

~~~{.dockerfile caption="Earthfile"}
    FROM golang:1.13-alpine3.11
    
    WORKDIR /kvserver
    
    kvserver:
        COPY go.mod go.sum ./
        RUN go mod download
        COPY ../proto+proto-go/kvapi kvapi
        COPY --dir cmd ./
        RUN go build -o kvserver cmd/server/main.go
        SAVE ARTIFACT kvserver
    
    kvserver-docker:
        FROM alpine:latest
        COPY +kvserver/kvserver /kvserver
        ENTRYPOINT /kvserver
        SAVE IMAGE as kvserver:latest
~~~

You can give it a try on your own by using our example code in our GitHub repository, just run:

~~~{.bash caption=">_"}
    git clone https://github.com/earthly/example-grpc-key-value-store.git
    cd example-grpc-key-value-store/go-server
    earth +kvserver-docker
~~~

Then start up the server in Docker, by running:

~~~{.bash caption=">_"}
    docker run --rm --network=host kvserver:latest
~~~

* * *

## Next step: Implementing a gRPC Client Using Python

Now that we've built and launched our Go-based key-value-store server, we'll cover how to talk to it using a Python client. Remember that initial Earthfile that generated the Go code? We'll extend it to _pip install grpc_ tooling, and generate Python code:

~~~{.dockerfile caption="Earthfile"}
    proto-py:
      RUN apt-get install -y python3 python3-pip
      RUN pip3 install grpcio grpcio-tools
      COPY api.proto /defs
      RUN mkdir /defs/py-api
      RUN python3 -m grpc_tools.protoc -I /defs --python_out=/defs/py-api \
          --grpc_python_out=/defs/py-api /defs/api.proto
      SAVE ARTIFACT ./py-api /py-pb AS LOCAL py-pb
~~~

Then we'll create a client that reads command line arguments, and if the argument contains an equals sign, it will store the value in the server, and otherwise it will retrieve the value from the server:

~~~{.python caption="Earthfile"}
    import sys
    import grpc
    
    import api_pb2
    import api_pb2_grpc
    
    addr = '127.0.0.1:50051'
    
    if len(sys.argv) < 2:
        print('program requires arguments in the form key, or key=value')
        sys.exit(1)
    
    channel = grpc.insecure_channel(addr)
    stub = api_pb2_grpc.KeyValueStub(channel)
    
    for arg in sys.argv[1:]:
        if '=' in arg:
            # send a value to the server
            key, value = arg.split('=')
            try:
                set_request = api_pb2.SetRequest(key=key, value=value)
                set_response = stub.Set(set_request)
            except grpc.RpcError as e:
                print(f'failed to send key to server: {e.details}')
            else:
                print(f'sent "{key}" to server')
        else:
            # get a value from the server
            key = arg
            try:
                get_request = api_pb2.GetRequest(key=key)
                get_response = stub.Get(get_request)
            except grpc.RpcError as e:
                print(f'failed to get key from server: {e.details}')
            else:
                value = get_response.value
                print(f'server returned value "{value}" for key "{key}"')

~~~

We then store this python code, along with the generated gRPC protobuf code with the following Earthfile:

~~~{.dockerfile caption="Earthfile"}
    FROM python:3
    
    RUN pip install grpcio protobuf pycodestyle
    
    WORKDIR /kvclient
    
    code:
        COPY client.py .
        COPY ../proto+proto-go/go-pb kvapi
    
    lint:
        FROM +code
        RUN pycodestyle client.py
    
    kvclient-docker:
        FROM +code
        SAVE IMAGE as python-kvclient:latest
    
    all:
        BUILD +lint
        BUILD +kvclient-docker

~~~

You can give it a try for yourself with the example code:

~~~{.bash caption=">_"}
    git clone https://github.com/earthly/example-grpc-key-value-store.git
    cd example-grpc-key-value-store/python-client
    earth +kvclient-docker
~~~

Then you can run it and set the weather to sunny with:

~~~{.bash caption=">_"}
    docker run --rm --network=host python-kvclient:latest python3 \
    /kvclient/client.py weather=sunny
~~~

And if all went well, you should see some output on both the client and server consoles:

~~~{.bash caption="Output"}
    # client output
    sent "weather" to server
    
    # server output
    2020/11/12 23:15:18 Listening on :50051
    2020/11/12 23:15:34 serving set request for key "weather" and value "sunny"
~~~

* * *

## Final Step: Implementing a gRPC Client Using Ruby

We've come a long ways with our Go and Python gRPC examples, but what if you also wanted to include a Ruby gRPC client implementation too? Well let's extend our proto Earthfile to generate Ruby protobufs too:

~~~{.dockerfile caption="Earthfile"}
    proto-rb:
      RUN apt-get install -y ruby
      RUN gem install grpc grpc-tools
      COPY api.proto /defs
      RUN mkdir /defs/rb-api
      RUN grpc_tools_ruby_protoc -I /defs --ruby_out=/defs/rb-api \
      --grpc_out=/defs/rb-api /defs/api.proto
      SAVE ARTIFACT ./rb-api /rb-pb AS LOCAL rb-pb

~~~

We can then use this generated Ruby gRPC code with a simple ruby client example that performs a get request for keys listed as command line arguments:

~~~{.ruby caption="client.rb"}
    $LOAD_PATH.unshift '.'
    
    require 'grpc'
    require 'api_pb'
    require 'api_services_pb'
     
    stub = Simplekeyvalue::KeyValue::Stub.new(
      '127.0.0.1:50051', :this_channel_is_insecure
    )
     
    ARGV.map do |arg|
      request = Simplekeyvalue::GetRequest.new(key: arg)
      response = stub.get(request)
      puts response.value
    end
~~~

~~~{.bash caption=">_"}
    git clone https://github.com/earthly/example-grpc-key-value-store.git
    cd example-grpc-key-value-store/ruby-client
    earth +kvclient-docker
~~~

Then you can try querying the server to see what the weather was set to:

~~~{.bash caption=">_"}
    docker run --rm --network=host ruby-kvclient:latest \
    ruby /kvclient/client.rb weather
~~~

And if all went well, it'll tell you that it's sunny outside.
{% include imgf src="sun.png" alt="drawing of the sunn" caption="It's Sunny Outside"%}

So there we go. You can find the code for the server, the two clients, and a bonus integration test in [GitHub](https://github.com/earthly/example-grpc-key-value-store).
