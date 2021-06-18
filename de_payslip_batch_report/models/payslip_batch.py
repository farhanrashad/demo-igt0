from odoo import models, api


class PayslipBatchInherit(models.Model):
    _inherit = 'hr.payslip.run'

#     def print_report(self):
#         print('ID: ', self.id)
#         id = self.id
#         data = {
#             'id': id
#         }
#         return self.env.ref('de_payslip_batch_report.payslip_batch_report_xlsx').report_action(self, data=data)
