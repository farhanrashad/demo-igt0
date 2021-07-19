# -- coding: utf-8 --

from odoo import models, fields, api

class ProductGroup(models.Model):
    _name = 'product.group'
    _description = 'Product Group'
    
    name = fields.Char(string="Group Name", required=True)
    
class Product(models.Model):
    _inherit = 'product.product'
    
    group_id = fields.Many2one('product.group', string='Product Group',store=True)
    test_bool = fields.Boolean('Test')


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    #@api.multi
    #def _compute_price_rule(self, products_qty_partner, date=False, uom_id=False):
    #    res = super(Pricelist, self)._compute_price_rule(products_qty_partner, date=date, uom_id=uom_id)
    #    for product_key, values in res.items():
    #        if product_key and values[1]:
    #            product_id = self.env['product.product'].browse(product_key)
    #            if product_id.test_bool:
    #                res.update({product_key: (values[0] + product_id.price_extra, values[1])})
    #    return res


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def _get_combination_info(self, combination=False, product_id=False, add_qty=1, pricelist=False,
                              parent_combination=False, only_template=False):
        if product_id:
            product_id = self.env['product.product'].browse(product_id)
            product_id.test_bool = True
        res = super(ProductTemplate, self.with_context(from_product_configurator_custom=1))._get_combination_info(combination=combination, product_id=product_id,
                                                                 add_qty=add_qty, pricelist=pricelist,
                                                                 parent_combination=parent_combination,
                                                                 only_template=only_template)
        return res