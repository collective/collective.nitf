function collapseSections() {
  //we are in edit or add nitf content
  if($("body").hasClass("template-collective.nitf.content") || 
    $("body").hasClass("portaltype-collective-nitf-content")) {
    $("fieldset legend").click(function() {
      //add a tab-collapser tab that wraps all the fields
      if($(".tab-collapser",$(this).parent()).length === 0) {
        $(".field",$(this).parent()).wrapAll("<span class='tab-collapser'>");
        //hide the tab-collapser
        var that = this;
        $(".tab-collapser" ,$(this).parent()).slideToggle(function() {
            $(that).css("background", 
              "url('++resource++collective.nitf/images/arrows.png') no-repeat \
              scroll 2px -28px transparent");
        });
      } else {
        //show the fields again and remove the tab-collapser (unwrap the fields)
        //this is done to avoid some compatibility issues with other plone's javascripts
        var that = this;
        
        $(".tab-collapser" ,$(this).parent()).slideToggle(function () {
          $(that).css("background", 
            "url('++resource++collective.nitf/images/arrows.png') no-repeat \
            scroll 2px 10px transparent");
          $(".tab-collapser" ,$(that).parent()).replaceWith(function() {
            return $(this).contents(); 
          });
        });
      }
    })
    $("fieldset legend").css("cursor", "pointer");
    $("fieldset legend").each(function(index) {
      if(index != 0) {
        if($(".tab-collapser",$(this).parent()).length === 0) {
          $(".field",$(this).parent()).wrapAll("<span class='tab-collapser'>");
          $(".tab-collapser",$(this).parent()).css("display", "none");
          $(this).css("background", 
            "url('++resource++collective.nitf/images/arrows.png') no-repeat \
            scroll 2px -28px transparent");
          $(this).css("padding-left", "20px");
        }
      } else {
          $(this).css("background", 
            "url('++resource++collective.nitf/images/arrows.png') no-repeat \
            scroll 2px 10px transparent");
          $(this).css("padding-left", "20px");
      }
    })
  } 
}

$(document).ready(function() {
  collapseSections();
});