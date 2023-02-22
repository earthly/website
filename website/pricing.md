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
   <em><span class="font-semibold"> Note:</span> A Free plan will be available in the near future.</em>
</div>

<div class="grid grid-cols-1 gap-4 lg:gap-2 lg:grid-cols-4 mb-12 relative z-10">
  {% include /pricing/v2/tier-1.html  %}
  {% include /pricing/v2/tier-2.html  %}
  {% include /pricing/v2/tier-3.html  %}
  {% include /pricing/v2/tier-4.html  %}

</div>

{% include /pricing/v2/compute-cost-table.html  %}

{% include /pricing/v2/pricing-faq.html  %}
