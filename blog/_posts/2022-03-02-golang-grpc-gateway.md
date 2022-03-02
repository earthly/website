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

### Proxy Alternatives - Kong gRPC-gateway

An stand-in alternative to the above is the KONG [gRPC-gateway](https://docs.konghq.com/hub/kong-inc/grpc-gateway/). If you are using as an API gateway then by enabling the grpc-gateway plugin and configuring things correctly you can get an equivalent proxy setup for you.

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

```
grpcurl -insecure localhost:8080 api.v1.Activity_Log/List
```
```
Failed to dial target host "localhost:8080": tls: first record does not look like a TLS handshake
```

Ok, well maybe not. Before I get it working I need to explain a little about TLS and HTTP/2 because they are getting in my way.


#### What is HTTP/2

Here is how HTTP was explained to me in a networking class once: A TCP connection is established, then a resource is requested and then the TCP connection is ended. That is how HTTP/1 works.

However, as webpages got more complex, they involved more and more resources and the time to establish a connection and then hang up became a significant bottleneck. HTTP/2 solves this problem by allowing the TCP connection once established to remain open and serve many resource requests.

gRPC uses HTTP/2 as its transport medium, HTTP/1 will not do. This makes my solution a bit more complex because I need to make sure any request I recieve is part of an HTTP/2 connection. Thankfully, this is totally possible using the goLang std lib `http.Server`so long as I use `ListenAndServeTLS` to establish a TLS connection. Which means its time for me to start generating certificates.

### Side Quest: Generating TLS Certs

Transport Layer Security is a huge topic, probably in need of its own whole article. So to keep things on track, I'll just mention that TLS uses public key cryptography to establish a secure connection between two parties, and uses a certification authority to validate that a party is who they say they are.

I'm going to be using CloudFlare's [CFSSL](https://github.com/cloudflare/cfssl) to generate a self signed certificate authority and then using that CA to generate a certificate for my service. Using your own certificate authority is  great for internal services. For externally facing services, you probably want something like Let's Encrypt. 

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

With all that generation in place, and wrapped up in a nice [Earth file target](), my side quest is over and I can head back to my service.

## TLS Time

Now that I have my certs, all I need to do is start using `ListenAndServeTLS` with my certificate and private key:

```
	log.Println("Starting listening on port 8080")
- err = http.ListenAndServe(":8080", grpcHandlerFunc(*grpcServer, mux))
+	err = http.ListenAndServeTLS(":8080", "./certs/server.pem", "./certs/server-key.pem", grpcHandlerFunc(*grpcServer, mux))
	if err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
```

And then I can make grpc request:
```
 grpcurl localhost:8080 api.v1.Activity_Log/List
```
```
Failed to dial target host "localhost:8080": x509: certificate signed by unknown authority
```

My TLS cert is signed by certificate authority that my machine is not aware of. I'm on MacOS and it is simple to add `ca.pem` to keychain but that seems like overkill for this situation. Instead I can just use the `-insecure` flag.

```
 grpcurl -insecure localhost:8080 api.v1.Activity_Log/List
{
  "activities": [
    {
      "id": 2,
      "time": "1970-01-01T00:00:00Z",
      "description": "christmas eve bike class"
    }
  ]
}
```

And for curl I can use `-k`:

```
curl -k -X POST -s https://localhost:8080/api.v1.Activity_Log/List -d \
'{ "offset": 0 }' 
{
  "activities": [
    {
      "id": 2,
      "time": "1970-01-01T00:00:00Z",
      "description": "christmas eve bike class"
    }
}
```
There we go, a single service that support gRPC and REST requests. Let's test it with my gRPC client:

```
./activity-client -list
```
```
http: TLS handshake error from [::1]:55763: tls: first record does not look like a TLS handshake
```

Of course, I need to tell the client to use a TLS connection.
```
func NewActivities(URL string) Activities {
- conn, err := grpc.Dial(URL, grpc.WithTransportCredentials(insecure.NewCredentials()))	
+	tlsCreds = credentials.NewTLS(&tls.Config{})
+	conn, err := grpc.Dial(URL, grpc.WithTransportCredentials(tlsCreds))
	if err != nil {
		log.Fatalf("did not connect: %v", err)
	}
	client := api.NewActivity_LogClient(conn)
	return Activities{client: client}
}
```
That gets me part of the way there.
```
go run cmd/client/main.go --list
```
```
Error: List failure: rpc error: code = Unavailable desc = connection error: desc = "transport: authentication handshake failed: x509: certificate signed by unknown authority"
```
 I am now connecting over TLS, but my client has no idea about my one off certificate authority. I can take the same approach I had used with grpcurl, and tell the client not to verify the cert:
 ```
 tlsCreds = credentials.NewTLS(&tls.Config{
		InsecureSkipVerify: true,
	})
	conn, err := grpc.Dial(URL, grpc.WithTransportCredentials(tlsCreds))
 ```

But, better than that, is that I make all my internal services aware of my certificate authority:

```
tlsCreds, err := credentials.NewClientTLSFromFile("../activity-log/certs/ca.pem", "")
	if err != nil {
		log.Fatalf("No cert found: %v", err)
	}
	conn, err := grpc.Dial(URL, grpc.WithTransportCredentials(tlsCreds))
```

And with that change, my gRPC client and server can communicate over TLS and my server can also respond to REST requests, which are all documented in a REST request.

### Sidenote: Fixing the Proxy

The proxy created in the first step is now no longer needed, because I can answer REST requests directly in the service. But also, its now broken, because much like the client was connecting insecurely and it doesn't know about the CA I created. 

Leaving things broken is bad form so I can fix it like this. 

```
func main() {
	log.Println("Starting listening on port 8081")
	port := ":8081"
	mux := runtime.NewServeMux()
+	tlsCreds, err := credentials.NewClientTLSFromFile("../activity-log/certs/ca.pem", "")
+	if err != nil {
+		log.Fatalf("No cert found: %v", err)
+	}
-	    opts := []grpc.DialOption{grpc.WithTransportCredentials(insecure.NewCredentials())}
+	opts := []grpc.DialOption{grpc.WithTransportCredentials(tlsCreds)}
	err = api.RegisterActivity_LogHandlerFromEndpoint(context.Background(), mux, grpcServerEndpoint, opts)
	if err != nil {
		log.Fatalf("failed to serve: %v", err)
	}

	err = http.ListenAndServe(port, mux)
	if err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
```

## Conclusion

There we have it. Rest to gRPC three ways, with all the complicated bits documented in a runnable [Earthfile](). With certs in place the gRPC + Rest service is not even that big of a lift from a standard gRPC solution. If fact, this approach is in use in [etcd](https://github.com/etcd-io/etcd/blob/main/server/embed/serve.go) and [istio](https://github.com/istio/istio/blob/f46f821fb13b7fc24b5d29193e2ad7c5c0a46877/pilot/pkg/bootstrap/server.go#L469)

