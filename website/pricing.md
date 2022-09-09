---
title: Pricing
layout: page
---

<link rel="stylesheet" href="/assets/css/subpage.css">

<div class="grid grid-cols-1 gap-2 lg:grid-cols-3 mb-12">
  {% include /pricing/core.html  %}
  {% include /pricing/satellites.html  %}
  {% include /pricing/ci.html  %}
</div>

<div class="text-3xl font-semibold mt-10" id="compute"> FAQ</div>

<h2 class="text-2xl font-semibold mb-5 mt-10" id="compute">How much does compute cost?<span class="hide"><a href="#compute">¶</a></span></h2>

The cost of compute is based on the AWS rack price for the instances that are used underneath, plus the cost of cache storage and the cost of network ingress/egress incurred. We follow a [zero-margin pricing model for the compute](#zero-margin-compute).

<div class="grid grid-cols-4">
<div class="font-semibold text-xl border-b flex">Instance type</div>
<div class="font-semibold text-xl border-b flex">Specs </div>
<div class="font-semibold text-xl border-b flex">Price per hour</div>
<div class="font-semibold text-xl border-b flex"><div>Price per month<span class="text-sm font-normal block text-gray-600">(if used 3 hours per work day)</span></div> </div>
</div>

<div class="grid grid-cols-4 border-b">
<div class="py-4"><span class="font-semibold">small</span></div>
<div class="py-4">Coming soon</div>
<div class="py-4">-</div>
<div class="py-4">-</div>
</div>

<div class="grid grid-cols-4 border-b">
<div class="py-4"><span class="font-semibold">medium</span> (default)</div>
<div class="py-4">4 CPUs, 16 GB RAM, 90 GB cache</div>
<div class="py-4">$0.18</div>
<div class="py-4">$11.475</div>
</div>

<div class="grid grid-cols-4">
<div class="py-4"><span class="font-semibold">large</span></div>
<div class="py-4">Coming soon</div>
<div class="py-4">-</div>
<div class="py-4">-</div>
</div>

<h2 class="text-2xl font-semibold mb-5 mt-20" id="usage-tracked">How is my usage of Satellites tracked?<span class="hide"><a href="#usage-tracked">¶</a></span></h2>

The usage of Satellites is tracked by monitoring the Satellites for active builds. If there are no active builds,the Satellite goes to sleep automatically after some time. When a Satellite is asleep, it is not billed for compute. When a build is started, the Satellite is woken up automatically and billed for compute.

<h2 class="text-2xl font-semibold mb-5 mt-20" id="zero-margin-compute">What is zero-margin compute?<span class="hide"><a href="#zero-margin-compute">¶</a></span></h2>

Zero-margin compute is a pricing model where the cost of compute is passed on directly to the user, without any profit-generating margin. This allows us, the CI vendor, to better align our incentives with the end-user. Slow builds should not mean more profit for us.

<h2 class="text-2xl font-semibold mb-5 mt-20" id="how-many-satellites">How many Satellites do I need?<span class="hide"><a href="#how-many-satellites">¶</a></span></h2>

The number of Satellites depends on the amount of workload they need to handle. For maximum performance, you can create a different Satellite for each CI pipeline. In some setups, where the CI pipelines are small, that might be an overkill. The best method to determine the number of satellites is to start with one or two, and add more as needed.

Earthly prints information on build startup about how loaded the Satellite is currently. This can be used as a guide to determine if more Satellites are needed.
