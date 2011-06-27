jq(function($) {
    $(".thumbnails").scrollable();
    $(".items img[src].media-image").prepOverlay({
        subtype:'image',
        urlmatch: '/image_.+$',
        urlreplace: '/image_large',
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
