# -*- coding: utf-8 -*-

{
    'name': 'EMPFIN Advance Salary',
    'version': '14.0.0.2',
    'summary': 'Advance Salary In HR',
    'description': """
        Helps you to manage Advance Salary Request of your company's staff.
        """,
    'category': 'Human Resources',
    'author': "Dynexcel",
    'company': 'Dynexcel',
    'maintainer': 'Dynexcel',
    'website': "https://www.dynexcel.com",
    'depends': [
        'hr_payroll', 'de_empfin_core', 'account_accountant', 
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/salary_advance_data.xml',
        'views/salary_structure_views.xml',
        'views/salary_advance_views.xml',
    ],
    'demo': [],
    'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}

