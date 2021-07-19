# -*- coding: utf-8 -*-
from odoo import http

# class DeCarouselTieredPricing(http.Controller):
#     @http.route('/de_carousel_tiered_pricing/de_carousel_tiered_pricing/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_carousel_tiered_pricing/de_carousel_tiered_pricing/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_carousel_tiered_pricing.listing', {
#             'root': '/de_carousel_tiered_pricing/de_carousel_tiered_pricing',
#             'objects': http.request.env['de_carousel_tiered_pricing.de_carousel_tiered_pricing'].search([]),
#         })

#     @http.route('/de_carousel_tiered_pricing/de_carousel_tiered_pricing/objects/<model("de_carousel_tiered_pricing.de_carousel_tiered_pricing"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_carousel_tiered_pricing.object', {
#             'object': obj
#         })