# -*- coding: utf-8 -*-
{
    'name': "Website Prices",

    'summary': """
        Display all prices rules""",

    'description': """
        Display all pricelist prices with quanity at shop page
    """,

    'author': "dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'website',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','website_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}