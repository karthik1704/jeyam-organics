{
    'name': 'Custom Tags Display',
    'version': '1.0',
    'summary': 'Display product tags with images on the website',
    'author': 'Karthik A',
    'category': 'Website',
    'depends': ['website_sale', 'product', 'website'],
    'data': [
        'views/health_concern_snippet.xml',
        # 'views/snippet_options.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'custom_tags/static/src/css/health_tags.css',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
}