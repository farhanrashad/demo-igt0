# -*- coding: utf-8 -*-
# from odoo import http


# class DeAttendanceLocation(http.Controller):
#     @http.route('/de_attendance_location/de_attendance_location/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/de_attendance_location/de_attendance_location/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('de_attendance_location.listing', {
#             'root': '/de_attendance_location/de_attendance_location',
#             'objects': http.request.env['de_attendance_location.de_attendance_location'].search([]),
#         })

#     @http.route('/de_attendance_location/de_attendance_location/objects/<model("de_attendance_location.de_attendance_location"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('de_attendance_location.object', {
#             'object': obj
#         })
