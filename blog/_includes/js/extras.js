// Open external links in another tab
function externalLinks() {
    for(var c = document.getElementsByTagName("a"), a = 0;a < c.length;a++) {
      var b = c[a];
      b.getAttribute("href") && b.hostname !== location.hostname && (b.target = "_blank")
    }
};

externalLinks();

// Customize code blocks
function syntaxLabel() {
  for (var c = document.querySelectorAll("pre.sourceCode:not(.merge-code)"), a = 0; a < c.length; a++) {
    var b = c[a];
    var caption = b.parentElement.getAttribute("data-caption");
    if (caption) {
      b.classList.add("pt-11");

      if (caption == ">_") {
        b.innerHTML =
          `<div class="toolbar"><div class="terminal">${caption}</div><div>Terminal</div></div>` +
          b.innerHTML;
      } else {
        b.innerHTML =
          `<div class="toolbar"><div>${caption}</div><div class="copy-item" data-clipboard-text="${
            b.querySelector("code").innerText.replace(/"/g, '&quot;')
          }">Copy</div></div>` + b.innerHTML;
      };
    };
  };
};

syntaxLabel();