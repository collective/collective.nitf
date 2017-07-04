import './nitf.less';
import './nitf_icon.png';
import './tile-nitf.png';

$(window).load(() => {
  if ($('.portaltype-collective-nitf-content.template-slideshow_view').length > 0) {
    new Swiper('.swiper-container', {
      nextButton: '.swiper-button-next',
      prevButton: '.swiper-button-prev',
      pagination: '.swiper-pagination',
      paginationClickable: true,
      autoplay: 5500
    });
  }
});

module.exports = SlideShow;
