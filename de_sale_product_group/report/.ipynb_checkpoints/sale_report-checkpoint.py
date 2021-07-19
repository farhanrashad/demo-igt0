# coding: utf-8
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models


class SaleReport(models.Model):
    _inherit = 'sale.report'

    #tag_ids = fields.Many2many('product.tags', readonly=True)
    group_id = fields.Many2one('product.group', string='Group', readonly=True)
    
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['group_id'] = ", p.group_id as group_id"
        groupby += ', p.group_id'
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
