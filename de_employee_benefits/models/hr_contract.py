# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HrContract(models.Model):
    _inherit = 'hr.contract'
    
    @api.model
    def create(self,vals):
        if vals.get('code',_('New')) == _('New'):
            vals['code'] = self.env['ir.sequence'].next_by_code('hr.contract') or _('New')    
        res = super(HrContract,self).create(vals)
        return res
    
    
    code = fields.Char(
        'Reference', copy=False, readonly=True, default=lambda x: _('New'))
    type = fields.Selection([
        ('expat', 'Expat'),
        ('local', 'Local'),
    ], default=False,  string='Contract Type', help="Technical field for UX purpose.")
    
    
   