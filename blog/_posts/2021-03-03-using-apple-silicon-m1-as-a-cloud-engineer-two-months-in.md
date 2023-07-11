---
title: Using Apple Silicon (M1) as a cloud engineer, two months in
featured: true
categories:
  - Articles
tags:
- docker
- apple-silicon
- m1
- arm64
- aarch64
author: Vlad
last_modified_at: 2023-04-17
internal-links:
  - m1
  - arm
excerpt: In this article, Vlad shares his experience using the Apple M1 as a cloud engineer. He discusses the compatibility of various software, including Docker and VS Code, and provides insights on performance, battery life, and cost. If you're curious about using Apple Silicon as a cloud engineer, this article offers valuable insights and recommendations.
---
**We're [Earthly.dev](https://earthly.dev/). We make building software simpler and therefore faster – like Dockerfile and Makefile had a baby. In this article, Vlad reviews the Apple M1 as a cloud engineer.**

So I've been using my new M1-based MacBook Pro for a couple of months for a mix of development, email, and other things an [open-source maintainer](https://github.com/earthly/earthly) does day-to-day.

The typical first reaction that you get when using this is "it runs my Docker stack without sounding like a plane taking off??".

It's a pretty amazing piece of engineering, and in many ways, I think that the ARM architecture is the future. A number of fast-growing tech giants (besides Apple) are pouring a ton of money into making ARM work for a ton of use-cases: Nvidia (trying to [buy ARM Holdings from SoftBank](https://www.cnbc.com/2020/09/14/nvidia-to-buy-arm-holdings-from-softbank-for-40-billion.html)) and Amazon (deep investment in the new [Graviton processors](https://aws.amazon.com/ec2/graviton/)) are the two that primarily come to mind.

As you might know, in processors low energy consumption (and low heat dissipation) often equates to the ability to scale processing efficiently for large workloads. It also means longer battery cycles for non-cloud use-cases (less waste, more bang for the buck). This is why I think ARM is the future, even if it might take a decade for the mainstream cloud to migrate over.

My Xeon Linux-based workstation suddenly feels old.

## Compatibility

All the software I need to use "just works". I found that if an ARM-native version is not available for an application, the emulated one works just fine and there's no performance drawback that I can notice. To emulate an application, you just need to install Rosetta 2. The OS will automatically detect that Rosetta is needed and prompt you to install it. However, you can also install it manually via

```
/usr/sbin/softwareupdate --install-rosetta
```

The tools you use for development are likely still catching up to this architectural change, and will be for some time. We engineers sometimes use very low-level system capabilities. In some cases, I had to install preview editions of software, but everything worked very well for me. Here are some programs that I've tested:

* ✅ Chrome (native)
* ✅ 1Password (emulated)
* ✅ Zoom (native)
* ✅ Backblaze (emulated)
* ✅ Signal (emulated)
* ✅ Spotify (emulated)
* ✅ VS Code. The amd64 version works perfectly well, however, the terminal will be an amd64 process, which may cause some programs to also run as amd64. The arm64 native version is available on the [VS Code Insiders](https://code.visualstudio.com/insiders/) and works really well.
* ✅ Docker. M1 native version is a must. Emulation doesn't have virtualization features, which the Docker app requires. You can download the [Docker App for M1](https://docs.docker.com/docker-for-mac/apple-m1/), which is in preview. As mentioned on the documentation page, there are some limitations currently related to HTTP proxy, VPN clients, and performance, but the Docker team is making progress fast. (A month or two ago [Kubernetes](/blog/building-on-kubernetes-ingress) wasn't working, but now it is!).
* ✅ Brew (native, encountered some issues with git, but was able to fix them)
* ✅ iTerm (native)
* ✅ Earthly (`v0.5.1+` now supports M1 natively - just `brew install earthly`)

I should also mention that during the first few weeks I had some issues with audio skips when using Bluetooth, but an OS update fixed it (just like [Apple promised](https://www.imore.com/fix-way-m1-mac-bluetooth-problems)).

I also use a ✅ YubiKey 5C Nano and a bunch of random peripherals like a ✅ USB microphone and a ✅ dock plugged into Ethernet.

Languages and frameworks I've tested - most of them in Docker containers:

* ✅ Go. [1.16 RC adds support for building darwin/arm64 binaries](https://golang.org/doc/go1.16#darwin). I built binaries in Docker and ran them natively. Works great.
* 🟡 Java and [Scala](/blog/top-5-scala-blogs). I had issues with the JVM, experiencing random process hangs. It seems that there are no official OpenJDK builds for aarch64, however there are some community options. See more info below.
* ✅ C++ works fine on native architecture in Docker. Minimal testing though.
* 🟡 .Net works fine when emulated as amd64 in a container. Did not immediately work natively (and I did not investigate).
* ✅ [Elixir](/blog/real-time-phoenix-elixir) works fine on native architecture in Docker. Minimal testing though.
* ✅ [gRPC](/blog/protobufs-and-grpc)  works fine on native architecture in Docker. Minimal testing though.
* ✅ JavaScript / Node works fine on native architecture in Docker. Minimal testing though.
* ✅ Python works fine on native architecture in Docker. Minimal testing though.
* ✅ Ruby and Ruby on Rails works fine on native architecture in Docker. Minimal testing though.
* ✅ Cobol (yes, really) works fine on native architecture in Docker. Minimal testing though.
* ✅ Rust works fine on native architecture in Docker. Minimal testing though.

## How to Tell What Architecture a Program Is Running As

It's extremely easy to mistake the kind of architecture you run as. Rosetta 2 is that good.

The easiest way to tell the difference is by opening Activity Monitor and looking at the Architecture column: if it says `Apple`, it's ARM. If it says `Intel`, it's X86_64. Here's how I can tell that Zoom is an ARM process, while Spotify is an X86_64 process.

![Activity Monitor showing Zoom as an Apple process]({{site.images}}{{page.slug}}/img1.png)

![Activity Monitor showing Spotify as an Intel process]({{site.images}}{{page.slug}}/img2.png)

If you're not sure about the terminal you're using, you can type `uname -m`. It'll say either `X86_64`, `arm64` (Mac) or `aarch64` (Linux). `arm64` and `aarch64` are both ARM - `uname` on Mac just reports it differently compared to Linux.

![Terminal showing the output of `uname -m` as `arm64`]({{site.images}}{{page.slug}}/img3.png)

## Brew Issues

One issue I encountered on both my M1 laptop and also a [MacStadium MacMini](https://www.macstadium.com/m1-mini) instance that we use for Mac testing is that Brew randomly started to complain about git missing. Not sure what the cause of this is, but it could be the fact that brew has been adding native arm support for many packages in the last few months and it's possible that this migration resulted in some inconsistencies. This is pure speculation, however, I've not researched this.

(In any case, a very impressive effort to switch architecture so quickly for a project that hosts so many packages!)

Back to fixing the issue now. Using `brew doctor` I was able to find out that Xcode needed a (re)install. Easy: `xcode-select --install`. However, the issue was still there. On the MacStadium instance, I was able to just uninstall brew and reinstall it and everything was fine. I was not as comfortable doing that on my laptop after having installed so much via casks. Instead, I was able to just remove the brew `git` via `brew uninstall git` and simply rely on `git` from Xcode, which seems to work just fine. (If anyone reading this knows what's up with my brew's git and can tell me how to fix it, ping me on Twitter: [`@vladaionescu`](https://twitter.com/VladAIonescu) )

## Using Docker

The Docker preview worked almost flawlessly for me from day 1. Making use of multi-platform images seems daunting at first, but really it's actually pretty simple.

<!-- vale HouseStyle.Spelling = NO -->

The Docker for Mac app comes packed with [QEMU](https://www.qemu.org/) out of the box - so Docker is able to run either arm64 and amd64 images. Most official images are now supported on arm64 too. If you're building an image, by default it'll use your native architecture to execute the build (arm64) and most things will magically just work. Your mileage may vary, however, if you are `curl`ing some binary that may need to switch from `X86_64` to `aarch64` in its URL, or if you're doing lower-level stuff. I also noticed that some alpine packages are also not available for ARM (for example `shellcheck`).

To build an image for a different architecture, you can use `docker buildx build --platform=linux/amd64 .` instead of the usual `docker build .`. For more details on building multi-platform images see [Akihiro Suda's blog](https://medium.com/nttlabs/buildx-multiarch-2c6c2df00ca2).

If you `docker pull` an image from the registry, it will again default to your native architecture (if available), unless you specify `--platform=linux/amd64`.

If you `docker run` an image, it will default to whatever version of the image you have available locally or it will attempt to pull the arm64 version from the registry. You can also override the platform via `--platform=linux/amd64` if you'd like to run the amd64 version specifically.

![Terminal showing the output of `uname -m` for different container platforms]({{site.images}}{{page.slug}}/img4.png)

[Docker Compose](/blog/youre-using-docker-compose-wrong) will happily run a mixture of various architectures. The same rules apply with regards to pulling and running. You can also specify `platform: linux/amd64` for the service definition in `docker-compose.yml` if you'd like to be specific.

One thing to note is that Docker-in-Docker is not supported by QEMU ([abandoned PR on GitHub](https://github.com/moby/qemu/pull/7)). So you cannot run an arm64 Docker in an amd64 Docker or vice-versa. **However**, if you run your natively-supported Docker-in-Docker, the inner Docker can still run multi-platform images fine.

There are currently performance issues with multi-processor use - so much so that performance using a single core is sometimes slightly better than the performance of using 8 cores. Or at least that's what [@jasmas claims](https://github.com/docker/roadmap/issues/142#issuecomment-772732443).

## Using VS Code

Native support for Apple Silicon is not yet available in the generally available VS Code version, but running the amd64 emulated version works pretty well. You can also use the native version via a VS Code Universal build (contains both architectures in a single package) available via [VS Code Insiders](https://code.visualstudio.com/insiders/#osx).

An issue I ran into with the amd64 version was that I did not realize that the terminal was also an amd64 process (Again, Rosetta 2 is just that good). In some situations, this led to some strange issues when running Docker, where QEMU was acting up with segmentation faults. After some head-scratching the issue was resolved by switching to the ARM-based VS Code Insiders edition.

## Using Earthly

We've added support for Apple M1 in Earthly and so far it's working wonderfully. This is in Beta, so if you end up giving this a try - we'd appreciate any feedback you can give us via [GitHub issues](https://github.com/earthly/earthly/issues) or in our [Slack](https://earthly.dev/slack).

One useful Earthly trick I've used a lot is that if one part of your build has not yet been ported to amd64, you can simply mark it as `--platform=linux/amd64` - and thus only that part will execute on amd64. The rest will run natively. This is relatively rare, however - most Docker builds just work across either platform. Our [examples build](https://github.com/earthly/earthly/blob/b7b640094f8b5a0982eca5376cb54147feac7878/Earthfile#L295-L321) is pretty representative. There's also an extensive guide on [multi-platform builds with Earthly](https://docs.earthly.dev/guides/multi-platform).

## Using Go

You don't necessarily need to build `darwin/arm64` binaries to run them on M1. Rosetta 2 emulation works great on Intel ones. If you want to, however, [Go 1.16 RC just added support for this](https://golang.org/doc/go1.16#darwin).

## Java / Scala / JVM Issues

I ran into issues when using the JVM. After investigating online, it seems that OpenJDK is not yet available for the M1. The way this was manifesting for me was that the JVM process would just hang randomly. By using `--platform=linux/amd64` in Docker or in Earthly builds, I was able to get OpenJDK to work most of the time, but I'm still seeing random hangs.

According to this [StackOverflow thread](https://stackoverflow.com/questions/64788005/java-jdk-for-apple-m1-chip), there are [Azul-provided builds of the Zulu JDK](https://www.azul.com/downloads/zulu-community/?package=jdk) for the M1 and also [Microsoft has put up an aarch64 build for the OpenJDK](https://github.com/microsoft/openjdk-aarch64/releases/tag/16-ea%2B10-macos) too. I have not tested these so I can't say whether they work well or not.

## Performance

One of the things I noticed about my new laptop is that everything opens up really fast and the awake from sleep time is also really low. These are sub-second differences though so you might not notice it - or maybe it's a placebo acting up on me and there's no real difference :-)

Docker is currently slower, however, as mentioned above, due to the multi-core issue. As far as I can tell the difference is approximately 1.75X compared to an Intel MacBook Pro. I would assume that this will be fixed in a future preview of the Docker for Mac app.

## Battery Life

<!-- vale HouseStyle.Repetition = NO -->
Battery life on the M1 is really really really good - half a day of Zoom meetings + email only took 20% of my battery. I work from home a lot, so I don't use this much. But it's great to know it really lasts for a serious coding session if I needed it on the go.
<!-- vale HouseStyle.Repetition = YES -->

## Cost

I can't talk about the M1 without mentioning the cost of the setup. It has very similar specs to the Intel MBP I bought last year, but it's a whole $1000 cheaper. It's crazy. I don't know why - it feels really performant for the most part, it has 100% fewer fans and a long-lasting battery. Why would anyone buy the old version anymore?

The only downside is that it only has two Thunderbolt ports, rather than four. But it's not a huge deal for me as I use a dock.

I think the strategy here is that this will be the low-end MacBook Pro of the line-up, while a future Apple Silicon-based one will have even beefier specs.

## Conclusion

As you can see, my workflow is very much Docker-heavy. Docker seems to be working well enough for me and it's taken away any possible pain that may be associated with individual language ecosystem tooling.

For most binaries, if they don't work across platforms natively, Rosetta 2 works wonders on them, or `--platform=linux/amd64` in Docker is all that is needed. The JVM issues were the only ones I could not figure out completely - but also, I did not spend time trying out the Microsoft-provided OpenJDK build or the Zulu JVM.

Overall I'm happy with my M1. I like bleeding-edge technology, and I had to use preview versions of some software, but had no major issues in my typical workflow. I'm surprised how well most things just work.

If you're a developer and your coding productivity depends on your laptop, I would triple check that my setup works as expected on an ARM architecture before making a purchase. For the most part you should be fine outside the Java / Scala world - but you never know!

If you're not a developer, or only use your laptop for browsing and email, I really don't see any reason why you would pick an Intel MacBook over this one. I would also assume that the MacBook Air version is also amazing (unlike the Intel version of MacBook Air, which is often on the slow side for modern web browsing). The M1 chip is very similar between Pro and Air and there's no need for fans.

And if you liked this article you might like to hear a little about the [backstory behind](/blog/introducing-earthly-build-automation-for-the-container-era) [Earthly](https://earthly.dev/).

{% include_html cta/bottom-cta.html %}
