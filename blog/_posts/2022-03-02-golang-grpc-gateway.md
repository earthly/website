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
