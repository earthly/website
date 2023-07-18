---
#header:
title: The 15-Minute Project
categories:
  - Articles
author: Corey
excerpt: |
    Discover how the principles of city planning can be applied to software projects, creating a more accessible and efficient development environment. Learn how concepts like zoning, building codes, transportation, equity, and taxes can improve collaboration and make your project a desirable place for contributors.
toc: true
internal-links:
  - planning
  - project-management
---
**We're [Earthly](https://earthly.dev/). We simplify software builds using containers, making your software projects more streamlined and efficient - just like city planning. [Take a peek](/).**

Like many others, 2020 encouraged me to find some new interests and hobbies to fill the time spent at home. At risk of sounding terribly boring, one of my newfound interests is that of city planning.

## What Is City Planning?

According to Wikipedia, city planning is ["...a technical and political process that is focused on the development and design of land use and the built environment..."](https://en.wikipedia.org/wiki/Urban_planning). It includes basically everything, from air, and water to transportation and accessibility. Seems like a fairly broad and ill-specified discipline!

In a typical American city or town, there is a city planning board that controls development and design. They meet regularly, and in public at their city hall. During 2020, many of these meetings became much more accessible and easy to observe through video calls. It was very interesting to watch how this big, broad concept of "city planning" was boiled down to actual, concrete actions that affected my day-to-day life.

## The Built Environment

One phrase I kept hearing over and over in planning meetings, in videos on YouTube[^1], and other literature is that of the "built environment". Tuns out that the phrase "built environment" is actually a well defined, distinct concept! It even has [its own Wikipedia page, too](https://en.wikipedia.org/wiki/Built_environment)!

Simply put, the built environment is the stuff we've "built" around us; like roads, sidewalks, buildings, parks, and utilities. Feels tautological; but the built environment also encompasses *how* these things affect us in our day-to-day life.

The built environment is *why* some areas are more desirable than others, and *how* you can improve the lives of people within a city.

## Building A Built Environment

City planners are very concerned with designing the built environment within a city. To this end, they have many tools to guide development in a way that is (hopefully) beneficial and equitable to the community. Things like zoning, building codes, affordable housing, and traffic management can all influence the built environment in very consequential ways.

But, a planning commission can't design a built environment without a goal. Or, at least if they try, it won't create the kind of built environment that people want to live in. Cities need targets and goals to help them design the places that people want to make their home.

One model that I really like is that of the "[15 Minute City](https://www.cnu.org/publicsquare/2021/02/08/defining-15-minute-city)". Originally conceived in 2016, it has since become a global movement; with many cities around the world adopting variations of the concept into their future planning goals. The idea behind a 15-minute city is that *most* residents should be able to satisfy *most* of their needs within a 15 minute bike ride from their home. This promotes a well-mixed, accessible, and human scale to target when designing a built environment.

## What Does This Have To Do With Software Development?

At the risk of falling into the analogy trap, I think we can learn a lot by applying the "built environment" to our software projects. The code, tooling, and infrastructure we use constitutes the physical component, and the contributors working on the project are the citizens living within it.

After all, [the cathedral *and* the bazaar](http://www.catb.org/~esr/writings/cathedral-bazaar/cathedral-bazaar/index.html#catbmain) both have to exist *somewhere*.

## The 15-Minute Project?

Like cities may strive to become a "15-minute city", I propose that software projects should strive to be "15-minute projects". To become a 15-minute project, any blocked contributor should be able to find what they need to continue progressing within 15 minutes. Finding what you need could involve any piece of your project - the code, documentation, or the community.

Yes, software is *hard*. But so is city planning. Just as no city will achieve a "100% 15-minute city" goal, no software project will either. But, keeping this goal top of mind will do wonders for your project, and make it a desirable place for contributors to congregate.

## How Do We Get There?

Before we begin, I am well aware that city planners are not perfect; and that cities quite often make poor decisions. For this analogy, we are considering the platonic ideal of a city and of the planners within it. Frictionless cities with perfectly spherical planners, if you will.

From this, there are some lessons we can learn when applying city planning concepts to software projects. Below are a couple that I feel can really make a difference to the built environment within your project, and help inch closer to that 15-minute ideal.

### Zoning

While we can [argue about the necessity and efficacy of zoning](https://www.urban.org/debates/land-use-regulation-whats-it-worth-anyway) within a city plan, having a general plan for your software project can make life a lot easier. If you have a general idea of what will go where, eventually, you can make intelligent decisions about what gets built *now*. In a city, these plans are typically public, and can be viewed by everyone. So too should they be in a software project.

Just like software, requirements for cities also tend to drift (just on a longer timescale). To this end, general plans should also be revisited and re-approved on a regular basis.

### Building Codes

Just like new construction within a city is governed by a [building code](https://codes.iccsafe.org/content/IBC2021P1), so too should new contributions. Building codes typically get very verbose for safety reasons, but ours don't need to be quite that strict (well, unless your code actually *is* safety critical). Often, listing what tools and languages are to be used is sufficient. Most importantly, the building code for your software project should also be public and accessible.

You can take this even further and codify the languages and tools. One approach I have seen is to use tools like `eslint` on a Git commit hook to keep the code looking uniform, so things like formatting aren't even a question. (This is why the author loves Go, for instance.) Earthly is a great tool to help you codify all parts of your pipeline.

### Transportation

Getting people from place to place efficiently is a challenge that most cities face. Proper planning can help mitigate the inevitable traffic jam. Roads, public transit, and sidewalks are all part of the infrastructure that keeps a city moving.

Likewise, our choices in communication tools affect the transportation of ideas and contributions within a project. Different tools are appropriate for different projects, because they have different citizens. But, if your project's Slack channels and JIRA boards feel like rush hour in LA, then perhaps it is time to consider improvements.

### Equity

Cities and towns should be places for people from all walks of life, not just the "elites". One common way to accomplish this is by enforcing affordable housing in new developments, and by making sure general improvements are evenly distributed across the city.

Software projects, like cities, should try to improve the lives of all contributors, not just an insular group with the most control. Reserving "easy" issues for first time contributors, keeping documentation up to date, and making decisions in public can go a long way toward leveling the playing field for all contributors.

A project that is known for being clear, fair, and equitable will end up with a more vibrant community that can carry it far further than it could otherwise travel on its own. A rising tide lifts all boats.

### Taxes

Public infrastructure isn't free. Cities levy taxes, typically in the form of property taxes, to pay for installation and ongoing maintenance. If the city is responsible, the taxes aren't too onerous and the infrastructure isn't too extravagant.

In our software projects, there is also some form of "tax" to be paid for the shared infrastructure. The tax is paid in updating and maintaining shared resources, from build scripts, to CI/CD, to documentation.

By keeping this shared infrastructure well maintained and right-sized for the project, you can also keep your takes low and the benefits high.

## Conclusion

This analogy has been truly enlightening, showing how interconnected seemingly distinct domains can be. It's reshaped my approach to projects, and I hope it'll do the same for you. 

And if you're looking to bring the same level of efficiency to your code builds as you would to city planning, you might want to give [Earthly](https://www.earthly.dev/) a try.

{% include_html cta/bottom-cta.html %}

[^1]: You would be surprised at how many [beautiful](https://www.youtube.com/channel/UCGc8ZVCsrR3dAuhvUbkbToQ) [channels](https://www.youtube.com/channel/UC0intLFzLaudFG-xAvUEO-A) [there](https://www.youtube.com/channel/UCqdUXv9yQiIhspWPYgp8_XA) [are](https://www.youtube.com/user/strongtowns) in this space!
