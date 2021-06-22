# -*- coding: utf-8 -*-

import base64

from odoo import api, fields, models, tools, _
from odoo.modules.module import get_module_resource
from random import randint

CATEGORY_SELECTION = [
    ('required', 'Required'),
    ('optional', 'Optional'),
    ('no', 'None')]

class PenaltyEntryType(models.Model):
    _name = 'account.penalty.entry.type'
    _description = 'Penalty Entry Type'
    _order = 'id'
    
    name = fields.Char(string='Name', required=True, translate=True)
    active = fields.Boolean(default=True)
    description = fields.Char(string='Description')
    
    label_types = fields.Char(string='Use Types as', default='Penalty Entry', help="Label used for the subscriptions of the types.", translate=True)

    image = fields.Binary(string='Image', )
    color = fields.Integer(string='Color Index')
    company_id = fields.Many2one(
        'res.company', 'Company', copy=False,
        required=True, index=True, default=lambda s: s.env.company)
    automated_sequence = fields.Boolean('Automated Sequence?',
        help="If checked, the Approval Requests will have an automated generated name based on the given code.")
    sequence_code = fields.Char(string="Code")

    sequence_id = fields.Many2one('ir.sequence', 'Reference Purchase Subscription Sequence',
        copy=False, check_company=True)
    
    expense_advance = fields.Boolean(string='Pay Advance Expense')
    journal_id = fields.Many2one('account.journal', string="Accounting Journal", required=True, company_dependent=True, check_company=True,)

    
    #Main Type fields
    has_penalty_fields = fields.Selection(CATEGORY_SELECTION, string="Penalty Alarm & Invoices", default="no", required=True,)
    has_travel_fields = fields.Selection(CATEGORY_SELECTION, string="Asset Lifetime Invoices", default="no", required=True,)
    has_accommodation_fields = fields.Selection(CATEGORY_SELECTION, string="HSE Invoice", default="no", required=True,)
    has_pm_fields = fields.Selection(CATEGORY_SELECTION, string="PM Invoice", default="no", required=True,)
    
    #header fields    
    has_partner = fields.Selection(CATEGORY_SELECTION, string="Partner", default="no", required=True,)
    has_ref = fields.Selection(CATEGORY_SELECTION, string="Reference", default="no", required=True,)
    has_purchase_requisition = fields.Selection(CATEGORY_SELECTION, string="Requisition", default="no", required=True,)
    has_purchase = fields.Selection(CATEGORY_SELECTION, string="Purchase", default="no", required=True,)
    has_picking = fields.Selection(CATEGORY_SELECTION, string="Picking", default="no", required=True,)
    has_invoice = fields.Selection(CATEGORY_SELECTION, string="Invoice", default="no", required=True,)
    has_purchase_subscription = fields.Selection(CATEGORY_SELECTION, string="Purchase Subscription", default="no", required=True,)
    #new fields for Fleet Bill(form)
    has_supplier_inv_no = fields.Selection(CATEGORY_SELECTION, string="Supplier Invoice Number", default="no", required=True,)
    has_supplier = fields.Selection(CATEGORY_SELECTION, string="Supplier", default="no", required=True,)
    has_invoice_no = fields.Selection(CATEGORY_SELECTION, string="Invoice Number", default="no", required=True,)
    has_amount_total = fields.Selection(CATEGORY_SELECTION, string="Amount Total", default="no", required=True,)
    has_duration = fields.Selection(CATEGORY_SELECTION, string="Duration", default="no", required=True,)
    #new fields for travel bill (form)
    has_travel_by = fields.Selection(CATEGORY_SELECTION, string="Travel By", default="no", required=True,)
    has_customer_type = fields.Selection(CATEGORY_SELECTION, string="Customer Type", default="no", required=True,)
    has_effective_date = fields.Selection(CATEGORY_SELECTION, string="Effective Date", default="no", required=True,)
    has_date_of_sub = fields.Selection(CATEGORY_SELECTION, string="Date of Submission", default="no", required=True,)
    
    

    #Line Item fields(fleet bill)
    has_car_details = fields.Selection(CATEGORY_SELECTION, string="Car Detail", default="no", required=True,)
    has_driver = fields.Selection(CATEGORY_SELECTION, string="Driver", default="no", required=True,)
    has_user = fields.Selection(CATEGORY_SELECTION, string="User", default="no", required=True,)
    has_job_scope = fields.Selection(CATEGORY_SELECTION, string="Job Scope", default="no", required=True,)
    has_days = fields.Selection(CATEGORY_SELECTION, string="Days", default="no", required=True,)
    has_amount = fields.Selection(CATEGORY_SELECTION, string="Amount (MMK)", default="no", required=True,)
    has_remark = fields.Selection(CATEGORY_SELECTION, string="Remark", default="no", required=True,)
    #Line Item fields(Travel bill)
    has_category = fields.Selection(CATEGORY_SELECTION, string="Category", default="no", required=True,)
    has_from = fields.Selection(CATEGORY_SELECTION, string="From", default="no", required=True,)
    has_to = fields.Selection(CATEGORY_SELECTION, string="To", default="no", required=True,)
    has_departure_date = fields.Selection(CATEGORY_SELECTION, string="Departure Date", default="no", required=True,)
    has_arrival_date = fields.Selection(CATEGORY_SELECTION, string="Arrival Date", default="no", required=True,)
    has_number_of_days = fields.Selection(CATEGORY_SELECTION, string="Number of Days", default="no", required=True,)
    has_travel_reference = fields.Selection(CATEGORY_SELECTION, string="Travel Reference", default="no", required=True,)
    has_description = fields.Selection(CATEGORY_SELECTION, string="Description", default="no", required=True,)
    has_unit_price = fields.Selection(CATEGORY_SELECTION, string="Unit Price", default="no", required=True,)
    has_extra_charges = fields.Selection(CATEGORY_SELECTION, string="Extra Charges", default="no", required=True,)
    
    


    @api.model
    def create(self, vals):
        if vals.get('automated_sequence'):
            sequence = self.env['ir.sequence'].create({
                'name': _('Sequence') + ' ' + vals['sequence_code'],
                'padding': 5,
                'prefix': vals['sequence_code'],
                'company_id': vals.get('company_id'),
            })
            vals['sequence_id'] = sequence.id

        penalty_entry_type = super().create(vals)
        return penalty_entry_type

    def write(self, vals):
        if 'sequence_code' in vals:
            for penalty_entry_type in self:
                sequence_vals = {
                    'name': _('Sequence') + ' ' + vals['sequence_code'],
                    'padding': 5,
                    'prefix': vals['sequence_code'],
                }
                if penalty_entry_type.sequence_id:
                    penalty_entry_type.sequence_id.write(sequence_vals)
                else:
                    sequence_vals['company_id'] = vals.get('company_id', penalty_entry_type.company_id.id)
                    sequence = self.env['ir.sequence'].create(sequence_vals)
                    penalty_entry_type.sequence_id = sequence
        if 'company_id' in vals:
            for penalty_entry_type in self:
                if penalty_entry_type.sequence_id:
                    penalty_entry_type.sequence_id.company_id = vals.get('company_id')
        return super().write(vals)
    
    def create_request(self):
        self.ensure_one()
        if self.automated_sequence:
            name = self.sequence_id.next_by_id()
        else:
            name = self.name
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.penalty.entry",
            "views": [[False, "form"]],
            "context": {
                'form_view_initial_mode': 'edit',
                'default_name': name,
                'default_penalty_entry_type_id': self.id,
                'default_user_id': self.env.user.id,
            },
        }