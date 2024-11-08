from odoo import models, fields
from odoo.exceptions import UserError

class PaymentProviderCOD(models.Model):
    _inherit = 'payment.provider'

    
    code = fields.Selection(
        selection_add=[('cod', 'Cash on Delivery')],
        ondelete={'cod': 'set default'},
    )

    def _cod_get_default_payment_method_id(self):
        """ Define the default payment method for COD. """
        return self.env.ref('payment_cod.payment_method_cod').id

    def _create_payment_cod(self, **kwargs):
        """Create a payment transaction record for Cash on Delivery"""
        
        # Ensure that required parameters are available
        order = kwargs.get('order')
        if not order:
            raise UserError("Order information is required for COD payment.")
        
        # Create a payment transaction
        transaction_vals = {
            'provider_id': self.id,
            'reference': order.name,
            'amount': order.amount_total,
            'currency_id': order.currency_id.id,
            'partner_id': order.partner_id.id,
            'acquirer_reference': 'COD-{}'.format(order.name),
            'state': 'done',  # Set to pending for manual processing
        }
        
        # Create and return the transaction
        transaction = self.env['payment.transaction'].create(transaction_vals)
        
        # Optionally update order status to reflect COD status
        order.write({'payment_state': 'to_invoice'})  # Example state; adjust to fit your workflow
        return transaction


class PaymentTransactionCOD(models.Model):
    _inherit = 'payment.transaction'

    def _send_cod_confirmation(self):
        """Logic to handle COD confirmation, e.g., sending an email or notification"""
        # You can use this method to confirm the COD payment
        self._set_done()

        for transaction in self:
            # Custom logic to confirm or notify about the COD transaction
            transaction.state = 'done'  # Mark as done when COD is confirmed
            # Additional notification or confirmation logic