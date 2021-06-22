# -*- coding: utf-8 -*-
# from odoo import http


# class DeProductSerial(http.Controller):
#     @http.route('/de_product_serial/de_product_serial/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_product_serial/de_product_serial/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_product_serial.listing', {
#             'root': '/de_product_serial/de_product_serial',
#             'objects': http.request.env['de_product_serial.de_product_serial'].search([]),
#         })

#     @http.route('/de_product_serial/de_product_serial/objects/<model("de_product_serial.de_product_serial"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_product_serial.object', {
#             'object': obj
#         })
