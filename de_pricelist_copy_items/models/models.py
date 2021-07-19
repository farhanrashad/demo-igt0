# -*- coding: utf-8 -*-

import json
import re
import uuid
from functools import partial

from lxml import etree
from dateutil.relativedelta import relativedelta
from werkzeug.urls import url_encode

from odoo import api, exceptions, fields, models, _
from odoo.tools import email_re, email_split, email_escape_char, float_is_zero, float_compare, \
    pycompat, date_utils
from odoo.tools.misc import formatLang

from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning

from odoo.addons import decimal_precision as dp
import logging

class PriceList(models.Model):
    _inherit = 'product.pricelist'
    
    ref_pricelist_ids = fields.Many2many('product.pricelist', relation='ref_product_pricelist_product_pricelist_rel', column1='id1', culomn2='id2', string='Ref. Pricelist', stored=True)
    
    

class PriceListItem(models.Model):
    _inherit = 'product.pricelist.item'

    price_on_basepricelist = fields.Float(string="Price on base pricelist",compute="_calculate_price_on_basepricelist",digits=dp.get_precision('Product Price'))
    currency_id = fields.Many2one('res.currency',related='pricelist_id.currency_id',string='Currency')
    
    
    @api.one
    @api.depends('pricelist_id','base_pricelist_id','product_tmpl_id','min_quantity')
    def _calculate_price_on_basepricelist(self):
        from_amount = 0
        date = self._context.get('date') or fields.Date.today()
        company_id = self._context.get('company_id') or self.env['res.users']._get_company().id
        round_curr = self.pricelist_id.currency_id.round
        for rs in self:
            from_currency_id = rs.pricelist_id.currency_id
            to_currency_id = rs.base_pricelist_id.currency_id
            
            if rs.base_pricelist_id:
                if rs.applied_on == '1_product':
                    from_amount = self.env['product.pricelist.item'].search([('pricelist_id', '=', rs.base_pricelist_id.id),('product_tmpl_id', '=', rs.product_tmpl_id.id),('min_quantity', '=', rs.min_quantity)],limit=1).fixed_price
                elif rs.applied_on == '0_product_variant':
                    from_amount = self.env['product.pricelist.item'].search([('pricelist_id', '=', rs.base_pricelist_id.id),('product_id', '=', rs.product_id.id),('min_quantity', '=', rs.min_quantity)],limit=1).fixed_price
            else:
                from_amount = 0
                #from_amount = 0
            rs.price_on_basepricelist = abs(from_amount) * rs.pricelist_id.currency_id.rate
            #rs.price_on_basepricelist = from_currency_id._convert(abs(from_amount),to_currency_id,company_id,date)
            
            #currency_id._convert(self.amount_total, self.company_id.currency_id, self.company_id, self.date_invoice or fields.Date.today())
            #rs.price_on_basepricelist = from_amount
    
    @api.multi
    def _write(self, values):
        res = super(PriceListItem, self)._write(values)
       
        return res
    