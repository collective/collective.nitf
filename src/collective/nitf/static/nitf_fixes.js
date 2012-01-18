function collapseSections() {
  if($("body").hasClass("template-collective.nitf.content") || 
    $("body").hasClass("portaltype-collective-nitf-content")) {
      var i = 0;
      var fieldset = $("fieldset")
      for(i=0; i<fieldset.length; i++) {
        $(".field" ,fieldset[i]).wrapAll("<span class='tab-collapser'>")
      }
      $("fieldset legend").click(function() {
        $(".tab-collapser" ,$(this).parent()).slideToggle();
      })
      $("fieldset legend").css("cursor", "pointer");
  } 
}

$(document).ready(function() {
  collapseSections();
});