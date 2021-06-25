import xlwt
from odoo import models
import datetime


class ProductAvailableReport(models.AbstractModel):
    _name = 'report.de_product_availability_report.product_xlsx_report'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        format1 = workbook.add_format({'font_size':'12', 'align':'vcenter', 'bold':True})
        format2 = workbook.add_format({'font_size':'12', 'align':'vcenter', 'bold':False})
        
        width = 4
        sheet = workbook.add_worksheet('Product Availability Report')
        sheet.merge_range('C2:E2', 'Check Product Availability in ' + str(data['location_name']) , format1)
#         sheet.write(1, 4, 'Check Product Availability in ' + str(data['location_name']) , format1)
        sheet.write(3, 0, 'Report Date ', format1)
        sheet.write(3, 1, data['date'], format1)
        
        sheet.write(5, 0, 'Product', format1)
        sheet.write(5, 1, 'Product Code', format1)
        sheet.write(5, 2, 'UOM', format1)
        sheet.write(5, 3, 'Onhand Qty', format1)
        sheet.write(5, 4, 'Available Qty', format1)
        sheet.write(5, 5, 'Received Qty in Mrf', format1)
        sheet.write(5, 6, 'Received Qty in SP Mrf', format1)
        
        products = self.env['stock.quant'].search([('product_id', 'in', data['product_ids']),('location_id', '=',data['location_id'])])
        print('products-----',products)
        row = 6
        col = 1
        width = 4
#         format3 = workbook.add_format({'font_size':'12', 'align':'vcenter', 'bold':True})
        sheet.set_column(0, 0, 30)
        sheet.set_column(1, 1, 15)
        sheet.set_column(2, 2, 15)
        sheet.set_column(3, 3, 15)
        sheet.set_column(4, 4, 15)
        sheet.set_column(5, 5, 20)
        sheet.set_column(6, 6, 20)
        
        for product in products:
            print('product-----',product.product_id.name)
            print('inventory_quantity-----',product.inventory_quantity)
            
            sheet.write(row, 0, product.product_id.name, format2)
            sheet.write(row, 1, product.product_id.barcode, format2)
            sheet.write(row, 2, product.product_id.uom_id.name, format2)
            sheet.write(row, 3, product.available_quantity, format2)
            sheet.write(row, 4, product.available_quantity, format2)
            row = row + 1

