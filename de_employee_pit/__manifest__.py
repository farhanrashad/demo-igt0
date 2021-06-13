# -*- coding: utf-8 -*-
{
    'name': "Employee PIT",
    'summary': """Employee PIT""",
    'description': """ """,
    'author': "Dynexcel",
    'website': "https://www.dynexcel.com",
    'category': 'Human Resource',
    'version': '14.0.0.1',
    'depends': ['base', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'data/form_name.xml',
        'views/employee_pit.xml',
        'views/employee_pit_menu.xml',
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
