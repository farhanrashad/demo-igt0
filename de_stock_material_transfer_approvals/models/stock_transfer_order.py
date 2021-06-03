# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import datetime, time

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class StockTransferOrder(models.Model):
    _inherit = 'stock.transfer.order'

    
    category_id = fields.Many2one('approval.category', string="Wrorkflow", required=True, domain="[('approval_type','=','ir')]")

    approval_state = fields.Selection([
        ('new', 'Draft'),
        ('pending', 'In Approval'),
        ('approved', 'Approved')
    ],default='new')

    approval_request_id = fields.Many2one('approval.request', string='Approval Request', copy=False, readonly=True)
    request_status = fields.Selection(related='approval_request_id.request_status')
    approvers_count = fields.Integer(compute='_compute_approvers_count')

    def _compute_approvers_count(self):
        Approvers = self.env['approval.approver']
        can_read = Approvers.check_access_rights('read', raise_exception=False)
        for transfer in self:
            transfer.approvers_count = can_read and Approvers.search_count([('stock_transfer_order_id', '=', transfer.id)]) or 0
        
    def action_submit(self):
        approver_ids  = []
        request_list = []
        for transfer in self:
            request_list.append({
                'name': transfer.name,
                'request_owner_id': transfer.user_id.id,
                'category_id': transfer.category_id.id,
                'stock_transfer_order_id': transfer.id,
                'reason': transfer.user_id.name + ' Has requested ' + transfer.name + ' for approval.' ,
                'request_status': 'new',
            })
            approval_request_id = self.env['approval.request'].create(request_list)
            approval_request_id._onchange_category_id()
            approval_request_id.action_confirm()
            transfer.approval_request_id = approval_request_id.id
        self.approval_state = 'pending'
