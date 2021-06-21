from odoo import api, fields, models, _
from odoo.exceptions import UserError


class GtnDgnMrfSpmrfWizard(models.TransientModel):
    _name = "gtn.dgn.mrf.spmrf.wizard"
    
    src =  fields.Datetime(string='From')
    dest =  fields.Datetime(string='To')
    
    def generate_report(self):
        order_ids = self.env['stock.transfer.order'].browse(self._context.get('active_ids',[]))
        data = {'start_date': self.src, 'end_date': self.dest, 'order_ids': order_ids.id}
        if self.src < self.dest:
            return self.env.ref('de_gtn_dgn_mrf_spmrf_line_report.mrf_spmrf_report').report_action(self, data=data)
