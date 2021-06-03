# -*- coding: utf-8 -*-
from datetime import timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date
from random import randint


class StockTransferOrderType(models.Model):
    _name = "stock.transfer.order.type"
    _description = "Transfer Order Type"

    name = fields.Char('Name', required=True)
    code = fields.Char('Code', size=3, required=True)
    active = fields.Boolean('Active', default=True, help="If unchecked, it will allow you to hide the transfer type without removing it.")
    description = fields.Text("Requirements", help="Enter here the details of transfer type.")
    disallow_staging = fields.Boolean(string='Disallow Staging')
    _sql_constraints = [
        ('name_uniq', 'unique (name)', "type name already exists!"),
    ]
    sequence_id = fields.Many2one('ir.sequence', 'Reference Sequence',
        copy=False, check_company=True)
    company_id = fields.Many2one(
        'res.company', 'Company', copy=False,
        required=True, index=True, default=lambda s: s.env.company)
    
    @api.model
    def create(self, vals):
        if vals.get('code'):
            sequence = self.env['ir.sequence'].create({
                'name': _('Sequence') + ' ' + vals['code'],
                'padding': 5,
                'prefix': vals['code'],
                'company_id': vals.get('company_id'),
            })
            vals['sequence_id'] = sequence.id

        transfer_type = super().create(vals)
        return transfer_type

    def write(self, vals):
        if 'code' in vals:
            for transfer_type in self:
                sequence_vals = {
                    'name': _('Sequence') + ' ' + vals['code'],
                    'padding': 5,
                    'prefix': vals['code'],
                }
                if transfer_type.sequence_id:
                    transfer_type.sequence_id.write(sequence_vals)
                else:
                    sequence_vals['company_id'] = vals.get('company_id', transfer_type.company_id.id)
                    sequence = self.env['ir.sequence'].create(sequence_vals)
                    transfer_type.sequence_id = sequence
        if 'company_id' in vals:
            for transfer_type in self:
                if transfer_type.sequence_id:
                    transfer_type.sequence_id.company_id = vals.get('company_id')
        return super().write(vals)