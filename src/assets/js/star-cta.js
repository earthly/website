
var mouseY = 0;

$(document).ready(function() {

    document.addEventListener("mousemove", function(e) {
        mouseY = e.clientY;
    });

    $(document).mouseleave(function () {
        if (mouseY < 100) {
            $('.star-cta').attr({
                "data-balloon-visible": "",
                "aria-label": "Bookmark me for later!",
                "data-balloon-pos": "down",
            });
        }
    });
});
