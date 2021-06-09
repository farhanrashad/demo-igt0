# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PaymentAllocation(models.Model):
    _name = 'payment.allocation.wizard'
    _description = 'Payment Allocation Wizard'
    
    
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    company_id = fields.Many2one('res.company', string='Company')
    account_id = fields.Many2one('account.account', string='Account', required=True)
    amount = fields.Float(string='Amount')
    payment_line_ids = fields.One2many('payment.allocation.wizard.line', 'allocation_id', string='Payment Lines')
    invoice_line_ids = fields.One2many('invoice.allocation.wizard.line', 'allocation_id', string='Invoice Lines')

    
    def action_allocate_payment(self):
        pass
    
    
class PaymentAllocationLine(models.Model):
    _name = 'payment.allocation.wizard.line'
    _description = 'Payment Allocation Wizard Line'
    
    
    payment_id = fields.Many2one('account.payment', string='Payment')
    allocation_id = fields.Many2one('payment.allocation.wizard', string='Allocation')
    payment_amount = fields.Float(string='Payment Amount')
    payment_date = fields.Date(string='Payment Date')
    unallocate_amount = fields.Float(string='Unallocated Amount')
    allocate = fields.Boolean(string='Allocate')
    allocate_amount = fields.Float(string='allocate Amount')
    
    
class InvoiceAllocationLine(models.Model):
    _name = 'invoice.allocation.wizard.line'
    _description = 'Invoice Allocation Wizard Line'
    
    
    move_id = fields.Many2one('account.move', string='Invoice')
    allocation_id = fields.Many2one('payment.allocation.wizard', string='Allocation')
    payment_date = fields.Date(string='Invoice Date')
    due_date = fields.Date(string='Due Date')
    invoice_amount = fields.Float(string='Invoice Amount')
    unallocate_amount = fields.Float(string='Unallocated Amount')
    allocate = fields.Boolean(string='Allocate')
    allocate_amount = fields.Float(string='allocate Amount')    