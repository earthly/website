---
title: Pricing
layout: default
---

<link rel="stylesheet" href="/assets/css/subpage.css">

<div class="background-pricing">
  <div class="max-w-7xl mx-auto mt-[70px] px-6 lg:px-10">
    {% include /pricing/v2/hero.html %}

    <div id="cloud-pricing" class="text-[40px] font-semibold mt-2 text-center">Earthly Cloud Pricing</div>

    <div class="flex gap-6 lg:gap-10 justify-center mt-4">
      <p id="highlight-category-1" class="highlight-category active" onclick="">Cloud</p>
      <p id="highlight-category-2" class="highlight-category" onclick="">Self-Hosted</p>
      <p id="highlight-category-3" class="highlight-category" onclick="">BYOC</p>
    </div>

    <div class="flex justify-center lg:justify-start mt-4">
      <span class="font-bold text-gray-900">Monthly</span>
      <label class="toggle-switch">
        <input id="pricing-toggle-switch" type="checkbox" checked>
        <span class="slider"></span>
      </label>
      <span class="font-bold text-gray-900">Annual</span>
    </div>

    {% include /pricing/v2/estimate.html %}

    <div id="pricing-tiers" class="grid grid-cols-1 gap-4 lg:gap-2 lg:grid-cols-4 mt-6 relative z-10">
      {% include /pricing/v2/tier-1.html %}
      {% include /pricing/v2/tier-2.html %}
      {% include /pricing/v2/tier-3.html %}
      {% include /pricing/v2/tier-4.html %}
    </div>
    <div id="tier-5-subheading" class="text-2xl lg:text-3xl font-semibold text-center pt-1 pb-1 hidden">Bring Your Own Cloud</div>
    <div id="tier-5-subheading-2" class="text-xl lg:text-2xl text-slate-500 text-center pt-1 pb-3 hidden">Single-tenant SaaS, fully managed by Earthly in your AWS account</div>
    {% include /pricing/v2/tier-5.html %}

    {% include /pricing/v2/compute-cost-table.html %}
    {% include /pricing/v2/pricing-faq.html %}
  </div>
</div>

<script>
  document.addEventListener("DOMContentLoaded", function () {
    [...document.querySelectorAll("#tier-3-pricing > div")].slice(-2).forEach(x => x.classList.add("hidden"))

    var checkbox = document.getElementById("pricing-toggle-switch")
    var sliderInput = document.getElementById("pricing-slider")
    var planPrice = document.querySelectorAll(".plan-price")

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

      if (sliderInput.value == 1) {
        planPrice.forEach(x => x.innerText = (0).toLocaleString())
      } else if (sliderInput.value <= 5) {
        planPrice.forEach(x => x.innerText = Number(((checkbox.checked ? 9.17 : 11)* sliderInput.value).toFixed(2)).toLocaleString())
      } else if (sliderInput.value <= 15) {
        planPrice.forEach(x => x.innerText = Number(((checkbox.checked ? 29.17 : 35)* sliderInput.value).toFixed(2)).toLocaleString())
      } else {
        planPrice.forEach(x => x.innerText = Number(((checkbox.checked ? 49.17 : 59)* sliderInput.value).toFixed(2)).toLocaleString())
      }
    })

    let currentHighlight = 1;
  
    const tabs = document.querySelectorAll('[id^="highlight-category"]');
    tabs.forEach(tab => {
      tab.addEventListener("click", e => {
        const id = +e.target.id.replace("highlight-category-", "")

        if (id !== currentHighlight) {
          document.getElementById(`highlight-category-${currentHighlight}`).classList.remove('active')
          currentHighlight = id
          document.getElementById(`highlight-category-${currentHighlight}`).classList.add('active')

          const pricingCalculator = document.getElementById("pricing-calculator")
          const priceEstimate = document.querySelector(".cost-estimate > div:last-of-type")
          const tier1PricingCloud = document.getElementById("tier-1-pricing-cloud")
          const tier1PricingSelfHosted = document.getElementById("tier-1-pricing-self-hosted")
          const tier2 = document.getElementById("tier-2")
          const tier3PricingCloud = document.getElementById("tier-3-pricing-cloud")
          const tier3PricingSelfHosted = document.getElementById("tier-3-pricing-self-hosted")
          const tier4PricingCloud = document.getElementById("tier-4-pricing-cloud")
          const tier4PricingSelfHosted = document.getElementById("tier-4-pricing-self-hosted")
          const tier5 = document.getElementById("tier-5")
          const tier5Subheading = document.getElementById("tier-5-subheading")
          const tier5Subheading2 = document.getElementById("tier-5-subheading-2")
          const tier5Subtitle = document.getElementById("tier-5-subtitle")
          const tier5Pricing = document.getElementById("tier-5-pricing")
          const tier5PricingDedicated = document.getElementById("tier-5-pricing-dedicated")
          const pricingTiers = document.getElementById("pricing-tiers")
          const minutesPerMonth = document.querySelectorAll(".minutes-per-month")
          const pricePerMonth = document.querySelectorAll(".price-per-month")
          const toggleSwitch = document.getElementsByClassName("toggle-switch")[0].parentElement
          const cloudEstimate = document.getElementById("cloud-estimate")
          const selfHostedEstimate = document.getElementById("self-hosted-estimate")
          const computePricingContainer = document.getElementById("compute-pricing-container")

          if (id == 1) {
            computePricingContainer.classList.remove("hidden")
          } else {
            computePricingContainer.classList.add("hidden")
          }

          if (id == 2) {
            priceEstimate.classList.add("hidden")
            tier1PricingCloud.classList.add("hidden")
            tier1PricingSelfHosted.classList.remove("hidden")
            tier2.classList.add("hidden")
            tier3PricingCloud.classList.add("hidden")
            tier3PricingSelfHosted.classList.remove("hidden")
            tier4PricingCloud.classList.add("hidden")
            tier4PricingSelfHosted.classList.remove("hidden")
            tier5.classList.add("hidden")
            pricingTiers.classList.remove("lg:grid-cols-4")
            pricingTiers.classList.add("lg:grid-cols-3")
            minutesPerMonth.forEach((x, i) => {
              pricePerMonth[i].classList.remove("h-48", "xl:h-44")
              pricePerMonth[i].classList.add("h-[108px]", "xl:h-24")
              x.classList.add("hidden")
            })
            cloudEstimate.classList.add("hidden")
            selfHostedEstimate.classList.remove("hidden")
          } else {
            priceEstimate.classList.remove("hidden")
            tier1PricingCloud.classList.remove("hidden")
            tier1PricingSelfHosted.classList.add("hidden")
            tier2.classList.remove("hidden")
            tier3PricingCloud.classList.remove("hidden")
            tier3PricingSelfHosted.classList.add("hidden")
            tier4PricingCloud.classList.remove("hidden")
            tier4PricingSelfHosted.classList.add("hidden")
            tier5.classList.remove("hidden")
            pricingTiers.classList.remove("lg:grid-cols-3")
            pricingTiers.classList.add("lg:grid-cols-4")
            minutesPerMonth.forEach((x, i) => {
              pricePerMonth[i].classList.add("h-48", "xl:h-44")
              pricePerMonth[i].classList.remove("h-[108px]", "xl:h-24")
              x.classList.remove("hidden")
            })
            cloudEstimate.classList.remove("hidden")
            selfHostedEstimate.classList.add("hidden")
          }

          if (id == 3) {
            pricingCalculator.style = "display: none"
            pricingTiers.classList.add("hidden")
            tier5.classList.remove("mt-8")
            tier5.classList.add("mt-4")
            tier5Subheading.classList.remove("hidden")
            tier5Subheading2.classList.remove("hidden")
            tier5Subtitle.classList.add("hidden")
            tier5Pricing.classList.add("hidden", "lg:hidden")
            tier5PricingDedicated.classList.remove("hidden", "lg:hidden")
            toggleSwitch.classList.add("hidden")
          } else {
            pricingCalculator.style = ""
            pricingTiers.classList.remove("hidden")
            tier5.classList.add("mt-8")
            tier5.classList.remove("mt-4")
            tier5Subheading.classList.add("hidden")
            tier5Subheading2.classList.add("hidden")
            tier5Subtitle.classList.remove("hidden")
            tier5Pricing.classList.remove("hidden", "lg:hidden")
            tier5PricingDedicated.classList.add("hidden", "lg:hidden")
            toggleSwitch.classList.remove("hidden")
          }
        }
      })
    })
  })
</script>
