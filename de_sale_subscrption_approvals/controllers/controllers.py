# -*- coding: utf-8 -*-
# from odoo import http


# class DeSaleSubscrptionApprovals(http.Controller):
#     @http.route('/de_sale_subscrption_approvals/de_sale_subscrption_approvals/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_sale_subscrption_approvals/de_sale_subscrption_approvals/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_sale_subscrption_approvals.listing', {
#             'root': '/de_sale_subscrption_approvals/de_sale_subscrption_approvals',
#             'objects': http.request.env['de_sale_subscrption_approvals.de_sale_subscrption_approvals'].search([]),
#         })

#     @http.route('/de_sale_subscrption_approvals/de_sale_subscrption_approvals/objects/<model("de_sale_subscrption_approvals.de_sale_subscrption_approvals"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_sale_subscrption_approvals.object', {
#             'object': obj
#         })
