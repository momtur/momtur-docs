// WriteSonic SEO Fixer Script
(function() {
  // Load the SEO fixer script
  var script = document.createElement('script');
  script.id = 'wsAiSeoMb';
  script.type = 'application/javascript';
  script.async = true;
  script.src = 'https://seo-fixer.writesonic.com/site-audit/fixer-script/index.js';
  
  // Configure after script loads
  script.onload = function() {
    if (typeof wsSEOfixer !== 'undefined') {
      wsSEOfixer.configure({
        hostURL: 'https://seo-fixer.writesonic.com',
        siteID: '687c9842e7e209b5e598adef'
      });
    }
  };
  
  // Append to head
  document.head.appendChild(script);
})();