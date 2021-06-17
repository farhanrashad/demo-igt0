from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PayslipBatch(models.TransientModel):
    _name = "pay.slip.batch"
    _description = "Payslip Batch Wizard"

    contract_type = fields.Selection([('local', 'Local'),('expats', 'Expats')], string='Contract Type')
    doe = fields.Date(string='Date of Execution')
    debit_ac_no = fields.Float(string='Debit A/C No.')
    currency = fields.Many2one('res.currency', string='Currency')
    
    def print_report(self):
        print('ID: ', self.id)
        id = self.id
        data = {
            'id': id
        }
        return self.env.ref('de_payslip_batch_report.payslip_batch_report').report_action(self, data=data)