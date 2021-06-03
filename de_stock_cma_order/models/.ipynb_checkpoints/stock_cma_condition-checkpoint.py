# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class StockCMACondition(models.Model):
    _name = "stock.cma.condition"
    _description = "Material Condition"

    name = fields.Char('Name', required=True)
    is_default = fields.Boolean('Default Condition')