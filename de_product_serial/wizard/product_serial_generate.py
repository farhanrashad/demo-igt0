# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class ProductSerialGenerate(models.TransientModel):
    _name = "product.serial.generate"
    _description = "Product Serial Generate"
    
    
    
    serial_count = fields.Integer(string='Number of Serial')  
    product_ids = fields.Many2many('product.template', string='Product Template')
    

