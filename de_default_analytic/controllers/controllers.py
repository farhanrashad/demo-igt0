# -*- coding: utf-8 -*-
from odoo import http

# class DeDefaultAnalytic(http.Controller):
#     @http.route('/de_default_analytic/de_default_analytic/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_default_analytic/de_default_analytic/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_default_analytic.listing', {
#             'root': '/de_default_analytic/de_default_analytic',
#             'objects': http.request.env['de_default_analytic.de_default_analytic'].search([]),
#         })

#     @http.route('/de_default_analytic/de_default_analytic/objects/<model("de_default_analytic.de_default_analytic"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_default_analytic.object', {
#             'object': obj
#         })