import json

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime


class PayslipBatch(models.TransientModel):
    _name = "pay.slip.batch"
    _description = "Payslip Batch Wizard"

    contract_type = fields.Selection([('local', 'Local'),('expats', 'Expats')], string='Contract Type')
    doe = fields.Date(string='Date of Execution')
    debit_ac_no = fields.Float(string='Debit A/C No.')
    currency = fields.Many2one('res.currency', string='Currency')
    batch_id = fields.Many2one('hr.payslip.run')
    date_today = fields.Date(default=datetime.today())
    
    def print_report(self):
        print('ID: ', self.id)
        datas = {
            'contract_type': self.contract_type,
            'doe': self.doe,
            'debit_ac_no': self.debit_ac_no,
            'currency': self.currency,
            'id': self.batch_id.id,
        }
        return self.env.ref('de_payslip_batch_report.payslip_batch_report').report_action(self, data=datas)
    
    
    
    def print_txt_report(self):
        data_val = ''
        vals = ''
        filename = "readme-odoo.txt"
        file_ = open(filename + str(), 'w')
        payslips = self.env['hr.payslip'].search([('payslip_run_id', '=', self.batch_id.id)])
        for payslip in payslips:
            line = 'TT' + '  ' + str(payslip.number) + '        ' + str(self.debit_ac_no) + '  ' + str(self.currency.name) + str(self.date_today) + '   ' + str(payslip.net_wage) + '         ' + str(payslip.employee_id.bank_account_id.acc_number) + '                    ' + str(payslip.employee_id.address_id.street) + str(payslip.employee_id.address_id.street2) + str(payslip.employee_id.address_id.city) + ' ' + str(payslip.employee_id.address_id.country_id.name) + '                              ' + str(payslip.employee_id.bank_account_id.bank_id.name) + '                      ' + str(payslip.employee_id.bank_account_id.bank_id.street) + "\n" + str(payslip.name) + "\n" + str(payslip.employee_id.work_email)
            data_val = str(line)
        file_.write(data_val)
        file_.close()
 