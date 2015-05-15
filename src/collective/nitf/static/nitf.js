(function ($) {
  "use strict";
  $(document).ready(function () {
    // If this is a NITF content with an image
    var nitf_view = $('body.portaltype-collective-nitf-content.template-view').length > 0;
    var nitf_with_image = nitf_view && $('.newsImageContainer').length > 0;
    var nitf_galleria = $('body.portaltype-collective-nitf-content.template-galleria').length > 0;
    if (nitf_with_image) {
      // Turn image link into something special
      var link = $('#parent-fieldname-image');
      // Add a magnify icon over the image
      link.append('<span class="magnify"></span>');
      // For mobile devices, link will open galleria
      if (/Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent)) {
        link.attr('href', link.attr('href').replace('@@galleria', '@@galleria?ajax_include_head=1&amp;ajax_load=1'));
      } else {
        // For other devices open a galleria in an overlay
        link.prepOverlay({
          subtype: 'ajax',
          filter: '#content > *',
          width: ($(document).width() * 0.95) + 'px',
          config: {
            onLoad: function (e) {
              // Start cycle2
              $('#galleria').cycle();
            }
          }
        });
      }
    } else if (nitf_galleria) {
      // For galleria template, hide address bar after page load
      // in mobile devices
      /* To hide address bar after page load */
      var hideAddressBar = function() {
        if (!window.location.hash) {
          if (document.height < window.outerHeight) {
            document.body.style.height = (window.outerHeight + 50) + 'px';
          }

          setTimeout(function () {
            window.scrollTo(0, 1);
          }, 50);
        }
      };

      window.addEventListener("load", function () {
        if (!window.pageYOffset) {
          hideAddressBar();
        }
      });
      window.addEventListener("orientationchange", hideAddressBar);
    }
  });
})(jQuery);
