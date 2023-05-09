var script = document.createElement("script")
script.id = "growthbookScript"
script.src = "https://cdn.jsdelivr.net/npm/@growthbook/growthbook/dist/bundles/index.js"
document.head.appendChild(script)

var script = document.querySelector("#growthbookScript");
script.addEventListener("load", function () {
  // Uncomment for testing
  // var earthlyID = uuidv4();
  var earthlyID = getAnalyticCookie();

  // Create a GrowthBook instance
  const gb = new growthbook.GrowthBook({
    apiHost: "https://cdn.growthbook.io",
    clientKey: "sdk-7wtJG1WYaaYBiQ",
    enableDevMode: true,
    attributes: {
      id: earthlyID
    },
    trackingCallback: (experiment, result) => {
      analytics.track("Experiment Viewed", {
        experimentId: experiment.key,
        variationId: result.key,
      });
    }
  });

  //Page loaded
  document.addEventListener("DOMContentLoaded", function () {
    // Wait for features to be available
    gb.loadFeatures({ autoRefresh: true, timeout: 2000 }).then(() => {
      // console.log("Features loaded");
      if(document.getElementById("nav-cta-button-copy-control")){
        //console.log("control element rendered");
        
        // Gavin, 20230502: Added for homepage-and-nav-cta-button-copy test
        const ctaOpt = gb.getFeatureValue("homepage-and-nav-cta-button-copy", 0);
        switch(ctaOpt) {
          case 1:
            document.getElementById("nav-cta-button-copy-control").style.display = "none";
            document.getElementById("nav-cta-button-copy-test1").style.display = "inline-flex";
            document.getElementById("nav-cta-button-copy-test2").style.display = "none";
            document.getElementById("nav-mobile-cta-button-copy-control").style.display = "none";
            document.getElementById("nav-mobile-cta-button-copy-test1").style.display = "flex";
            document.getElementById("nav-mobile-cta-button-copy-test2").style.display = "none";
            document.getElementById("homepage-cta-button-copy-control").style.display = "none";
            document.getElementById("homepage-cta-button-copy-test1").style.display = "inline-block";
            document.getElementById("homepage-cta-button-copy-test2").style.display = "none";
            break;
          case 2:
            document.getElementById("nav-cta-button-copy-control").style.display = "none";
            document.getElementById("nav-cta-button-copy-test1").style.display = "none";
            document.getElementById("nav-cta-button-copy-test2").style.display = "inline-flex";
            document.getElementById("nav-mobile-cta-button-copy-control").style.display = "none";
            document.getElementById("nav-mobile-cta-button-copy-test1").style.display = "none";
            document.getElementById("nav-mobile-cta-button-copy-test2").style.display = "flex";
            document.getElementById("homepage-cta-button-copy-control").style.display = "none";
            document.getElementById("homepage-cta-button-copy-test1").style.display = "none";
            document.getElementById("homepage-cta-button-copy-test2").style.display = "inline-block";
            break;
          default:
            document.getElementById("nav-cta-button-copy-control").style.display = "inline-flex";
            document.getElementById("nav-cta-button-copy-test1").style.display = "none";
            document.getElementById("nav-cta-button-copy-test2").style.display = "none";
            document.getElementById("nav-mobile-cta-button-copy-control").style.display = "flex";
            document.getElementById("nav-mobile-cta-button-copy-test1").style.display = "none";
            document.getElementById("nav-mobile-cta-button-copy-test2").style.display = "none";
            document.getElementById("homepage-cta-button-copy-control").style.display = "inline-block";
            document.getElementById("homepage-cta-button-copy-test1").style.display = "none";
            document.getElementById("homepage-cta-button-copy-test2").style.display = "none";
        }
      }
    });
  });
});
