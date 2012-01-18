function collapseSections() {
  //we are in edit or add nitf content
  if($("body").hasClass("template-collective.nitf.content") || 
    $("body").hasClass("portaltype-collective-nitf-content")) {
    $("fieldset legend").click(function() {
      //add a tab-collapser tab that wraps all the fields
      if($(".tab-collapser",$(this).parent()).length === 0) {
        $(".field",$(this).parent()).wrapAll("<span class='tab-collapser'>");
        //hide the tab-collapser
        $(".tab-collapser" ,$(this).parent()).slideToggle();
      } else {
        //show the fields again and remove the tab-collapser (unwrap the fields)
        //this is done to avoid some compatibility issues with other plone's javascripts
        $(".tab-collapser" ,$(this).parent()).slideToggle();
        $(".tab-collapser" ,$(this).parent()).replaceWith(function() { return $(this).contents(); });
      }
    })
    $("fieldset legend").css("cursor", "pointer");
  } 
}

$(document).ready(function() {
  collapseSections();
});