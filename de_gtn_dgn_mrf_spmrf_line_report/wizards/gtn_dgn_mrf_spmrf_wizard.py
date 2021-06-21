from odoo import api, fields, models, _
from odoo.exceptions import UserError


class GtnDgnMrfSpmrfWizard(models.TransientModel):
    _name = "gtn.dgn.mrf.spmrf.wizard"
    
    src =  fields.Datetime(string='From')
    dest =  fields.Datetime(string='To')
    
    def generate_report(self):
        order_ids = self.env['stock.transfer.order'].browse(self._context.get('active_ids',[]))
        raise UserError(order_ids)
