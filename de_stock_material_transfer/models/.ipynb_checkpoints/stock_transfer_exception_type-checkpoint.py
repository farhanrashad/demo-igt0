# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class TransferOrderException(models.Model):
    _name = "stock.transfer.exception.type"
    _description = "Transfer Exception"

    code = fields.Char(string='Code', size=2, required=True)
    name = fields.Char(string='Name', required=True)
    message_type = fields.Selection([
        ('none', 'None'),
        ('warning', 'Warning'),
        ('block', 'Block Message'),
    ], string='Message Type', default='none', required=True)
    message = fields.Char(string='Message', required=True)
    sequence = fields.Integer(default=1)
    transfer_order_type_id = fields.Many2one('stock.transfer.order.type', string='Transfer Type', copy=False)
    stage_id = fields.Many2one('stock.transfer.order.stage', domain="[('transfer_order_type_ids','=',transfer_order_type_id)]", string='Add Stage', copy=False)
    apply_stage_id = fields.Many2one('stock.transfer.order.stage', domain="[('transfer_order_type_ids','=',transfer_order_type_id)]", string='Apply On', copy=False)
    exec_stage_id = fields.Many2one('stock.transfer.order.stage', domain="[('transfer_order_type_ids','=',transfer_order_type_id)]", string='Execute On', copy=False)
    stage_auto_apply = fields.Boolean(string='Stage Auto Apply')
    picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type', )
    location_src_id = fields.Many2one('stock.location', string='Source Location',  )
    location_dest_id = fields.Many2one('stock.location', string='Destination Location', )
    return_picking_type_id = fields.Many2one('stock.picking.type',related='picking_type_id.return_picking_type_id')
    return_location_id = fields.Many2one('stock.location', string='Return Location', domain="[('return_location','=',True)]")
    active = fields.Boolean('Active', default=True,
        help="If unchecked, it will allow you to hide the exception without removing it.")
    
    _sql_constraints = [
        ('unique_exception', 'unique (code)', 'Exception already defined'),
    ]
