# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductTags(models.Model):
    _name = 'product.tags'
    _description = 'Product Tags'
    
    name = fields.Char(string="Tag Name", required=True)
    
class Product(models.Model):
    _inherit = 'product.product'
    
    tag_ids = fields.Many2many('product.tags', string='Tags',readonly=True, store=True)

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100