---
title: Earthly
---
<html>

  {%- include head.html -%}

  <body class="body body--{{ page.layout }}">
    <div class="modal-background"></div>
    <div class="color1">
    <header class="siteHeader2">
      <div class="siteHeader-logoAndMenuButton">
        <a class="siteHeader-logoLink" href="{{site.landingurl}}/">
          {% svg assets/svg/white-logo.svg class="siteHeader-logoLink-svg" height=100 %}
        </a>
      </div>
    </header>
    </div>
    <main aria-label="Content">
      <div class="color2">
      <div class="wrapper">
        {% include index_cta.html %}
      </div>
      </div>
      <div class="color1">
      <div class="wrapper">
        {% include index_cta.html %}
      </div>
      </div>
      <div class="color2">
      <div class="wrapper">
      {% include understandable.html %}
      </div>
      </div>
      <div class="color1">
      <div class="wrapper">
      {% include understandable.html %}
      </div>
      </div>
    </main>
    {%- include footer.html -%}
  </body>
</html>