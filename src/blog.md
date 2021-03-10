---
title: Blog
layout: page
---
{%- assign posts = site.blog | sort: date | reverse -%}

{% for post in posts %}
  <h2><a href="{{post.url}}">{{ post.title }}</a></h2>
{% endfor %}