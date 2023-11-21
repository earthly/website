---
title: Earthly
layout: default
banner: <b>Introducing Earthly Cloud.</b> Consistent builds. Ridiculous speed. Next-gen developer experience. Works with any CI. Get 6,000 min/mth free! <a href="https://earthly.dev/blog/earthly-cloud-free-tier-launch/" onclick="bannerLinkClick()">Learn more</a>.
mobileBanner: <b>Introducing Earthly Cloud.</b> Get 6,000 min/mth free! <a href="https://earthly.dev/blog/earthly-cloud-free-tier-launch/" onclick="bannerLinkClick()">Learn more</a>.
---

<!-- Gavin, 20231109, A/B test homepage-hero-earthfile-image: added divs -->
<div id="homepage-hero-earthfile-image-control-01">{% include home/layout.html template='home/v2/hero.html' %}</div>
<div id="homepage-hero-earthfile-image-test-01" style="display: none">
  <div class="lg:hidden">{% include home/layout.html template='home/v2/hero-with-graphic-mobile.html' %}</div>
  <div class="hidden lg:block">{% include home/layout.html template='home/v2/hero-with-graphic.html' %}</div>
</div>
{% include home/layout.html template='home/v2/customers.html' %}
{% include home/layout.html template='home/v2/customer-quotes.html' %}
{% include home/layout.html template='home/why.html' %}

{% include home/layout.html template='cloud/benefits-title.html' %}
{% include home/layout.html template='cloud/benefits-build-automation.html' %}
{% include home/layout.html template='cloud/benefits-write-once.html' %}
{% include home/layout.html template='cloud/benefits-caching.html' %}
{% include home/layout.html template='cloud/benefits-speed.html' %}
{% include home/layout.html template='home/v2/benefits-earthfile.html' %}
{% include home/layout.html template='home/v2/benefits-monorepo.html' %}

{% include home/layout.html template='cta-home-button.html' %}
