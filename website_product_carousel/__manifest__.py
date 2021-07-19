{
    'name': 'Website Product Carousel Slider',
    'summary': 'Easily drag and drop Website Product Carousel and Quickly Configure our Product Carousel',
    'description': 'Easily drag and drop Website Product Carousel and Quickly Configure our Product Carousel',
    'category': 'Website/eCommerce',
    'version': '12.0.1.0.1',
    'author': 'Tecspek',
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/carousel_snippet_options.xml',
        'views/website_filter_view.xml',
        'views/product_carousel.xml',
        'views/product_view.xml',
    ],
    'depends': [
        'website_sale',
        'rating',
        'website_sale_wishlist',
    ],
    'images': [
        'static/description/banner.png'
    ],
    'support': 'help.tecspek@gmail.com',
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 49,
    'license': 'OPL-1',
    'currency': 'EUR',
}
