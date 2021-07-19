odoo.define('website_product_carousel.carousel_frontend', function(require) {
    "use strict";

    var core = require('web.core');
    var ajax = require('web.ajax');
    var website = require('website.website');
    var sAnimation = require('website.content.snippets.animation');

    var _t = core._t;
    var qweb = core.qweb;
    var page_widgets = {};
    sAnimation.registry.js_get_objects=sAnimation.Class.extend({selector:".js_get_objects",start:function(){this.redraw()},destroy:function(){this.clean(),this._super.apply(this,arguments)},redraw:function(t){this.clean(t),this.build(t)},clean:function(t){this.$target.empty()},carousel_view:function(t){$(".owl-carousel").owlCarousel({loop:!0,margin:10,responsiveClass:!0,dots:!1,nav:!0,pagination:!1,autoplay:!1,responsive:{768:{items:2},979:{items:2},479:{items:1},320:{items:1},1199:{items:this.$target.data("objects_in_slide")}}})},build:function(t){var e=this,i=e.$target.data("objects_limit"),a=e.$target.data("filter_by_filter_id"),n=e.$target.data("objects_in_slide");e.$target.attr("contentEditable",!1),n||(n=3),i||(i=6),ajax.jsonRpc("/render_product_carousel_slider/product_slider/","call",{filter_id:a,objects_in_slide:n,limit:i}).then(function(t){$(t).appendTo(e.$target),e.carousel_view(t)}).then(function(){e.loading(t)}).fail(function(t){})},loading:function(t){}});
});
