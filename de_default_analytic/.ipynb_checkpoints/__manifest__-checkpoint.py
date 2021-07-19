# -*- coding: utf-8 -*-
{
    'name': "Default Analytic",

    'summary': """
        Analytical Account Default
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','product','sale','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_view.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}