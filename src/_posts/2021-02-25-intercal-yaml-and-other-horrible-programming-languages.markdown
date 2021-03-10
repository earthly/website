---
layout: post
title: INTERCAL, YAML, And Other Horrible Programming Languages
date: '2021-02-25 13:00:00'
---

## PROGRAM REJECTED FOR MENTAL HEALTH REASONS

In 1972, two students learning FORTRAN came up with a fantastic new programming language called INTERCAL. INTERCAL is a bit unusual. For example, single quotes are called _sparks_, and double quotes are called _rabbit ears_, less than (\<) is an _angle_, and a dash (-) is a _worm_. This makes the manual read like a word puzzle combined with an extended in-joke:

> One final comment about sparks and rabbit-ears; if the next character in the program is a spot, as often happens because onespot variables are common choices for operands, a spark and the following spot can be combined into a wow (!). - [INTERCAL Manual](http://www.catb.org/~esr/intercal/ick.htm).

The compiler errors are where the authors got genuinely creative. Errors include `VARIABLES MAY NOT BE STORED IN WEST HYPERSPACE` for accessing an array incorrectly, `IT CAME FROM BEYOND SPACE` for invalid control flow, `PROGRAM REJECTED FOR MENTAL HEALTH REASONS` for threading issues, `I HAVE NO FILE AND I MUST SCREAM` for file not found, and [many many more](http://www.catb.org/~esr/intercal/ick.htm#Errors).

Yes, this is a parody language, and reading the manual, you get the sense that no one has yet had as much fun writing technical documentation as Lyon and Woods did writing this.

The language itself looks less fun. Here is [Hello World](http://www.rosettacode.org/wiki/Category:Intercal):

           NOTE THIS IS INTERCAL
           PLEASE ,1 <- #5
           DO ,1 SUB #1 <- #54
           DO ,1 SUB #2 <- #192
           DO ,1 SUB #3 <- #136
           PLEASE ,1 SUB #4 <- #208
           DO ,1 SUB #5 <- #98
           DO COME FROM (1)
           DO READ OUT ,1
    (2) DO ,1 SUB #1 <- #134
    (1) PLEASE ABSTAIN FROM (2)

One of the exciting innovations of INTERCAL is the `COMEFROM` [instruction](https://en.wikipedia.org/wiki/COMEFROM#Examples), seen here in a variant of BASIC.<sup class="footnote-ref"><a href="#fn1" id="fnref1">[1]</a></sup>

    10 COMEFROM 40
    20 INPUT "WHAT IS YOUR NAME? "; A$
    30 PRINT "HELLO, "; A$
    40 REM

A `COMEFROM` anywhere in a program can grab control flow from the line you are reading. And in some implementations, if many `COMEFROM`'s reference the same line, execution splits off in each direction.

A `COMEFROM` is the inverse of a `GOTO` statement with multi-threading thrown in. It breaks the mental model of imperative execution where each line's evaluation leads to the next line. The idea that you can simulate its execution in your head, line by line, is fundamental to imperative programming and `COMEFROM` attempts to break that model.

## VARIABLES MAY NOT BE STORED IN WEST HYPERSPACE

At Twitter, they have a giant monorepo with lots of services in it. And somebody at Twitter wanted to know which language was most prevalent. Which language does Twitter use the most?

Java came in 3rd, and Scala came in 2nd. But 1st was a surprise. The number one programming language used at Twitter was YAML.<sup class="footnote-ref"><a href="#fn2" id="fnref2">[2]</a></sup>

YAML usually doesn't feel like a programming language to me. The file I'm currently writing in is in markdown with some YAML at the top to set the title and associated fields:

    title: INTERCAL, YAML, And Other Horrible Programming Languages
    author: Adam

Nothing executes this YAML. It only offers some information to the blogging platform. But I don't think that is the type of YAML that made up the bulk of config at Twitter.

I suspect a lot of it was build and deployment scripts in the form of YAML. It was the type of configuration that encoded the control flow of some external system. YAML like that lives in this grey zone between declarative configuration and a full-blown programming language.

I'll show you what I mean. Let's look at an example from [shellcheck](https://github.com/koalaman/shellcheck/blob/master/.travis.yml)'s build script:

    language: shell
    os: linux
    
    services:
      - docker

That seems like straight-forward config.

    jobs:
      include:
        - stage: Build
          env: BUILD=linux
          workspaces:
            create:
              name: ws-linux
              paths: deploy

`create`, in the above, is starting to seem a bit more like execution. Let's continue.

          script:
            - ls -la ${CASHER_DIR}/ || true
            - tar -xvf ${CASHER_DIR}/ws-osx-fetch.tgz --strip-components=5
            - ls -la deploy
            - ./.github_deploy

Now the YAML has just devolved into specifying how to execute a grab bag of commands. We haven't seen control-flow yet, but it's coming.

          if: type = push
          script:
            - source ./.multi_arch_docker
            - set -ex; multi_arch_docker::main; set +x

There we go, branching. It's an if statement in a YAML file!

That was for TravisCI but this isn't TravisCI, or CI specific. Here is a simple example from Ansible:

    - hosts: all
      tasks:
        - include: foo.yml
          when: something == "foo"
        
        - include: bar.yml
          when: something == "bar"

Here is GitHub Actions:

    steps:
     - name: Step 7
       if: ${{ github.event_name == 'pull_request' && github.event.action == 'unassigned' }}
       run: echo This event is a pull request that had an assignee removed.

Here is part of a Grafana [Helm Chart](https://github.com/grafana/helm-charts/blob/main/charts/grafana/templates/deployment.yaml):

    
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

I think this is a problem. Writing control flow in a config file is like hammering in a screw. It's a useful tool being used for the wrong job<sup class="footnote-ref"><a href="#fn3" id="fnref3">[3]</a></sup>.

How did we get to this world of little programming languages embedded into YAML? Is calling something configuration just less scary? And if so, is a c++ program just config you give to gcc?

Did things ever get this complicated in XML times?

It turns out they did:

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

That is `FizzBuzz` in [XSLT](https://gist.github.com/JustinPealing/6f619a23729720a9c14d9917201028c8). I assume it was written in jest, but in many ways, XML and XSLT are better than an ad-hoc YAML based scripting language. XSLT is a documented and standardized thing, not just some ad-hoc format for specifying execution.

It burns my eyes to look at it, but at least XSLT was intended to be used as a programming language. That is something we can't say about YAML or INTERCAL.

The problem with these languages embedded into YAML is they are all one-off implementations. TravisCI conditionals have a TravisCI specific syntax, usage, and features. You can't use Travis's `concat` function or conditional regex in the YAML configuration for your ansible playbooks.

In a vague way, this YAML problem is like the `COMEFROM` problem. If you know yaml, you can't just open a .yml file and start reading file line by line. You need to understand how the configuration controls the execution of the specific system it's for. And that is hard.

## I HAVE NO FILE AND I MUST SCREAM

The line between configuration and programming languages is not some bright dividing line. It's easy to slowly drift into adding programming language constructs to a config file. Before you know it, you have a full unspecified programming language embedded in the interpretation of your config file.

That is the worst of both worlds, and so much YAML seems to drift into this area.

I like YAML more than XML, but for control flow, you know what would be better than YAML? Anything else! Maybe even INTERCAL? I mean, how bad could a joke programming language be?

    (100) PLEASE NOTE THIS IS THE FIZZBUZZ FUNCTION	
    
    	PLEASE NOTE: IS THE INPUT DIVISIBLE BY #15?
    	DO .1 <- .100	
    	DO .2 <- #15
    	DO (2030) NEXT
    	PLEASE NOTE: is .4 (remainder) == 0?
    	DO .4 <- '?"'.4~.4'~#1"$#1'~#3
    	DO (130) NEXT
    	
    	PLEASE NOTE NUMBER IS NOT DIVISIBLE BY #15 => CHECK IF DIVISIBLE BY #3
    	DO .2 <- #3
    	DO (2030) NEXT
    	PLEASE NOTE: is .4 (remainder) == 0?
    	DO .4 <- '?"'.4~.4'~#1"$#1'~#3
    	DO (110) NEXT
    
    	PLEASE NOTE NUMBER IS NOT DIVISIBLE BY #3 => CHECK IF DIVISIBLE BY #5
    	DO .2 <- #5
    	DO (2030) NEXT
    	PLEASE NOTE: is .4 (remainder) == 0?
    	DO .4 <- '?"'.4~.4'~#1"$#1'~#3
    	DO (120) NEXT
    	
    	PLEASE NOTE NUMBER IS REGULAR => RETURN THE INPUT
    	DO .101 <- .100
    	DO (199) NEXT
    
    (110)	DO (111) NEXT
    	DO FORGET #1
    	PLEASE NOTE NUMBER IS DIVISIBLE BY #3 => RETURN FIZZ
    	DO .101 <- #61440
    	DO (199) NEXT
    
    
    (120)	DO (111) NEXT
    	DO FORGET #1
    	PLEASE NOTE NUMBER IS DIVISIBLE BY #5 => RETURN BUZZ
    	DO .101 <- #45056
    	DO (199) NEXT
    
    (130)	DO (111) NEXT
    	DO FORGET #1
    	PLEASE NOTE NUMBER IS DIVISIBLE BY #15 => RETURN FIZZ-BUZZ
    	DO .101 <- #64256
    	DO (199) NEXT
    
    (111)	DO RESUME .4
    	
    (199)	DO FORGET #1
    	DO RESUME #1

Oh God.

Well, ok, maybe not INTERCAL but anything else. <sup class="footnote-ref"><a href="#fn4" id="fnref4">[4]</a></sup><sup class="footnote-ref"><a href="#fn5" id="fnref5">[5]</a></sup>

* * *
<section class="footnotes">
<ol class="footnotes-list">
<li id="fn1" class="footnote-item">
<p><code>COME FROM</code> was introduced in INTERCAL-90 and not part of the orginal implementation (INTERCAL-72). <code>I HAVE NO FILE AND I MUST SCREAM</code> was also introduced in INTERCAL-90. <a href="#fnref1" class="footnote-backref">↩︎</a></p>
</li>
<li id="fn2" class="footnote-item">
<p>See my interview with <a href="https://www.se-radio.net/2019/08/episode-375-gabriel-gonzalez-on-configuration/">Gabriel Gonzalez on Configuration</a> at Software Engineering Radio. <a href="#fnref2" class="footnote-backref">↩︎</a></p>
</li>
<li id="fn3" class="footnote-item">
<p>Ansible and Helm use templating languages built on top of YAML, which is better than embedded control flow, but I think the point still stands. <a href="#fnref3" class="footnote-backref">↩︎</a></p>
</li>
<li id="fn4" class="footnote-item">
<p>Practically, you may have to use tools that encode a DSL into config, but you can use them while recognizing that we can do better. I think something like <a href="https://dhall-lang.org/#">Dhall</a> for complicated config and something like <a href="https://www.pulumi.com/">pulumi</a> for complex configuration as code should be where we aim for as an industry. <a href="#fnref4" class="footnote-backref">↩︎</a></p>
</li>
<li id="fn5" class="footnote-item">
<p>The fizzbuzz example listed in this example is now part the <a href="https://gitlab.com/esr/intercal/-/commit/660c3e92245dd58ff43ccf02c0d496c2084cf599">INTERCAL source</a> as is <a href="https://gitlab.com/esr/intercal/-/commit/3bce7df74dde7642757cc843275c3ae3370b489e">quine</a>, that Reddit user Frederic Stark wrote and shared with me on Reddit. <a href="#fnref5" class="footnote-backref">↩︎</a></p>
</li>
</ol>
</section><!--kg-card-end: markdown-->