# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging
import datetime
import traceback

from ast import literal_eval
from collections import Counter
from dateutil.relativedelta import relativedelta
from uuid import uuid4

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.osv import expression
from odoo.tools import format_date, float_compare
from odoo.tools.float_utils import float_is_zero


_logger = logging.getLogger(__name__)

PERIODS = {'daily': 'days', 'weekly': 'weeks', 'monthly': 'months', 'yearly': 'years'}

class SaleSubscriptionAgreement(models.Model):
    _name = 'sale.subscription.agreement'
    _description = 'Sale Subscription Agreement'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _check_company_auto = True
    _mail_post_access = 'read'
    
    
    def _get_default_pricelist(self):
        return self.env['product.pricelist'].search([('currency_id', '=', self.env.company.currency_id.id)], limit=1).id

    @api.model
    def _get_default_team(self):
        return self.env['crm.team']._get_default_team_id()
    
    def _get_default_stage_id(self):
        return self.env['sale.subscription.agreement.stage'].search([], order='sequence', limit=1)
    
    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        return stages.sudo().search([], order=order)
    
    
    name = fields.Char(required=True, tracking=True, default="New")
    code = fields.Char(string="Reference", required=True, tracking=True, index=True, copy=False)
    stage_id = fields.Many2one('sale.subscription.agreement.stage', string='Stage', index=True, default=lambda s: s._get_default_stage_id(), copy=False, tracking=True)
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',
                                          domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", check_company=True)
    
    company_id = fields.Many2one('res.company', string="Company", default=lambda s: s.env.company, required=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True, auto_join=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    partner_invoice_id = fields.Many2one(
        'res.partner', string='Invoice Address',
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",)
    partner_shipping_id = fields.Many2one(
        'res.partner', string='Service Address',
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", )
    subscription_agreement_date = fields.Date(string='Agreement Date', default=fields.Date.today)
    date_start = fields.Date(string='Start Date', default=fields.Date.today)
    date = fields.Date(string='End Date', tracking=True, help="If set in advance, the subscription will be set to renew 1 month before the date and will be closed on the date set in this field.")
    pricelist_id = fields.Many2one('product.pricelist',  domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", string='Pricelist', default=_get_default_pricelist, required=True, check_company=True)
    recurring_next_date = fields.Date(string='Date of Next Invoice', default=fields.Date.today, help="The next invoice will be created on this date then the period will be extended.")
    recurring_invoice_day = fields.Integer('Recurring Invoice Day', copy=False, default=lambda e: fields.Date.today().day)

    recurring_interval_rule = fields.Selection(related='subscription_plan_id.recurring_interval_rule', )
    recurring_interval_type = fields.Selection(related='subscription_plan_id.recurring_interval_type', )
    recurring_interval = fields.Integer(related='subscription_plan_id.recurring_interval')
    recurring_interval_count = fields.Integer(related='subscription_plan_id.recurring_interval_count')
    invoicing_mode = fields.Selection(related='subscription_plan_id.invoicing_mode')
    
    currency_id = fields.Many2one('res.currency', related='pricelist_id.currency_id', string='Currency', readonly=True)
    subscription_plan_id = fields.Many2one('sale.subscription.plan', string='Subscription Plan',
                                           domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", required=True, help="The subscription plan defines the invoice policy and the payment terms.", tracking=True, check_company=True)
    
    description = fields.Text()
    user_id = fields.Many2one('res.users', string='Salesperson', tracking=True, default=lambda self: self.env.user)
    team_id = fields.Many2one('crm.team', 'Sales Team', change_default=True, default=_get_default_team,
        check_company=True, domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    subscription_agreement_line = fields.One2many('sale.subscription.agreement.line', 'subscription_agreement_id', string='Subscription Lines', copy=True)
    subscription_invoice_ids = fields.One2many('account.move','subscription_agreement_id', string='Subscription', readonly=True)
    subscription_invoice_count = fields.Integer(compute='_compute_invoice_count')
    
    recurring_total = fields.Float(compute='_amount_all', string="Recurring Price", store=True, tracking=40)
    # add tax calculation
    recurring_tax = fields.Float('Taxes', compute="_amount_all", compute_sudo=True, store=True)
    recurring_total_incl = fields.Float('Total', compute="_amount_all", compute_sudo=True, store=True, tracking=50)
    payment_term_id = fields.Many2one('account.payment.term', string='Default Payment Terms', check_company=True, tracking=True, help="These payment terms will be used when generating new invoices and renewal/upsell orders. Note that invoices paid using online payment will use 'Already paid' regardless of this setting.")


    @api.depends('subscription_agreement_line.price_subtotal')
    def _amount_all(self):
        """
        Compute the total amounts of the subscription.
        """
        for subscription in self:
            amount_tax = 0.0
            recurring_total = 0.0
            for line in subscription.subscription_agreement_line:
                recurring_total += line.price_subtotal
                # _amount_line_tax needs singleton
                amount_tax += line._amount_line_tax()
            recurring_tax = subscription.currency_id and subscription.currency_id.round(amount_tax) or 0.0
            subscription.update({
                'recurring_total': recurring_total,
                'recurring_tax': recurring_tax,
                'recurring_total_incl': recurring_tax + recurring_total,
            })
    
    
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        if self.partner_id:
            self.pricelist_id = self.partner_id.with_company(self.company_id).property_product_pricelist.id
            self.payment_term_id = self.partner_id.with_company(self.company_id).property_payment_term_id.id
            #addresses = self.partner_id.address_get(['delivery', 'invoice'])
            #self.partner_shipping_id = addresses['delivery']
            #self.partner_invoice_id = addresses['invoice']
        if self.partner_id.user_id:
            self.user_id = self.partner_id.user_id
            

    @api.onchange('date_start', 'subscription_plan_id')
    def onchange_date_start(self):
        if self.date_start and self.recurring_interval_rule == 'limited':
            self.date = fields.Date.from_string(self.date_start) + relativedelta(**{
                PERIODS[self.recurring_interval_type]: self.subscription_plan_id.recurring_interval_count * self.subscription_plan_id.recurring_interval})
            
    @api.onchange('recurring_next_date')
    def onchange_recurring_next_date(self):
        if self.recurring_next_date:
            recurring_next_date = self.recurring_next_date
            self.recurring_invoice_day = recurring_next_date.day
            
    @api.model
    def create(self, vals):
        vals['code'] = (
            vals.get('code') or
            self.env.context.get('default_code') or
            self.env['ir.sequence'].with_company(vals.get('company_id')).next_by_code('sale.subscription.agreement') or
            'New'
        )
        if vals.get('name', 'New') == 'New':
            vals['name'] = vals['code']
        if not vals.get('recurring_invoice_day'):
            sub_date = vals.get('recurring_next_date') or vals.get('date_start') or fields.Date.context_today(self)
            if isinstance(sub_date, datetime.date):
                vals['recurring_invoice_day'] = sub_date.day
            else:
                vals['recurring_invoice_day'] = fields.Date.from_string(sub_date).day
        subscription = super(SaleSubscriptionAgreement, self).create(vals)
       
        if subscription.partner_id:
            subscription.message_subscribe(subscription.partner_id.ids)
        return subscription
   
    def write(self, vals):
        recurring_next_date = vals.get('recurring_next_date')
        if recurring_next_date and not self.env.context.get('skip_update_recurring_invoice_day'):
            if isinstance(recurring_next_date, datetime.date):
                vals['recurring_invoice_day'] = recurring_next_date.day
            else:
                vals['recurring_invoice_day'] = fields.Date.from_string(recurring_next_date).day
        if vals.get('partner_id'):
            self.message_subscribe([vals['partner_id']])
        result = super(SaleSubscriptionAgreement, self).write(vals)
        return result
    
    def generate_recurring_invoice(self):
        res = self._recurring_create_invoice()
        return self.action_subscription_invoice()
       
        
        
    def _recurring_create_invoice(self):
        for subscription in self:
            current_date = subscription.recurring_next_date or self.default_get(['recurring_next_date'])['recurring_next_date']
            new_date = subscription._get_recurring_next_date(subscription.recurring_interval_type, subscription.recurring_interval, current_date, subscription.recurring_invoice_day)
            new_values = {'recurring_next_date': new_date}
            if subscription.date:
                new_values['date'] = subscription.date + relativedelta(**{
                    PERIODS[subscription.recurring_interval_type]:
                        subscription.subscription_plan_id.recurring_interval_count * subscription.subscription_plan_id.recurring_interval
                })
            subscription.write(new_values)
            
        invoice = self.env['account.move']
        lines_data = []
        for line in self.subscription_agreement_line:
            lines_data.append([0,0,{
                'name': line.name,
                'subscription_agreement_id': line.subscription_agreement_id.id,
                'price_unit': line.price_unit or 0.0,
                #'discount': line.discount,
                'quantity': line.quantity,
                'product_uom_id': line.uom_id.id,
                'product_id': line.product_id.id,
                #'tax_ids': [(6, 0, tax_ids.ids)],
                #'analytic_account_id': line.analytic_account_id.analytic_account_id.id,
                #'analytic_tag_ids': [(6, 0, line.analytic_account_id.tag_ids.ids)],
                'subscription_agreement_start_date': self.date_start,
                'subscription_agreement_end_date': self.date,
            }])
        invoice.create({
            'move_type': 'out_invoice',
            'invoice_date': current_date,
            'partner_id': self.partner_id.id,
            'partner_shipping_id': self.partner_id.id,
            'currency_id': self.pricelist_id.currency_id.id,
            'journal_id': self.subscription_plan_id.journal_id.id,
            'invoice_origin': self.code,
            #'fiscal_position_id': fpos.id,
            'invoice_payment_term_id': self.payment_term_id.id,
            'narration': 'test entry',
            'invoice_user_id': self.user_id.id,
            #'partner_bank_id': company.partner_id.bank_ids.filtered(lambda b: not b.company_id or b.company_id == company)[:1].id,
            'invoice_line_ids':lines_data,
        })
        return invoice
    
    @api.model
    def _get_recurring_next_date(self, interval_type, interval, current_date, recurring_invoice_day):
        """
        This method is used for calculating next invoice date for a subscription
        :params interval_type: type of interval i.e. yearly, monthly, weekly etc.
        :params interval: number of interval i.e. 2 week, 1 month, 6 month, 1 year etc.
        :params current_date: date from which next invoice date is to be calculated
        :params recurring_invoice_day: day on which next invoice is to be generated in future
        :returns: date on which invoice will be generated
        """
        interval_type = PERIODS[interval_type]
        recurring_next_date = fields.Date.from_string(current_date) + relativedelta(**{interval_type: interval})
        if interval_type == 'months':
            last_day_of_month = recurring_next_date + relativedelta(day=31)
            if last_day_of_month.day >= recurring_invoice_day:
                # In cases where the next month does not have same day as of previous recurrent invoice date, we set the last date of next month
                # Example: current_date is 31st January then next date will be 28/29th February
                return recurring_next_date.replace(day=recurring_invoice_day)
            # In cases where the subscription was created on the last day of a particular month then it should stick to last day for all recurrent monthly invoices
            # Example: 31st January, 28th February, 31st March, 30 April and so on.
            return last_day_of_month
        # Return the next day after adding interval
        return recurring_next_date
    
    def action_subscription_invoice(self):
        self.ensure_one()
        invoices = self.env['account.move'].search([('invoice_line_ids.subscription_agreement_id', 'in', self.ids)])
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
        action["context"] = {
            "create": False,
            "default_move_type": "out_invoice"
        }
        if len(invoices) > 1:
            action['domain'] = [('id', 'in', invoices.ids)]
        elif len(invoices) == 1:
            form_view = [(self.env.ref('account.view_move_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = invoices.ids[0]
        else:
            action = {'type': 'ir.actions.act_window_close'}
        return action
    
    
    def _compute_invoice_count(self):
        Invoice = self.env['account.move']
        can_read = Invoice.check_access_rights('read', raise_exception=False)
        for subscription in self:
            subscription.subscription_invoice_count = can_read and Invoice.search_count([('invoice_line_ids.subscription_agreement_id', '=', subscription.id)]) or 0
            
            
class SaleSubscriptionAgreementLine(models.Model):
    _name = 'sale.subscription.agreement.line'
    _description = "Sale Subscription Agreement Line"
    _check_company_auto = True
        
    subscription_agreement_id = fields.Many2one('sale.subscription.agreement', string='Subscription', ondelete='cascade')
    product_id = fields.Many2one(
        'product.product', string='Product', check_company=True, domain="[('subscription_invoice','=',True)]", required=True)
    company_id = fields.Many2one('res.company', related='subscription_agreement_id.company_id', store=True, index=True)
    name = fields.Text(string='Description', required=True)
    quantity = fields.Float(string='Quantity', help="Quantity that will be invoiced.", default=1.0, digits='Product Unit of Measure')
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True, domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)
    price_unit = fields.Float(string='Unit Price', required=True, digits='Product Price')
    discount = fields.Float(string='Discount (%)', digits='Discount')
    price_subtotal = fields.Float(compute='_compute_amount', string='Subtotal', digits='Account', store=True)
    currency_id = fields.Many2one('res.currency', 'Currency', related='subscription_agreement_id.currency_id', store=True)
    analytic_account_id = fields.Many2one(related='subscription_agreement_id.analytic_account_id')

    @api.depends('quantity', 'discount', 'price_unit', 'subscription_agreement_id.pricelist_id', 'uom_id', 'company_id')
    def _compute_amount(self):
        """
        Compute the amounts of the Subscription line.
        """
        AccountTax = self.env['account.tax']
        for line in self:
            price = AccountTax._fix_tax_included_price_company(line.price_unit, line.product_id.sudo().taxes_id, AccountTax, line.company_id)
            price_subtotal = line.quantity * price * (100.0 - line.discount) / 100.0
            if line.subscription_agreement_id.pricelist_id.sudo().currency_id:
                price_subtotal = line.subscription_agreement_id.pricelist_id.sudo().currency_id.round(price_subtotal)
            line.update({
                'price_subtotal': price_subtotal,
            })
    

    def _amount_line_tax(self):
        self.ensure_one()
        val = 0.0
        product = self.product_id
        product_tmp = product.sudo().product_tmpl_id
        for tax in product_tmp.taxes_id.filtered(lambda t: t.company_id == self.analytic_account_id.company_id):
            fpos_obj = self.env['account.fiscal.position']
            partner = self.analytic_account_id.partner_id
            fpos = fpos_obj.with_company(self.analytic_account_id.company_id).get_fiscal_position(partner.id)
            tax = fpos.map_tax(tax, product, partner)
            compute_vals = tax.compute_all(self.price_unit * (1 - (self.discount or 0.0) / 100.0), self.analytic_account_id.currency_id, self.quantity, product, partner)['taxes']
            if compute_vals:
                val += compute_vals[0].get('amount', 0)
        return val
    
