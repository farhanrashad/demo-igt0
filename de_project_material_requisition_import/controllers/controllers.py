# -*- coding: utf-8 -*-
# from odoo import http


# class DeProjectMaterialRequisitionImport(http.Controller):
#     @http.route('/de_project_material_requisition_import/de_project_material_requisition_import/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_project_material_requisition_import/de_project_material_requisition_import/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_project_material_requisition_import.listing', {
#             'root': '/de_project_material_requisition_import/de_project_material_requisition_import',
#             'objects': http.request.env['de_project_material_requisition_import.de_project_material_requisition_import'].search([]),
#         })

#     @http.route('/de_project_material_requisition_import/de_project_material_requisition_import/objects/<model("de_project_material_requisition_import.de_project_material_requisition_import"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_project_material_requisition_import.object', {
#             'object': obj
#         })
