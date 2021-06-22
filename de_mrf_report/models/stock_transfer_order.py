from odoo import models, api,fields


class StockTransferOrderInherit(models.Model):
    _inherit = 'stock.transfer.order'
    
    mobile_phone = fields.Char(string = 'Work Mobile', related='user_id.employee_id.work_phone')
    job_title = fields.Many2one('hr.job',string='Job Position',related='user_id.employee_id.job_id')
    