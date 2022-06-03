// Conditionally loads scripts.
var loadScripts = function(params) {

  // Iterate over each source.
  var eachSource = function(callback) {
    if (typeof params.scripts == 'string') {
      callback(params.scripts);
    }
    else {
      for (var i=0; i < params.scripts.length; i++) {
        callback(params.scripts[i]);
      }
    }
  };

  // Perform a test immediately.
  if (!params.test()) {

    // Add the sources to the code.
    var tag = null;
    var firstScriptTag = document.getElementsByTagName('script')[0];
    eachSource(function(source) {
      tag = document.createElement('script');
      tag.src = source;
      firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
    });

    // Check every 200ms.
    setTimeout(function tryAgain() {
      if (params.test()) {
        params.done();
      }
      else {
        setTimeout(tryAgain, 200);
      }
    }, 200);
  }
  else {

    // Say we are done.
    params.done();
  }
};


