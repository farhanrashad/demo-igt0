# -*- coding: utf-8 -*-
{
    'name': "Stock Transfer Material Approvals",
    'summary': """
    Transfer Material Approvals
        """,
    'description': """
Stock Transfer Material Approvals
============================================
1 - Approvals
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",
    'category': 'Purchase',
    'version': '14.0.0.1',
    'depends': ['approvals','de_stock_material_transfer'],
    'data': [
        #'security/ir.model.access.csv',
        'views/approval_request_views.xml',
        'views/approval_approver_views.xml',
        'views/stock_transfer_order_views.xml',
    ],
}
