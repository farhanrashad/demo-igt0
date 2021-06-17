import json
from odoo import models
from odoo.exceptions import UserError


class GenerateXLSXReport(models.Model):
    _name = 'report.de_payslip_batch_report.payslip_batch_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):

        format1 = workbook.add_format({'font_size': '12', 'align': 'vcenter', 'bold': True})
        sheet = workbook.add_worksheet('Payslip Batch Report')
        sheet.write(3, 0, 'SR. No', format1)
        sheet.write(3, 1, 'Account Name', format1)
        sheet.write(3, 2, 'Account No', format1)
        sheet.write(3, 3, 'Amount', format1)
        sheet.write(3, 4, 'Currency', format1)


        format2 = workbook.add_format({'font_size': '12', 'align': 'vcenter'})
        row = 4
        sheet.set_column(row, 0, 50)
        sheet.set_column(row, 1, 25)
        sheet.set_column(row, 2, 20)
        sheet.set_column(row, 3, 20)
        sheet.set_column(row, 4, 20)
       
        get_wiz = self.env['pay.slip.batch'].search(data[('id')])
        count = 1
        for order in get_wiz:
            sheet.write(row, 0, count, format2)
            sheet.write(row, 1, contract_type, format2)
            sheet.write(row, 2, str(doe), format2)
            sheet.write(row, 3, debit_ac_no, format2)
            sheet.write(row, 4, currency, format2)
            
            count = count + 1
            row = row + 1
        
        # purchase_order_ids = self.env['purchase.order'].browse(data['id'])
        #
        # for id in purchase_order_ids:
        #     date = id.date_order
        #     if date:
        #         ordering_date = date.strftime("%m/%d/%Y")
        #     else:
        #         ordering_date = None
        #
        #     receipt_date = id.date_planned
        #     if receipt_date:
        #         delivery_date = receipt_date.strftime("%m/%d/%Y")
        #     else:
        #         delivery_date = None
        #
        #     effective_date = id.effective_date
        #     if effective_date:
        #         effective_date = effective_date.strftime("%m/%d/%Y")
        #     else:
        #         effective_date = None
        #
        #     if id.user_id.name:
        #         created_by = id.user_id.name
        #     else:
        #         created_by = None
        #
        #     if id.incoterm_id:
        #         incoterm = id.incoterm_id.name
        #     else:
        #         incoterm = None
        #     if id.payment_term_id:
        #        payment_term =  id.payment_term_id.name
        #     else:
        #         payment_term = None
        #
        #     if self.env['account.move'].search(['|',('payment_reference','=',id.name),('payment_reference','=','/ ' + id.name)]):
        #         vendor_bills = self.env['account.move'].search(['|',('payment_reference','=',id.name),('payment_reference','=','/ ' + id.name)])[0]
        #         vendor_currency = vendor_bills.currency_id.name
        #         if vendor_bills:
        #             invoice_date = vendor_bills.invoice_date
        #             if invoice_date:
        #                 invoice_date = invoice_date.strftime("%m/%d/%Y")
        #             else:
        #                 invoice_date = None
        #
        #             payment_schedule_date = vendor_bills.invoice_payment_term_id
        #             if payment_schedule_date:
        #                 payment_date = payment_schedule_date.strftime("%m/%d/%Y")
        #             else:
        #                 payment_date = None
        #
        #             if vendor_bills.amount_residual:
        #                 amount_due = vendor_bills.amount_residual
        #             else:
        #                 amount_due = None
        #             if vendor_bills.amount_total:
        #                 amount_total = vendor_bills.amount_total
        #             else:
        #                 amount_total = None
        #
        #             if vendor_bills.invoice_payments_widget:
        #                 invoice_payment_widget = vendor_bills.invoice_payments_widget
        #                 invoice_payment_widget = json.loads(invoice_payment_widget)
        #                 if invoice_payment_widget:
        #                     invoice_payment_widget = invoice_payment_widget['content'][0]['amount']
        #                 else:
        #                     invoice_payment_widget = None
        #             else:
        #                 invoice_payment_widget = None
        #             if vendor_bills.date:
        #                 vendor_payment_date = vendor_bills.date
        #                 vendor_payment_date = vendor_payment_date.strftime("%m/%d/%Y")
        #             else:
        #                 vendor_payment_date = None
        #             if vendor_bills.name:
        #                 vendor_name = vendor_bills.name
        #             else:
        #                 vendor_name = None
        #
        #         else:
        #             invoice_date = None
        #             payment_date = None
        #             amount_due = None
        #             amount_total = None
        #             invoice_payment_widget = None
        #             vendor_payment_date = None
        #             vendor_name = None
        #     else:
        #         invoice_date = None
        #         payment_date = None
        #         vendor_currency = None
        #         amount_due = None
        #         amount_total = None
        #         invoice_payment_widget = None
        #         vendor_payment_date = None
        #         vendor_name = None
        #
        #     if self.env['stock.picking'].search([('origin','=',id.name)]):
        #         receipts = self.env['stock.picking'].search([('origin','=',id.name)])[0]
        #         if receipts:
        #             receipt_doc_no = receipts.name
        #             sched_date = receipts.scheduled_date
        #
        #             if sched_date:
        #                 receipt_doc_date = sched_date.strftime("%m/%d/%Y")
        #             else:
        #                 receipt_doc_date = None
        #         else:
        #             receipt_doc_no = None
        #             receipt_doc_date = None
        #     else:
        #         receipt_doc_no = None
        #         receipt_doc_date = None
        #     if id.order_line:
        #         for line in id.order_line:
        #             if self.env['account.move'].search(['|',('payment_reference','=',id.name),('payment_reference','=','/ ' + id.name)]):
        #                 vendor_bill = self.env['account.move'].search(['|',('payment_reference','=',id.name),('payment_reference','=','/ ' + id.name)])[0]
        #                 if vendor_bill.line_ids:
        #                     for vendor_line in vendor_bill.line_ids:
        #                         account = vendor_line.account_id.name
        #
        #                         sheet.write(row, 0, id.partner_id.name, format2)
        #                         sheet.write(row, 1, id.name, format2)
        #                         sheet.write(row, 2, ordering_date, format2)
        #                         sheet.write(row, 3, id.requisition_id.line_ids.id, format2)
        #                         sheet.write(row, 4, line.purchase_budget_line_id.name, format2)
        #                         sheet.write(row, 5, line.product_id.name, format2)
        #                         sheet.write(row, 6, line.product_id.categ_id.name, format2)
        #                         sheet.write(row, 7, line.name, format2)
        #                         sheet.write(row, 8, line.analytic_tag_ids.name, format2)
        #                         sheet.write(row, 9, line.project_id.name, format2)
        #                         sheet.write(row, 10, line.candidate, format2)
        #                         sheet.write(row, 11, line.tenant.name, format2)
        #                         sheet.write(row, 12, line.product_qty, format2)
        #                         sheet.write(row, 13, line.product_uom.name, format2)
        #                         sheet.write(row, 14, delivery_date, format2)
        #                         sheet.write(row, 15, effective_date, format2)
        #                         sheet.write(row, 16, payment_date, format2)
        #                         sheet.write(row, 17, line.price_unit, format2)
        #                         sheet.write(row, 18, line.discount, format2)
        #         #                 sheet.write(row, 19, payment_date, format2)
        #                         sheet.write(row, 20, line.price_subtotal, format2)
        #                         sheet.write(row, 21, id.currency_id.name, format2)
        #         #                 sheet.write(row, 22, payment_date, format2)
        #                         sheet.write(row, 23, line.qty_received, format2)
        #         #                 sheet.write(row, 24, payment_date, format2)
        #                         sheet.write(row, 25, amount_due, format2)
        #                         sheet.write(row, 26, receipt_doc_no, format2)
        #                         sheet.write(row, 27, receipt_doc_date, format2)
        #                         sheet.write(row, 28, line.qty_invoiced, format2)
        #                         sheet.write(row, 29, line.qty_invoiced, format2)
        #                         sheet.write(row, 30, amount_total, format2)
        #                         sheet.write(row, 31, amount_total, format2)
        #         #                 sheet.write(row, 32, line.qty_invoiced, format2)
        #                         sheet.write(row, 33, vendor_name, format2)
        #                         sheet.write(row, 34, vendor_currency, format2)
        #                         sheet.write(row, 35, invoice_date, format2)
        #                         sheet.write(row, 36, account, format2)
        #                         sheet.write(row, 37, invoice_payment_widget, format2)
        #                         sheet.write(row, 38, invoice_payment_widget, format2)
        #         #                 sheet.write(row, 39, invoice_date, format2)
        #                         sheet.write(row, 40, vendor_payment_date, format2)
        #                         sheet.write(row, 41, created_by, format2)
        #                         sheet.write(row, 42, incoterm, format2)
        #                         sheet.write(row, 43, payment_term, format2)
        #
        #                         row = row + 1
        #                 else:
        #                     account = None
        #                     sheet.write(row, 0, id.partner_id.name, format2)
        #                     sheet.write(row, 1, id.name, format2)
        #                     sheet.write(row, 2, ordering_date, format2)
        #                     sheet.write(row, 3, id.requisition_id.line_ids.id, format2)
        #                     sheet.write(row, 4, line.purchase_budget_line_id.name, format2)
        #                     sheet.write(row, 5, line.product_id.name, format2)
        #                     sheet.write(row, 6, line.product_id.categ_id.name, format2)
        #                     sheet.write(row, 7, line.name, format2)
        #                     sheet.write(row, 8, line.analytic_tag_ids.name, format2)
        #                     sheet.write(row, 9, line.project_id.name, format2)
        #                     sheet.write(row, 10, line.candidate, format2)
        #                     sheet.write(row, 11, line.tenant.name, format2)
        #                     sheet.write(row, 12, line.product_qty, format2)
        #                     sheet.write(row, 13, line.product_uom.name, format2)
        #                     sheet.write(row, 14, delivery_date, format2)
        #                     sheet.write(row, 15, effective_date, format2)
        #                     sheet.write(row, 16, payment_date, format2)
        #                     sheet.write(row, 17, line.price_unit, format2)
        #                     sheet.write(row, 18, line.discount, format2)
        #     #                 sheet.write(row, 19, payment_date, format2)
        #                     sheet.write(row, 20, line.price_subtotal, format2)
        #                     sheet.write(row, 21, id.currency_id.name, format2)
        #     #                 sheet.write(row, 22, payment_date, format2)
        #                     sheet.write(row, 23, line.qty_received, format2)
        #     #                 sheet.write(row, 24, payment_date, format2)
        #                     sheet.write(row, 25, amount_due, format2)
        #                     sheet.write(row, 26, receipt_doc_no, format2)
        #                     sheet.write(row, 27, receipt_doc_date, format2)
        #                     sheet.write(row, 28, line.qty_invoiced, format2)
        #                     sheet.write(row, 29, line.qty_invoiced, format2)
        #                     sheet.write(row, 30, amount_total, format2)
        #                     sheet.write(row, 31, amount_total, format2)
        #     #                 sheet.write(row, 32, line.qty_invoiced, format2)
        #                     sheet.write(row, 33, vendor_name, format2)
        #                     sheet.write(row, 34, vendor_currency, format2)
        #                     sheet.write(row, 35, invoice_date, format2)
        #                     sheet.write(row, 36, account, format2)
        #                     sheet.write(row, 37, invoice_payment_widget, format2)
        #                     sheet.write(row, 38, invoice_payment_widget, format2)
        #     #                 sheet.write(row, 39, invoice_date, format2)
        #                     sheet.write(row, 40, vendor_payment_date, format2)
        #                     sheet.write(row, 41, created_by, format2)
        #                     sheet.write(row, 42, incoterm, format2)
        #                     sheet.write(row, 43, payment_term, format2)
        #
        #                     row = row + 1
        #             else:
        #                 account = None
        #                 sheet.write(row, 0, id.partner_id.name, format2)
        #                 sheet.write(row, 1, id.name, format2)
        #                 sheet.write(row, 2, ordering_date, format2)
        #                 sheet.write(row, 3, id.requisition_id.line_ids.id, format2)
        #                 sheet.write(row, 4, line.purchase_budget_line_id.name, format2)
        #                 sheet.write(row, 5, line.product_id.name, format2)
        #                 sheet.write(row, 6, line.product_id.categ_id.name, format2)
        #                 sheet.write(row, 7, line.name, format2)
        #                 sheet.write(row, 8, line.analytic_tag_ids.name, format2)
        #                 sheet.write(row, 9, line.project_id.name, format2)
        #                 sheet.write(row, 10, line.candidate, format2)
        #                 sheet.write(row, 11, line.tenant.name, format2)
        #                 sheet.write(row, 12, line.product_qty, format2)
        #                 sheet.write(row, 13, line.product_uom.name, format2)
        #                 sheet.write(row, 14, delivery_date, format2)
        #                 sheet.write(row, 15, effective_date, format2)
        #                 sheet.write(row, 16, payment_date, format2)
        #                 sheet.write(row, 17, line.price_unit, format2)
        #                 sheet.write(row, 18, line.discount, format2)
        # #                 sheet.write(row, 19, payment_date, format2)
        #                 sheet.write(row, 20, line.price_subtotal, format2)
        #                 sheet.write(row, 21, id.currency_id.name, format2)
        # #                 sheet.write(row, 22, payment_date, format2)
        #                 sheet.write(row, 23, line.qty_received, format2)
        # #                 sheet.write(row, 24, payment_date, format2)
        #                 sheet.write(row, 25, amount_due, format2)
        #                 sheet.write(row, 26, receipt_doc_no, format2)
        #                 sheet.write(row, 27, receipt_doc_date, format2)
        #                 sheet.write(row, 28, line.qty_invoiced, format2)
        #                 sheet.write(row, 29, line.qty_invoiced, format2)
        #                 sheet.write(row, 30, amount_total, format2)
        #                 sheet.write(row, 31, amount_total, format2)
        # #                 sheet.write(row, 32, line.qty_invoiced, format2)
        #                 sheet.write(row, 33, vendor_name, format2)
        #                 sheet.write(row, 34, vendor_currency, format2)
        #                 sheet.write(row, 35, invoice_date, format2)
        #                 sheet.write(row, 36, account, format2)
        #                 sheet.write(row, 37, invoice_payment_widget, format2)
        #                 sheet.write(row, 38, invoice_payment_widget, format2)
        # #                 sheet.write(row, 39, invoice_date, format2)
        #                 sheet.write(row, 40, vendor_payment_date, format2)
        #                 sheet.write(row, 41, created_by, format2)
        #                 sheet.write(row, 42, incoterm, format2)
        #                 sheet.write(row, 43, payment_term, format2)
        #
        #                 row = row + 1
        #     else:
        #         account = None
        #         sheet.write(row, 0, id.partner_id.name, format2)
        #         sheet.write(row, 1, id.name, format2)
        #         sheet.write(row, 2, ordering_date, format2)
        #         sheet.write(row, 3, id.requisition_id.line_ids.id, format2)
        #         sheet.write(row, 14, delivery_date, format2)
        #         sheet.write(row, 15, effective_date, format2)
        #         sheet.write(row, 16, payment_date, format2)
        #         sheet.write(row, 21, id.currency_id.name, format2)
        #         sheet.write(row, 25, amount_due, format2)
        #         sheet.write(row, 26, receipt_doc_no, format2)
        #         sheet.write(row, 27, receipt_doc_date, format2)
        #         sheet.write(row, 30, amount_total, format2)
        #         sheet.write(row, 31, amount_total, format2)
        #         sheet.write(row, 33, vendor_name, format2)
        #         sheet.write(row, 34, vendor_currency, format2)
        #         sheet.write(row, 35, invoice_date, format2)
        #         sheet.write(row, 36, account, format2)
        #         sheet.write(row, 37, invoice_payment_widget, format2)
        #         sheet.write(row, 38, invoice_payment_widget, format2)
        #         sheet.write(row, 40, vendor_payment_date, format2)
        #         sheet.write(row, 41, created_by, format2)
        #         sheet.write(row, 42, incoterm, format2)
        #         sheet.write(row, 43, payment_term, format2)
        #
        #         row = row + 1
        #