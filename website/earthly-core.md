---
title: Earthly
layout: default
---

<div id="animation" style="width: 100%; height: 400px; margin-top: 70px">
  <p>Lottie library loaded from local file</p>
</div>
<div class="pt-24"></div>
{% include home/layout.html template='home/v2/core-header.html' %}
{% include home/layout.html template='home/why.html' %}
{% include home/layout.html template='home/explanation.html' backgroundColor="green-20" %}
{% include home/layout.html template='home/developers.html' backgroundColor="blue-20" %}
{% include home/layout.html template='home/community.html' %}
{% include home/layout.html template='home/endorsements.html' %}
{% include home/layout.html template='home/support.html' %}

<script id="lottieScript" defer src="/assets/js/lottie.min.js"></script>
<script>
  var script = document.querySelector('#lottieScript');
  script.addEventListener('load', function() {
    var animation = bodymovin.loadAnimation({
        container: document.getElementById('animation'),
        renderer: 'svg',
        loop: true,
        autoplay: true,
        path: '/assets/js/animation.json'
    })
  });
</script>
