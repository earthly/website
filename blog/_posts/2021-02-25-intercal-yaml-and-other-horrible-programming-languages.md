---
title: INTERCAL, YAML, And Other Horrible Programming Languages
categories:
  - Articles
featured: true
author: Adam
sidebar:
  nav: "thoughts"
excerpt: |
    Discover the bizarre world of INTERCAL, a parody programming language that will leave you scratching your head. Then, delve into the blurred line between configuration and programming languages, and why YAML might not be the best choice for control flow.
internal-links:
  - intercal
---
**We're [Earthly](https://earthly.dev/). We simplify and speed up software building with containerization. Earthly helps you avoid YAML hell. [Check it out](/).**

## PROGRAM REJECTED FOR MENTAL HEALTH REASONS

In 1972, two students learning FORTRAN came up with a fantastic new programming language called INTERCAL. INTERCAL is a bit unusual. For example, single quotes are called *sparks*, and double quotes are called *rabbit ears*, less than (<) is an *angle*, and a dash (-) is a *worm*. This makes the manual read like a word puzzle combined with an extended in-joke.

> One final comment about sparks and rabbit-ears; if the next character in the program is a spot, as often happens because onespot variables are common choices for operands, a spark and the following spot can be combined into a wow (!). - [INTERCAL Manual](http://www.catb.org/~esr/intercal/ick.htm).

<!-- vale HouseStyle.Repetition = NO -->
The compiler errors are where the authors got genuinely creative. Errors include `VARIABLES MAY NOT BE STORED IN WEST HYPERSPACE` for accessing an array incorrectly, `IT CAME FROM BEYOND SPACE` for invalid control flow, `PROGRAM REJECTED FOR MENTAL HEALTH REASONS` for threading issues, `I HAVE NO FILE AND I MUST SCREAM` for file not found, and [many many more](http://www.catb.org/~esr/intercal/ick.htm#Errors).
<!-- vale HouseStyle.Repetition = YES -->

Yes, this is a parody language, and reading the manual, you get the sense that no one has yet had as much fun writing technical documentation as Lyon and Woods did writing this.

The language itself looks less fun. Here is [Hello World](http://www.rosettacode.org/wiki/Category:Intercal):

``` fortran
       NOTE THIS IS INTERCAL
       PLEASE ,1 <- #5
       DO ,1 SUB #1 <- #54
       DO ,1 SUB #2 <- #192
       DO ,1 SUB #3 <- #136
       PLEASE ,1 SUB #4 <- #208
       DO ,1 SUB #5 <- #98
       DO COME FROM (1)
       DO READ OUT ,1
(2)    DO ,1 SUB #1 <- #134
(1)    PLEASE ABSTAIN FROM (2)
```

One of the exciting innovations of INTERCAL is the `COMEFROM` [instruction](https://en.wikipedia.org/wiki/COMEFROM#Examples), seen here in a variant of BASIC.  

``` qwbasic
10 COMEFROM 40
20 INPUT "WHAT IS YOUR NAME? "; A$
30 PRINT "HELLO, "; A$
40 REM
```

 A `COMEFROM` anywhere in a program can grab control flow from the line you are reading. And in some implementations, if many `COMEFROM`'s reference the same line, execution splits off in each direction.  

 A `COMEFROM` is the inverse of a `GOTO` statement with multi-threading thrown in. It breaks the mental model of imperative execution where each line's evaluation leads to the next line. The idea that you can simulate its execution in your head, line by line, is fundamental to imperative programming and `COMEFROM` attempts to break that model.

## VARIABLES MAY NOT BE STORED IN WEST HYPERSPACE

At Twitter, they have a giant [monorepo](/blog/monorepo-vs-polyrepo) with lots of services in it. And somebody at Twitter wanted to know which language was most prevalent. Which language does Twitter use the most?  

Java came in 3rd, and [Scala](/blog/top-5-scala-blogs) came in 2nd. But 1st was a surprise. The number one programming language used at Twitter was YAML[^1].

YAML usually doesn't feel like a programming language to me. The file I'm currently writing in is in markdown with some YAML at the top to set the title and associated fields.

``` yaml
title: INTERCAL, YAML, And Other Horrible Programming Languages
author: Adam
```

Nothing executes the YAML. It only offers some information to the blogging platform. But I don't think that is the type of YAML that made up the volume of config at Twitter.

I suspect a lot of it was build and deployment scripts in the form of YAML. It was the type of configuration that encoded the control flow of some external system. YAML like that lives in this grey zone between declarative configuration and a full-blown programming language.

I'll show you what I mean. Let's look at an example from [ShellCheck](https://github.com/koalaman/shellcheck/blob/bd3299edd3b517f92f74c2e3327c9f6b72b31f7c/.travis.yml)'s build script.

``` yaml
language: shell
os: linux

services:
  - docker
```

That seems like straight-forward config.

``` yaml
jobs:
  include:
    - stage: Build
      env: BUILD=linux
      workspaces:
        create:
          name: ws-linux
          paths: deploy
```

`create`, in the above, is starting to seem a bit more like execution. Let's continue.  

``` yaml
  {% raw %}
      script:
        - ls -la ${CASHER_DIR}/ || true
        - tar -xvf ${CASHER_DIR}/ws-osx-fetch.tgz --strip-components=5
        - ls -la deploy
        - ./.github_deploy
  {% endraw %}
```

Now the YAML has just devolved into specifying how to execute a grab bag of commands. We haven't seen control-flow yet, but it's coming.

``` yaml
      if: type = push
      script:
        - source ./.multi_arch_docker
        - set -ex; multi_arch_docker::main; set +x
```

There we go, branching. It's an if statement in a YAML file!

And this isn't [TravisCI](/blog/migrating-from-travis), or CI specific. Here is a simple example from Ansible:

``` yaml
- hosts: all
  tasks:
    - include: foo.yml
      when: something == "foo"
    
    - include: bar.yml
      when: something == "bar"
```

Here is GitHub Actions:

``` yaml
{% raw %}
steps:
 - name: Step 7
   if: ${{ github.event_name == 'pull_request' && github.event.action == 'unassigned' }}
   run: echo This event is a pull request that had an assignee removed.
{% endraw %}
```

Here is part of a Grafana [Helm Chart](https://github.com/grafana/helm-charts/blob/main/charts/grafana/templates/deployment.yaml):

``` liquid
  {% raw %}
  {{ if (or (not .Values.persistence.enabled) (eq .Values.persistence.type "pvc")) }}
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: {{ template "grafana.fullname" . }}
    namespace: {{ template "grafana.namespace" . }}
    labels:
      {{- include "grafana.labels" . | nindent 4 }}
  {{- if .Values.labels }}
  {{ toYaml .Values.labels | indent 4 }}
  {{- end }}
  {{- with .Values.annotations }}
    annotations:
  {{ toYaml . | indent 4 }}
  {{- end }}
  {% endraw %}
```

 I think this is a problem[^2]. Writing control flow in a config file is like hammering in a screw. It's a useful tool being used for the wrong job.

 How did we get to this world of little programming languages embedded into YAML? Is calling something configuration just less scary? And if so, is a c++ program just config you give to gcc?

Did things ever get this complicated in XML times?

It turns out they did:

``` xml
  {% raw %}
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  <xsl:output method="text" omit-xml-declaration="yes" />

  <xsl:template match="/">
    <xsl:call-template name="FizzBuzz">
      <xsl:with-param name="i" select="1" />
    </xsl:call-template>
  </xsl:template>

  <xsl:template name="FizzBuzz">
    <xsl:param name="i" />
    <xsl:choose>
      <xsl:when test="($i mod 3) = 0 and ($i mod 5) = 0">FizzBuzz&#xa;</xsl:when>
      <xsl:when test="$i mod 3 = 0">Fizz&#xa;</xsl:when>
      <xsl:when test="$i mod 5 = 0">Buzz&#xa;</xsl:when>
      <xsl:otherwise><xsl:value-of select="$i" /><xsl:text>&#xa;</xsl:text></xsl:otherwise>
    </xsl:choose>
    <xsl:if test="$i &lt; 100">
      <xsl:call-template name="FizzBuzz">
        <xsl:with-param name="i" select="$i + 1" />
      </xsl:call-template>
    </xsl:if>
  </xsl:template>
</xsl:stylesheet>
  {% endraw %}
```

That is `FizzBuzz` in [XSLT](https://gist.github.com/JustinPealing/6f619a23729720a9c14d9917201028c8). I assume it was written in jest, but in many ways, XML and XSLT are better than an ad-hoc YAML based scripting language. XSLT is a documented and standardized thing, not just some ad-hoc format for specifying execution.  

It burns my eyes to look at it, but at least XSLT was intended to be used as a programming language. That is something we can't say about YAML or INTERCAL.

The problem with these languages embedded into YAML is they are all one-off implementations. TravisCI conditionals have a TravisCI specific syntax, usage, and features. You can't use Travis's `concat` function or conditional regex in the YAML configuration for your Ansible playbooks.

In a vague way, this YAML problem is like the `COMEFROM` problem. If you know YAML, you can't just open a .yml file and start reading file line by line. You need to understand how the configuration controls the execution of the specific system it's for. And that is hard.

<!-- If it's `title: bla` that is easy enough, but once we hit conditionals and filters, it feels like we are using the wrong tool. -->

## I HAVE NO FILE AND I MUST SCREAM
<!--sgpt-->
The boundary between configuration and programming languages can blur easily, leading to complex config files that resemble programming languages. This isn't ideal and YAML often falls into this trap. While YAML beats XML, using it for control flow isn't the best. Anything, even joke languages like INTERCAL, could potentially be better. However, after seeing INTERCAL's FizzBuzz function, maybe we should reconsider that. So, perhaps not INTERCAL, but certainly something else. 

If you're tired of complex configs and odd languages, you might want to give [Earthly](https://www.earthly.dev/) a shot. It offers a clearer and more straightforward approach to build automation, which could be the breath of fresh air you need in your development process.

[^1]: See my interview with [Gabriel Gonzalez on Configuration](https://www.se-radio.net/2019/08/episode-375-gabriel-gonzalez-on-configuration/) at Software Engineering Radio.
[^2]: Ansible and Helm are actually templating languages built on top of YAML, which is better than embedded control flow, but the point still stands.
[^3]: Practically, you may have to use tools that encode a DSL into config, but you can use them while recognizing that we can do better. I think something like [Dhall](https://dhall-lang.org/#) for complicated config and something like [Pulumi](https://www.pulumi.com/) for complex configuration as code should be where we aim for as an industry.