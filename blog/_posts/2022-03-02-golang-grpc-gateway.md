---
title: "gRPC Gateway"
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - just an example
---

## Intro

Welcome back. I’m an experienced developer, learning Golang. Last time I moved my service from REST to gRPC but there are times when http and REST is still needed. So Today, I'm going to build a gRPC gateway that accepts http rest requests and proxies it through to my gRPC service. And I'm actually going to do it three ways.

The First way is to build a proxy using grpc-gateway and an existing proto file. This method is great if you have an existing gRPC service that you don't want to touch. It's also the only way I'll cover that will work great with a non-golang service. You can use it to proxy to any service that speaks gRPC. 

The second way will be to will be to build a REST service, using the same proto file but that actually uses the same implementation as the existing gRPC service. Assuming you have a shared backing database this means you could scale the REST endpoint seperately from the gRPC endpoint.

The third solution is the most fun. I'll change my original gRPC service to answer both REST and gRPC requests over the same port. And to get that working, I'm going to have to learn a bit about TLS, and cert generation and HTTP/2.

Ok, lets start. The first thing I need to do is get the GRPC gateway plugin:

```
go get github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-grpc-gateway
```

Then I update my protoc invocation to use this plugin:
```
    RUN protoc api/v1/*.proto \
            --go_out=. \
            --go_opt=paths=source_relative \
            --go-grpc_out=. \
            --go-grpc_opt=paths=source_relative \
+            --grpc-gateway_out . \
+            --grpc-gateway_opt logtostderr=true \
+            --grpc-gateway_opt paths=source_relative \
+            --grpc-gateway_opt generate_unbound_methods=true \
```

My proto file looks contains this service:

```
service Activity_Log {
    rpc Insert(Activity) returns (InsertResponse) {}
    rpc Retrieve(RetrieveRequest) returns (Activity) {}
    rpc List(ListRequest) returns (Activities) {}
}
```

with that, I get a new generated file `activity.pb.go` which I can use to build a stand alone gRPC proxy in GoLang.

## gRPC Proxy

So I create a new folder and a new main file and I import the generated code. 

```
package main

import (
	"context"
	"log"
	"net/http"

	"github.com/grpc-ecosystem/grpc-gateway/v2/runtime"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"

	api "github.com/adamgordonbell/cloudservices/activity-log/api/v1"
)
```

And I tell this service how to connect to my existing gRPC service:
```

func main() {

  var grpcServerEndpoint = "localhost:8080"
	mux := runtime.NewServeMux()
	opts := []grpc.DialOption{grpc.WithTransportCredentials(insecure.NewCredentials())}
	err := api.RegisterActivity_LogHandlerFromEndpoint(context.Background(), mux, grpcServerEndpoint, opts)
	if err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
```

`grpc.DialOption` can be used to set up auth credentials, including TLS settings and JWT credentials but since the service I'm proxying to currently runs unsecured and with TLS nothing besides `insecure.NewCredentials()` is needed for now. ( Stay tuned though, It's going to come up later)

TODO: say stuff about how that works

After that, I start up the proxy, listening on port 8081
```
	log.Println("Listening on port 8081")
	port := ":8081"
	http.ListenAndServe(port, mux)
}
```
And that is it. I can start this service up, start the gRPC service up and make curl requests that get proxied through to grpc:

```

```

Ok, I have a REST end point now, but what are the endpoints? What type of request and what type of response should I expect? In all cases checked, in this version of the gRPC gateway, the expected request format and the given responses look like just a straight conversion to JSON.

GRPC request:
```
grpcurl -insecure -d '{ "id": 1 }' localhost:8080 api.v1.Activity_Log/Retrieve 
```
CURL request:
```
curl -X POST -s localhost:8081/api.v1.Activity_Log/Retrieve -d \
'{ "id": 1 }'
```

However, we can do better than just assuming it is always going to be the same. We can generate a spec for the REST service.

### OpenAPI 

OpenAPI specs, which I've always just called Swagger documents are defined like this:

> The OpenAPI Specification (OAS) defines a standard, language-agnostic interface to RESTful APIs which allows both humans and computers to discover and understand the capabilities of the service without access to source code, documentation, or through network traffic inspection. [^1]

That sounds like exactly what I need, and they are easy to generate with the `protoc-gen-openapiv2 ` protoc plugin.

```
go get github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-openapiv2
```

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
+            --openapiv2_out . \
+            --openapiv2_opt logtostderr=true \
+            --openapiv2_opt generate_unbound_methods=true \
```

After running that I get `activity.swagger.json`

```
{
  "swagger": "2.0",
  "info": {
    "title": "api/v1/activity.proto",
    "version": "version not set"
  },
  "paths": {
    "/api.v1.Activity_Log/Insert": {
     ...
    },
    "/api.v1.Activity_Log/List": {
      ...
    },
    "/api.v1.Activity_Log/Retrieve": {
      ...
    }
```
Which I can view in a more human readble form using the online [swagger editor](https://editor.swagger.io/):

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/7820.png --alt {{  }} %}
<figcaption></figcaption>
</div>

You can find the code for this gRPC proxy on github. If you have the proto files of a service you would like to proxy then all you need to do is generate the proxy and swagger file with `protoc` and then adapt the one file service to you needs.

Let's move on to the next grpc gateway example.

## REST GRPC (HTTP Frontend)

The Proxy service above is great if your gRPC service is written in a langauge besides go, or if its not your code or your service. You can interact with it from the outside and not worry about the implementation details.

However, if it is your service and if its stateless because it uses a database, there is another way do things. You can create a REST service that shares its implementation with the gRPC service. gRPC gateway can help with this was well.

To setup this configuration, I'll create a new file, rest.go, and slightly modify the code I've used above:

```
func main() {

-	var grpcServerEndpoint = "localhost:8080"
+	_, srv := server.NewGRPCServer()

	mux := runtime.NewServeMux()
- opts := []grpc.DialOption{grpc.WithTransportCredentials(insecure.NewCredentials())} 
-	err := api.RegisterActivity_LogHandlerServer(context.Background(), mux, &srv)
+ err := api.RegisterActivity_LogHandlerFromEndpoint(context.Background(), mux, grpcServerEndpoint, opts)
	if err != nil {
		log.Fatalf("failed to serve: %v", err)
	}

	log.Println("Starting listening on port 8081")
	err = http.ListenAndServe(":8081", mux)
	if err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}

```

The big change is calling `RegisterActivity_LogHandlerServer` instead of `RegisterActivity_LogHandlerFromEndpoint`, which takes the backend implementation of a GRPC service instead of a network location of an existing instance. So I just hand it the same ActivityService implementation I use and no network calls are needed to serve requests.

SQLite Note: My toy example here is using SQLite, which probably isn't a great fit for this particular solution because it involves multiple writing services. With a network based database, however, this could work quite well.

And practically, the reason I'm showing this solution is a half way step toward teh final solution: responding to HTTP rest requests and gRPC requests in a single service. So lets go there next.

### REST and gRPC in one Service

To start with I can create a service exactly like our last REST service above:
```
package main

import (
	"context"
	"log"
	"net/http"
	"strings"

	"github.com/adamgordonbell/cloudservices/activity-log/internal/server"
	"github.com/grpc-ecosystem/grpc-gateway/v2/runtime"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"

	api "github.com/adamgordonbell/cloudservices/activity-log/api/v1"
)

func main() {

	// GRPC Server
	grpcServer, srv := server.NewGRPCServer()

	// Rest Server
	mux := runtime.NewServeMux()
	err := api.RegisterActivity_LogHandlerServer(context.Background(), mux, &srv)
	if err != nil {
		log.Fatalf("failed to serve: %v", err)
	}

log.Println("Starting listening on port 8080")
	err = http.ListenAndServe(":8080", mux)
	if err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
```

I now have two possible `http.Handler`'s: one is returned by `grpcServer.ServeHTTP` and one by `mux.ServeHTTP`. So all I need now is a way to choose the correct one on a per request basis. The Content-Type headers are a great way to do this.

```golang
func grpcHandlerFunc(grpcServer grpc.Server, otherHandler http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.ProtoMajor == 2 && strings.HasPrefix(
			r.Header.Get("Content-Type"), "application/grpc") {
			log.Println("GRPC")
			grpcServer.ServeHTTP(w, r)
		} else {
			log.Println("REST")
			otherHandler.ServeHTTP(w, r)
		}
	})
}
```

grpcHandlerFunc sends all gRPC content types to the grpc and defaults everything else to a secondary source, which of me will be the rest service:

```
func main() {
  ...
	log.Println("Starting listening on port 8080")
- err = http.ListenAndServe(":8080", mux)
+	err = http.ListenAndServe(":8080", grpcHandlerFunc(*grpcServer, mux))
	if err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
```

And if I start that up, I should have a working service than can handle REST and gRPC.

....

Ok, well maybe not. Before I get it working I need to explain a little about what is getting in my way.


#### What is HTTP/2

HTTP 1 uses the simple model of making requests I was introduced to in a networking class. A TCP connection is established, then a resource is requested and then the TCP connection is ended. 

However, as webpages got more complex, they involved more and more resources and the time to establish a connection and then hang up became a significant bottleneck. HTTP/2 solves this problem by allowing the TCP connection once established to remain open and serve many resource requests.

gRPC uses HTTP/2 as its transport medium, HTTP/1 will not do. This makes my solution a bit more complex because I need to make sure any request I recieve is part of an HTTP/2 connection. Thankfully, this is totally possible using the goLang std lib `http.Server`so long as I use `ListenAndServeTLS` to establish a TLS connection. Which means its time for me to start generating certificates.

### Side Quest: TLS

Transport Layer Security is a huge topic, probably in need of its own whole article. So to keep things on track, I'll just mention that TLS uses public key cryptography to establish a secure connection between two parties, and uses a certification authority to validate that a party is who they say they are.

I'm going to be using CloudFlare's [CFSSL](https://github.com/cloudflare/cfssl) to generate a self signed certificate authority and then using that CA to generate a certificate for my service.

First I install CFSSL:
```
go get github.com/cloudflare/cfssl/cmd/cfssl \
      github.com/cloudflare/cfssl/cmd/cfssljson
```

Then I create my certificate signing request (`cs-crs.json`):
```json 
{
    "CN": "Earthly Example Code CA",
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "CA",
            "L": "ON",
            "ST": "Peterborough",
            "O": "Earthly Example Code",
            "OU": "CA"
        }
    ]
}
```
Then I need to define the CA's signing policies ('ca-config.json`):
```
{
    "signing": {
        "default": {
            "expiry": "168h"
        },
        "profiles": {
            "server": {
                "expiry": "8760h",
                "usages": [
                    "signing",
                    "key encipherment",
                    "server auth"
                ]
            }
        }
    }
}
``` 

CFSSL uses those policies, like a one year expiring ( 8760h) when creating the server certificate. Next I need to create a certificate signing request for the server. I need to specify which hosts its valid for and what encryption alogorithm to use. It ends up looking like this (server-csr.json):

```{
    "CN": "127.0.0.1",
    "hosts": [
        "localhost",
        "127.0.0.1",
        "activity-log"
    ],
    "key": {
        "algo": "rsa",
        "size": 2048
    },
    "names": [
        {
            "C": "CA",
            "L": "ON",
            "ST": "Peterborough",
            "O": "Earthly Example Code",
            "OU": "CA"
        }
    ]
}
```

With all those files in place, I can generate my CA private key (ca-key.pem) and certificate (ca.pem) and then my server private key (server-key.pem) and certificate (server.pem).

```
cfssl gencert -initca ca-csr.json | cfssljson -bare ca
cfssl gencert -ca ca.pem -ca-key=ca-key.pem -config ca-config.json \
               -profile=server server-csr.json | cfssljson -bare server 
```

With all that generation in place, and wrapped up in a nice [Earth file target](), I can start building my REST + gRPC service.

## Testing it

#### HTTP

#### gRPC

### Client

### Side quest: Don't Verify

### Proxy Alternatives

## Silly: Making certs work with Proxy and Activity Log

## Conclusion

## Notes

--
details

Starting with <https://github.com/grpc-ecosystem/grpc-gateway>

install stuff

```
 go install \
    github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-grpc-gateway \
    github.com/grpc-ecosystem/grpc-gateway/v2/protoc-gen-openapiv2 \
    google.golang.org/protobuf/cmd/protoc-gen-go \
    google.golang.org/grpc/cmd/protoc-gen-go-grpc
```

Had to run go get as well. Not totally suer why

```
 require (
-       github.com/golang/protobuf v1.5.0 // indirect
-       golang.org/x/net v0.0.0-20200822124328-c89045814202 // indirect
-       golang.org/x/sys v0.0.0-20200323222414-85ca7c5b95cd // indirect
-       golang.org/x/text v0.3.0 // indirect
-       google.golang.org/genproto v0.0.0-20200526211855-cb27e3aa2013 // indirect
+       github.com/golang/glog v1.0.0 // indirect
+       github.com/golang/protobuf v1.5.2 // indirect
+       github.com/grpc-ecosystem/grpc-gateway/v2 v2.7.3 // indirect
+       golang.org/x/net v0.0.0-20210405180319-a5a99cb37ef4 // indirect
+       golang.org/x/sys v0.0.0-20210510120138-977fb7262007 // indirect
+       golang.org/x/text v0.3.5 // indirect
+       google.golang.org/genproto v0.0.0-20220118154757-00ab72f36ad5 // indirect
+       google.golang.org/grpc/cmd/protoc-gen-go-grpc v1.2.0 // indirect
+       gopkg.in/yaml.v2 v2.4.0 // indirect
+       sigs.k8s.io/yaml v1.3.0 // indirect
 )
```

example:
<https://web.archive.org/web/20160306083908/https://coreos.com/blog/grpc-protobufs-swagger.html>

using the proxy:

```
curl -v  -X POST -s localhost:8080/api.v1.Activity_Log/Insert -d \
'{"activity": {"description": "christmas eve bike class", "time":"2021-12-09T16:34:04Z"}}'
```

Problems:
```
2022/02/24 14:51:47 http: TLS handshake error from 127.0.0.1:61470: tls: first record does not look like a TLS handshake
```
I was doing this, when I had no TLS stuff setup:
```
err = srv.Serve(tls.NewListener(conn, srv.TLSConfig))
```

Making an HTTP server that doens't proxy, but processes the requests:
...
 
see commit 6230e9f

### GRPC 
// The provided HTTP request must have arrived on an HTTP/2
// connection. When using the Go standard library's server,
// practically this means that the Request must also have arrived
// over TLS.

What is http/2?

Then I need to follow the cret creation guide:
https://github.com/denji/golang-tls

But then:
```
2022/02/25 09:33:43 http: TLS handshake error from 127.0.0.1:53499: remote error: tls: bad certificate
```

```
2022/02/25 09:34:40 http: TLS handshake error from [::1]:53511: remote error: tls: unknown certificate
```

From the book
cfssl gencert -initca ca-csr.json | cfssljson -bare ca

cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=server server-csr.json | cfssljson -bare server


If you use curl on http you need to `-k` or you get
Client sent an HTTP request to an HTTPS server.


## Question

how do I get ca cert compiled into program?

Getting problems like this:


```
curl -X POST -s localhost:8081/api.v1.Activity_Log/List -d \
'{ "offset": 0 }'
{"code":14, "message":"connection error: desc = \"transport: Error while dialing dial tcp 127.0.0.1:8080: connect: connection refused\"", "details":[]}%
```

Because of docker netowrking and needing to refer to things by name.

Then, needed to update cert and then got:
```
TLS: private key does not match public key
```


