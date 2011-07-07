jq(function($) {
    $(".thumbnails").scrollable({size: 3,});
    $(".thumbnails .items img[src].media-image").prepOverlay({
        subtype:'image',
        urlmatch: '/image_.+$',
        urlreplace: '/image_large',
    });

    $("#mediabox #images").scrollable({size: 1,});
    $(".newsImageContainer a").overlay({
            effect: 'apple',
            target: '#mediabox',
            mask: { maskId: 'mask' },

            // when box is opened, scroll to correct position (in 0 seconds)
            onLoad: function() {
            $("#mediabox #images").data("scrollable").seekTo(0, 0);
        }
    });
    
    $("#mediabox #images img").tooltip({
        position: 'bottom center',
        offset: [-85, -30],
        opacity: 0.8,
        effect: 'fade',

        // position tooltips relative to the parent scrollable
        relative: true
    });
    flowplayer("a.media-video", "./++resource++collective.nitf/flowplayer/flowplayer.swf", {
        // change the default controlbar to modern
        plugins: {
            controls: {
                url: "/%2B%2Bresource%2B%2Bcollective.nitf/flowplayer/flowplayer.controls.swf",

                buttonColor: 'rgba(0, 0, 0, 0.9)',
                buttonOverColor: '#000000',
                backgroundColor: '#D7D7D7',
                backgroundGradient: 'medium',
                sliderColor: '#FFFFFF',

                sliderBorder: '1px solid #808080',
                volumeSliderColor: '#FFFFFF',
                volumeBorder: '1px solid #808080',

                timeColor: '#000000',
                durationColor: '#535353'
            }
        },
        clip: {
            autoBuffering: true,
            autoPlay: false
        }
    });
});
