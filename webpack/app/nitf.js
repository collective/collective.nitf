import './nitf.less';
import './nitf_icon.png';
import './tile-nitf.png';

import Swiper from 'swiper/bundle';

$(window).load(() => {
  if ($('.portaltype-collective-nitf-content.template-slideshow_view').length > 0) {
    new Swiper('.swiper-container', {
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
      pagination: {
        el: '.swiper-pagination',
        type: 'bullets',
        clickable: true,
      },
      autoplay: {
        delay: 5500,
      }, 
    });
  }
});
