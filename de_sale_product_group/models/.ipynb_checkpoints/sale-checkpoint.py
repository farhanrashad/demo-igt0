# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order.line'
    
    #tag_ids = fields.Many2many(related='product_id.tag_ids', string='Tags', readonly=True)
    group_id = fields.Many2many('product.group', related='product_id.group_id', string="Group", readonly=True)

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100