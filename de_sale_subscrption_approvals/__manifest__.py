# -*- coding: utf-8 -*-
{
    'name': "Sale Subscription Approvals",

    'summary': """
        Sale Subscription Approvals 
        """,

    'description': """
        Sale Subscription Approvals 
        1- Multi Level Approvals
    """,

    'author': "Dynexcel",
    'website': "http://www.dynexcel.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sale Subscription',
    'version': '14.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','approvals','de_operations'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/agreement_stage_views.xml',
        'views/sale_subscription_type_views.xml',
        'views/approval_request_views.xml',
        'views/sale_subscription_agreement_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
