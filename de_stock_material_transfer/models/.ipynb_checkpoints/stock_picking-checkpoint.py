# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    stock_transfer_order_id = fields.Many2one('stock.transfer.order', string='Transfer Order', copy=False)
    
class StockMove(models.Model):
    _inherit = 'stock.move'
   
    def _get_default_condition(self):
        condition_id = self.env['stock.transfer.material.condition'].search([('is_default','=',True)], limit=1)
        return condition_id
    
    stock_transfer_order_line_id = fields.Many2one('stock.transfer.order.line')
    stock_material_condition_id = fields.Many2one('stock.transfer.material.condition', string="Condition", default=_get_default_condition)
