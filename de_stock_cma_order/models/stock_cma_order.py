# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.safe_eval import safe_eval
from odoo.tools.misc import format_date

class StockCMAOrder(models.Model):
    _name = 'stock.cma.order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Stock CMA Order'
    _order = 'date_order desc, id desc'
    _check_company_auto = True

    
    def _get_type_id(self):
        return self.env['stock.cma.type'].search([], limit=1)
    
    def _get_picking_in(self):
        pick_in = self.env['stock.picking.type'].search([('code', '=', 'outgoing')],limit=1,)
        company = self.env.company
        if not pick_in or pick_in.sudo().warehouse_id.company_id.id != company.id:
            pick_in = self.env['stock.picking.type'].search(
                [('warehouse_id.company_id', '=', company.id), ('code', '=', 'outgoing')],
                limit=1,
            )
        return pick_in
    
    def _get_default_location(self):
        location_id = self.env['stock.location'].search([('return_location','=',True)],limit=1)
        return location_id
    
    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    cma_type_id = fields.Many2one('stock.cma.type', string='CMA Type', index=True, required=True, default=_get_type_id, readonly=True, states={'draft': [('readonly', False)],'in_progress': [('readonly', False)]},)
    cma_type = fields.Selection(related='cma_type_id.action_type')
    partner_id = fields.Many2one('res.partner', 'Contractor',check_company=True, required=True,
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]})

    state = fields.Selection([
        ('draft', 'New'),
        ('confirm', 'Confirmed'),
        ('delivery', 'Delivered'),
        ('return', 'Returned'),
        ('done', 'Closed'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True, copy=False, index=True, tracking=4, default='draft')
    
    date_request = fields.Datetime(string='Request Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)],'in_progress': [('readonly', False)] }, copy=False, default=fields.Datetime.now, help="Order request date")

    date_order = fields.Datetime(string='Order Date', required=True, readonly=True, index=True, states={'draft': [('readonly', False)],'in_progress': [('readonly', False)] }, copy=False, default=fields.Datetime.now, help="Order confirmation date")
    date_scheduled = fields.Datetime(string='Date Scheduled', required=True, readonly=True, index=True, states={'draft': [('readonly', False)],'in_progress': [('readonly', False)] }, copy=False, default=fields.Datetime.now, help="Deadline schedule date")
    delivery_deadline = fields.Datetime(string='Delivery Deadline', required=True, readonly=True, index=True, states={'draft': [('readonly', False)],'in_progress': [('readonly', False)] }, copy=False, default=fields.Datetime.now, help="Delivery Deadline")
    return_deadline = fields.Datetime(string='Return Deadline', readonly=False, compute='_compute_return_deadline', states={'draft': [('readonly', False)],'in_progress': [('readonly', False)] }, copy=False, help="Retrun Material Deadline")
    date_delivered = fields.Datetime(string="Actual Delivery", compute="_compute_all_dates")
    date_returned = fields.Datetime(string="Actual Return", compute="_compute_all_dates")
    
    stock_cma_order_line = fields.One2many('stock.cma.order.line', 'stock_cma_order_id', string='CMA Line', copy=True, auto_join=True,readonly=True, states={'draft': [('readonly', False)],'in_progress': [('readonly', False)]},)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True, default=lambda self: self.env.company, readonly=True, states={'draft': [('readonly', False)],'in_progress': [('readonly', False)]},)
    description = fields.Text()
    user_id = fields.Many2one('res.users', string="Request Owner",check_company=True, domain="[('company_ids', 'in', company_id)]", default=lambda self: self.env.user, required=True,readonly=True, states={'draft': [('readonly', False)]},)    

    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', domain="[('company_id', '=', company_id)]", required=True, readonly=True, states={'draft': [('readonly', False)]},)
    picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type', default=_get_picking_in, required=True, readonly=True, states={'draft': [('readonly', False)]},)
    return_picking_type_id = fields.Many2one('stock.picking.type',related='picking_type_id.return_picking_type_id')
    location_src_id = fields.Many2one('stock.location', string='Source Location',  required=True, readonly=True, states={'draft': [('readonly', False)]})
    location_dest_id = fields.Many2one('stock.location', string='Destination Location', readonly=True, required=True, states={'draft': [('readonly', False)]},)
    return_location_id = fields.Many2one('stock.location', string='Return Location', default=_get_default_location, readonly=True, required=True, states={'draft': [('readonly', False)]},)

    purchase_id = fields.Many2one('purchase.order', string='Purchase Order')
    cma_order_id = fields.Many2one('stock.cma.order', string='CMA Order')
    
    delivery_count = fields.Integer(compute='_compute_picking_count', string='Number of Delivery')
    return_count = fields.Integer(compute='_compute_picking_count', string='Number of Return')
    picking_ids = fields.One2many('stock.picking', 'stock_cma_order_id', string='Picking', states={'done': [('readonly', True)]})
    bill_count = fields.Integer(compute='_compute_bill_count')

    
    @api.onchange('picking_type_id')
    def _onchange_picking_type(self):
        for line in self:
            line.location_src_id = line.picking_type_id.default_location_src_id
            line.location_dest_id = line.picking_type_id.default_location_dest_id
    
    @api.onchange('cma_type_id')
    def _onchange_cma_type(self):
        if self.cma_type_id:
            ddays = self.cma_type_id.default_delivery_validity
            ldays = self.cma_type_id.delivery_lead_days
            if ddays > 0:
                self.delivery_deadline = fields.Date.to_string(datetime.now() + timedelta(ddays))
                self.date_scheduled = fields.Date.to_string(datetime.now() + timedelta(ldays))
        
    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id:
            warehouse = self.env['stock.warehouse'].search([('company_id', '=', self.company_id.id)], limit=1)
            self.warehouse_id = warehouse
        else:
            self.warehouse_id = False
    
    def _compute_all_dates(self):
        ddt = rdt = False
        pickings = self.env['stock.picking']
        for order in self:
            pickings = self.env['stock.picking'].search([('stock_cma_order_id','=',order.id),('picking_type_id','=',order.picking_type_id.id),('state','=','done')])
        for picking in pickings:
            if picking.date_done:
                ddt = picking.date_done
        for order in self:
            pickings = self.env['stock.picking'].search([('stock_cma_order_id','=',order.id),('picking_type_id','=',order.return_picking_type_id.id),('state','=','done')])
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
                days = order.cma_type_id.default_return_validity
                dt = fields.Date.to_string(order.date_delivered + timedelta(days))
        self.return_deadline = dt
        
    @api.model
    def create(self, vals):
        if 'company_id' in vals:
            self = self.with_company(vals['company_id'])
        if vals.get('name', _('New')) == _('New'):
            seq_date = None
            if 'refill_date' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
            vals['name'] = self.env['ir.sequence'].next_by_code('stock.cma.order', sequence_date=seq_date) or _('New')
        result = super(StockCMAOrder, self).create(vals)       
        return result
    
    def action_draft(self):
        self.state = 'draft'
    
    def action_confirm(self):
        self.update({
            'state' : 'confirm',
            'date_order': fields.Datetime.now()
        })
        
    def action_done(self):
        """
        Generate all stock order based on selected lines, should only be called on one agreement at a time
        """
        if any(picking.state in ['draft', 'sent', 'to approve'] for picking in self.mapped('picking_ids')):
            raise UserError(_('You have to cancel or validate every CMA before closing the CMA order.'))
        self.write({'state': 'done'})
        
    def action_cancel(self):
        self.state = 'cancel'
        
    def unlink(self):
        if any(cma.state not in ('draft', 'cancel') for cma in self):
            raise UserError(_('You can only delete draft CMA orders.'))
        self.mapped('stock_cma_line').unlink()
        return super(StockCMAOrder, self).unlink()
    
    def create_delivery(self):
        self.ensure_one()
        picking = self.env['stock.picking']
        lines_data = []
        for order in self:
            for line in order.stock_cma_order_line:
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
                    'stock_cma_order_line_id': line.id,
                }])
        picking.create({
            'picking_type_id':self.picking_type_id.id,
            'partner_id': order.partner_id.id,
            'location_id': self.location_src_id.id,
            'location_dest_id':self.location_dest_id.id,
            'scheduled_date':self.date_scheduled,
            'origin':self.name,
            'stock_cma_order_id':self.id,
            'move_lines':lines_data,
        })
        self.state = 'delivery'
        return picking
    
    def create_return(self):
        self.ensure_one()
        picking = self.env['stock.picking']
        origin_picking_id = self.env['stock.picking']
        lines_data = []
        for order in self:
            origin_picking_id = self.env['stock.picking'].search([('stock_cma_order_id','=',order.id),('picking_type_id','=',order.picking_type_id.id),('state','!=','cancel')],limit=1)
            for line in order.stock_cma_order_line:
                lines_data.append([0,0,{
                    #'reference': order.name,
                    'product_id': line.product_id.id,
                    'product_uom': line.product_id.uom_po_id.id,
                    'product_uom_qty': line.product_uom_qty,
                    'origin': 'return of ' + origin_picking_id.name,
                    'name': order.name,
                    'date_deadline': order.date_scheduled,
                    'location_id': line.location_dest_id.id,
                    'location_dest_id': order.return_location_id.id,
                    'stock_cma_order_line_id': line.id,
                    'origin_returned_move_id': self.env['stock.move'].search([('stock_cma_order_line_id','=',line.id),('picking_id','=',origin_picking_id.id)]).id
                }])
            picking.create({
                'picking_type_id':order.return_picking_type_id.id,
                'partner_id': order.partner_id.id,
                'location_id': line.location_dest_id.id,
                'location_dest_id':order.return_location_id.id,
                'scheduled_date':self.date_scheduled,
                'origin': 'return of ' + origin_picking_id.name,
                'stock_cma_order_id':self.id,
                'move_lines':lines_data,
            })
        self.state = 'return'
        return picking
    
    
    def _compute_picking_count(self):
        Picking = self.env['stock.picking']
        can_read = Picking.check_access_rights('read', raise_exception=False)
        for order in self:
            order.delivery_count = can_read and Picking.search_count([('stock_cma_order_id', '=', order.id),('picking_type_id', '=', order.picking_type_id.id),('state', '!=', 'cancel')]) or 0
            order.return_count = can_read and Picking.search_count([('stock_cma_order_id', '=', order.id),('picking_type_id', '=', order.return_picking_type_id.id),('state', '!=', 'cancel')]) or 0

    def action_view_delivery(self):
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")
        pickings = self.env['stock.picking'].search([('stock_cma_order_id', '=', self.id),('picking_type_id', '=', self.picking_type_id.id),('state', '!=', 'cancel')])
        if len(pickings) > 1:
            action['domain'] = [('stock_cma_order_id', '=', self.id),('picking_type_id', '=', self.picking_type_id.id),('state', '!=', 'cancel')]
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
        pickings = self.env['stock.picking'].search([('stock_cma_order_id', '=', self.id),('picking_type_id', '=', self.return_picking_type_id.id),('state', '!=', 'cancel')])
        if len(pickings) > 1:
            action['domain'] = [('id', 'in', pickings.ids),('picking_type_id', '=', self.return_picking_type_id.id)]
        elif pickings:
            form_view = [(self.env.ref('stock.view_picking_form').id, 'form')]
            if 'views' in action:
                action['views'] = form_view + [(state,view) for state,view in action['views'] if view != 'form']
            else:
                action['views'] = form_view
            action['res_id'] = pickings.id
        # Prepare the context.
        picking_id = pickings.filtered(lambda l: l.picking_type_id.code == self.return_picking_type_id.id)
        if picking_id:
            picking_id = picking_id[0]
        else:
            picking_id = pickings[0]
        action['context'] = dict(self._context, default_partner_id=self.partner_id.id, default_picking_type_id=picking_id.picking_type_id.id, default_origin=self.name, default_group_id=picking_id.group_id.id)
        return action
    
    def _compute_bill_count(self):
        Bill = self.env['account.move']
        can_read = Bill.check_access_rights('read', raise_exception=False)
        for order in self:
            order.bill_count = can_read and Bill.search_count([('stock_cma_order_id', '=', order.id)]) or 0

    def action_view_credit_note(self):
        self.ensure_one()
        invoices = self.env['account.move'].search([('stock_cma_order_id', 'in', self.ids)])
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
    
    
class StockCMAOrderLine(models.Model):
    _name = 'stock.cma.order.line'
    _description = 'Stock CMA Line'
    
    stock_cma_order_id = fields.Many2one('stock.cma.order', string='Stock CMA Order', required=True, ondelete='cascade', index=True, copy=False)
    state = fields.Selection(related='stock_cma_order_id.state', readonly=True)
    partner_id = fields.Many2one('res.partner', related='stock_cma_order_id.partner_id', readonly=True)
    user_id = fields.Many2one('res.users', related='stock_cma_order_id.user_id', readonly=True)

    name = fields.Text(string='Description', required=True)
    product_id = fields.Many2one('product.product', string='Product', domain="[('purchase_ok', '=', True)]", change_default=True, ondelete='restrict', required=True) 
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)
    product_uom_qty = fields.Float(string='Quantity', required=True)
    received_qty = fields.Float(string='Received Quantity', compute='_compute_all_qty')
    delivered_qty = fields.Float(string='Delivered Qty', compute='_compute_all_qty')
    date_scheduled = fields.Date(string='Scheduled Date')
    state = fields.Selection(related='stock_cma_order_id.state')
    location_src_id = fields.Many2one('stock.location', string='From', required=True,)
    location_dest_id = fields.Many2one('stock.location', string='To', required=True,)
    
    def _compute_all_qty(self):
        del_qty = rcv_qty = 0
        move_lines = self.env['stock.move']
        for line in self:
            del_qty = rcv_qty = 0
            move_lines = self.env['stock.move'].search([('stock_cma_order_line_id', '=', line.id),('picking_id.stock_cma_order_id', '=', line.stock_cma_order_id.id), ('state', '=', 'done'),('picking_id.picking_type_id','=', line.stock_cma_order_id.picking_type_id.id)],limit=1)
            for move in move_lines:
                del_qty = move.quantity_done
        
        #picking_id = self.env['stock.picking'].search([('stock_cma_order_id', '=', self.stock_cma_order_id.id),('picking_type_id', '=', self.stock_cma_order_id.picking_type_id.id),('state', '=', 'done')],limit=1)
        #move_lines = self.env['stock.move'].search([('stock_cma_order_line_id', '=', self.id)])
        #for move in move_lines:
        #    rcv_qty = move.product_uom_qty
            
        self.update({
            'delivered_qty': del_qty,
            'received_qty' :rcv_qty,
        })
        
    def _compute_received_qty(self):
        qty = 0
        for picking in self.stock_cma_order_id.picking_ids:
            for move in picking.move_lines.filtered(lambda r: r.state not in ['cancel'] and r.product_id.id == self.product_id.id):
                qty += move.product_uom_qty
        self.update({
            'received_qty': qty
        })
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.product_tmpl_id.name
            self.product_uom = self.product_id.uom_po_id
            self.product_uom_qty = 1.0
            self.location_src_id = self.stock_cma_order_id.location_src_id.id
            self.location_dest_id = self.stock_cma_order_id.location_dest_id.id
        if not self.date_scheduled:
            self.date_scheduled = self.stock_cma_order_id.date_scheduled
            
    def action_view_cma_order(self):
        action = self.env["ir.actions.actions"]._for_xml_id("action_stock_cma_order_pending")
        pickings = self.env['stock.cma.order'].search([('id', '=', self.stock_cma_order_id.id)])
        if len(pickings) > 1:
            action['domain'] = [('id', '=', self.stock_cma_order_id.id)]
        elif pickings:
            form_view = [(self.env.ref('de_stock_cma_order.stock_cma_order_form_view').id, 'form')]
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