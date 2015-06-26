(function ($) {
  "use strict";

  var SlideShow = (function() {
    function SlideShow(el) {
      var self = this;
      self.$el = $(el);
      self.proportion = 3 / 2;
      self.bind_events();
      self.fix_image_size();
    }
    SlideShow.prototype.$ = function(selector) {
      var self = this;
      return $(selector, self.$el);
    };
    SlideShow.prototype.bind_events = function() {
      var self = this;
      self.$('.cycle-player').on('cycle-next cycle-prev', self, self.sync_slideshows);
      self.$('.cycle-carrossel .thumb-itens').on('click', self, self.thumbs_click);
    };
    SlideShow.prototype.fix_image_size = function() {
      var self, max_height, max_width, i, len, ref, img, $player, $img;
      self = this;

      // Calc max_with and max_height
      $player = self.$('.cycle-player');
      max_width = $player.width();
      max_height = max_width / self.proportion;
      // Calc max_with and max_height

      // Update properties when necessary
      ref = self.$('.cycle-player img');
      for (i = 0, len = ref.length; i < len; i++) {
        img = ref[i];
        $img = $(img);
        if ($img.height() > $img.width()) {
          $img.css('width', 'auto');
          $img.height(max_height);
        } else {
          $img.width(max_width);
          $img.height(max_height);
        }
      }
    };

    SlideShow.prototype.sync_slideshows = function(e, opts) {
      var self, index, $player, $slideshows;
      self = e.data;
      $slideshows = self.$('.cycle-slideshow');
      $slideshows.cycle('goto', opts.currSlide);
    };

    SlideShow.prototype.thumbs_click = function(e) {
      var self, index, $thumbs, $slideshows;
      self = e.data;
      e.preventDefault();
      $thumbs = self.$('.cycle-carrossel');
      index = $thumbs.data('cycle.API').getSlideIndex(this);
      $slideshows = self.$('.cycle-slideshow');
      $slideshows.cycle('goto', index);
    };
    return SlideShow;
  })();

  $(document).ready(function () {
    // If this is a NITF content with an image
    var nitf_view = $('body.portaltype-collective-nitf-content.template-view').length > 0;
    var nitf_with_image = nitf_view && $('.newsImageContainer').length > 0;
    var slideshow = $('body.portaltype-collective-nitf-content.template-slideshow').length > 0;
    if (nitf_with_image) {
      // Turn image link into something special
      var link = $('#parent-fieldname-image');
      // Add a magnify icon over the image
      link.append('<span class="magnify"></span>');
      // For mobile devices, link will open slideshow
      if (/Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent)) {
        link.attr('href', link.attr('href').replace('@@slideshow', '@@slideshow?ajax_include_head=1&amp;ajax_load=1'));
      } else {
        // For other devices open a slideshow in an overlay
        link.prepOverlay({
          subtype: 'ajax',
          filter: '#content > *',
          width: ($(document).width() * 0.95) + 'px',
          config: {
            onLoad: function (e) {
              // Start cycle2
              $('.cycle-slideshow').cycle();
              new SlideShow($('.slideshow-container'));
            }
          }
        });
      }
    } else if (slideshow) {
      // For slideshow template, hide address bar after page load
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
        new SlideShow($('.slideshow-container'));
      });
      window.addEventListener("orientationchange", hideAddressBar);
    }
  });
  $(window).load(function() {
    if ($('body.portaltype-collective-nitf-content.template-slideshow_view').length > 0) {
      new SlideShow($('.slideshow-container'));
    }
  });
})(jQuery);
