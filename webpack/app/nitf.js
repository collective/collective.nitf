import './nitf.less';
import './nitf_icon.png';
import './tile-nitf.png';

class SlideShow {
  constructor(el) {
    this.$el = $(el);
    this.proportion = 3 / 2;
    this.bind_events();
    this.fix_image_size();
  }

  $(selector) {
    return $(selector, this.$el);
  }

  bind_events() {
    this.$('.cycle-player').on('cycle-next cycle-prev', $.proxy(this.sync_slideshows, this));
    this.$('.cycle-carrossel .thumb-itens').on('click', $.proxy(this.thumbs_click, this));
  }

  fix_image_size() {
    var max_height, max_width, i, len, ref, img, $player, $img;

    // Calc max_with and max_height
    $player = this.$('.cycle-player');
    max_width = $player.width();
    max_height = max_width / this.proportion;
    // Calc max_with and max_height

    // Update properties when necessary
    ref = this.$('.cycle-player img');
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
  }

  sync_slideshows(e, opts) {
    var index, $player, $slideshows;
    $slideshows = this.$('.cycle-slideshow');
    $slideshows.cycle('goto', opts.currSlide);
  }

  thumbs_click(e) {
    var index, $thumbs, $slideshows;
    e.preventDefault();
    $thumbs = this.$('.cycle-carrossel');
    index = $thumbs.data('cycle.API').getSlideIndex(this);
    $slideshows = this.$('.cycle-slideshow');
    $slideshows.cycle('goto', index);
  }
}

$(window).load(() => {
  if ($('.portaltype-collective-nitf-content.template-slideshow_view').length > 0) {
    new SlideShow($('.slideshow-container'));
  }
});

module.exports = SlideShow;
