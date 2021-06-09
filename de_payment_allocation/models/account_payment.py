# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    
    def action_payment_allocation(self):
        payment_list = []
        invoice_list = []
        partner = []
        for rec in self:
            selected_ids = rec.env.context.get('active_ids', [])
            selected_records = rec.env['account.payment'].browse(selected_ids)
        for  payment in  selected_records:
            payment_list.append((0,0,{
                'payment_id': payment.id,
                'payment_date': payment.date,
                'payment_amount': payment.amount,
                'unallocate_amount': payment.amount,
                'allocate': False,
                'allocate_amount': payment.amount,
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
                        'default_account_id': self.destination_account_id.id,
                       },
        }

