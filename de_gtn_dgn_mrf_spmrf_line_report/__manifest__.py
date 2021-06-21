# -*- coding: utf-8 -*-

{
    "name": "GTN-GDN-MRF-SPMRF Lines Report",
    'version': '14.0.0.0',
    "category": 'GTN-GDN-MRF-SPMRF Lines Report',
    "summary": ' GTN-GDN-MRF-SPMRF Lines Report',
    'sequence': 1,
    "description": """"Generate GTN-GDN-MRF-SPMRF Lines Report """,
    "author": "Dynexcel",
    "website": "http://www.dynexcel.co",
    'depends': ['base','stock','purchase','hr','de_stock_material_transfer'],
    'data': [
	'security/ir.model.access.csv',
        'wizards/gtn_dgn_mrf_spmrf_wizard.xml',
        'views/view_stock_transfer_order.xml',
        #'reports/mrf_report.xml',
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}

