---
title: Earthly
layout: default
---
<script>
    $(document).ready(function() {
    // Run after all ajax requests, so analytics has fired.
    $(document).ajaxStop(function() {
       window.location.href = '/';
    });
});
</script>
