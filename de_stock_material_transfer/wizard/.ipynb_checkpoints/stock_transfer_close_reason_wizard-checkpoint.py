# -*- coding: utf-8 -*-
from odoo import api, fields, models


class StockTransferCloseReasonWizard(models.TransientModel):
    _name = "stock.transfer.close.reason.wizard"
    _description = 'Stock Transfer Close Reason Wizard'

    close_reason_id = fields.Many2one("stock.transfer.close.reason", string="Close Reason")
    close_reason_message = fields.Char(string='Message')

    def set_close(self):
        self.ensure_one()
        order = self.env['stock.transfer.order'].browse(self.env.context.get('active_id'))
        order.close_reason_id = self.close_reason_id
        order.close_reason_message = self.close_reason_message
        order.set_close()
