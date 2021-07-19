# -*- coding: utf-8 -*-
from odoo import http

# class DeInvoiceReportEnhancement(http.Controller):
#     @http.route('/de_invoice_report_enhancement/de_invoice_report_enhancement/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_invoice_report_enhancement/de_invoice_report_enhancement/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_invoice_report_enhancement.listing', {
#             'root': '/de_invoice_report_enhancement/de_invoice_report_enhancement',
#             'objects': http.request.env['de_invoice_report_enhancement.de_invoice_report_enhancement'].search([]),
#         })

#     @http.route('/de_invoice_report_enhancement/de_invoice_report_enhancement/objects/<model("de_invoice_report_enhancement.de_invoice_report_enhancement"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_invoice_report_enhancement.object', {
#             'object': obj
#         })