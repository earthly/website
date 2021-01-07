function installOnDownload() {
    $('.on-download-listen').mousedown(function() {
        setTimeout(function() {
            $('.on-download-show-wrap').height('auto');
            $('.on-download-show').css({top: '0px'});
        }, 1000);
    });
}

$(document).ready(function() {
    installOnDownload();
});
