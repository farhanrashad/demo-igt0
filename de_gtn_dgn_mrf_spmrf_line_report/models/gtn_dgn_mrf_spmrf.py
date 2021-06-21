from odoo import models, api
from odoo.exceptions import UserError

class MrfSpmrf(models.Model):
    _inherit = 'stock.transfer.order'

#     def generate_report(self):
#         ids = self.env['stock.transfer.order'].browse(self._context.get('active_ids',[]))
#         raise UserError(ids)
#         data = {'start_date': self.start_date, 'end_date': self.end_date, 'config_ids': self.pos_config_ids.ids}
#         if self.start_date < self.end_date:
#             return self.env.ref('de_pos_sales_report.sale_analysis_report').report_action(self, data=data)