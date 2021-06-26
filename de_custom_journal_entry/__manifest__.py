# -*- coding: utf-8 -*-
{
    'name': "Third-Party Billing",

    'summary': """
           Customize Journal Entries 
           """,

    'description': """
           Customize Journal Entries 
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['de_purchase_subscription','account', 'project','stock','purchase_requisition','purchase','de_travel_request'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/custom_entry_menu.xml',
        'views/custom_entry_type_views.xml',
        'views/custom_entry_stage_views.xml',
        'views/account_move_views.xml',
        'views/custom_entry_views.xml',
        'views/account_payment_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}


