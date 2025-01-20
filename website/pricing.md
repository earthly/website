---
title: Pricing
layout: default
permalink: /earthfile/satellites/pricing
---

<link rel="stylesheet" href="/assets/css/subpage.css">

<div class="background-pricing">
  <div class="max-w-7xl mx-auto mt-[70px] px-6 lg:px-10">
    {% include /pricing/v2/hero.html %}

    <div id="satellites-pricing" class="text-[40px] font-semibold pt-4 text-center tracking-tight">Earthly Satellites Pricing</div>

    <div class="flex justify-center mt-9">
      <span class="font-bold text-gray-900 tracking-tight">Self-Hosted</span>
      <label class="toggle-switch">
        <input id="toggle-switch" type="checkbox">
        <span class="slider"></span>
      </label>
      <span class="font-bold text-[#9CA3AF] tracking-tight">BYOC</span>
    </div>

    {% include /pricing/v2/self-hosted.html %}
    {% include /pricing/v2/byoc.html %}

    {% include /pricing/v2/faq.html %}
  </div>
</div>

<script>
  const selfHosted = document.getElementById("self-hosted")
  const byoc = document.getElementById("byoc")

  function handleCheckboxChange(checkbox) {
    const selfHostedLabel = checkbox.parentElement.previousSibling.previousSibling
    const byocLabel = checkbox.parentElement.nextSibling.nextSibling

    if (checkbox.checked) {
      selfHostedLabel.classList.replace("text-gray-900", "text-[#9CA3AF]")
      byocLabel.classList.replace("text-[#9CA3AF]", "text-gray-900")

      selfHosted.classList.add("hidden")
      byoc.classList.remove("hidden")
    } else {
      selfHostedLabel.classList.replace("text-[#9CA3AF]", "text-gray-900")
      byocLabel.classList.replace("text-gray-900", "text-[#9CA3AF]")

      selfHosted.classList.remove("hidden")
      byoc.classList.add("hidden")
    }
  }

  document.querySelectorAll("#toggle-switch").forEach(checkbox => {
    checkbox.addEventListener("change", () => handleCheckboxChange(checkbox))
  })
</script>
