import logging
from odoo import http
from odoo.http import request
from odoo.exceptions import UserError

logger = logging.getLogger(__name__)

class PaymentController(http.Controller):


    @http.route('/payment/cod/initiate', type='json', auth='public')
    def initiate_cod_payment(self, **kwargs):
        partner_id = kwargs.get('partner_id')
        amount = kwargs.get('amount')
        currency_id = kwargs.get('currency_id')

        existing_order = request.env['sale.order'].browse(kwargs.get('order_id'))
        if not existing_order:
            # Create a new order if it doesn't exist
            order = request.env['sale.order'].create({
                'partner_id': partner_id,
                'amount_total': amount,
                'currency_id': currency_id,
                'payment_provider_id': provider_id,
            })
            processing_values = {
                'provider_id': order.payment_provider_id.id,
                'provider_code': 'cod',
                'reference': order.name,
                'amount': order.amount_total,
                'currency_id': order.currency_id.id,
                'partner_id': order.partner_id.id,
                'order_id': order.id,  # Include the order_id
            }
            return processing_values

        processing_values = {
            'provider_id': existing_order.payment_provider_id.id,
            'provider_code': 'cod',
            'reference': existing_order.name,
            'amount': existing_order.amount_total,
            'currency_id': existing_order.currency_id.id,
            'partner_id': existing_order.partner_id.id,
            'order_id': order.id,  # Include the order_id
        }
        return processing_values

    @http.route('/payment/cod/confirmation', type='json', auth='public', website=True,  csrf=False)
    def cod_confirmation(self, **kwargs):
        # Retrieve the submitted information from the form
        ref = kwargs.get('reference')
        amount = kwargs.get('amount')
        currency = kwargs.get('currency')
        partner_id = kwargs.get('partner_id')
        currency_id = kwargs.get('currency_id')
        provider_id = kwargs.get('provider_id')
        method_id = kwargs.get('method_id')


        # Perform basic validation
        if not amount:
            raise UserError("Order ID and amount are required.")

        # Fetch the corresponding order
        order_id = ref.split('-')[0]
        logger.debug(f"ref,{ref}")
        logger.info(f"ref,{ref}")
        order = request.env['sale.order'].sudo().search([('name', '=', order_id)], limit=1)
        # order = request.env['sale.order'].sudo().browse(ref)

        
        if not order:
            raise UserError("Order not found.")
            # order = request.env['sale.order'].create({
            #     'partner_id': partner_id,
            #     'amount_total': amount,
            #     'currency_id': currency_id,
            #     # 'payment_provider_id': request.env.ref('payment_cod.payment_method_cod').id,
            #     # 'provider_id': provider_id,

            # })
        print(order)
        unique_reference = f"{order.name}-COD"
        # Create a payment transaction for the COD
        transaction_vals = {
            # 'provider_id': request.env.ref('payment_cod.payment_provider_cod').id,  # Adjust with your actual provider reference
            "payment_method_id": method_id,
            'provider_id': provider_id,
            'reference': unique_reference,
            'amount': float(amount),
            'currency_id': currency_id,
            'partner_id': order.partner_id.id,
            # 'acquirer_reference': f'COD-{order.name}',
            'state': 'done',  # Set to pending for manual processing
        }

        # Create the transaction
        transaction = request.env['payment.transaction'].sudo().create(transaction_vals)
        request.env['payment.transaction'].sudo()._send_cod_confirmation()
        order.sudo().action_confirm()  # Confirm the sale order
        # order._create_invoice()
        # Optionally, update order status to reflect COD status
        # order.write({'state': 'to_invoice'})  # Adjust to fit your workflow

        # Render a confirmation template or redirect
        # return request.render('payment_cod.payment_data', {
        #     'transaction': transaction,
        # })
