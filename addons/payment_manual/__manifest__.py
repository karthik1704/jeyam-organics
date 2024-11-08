# -*- coding: utf-8 -*-
# custom_cod_payment/__manifest__.py

{
    'name': 'Custom Cash on Delivery Payment Provider',
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'summary': 'Custom implementation of Cash on Delivery payment provider',
    'description': """
        This module adds Cash on Delivery as a payment provider option.
        It allows customers to select COD as their payment method during checkout.
    """,
    'depends': ['payment'],
    'data': [
        'views/payment_provider_views.xml',
        'data/payment_provider_data.xml',
    ],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}