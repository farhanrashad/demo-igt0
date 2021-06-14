# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AttendanceGeolocation(models.TransientModel):
    _name = 'de.attendance.location'
    name = fields.Char(default='Google Maps Search')
    department_id = fields.Many2one('hr.department', string='Department')
    job_id = fields.Many2one('hr.job', string='Job Position')
    employee_ids = fields.Many2many('hr.employee', 'de_attendance_loc_id_rel', 'emp_id', 'de_att_id', string='Employees')
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    map_id = fields.Char()

    def get_lat_lng_of_employee(self, emp_id, from_date, to_date):
        employee_attendances = self.env['hr.attendance'].search([('employee_id', '=', emp_id), ('check_in', '>=', from_date),
                                                                 ('check_out', '<=', to_date)])
        lat_lngs = []
        for atn in employee_attendances:
            if atn.chk_in_lat and atn.chk_in_lng:
                lat_lngs.append([atn.chk_in_lat, atn.chk_in_lng, str(atn.employee_id.name), emp_id])
            if atn.chk_out_lat and atn.chk_out_lng:
                lat_lngs.append([atn.chk_out_lat, atn.chk_out_lng, str(atn.employee_id.name), emp_id])
        return lat_lngs

    def search_employees(self):
        atn_data = []
        for employee in self.employee_ids:
            atn_data.append(self.get_lat_lng_of_employee(employee.id, self.from_date, self.to_date))
        self.map_id = atn_data
        print(atn_data)
        return

    def clear_fields(self):
        self.department_id = self.job_id = self.employee_ids = self.from_date = self.to_date = False
        return


class HrAttendance(models.Model):
    _name = "hr.attendance"
    _inherit = 'hr.attendance'

    check_in_msg = fields.Char('Check In Message')
    check_out_msg = fields.Char('Check Out Message')
    chk_in_link = fields.Char('Open Check-in Location in Google Maps')
    chk_out_link = fields.Char('Open Check-out Location in Google Maps')

    chk_in_lat = fields.Char()
    chk_in_lng = fields.Char()

    chk_out_lat = fields.Char()
    chk_out_lng = fields.Char()


class HrEmployee(models.Model):
    _inherit = "hr.employee"
    _name = "hr.employee"

    check_in_msg = fields.Char('Check in message')
    check_out_msg = fields.Char('Check out message')
    lat_lng_lnk = fields.Char()
    lat = fields.Char('Lat')
    lng = fields.Char('Lng')

    def _attendance_action_change(self):
        attendance = super(HrEmployee, self)._attendance_action_change()
        if self.check_in_msg:
            attendance.check_in_msg = self.check_in_msg
            attendance.chk_in_link = self.lat_lng_lnk
            attendance.chk_in_lat = self.lat
            attendance.chk_in_lng = self.lng
        if self.check_out_msg:
            attendance.check_out_msg = self.check_out_msg
            attendance.chk_out_link = self.lat_lng_lnk
            attendance.chk_out_lat = self.lat
            attendance.chk_out_lng = self.lng
        return attendance

    def update_attendance_data(self, state=False, check_in_out_msg=False, lat=False, lng=False):
        if not check_in_out_msg:
            check_in_out_msg = 'no_msg'
        if lat and lng:
            self.lat_lng_lnk = "https://maps.google.com/maps?q={},{}".format(lat, lng)
            self.lat = lat
            self.lng = lng
        else:
            self.lat_lng_lnk = ""
        if state == 'checked_out':
            self.check_in_msg = check_in_out_msg
            self.check_out_msg = False
        elif state == 'checked_in':
            self.check_out_msg = check_in_out_msg
            self.check_in_msg = False
        else:
            self.check_out_msg = False
            self.check_in_msg = False
            return
        return 'Success'
