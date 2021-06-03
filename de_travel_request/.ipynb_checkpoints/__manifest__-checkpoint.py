# -*- coding: utf-8 -*-
{
    'name': "Travel Request",
    'summary': """Travel Request""",
    'description': """ """,
    'author': "Dynexcel",
    'website': "http://www.dynexcel.co",
    'category': 'Hr',
    'version': '14.0.0.0',
    'depends': ['base', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'data/form_name.xml',
        'views/travel_request_menu.xml',
        'views/travel_request_view.xml',
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
