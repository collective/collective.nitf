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
                        top: 'center',
                        onBeforeLoad: function(e) {
                            $('#mediabox').width($(window).width()*0.9).height($(window).height()*0.9);
                        },
                        onLoad: function (e) {
                            Galleria.loadTheme("++resource++collective.nitf/galleria-theme/galleria.nitf_theme.js");
                            Galleria.configure({
                                autoplay: true,
                                debug: false,
                                carousel: true,
                                thumbnails: true,
                                _toggleInfo: true,
                                width: $(window).width() * .9,
                                height: $(window).height() * .9
                            });
                            Galleria.run(".pb-ajax #mediabox");
                        }
                    }
                });
            }
        } else if (nitf_galleria) {
            // If this is a NITF content in a galleria template WITH images
            if ($('.newsview #mediabox').length) {
                // set dimensions of galleria container
                $('#mediabox').width($('#content').width() * 0.95).height($(window).height() * 0.9);
                // and run Galleria
                Galleria.loadTheme("++resource++collective.nitf/galleria-theme/galleria.nitf_theme.js");
                Galleria.configure({
                    autoplay: true,
                    debug: false,
                    thumbnails: true,
                    _toggleInfo: true,
                    width: $('#content').width(),
                    height: $(window).height() * .9
                });
                Galleria.run('.newsview #mediabox', {
                    keepSource: true
                });
            }

            // Also, for galleria template, hide address bar after page load
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
            }

            window.addEventListener("load", function () {
                if (!window.pageYOffset) {
                    hideAddressBar();
                }
            });
            window.addEventListener("orientationchange", hideAddressBar);

        }
    });
})(jQuery);
