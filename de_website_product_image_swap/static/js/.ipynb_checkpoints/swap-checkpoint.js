$(document).ready(function () {
$('.oe_product_image').on('mouseenter', function() {
    $(this).addClass('active').siblings().removeClass('active');
});
});
$(document).ready(function(){
	$(".oe_product_secondary_image").hide();
  $(".oe_product_image").mouseenter(function(){
  if($(this).find('.oe_product_secondary_image').length){
  	$(this).find('.oe_product_primary_image').hide();
    $(this).find('.oe_product_secondary_image').show();
    }
  });
  $(".oe_product_image").mouseleave(function(){
  if($(this).find('.oe_product_secondary_image').length){
    $(this).find('.oe_product_secondary_image').hide();
    $(this).find('.oe_product_primary_image').show();
    }
  });
});