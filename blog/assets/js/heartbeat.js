//Heartbeat for session tracking
function heartbeat() {
      // console.log('heartbeat');
      analytics.track('blog-heartbeat', {
        category: 'heartbeat',
        label: 'blog-heartbeat'
      });
  }

  var heartbeatInterval = null;

  function startHeartbeat() {
    if (!heartbeatInterval) {
      heartbeatInterval = setInterval(heartbeat, 5000);
    }
  }

  function stopHeartbeat() {
    clearInterval(heartbeatInterval);
    heartbeatInterval = null;
  }

  function supportsPageVisibility() {
    return typeof document.hidden !== "undefined" || typeof document.msHidden !== "undefined";
  }

  if (supportsPageVisibility()) {
    startHeartbeat();

    // Listen for visibility change events
    document.addEventListener('visibilitychange', function() {
      if (document.hidden) {
        stopHeartbeat();
      } else {
        startHeartbeat();
      }
    });
  }
