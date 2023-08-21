function setCookie(name, value, days, domain) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    var domStr = "";
    if (domain) {
        domStr = "; Domain=" + domain;
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/" + domStr;
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function uuidv4() {
    return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
      (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
    );
}

var newVisitor = false;

function getAnalyticCookie() {
    var cookieName = 'earthlyID';
    var earthlyID = getCookie(cookieName);
    if (!earthlyID) {
        // Generate new cookie.
        earthlyID = uuidv4();
        newVisitor = true;
    }
    setCookie(cookieName, earthlyID, 100*365, ".earthly.dev");
    return earthlyID;
}

$(document).ready(function() {
    var earthlyID = getAnalyticCookie();
    $.ajax({
        type: "POST",
        url: "https://api.earthly.dev/analytics",
        data: JSON.stringify({
            key: "website",
            url: window.location.href,
            referrer: document.referrer,
            earthlyID: earthlyID,
        }),
    });

    analytics.identify(earthlyID);
    if (newVisitor) {
        analytics.track('Cookie created');
    }
});
