---
title: Earthly Blog
layout: blog/blog-list
pagination:
  enabled: true
  collection: blog
permalink: '/blog1/'
---
{%- assign posts = paginator.posts -%}

{% for post in posts %}
  <h2><a href="{{post.url}}">{{ post.title }}</a></h2>
{% endfor %}