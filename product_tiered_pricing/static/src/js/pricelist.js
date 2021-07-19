odoo.define('product_tiered_pricing.pricelist_js', function(require) {
    "use strict";

    require('web.dom_ready');
    var base = require("web_editor.base");
    var ajax = require('web.ajax');
    var utils = require('web.utils');
    var core = require('web.core');
    var config = require('web.config');
    // var VariantMixin = require('sale.VariantMixin');
    require("website.content.zoomodoo");
    var _t = core._t;


    function CusgetSelectedVariantValues ($container) {
        var values = [];
        var unchangedValues = $container
            .find('div.oe_unchanged_value_ids')
            .data('unchanged_value_ids') || [];

        var variantsValuesSelectors = [
            'input.js_variant_change:checked',
            'select.js_variant_change'
        ];
        _.each($container.find(variantsValuesSelectors.join(', ')), function (el) {
            values.push(+$(el).val());
        });

        return values.concat(unchangedValues);
    }
    if(!$('.oe_website_sale').length) {
        return $.Deferred().reject("DOM doesn't contain '.oe_website_sale'");
    }

    $(document).ready(function() {
        var product = $('.product_id').attr('value');
        if (product) {
            var attribute = ajax.jsonRpc("/shop/product_pricelist", 'call', {
                'product': product,
            }).then(function(res) {
                $('.product_pricelist').html(res);
                return true;
            });
            return true;
        }
    });


    // $('.oe_website_sale').each(function() {
    //     var oe_website_sale = this;

    //     $(oe_website_sale).on('change', 'input.js_variant_change, select.js_variant_change, ul[data-attribute_value_ids]', function (ev) {
    //         var product_id = $('.product_id').attr('value');
    //         console.log('------------product_id------',product_id)
    //         if (product_id) {
    //             var attributes = ajax.jsonRpc("/shop/product_pricelist", 'call', {
    //                 'product': product_id,
    //             }).then(function(res) {
    //                 $('.product_pricelist').html(res);
    //                 return true;
    //             });
    //             return true;
    //         }
    //     });

    // });

    setTimeout(function() {
        $('.oe_website_sale').on('change', 'ul[data-attribute_exclusions]', function(ev) {
            var self = this
            setTimeout(function() {
                var $parent = $(ev.target).closest('.js_product');
                var combination = CusgetSelectedVariantValues($parent);
                console.log('combinationcombinationcombination---',combination)
                var product_id = $('input.product_id').val();
                if (product_id) {
                    var attributes = ajax.jsonRpc("/shop/product_pricelist", 'call', {
                    'product': product_id,
                    'combination' : combination,
                }).then(function(res) {
                    $('.product_pricelist').html(res);
                    return true;
                });
                return true;
                }
            }, 500)
        });
   } ,500)




});
