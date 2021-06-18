from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PayslipBatch(models.TransientModel):
    _name = "pay.slip.batch"
    _description = "Payslip Batch Wizard"

    contract_type = fields.Selection([('local', 'Local'),('expats', 'Expats')], string='Contract Type')
    doe = fields.Date(string='Date of Execution')
    debit_ac_no = fields.Float(string='Debit A/C No.')
    currency = fields.Many2one('res.currency', string='Currency')
    batch_id = fields.Many2one('hr.payslip.run')
    
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