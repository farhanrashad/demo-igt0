# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "Sale Subscription",
    "category": 'Sale',
    "summary": 'Sale Subscription',
    "description": """
    Sale Subscription
    """,
    "sequence": 1,
    "author": "Dynexcel",
    "website": "https://www.dynexcel.com",
    "version": '14.1.0.4',
    "depends": ['sales_team','account'],
    "data": [
        'security/security.xml',
        'security/ir.model.access.csv',
        #'data/data.xml',
        'data/sequence.xml',
        'views/subscription_menus.xml',
        'views/product_views.xml',
        'views/sale_subscription_stage_views.xml',
        'views/sale_subscription_plan_views.xml',
        'views/sale_subscription_views.xml',       
    ],
    
    "price": 55,
    "currency": 'EUR',
    "installable": True,
    "application": False,
    "auto_install": False,
}
