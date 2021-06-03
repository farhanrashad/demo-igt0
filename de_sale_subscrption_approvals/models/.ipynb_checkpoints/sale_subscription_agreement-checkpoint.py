from odoo import models, fields, api, _

class SalesubscriptionAgreement(models.Model):
    _inherit = 'sale.subscription.agreement'
    
    
    category_id = fields.Many2one('approval.category', related='subscription_type_id.category_id', string="Category", required=False)
    approval_request_id = fields.Many2one('approval.request', string='Approval Request', copy=False, readonly=True)
    request_status = fields.Selection(related='approval_request_id.request_status')
    
    
    

    
    
    
    @api.model
    def create(self, vals):
        sheet = super(SalesubscriptionAgreement, self.with_context(mail_create_nosubscribe=True, mail_auto_subscribe_no_notify=True)).create(vals)
        if sheet.category_id:
            sheet.action_submit()
        return sheet
    

    
    
    def action_submit(self):
        approver_ids  = []
        
        request_list = []
        for line in self:
            
            request_list.append({
                'name': line.partner_id.name + ' Has Sale Subscriptions on ' + str(line.subscription_agreement_date)+ ' For Recurring Price ' + str(line.recurring_total) + ' Sequence# ' +' ' + str(line.name) ,
                'request_owner_id': line.partner_id.user_id.id,
                'category_id': line.category_id.id,
                'sale_subscription_id': line.id,
                'reason': line.partner_id.name + ' Has Sale Subscriptions on ' + str(line.subscription_agreement_date)+ ' For Recurring Price ' + str(line.recurring_total) + ' Sequence# ' +' ' + str(line.name) ,
                'request_status': 'new',
            })
            approval_request_id = self.env['approval.request'].create(request_list)
            approval_request_id._onchange_category_id()
            approval_request_id.action_confirm()
            line.approval_request_id = approval_request_id.id
