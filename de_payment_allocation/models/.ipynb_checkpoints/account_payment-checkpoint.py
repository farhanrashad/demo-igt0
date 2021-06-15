# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    
    reconcile_amount = fields.Float(string='Reconcile Amount', compute='_compute_reconcile_amount')
    
    def _compute_reconcile_amount(self):
        for payment in self:
            reconcile_amount = 0.0
            for move_line in payment.move_id.line_ids:
                if move_line.credit == 0.0:
                    for credit_line in move_line.match_credit_ids:
                        reconcile_amount = reconcile_amount + credit_line.credit_amount_currency
            payment.update({
                'reconcile_amount' : reconcile_amount
            })
            if payment.reconcile_amount == payment.amount:
                payment.update({
                'is_reconciled' : True
                })
                
                          
    
    
    
    
    def action_payment_allocation(self):
        payment_list = []
        invoice_list = []
        partner = []
        for rec in self:
            selected_ids = rec.env.context.get('active_ids', [])
            selected_records = rec.env['account.payment'].browse(selected_ids)
            
            
        for  payment in  selected_records:
            if self.is_reconciled == True:
                raise UserError_(('This Payment Already Reconciled'))
            else:
                payment_amount = 0.0
                if payment.amount_residual == 0.0:
                    payment_amount = payment.amount
                else:
                    payment_amount = payment.amount_residual

                payment_list.append((0,0,{
                    'payment_id': payment.id,
                    'payment_date': payment.date,
                    'payment_amount': payment.amount,
                    'unallocate_amount': payment_amount,
                    'allocate': True,
                    'allocate_amount': payment_amount,
                }))
                partner.append(payment.partner_id.id)
        uniq_partner =  set(partner) 
        for ppartner in uniq_partner:
            invoices = self.env['account.move'].search([('partner_id','=',ppartner),('state','=','posted'),('payment_state','in', ('not_paid','partial'))]) 
            
            for  inv in invoices:
                invoice_list.append((0,0,{
                    'move_id': inv.id,
                    'payment_date': inv.invoice_date,
                    'due_date': inv.invoice_date_due,
                    'invoice_amount': inv.amount_total,
                    'unallocate_amount': inv.amount_residual,
                    'allocate': False,
                    'allocate_amount': inv.amount_residual,
                }))    
        return {
            'name': ('Payment Allocation'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'payment.allocation.wizard',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {'default_payment_line_ids': payment_list, 
                        'default_invoice_line_ids': invoice_list, 
                        'default_company_id': self.env.company.id,
                        'default_partner_id': self.partner_id.id,
                        'default_is_payment': True,
                        'default_account_id': self.destination_account_id.id,
                        'default_payment_id': self.id,
                       },
        }

