from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = ['product.template', 'product.carousel.data']
    _name = 'product.template'

    is_discount = fields.Boolean(string='Discount ?')
    is_best_seller = fields.Boolean(string='Best Seller ?')
    is_new_arrival = fields.Boolean(string='New Arrival ?')
    is_special = fields.Boolean(String='Special For Today ?')
    name_ribbon = fields.Char(string='Ribbon Name', size=20, translate=True)
