# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import fields, models, api

class AccountMove(models.Model):
    _inherit = "account.move"

    subscription_agreement_id = fields.Many2one("sale.subscription.agreement")
    
class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    subscription_agreement_id = fields.Many2one("sale.subscription.agreement")
    subscription_agreement_start_date = fields.Date(
        string="Subscription Revenue Start Date", readonly=True
    )
    subscription_agreement_end_date = fields.Date(
        string="Subscription Revenue End Date", readonly=True
    )