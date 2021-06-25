# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import datetime
import calendar


class EmployeeAttandanceWizard(models.Model):
    _name = "product.availablity.report"
    _description = "Product availablity Report"

    date = fields.Date(string="Date", required=True , default=datetime.date.today())
    location = fields.Many2one('stock.location', string="Location", required=True)
    product_ids = fields.Many2many('product.product', string="Product")

    def action_report_gen(self):
        datas = {
            'date': self.date,
            'location_id': self.location.id,
            'location_name': self.location.complete_name,
            'product_ids': self.product_ids.ids,
        }
        return self.env.ref('de_product_availability_report.view_product_report_xlsx').report_action(self, data=datas)
