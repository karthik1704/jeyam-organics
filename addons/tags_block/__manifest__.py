{
    'name': 'Tags Block',
    'version': '1.0',
    'summary': 'Display product tags with images on the website',
    'author': 'Karthik A',
    'category': 'Website',
    'depends': ['website_sale', 'product', 'website'],
    'data': [
        'views/tags.xml',
        'views/tags_snippet.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'tags_block/static/src/css/health_tags.css',
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
}