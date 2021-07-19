# -*- coding: utf-8 -*-
from odoo import http

# class DeWebsiteProductCarouselExtend(http.Controller):
#     @http.route('/de_website_product_carousel_extend/de_website_product_carousel_extend/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_website_product_carousel_extend/de_website_product_carousel_extend/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_website_product_carousel_extend.listing', {
#             'root': '/de_website_product_carousel_extend/de_website_product_carousel_extend',
#             'objects': http.request.env['de_website_product_carousel_extend.de_website_product_carousel_extend'].search([]),
#         })

#     @http.route('/de_website_product_carousel_extend/de_website_product_carousel_extend/objects/<model("de_website_product_carousel_extend.de_website_product_carousel_extend"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_website_product_carousel_extend.object', {
#             'object': obj
#         })