# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    business_type = fields.Selection([
        ('producer', 'Producer'),
        ('processor', 'Processor'),
        ('exporter', 'Exporter'),
        ('distributor', 'Distributor'),
        ('manufacturer', 'Manufacturer'),
        ('vendor', 'Vendor'),
    ], string='Business Type')
    
    country_state = fields.Char(string='State')

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100