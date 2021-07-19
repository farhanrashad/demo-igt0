# -*- coding: utf-8 -*-
from odoo import http

# class DeWebsieShowAllPrices(http.Controller):
#     @http.route('/de_websie_show_all_prices/de_websie_show_all_prices/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_websie_show_all_prices/de_websie_show_all_prices/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_websie_show_all_prices.listing', {
#             'root': '/de_websie_show_all_prices/de_websie_show_all_prices',
#             'objects': http.request.env['de_websie_show_all_prices.de_websie_show_all_prices'].search([]),
#         })

#     @http.route('/de_websie_show_all_prices/de_websie_show_all_prices/objects/<model("de_websie_show_all_prices.de_websie_show_all_prices"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_websie_show_all_prices.object', {
#             'object': obj
#         })