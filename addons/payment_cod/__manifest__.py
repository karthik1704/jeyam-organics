{
    'name': 'Payment Provider: Cash On Delivery',
    'version': '17.0.1.0.0',
    'category': 'Accounting/Payment Providers',
    'depends': ['payment', 'website_sale'],
    'data': [
        'views/payment_cod_templates.xml',
        'data/payment_provider_data.xml',
        'security/ir.model.access.csv',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}