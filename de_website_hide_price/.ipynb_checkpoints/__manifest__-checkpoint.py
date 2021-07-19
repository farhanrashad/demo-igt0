# -*- coding: utf-8 -*-
{
    'name': "Website Hide Price",

    'summary': """
        Show/Hide Product Price""",

    'description': """
        Show/Hide product prices at website
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Website',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','website_sale','website_product_carousel','de_website_tiered_pricing','de_carousel_tiered_pricing', 'crm'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'data/website_hide_price.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}