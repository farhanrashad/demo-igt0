import json
from odoo import models
from odoo.exceptions import UserError


class GenerateXLSXReport(models.Model):
    _name = 'report.de_pr_deviation_report.pr_deviation_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):

        format1 = workbook.add_format({'font_size': '12', 'align': 'vcenter', 'bold': True})
        sheet = workbook.add_worksheet('PR Deviation Report')
        sheet.write(3, 0, 'Order Reference', format1)
        sheet.write(3, 1, 'Old PR / Current PR', format1)
        sheet.write(3, 2, 'User Name', format1)
        sheet.write(3, 3, 'Currency', format1)
        sheet.write(3, 4, 'Original PR Amount', format1)
        sheet.write(3, 5, 'PR Updated Amount', format1)
        sheet.write(3, 6, 'Total Deviation Value', format1)
        sheet.write(3, 7, 'History Create Date', format1)
        sheet.write(3, 8, 'History Record', format1)
        sheet.write(3, 9, 'Reason', format1)

        format2 = workbook.add_format({'font_size': '12', 'align': 'vcenter'})
        row = 4
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

        #purchase_order_ids = self.env['purchase.order'].browse(data['id'])

        for id in lines:
            if id.user_id:
                username = id.user_id.name
            else:
                username = None
            if id.currency_id:
                currency = id.currency_id.name
            else:
                currency = None
            try:
                if id.amount_total:
                    updated_po_amount = id.amount_total
                    # original_po_amount = id.amount_total
                else:
                    updated_po_amount = None
                if id.reason:
                    reason = id.reason
                else:
                    reason = None
            except:
                updated_po_amount = None
                reason = None
                # original_po_amount = None
            if id.line_ids:
                updated_po_amount = 0
                for line in id.line_ids:
                    price_total_base  = line.price_total_base
                    updated_po_amount += price_total_base
            
            if id.old_revision_ids:
                for line in id.old_revision_ids[-1]:
                    name = line.name
                    history_create_date = line.create_date
                    if history_create_date:
                        history_create_date = history_create_date.strftime("%Y-%m-%d %H:%M:%S")
                        history_record = 'Yes'
                    else:
                        history_record = 'No'
                    purchase_req = self.env['purchase.requisition'].search([('name', '=', name)])
                    for order in purchase_req:
                        if order.line_ids:
                            original_po_amount = 0
                            for order_line in order.line_ids:
                                price_total_base  = order_line.price_total_base
                                original_po_amount += price_total_base
                        else:
                            original_po_amount = None
                    if updated_po_amount:
                        total_deviation = updated_po_amount - original_po_amount
                    else:
                        total_deviation = None
                    sheet.write(row, 0, name, format2)
                    sheet.write(row, 1, name, format2)
                    sheet.write(row, 2, username, format2)
                    sheet.write(row, 3, currency, format2)
                    sheet.write(row, 4, original_po_amount, format2)
                    sheet.write(row, 5, updated_po_amount, format2)
                    sheet.write(row, 6, total_deviation, format2)
                    sheet.write(row, 7, history_create_date, format2)
                    sheet.write(row, 8, history_record, format2)
                    sheet.write(row, 9, reason, format2)

                    row = row + 1
