# -*- coding: utf-8 -*-

from odoo import fields, models, _, api


class HrExpense(models.Model):
    _inherit = 'hr.expense'

    advance_line_id  = fields.Many2one('hr.salary.advance.line', string='Advances Line', domain='[("employee_id","=", employee_id), ("state","not in", ("paid", "cancel", "close", "reject"))]')
    
    
    
    
    @api.depends('product_id', 'company_id')
    def _compute_from_product_id_company_id(self):
        for expense in self.filtered('product_id'):
            expense = expense.with_company(expense.company_id)
            expense.name = expense.name or expense.product_id.display_name
            if not expense.attachment_number or (expense.attachment_number and not expense.unit_amount):
                expense.unit_amount = expense.unit_amount
            expense.product_uom_id = expense.product_id.uom_id
            expense.tax_ids = expense.product_id.supplier_taxes_id.filtered(lambda tax: tax.company_id == expense.company_id)  # taxes only from the same company
            account = expense.product_id.product_tmpl_id._get_product_accounts()['expense']
            if account:
                expense.account_id = account
    
    
    
    @api.onchange('advance_line_id')
    def onchange_advaces(self):
        if self.advance_line_id:
            self.update({
                'product_id': self.advance_line_id.product_id.id,
                'unit_amount': self.advance_line_id.approve_amount,
            })

