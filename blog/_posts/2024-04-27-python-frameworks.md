---
title: "Top Python Frameworks for 2024"
toc: true
author: Jura Gorohovsky

internal-links:
 - python frameworks
 - top python frameworks
 - python frameworks in 2024
 - python frameworks to look at
excerpt: |
    This article provides an overview of the top Python web frameworks for 2024, including Django, Flask, and FastAPI. It discusses the features and use cases of each framework, as well as factors to consider when choosing a framework for your project.
categories:
  - python
---
**The article provides an overview of Python web frameworks. Earthly improves the efficiency of CI builds within your development lifecycle. [Learn more about Earthly](https://cloud.earthly.dev/login).**

If you're a professional Python web developer, you're likely aware of the robust and competitive nature of Python's web development ecosystem. If you've recently completed a web application project and are looking to evaluate the current state of Python web frameworks, you've come to the right place.

Whether you're developing full-stack web applications or API-only web backends, Python has options. In this article, you'll learn all about Python web frameworks and how they differ from libraries. You'll also take a look at some of the most popular frameworks and what they're typically used for.

> **Please note:** While Python is used in many different areas, this article only considers Python frameworks for web application development. There's also a powerful bunch of Python frameworks for data science, but they're a very distinct breed and will not be covered here.

## What Is a Python Framework?

Let's quickly recap what a framework is and how it's different from a library.

A library is something that you include in the dependencies of your script or application to take advantage of code that someone else previously wrote. You do this to perform a certain specialized task, such as format strings, encode or decode URLs, or deal with timestamps and time zones.

A library is somewhat disposable: you try a library, you don't like it, you remove it, you try something new.

A [web framework](https://www.fullstackpython.com/web-frameworks.html) is a more comprehensive tool that provides conventions, a structure, and APIs for building an entire application, as well as code and libraries to handle lower-level tasks. These lower-level tasks typically include capturing HTTP requests and handing them over to your code to handle, mapping requested URLs to functions in your application, and enabling middleware to apply additional processing of HTTP requests and responses. Some frameworks also include tools for working with data, such as object-relational mappers (ORMs), form generation and validation, and tools for authentication and authorization.

Here's a good way to distinguish libraries from frameworks:

* You plug a library into your application.
* You plug your application into a framework.

A framework comes with a more serious commitment than a library. Once you've chosen one, switching to another may be challenging.

Every Python web framework sits somewhere on a spectrum between [two extremes](https://www.reddit.com/r/Python/comments/26a0wr/comment/chp7a6m/):

* **Full frameworks** (a.k.a. "batteries included" frameworks) bundle the whole set of components involved in web development, such as a template engine, ORM, form validation, authentication, authorization, and administration. The developers of these frameworks make many decisions for you, leaving you to write code within the chosen path. These frameworks usually work best when you create functionally similar business applications.
* **Microframeworks** tend to only provide the core functionality, which is typically limited to HTTP request management and URL routing. They give developers the freedom to choose the other components of their web applications on their own. Popular microframeworks naturally come with a rich set of community extensions that enable you to plug in components of your choice.

## Top Python Frameworks

Recent surveys by [JetBrains](https://www.jetbrains.com/lp/devecosystem-2023/python/#python_web_libs_two_years) and [Stack Overflow](https://survey.stackoverflow.co/2023/#most-popular-technologies-webframe) indicate that there are three distinct leaders among Python frameworks in 2024: Django, Flask, and FastAPI. All other Python web frameworks don't come close to the market shares held by these three.

### Django

![Django]({{site.images}}{{page.slug}}/django.png)\

[Django](https://www.djangoproject.com/) is the most popular full-stack web framework in the Python ecosystem. First released in 2005, it's one of the oldest actively used Python web frameworks, boasting a 40 percent market share in 2023. When you want to use one framework to develop both the backend and the frontend of your application, Django is a natural choice.

Django is an archetypal full framework; it's feature-rich and tends to provide out-of-the-box tools for every step of the web application development process. These include object-relational mapping, templating, user management and authentication, form validation, caching, and even an admin panel. However, developers often call Django "opinionated," and it comes at a cost. Whenever you're not entirely happy with a component that comes with Django, replacing it with a third-party component can be challenging.

For someone who's just getting started with Django, the learning curve may be steep, but once you've learned it, you have a lot of tools at your disposal out of the box. Luckily, due to the long history and popularity of the framework, there's no shortage of Django professionals on the job market.

Django is backed by the [Django Software Foundation](https://www.djangoproject.com/foundation/) and has a lot of [active contributors](https://github.com/django/django/graphs/contributors), indicating that the framework is here to stay and will be maintained in the long run.

Django is a great choice if you work for a web development shop that creates a lot of similar server-side CRUD applications. It can also be a good fit for larger custom web applications with a relatively simple database schema that doesn't require high-end database performance.

However, if you want to have fine-grained control over the components you're using in your web applications, Django may not be the best fit. Additionally, building advanced database queries using the Django ORM [can be problematic](https://djangostars.com/blog/merging-django-orm-with-sqlalchemy-for-easier-data-analysis/).

### Flask

![Flask]({{site.images}}{{page.slug}}/flask.png)\

With a 38 percent market share, [Flask](https://palletsprojects.com/p/flask/) is just as popular as Django but sits on the opposite end of the framework spectrum. It's a small, minimalistic, extendable microframework that focuses on making it easy to get started.

Flask doesn't dictate the usage of particular libraries or a project layout; instead, it enables developers to choose their favorite plugins for object-relational mapping, form validation, caching, and more web framework functions. Some of the most popular Flask extensions include [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/), [Flask-Caching](https://flask-caching.readthedocs.io/en/latest/), [Flask-Admin](https://github.com/flask-admin/flask-admin), [Flask-Login](https://flask-login.readthedocs.io/en/latest/), and [Flask-Security](https://flask-security-too.readthedocs.io/en/stable/).

Since Flask doesn't enforce specific components, it's one of the frameworks that is better suited for applications with complex database schemas and a lot of data aggregation. Flask enables you to easily plug in SQLAlchemy as an ORM, which is the top choice for such applications.

Flask is a good fit for developing APIs that serve separate frontends and for full-stack web application development if you plug in the [Jinja2 template engine](https://flask.palletsprojects.com/en/3.0.x/tutorial/templates/).

Developers [praise](https://www.reddit.com/r/Python/comments/tz2v7b/comment/i3yr8ty/) Flask for its clear, concise, and well-searchable [documentation](https://flask.palletsprojects.com/en/3.0.x/), which will probably save you valuable time when you get stuck. There's also an outstanding [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world) by Miguel Grinberg, which [many developers](https://www.reddit.com/r/Python/comments/tz2v7b/comment/i3wwr4n/) believe is a masterpiece in engineering education.

Flask is maintained by the [Pallets](https://palletsprojects.com/) team. Although not as deep a contributor base as the Django Software Foundation, it still has a healthy set of [active maintainers](https://github.com/pallets/flask/graphs/contributors).

### FastAPI

![FastAPI]({{site.images}}{{page.slug}}/fast.png)\

[FastAPI](https://fastapi.tiangolo.com/) is the youngest of the top three Python web frameworks. Established in 2018, it quickly rose to the top of the ranks and is now considered the go-to framework for building lightning-fast APIs. It's also one of the most admired frameworks. According to the latest [Stack Overflow Developer Survey](https://survey.stackoverflow.co/2023/#section-admired-and-desired-web-frameworks-and-technologies), 64.49 percent of developers who have tried FastAPI said they wanted to use it again.

FastAPI is consistently at or near the top of [performance benchmarks](https://www.techempower.com/benchmarks/#section=data-r22&hw=ph&test=composite&l=zijzen-cn3) among Python web frameworks.

FastAPI is designed to use Python type hints, which helps minimize errors early in development. It also supports asynchronous programming out of the box, making it a solid choice for real-time applications.

Another standout feature of FastAPI is automatic interactive API doc generation based on [Swagger UI](https://github.com/swagger-api/swagger-ui). Because FastAPI uses Python type hints, the generated documentation takes type restrictions into account. For example, if you test an endpoint with a value of the wrong type, you won't be able to make the request.

One notable risk associated with FastAPI is that it's created and still [mostly maintained](https://github.com/tiangolo/fastapi/graphs/contributors) by a single developer with no corporate or sponsor backing.

### Pyramid

![Pyramid]({{site.images}}{{page.slug}}/pyramid.png)\

First released in 2008, [Pyramid](https://trypyramid.com/) is an established Python framework that aims to be a good fit for web applications at every step of their lifecycle.

Pyramid is often valued for its flexibility. It's a convention-over-configuration framework with sensible defaults that developers can override if necessary. On the framework spectrum, it stands midway between the feature-rich but highly opinionated Django and the minimalistic but pluggable Flask.

Pyramid doesn't require a particular database, form library, or templating syntax. You can use Chameleon, Jinja2, and Mako for templates, SQLAlchemy or ZODB for data persistence, and libraries like Deform for generating forms. Pyramid also provides ways to set up unit and functional tests as part of its commitment to high test coverage. All these choices can be made when you use Pyramid's scaffolding tool to guide you through creating a project with your preferred components.

One obvious drawback of Pyramid is its usage: according to the [JetBrains State of Developer Ecosystem in 2023 report](https://www.jetbrains.com/lp/devecosystem-2023/python/), it's only used by 2 percent of Python developers. Lower usage usually means fewer Q&As that you can Google, longer wait times for community help, and fewer actively maintained plugins. This drawback, however, is somewhat offset by thorough and very thoughtful [documentation](https://docs.pylonsproject.org/projects/pyramid/en/1.10-branch/quick_tour.html).

### Bottle

![Bottle]({{site.images}}{{page.slug}}/bottle.png)\

[Bottle](https://bottlepy.org/docs/dev/) is a Python microframework that's been around since 2009. It provides URL routing, a built-in SimpleTemplate engine, support for other template engines like Jinja2 and Cheetah, and convenient APIs to access form data, file uploads, and cookies.

Bottle has no hard dependencies other than the Python standard library and is known for its clean and readable syntax. On the framework spectrum, it's comparable to Flask but easier to get started.

Bottle is best suited for prototyping and building smaller web applications. As noted in its [documentation](https://bottlepy.org/docs/dev/faq.html#about-bottle), while it's possible to add more features and build more complex applications with Bottle, there are frameworks with much better upscaling support.

### CherryPy

![CherryPy]({{site.images}}{{page.slug}}/cherry.png)\

[CherryPy](https://cherrypy.dev/) is the oldest framework in this roundup and was first released back in 2002.

Self-described as a minimalist Python web framework, it focuses on being object-oriented and enables writing web applications in much the same way any other object-oriented Python program would be written.

CherryPy is closer to microframeworks on the framework spectrum, although it does have built-in components for caching, authentication, and session management. It doesn't bundle any database access components, suggesting third-party ORMs like SQLAlchemy or SQLObject instead. The same goes for template engines. Unfortunately, for template and database integration recipes, the [CherryPy documentation](https://docs.cherrypy.dev/en/latest/advanced.html#database-support) links to external resources that are no longer available.

The online community around CherryPy doesn't show a lot of signs of life. Unless you're an established CherryPy expert, this means it'll be hard to find outside help when you get stuck.

## How to Choose a Python Framework

When choosing a framework for your next project, consider the following factors to guide your decision:

* **Past success with a particular framework:** If your current framework works for you and your team and your next web application isn't going to be conceptually different from your past applications, then just go with your experience.
* **Web development style:** Are you going to develop a full-stack, server-rendered web application that includes both the client and the server, or are you going to focus on developing an API to serve a separate frontend?
* **Preferred level of control:** Are you comfortable with a framework that defines components to use, or do you prefer to take more control and choose components yourself?
* **ORM preference:** SQLAlchemy is the ORM of choice for many in the Python community. Django comes with its own ORM, which is fine for most use cases but can be hard to work with when you perform a lot of data aggregations or when database connection performance is critical. While there are ways to make SQLAlchemy work with Django, if using SQLAlchemy is a major requirement for your next web application, you may be better off with a different web development framework.

Here's a table to help guide you through your decision:

| Framework | Consider using if | Think twice before using if |
|----|----|----|
| Django | You create a lot of similar CRUD applications for various clients<br/><br/>You prefer the "batteries included" approach, where a framework suggests components for you<br/><br/>Your applications are just fine with server-side rendering and don't require rich frontends<br/><br/>You need to grow your development team and onboard new developers quickly<br/><br/>You want to invest in a framework that is backed by sponsors and the community and is sure to stay maintained in the foreseeable future | Highest performance is a critical requirement for your application<br/><br/>You expect to be working on a data-heavy application with lots of data aggregation<br/><br/>You like to have a lot of freedom in picking the components of your web framework |
| Flask | You want more control over the components that you can use in your framework of choice<br/><br/>You expect to be working on a data-heavy application with lots of data aggregation<br/><br/>You need to grow your development team and onboard new developers quickly<br/><br/>You want to pick a framework that is well maintained by a dedicated team | You prefer opinionated frameworks that suggest the entire set of components to use in your applications |
| FastAPI | You need the highest performance out of all the popular Python frameworks<br/><br/>You have a frontend team ready to craft rich frontend experiences with JavaScript-based frameworks such as React or Vue | You want to develop monolithic web applications with server-side rendering<br/><br/>You want to rest assured that your framework of choice is going to be maintained long-term |
| Pyramid | You want to find a better balance between opinionated full frameworks and minimalistic microframeworks | You need to quickly hire developers who have experience with your framework of choice |
| Bottle | You are about to create multiple quick application prototypes | Your next application is strongly defined in scope and is expected to grow in complexity |
| CherryPy | Your team has considerable prior experience with the framework | All other scenarios |

## Summary

If you're a professional Python web developer who's looking to pick a framework for your next project, this article provided you with a concise overview of the current web framework landscape, along with practical tips to help you make an informed decision.

Django, Flask, and FastAPI are the current leaders, but if you're not happy with those three, there are a few less popular frameworks to consider.

Happy pythonic coding!

{% include_html cta/bottom-cta.html %}
