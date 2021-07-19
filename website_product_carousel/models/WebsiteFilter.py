from odoo import models, fields, api


class WebsiteProductFilter(models.Model):
    _name = "website.product.filter"
    _rec_name = "name"
    _description = 'Product Filter'

    name = fields.Char("Product Filter Name")
    filter_id = fields.Many2one("ir.filters", "Select Product Filter")
    website_filter_published = fields.Boolean("Website Filter Published")
