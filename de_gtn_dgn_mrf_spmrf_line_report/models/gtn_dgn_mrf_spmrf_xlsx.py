import json
from odoo import models
from odoo.exceptions import UserError


class GenerateXLSXReport(models.Model):
    _name = 'report.de_gtn_dgn_mrf_spmrf_line_report.mrf_spmrf_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        ###For SPMRF
        format1 = workbook.add_format({'font_size': '12', 'align': 'vcenter', 'bold': True})
        spmrf_order_ids = self.env['stock.transfer.order'].browse(data['order_ids'])
        
        
        
        
        for spmrf_order in spmrf_order_ids:
            if spmrf_order.transfer_order_type_id.name == 'Spare Part Request Form':
                sheet = workbook.add_worksheet('SPMRF Line Report')
                sheet.merge_range('C2:E2', 'SPMRF Line Report', format1)
                sheet.write(1, 4, 'SPMRF Line Report', format1)
                sheet.write(3, 0, 'Date From', format1)
                sheet.write(3, 1, data['start_date'], format1)
                sheet.write(4, 0, 'Date To', format1)
                sheet.write(4, 1, data['end_date'], format1)


                sheet.write(6, 0, 'GTN/GDN Number', format1)
                sheet.write(6, 1, 'GTN/GDN Creation Date', format1)
                sheet.write(6, 2, 'GTN/GDN Date of Transfer', format1)
                sheet.write(6, 3, 'GTN/GDN Amount', format1)
                sheet.write(6, 4, 'SPMRF', format1)
                sheet.write(6, 5, 'Requestor', format1)
                sheet.write(6, 6, 'SPMRF Type', format1)
                sheet.write(6, 7, 'Related PO', format1)
                sheet.write(6, 8, 'Source', format1)
                sheet.write(6, 9, 'Destination', format1)
                sheet.write(6, 10, 'Contractor', format1)
                sheet.write(6, 11, 'Create Date', format1)
                sheet.write(6, 12, 'Pick Up Date', format1)
                sheet.write(6, 13, 'Return Date', format1)
                sheet.write(6, 14, 'Material Supplier', format1)
                sheet.write(6, 15, 'Product', format1)
                sheet.write(6, 16, 'Description', format1)
                sheet.write(6, 17, 'Product Code', format1)
                sheet.write(6, 18, 'Product Category', format1)
                sheet.write(6, 19, 'Material Condition', format1)
                sheet.write(6, 20, 'Required QTY', format1)
                sheet.write(6, 21, 'Transferred QTY', format1)
                sheet.write(6, 22, 'Return QTY', format1)
                sheet.write(6, 23, 'Received QTY', format1)
                sheet.write(6, 24, 'SPMRF State', format1)

                format2 = workbook.add_format({'font_size': '12', 'align': 'vcenter'})
                row = 7
                sheet.set_column(row, 0, 50)
                sheet.set_column(row, 1, 25)
                sheet.set_column(row, 2, 20)
                sheet.set_column(row, 3, 20)
                sheet.set_column(row, 4, 20)
                sheet.set_column(row, 5, 20)
                sheet.set_column(row, 6, 20)
                sheet.set_column(row, 7, 20)
                sheet.set_column(row, 8, 20)
                sheet.set_column(row, 9, 20)
                sheet.set_column(row, 10, 20)
                sheet.set_column(row, 11, 20)
                sheet.set_column(row, 12, 20)
                sheet.set_column(row, 13, 20)
                sheet.set_column(row, 14, 20)
                sheet.set_column(row, 15, 20)
                sheet.set_column(row, 16, 20)
                sheet.set_column(row, 17, 20)
                sheet.set_column(row, 18, 20)
                sheet.set_column(row, 19, 20)
                sheet.set_column(row, 20, 20)
                sheet.set_column(row, 21, 20)
                sheet.set_column(row, 22, 20)
                sheet.set_column(row, 23, 20)
                sheet.set_column(row, 24, 20)
                
                if spmrf_order.name:
                    name = spmrf_order.name
                else:
                    name = None
                if spmrf_order.user_id:
                    requestor = spmrf_order.user_id.name
                else:
                    requestor = None
                if spmrf_order.transfer_order_category_id:
                    transfer_category = spmrf_order.transfer_order_category_id.name
                else:
                    transfer_category = None
                if spmrf_order.location_src_id:
                    src = spmrf_order.location_src_id.name
                else:
                    src = None
                if spmrf_order.location_dest_id:
                    dest = spmrf_order.location_dest_id.name
                else:
                    dest = None
                if spmrf_order.partner_id:
                    partner = spmrf_order.partner_id.name
                else:
                    partner = None
                if spmrf_order.date_order:
                    create_date = spmrf_order.date_order
                    create_date = create_date.strftime("%Y/%m/%s %H:%M:%S")
                else:
                    create_date = None
                if spmrf_order.date_delivered:
                    actual_date = spmrf_order.date_delivered
                    actual_date = actual_date.strftime("%Y/%m/%s %H:%M:%S")
                else:
                    actual_date = None
                if spmrf_order.date_returned:
                    return_date = spmrf_order.date_returned
                    return_date = return_date.strftime("%Y/%m/%s %H:%M:%S")
                else:
                    return_date = None

                if spmrf_order.stage_id:
                    stage = spmrf_order.stage_id.name
                else:
                    stage = None
                for product in spmrf_order.stock_transfer_order_line:
                    if product.supplier_id:
                        supplier = product.supplier_id.name
                    else:
                        supplier = None
                    if product.product_id:
                        product_name = product.product_id.name
                    else:
                        product_name = None
                    if product.product_id.categ_id:
                        product_category = product.product_id.categ_id.name
                    else:
                        product_category = None
                    if product.name:
                        description = product.name
                    else:
                        description = None
                    if product.product_id.default_code:
                        reference = product.product_id.default_code
                    else:
                        reference = None
                    if product.product_uom_qty:
                        demanded_qty = product.product_uom_qty
                    else:
                        demanded_qty = None
                    if product.delivered_qty:
                        delivered_qty = product.delivered_qty
                    else:
                        delivered_qty = None
                    for return_product in spmrf_order.stock_transfer_return_line:
                        if return_product:
                            if return_product.product_id.name == product.product_id.name:
                                if return_product.product_uom_qty:
                                    return_qty = return_product.product_uom_qty
                                else:
                                    return_qty = None
                                if return_product.received_qty:
                                    received_qty = return_product.received_qty
                                else:
                                    received_qty = None
                    #             sheet.write(row, 0, name, format2)
                    #             sheet.write(row, 1, name, format2)
                    #             sheet.write(row, 2, name, format2)
                    #             sheet.write(row, 3, name, format2)
                                sheet.write(row, 4, name, format2)
                                sheet.write(row, 5, requestor, format2)
                                sheet.write(row, 6, transfer_category, format2)
    #                 #             sheet.write(row, 7, transfer_category, format2)
                                sheet.write(row, 8, src, format2)
                                sheet.write(row, 9, dest, format2)
                                sheet.write(row, 10, partner, format2)
                                sheet.write(row, 11, create_date, format2)
                                sheet.write(row, 12, actual_date, format2)
                                sheet.write(row, 13, return_date, format2)
                                sheet.write(row, 14, supplier, format2)
                                sheet.write(row, 15, product_name, format2)
                                sheet.write(row, 16, description, format2)
                                sheet.write(row, 17, reference, format2)
                                sheet.write(row, 18, product_category, format2)
                                #sheet.write(row, 19, product_category, format2)            
                                sheet.write(row, 20, demanded_qty, format2)
                                sheet.write(row, 21, delivered_qty, format2)
                                sheet.write(row, 22, return_qty, format2)
                                sheet.write(row, 23, received_qty, format2)
                                sheet.write(row, 24, stage, format2)

                                row = row + 1
                                
            elif spmrf_order.transfer_order_type_id.name == 'Material Request Form':
                sheet = workbook.add_worksheet('MRF Line Report')
                sheet.merge_range('C2:E2', 'MRF Line Report', format1)
                sheet.write(1, 4, 'MRF Line Report', format1)
                sheet.write(3, 0, 'Date From', format1)
                sheet.write(3, 1, data['start_date'], format1)
                sheet.write(4, 0, 'Date To', format1)
                sheet.write(4, 1, data['end_date'], format1)


                sheet.write(6, 0, 'GTN/GDN Number', format1)
                sheet.write(6, 1, 'GTN/GDN Creation Date', format1)
                sheet.write(6, 2, 'GTN/GDN Date of Transfer', format1)
                sheet.write(6, 3, 'GTN/GDN Amount', format1)
                sheet.write(6, 4, 'MRF', format1)
                sheet.write(6, 5, 'Requestor', format1)
                sheet.write(6, 6, 'MRF Type', format1)
                sheet.write(6, 7, 'Related PO', format1)
                sheet.write(6, 8, 'Source', format1)
                sheet.write(6, 9, 'Destination', format1)
                sheet.write(6, 10, 'Contractor', format1)
                sheet.write(6, 11, 'Create Date', format1)
                sheet.write(6, 12, 'Pick Up Date', format1)
                sheet.write(6, 13, 'Return Date', format1)
                sheet.write(6, 14, 'Material Supplier', format1)
                sheet.write(6, 15, 'Product', format1)
                sheet.write(6, 16, 'Description', format1)
                sheet.write(6, 17, 'Product Code', format1)
                sheet.write(6, 18, 'Product Category', format1)
                sheet.write(6, 19, 'Material Condition', format1)
                sheet.write(6, 20, 'Required QTY', format1)
                sheet.write(6, 21, 'Transferred QTY', format1)
                sheet.write(6, 22, 'Return QTY', format1)
                sheet.write(6, 23, 'Received QTY', format1)
                sheet.write(6, 24, 'MRF State', format1)

                format2 = workbook.add_format({'font_size': '12', 'align': 'vcenter'})
                row = 7
                sheet.set_column(row, 0, 50)
                sheet.set_column(row, 1, 25)
                sheet.set_column(row, 2, 20)
                sheet.set_column(row, 3, 20)
                sheet.set_column(row, 4, 20)
                sheet.set_column(row, 5, 20)
                sheet.set_column(row, 6, 20)
                sheet.set_column(row, 7, 20)
                sheet.set_column(row, 8, 20)
                sheet.set_column(row, 9, 20)
                sheet.set_column(row, 10, 20)
                sheet.set_column(row, 11, 20)
                sheet.set_column(row, 12, 20)
                sheet.set_column(row, 13, 20)
                sheet.set_column(row, 14, 20)
                sheet.set_column(row, 15, 20)
                sheet.set_column(row, 16, 20)
                sheet.set_column(row, 17, 20)
                sheet.set_column(row, 18, 20)
                sheet.set_column(row, 19, 20)
                sheet.set_column(row, 20, 20)
                sheet.set_column(row, 21, 20)
                sheet.set_column(row, 22, 20)
                sheet.set_column(row, 23, 20)
                sheet.set_column(row, 24, 20)
                
                if spmrf_order.name:
                    name = spmrf_order.name
                else:
                    name = None
                if spmrf_order.user_id:
                    requestor = spmrf_order.user_id.name
                else:
                    requestor = None
                if spmrf_order.transfer_order_category_id:
                    transfer_category = spmrf_order.transfer_order_category_id.name
                else:
                    transfer_category = None
                if spmrf_order.location_src_id:
                    src = spmrf_order.location_src_id.name
                else:
                    src = None
                if spmrf_order.location_dest_id:
                    dest = spmrf_order.location_dest_id.name
                else:
                    dest = None
                if spmrf_order.partner_id:
                    partner = spmrf_order.partner_id.name
                else:
                    partner = None
                if spmrf_order.date_order:
                    create_date = spmrf_order.date_order
                    create_date = create_date.strftime("%Y/%m/%s %H:%M:%S")
                else:
                    create_date = None
                if spmrf_order.date_delivered:
                    actual_date = spmrf_order.date_delivered
                    actual_date = actual_date.strftime("%Y/%m/%s %H:%M:%S")
                else:
                    actual_date = None
                if spmrf_order.date_returned:
                    return_date = spmrf_order.date_returned
                    return_date = return_date.strftime("%Y/%m/%s %H:%M:%S")
                else:
                    return_date = None

                if spmrf_order.stage_id:
                    stage = spmrf_order.stage_id.name
                else:
                    stage = None
                for product in spmrf_order.stock_transfer_order_line:
                    if product.supplier_id:
                        supplier = product.supplier_id.name
                    else:
                        supplier = None
                    if product.product_id:
                        product_name = product.product_id.name
                    else:
                        product_name = None
                    if product.product_id.categ_id:
                        product_category = product.product_id.categ_id.name
                    else:
                        product_category = None
                    if product.name:
                        description = product.name
                    else:
                        description = None
                    if product.product_id.default_code:
                        reference = product.product_id.default_code
                    else:
                        reference = None
                    if product.product_uom_qty:
                        demanded_qty = product.product_uom_qty
                    else:
                        demanded_qty = None
                    if product.delivered_qty:
                        delivered_qty = product.delivered_qty
                    else:
                        delivered_qty = None
                    for return_product in spmrf_order.stock_transfer_return_line:
                        if return_product:
                            if return_product.product_id.name == product.product_id.name:
                                if return_product.product_uom_qty:
                                    return_qty = return_product.product_uom_qty
                                else:
                                    return_qty = None
                                if return_product.received_qty:
                                    received_qty = return_product.received_qty
                                else:
                                    received_qty = None
                    #             sheet.write(row, 0, name, format2)
                    #             sheet.write(row, 1, name, format2)
                    #             sheet.write(row, 2, name, format2)
                    #             sheet.write(row, 3, name, format2)
                                sheet.write(row, 4, name, format2)
                                sheet.write(row, 5, requestor, format2)
                                sheet.write(row, 6, transfer_category, format2)
    #                 #             sheet.write(row, 7, transfer_category, format2)
                                sheet.write(row, 8, src, format2)
                                sheet.write(row, 9, dest, format2)
                                sheet.write(row, 10, partner, format2)
                                sheet.write(row, 11, create_date, format2)
                                sheet.write(row, 12, actual_date, format2)
                                sheet.write(row, 13, return_date, format2)
                                sheet.write(row, 14, supplier, format2)
                                sheet.write(row, 15, product_name, format2)
                                sheet.write(row, 16, description, format2)
                                sheet.write(row, 17, reference, format2)
                                sheet.write(row, 18, product_category, format2)
                                #sheet.write(row, 19, product_category, format2)            
                                sheet.write(row, 20, demanded_qty, format2)
                                sheet.write(row, 21, delivered_qty, format2)
                                sheet.write(row, 22, return_qty, format2)
                                sheet.write(row, 23, received_qty, format2)
                                sheet.write(row, 24, stage, format2)

                                row = row + 1
                