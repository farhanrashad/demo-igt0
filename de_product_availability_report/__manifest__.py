# -*- coding: utf-8 -*-
{
    'name': "Product Availability Report",
    'version': '14.0.0.0',
    'category': 'Reort ',
    'summary': 'Product Availability Report ',
    'sequence': 3,
    'description': """"  """,
    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",
    'license': 'LGPL-3',
    'depends': ['base','stock','report_xlsx'],
    
    'data': [
	
	'security/ir.model.access.csv',   
	'wizards/product_availability_report_wizard.xml',
    'views/product_availability_report_menu.xml',
	'report/product_availiability_report_xlsx.xml'
    ],

    "installable": True,
    "application": True,
    "auto_install": False,
}
