# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from dateutil.relativedelta import relativedelta
from datetime import date

class SaleSubscriptionPlan(models.Model):
    _name = 'sale.subscription.plan'
    _description = 'Subscription Plan'
    
    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
    code = fields.Char(help="Code is added automatically in the display name of every subscription.")
    description = fields.Text(translate=True, string="Terms and Conditions")
    recurring_interval_type = fields.Selection([('daily', 'Days'), ('weekly', 'Weeks'),
                                                ('monthly', 'Months'), ('yearly', 'Years'), ],
                                               string='Recurrence', required=True,
                                               help="Invoice automatically repeat at specified interval",
                                               default='monthly', tracking=True)
    recurring_interval_rule = fields.Selection([
        ('unlimited', 'Forever'),
        ('limited', 'Fixed')
    ], string='Duration', default='unlimited')
    recurring_interval = fields.Integer(string="Invoicing Period", help="Repeat every (Days/Week/Month/Year)", required=True, default=1, tracking=True)
    recurring_interval_count = fields.Integer(string="End After", default=1)
    invoicing_mode = fields.Selection([
        ('manual', 'Manually'),
        ('draft', 'Draft'),
        ('validate', 'Validate'),
    ], required=True, default='draft')
    group_invoices = fields.Boolean(string='Group Invoices', help="Only one invoice will generate for multiple subscription lines of the period ")
    journal_id = fields.Many2one('account.journal', string="Accounting Journal",
                                 domain="[('type', '=', 'sale')]", company_dependent=True,
                                 check_company=True,
                                 help="If set, subscriptions with this template will invoice in this journal; otherwise the sales journal with the lowest sequence is used.")

    company_id = fields.Many2one('res.company', index=True)
