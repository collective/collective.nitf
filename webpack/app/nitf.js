import './nitf.less';
import './nitf_icon.png';
import './tile-nitf.png';

class SlideShow {
  constructor(el) {
    this.$el = $(el);
    this.proportion = 3 / 2;
    this.bind_events();
  }

  $(selector) {
    return $(selector, this.$el);
  }

  bind_events() {
    this.$('.cycle-player').on('cycle-next cycle-prev', $.proxy(this.sync_slideshows, this));
    this.$('.cycle-carrossel .thumb-itens').on('click', $.proxy(this.thumbs_click, this));
  }

  sync_slideshows(e, opts) {
    var index, $player, $slideshows;
    $slideshows = this.$('.cycle-slideshow');
    $slideshows.cycle('goto', opts.currSlide);
  }

  thumbs_click(e) {
    var index, $thumbs, api, $slideshows;
    e.preventDefault();
    $thumbs = this.$('.cycle-carrossel');
    api = $thumbs.data('cycle.API');
    index = api.getSlideIndex(e.target.parentElement);
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
