# -*- coding: utf-8 -*-

from odoo import models, fields, api

# class de_website_product_image_swap(models.Model):
#     _name = 'de_website_product_image_swap.de_website_product_image_swap'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100