# -*- coding: utf-8 -*-
from odoo import http

# class DePricelistCopyItems(http.Controller):
#     @http.route('/de_pricelist_copy_items/de_pricelist_copy_items/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_pricelist_copy_items/de_pricelist_copy_items/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_pricelist_copy_items.listing', {
#             'root': '/de_pricelist_copy_items/de_pricelist_copy_items',
#             'objects': http.request.env['de_pricelist_copy_items.de_pricelist_copy_items'].search([]),
#         })

#     @http.route('/de_pricelist_copy_items/de_pricelist_copy_items/objects/<model("de_pricelist_copy_items.de_pricelist_copy_items"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_pricelist_copy_items.object', {
#             'object': obj
#         })