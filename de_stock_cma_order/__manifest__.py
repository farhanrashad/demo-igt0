# -*- coding: utf-8 -*-
{
    'name': "Contractor Material Requisition",

    'summary': """
    Contractor Material Requisition - CMA
        """,

    'description': """
        Contractor Material Requisition:-
        1 - Issue Material for Consumption
        2 - Issue & Return Material
        3 - Material replacement
        4 - Dependency on transfer order
    """,

    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",
    'category': 'Warehouse',
    'version': '14.0.0.1',
    'depends': ['base', 'stock','purchase','account'],
    'data': [
        'security/cma_security.xml',
        'security/ir.model.access.csv',
        'data/cma_data.xml',
        'views/stock_cma_menu.xml',
        #'wizard/cma_order_replace_wizard_views.xml',
        'views/account_move_views.xml',
        'views/stock_picking_views.xml',
        'views/stock_cma_type_views.xml',
        'views/stock_cma_condition_views.xml',
        'views/stock_cma_order_views.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
