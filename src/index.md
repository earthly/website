---
title: Earthly
layout: home
---

<section class="Home-hero">
  <div class="Home-heroText">
    <h2 class="Home-heroText-title">
      Reproducible Builds
    </h2>
    <p class="Home-heroText-subtitle">
    Earthly is a syntax for defining your build.  It works with your existing build system.  Get reproducible and understanble builds today.
      <code class="Home-heroText-subtitle-code">earth +build</code> and run your build locally
    </p>
  </div>
  <div class="Home-heroIllustration">
    {% svg assets/svg/symbol-only.svg %}
  </div>
</section>

{% include index_cta.html %}

<section class="Home-product">
  <div class="Home-product-UI">
    <img src="/assets/img/screen2.png">
  </div>

  <!-- <div class="Home-product-Earthfile">
    <header class="Home-product-Earthfile-header">
      <div class="Home-product-Earthfile-header-chromeDecoration">
        {% svg assets/svg/chrome-button.svg class="chrome-button1" %}
        {% svg assets/svg/chrome-button.svg class="chrome-button2" %}
        {% svg assets/svg/chrome-button.svg class="chrome-button3" %}
      </div>
      Earthfile
    </header>
    <code class="Home-product-Earthfile-code">
      <p class="earthfile-comment"># Deploy: tell Earth what YAML to deploy</p>
      <p>k8s_yaml(<span class="earthfile-arg">'app.yaml'</span>)</p>
      <p></p>
      <p class="earthfile-comment"># Build: tell Earth what images to build from which directories</p>
      <p>docker_build(<span class="earthfile-arg">'companyname/frontend'</span>, <span class="earthfile-arg">'frontend'</span>)</p>
      <p>docker_build(<span class="earthfile-arg">'companyname/backend'</span>, <span class="earthfile-arg">'backend'</span>)</p>
      <p class="earthfile-comment"># ...</p>
      <p></p>
      <p class="earthfile-comment"># Watch: tell Earth how to connect locally (optional)</p>
      <p>k8s_resource(<span class="earthfile-arg">'frontend'</span>, port_forwards=<span class="earthfile-arg-value">8080</span>)</p>
    </code>
  </div> -->

  <p class="Home-product-caption">Earthly is like if a dockerfile and a makefile had a baby (replace pic)</p>
</section>


 <section class="Home-featuresIntro">
  <p class="Home-featuresIntro-text">
    With Earthly, all builds are 
    <button class="Home-featuresIntro-text-button Home-featuresIntro-text-button--pillar-1">containerized</button> and <button class="Home-featuresIntro-text-button Home-featuresIntro-text-button--pillar2">reproducible</button> and <button class="Home-featuresIntro-text-button Home-featuresIntro-text-button--pillar3">langauge agnostic</button>
  </p>
</section>
 
<h3 class="Home-sectionHeading Home-sectionHeading--features">Why Use Earthly?</h3>
<section class="Home-features">
  <div class="Home-features-contentList-gradient"></div>
  <ul class="Home-features-contentList">
    {% for feature in site.data.features %}
      <li class="Home-features-contentItem js-featuresContentItem" 
          data-feature-id="{{ forloop.index }}">
        <button class="Home-features-contentItem-title Home-features-contentItem-title--pillar{{ feature.pillar }}" 
          data-feature-target="{{forloop.index}}"
          onclick="featureScroll(this)">
          {{feature.title}}
        </button>
        <div>
          {{feature.description}}
        </div>
      </li>
    {% endfor %}
  </ul>
</section>

{% include index_cta.html %}

<!-- <h3 class="Home-sectionHeading">See Earth in Action</h3> 
<div class="Home-video">
  <iframe width="560" height="315" src="https://www.youtube.com/embed/FSMc3kQgd5Y?controls=0" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
</div> -->

<!-- <h3 class="Home-sectionHeading">Learn More</h3>
<section class="Home-resources">
  <ul class="Home-resources-list">
    <li class="Home-resources-listItem">
      <div class="Home-resources-listItem-text">
        <h4 class="Home-subsectionHeading Home-subsectionHeading--resources">
          {% svg assets/svg/resources-docs.svg class="Home-resources-svg" %}
          Read the Docs
        </h4>
        <p>Already have a Dockerfile and a Kubernetes config? Set up Earth in no time and start getting things done. </p>
      </div>
      <a href="{{site.docsurl}}/" class="Home-resources-link">Check out Docs</a>
    </li>
    <li class="Home-resources-listItem">
      <div class="Home-resources-listItem-text">
        <h4 class="Home-subsectionHeading Home-subsectionHeading--resources">
        {% svg assets/svg/social-slack.svg class="Home-resources-svg" %}
          Chat with Us
        </h4>
        <p>Find us in the #earth channel of the official Kubernetes Slack. We’re there Mon-Fri EST business hours. We don’t bite.</p>
      </div>
      <a href="https://slack.k8s.io/" class="Home-resources-link">Get Your Invite</a>
    </li>
    <li class="Home-resources-listItem">
      <div class="Home-resources-listItem-text">
        <h4 class="Home-subsectionHeading Home-subsectionHeading--resources">
          {% svg assets/svg/resources-videos.svg class="Home-resources-svg" %}
          Quick Start
        </h4>
        <p>Short & sweet videos about Earth</p>
      </div>
      <div class="Home-resources-listItem-cta">
        <a href="https://www.youtube.com/watch?v=MIzf9vDs9JU" rel="noopener noreferrer" target="_blank" class="Home-resources-link">Earth’s Main Features <span class="Home-resources-link-meta">6m</span></a>
        <a href="https://www.youtube.com/watch?v=HSFGKxvxsWs&t=69s" rel="noopener noreferrer" target="_blank" class="Home-resources-link">Basic Concepts <span class="Home-resources-link-meta">5.5m</span></a>
        <a href="https://www.youtube.com/watch?v=MhYIsTwwPC8" rel="noopener noreferrer" target="_blank" class="Home-resources-link">Setting up Earth <span class="Home-resources-link-meta">15.5m</span></a>
      </div>
    </li>
    <li class="Home-resources-listItem">
      <div class="Home-resources-listItem-text">
        <h4 class="Home-subsectionHeading Home-subsectionHeading--resources">
          {% svg assets/svg/resources-github.svg class="Home-resources-svg" %}
          GitHub Issues
        </h4>
        <p>Have an idea or a bug to report? Check our GitHub issues. In case you want to tackle some of your own we have a collection for that.</p>
      </div>
      <a href="https://github.com/{{site.github_username}}/earth" rel="noopener noreferrer" target="_blank" class="Home-resources-link">Earth GitHub</a>
    </li>
    <li class="Home-resources-listItem">
      <div class="Home-resources-listItem-text">
        <h4 class="Home-subsectionHeading Home-subsectionHeading--resources">
          {% svg assets/svg/resources-contact.svg class="Home-resources-svg" %}
          Email us
        </h4>
        <p>Have questions or feature requests for Earth? Want to use it for your company? Just want to say hi? We love hearing from you!</p>
      </div>
      <a href="mailto:hi@earth.dev" class="Home-resources-link">hi@earth.dev</a>
    </li>
    <li class="Home-resources-listItem">
      <div class="Home-resources-listItem-text">
        <h4 class="Home-subsectionHeading Home-subsectionHeading--resources">
          {% svg assets/svg/resources-mailing-list.svg class="Home-resources-svg" %}
          Our Mailing List
        </h4>
        <p>Keep up with Multi-Service Development and all things Earth.</p>
      </div>
      <div class="Home-resources-listItem-cta">
        <form action="https://www.getdrip.com/forms/507796156/submissions" method="post" data-drip-embedded-form="507796156">
          <label for="drip-email" class="Home-resources-label">Your Email</label>
          <input class="Home-resources-input" type="email" id="drip-email" name="fields[email]" value="" placeholder="me@company.com" />
          <button class="Home-resources-button" type="submit" data-drip-attribute="sign-up-button">
            Subscribe
          </button>
          <div style="display: none;" aria-hidden="true">
            <label for="website">Website</label><br />
            <input type="text" id="website" name="website" tabindex="-1" autocomplete="false" value="" />
          </div>
        </form>
      </div>
    </li>
  </ul>
</section> -->
