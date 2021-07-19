# -*- coding: utf-8 -*-
from odoo import http

# class DeVariantType(http.Controller):
#     @http.route('/de_variant_type/de_variant_type/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_variant_type/de_variant_type/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_variant_type.listing', {
#             'root': '/de_variant_type/de_variant_type',
#             'objects': http.request.env['de_variant_type.de_variant_type'].search([]),
#         })

#     @http.route('/de_variant_type/de_variant_type/objects/<model("de_variant_type.de_variant_type"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_variant_type.object', {
#             'object': obj
#         })