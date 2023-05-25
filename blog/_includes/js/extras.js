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
  for (var c = document.querySelectorAll("pre.sourceCode"), a = 0; a < c.length; a++) {
    var b = c[a];
    var caption = b.parentElement.getAttribute('data-caption');
    b.innerHTML =
      `<div class="toolbar"><div>${caption || "Terminal"}</div><div class="copy-item" data-clipboard-text="${
        b.querySelector("code").innerText
      }">Copy</div></div>` + b.innerHTML;
  };
};

syntaxLabel();