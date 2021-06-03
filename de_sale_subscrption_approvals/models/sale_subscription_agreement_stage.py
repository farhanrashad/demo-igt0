# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AgreementStage(models.Model):
    _inherit = 'sale.subscription.agreement.stage'

    is_refused = fields.Boolean(string="Refused Stage")
