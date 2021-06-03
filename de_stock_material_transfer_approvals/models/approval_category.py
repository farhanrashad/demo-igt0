# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ApprovalCategory(models.Model):
    _inherit = 'approval.category'

    # ir for internal requisition
    approval_type = fields.Selection(selection_add=[('ir', 'Stock Material Transfer\'s')])

    #@api.onchange('approval_type')
    #def _onchange_approval_type(self):
    #    if self.approval_type == 'purchase':
    #        self.has_product = 'required'
    #        self.has_quantity = 'required'
