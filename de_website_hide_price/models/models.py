# -*- coding: utf-8 -*-

from odoo import models, fields, api

class CrmLead(models.Model):
    _inherit = 'crm.lead'
    
    fname = fields.Char('First Name')
    lname = fields.Char('Last Name')
    
    business_type = fields.Selection([
        ('producer', 'Producer'),
        ('processor', 'Processor'),
        ('exporter', 'Exporter'),
        ('distributor', 'Distributor'),
        ('manufacturer', 'Manufacturer'),
        ('vendor', 'Vendor'),
    ], string='Business Type')
    
    country_state = fields.Char(string='State')

    @api.model
    def create(self, vals):
        res = super(CrmLead, self).create(vals)
        for rec in res:
            state_obj = self.env['res.country.state']
            if rec.country_state:
                state_id = state_obj.search([('name', '=', rec.country_state)])
                if len(state_id) >=1:
                    rec.state_id = state_id[0].id
        return res