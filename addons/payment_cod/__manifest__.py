{
    'name': 'Payment Provider: Cash On Delivery',
    'version': '17.0.1.0.0',
    'category': 'Accounting/Payment Providers',
    'depends': ['payment',],
    'data': [
        'views/payment_cod_templates.xml',
        'views/confirmation_template.xml',
        'data/payment_method_cod.xml', 
        # 'data/payment_provider_data.xml',
        
    ],
    'assets': {
        'web.assets_frontend': [
            'payment_cod/static/src/js/**/*',  # Add your JS file here
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}