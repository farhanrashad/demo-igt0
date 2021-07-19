# -*- coding: utf-8 -*-
from odoo import http

# class DeWebsiteHidePrice(http.Controller):
#     @http.route('/de_website_hide_price/de_website_hide_price/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_website_hide_price/de_website_hide_price/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_website_hide_price.listing', {
#             'root': '/de_website_hide_price/de_website_hide_price',
#             'objects': http.request.env['de_website_hide_price.de_website_hide_price'].search([]),
#         })

#     @http.route('/de_website_hide_price/de_website_hide_price/objects/<model("de_website_hide_price.de_website_hide_price"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_website_hide_price.object', {
#             'object': obj
#         })