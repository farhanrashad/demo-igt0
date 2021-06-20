import json
from odoo import models
from odoo.exceptions import UserError


class GenerateXLSXReport(models.Model):
    _name = 'report.de_payslip_batch_report.payslip_batch_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, line):
        #         raise UserError(data['id'])
        format1 = workbook.add_format({'font_size': '12', 'align': 'vcenter', 'bold': True})
        sheet = workbook.add_worksheet('Payslip Batch Report')
        sheet.write(3, 0, 'Account Name', format1)
        sheet.write(3, 1, 'Account No', format1)
        sheet.write(3, 2, 'Amount', format1)
        sheet.write(3, 3, 'Currency', format1)

        format2 = workbook.add_format({'font_size': '12', 'align': 'vcenter'})
        row = 4
        sheet.set_column(row, 0, 50)
        sheet.set_column(row, 1, 25)
        sheet.set_column(row, 2, 20)
        sheet.set_column(row, 3, 20)


        #         get_wiz = self.env['pay.slip.batch'].search(data['id'])
        #         count = 1
        #         for order in get_wiz:
        sheet.write(row, 0, data['contract_type'], format2)
        sheet.write(row, 1, data['doe'], format2)
        sheet.write(row, 2, data['debit_ac_no'], format2)
        sheet.write(row, 3, data['currency'], format2)

#             count = count + 1
#             row = row + 1
