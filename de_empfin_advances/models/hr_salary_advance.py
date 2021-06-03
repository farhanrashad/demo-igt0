# -*- coding: utf-8 -*-
import time
from datetime import datetime
from odoo import fields, models, api, _
from odoo.exceptions import except_orm
from odoo import exceptions
from odoo.exceptions import UserError, ValidationError

class SalaryAdvancePayment(models.Model):
    _name = "hr.salary.advance"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    

    def _default_get_contract(self):
        contract_id = self.env['hr.contract'].search([('employee_id','=', self.employee_id.id),('state','=','open')], limit=1)        
        if contract_id:
            self.employee_contract_id = contract_id.id
        else:
            self.employee_contract_id = None       

    name = fields.Char(string='Name', readonly=True, select=True, default=lambda self: 'Adv/')
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    date = fields.Date(string='Date', required=True, default=lambda self: fields.Date.today())
    reason = fields.Text(string='Reason')
    currency_id = fields.Many2one('res.currency', string='Currency', required=True,
                                  default=lambda self: self.env.user.company_id.currency_id)
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.user.company_id)
    exceed_condition = fields.Boolean(string='Exceed than maximum',
                                      help="The Advance is greater than the maximum percentage in salary structure")
    department = fields.Many2one('hr.department', string='Department', related='employee_id.department_id')
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Waiting Line Manager Approval'),
                              ('hr_approval', 'Waiting HR Approval'),
                              ('finance_approval', 'Waiting Finance Approval'),
                              ('accepted', 'Waiting Account Entries'),
                              ('approved', 'Waiting Payment'),
                              ('paid', 'Paid'),
                              ('close', 'Close'),
                              ('cancel', 'Cancelled'),
                              ('reject', 'Rejected')], string='Status', default='draft', track_visibility='onchange')
    employee_contract_id = fields.Many2one('hr.contract', string='Contract', default=_default_get_contract)        
        
    deductable = fields.Boolean(string='Deductable', default=True)
    partner_id = fields.Many2one('res.partner', 'Employee Partner', readonly=False, states={'paid': [('readonly', True)]},)
    journal_id = fields.Many2one('account.journal', string='Journal', domain="[('type','in',['cash','bank'])]")
    journal_type = fields.Selection(related='journal_id.type', readonly=True)
    payment_id = fields.Many2one('account.payment', string='Payment', readonly=True, compute='_get_payment')
    payment_amount = fields.Monetary(related='payment_id.amount')
    account_id = fields.Many2one('account.account',string="Account")
    payment_method_id = fields.Many2one('account.payment.method', string='Payment Method Type', oldname="payment_method",)
    bill_count = fields.Integer(string='Advances Bill', compute='get_bill_count')
    payment_count = fields.Integer(string='Payment', compute='get_payment_count')
    
    
    def get_bill_count(self):
        count = self.env['account.move'].search_count([('hr_salary_advance_id', '=', self.id),('journal_id.type', '=', 'purchase')])
        self.bill_count = count
        
    def get_payment_count(self):
        count = self.env['account.payment'].search_count([('hr_salary_advance_id', '=', self.id)])
        self.payment_count = count
      
    @api.depends('state')
    def _get_payment(self):
        payment_id = self.env['account.payment'].search([('hr_salary_advance_id','=',self.id)],limit=1)
        self.payment_id = payment_id.id
        if not payment_id:
            self.payment_id = False

    def unlink(self):
        if any(self.filtered(lambda loan: loan.state not in ('draft', 'cancel'))):
            raise UserError(_('You cannot delete a Loan which is not draft or cancelled!'))
        return super(SalaryAdvancePayment, self).unlink()
    
    def onchange_employee_id(self, employee_id,employee_contract_id):
        if employee_id:
            employee_obj = self.env['hr.employee'].browse(employee_id)
            department_id = employee_obj.department_id.id
            employee_contract_id = employee_obj.contract_id.id
            domain = [('employee_id', '=', employee_id)]
            return {'value': {'department': department_id,'employee_contract_id':employee_contract_id}, 'domain': {
                        'employee_contract_id': domain,
                    }}

    @api.onchange('company_id')
    def onchange_company_id(self):
        company = self.company_id
        domain = [('company_id.id', '=', company.id)]
        result = {
            'domain': {
                'journal': domain,
            },

        }
        return result

    def submit_to_manager(self):
        self.state = 'confirmed'
        for cash_line in self.cash_line_ids:
            cash_line.update({
                'state': 'confirmed'
            })

    def cancel(self):
        self.state = 'cancel'
        for cash_line in self.cash_line_ids:
            cash_line.update({
                'state': 'cancel'
            })

    def action_line_manager_approve(self):
        self.state = 'hr_approval'
        for cash_line in self.cash_line_ids:
            cash_line.update({
                'state': 'hr_approval'
            })
        
    def action_hr_manager_approve(self):
        self.state = 'finance_approval'
        for cash_line in self.cash_line_ids:
            cash_line.update({
                'state': 'finance_approval'
            })
        
    def action_finance_manager_approve(self):
        self.state = 'approved'
        for cash_line in self.cash_line_ids:
            cash_line.update({
                'state': 'approved'
            })
        
        
    def action_close(self):
        self.state = 'close'
        for cash_line in self.cash_line_ids:
            cash_line.update({
                'state': 'close'
            })
        
         
          
        
    def action_refuse(self):
        self.state = 'reject'
        for cash_line in self.cash_line_ids:
            cash_line.update({
                'state': 'reject'
            })

    def action_view_invoice(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
            'name': 'Advances Bill',
            'domain': [('hr_salary_advance_id','=', self.id)],
            'target': 'current',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
        }
    
    def action_view_payment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'binding_type': 'action',
            'name': 'Payment',
            'domain': [('hr_salary_advance_id','=', self.id)],
            'target': 'current',
            'res_model': 'account.payment',
            'view_mode': 'tree,form',
        }
    
    @api.model
    def create(self, vals):
            
        vals['name'] = self.env['ir.sequence'].get('hr.salary.advance') or ' '
        res_id = super(SalaryAdvancePayment, self).create(vals)
        return res_id
    
    def action_payment(self):
        invoice = False
        if self.journal_id.type == 'purchase':
            invoice = self.env['account.move']
            lines_data = []
            lines_data.append([0,0,{
                'name': self.name,
                'price_unit': self.amount_total,
                'account_id': self.account_id.id,
                'quantity': 1,
            }])
            invoice.create({
                'partner_id': self.partner_id.id,
                'type': 'in_invoice',
                'reference': self.name,
                'origin': self.name,
                'date_invoice':self.date,
                'journal_id':self.journal_id.id,
                'hr_salary_advance_id':self.id,
                'invoice_line_ids':lines_data,
            })
        
        elif self.journal_id.type in ('bank','cash'):
            payment = self.env['account.payment']
            payment.create({
                'payment_type': 'outbound',
                'partner_type': 'supplier',
                'partner_id': self.partner_id.id,
                'payment_method_id': self.payment_method_id.id,
                'company_id': self.company_id.id,
                'amount': self.amount_total,
                'currency_id': self.currency_id.id,
                'journal_id': self.journal_id.id,
                'date': fields.Date.today(),
                'ref': self.name,
                'hr_salary_advance_id':self.id,
            })
        self.update({
            'state': 'paid'
        })
        return invoice
    
    
    
    
    @api.depends('cash_line_ids.approve_amount')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.cash_line_ids:
                amount_untaxed += line.approve_amount
            order.update({
                'amount_total': amount_untaxed 
            })
    
    
    
    cash_line_ids = fields.One2many('hr.salary.advance.line', 'advance_id', string='Advances Line')
    amount_total = fields.Monetary(string='Approved Amount', store=True, readonly=True, compute='_amount_all')

    
    
    
    
    
    
    
    
    
class AdvancePayment(models.Model):
    _name = "hr.salary.advance.line"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name='description'
    



    
    type_id = fields.Many2one('hr.advance.type', string='Type')
    product_id = fields.Many2one('product.product', string='Product', domain="[('can_be_expensed','=', True)]", required=True)
    description = fields.Char(related='product_id.name', string='Description')
    quantity = fields.Float(string='Qunatity')
    unit_price = fields.Float(string='Unit Price')
    total_amount = fields.Float(string='Total Amount', compute='_compute_amount')
    remarks = fields.Text(string='Remarks')
    finance_remarks = fields.Text(string='Finance Remarks')
    approve_amount = fields.Float(string='Amount For Approval')
    advance_id = fields.Many2one('hr.salary.advance', string='Advances')
    employee_id = fields.Many2one(related='advance_id.employee_id')
    approved = fields.Boolean(string='Approved', default=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Waiting Line Manager Approval'),
                              ('hr_approval', 'Waiting HR Approval'),
                              ('finance_approval', 'Waiting Finance Approval'),
                              ('accepted', 'Waiting Account Entries'),
                              ('approved', 'Waiting Payment'),
                              ('paid', 'Paid'),
                              ('close', 'Close'),
                              ('cancel', 'Cancelled'),
                              ('reject', 'Rejected')], string='Status', default='draft', track_visibility='onchange')
    
    
    @api.onchange('unit_price')
    def onchange_amount(self):
        for line in self:
            
            line.update({
                'approve_amount': line.unit_price * line.quantity,
            })
    
    
    
    @api.depends('quantity', 'unit_price')
    def _compute_amount(self):
        for line in self:
            
            line.update({
                'total_amount': line.unit_price * line.quantity,
            })
