# -*- coding: utf-8 -*-
from odoo import http

# class DeWebsiteProductImageSwap(http.Controller):
#     @http.route('/de_website_product_image_swap/de_website_product_image_swap/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_website_product_image_swap/de_website_product_image_swap/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_website_product_image_swap.listing', {
#             'root': '/de_website_product_image_swap/de_website_product_image_swap',
#             'objects': http.request.env['de_website_product_image_swap.de_website_product_image_swap'].search([]),
#         })

#     @http.route('/de_website_product_image_swap/de_website_product_image_swap/objects/<model("de_website_product_image_swap.de_website_product_image_swap"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_website_product_image_swap.object', {
#             'object': obj
#         })