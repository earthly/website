// Open external links in another tab
function externalLinks() {
    for(var c = document.getElementsByTagName("a"), a = 0;a < c.length;a++) {
      var b = c[a];
      b.getAttribute("href") && b.hostname !== location.hostname && (b.target = "_blank")
    }
};

externalLinks();

// Add label to code blocks
//.caption
function addStuff(label, action){
  for(var c = document.querySelectorAll('['+ label +']') , a = 0;a < c.length; a++) {
    var b = c[a];
    var caption = b.getAttribute(label);
    var elem;
    if(b.tagName == "PRE"){
      elem = b;
    } else if (b.tagName == "DIV" && b.firstChild.tagName == "PRE") {
      elem = b.firstChild;
    }
    if(elem && caption) {
      if (!elem.classList.contains('output') && !["Results", "Output", ">_"].includes(caption)) {
        elem.classList.add("relative", "pt-11");
        elem.innerHTML =
          `<div class="toolbar"><div>${caption}</div><div class="copy-item" data-clipboard-text="${
            b.querySelector("code").innerText.replace(/"/g, '&quot;')
          }">Copy</div></div>` + elem.innerHTML;
      } else {
        action(elem, caption)
      }
    }
  }
}

function syntaxLabel() {
    //mobile version
    // use ~~~{captionm="filename"}
    addStuff("data-caption",
    function (elem, caption) {
      elem.innerHTML =  "<span class=\"syntax-label\">"+caption+"</span>" + elem.innerHTML ; 
    }
    );

    //wide caption : too wide to show on mobile
    // use ~~~{captionw="filename"}
    addStuff("data-captionw",
     function (elem, caption) {
      elem.innerHTML =  "<span class=\"syntax-label-wide\">"+caption+"</span>" + elem.innerHTML ; 
     }
    );

    // bottom caption
    // use ~~~{captionb="filename"}
    addStuff("data-captionb",
      function (elem, caption) {
         elem.innerHTML = elem.innerHTML + "<span class=\"syntax-label-bottom\">"+caption+"</span>" ; 
       }
    );

    // bottom caption
    // use ~~~{bcaptionb="filename"}
    addStuff("data-bcaption",
    function (elem, caption) {
       elem.innerHTML = elem.innerHTML + "<span class=\"syntax-label-bottom\">"+caption+"</span>" ; 
     }
  );
};

syntaxLabel();