(function($) {

  $.fn.charCount = function(options){
    
    // default configuration properties
    var defaults = {
      allowed: 140,
      optimal: 40,
      warning: 25,
      css: 'counter',
      counterElement: 'span',
      cssOptimal: 'optimal',
      cssWarning: 'warning',
      cssExceeded: 'exceeded',
      counterText: ''
    };
      
    var options = $.extend(defaults, options);
    
    function calculate(obj){
      var count = $(obj).val().length;
      var available = options.allowed - count;
      if (available <= options.optimal && available >=0) {
        $(obj).next().addClass(options.cssOptimal);
      } else {
        $(obj).next().removeClass(options.cssOptimal);
      }

      if(available <= options.warning && available >= 0){
        $(obj).next().addClass(options.cssWarning);
      } else {
        $(obj).next().removeClass(options.cssWarning);
      }

      if(available < 0){
        $(obj).next().addClass(options.cssExceeded);
      } else {
        $(obj).next().removeClass(options.cssExceeded);
      }
      
      $(obj).next().html(options.counterText + available);
    };
        
    this.each(function() {
      $(this).after('<'+ options.counterElement +' class="' + options.css + '">'+ options.counterText +'</'+ options.counterElement +'>');
      calculate(this);
      $(this).keyup(function(){calculate(this)});
      $(this).change(function(){calculate(this)});
    });
    
  };

})(jQuery);

