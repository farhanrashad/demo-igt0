# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date
from random import randint


class StockCMAType(models.Model):
    _name = "stock.cma.type"
    _description = "CMA Type"

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char('Name', required=True)

    action_type = fields.Selection([
        ('regular', 'Regular'),
        ('returnable', 'Returnable'),
        ('replacement', 'Replacement'),
        ], string='Action Type', required=True, readonly=False, default='regular')
    
    description = fields.Text("Requirements", help="Enter here the reasons for this CMA type.")
    default_delivery_validity = fields.Integer('Delivery validity')
    delivery_lead_days = fields.Integer('Delivery Lead time')
    default_return_validity = fields.Integer('Return validity')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "type name already exists!"),
    ]