

$(document).ready(function() {
    var mouseY = 0;
    var scrolled = false;

    $(document).mousemove(function(e) {
        mouseY = e.clientY;
    });

    $(document).mouseleave(function () {
        if (mouseY < 100) {
            triggerStarCta();
        }
    });

    $(document).scroll(function() {
        if (!scrolled) {
            setTimeout(function() {
                triggerStarCta();
            }, 5000);
            scrolled = true;
        }
    });
});

function triggerStarCta() {
    if (localStorage && localStorage.getItem('earthly-star-cta-shown') === 'true') {
        return;
    }

    $('.star-cta').attr({
        "data-balloon-visible": "",
        "aria-label": "Bookmark me for later!",
        "data-balloon-pos": "down",
    });
    if (localStorage) {
        localStorage.setItem('earthly-star-cta-shown', 'true')
    }
}
