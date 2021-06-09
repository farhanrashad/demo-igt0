# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    
    def allocate_invoice_payment(self):
        pass

