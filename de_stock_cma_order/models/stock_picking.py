# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    stock_cma_order_id = fields.Many2one('stock.cma.order', string='CMA', copy=False)
    
class StockMove(models.Model):
    _inherit = 'stock.move'
   
    def _get_default_condition(self):
        condition_id = self.env['stock.cma.condition'].search([('is_default','=',True)], limit=1)
        return condition_id
    
    stock_cma_order_line_id = fields.Many2one('stock.cma.order.line')
    stock_cma_condition_id = fields.Many2one('stock.cma.condition', string="Condition", default=_get_default_condition)
