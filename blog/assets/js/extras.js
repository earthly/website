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
        console.log("pre")
        elem = b;
      } else if (b.tagName == "DIV" && b.firstChild.tagName == "PRE") {
        console.log("nested pre")
        elem = b.firstChild;
      }
      console.log(elem)
      if(elem)
      {
        console.log("setting")
        // elem.innerHTML = "<span class=\"syntax-label\">"+caption+"<img src=\"/blog/assets/images/iTerm-icon.png\"/ width=\"24\" height=\"24\"></span>" + elem.innerHTML;
        elem.innerHTML = "<span class=\"syntax-label\">"+caption+"</span>" + elem.innerHTML;
      }
    }
};

syntaxLabel();