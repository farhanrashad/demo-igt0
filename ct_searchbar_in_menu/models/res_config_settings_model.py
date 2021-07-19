# -*- coding: utf-8 -*-
# Part of CierTech.


from odoo import api, fields, models

class website(models.Model):
    _inherit = 'website'

    ct_searchbar_in_menu=fields.Boolean(string="Searchbar in menu")   


class res_config_settings(models.TransientModel):
    _inherit="res.config.settings"
    
    ct_searchbar_in_menu = fields.Boolean(
        related="website_id.ct_searchbar_in_menu", string="Searchbar in menu", readonly=False)

