$(document).ready(function() {
    $('.on-download-listen').mousedown(function() {
        setTimeout(function() {
            $('.on-download-show-wrap').height('auto');
            $('.on-download-show').css({top: '0px'});
        }, 1000);
    });
});
