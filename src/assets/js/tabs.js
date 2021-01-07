
function getOS() {
    var userAgent = window.navigator.userAgent,
        platform = window.navigator.platform,
        macosPlatforms = ['Macintosh', 'MacIntel', 'MacPPC', 'Mac68K'],
        windowsPlatforms = ['Win32', 'Win64', 'Windows', 'WinCE'],
        iosPlatforms = ['iPhone', 'iPad', 'iPod'],
        os = null;

    if (macosPlatforms.indexOf(platform) !== -1) {
        os = 'mac';
    } else if (iosPlatforms.indexOf(platform) !== -1) {
        os = 'ios';
    } else if (windowsPlatforms.indexOf(platform) !== -1) {
        os = 'windows';
    } else if (/Android/.test(userAgent)) {
        os = 'android';
    } else if (!os && /Linux/.test(platform)) {
        os = 'linux';
    }

    return os;
}

$(document).ready(function() {
    // set the default content from data-defaultsource
    // if your page is script-heavy, you may want to make this execute early
    // in the $(document).ready() handler to avoid ugly delays.
    $('div.tabcontrol.body').each(function() {
        $(this).html($('#' + $(this).data('defaultsource')).html());
    });

    // detect os and set default tab if name of tab matches OS.
    var os = getOS();
    $('li.tabcontrol.tab').each(function() {
        if ($(this).data('name') === os) {
            $('#' + $(this).data('target')).html( $('#' + $(this).data('source')).html());
            $(this).siblings().removeClass('active');
            $(this).addClass('active');
            installOnDownload();
        }
    });

    // handle click on tabs
    $('li.tabcontrol.tab').click(function() {
        $('#' + $(this).data('target')).html( $('#' + $(this).data('source')).html());
        $(this).siblings().removeClass('active');
        $(this).addClass('active');
        installOnDownload();
    });
});
