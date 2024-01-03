---
title: "How to Handle Secrets with BuildKit"
categories:
  - Tutorials
toc: true
author: Rajkumar Venkatasamy

internal-links:
 - just an example
excerpt: |
    This markdown content provides a checklist for writing and publishing an article, including steps such as outlining, drafting, proofreading, creating a header image, and adding internal links. It also includes a checklist for optimizing an article for external publication, including adding an author page, optimizing images, and incorporating external links.
---

When it comes to modern containerization and Docker image building, security and efficiency are important. From API keys and database passwords to encryption keys and access tokens, secrets are the digital guardians of your applications' most sensitive information, and handling these secrets in an age of cloud-native architectures can be tricky.

Enter [BuildKit](https://docs.docker.com/build/buildkit/), the unsung hero in the Docker ecosystem. While Docker containers have become the de facto standard for packaging applications, BuildKit is the powerhouse responsible for constructing these containers.

In this article, you'll learn more about how you can use BuildKit to handle secrets.

## What Is BuildKit?

BuildKit is a modern build subsystem designed to revolutionize the way developers construct container images. Unlike its predecessor, the "legacy builder," BuildKit has [numerous enhancements and innovative features](https://docs.docker.com/build/buildkit/#overview) that make it a versatile and indispensable tool for those seeking to optimize their containerization workflow.

BuildKit boosts build performance through parallelization and caching. It employs a unique, fully concurrent build graph solver that can execute build steps and discard noncontributory commands. Additionally, BuildKit has revamped the traditional builder's caching model. It directly tracks the checksums of build graphs and associated content, leading to faster, more precise, and more flexible caching. The build cache can be moved to a registry for retrieval by subsequent invocations on any machine.

Another notable feature is secrets handling. BuildKit introduces a secure mechanism for managing secrets during the Docker image build process, ensuring that critical information, such as API keys and credentials, is never exposed within the Dockerfile or the final image. This not only strengthens the security posture of your containerized applications but also aligns with [best practices for secrets management](https://developer.cyberark.com/blog/container-security-best-practices-for-secrets-management-in-containerized-environments/) in modern development and deployment workflows.

## How to Handle Docker Secrets Using BuildKit

In this tutorial, you'll learn how to secure a build secret with Docker BuildKit secrets. To follow along, you'll need [Docker](https://www.docker.com/) or [Docker Desktop](https://www.docker.com/products/docker-desktop/) (23.0 or newer) installed on your machine. This article uses version 24.0 of Docker Desktop.

In this scenario, you're going to be working with a software company named XYZ Corporation, that has developed a microservice-based architecture. During the build process, several resources need to be downloaded from XYZ's servers. The servers have authentication set up, so proper credentials must be supplied during the build process.

However, developers at XYZ Corporation currently embed the credentials directly into Dockerfiles or environment variables during the build process. This poses a security risk because the keys may accidentally end up in the final Docker image or be exposed in source control.

To emulate this scenario, you'll write a simple Python program that reads a file and prints its output. The file is populated during the build process by making an HTTP request to a remote server. The remote server is protected by basic authentication, so you'll need to pass the proper username and password to it.

To illustrate the issue with the current approach, consider a Dockerfile with a snippet like this:

~~~
# Dockerfile (insecure method)
FROM base-image
COPY .netrc /app
# Other statements as per the app setup and run requirements
~~~

This approach copies the [`netrc`](https://everything.curl.dev/usingcurl/netrc) file with credentials into the image, making it vulnerable to exposure. Even if you remove the `netrc` file after copying it, the file won't actually get deleted from the image due to the layer caching techniques followed by Docker.

In this scenario, you need to implement a secure solution, which you can do using BuildKit's secrets handling feature. The following is a workflow diagram using BuildKit to handle secrets:

<div class="wide">
![Architecture diagram using BuildKit to handle secrets courtesy of Aniket Bhattacharyea]({{site.images}}{{page.slug}}/Addx8b8.png)
</div>

The "build machine" is the environment where the Docker image is built and where the BuildKit secrets handling process takes place. The build machine should have access to the API key files.

In this flow, you store the sensitive files required for communication with other services securely on the build machine. These keys need to be protected and not exposed in the final Docker image or source code.

The Dockerfile defines the instructions for building the Docker image. In this scenario, you have to modify it to include BuildKit secrets handling features to securely pass the secrets to the image.

The Docker BuildKit build process is responsible for constructing the Docker image. It securely retrieves the secrets from the build machine and makes them available to the Docker image during the build process, but doesn't store them in the final image (or, in any intermediate image). The resulting Docker image is securely embedded with the secrets during the build process. The secrets are not exposed in the final image, making it safe for deployment.

### Preparation

To follow along with this tutorial, you'll need:

* [Go](https://go.dev) installed and set up, to emulate the remote server.
* [Ngrok](https://ngrok.com/) to make it easy to expose the local server to the Docker build process.

To start, you need to create a project directory named `handling-secrets-with-docker-buildkit` and create a `main.go` file with the following code:

~~~
  package main
 
  import (
      "fmt"
      "log"
      "net/http"
      "crypto/sha256"
      "crypto/subtle"
      )
 
  func handler(w http.ResponseWriter, r *http.Request) {
      username, password, ok := r.BasicAuth()
          if ok {
              usernameHash := sha256.Sum256([]byte(username))
              passwordHash := sha256.Sum256([]byte(password))
              expectedUsernameHash := sha256.Sum256([]byte("admin"))
              expectedPasswordHash := sha256.Sum256([]byte("password"))
 
              usernameMatch := (subtle.ConstantTimeCompare(usernameHash[:], expectedUsernameHash[:]) == 1)
              passwordMatch := (subtle.ConstantTimeCompare(passwordHash[:], expectedPasswordHash[:]) == 1)
              
              fmt.Println(username, password)
              if usernameMatch && passwordMatch {
                  fmt.Fprintf(w, "Hello, Admin")
                  return
              }
          }
 
      fmt.Fprintf(w, "Hello, guest")
  }
 
  func main() {
      http.HandleFunc("/", handler)
      log.Fatal(http.ListenAndServe(":8080", nil))
  }
~~~

This code sets up a Go server with basic authentication. If you use the username `admin` and password `password`, it responds with `Hello, Admin`. Otherwise, it returns `Hello, guest`.

Run this server with `go run main.go`.

Then, in another terminal, run ngrok:

~~~
ngrok http 8080
~~~

> Please make note of the URL generated by Ngrok.

In the same folder, create a file named `netrc` with the following content:

~~~
 machine <Ngrok-Hostname>
 login admin
 password password
~~~

Replace `<Ngrok-Hostname>` with the hostname of the URL generated by Ngrok.

Test out the server by running the following command:

~~~
curl -n --netrc-file ./netrc <YOUR_NGROK_URL>
~~~

You should get the output `Hello, Admin`.

Omitting the credentials will return `Hello, guest`:

~~~
$ curl <YOUR_NGROK_URL>
Hello, guest
~~~

Your goal is to pass the credentials in the `netrc` file to the Docker build process without exposing it in the final image.

### Prepare a Simple Python App

Next, you need to create a `main.py` file and paste the following code into it:

~~~
  with open('message.txt', 'r') as f:
      print(f.readline())
~~~

This file opens the `message.txt` file and prints its contents. The `message.txt` file is populated using the output of the server prepared in the previous step.

### Enable Docker BuildKit Secrets

Ensure that Docker BuildKit is enabled by setting the `DOCKER_BUILDKIT` environment variable. If you're using a Linux-based operating system, you can set this environment variable with the following command:

~~~
export DOCKER_BUILDKIT=1
~~~

If you're using a Windows-based operating system, use the following command:

~~~
set DOCKER_BUILDKIT=1
~~~

### Build Docker Image with Secrets Using `--secret`

To build a Docker image with secrets, create a Dockerfile in the project directory:

~~~
 # Use the official Python 3.9 image as the base image
 FROM python:3.9-slim
 
 # Create a directory for your application
 WORKDIR /
 
 RUN apt-get update && apt-get install curl -y

# Mount the secret and use it to make HTTP request
 RUN --mount=type=secret,id=netrc,target=/root/.netrc \
     curl -n <YOUR_NGROK_URL> > message.txt
     
 # Your application code and instructions can follow below
 # For example, install dependencies or copy your application files
 
 COPY main.py .
 
 CMD ["python", "main.py"]
~~~

Following is the most important part of this code:

~~~
RUN --mount=type=secret,id=netrc,target=/root/.netrc \
     curl -n <YOUR_NGROK_URL> > message.txt
~~~

This line mounts the secret with the ID `netrc` to `/root/.netrc`. By passing the `-n` flag, you instruct `curl` to use credentials from the `netrc` file. (Note that, here the `--netrc-file` parameter is not needed because `/root/.netrc` is the default location where `curl` looks for this file.) The output of the request is then stored in the `message.txt` file. Using this syntax, the `netrc` file is not exposed in the final image, any intermediate image, or the image history.

Next, you need to build the Docker image, passing the secrets using the `--secret` flag:

~~~
docker build --secret id=netrc,src=./netrc -t my-app .
~~~

In this command, `--secret` is used to specify the secret to be passed, where `id=netrc` matches the defined identifier for the secret and `src=./netrc` is the path on the build machine to the secrets file.

Now you can run the container and ensure that you can see the `Hello, Admin` message:

~~~
$ docker run my-app
Hello, Admin
~~~

### Security Assurance

The credentials are now securely passed to the Docker image during the build process and are not exposed in the Dockerfile. You're not passing the hard-coded value of the credentials anywhere in the Dockerfile content coded earlier or the final image.

To check verify the security of your application, open a shell on the container with the following command:

~~~
docker run -it my-app /bin/sh
~~~

If you try to read the `netrc` file, you'll get an error message:

~~~
# cat /root/.netrc
cat: /root/.netrc: No such file or directory
~~~

This proves that using the `--secret` flag with Docker BuildKit provides a secure way to pass secrets during the build process, and the secrets remain hidden from the Dockerfile, build cache, and final image.

## Conclusion

In this tutorial, you learned how to securely manage and embed secrets during the Docker image build process with BuildKit, ensuring that these valuable secrets remain concealed.

As you wrap up your exploration of BuildKit, it's essential to emphasize how important secrets management is in the modern software landscape. If you use BuildKit as your ally, you'll not only enhance security but also embrace the principles of efficiency and best practices in handling sensitive data.

All the source code for this tutorial can be found in [this GitHub repository](https://github.com/heraldofsolace/docker-buildkit-secrets).

## Outside Article Checklist

* [ ] Create header image in Canva

* [ ] Add keywords for internal links to front-matter
* [ ] Run `link-opp` and find 1-5 places to incorporate links
* [ ] Add Earthly `CTA` at bottom `{% include_html cta/bottom-cta.html %}`
