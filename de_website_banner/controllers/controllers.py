# -*- coding: utf-8 -*-
from odoo import http

# class DeWebsiteBanner(http.Controller):
#     @http.route('/de_website_banner/de_website_banner/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_website_banner/de_website_banner/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_website_banner.listing', {
#             'root': '/de_website_banner/de_website_banner',
#             'objects': http.request.env['de_website_banner.de_website_banner'].search([]),
#         })

#     @http.route('/de_website_banner/de_website_banner/objects/<model("de_website_banner.de_website_banner"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_website_banner.object', {
#             'object': obj
#         })