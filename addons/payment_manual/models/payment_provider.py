# -*- coding: utf-8 -*-
# custom_cod_payment/models/payment_provider.py

from odoo import api, fields, models, _

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('custom_cod', 'Cash on Delivery')],
        ondelete={'custom_cod': 'set default'}
    )

    @api.model
    def _get_compatible_providers(self, *args, currency_id=None, **kwargs):
        """ Override of payment to filter out COD payment providers based on currency. """
        providers = super()._get_compatible_providers(*args, currency_id=currency_id, **kwargs)
        if currency_id:
            currency = self.env['res.currency'].browse(currency_id)
            # You can add specific currency restrictions here if needed
        return providers

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """ Override of payment to return custom rendering values for COD transactions. """
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'custom_cod':
            return res

        return {
            'reference': self.reference,
            'amount': self.amount,
            'currency': self.currency_id.name,
        }

    def _process_notification_data(self, data):
        """ Override of payment to process the transaction based on COD notification data. """
        super()._process_notification_data(data)
        if self.provider_code != 'custom_cod':
            return

        self._set_pending()