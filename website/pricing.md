---
title: Pricing
layout: default
---

<link rel="stylesheet" href="/assets/css/subpage.css">

<div class="background-pricing">
  <div class="max-w-7xl mx-auto mt-[70px] px-6 lg:px-10">
    {% include /pricing/v2/hero.html %}

    <div class="text-[40px] font-semibold mt-2 text-center">Earthly cloud pricing</div>

    <div class="flex justify-center mt-8">
      <label class="toggle-switch">
        <input id="pricing-toggle-switch" type="checkbox" checked>
        <span class="slider"></span>

        <span class="label left-0">Monthly</span>
        <span class="label right-0">Annual</span>
      </label>
    </div>

    {% include /pricing/v2/estimate.html %}

    <div class="grid grid-cols-1 gap-4 lg:gap-2 lg:grid-cols-4 mb-8 mt-6 relative z-10">
      {% include /pricing/v2/tier-1.html %}
      {% include /pricing/v2/tier-2.html %}
      {% include /pricing/v2/tier-3.html %}
      {% include /pricing/v2/tier-4.html %}
    </div>
    {% include /pricing/v2/tier-5.html %}

    {% include /pricing/v2/compute-cost-table.html %}
    {% include /pricing/v2/pricing-faq.html %}
  </div>
</div>

<script>
  document.addEventListener("DOMContentLoaded", function () {
    var checkbox = document.getElementById("pricing-toggle-switch")
    var sliderInput = document.getElementById("pricing-slider")
    var planPrice = document.getElementById("plan-price")

    checkbox.addEventListener("change", function () {
      if (checkbox.checked) {
        document.getElementById("tier-2-pricing").innerText = 9.17
        document.getElementById("tier-3-pricing").innerText = 29.17
        document.getElementById("tier-4-pricing").innerText = 49.17
      } else {
        document.getElementById("tier-2-pricing").innerText = 11
        document.getElementById("tier-3-pricing").innerText = 35
        document.getElementById("tier-4-pricing").innerText = 59
      }

      if (sliderInput.value <= 5) {
        planPrice.innerText = Number(((checkbox.checked ? 9.17 : 11)* sliderInput.value).toFixed(2)).toLocaleString()
      } else if (sliderInput.value <= 5) {
        planPrice.innerText = Number(((checkbox.checked ? 29.17 : 35)* sliderInput.value).toFixed(2)).toLocaleString()
      } else {
        planPrice.innerText = Number(((checkbox.checked ? 49.17 : 59)* sliderInput.value).toFixed(2)).toLocaleString()
      }
    })
  })
</script>
