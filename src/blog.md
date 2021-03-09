---
title: Blog
layout: page
---
{% for post in site.blog %}
  <h2><a href="{{post.url}}">{{ post.title }}</a></h2>
{% endfor %}