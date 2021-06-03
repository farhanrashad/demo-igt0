# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta



class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    subscription_invoice = fields.Boolean('Subscription Product',
        help='If set, confirming a sale order with this product will create a subscription')

