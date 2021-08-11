# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AttendanceRectification(models.Model):
    _inherit = 'hr.attendance.rectification'
    
    
    
    def action_send_rectification_data(self):
        for rectify in self:
            APPLICANT_ID = rectify.employee_id.barcode.lstrip("0")
            APPROVER_ID = leave.employee_id.manager_id.barcode.lstrip("0")
            APP_DATE = leave.employee_id.company_id.segment1
            APP_REMARKS = leave.employee_id.barcode.lstrip("0")
            CMTMT_DATE = leave.create_date
            CMTMT_DATE_TO = leave.request_date_from
            CMTMT_STATUS = leave.employee_id.barcode.lstrip("0")
            CMTMT_TIME_FROM = leave.request_date_to
            CMTMT_TIME_TO = False
            CMTMT_TYPE =  leave.employee_id.manager_id.barcode.lstrip("0")
            IO_TIME =  False
            POST = 0
            PREVIOUS_DAY_NIGHT_SHIFT = 0
            REASON_CODE = ' '
            REMARKS = leave.number_of_days
            REQ_DATE = leave.leave_category  
            REQ_ID = 'A'
            
            conn = cx_Oracle.connect('xx_odoo/xxodoo123$@//10.8.7.153:1524/test3')
            cur = conn.cursor()
            statement = 'insert into ODOO_HR_COMMITMENT_SLIP_HEADER(ACTIVITY_ID,APPROVED_BY, APPROVED_DATE, COMPANY_ID,CREATED_BY,CREATION_DATE,EFFECTIVE_DATE,EMPLOYEE_ID,END_DATE, END_TIME, FORWARDED_TO, HR_ACTION_DATE, HR_APPROVAL_FLG, HR_APPROVAL_ID, HR_APPROVAL_REQUIRED, LEAVE_DAYS, LEAVE_DAY_TYPE, LEAVE_STATUS, LEAVE_TYPE_ID, REASON, REMARKS, START_DATE, START_TIME, TRANSACTION_ID,YEAR) values(: 2,:3,: 4,:5,: 6,:7,: 8,:9,: 10,:11,: 12,:13,: 14,:15,: 16,:17,: 18,:19,: 20,:21,: 22,:23,: 24,:25,:26)'
            cur.execute(statement, (
            ACTIVITY_ID,APPROVED_BY, APPROVED_DATE, COMPANY_ID,CREATED_BY,CREATION_DATE,EFFECTIVE_DATE,EMPLOYEE_ID,END_DATE, END_TIME, FORWARDED_TO, HR_ACTION_DATE, HR_APPROVAL_FLG, HR_APPROVAL_ID, HR_APPROVAL_REQUIRED, LEAVE_DAYS, LEAVE_DAY_TYPE, LEAVE_STATUS, LEAVE_TYPE_ID, REASON, REMARKS, START_DATE, START_TIME, TRANSACTION_ID,YEAR))
            conn.commit()
                        
            leave.action_send_holiday_line_data()            
                        


    def action_send_holiday_line_data(self):
        for leave in self:
            if leave.number_of_days >=  1:            
                for day in range(leave.number_of_days):            
                    EMPLOYEE_ID = leave.employee_id.barcode.lstrip("0")
                    ENABLED = 'Y'
                    LEAVE_DATE = leave.request_date_from
                    LEAVE_DAYS = -1
                    LEAVE_DAY_TYPE = leave.leave_category
                    if leave.leave_category == 'day':
                        LEAVE_DAY_TYPE = 'Full Day'  
                    if leave.leave_category == 'half_day':
                        LEAVE_DAY_TYPE = 'First Half'              
                    LTD_ID = leave.id 
                    TRANSACTION_ID = leave.id
                    YEAR = fields.date.today().year            
                    conn = cx_Oracle.connect('xx_odoo/xxodoo123$@//10.8.7.153:1524/test3')
                    cur = conn.cursor()
                    statement = 'insert into ODOO_LEAVE_TRANSACTION(EMPLOYEE_ID,ENABLED, LEAVE_DATE, LEAVE_DAYS,LEAVE_DAY_TYPE,LTD_ID,TRANSACTION_ID,YEAR) values(: 2,:3,: 4,:5,: 6,:7,: 8,:9)'
                    cur.execute(statement, (
                    EMPLOYEE_ID,ENABLED, LEAVE_DATE, LEAVE_DAYS,LEAVE_DAY_TYPE,LTD_ID,TRANSACTION_ID,YEAR))
                    conn.commit()
        else:
             EMPLOYEE_ID = leave.employee_id.barcode.lstrip("0")
             ENABLED = 'Y'
             LEAVE_DATE = leave.request_date_from
             LEAVE_DAYS = -0.5
             LEAVE_DAY_TYPE = leave.leave_category
             if leave.leave_category == 'day':
                 LEAVE_DAY_TYPE = 'Full Day'  
             if leave.leave_category == 'half_day':
                 LEAVE_DAY_TYPE = 'First Half'              
             LTD_ID = leave.id 
             TRANSACTION_ID = leave.id
             YEAR = fields.date.today().year            
             conn = cx_Oracle.connect('xx_odoo/xxodoo123$@//10.8.7.153:1524/test3')
             cur = conn.cursor()
             statement = 'insert into ODOO_LEAVE_TRANSACTION(EMPLOYEE_ID,ENABLED, LEAVE_DATE, LEAVE_DAYS,LEAVE_DAY_TYPE,LTD_ID,TRANSACTION_ID,YEAR) values(: 2,:3,: 4,:5,: 6,:7,: 8,:9)'
             cur.execute(statement, (
                EMPLOYEE_ID,ENABLED, LEAVE_DATE, LEAVE_DAYS,LEAVE_DAY_TYPE,LTD_ID,TRANSACTION_ID,YEAR))
             conn.commit()


