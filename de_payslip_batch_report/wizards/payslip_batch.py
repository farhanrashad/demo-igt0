from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PayslipBatch(models.TransientModel):
    _name = "pay.slip.batch"
    _description = "Payslip Batch Wizard"

    name = fields.Char(string='Name')
