# -*- coding: utf-8 -*-
################################################################################
#

{
    'name': 'Theme Jeyam Organics',
    'version': '17.0.1.0.0',
    'category': 'Theme/eCommerce',
    'summary': "Theme  "
               "theme",
    'description': "",
    'author': 'Karthi',
    'company': 'Vimkes',
    'maintainer': 'Vimkes',
    'website': "",
    'depends': ['website_blog', 'website_sale_wishlist', 'website_sale',
                'website_sale_comparison'],
    'data': [
        
        'views/header_templates.xml',
        
    ],
    'assets': {
        'web.assets_frontend': [
            # 'theme_boec/static/src/js/sale_utils.js',
            "/theme_jeyam/static/src/css/style.css",
            
            "https://fonts.googleapis.com/css2?family=Karla:ital,wght@0,200;0,300;0,400;0,500;0,600;0,700;0,800;1,300;1,500&amp;family=Montserrat&amp;display=swap"
        ],
    },
    'images': [
        
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
