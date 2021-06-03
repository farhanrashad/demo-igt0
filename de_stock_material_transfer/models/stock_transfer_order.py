# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date

class StockTransferOrder(models.Model):
    _name = 'stock.transfer.order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Stock Transfer Order'
    _order = 'date_order desc, id desc'
    _check_company_auto = True

    def _get_default_stage_id(self):
        return self.env['stock.transfer.order.stage'].search([], order='sequence', limit=1)
    
    def _get_type_id(self):
        return self.env['stock.transfer.order.type'].search([], limit=1)
    
    def _get_default_category_id(self):
        return self.env['stock.transfer.order.category'].search([('transfer_order_type_id','=',self.transfer_order_type_id.id)], limit=1)
    
    
    def _get_default_location(self):
        location_id = self.env['stock.location'].search([('return_location','=',True)],limit=1)
        return location_id
    
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    transfer_order_type_id = fields.Many2one('stock.transfer.order.type', string='Transfer Type', index=True, required=True, default=_get_type_id, readonly=True, states={'draft': [('readonly', False)],'in_progress': [('readonly', False)]},)
    code = fields.Char(related='transfer_order_type_id.code')
    sequence_code = fields.Char(String="Sequence Code")
    
    @api.onchange('transfer_order_type_id')
    def _check_code(self):
        self.sequence_code = self.code    
    
    transfer_order_category_id = fields.Many2one('stock.transfer.order.category', string='Transfer Category', index=True, readonly=True, copy=False, domain="[('transfer_order_type_id','=',transfer_order_type_id)]",default=_get_default_category_id,  states={'draft': [('readonly', False)],'in_progress': [('readonly', False)]},)
    action_type = fields.Selection(related='transfer_order_category_id.action_type')
    disallow_staging = fields.Boolean(related='transfer_order_type_id.disallow_staging')
    filter_products = fields.Boolean(related='transfer_order_category_id.filter_products')
    categ_control_ids = fields.Many2many(related='transfer_order_category_id.categ_control_ids')
    
    partner_id = fields.Many2one('res.partner', 'Contractor',check_company=True, readonly=True, states={'draft': [('readonly', False)]},)

    state = fields.Selection([
        ('draft', 'New'),
        ('confirm', 'Confirmed'),
        ('process', 'Inprocess'),
        ('done', 'Closed'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, tracking=4, default='draft')
    
    stage_id = fields.Many2one('stock.transfer.order.stage', string='Stage', compute='_compute_stage_id',
        store=True, readonly=False, ondelete='restrict', tracking=True, index=True,
        default=_get_default_stage_id, copy=False)
    next_stage_id = fields.Many2one('stock.transfer.order.stage',compute='_compute_next_stage')
    prv_stage_id = fields.Many2one('stock.transfer.order.stage',related='stage_id.prv_stage_id')
    stage_category = fields.Selection(related='stage_id.stage_category')
    next_stage_category = fields.Selection(related='next_stage_id.stage_category')
    prv_stage_category = fields.Selection(related='next_stage_id.stage_category')
    stage_code = fields.Char(related='stage_id.stage_code')
    
    #exceptions or transactions
    transfer_exception_type_id = fields.Many2one("stock.transfer.exception.type", string="Exception Type", domain="[('transfer_order_type_id','=',transfer_order_type_id)]")
    transaction_code = fields.Char(related='transfer_exception_type_id.code', string='T Code')
    txn_stage_id = fields.Many2one('stock.transfer.order.stage', related='transfer_exception_type_id.stage_id', string='TXN Stage')
    
    #exception with multiple lines
    stock_transfer_txn_line = fields.One2many('stock.transfer.txn.line', 'stock_transfer_order_id', string='Transaction Line', copy=True, auto_join=True,)
    #transfer_txn_type_ids = fields.Many2many("stock.transfer.exception.type", string="TXN Types", domain="[('transfer_order_type_id','=',transfer_order_type_id)]")
    curr_txn_type_id = fields.Many2one("stock.transfer.exception.type", string="Currenct TXN Type", compute='_compute_all_txn')
    txn_stage_ids = fields.Many2many("stock.transfer.order.stage", string="TXN Stages", compute='_compute_all_txn')
    curr_txn_stage_id = fields.Many2one("stock.transfer.order.stage", related='curr_txn_type_id.stage_id')
    message_type = fields.Selection(related='curr_txn_type_id.message_type')
    exception_message = fields.Char(related='curr_txn_type_id.message', string='Exception')


    
    close_reason_id = fields.Many2one("stock.transfer.close.reason", string="Close Reason", copy=False, tracking=True, readonly=True)
    close_reason_message = fields.Char(string='Close Message', readonly=True)
    date_closed = fields.Datetime(string='Closed Date', readonly=True)

    date_request = fields.Datetime(string='Request Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)],'in_progress': [('readonly', False)] }, copy=False, default=fields.Datetime.now, help="Order request date")

    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)],'in_progress': [('readonly', False)] }, copy=False, default=fields.Datetime.now, help="Order confirmation date")
    date_scheduled = fields.Datetime(string='Date Scheduled', required=True, readonly=True, index=True, states={'draft': [('readonly', False)],'in_progress': [('readonly', False)] }, copy=False, default=fields.Datetime.now, help="Deadline schedule date")
    delivery_deadline = fields.Datetime(string='Delivery Deadline', required=True, readonly=True, index=True, states={'draft': [('readonly', False)],'in_progress': [('readonly', False)] }, copy=False, default=fields.Datetime.now, help="Delivery Deadline")
    return_deadline = fields.Datetime(string='Return Deadline', readonly=False, compute='_compute_return_deadline', states={'draft': [('readonly', False)],'in_progress': [('readonly', False)] }, copy=False, help="Retrun Material Deadline")
    date_delivered = fields.Datetime(string="Actual Delivery", compute="_compute_all_dates")
    date_returned = fields.Datetime(string="Actual Return", compute="_compute_all_dates")
    
    stock_transfer_order_line = fields.One2many('stock.transfer.order.line', 'stock_transfer_order_id', string='Transfer Line', copy=True, auto_join=True,readonly=True, states={'draft': [('readonly', False)],'in_progress': [('readonly', False)]},)
    
    stock_transfer_return_line = fields.One2many('stock.transfer.return.line', 'stock_transfer_order_id', string='Return Transfer Line', copy=True, auto_join=True,readonly=True, states={'draft': [('readonly', False)],'in_progress': [('readonly', False)]},)

        
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company, readonly=True, states={'draft': [('readonly', False)],'in_progress': [('readonly', False)]},)
    description = fields.Text()
    user_id = fields.Many2one('res.users', string="Request Owner",check_company=True, domain="[('company_ids', 'in', company_id)]", default=lambda self: self.env.user, required=True,readonly=True, states={'draft': [('readonly', False)]},)
    
    delivery_count = fields.Integer(compute='_compute_picking_count', string='Number of Delivery')
    return_count = fields.Integer(compute='_compute_picking_count', string='Number of Return')
    picking_ids = fields.One2many('stock.picking', 'stock_transfer_order_id', string='Picking', states={'done': [('readonly', True)]})
    bill_count = fields.Integer(compute='_compute_bill_count')

    location_src_id = fields.Many2one('stock.location', string='Source Location', readonly=True, states={'draft': [('readonly', False)]},)
    location_dest_id = fields.Many2one('stock.location', string='Destination Location', readonly=True, states={'draft': [('readonly', False)]},)
    picking_type_id = fields.Many2one('stock.picking.type', related='transfer_order_category_id.picking_type_id' )
    picking_type_code = fields.Selection(related='picking_type_id.code')
    sequence_id = fields.Many2one('ir.sequence', 'Reference Sequence',
        copy=False, check_company=True)
    
    #optional fields
    #has_penalty = fields.Boolean(related="transfer_order_category_id.has_penalty", ondelete='set default')
    #has_closed = fields.Boolean(related="transfer_order_category_id.has_closed", ondelete='set default')
    
    has_reference = fields.Selection(related="transfer_order_category_id.has_reference")
    has_purchase_order = fields.Selection(related="transfer_order_category_id.has_purchase_order")
    has_transfer_order = fields.Selection(related="transfer_order_category_id.has_transfer_order")
    has_transporter = fields.Selection(related="transfer_order_category_id.has_transporter")
    has_analytic_account = fields.Selection(related="transfer_order_category_id.has_analytic_account")
    has_analytic_tags = fields.Selection(related="transfer_order_category_id.has_analytic_tags")
    has_supplier = fields.Selection(related="transfer_order_category_id.has_supplier")
    has_tower_info = fields.Selection(related="transfer_order_category_id.has_tower_info")

    
    reference = fields.Char(string="Reference")
    purchase_id = fields.Many2one('purchase.order', string='Purchase Order')
    stock_transfer_order_id = fields.Many2one('stock.transfer.order', string='Transfer Order')
    transporter_id = fields.Many2one('res.partner', string='Transporter')
    
    @api.onchange('transfer_order_category_id')
    def _onchange_transfer_order_category_id(self):
        self.stage_id = self.env['stock.transfer.order.stage'].search([('transfer_order_category_ids','=',self.transfer_order_category_id.id)], limit=1).id
    
    def write(self,vals):
        #if vals.get('stage_id'):
        stage_id = self.env['stock.transfer.order.stage'].browse(vals.get('stage_id'))
            #txn_ids = self.env['stock.transfer.exception.type'].search([('apply_stage_id','=',vals.get('stage_id')),('stage_auto_apply','=',True)])
        txn_ids = self.env['stock.transfer.exception.type'].search([('apply_stage_id','=',stage_id.id),('stage_auto_apply','=',True)])

        for txn in txn_ids:
            self.env['stock.transfer.txn.line'].create({
                'stock_transfer_order_id': self.id,
                'transfer_exception_type_id': txn.id,
            })
            #self.stock_transfer_txn_line.sudo().create({
            #    'stock_transfer_order_id': self.id,
            #    'transfer_exception_type_id': txn.id,
            #})
        result = super(StockTransferOrder, self).write(vals)
        return result
    #@api.depends('stage_id','txn_stage_id')
    @api.depends('stage_id','curr_txn_stage_id')
    def _compute_next_stage(self):
        next_stage = self.stage_id.id
        for order in self:
            if not order.curr_txn_stage_id.id == order.stage_id.id:
                if order.curr_txn_stage_id.next_stage_id.id == order.stage_id.next_stage_id.id:
                    next_stage = self.curr_txn_stage_id.id
                else:
                    next_stage = self.stage_id.next_stage_id.id
            else:
                next_stage = self.stage_id.next_stage_id.id
            order.next_stage_id = next_stage
        #for order in self:
        #    if not order.txn_stage_id.id == order.stage_id.id:
        #        if order.txn_stage_id.next_stage_id.id == order.stage_id.next_stage_id.id:
        #            next_stage = self.txn_stage_id.id
        #        else:
        #            next_stage = self.stage_id.next_stage_id.id
        #    else:
        #        next_stage = self.stage_id.next_stage_id.id
        #    order.next_stage_id = next_stage
    
    @api.model
    def cron_expire_order(self):
        #picking = self.env['stock.picking'].search([('stock_transfer_order_id', '=', self.id),('picking_type_id', '=', self.transfer_order_category_id.return_picking_type_id.id)],limit=1)
        
        today = fields.Datetime.now()
        # set to close if date is passed
        domain_close = [('return_deadline', '<', today), ('date_returned', '=', False), ('stage_category', 'in', ['progress','confirm'])]
        order_close = self.search(domain_close)
        #order_close = self
        #for picking in self.picking_ids.filtered(lambda p: p.picking_type_id.id == self.transfer_order_category_id.picking_type_id.id):
            #if picking.id:
        self.update({
            'close_reason_message' : 'Document expired automatically',
        })
        order_close.set_close()
        #return dict(closed=order_close.ids)
        return self._cancel_delivery(automatic=True)
    
    
    def _cancel_delivery(self, automatic=False):
        auto_commit = self.env.context.get('auto_commit', True)
        cr = self.env.cr
        picking = self.env['stock.picking'].search([('stock_transfer_order_id', '=', self.id),('picking_type_id', '=', self.transfer_order_category_id.return_picking_type_id.id)],limit=1)
        picking.sudo().action_cancel()
        for order in self:
            order.write({
                'close_reason_message' : 'Document expired automatically',
                'date_closed': fields.Date.from_string(fields.Date.context_today(self)),
            })
        cr.commit()
        if auto_commit:
            cr.commit()
            
    @api.depends('transfer_order_type_id','transfer_order_category_id')
    def _compute_stage_id1(self):
        for order in self:
            if not order.stage_id:
                order.stage_id = lead._stage_find(order.transfer_order_type_id.id, order.transfer_order_category_id.id, domain=[('fold', '=', False),('stage_category', '=', 'draft')]).id
    
    def _stage_find(self, type_id=None, category_id=None, domain=None, order='sequence'):
        if category_id:
            search_domain = [('transfer_order_category_ids', '=', category_id)]
        if domain:
            search_domain += list(domain)
        return self.env['stock.transfer.order.stage'].search(search_domain, order=order, limit=1)
    
    @api.depends('transfer_order_type_id')
    def _compute_stage_id(self):
        for order in self:
            if order.transfer_order_type_id:
                if order.transfer_order_type_id not in order.stage_id.transfer_order_type_ids:
                    order.stage_id = order.stage_find(order.transfer_order_type_id.id, [('fold', '=', False), ('stage_category', '=', 'draft')])
            else:
                order.stage_id = False
    
    def stage_find(self, section_id, domain=[], order='sequence'):
        section_ids = category_ids = []
        if section_id:
            section_ids.append(section_id)
        section_ids.extend(self.mapped('transfer_order_type_id').ids)
        search_domain = []
        if section_ids:
            search_domain = [('|')] * (len(section_ids) - 1)
            for section_id in section_ids:
                search_domain.append(('transfer_order_type_ids', '=', section_id))
        """
        if category_id:
            category_ids.append(category_id)
        category_ids.extend(self.mapped('transfer_order_category_id').ids)
        search_domain = []
        if category_ids:
            search_domain = [('|')] * (len(category_ids) - 1)
            for category_id in category_ids:
                search_domain.append(('transfer_order_category_ids', '=', category_id))
        """       
        search_domain += list(domain)
        # perform search, return the first found
        return self.env['stock.transfer.order.stage'].search(search_domain, order=order, limit=1).id
    
    def _compute_all_txn(self):
        transfer_order_type_id = self.curr_txn_type_id
        stage_id = self.stage_id
        stage = []
        if self.stock_transfer_txn_line:
            for txn in self.stock_transfer_txn_line.filtered(lambda t: t.txn_action == 'open').sorted(key=lambda r: r.sequence):
                transfer_order_type_id = txn.transfer_exception_type_id
                break
        self.curr_txn_type_id = transfer_order_type_id
        self.txn_stage_ids = [(6, 0, self.stock_transfer_txn_line.txn_stage_id.ids)]
            #for txn in self.stock_transfer_txn_line.filtered(lambda t: t.txn_action == 'open').sorted(key=lambda r: r.sequence):
             #   stages.append({
              #      'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
               # })
    #@api.onchange('transfer_exception_type_id')
    #def _onchange_transfer_exception_type_id(self):
    #    if self.transfer_exception_type_id.stage_id:
    #        self.stage_id = self.transfer_exception_type_id.stage_id.id

    def set_close(self):
        today = fields.Date.from_string(fields.Date.context_today(self))
        stage_id = self.env['stock.transfer.order.stage'].search([('transfer_order_type_ids','=',self.transfer_order_type_id.id),('stage_category','=','close')])
        for sub in self:
            sub.write({
                'stage_id': stage_id.id, 
                'date_closed': today,
            })
        return True
        
    #@api.onchange('picking_type_id')
    #def _onchange_picking_type(self):
        #for line in self:
            #line.location_src_id = line.picking_type_id.default_location_src_id
            #line.location_dest_id = line.picking_type_id.default_location_dest_id
    
    @api.onchange('transfer_order_category_id')
    def _onchange_trasnfer_order_category(self):
        if self.transfer_order_category_id:
            self.location_src_id = self.transfer_order_category_id.location_src_id.id
            self.location_dest_id = self.transfer_order_category_id.location_dest_id.id
            ddays = self.transfer_order_category_id.default_delivery_validity
            ldays = self.transfer_order_category_id.delivery_lead_days
            if ddays > 0:
                self.delivery_deadline = fields.Date.to_string(datetime.now() + timedelta(ddays))
                self.date_scheduled = fields.Date.to_string(datetime.now() + timedelta(ldays))
        

    
    def _compute_all_dates(self):
        ddt = rdt = False
        pickings = self.env['stock.picking']
        for order in self:
            pickings = self.env['stock.picking'].search([('stock_transfer_order_id','=',order.id),('picking_type_id','=',order.picking_type_id.id),('state','=','done')])
        for picking in pickings:
            if picking.date_done:
                ddt = picking.date_done
        for order in self:
            pickings = self.env['stock.picking'].search([('stock_transfer_order_id','=',order.id),('picking_type_id','=',order.transfer_order_category_id.return_picking_type_id.id),('state','=','done')])
        for picking in pickings:
            if picking.date_done:
                rdt = picking.date_done
        self.date_delivered = ddt
        self.date_returned = rdt
        
    def _compute_return_deadline(self):  
        dt = False
        days = 0
        for order in self:
            if order.date_delivered:
                days = order.transfer_order_category_id.default_return_validity
                dt = fields.Date.to_string(order.date_delivered + timedelta(days))
        self.return_deadline = dt
        
    @api.model
    def create(self, vals):            
        vals['name'] = (
        vals.get('code') or
        self.env.context.get('default_code') or
        self.env['ir.sequence'].with_company(vals.get('company_id')).next_by_code('stock.transfer.order') or
         'New'
        )
        sequence = self.env['ir.sequence'].search([('prefix','=', vals['sequence_code'])
        ], limit=1)
        vals['sequence_id'] = sequence.id
        vals['name'] = sequence.next_by_id()
        transfer_order = super(StockTransferOrder, self).create(vals)
        
        
        return transfer_order


        
    """
    @api.model
    def create(self, vals):
        vals['code'] = (
            vals.get('code') or
            self.env.context.get('default_code') or
            self.env['ir.sequence'].with_company(vals.get('company_id')).next_by_code('stock.transfer.order') or
            'New'
        )
        result = super(StockTransferOrder, self).create(vals)       
        return result
        
    @api.model
    def create1(self, vals):
        if 'company_id' in vals:
            self = self.with_company(vals['company_id'])
        if vals.get('name', _('New')) == _('New'):
            seq_date = None
            if 'refill_date' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
            vals['name'] = self.env['ir.sequence'].next_by_code('stock.transfer.order', sequence_date=seq_date) or _('New')
        result = super(StockTransferOrder, self).create(vals)       
        return result
        
        """ 
    
    def action_draft(self):
        self.state = 'draft'
    
    def action_confirm(self):
        for order in self:
            if order.next_stage_id.id == order.curr_txn_stage_id.id:
                for txn in self.stock_transfer_txn_line.filtered(lambda t: t.transfer_exception_type_id.id == order.curr_txn_type_id.id):
                    txn.txn_action = 'apply'
                    for line in order.stock_transfer_order_line:
                        if txn.transfer_exception_type_id.location_src_id:
                            line.location_src_id = txn.transfer_exception_type_id.location_src_id.id
                        if txn.transfer_exception_type_id.location_dest_id:
                            line.location_dest_id = txn.transfer_exception_type_id.location_dest_id.id
                    #for line in order.stock_transfer_return_line:
                     #   if txn.transfer_exception_type_id.location_dest_id:
                      #      line.location_dest_id = txn.transfer_exception_type_id.location_dest_id.id
                            
        self.update({
            'stage_id' : self.next_stage_id.id,
            'date_order': fields.Datetime.now(),
        })
    def action_refuse(self):
        
        self.update({
            'stage_id' : self.prv_stage_id.id,
            'date_order': fields.Datetime.now(),
        })
        
        
    def action_submit(self):
        self.ensure_one()
        if not self.stock_transfer_order_line:
            raise UserError(_("You cannot submit requisition '%s' because there is no product line.", self.name))
        self.update({
            'stage_id' : self.next_stage_id.id,
        })
        
    def action_done(self):
        """
        Generate all stock order based on selected lines, should only be called on one agreement at a time
        """
        if any(picking.state in ['draft', 'sent', 'to approve'] for picking in self.mapped('picking_ids')):
            raise UserError(_('You have to cancel or validate every Transfer before closing the Transfer order.'))
        self.write({'state': 'done'})
        
    def action_cancel(self):
        self.state = 'cancel'
        
    def unlink(self):
        if any(transfer.order.state not in ('draft', 'cancel') for transfer.order in self):
            raise UserError(_('You can only delete draft transfer.order orders.'))
        self.mapped('stock_transfer.order_line').unlink()
        return super(Stocktransfer.orderOrder, self).unlink()
    
    def create_delivery(self):
        self._create_delivery()
        if self.action_type != 'normal':
            self._create_return()
        self.stage_id = self.next_stage_id.id,
        #return self.action_subscription_invoice()
        
    def _create_delivery(self):
        self.ensure_one()
        picking = self.env['stock.picking']
        lines_data = []
        line = False
        for order in self:
            for line in order.stock_transfer_order_line:
                lines_data.append([0,0,{
                    #'reference': order.name,
                    'product_id': line.product_id.id,
                    'product_uom': line.product_id.uom_po_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'origin': order.name,
                    'name': order.name,
                    'date_deadline': order.date_scheduled,
                    'location_id': line.location_src_id.id,
                    'location_dest_id': line.location_dest_id.id,
                    'stock_transfer_order_line_id': line.id,
                }])
        picking.create({
            'picking_type_id':self.picking_type_id.id,
            'partner_id': order.partner_id.id,
            'location_id': self.location_src_id.id,
            'location_dest_id':self.location_dest_id.id,
            'scheduled_date':self.date_scheduled,
            'origin':self.name,
            'stock_transfer_order_id':self.id,
            'state': 'draft',
            'move_lines':lines_data,
        })
        
        return picking
    
    def _create_return(self):
        self.ensure_one()
        picking = self.env['stock.picking']
        origin_picking_id = self.env['stock.picking']
        lines_data = []
        order = False
        Line = False
        origin_picking_id = self.env['stock.picking'].search([('stock_transfer_order_id','=',self.id),('picking_type_id','=',self.picking_type_id.id),('state','!=','cancel')],limit=1)

        for order in self:
            for line in order.stock_transfer_return_line:
                lines_data.append([0,0,{
                    #'reference': order.name,
                    'product_id': line.product_id.id,
                    'product_uom': line.product_id.uom_po_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'origin': 'return of ' + origin_picking_id.name,
                    'name': order.name,
                    'date_deadline': order.date_scheduled,
                    'location_id': line.location_dest_id.id,
                    'location_dest_id': order.transfer_order_category_id.return_location_id.id,
                    'stock_transfer_order_line_id': line.id,
                    'origin_returned_move_id': self.env['stock.move'].search([('stock_transfer_order_line_id','=',line.id),('picking_id','=',origin_picking_id.id)]).id
                }])
            picking.create({
                'picking_type_id':order.transfer_order_category_id.return_picking_type_id.id,
                'partner_id': order.partner_id.id,
                'location_id': order.location_dest_id.id,
                'location_dest_id':order.transfer_order_category_id.return_location_id.id,
                'scheduled_date':self.date_scheduled,
                'origin': 'return of ' + origin_picking_id.name,
                'stock_transfer_order_id':self.id,
                'state': 'draft',
                'move_lines':lines_data,
            })
        
        return picking
    
    
    def _compute_picking_count(self):
        Picking = self.env['stock.picking']
        can_read = Picking.check_access_rights('read', raise_exception=False)
        for order in self:
            order.delivery_count = can_read and Picking.search_count([('stock_transfer_order_id', '=', order.id),('picking_type_id', '=', order.picking_type_id.id),('state', '!=', 'cancel')]) or 0
            order.return_count = can_read and Picking.search_count([('stock_transfer_order_id', '=', order.id),('picking_type_id', '=', order.transfer_order_category_id.return_picking_type_id.id),('state', '!=', 'cancel')]) or 0

    def action_view_delivery(self):
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")
        pickings = self.env['stock.picking'].search([('stock_transfer_order_id', '=', self.id),('picking_type_id', '=', self.picking_type_id.id),('state', '!=', 'cancel')])
        if len(pickings) > 1:
            action['domain'] = [('stock_transfer_order_id', '=', self.id),('picking_type_id', '=', self.picking_type_id.id),('state', '!=', 'cancel')]
        elif pickings:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = pickings.id
        # Prepare the context.
        picking_id = pickings.filtered(lambda l: l.picking_type_id.code == self.picking_type_id.id)
        if picking_id:
            picking_id = picking_id[0]
        else:
            picking_id = pickings[0]
        action['context'] = dict(self._context, default_partner_id=self.partner_id.id, default_picking_type_id=picking_id.picking_type_id.id, default_origin=self.name, default_group_id=picking_id.group_id.id)
        return action
    
    def action_view_receipt(self):
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")
        #pickings = self.mapped('picking_ids')
        pickings = self.env['stock.picking'].search([('stock_transfer_order_id', '=', self.id),('picking_type_id', '=', self.transfer_order_category_id.return_picking_type_id.id),('state', '!=', 'cancel')])
        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids),('picking_type_id', '=', self.transfer_order_category_id.return_picking_type_id.id)]
        elif pickings:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = pickings.id
        # Prepare the context.
        
        return action
    
    def _compute_bill_count(self):
        Bill = self.env['account.move']
        can_read = Bill.check_access_rights('read', raise_exception=False)
        for order in self:
            order.bill_count = can_read and Bill.search_count([('stock_transfer_order_id', '=', order.id)]) or 0

    def action_view_credit_note(self):
        self.ensure_one()
        invoices = self.env['account.move'].search([('stock_transfer_order_id', 'in', self.ids)])
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
    
    
class StockTransferOrderLine(models.Model):
    _name = 'stock.transfer.order.line'
    _description = 'Stock transfer.order Line'
    
    stock_transfer_order_id = fields.Many2one('stock.transfer.order', string='Stock transfer.order Order', required=True, ondelete='cascade', index=True, copy=False)
    transfer_order_type_id = fields.Many2one(related='stock_transfer_order_id.transfer_order_type_id', readonly=True, store=True)
    transfer_order_category_id = fields.Many2one(related='stock_transfer_order_id.transfer_order_category_id', readonly=True, store=True)
    stage_id = fields.Many2one(related='stock_transfer_order_id.stage_id', readonly=True,store=True)
    state = fields.Selection(related='stock_transfer_order_id.state', readonly=True)
    stage_category = fields.Selection(related='stock_transfer_order_id.stage_category', store=True)
    action_type = fields.Selection(related='stock_transfer_order_id.action_type', store=True)
    date_request = fields.Datetime(realted='stock_transfer_order_id.date_request', readonly=True)
    date_order = fields.Datetime(realted='stock_transfer_order_id.date_order', readonly=True)
    
    partner_id = fields.Many2one('res.partner', related='stock_transfer_order_id.partner_id', readonly=True,store=True)
    user_id = fields.Many2one('res.users', related='stock_transfer_order_id.user_id', readonly=True,store=True)

    name = fields.Text(string='Description', required=True)
    product_id = fields.Many2one('product.product', string='Product', change_default=True, ondelete='restrict', )
    categ_id = fields.Many2one('product.category', related='product_id.categ_id')
    categ_control_ids = fields.Many2many(related='stock_transfer_order_id.categ_control_ids')
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)
    product_uom_qty = fields.Float(string='Demand Qty', required=True)
    
    delivered_qty = fields.Float(string='Dlvr. Qty', compute='_compute_delivered_qty')    
    date_scheduled = fields.Date(string='Scheduled Date')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',)
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string="Analytic Tags")
    supplier_id = fields.Many2one('res.partner', string='Supplier')
    project_id = fields.Many2one('project.project', string='Project')
    state = fields.Selection(related='stock_transfer_order_id.state')
    location_src_id = fields.Many2one('stock.location', string='From', required=True,)
    location_dest_id = fields.Many2one('stock.location', string='To', required=True,)
    
    return_product_id = fields.Many2one('product.product', string='Product', compute='_compute_product_return' )
    return_product_uom_qty = fields.Float(string='Return Qty', compute='_compute_product_return')

    
    site_type = fields.Selection([
        ('gbt', 'GBT'), 
        ('rtp', 'RTP'),
    ], string="Site Type", default="gbt")
    tower_height = fields.Float(string='Tower Height')
    kpa = fields.Integer(string='KPA')
    wind_zone = fields.Integer(string='Wind Zone')
    
    
    delivery_status = fields.Selection([
        ('draft', 'New'), ('cancel', 'Cancelled'),
        ('waiting', 'Waiting Another Move'),
        ('confirmed', 'Waiting Availability'),
        ('partially_available', 'Partially Available'),
        ('assigned', 'Available'),
        ('done', 'Done')],string="Status", compute="_get_delivery_status")
    
    
    @api.onchange('project_id')
    def onchange_project_id(self):
        if not self.analytic_account_id:
            self.analytic_account_id = self.project_id.analytic_account_id.id
    
    def _compute_product_return(self):
        for line in self:
            qty = 0
            returns = self.env['stock.transfer.return.line'].search([('stock_transfer_order_id','=',self.stock_transfer_order_id.id),('categ_id','=',self.categ_id.id)])
            for rtn in returns:
                qty += rtn.product_uom_qty
            line.return_product_uom_qty = qty
        
    def _get_delivery_status(self):
        #status = ''
        picking_code = ''
        for line in self:
            if line.stock_transfer_order_id.action_type != 'normal':
                if line.stock_transfer_order_id.state == 'delivered':
                    picking_code = line.stock_transfer_order_id.transfer_order_category_id.return_picking_type_id.code
                else:
                    picking_code = line.stock_transfer_order_id.picking_type_code
            else:
                picking_code = line.stock_transfer_order_id.picking_type_code
            stock_move = self.env['stock.move'].search([('stock_transfer_order_line_id','=',line.id),('picking_code','=',picking_code)],limit=1)
            status = stock_move.state
        self.delivery_status = status
    
    def _get_return_product(self):
        #status = ''
        product_id = False
        picking_code = False
        for line in self:
            if line.stock_transfer_order_id.action_type != 'normal':
                if line.stock_transfer_order_id.transfer_order_category_id.return_picking_type_id:
                    picking_code = line.stock_transfer_order_id.transfer_order_category_id.return_picking_type_id.code
                    stock_move = self.env['stock.move'].search([('stock_transfer_order_line_id','=',line.id),('picking_code','=',picking_code)],limit=1)
                    product_id = stock_move.product_id.id
        self.return_product_id = product_id
        
    def _compute_all_qty(self):
        del_qty = rcv_qty = 0
        move_lines = self.env['stock.move']
        for line in self:
            del_qty = rcv_qty = 0
            move_lines = self.env['stock.move'].search([('stock_transfer_order_line_id', '=', line.id),('picking_id.stock_transfer_order_id', '=', line.stock_transfer_order_id.id), ('state', '=', 'done'),('picking_id.picking_type_id','=', line.stock_transfer_order_id.picking_type_id.id)],limit=1)
            for move in move_lines:
                del_qty = move.quantity_done
            
        self.update({
            'delivered_qty': del_qty,
            'received_qty' :rcv_qty,
        })
    
    def _compute_delivered_qty(self):
        for line in self:
            if line.product_id.id:
                stock_move_obj = self.env['stock.move']
                domain = [('stock_transfer_order_line_id', '=', line.id),
                          ('picking_code', '=', line.stock_transfer_order_id.picking_type_code),           
                         ]
                where_query = stock_move_obj._where_calc(domain)
                stock_move_obj._apply_ir_rules(where_query, 'read')
                from_clause, where_clause, where_clause_params = where_query.get_sql()
                select = "SELECT SUM(product_qty) from " + from_clause + " where " + where_clause
            self.env.cr.execute(select, where_clause_params)
            line.delivered_qty = self.env.cr.fetchone()[0] or 0.0
    
    
            
            
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.product_tmpl_id.name
            self.product_uom = self.product_id.uom_po_id
            self.product_uom_qty = 1.0
            self.location_src_id = self.stock_transfer_order_id.location_src_id.id
            self.location_dest_id = self.stock_transfer_order_id.location_dest_id.id
        if not self.date_scheduled:
            self.date_scheduled = self.stock_transfer_order_id.date_scheduled
            
    def action_view_transfer_order(self):
        action = self.env["ir.actions.actions"]._for_xml_id("action_stock_transfer_order_pending")
        pickings = self.env['stock.transfer.order.order'].search([('id', '=', self.stock_transfer_order_id.id)])
        if len(pickings) > 1:
            action['domain'] = [('id', '=', self.stock_transfer_order_id.id)]
        elif pickings:
            form_view = [(self.env.ref('de_stock_transfer_order.stock_transfer_order_form_view').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = pickings.id
        # Prepare the context.
        picking_id = pickings.filtered(lambda l: l.picking_type_id.code == self.picking_type_id.id)
        if picking_id:
            picking_id = picking_id[0]
        else:
            picking_id = pickings[0]
        action['context'] = dict(self._context, default_partner_id=self.partner_id.id, default_picking_type_id=picking_id.picking_type_id.id, default_origin=self.name, default_group_id=picking_id.group_id.id)
        return action
    
    
class StockTransferReturnLine(models.Model):
    _name = 'stock.transfer.return.line'
    _description = 'Stock transfer Return Line'
    
    stock_transfer_order_id = fields.Many2one('stock.transfer.order', string='Stock transfer.order Order', required=True, ondelete='cascade', index=True, copy=False)
    state = fields.Selection(related='stock_transfer_order_id.state', readonly=True)
    partner_id = fields.Many2one('res.partner', related='stock_transfer_order_id.partner_id', readonly=True)
    user_id = fields.Many2one('res.users', related='stock_transfer_order_id.user_id', readonly=True)

    name = fields.Text(string='Description', required=True)
    product_id = fields.Many2one('product.product', string='Product', change_default=True, ondelete='restrict', )
    categ_id = fields.Many2one('product.category', related='product_id.categ_id')
    categ_control_ids = fields.Many2many(related='stock_transfer_order_id.categ_control_ids')
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)
    product_uom_qty = fields.Float(string='Demand Qty', required=True)
    
    received_qty = fields.Float(string='Rcvd. Qty', compute='_compute_received_qty')
    
    date_scheduled = fields.Date(string='Scheduled Date')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account',)
    analytic_tag_ids = fields.Many2many('account.analytic.tag', string="Analytic Tags")
    supplier_id = fields.Many2one('res.partner', string='Supplier')
    project_id = fields.Many2one('project.project', string='Project')
    state = fields.Selection(related='stock_transfer_order_id.state')
    location_src_id = fields.Many2one('stock.location', string='From', required=True,)
    location_dest_id = fields.Many2one('stock.location', string='To', required=True,)
    return_status = fields.Selection([
        ('draft', 'New'), ('cancel', 'Cancelled'),
        ('waiting', 'Waiting Another Move'),
        ('confirmed', 'Waiting Availability'),
        ('partially_available', 'Partially Available'),
        ('assigned', 'Available'),
        ('done', 'Done')],string="Status", compute="_get_delivery_status")
    
    def _compute_received_qty(self):
        for line in self:
            if line.product_id.id:
                stock_move_obj = self.env['stock.move']
                domain = [('stock_transfer_order_line_id', '=', line.id),
                          ('picking_code', '=', line.stock_transfer_order_id.transfer_order_category_id.return_picking_type_id.code),           
                         ]
                where_query = stock_move_obj._where_calc(domain)
                stock_move_obj._apply_ir_rules(where_query, 'read')
                from_clause, where_clause, where_clause_params = where_query.get_sql()
                select = "SELECT SUM(product_qty) from " + from_clause + " where " + where_clause
            self.env.cr.execute(select, where_clause_params)
            line.received_qty = self.env.cr.fetchone()[0] or 0.0
            
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.product_tmpl_id.name
            self.product_uom = self.product_id.uom_po_id
            self.product_uom_qty = 1.0
            self.location_src_id = self.stock_transfer_order_id.transfer_order_category_id.return_location_id.id
            self.location_dest_id = self.stock_transfer_order_id.location_src_id.id
        if not self.date_scheduled:
            self.date_scheduled = self.stock_transfer_order_id.date_scheduled
            
    def _get_delivery_status(self):
        #status = ''
        picking_code = ''
        for line in self:
            if line.stock_transfer_order_id.action_type != 'normal':
                if line.stock_transfer_order_id.state == 'delivered':
                    picking_code = line.stock_transfer_order_id.transfer_order_category_id.return_picking_type_id.code
                else:
                    picking_code = line.stock_transfer_order_id.picking_type_code
            else:
                picking_code = line.stock_transfer_order_id.picking_type_code
            stock_move = self.env['stock.move'].search([('stock_transfer_order_line_id','=',line.id),('picking_code','=',picking_code)],limit=1)
            status = stock_move.state
        self.return_status = status
        
class StockTransferTXNLine(models.Model):
    _name = 'stock.transfer.txn.line'
    _description = 'Stock transfer Transaction Line'
    
    stock_transfer_order_id = fields.Many2one('stock.transfer.order', string='Stock transfer.order Order', required=True, ondelete='cascade', index=True, copy=False)
    stage_id = fields.Many2one('stock.transfer.order.stage',related='stock_transfer_order_id.stage_id')
    transfer_order_type_id = fields.Many2one(related='stock_transfer_order_id.transfer_order_type_id', readonly=True, store=True)
    sequence = fields.Integer(default=1)
    transfer_exception_type_id = fields.Many2one("stock.transfer.exception.type", string="Exception Type", domain="[('transfer_order_type_id','=',transfer_order_type_id),('apply_stage_id','=',stage_id)]")
    txn_stage_id = fields.Many2one('stock.transfer.order.stage', related='transfer_exception_type_id.stage_id')
    txn_action = fields.Selection([
        ('open', 'Open'),
        ('apply', 'Applied'),
    ], string='Action', copy=False, default='open')
