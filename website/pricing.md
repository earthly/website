---
title: Pricing
layout: page
pageStyle: bg-background-pricing
---

<link rel="stylesheet" href="/assets/css/subpage.css">

<div class="text-xl lg:text-2xl text-slate-500 -mt-4 pt-1 pb-3">
    Pricing plans for Earthly CI 
</div>

<div class="text-base text-slate-500 -mt-4 pt-2 pb-3">
   <span class="font-semibold"> Note:</span> A Free plan will be available in the near future.
</div>

<div class="flex items-center mb-4">
  <label class="toggle-switch">
    <input id="pricing-toggle-switch" type="checkbox" checked>
    <span class="slider"></span>
  </label>

  <span class="ml-2">Annual Pricing</span>
</div>

<div class="grid grid-cols-1 gap-4 lg:gap-2 lg:grid-cols-4 mb-12 relative z-10">
  {% include /pricing/v2/tier-1.html  %}
  {% include /pricing/v2/tier-2.html  %}
  {% include /pricing/v2/tier-3.html  %}
  {% include /pricing/v2/tier-4.html  %}

</div>

{% include /pricing/v2/compute-cost-table.html  %}

{% include /pricing/v2/pricing-faq.html  %}

<script>
  document.addEventListener('DOMContentLoaded', function () {
    var checkbox = document.getElementById('pricing-toggle-switch')

    checkbox.addEventListener('change', function () {
      if (checkbox.checked) {
        document.getElementById("tier-1-pricing").innerText = 9
        document.getElementById("tier-2-pricing").innerText = 29
        document.getElementById("tier-3-pricing").innerText = 49
        document.getElementById("tier-1-satellite-pricing").innerText = 7
        document.getElementById("tier-2-satellite-pricing").innerText = 23
        document.getElementById("tier-3-satellite-pricing").innerText = 39
      } else {
        document.getElementById("tier-1-pricing").innerText = 11
        document.getElementById("tier-2-pricing").innerText = 35
        document.getElementById("tier-3-pricing").innerText = 59
        document.getElementById("tier-1-satellite-pricing").innerText = 9
        document.getElementById("tier-2-satellite-pricing").innerText = 28
        document.getElementById("tier-3-satellite-pricing").innerText = 47
      }
    })
  })
</script>
