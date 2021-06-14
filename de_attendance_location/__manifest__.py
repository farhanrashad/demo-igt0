# -*- coding: utf-8 -*-
{
    'name': "De Attendance Location",

    'summary': """
    Attendance Location of check in and check out
    """,

    'description': """
    Attendance Location of check in and check out
    """,

    'author': "Muhammad Awais",
    'website': "http://www.herawais.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources/Attendances',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_attendance', 'base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'application': True,
    'qweb': [
        "static/src/xml/attendance.xml",
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
