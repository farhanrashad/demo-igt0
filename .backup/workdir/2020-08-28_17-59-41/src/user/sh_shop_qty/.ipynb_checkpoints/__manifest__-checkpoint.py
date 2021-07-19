# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name" : "Product Shop Bunch Quantity",
    "author" : "Dynexcel",
    "support": "info@dynexcel.com",
    "website": "https://www.softhealer.com",
    "category": "Website",
    "summary": "Website Product Shop.",
    "description": """Website Product Shop.""",
    "version":"1.1",
    "depends" : ['sale_management', 'account', 'web', 'website', 'website_sale'],
    "data" : [  
            'views/sh_product_view.xml',
            'views/assets.xml',
            'views/sh_shop_template.xml',
            ],
    
#     "images": ['static/description/background.png', ],
                  
    "auto_install":False,
    "application" : True,
    "installable" : True,
}
