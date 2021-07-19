# -*- coding: utf-8 -*-
from odoo import http

# class DeOdooDebranding(http.Controller):
#     @http.route('/de_odoo_debranding/de_odoo_debranding/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_odoo_debranding/de_odoo_debranding/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_odoo_debranding.listing', {
#             'root': '/de_odoo_debranding/de_odoo_debranding',
#             'objects': http.request.env['de_odoo_debranding.de_odoo_debranding'].search([]),
#         })

#     @http.route('/de_odoo_debranding/de_odoo_debranding/objects/<model("de_odoo_debranding.de_odoo_debranding"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_odoo_debranding.object', {
#             'object': obj
#         })