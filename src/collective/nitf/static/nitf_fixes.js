
function collapseSections() {
  //we are in edit or add nitf content
  if($("body").hasClass("template-collective.nitf.content")  || 
    $("body").hasClass("portaltype-collective-nitf-content") && $("body").hasClass("template-edit")) {
      $("fieldset").each(function(index) {
       if(index != 0) {
         $(this).collapse({ closed : true });
       } else {
         $(this).collapse();
       }
     });
   } 
}

$(document).ready(function() {
  collapseSections();
});