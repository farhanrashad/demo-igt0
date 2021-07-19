# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    is_banner = fields.Boolean('Display Banner')
    main_desc = fields.Text('Main Description')
    flavor_desc = fields.Text('Flavor Description') 
    product_image = fields.Binary(
        "Product Image", attachment=True,
        help="This field holds the image used as image for the product, limited to 1024x1024px.")
    background_image = fields.Binary(
        "Background", attachment=True,
        help="This field holds the image used as background of the slider.")
    

