jq(function($) {
    $(".tiles .thumbnails").scrollable({size: 3});
    $(".previews .thumbnails").scrollable({size: 1, circular: true});
    $("#mediabox #images").scrollable({size: 1, circular: true});
    $(".template-newsmedia_view .tiles .thumbnails .items img[src].media-image").prepOverlay({
        subtype:'image',
        urlmatch: '/image_.+$',
        urlreplace: '/image_large'
    });

    $(".template-gallery .tiles .thumbnails .items img.media-image").click(function() {
        // see if same thumb is being clicked
        if ($(this).hasClass("active")) { return; }
        // calclulate large image's URL based on the thumbnail URL (flickr specific)
        var url = $(this).attr("src").replace("_tile", "_preview");
        // get handle to element that wraps the image and make it semi-transparent
        var wrap = $("#mediabox").fadeTo("medium", 0.5);
        // the large image from www.flickr.com
        var img = new Image();
        // call this function after it's loaded
        img.onload = function() {
            // make wrapper fully visible
            wrap.fadeTo("fast", 1);
            // change the image
            wrap.find("img").attr("src", url);
        };
        img.src = url;
        // activate item
        $(".template-gallery .tiles .thumbnails .items img.media-image").removeClass("active");
        $(this).addClass("active");
    }).filter(":first").click();
    $(".newsview #mediabox").appendTo("body");
    $("#mediabox #images").scrollable();
    $(".newsImageContainer a").prepOverlay({
        subtype:'inline',
        target: '#mediabox'
        /*
            */
    });

    $("#mediabox #images img").tooltip({
        position: 'bottom center',
        offset: [-85, -30],
        opacity: 0.8,
        effect: 'fade',

        // position tooltips relative to the parent scrollable
        relative: true
    });

    /*$(".newsImageContainer img").overlay({
            effect: 'apple',
            target: '#mediabox',
            mask: { maskId: 'mask' },

            // when box is opened, scroll to correct position (in 0 seconds)
            onLoad: function() {
            $("#mediabox #images").data("scrollable").seekTo(0, 0);
        }
    });

    $(".previews #images img").tooltip({
        position: 'bottom center',
        offset: [-85, -30],
        opacity: 0.8,
        effect: 'fade',

        // position tooltips relative to the parent scrollable
        relative: true
    });
    */
});
