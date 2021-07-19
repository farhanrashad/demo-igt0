# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'            
            

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            ana_tags = self.product_id.product_tmpl_id._get_product_analytic_tags()
            self.analytic_tag_ids = ana_tags['income']
    
    @api.multi
    def _write(self, values):
        res = super(SaleOrderLine, self)._write(values)
        if not(self.analytic_tag_ids):
            ana_tags = self.product_id.product_tmpl_id._get_product_analytic_tags()
            self.analytic_tag_ids = ana_tags['income']
        return res