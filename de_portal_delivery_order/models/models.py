# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'



    puser_id = fields.Many2one('res.users',string='Partner User', computed='_compute_user')

    @api.depends('partner_id')
    def _compute_user(self):
        for picking in self:
            user = self.env['res.users'].search([('partner_id', '=', picking.partner_id.id)], limit=1)
            return user.id

