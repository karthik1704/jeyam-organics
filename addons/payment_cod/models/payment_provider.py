# payment_cod/models/payment_provider.py
from odoo import api, fields, models

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('cod', 'Cash On Delivery')],
        ondelete={'cod': 'set default'})

    @api.model
    def _get_compatible_providers(self, *args, **kwargs):
        providers = super()._get_compatible_providers(*args, **kwargs)
        if self.env.context.get('website_sale_order_id'):
            return providers.filtered(lambda p: p.code in ['cod'])
        return providers
    
    def _get_validation_amount(self):
        self.ensure_one()
        if self.code == 'cod':
            return 0.0
        return super()._get_validation_amount()

    def _should_build_inline_form(self, is_validation=False):
        self.ensure_one()
        if self.code == 'cod':
            return False
        return super()._should_build_inline_form(is_validation=is_validation)