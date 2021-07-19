# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class de_websie_show_all_prices(models.Model):
#     _name = 'de_websie_show_all_prices.de_websie_show_all_prices'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100