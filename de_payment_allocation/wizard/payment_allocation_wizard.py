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
    payment_id = fields.Many2one('account.payment', string='Payment')
    journal_id = fields.Many2one(related='payment_id.journal_id')
    payment_type = fields.Selection(related='payment_id.payment_type')
    payment_method_id = fields.Many2one('account.payment.method', string='Payment Method',
        readonly=False, store=True,
        compute='_compute_payment_method_id',
        
        help="Manual: Get paid by cash, check or any other method outside of Odoo.\n"\
        "Electronic: Get paid automatically through a payment acquirer by requesting a transaction on a card saved by the customer when buying or subscribing online (payment token).\n"\
        "Check: Pay bill by check and print it from Odoo.\n"\
        "Batch Deposit: Encase several customer checks at once by generating a batch deposit to submit to your bank. When encoding the bank statement in Odoo, you are suggested to reconcile the transaction with the batch deposit.To enable batch deposit, module account_batch_payment must be installed.\n"\
        "SEPA Credit Transfer: Pay bill from a SEPA Credit Transfer file you submit to your bank. To enable sepa credit transfer, module account_sepa must be installed ")
    
    
    @api.depends('journal_id')
    def _compute_payment_method_id(self):
        for wizard in self:
            payment_type = wizard.payment_type

            if payment_type == 'inbound':
                available_payment_methods = wizard.journal_id.inbound_payment_method_ids
            else:
                available_payment_methods = wizard.journal_id.outbound_payment_method_ids

            # Select the first available one by default.
            if available_payment_methods:
                wizard.payment_method_id = available_payment_methods[0]._origin
            else:
                wizard.payment_method_id = False
                
    
    def action_allocate_payment(self):
        invoice_line = []
        line_ids = []
        for invoice in self.invoice_line_ids:
            invoice_line.append(invoice.move_id.invoice_line_ids.ids)
            line_ids.append(invoice.move_id.line_ids.ids)
            invoice.move_id.id        
            self.payment_id.update({
#                 'move_id': invoice.move_id.id ,
                'payment_method_id': self.payment_method_id.id,
                'invoice_line_ids': invoice_line,
                'reconciled_bills_count': 1,
                'line_ids': line_ids,
            })    
    
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