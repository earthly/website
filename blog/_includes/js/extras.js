// Open external links in another tab
function externalLinks() {
    for(var c = document.getElementsByTagName("a"), a = 0;a < c.length;a++) {
      var b = c[a];
      b.getAttribute("href") && b.hostname !== location.hostname && (b.target = "_blank")
    }
};

externalLinks();


// Add label to code blocks
function syntaxLabel() {
    for(var c = document.querySelectorAll('[data-caption]') , a = 0;a < c.length; a++) {
      var b = c[a];
      var caption = b.getAttribute('data-caption');
      var elem;
      if(b.tagName == "PRE"){
        elem = b;
      } else if (b.tagName == "DIV" && b.firstChild.tagName == "PRE") {
        elem = b.firstChild;
      }
      if(elem)
      {
        elem.innerHTML = "<span class=\"syntax-label\">"+caption+"</span>" + elem.innerHTML;
      }
    }
};

syntaxLabel();