# -*- coding: utf-8 -*-
from odoo import http

# class DeWebsiteHeader(http.Controller):
#     @http.route('/de_website_header/de_website_header/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_website_header/de_website_header/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_website_header.listing', {
#             'root': '/de_website_header/de_website_header',
#             'objects': http.request.env['de_website_header.de_website_header'].search([]),
#         })

#     @http.route('/de_website_header/de_website_header/objects/<model("de_website_header.de_website_header"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_website_header.object', {
#             'object': obj
#         })