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
      <p id="pricing-tab-1" class="highlight-category active">Cloud</p>
      <p id="pricing-tab-2" class="highlight-category">Self-Hosted</p>
      <p id="pricing-tab-3" class="highlight-category">BYOC</p>
    </div>

    {% include /pricing/v2/cloud.html %}
    {% include /pricing/v2/self-hosted.html %}
    {% include /pricing/v2/byoc.html %}

    {% include /pricing/v2/pricing-faq.html %}
  </div>
</div>

<script>
  const cloud = document.getElementById("cloud")
  const selfHosted = document.getElementById("self-hosted")
  const byoc = document.getElementById("byoc")

  let currentTabIndex = 1
  let currentTab = "cloud"
  let isAnnual = true
  let sliderValue = 1

  // Tab change listener
  const tabs = document.querySelectorAll('[id^="pricing-tab"]')
  tabs.forEach(tab => {
    tab.addEventListener("click", e => {
      const id = +e.target.id.replace("pricing-tab-", "")

      if (id !== currentTabIndex) {
        document.getElementById(`pricing-tab-${currentTabIndex}`).classList.remove("active")
        currentTabIndex = id
        currentTab = id == 1 ? "cloud" : id == 2 ? "self-hosted" : "byoc"
        document.getElementById(`pricing-tab-${currentTabIndex}`).classList.add("active")

        // Show the active tab content and hide others
        if (id == 1) {
          cloud.classList.remove("hidden")
          selfHosted.classList.add("hidden")
          byoc.classList.add("hidden")
        } else if (id == 2) {
          cloud.classList.add("hidden")
          selfHosted.classList.remove("hidden")
          byoc.classList.add("hidden")
        } else if (id == 3) {
          cloud.classList.add("hidden")
          selfHosted.classList.add("hidden")
          byoc.classList.remove("hidden")
        }

        // Set current toggle value on tab change
        const pricingToggleSwitch = document.querySelector(`#${currentTab} #pricing-toggle-switch`)
        if (pricingToggleSwitch) {
          pricingToggleSwitch.checked = isAnnual
          handleCheckboxChange(pricingToggleSwitch)
        }

        // Set current slider value on tab change
        const pricingSlider = document.querySelector(`#${currentTab} #pricing-slider`)
        if (pricingSlider) {
          pricingSlider.value = sliderValue
          handleSliderChange(pricingSlider)
        }
      }
    })
  })

  // Annual/Monthly toggle listener
  function handleCheckboxChange(checkbox) {
    const sliderInput = document.querySelector(`#${currentTab} #pricing-slider`)
    const planPrice = document.querySelector(`#${currentTab} #plan-price`)
    const tier2Pricing = document.querySelector(`#${currentTab} #tier-2-pricing`)
    const tier3Pricing = document.querySelector(`#${currentTab} #tier-3-pricing`)
    const tier4Pricing = document.querySelector(`#${currentTab} #tier-4-pricing`)

    if (tier2Pricing) tier2Pricing.innerText = checkbox.checked ? 9.17 : 11
    tier3Pricing.innerText = checkbox.checked ? 29.17 : 35
    tier4Pricing.innerText = checkbox.checked ? 49.17 : 59

    if (sliderInput.value == 1) {
      planPrice.innerText = (0).toLocaleString()
    } else if (sliderInput.value <= 5) {
      planPrice.innerText = Number(((checkbox.checked ? 9.17 : 11)* sliderInput.value).toFixed(2)).toLocaleString()
    } else if (sliderInput.value <= 15) {
      planPrice.innerText = Number(((checkbox.checked ? 29.17 : 35)* sliderInput.value).toFixed(2)).toLocaleString()
    } else {
      planPrice.innerText = Number(((checkbox.checked ? 49.17 : 59)* sliderInput.value).toFixed(2)).toLocaleString()
    }

    isAnnual = checkbox.checked
  }

  // Slider value change listener
  function handleSliderChange(slider) {
    const { min, max, value } = slider
    slider.style.backgroundSize = (value - min) * 100 / (max - min) + "% 100%"

    const checkbox = document.querySelector(`#${currentTab} #pricing-toggle-switch`)
    const numUsers = document.querySelector(`#${currentTab} #num-users`)
    const planName = document.querySelector(`#${currentTab} #plan-name`)
    const planDescription = document.querySelector(`#${currentTab} #plan-description`)
    const costEstimate = document.querySelector(`#${currentTab} #cost-estimate`)
    const planPrice = document.querySelector(`#${currentTab} #plan-price`)
    const planMinutes = document.querySelector(`#${currentTab} #plan-minutes`)
    const contactUsButton = document.querySelector(`#${currentTab} #contact-us-button`)
    const tier1 = document.querySelector(`#${currentTab} #tier-1`)
    const tier2 = document.querySelector(`#${currentTab} #tier-2`)
    const tier3 = document.querySelector(`#${currentTab} #tier-3`)
    const tier4 = document.querySelector(`#${currentTab} #tier-4`)

    numUsers.innerText = (value > 50 ? "50+" : value) + " user" + (value > 1 ? "s" : "")

    const width = numUsers.getBoundingClientRect().width / 2
    if (value > 45) {
      numUsers.style.left = "unset"
      numUsers.style.right = `calc((13px * (50 - ${value}) - 12px)`
    } else {
      numUsers.style.left = `calc(${value * 2}% - ${width}px - ${value * .5}px)`
      numUsers.style.right = "unset"
    }

    if (value == 1 || (value <= 5 && currentTab == "self-hosted")) {
      planName.innerText = "Free Plan"
      planDescription.innerText = "For hobby projects"
      planPrice.innerText = 0
      if (planMinutes) planMinutes.innerText = (6000).toLocaleString()
    } else if (value <= 5) {
      planName.innerText = "Starter Plan"
      planDescription.innerText = "For small projects"
      planPrice.innerText = ((checkbox.checked ? 9.17 : 11) * value).toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 2 })
      if (planMinutes) planMinutes.innerText = (10000 + 2000 * value).toLocaleString()
    } else if (value <= 15) {
      planName.innerText = "Pro Plan"
      planDescription.innerText = "For small teams"
      planPrice.innerText = ((checkbox.checked ? 29.17 : 35) * value).toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 2 })
      if (planMinutes) planMinutes.innerText = (20000 + 3000 * value).toLocaleString()
    } else if (value <= 50) {
      planName.innerText = "Team Plan"
      planDescription.innerText = "For large teams"
      planPrice.innerText = ((checkbox.checked ? 49.17 : 59) * value).toLocaleString(undefined, { maximumFractionDigits: 2, minimumFractionDigits: 2 })
      if (planMinutes) planMinutes.innerText = (50000 + 4000 * value).toLocaleString()
    } else {
      planName.innerText = "Enterprise Plan"
      planDescription.innerText = "For enterprises"
    }

    costEstimate.style.display = value > 50 ? "none" : "flex"
    contactUsButton.style.display = value > 50 ? "flex" : "none"

    tier1.style.opacity = value <= 5 ? 1 : 0.5
    tier1.style.pointerEvents = value <= 5 ? "unset" : "none"

    if (tier2) {
      tier2.style.opacity = value <= 5 ? 1 : 0.5
      tier2.style.pointerEvents = value <= 5 ? "unset" : "none"
    }

    tier3.style.opacity = value <= 15 ? 1 : 0.5
    tier3.style.pointerEvents = value <= 15 ? "unset" : "none"

    tier4.style.opacity = value <= 50 ? 1 : 0.5
    tier4.style.pointerEvents = value <= 50 ? "unset" : "none"

    sliderValue = value
  }

  document.querySelectorAll("#pricing-toggle-switch").forEach(checkbox => {
    checkbox.addEventListener("change", () => handleCheckboxChange(checkbox))
  })

  document.querySelectorAll("#pricing-slider").forEach(slider => {
    slider.addEventListener("input", () => handleSliderChange(slider))
  })
</script>
