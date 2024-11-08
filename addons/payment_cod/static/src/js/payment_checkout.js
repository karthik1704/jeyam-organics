/** @odoo-module **/

import {_t} from '@web/core/l10n/translation';
import publicWidget from '@web/legacy/js/public/public_widget';
import { ConfirmationDialog } from '@web/core/confirmation_dialog/confirmation_dialog';
import { jsonrpc } from '@web/core/network/rpc_service';
import { debounce } from '@web/core/utils/timing';

import { paymentExpressCheckoutForm } from '@payment/js/express_checkout_form';
import PaymentMixin from '@payment_cod/js/payment_mixin';


console.log("Hi1");

paymentExpressCheckoutForm.include({
    events: Object.assign({}, publicWidget.Widget.prototype.events, {
        'click button[name="o_payment_submit_button"]': '_initiateExpressPayment',
    }),

    // #=== WIDGET LIFECYCLE ===#

    /**
     * @override
     */
    start: async function () {
        await this._super(...arguments);
        document.querySelector('[name="o_payment_submit_button"]')?.removeAttribute('disabled');
        this.rpc = this.bindService('rpc');
        this._initiateExpressPayment = debounce(this._initiateExpressPayment, 500, true);
    },

    // #=== EVENT HANDLERS ===#

    /**
     * Process the payment.
     *
     * @private
     * @param {Event} ev
     * @return {void}
     */
    async _initiateExpressPayment(ev) {
        ev.stopPropagation();
        ev.preventDefault();

        const providerCode = ev.target.closest('[data-provider-code]')?.dataset.providerCode;
        const providerId = ev.target.closest('[data-provider-id]')?.dataset.providerId;
        
        // Handle COD payment directly if provider is COD
        if (providerCode === 'cod') {
            await this._processCodPayment();
            return;
        }

        const shippingInformationRequired = document.querySelector(
            '[name="o_payment_express_checkout_form"]'
        ).dataset.shippingInfoRequired;
        
        let expressShippingAddress = {};
        if (shippingInformationRequired) {
            const shippingInfo = document.querySelector(
                `#o_payment_demo_shipping_info_${providerId}`
            );
            expressShippingAddress = {
                'name': shippingInfo.querySelector('#o_payment_demo_shipping_name').value,
                'email': shippingInfo.querySelector('#o_payment_demo_shipping_email').value,
                'street': shippingInfo.querySelector('#o_payment_demo_shipping_address').value,
                'street2': shippingInfo.querySelector('#o_payment_demo_shipping_address2').value,
                'zip': shippingInfo.querySelector('#o_payment_demo_shipping_zip').value,
                'city': shippingInfo.querySelector('#o_payment_demo_shipping_city').value,
                'country': shippingInfo.querySelector('#o_payment_demo_shipping_country').value,
            };

            const availableCarriers = await this.rpc(
                this.paymentContext['shippingAddressUpdateRoute'],
                { partial_shipping_address: expressShippingAddress },
            );

            if (availableCarriers.length > 0) {
                const id = parseInt(availableCarriers[0].id);
                await this.rpc('/shop/update_carrier', { carrier_id: id });
            } else {
                this.call('dialog', 'add', ConfirmationDialog, {
                    title: _t("Validation Error"),
                    body: _t("No delivery method is available."),
                });
                return;
            }
        }

        await jsonrpc(
            document.querySelector(
                '[name="o_payment_express_checkout_form"]'
            ).dataset['expressCheckoutRoute'],
            {
                'shipping_address': expressShippingAddress,
                'billing_address': {
                    'name': 'Demo User',
                    'email': 'demo@test.com',
                    'street': 'Rue des Bourlottes 9',
                    'street2': '23',
                    'country': 'BE',
                    'city': 'Ramillies',
                    'zip': '1367'
                },
            }
        );

        const processingValues = await jsonrpc(
            this.paymentContext['transactionRoute'],
            this._prepareTransactionRouteParams(providerId),
        );
        
        PaymentMixin.processCODPayment(processingValues);
    },

    /**
     * Process the COD payment flow.
     *
     * @private
     * @return {void}
     */
    async _processCodPayment() {
        // Assuming COD does not need further processing or an API call
        this.call('dialog', 'add', ConfirmationDialog, {
            title: _t("Cash on Delivery"),
            body: _t("Your order has been placed and will be paid upon delivery."),
            confirm: async () => {
                window.location.href = '/payment/success'; // Redirect to the success page
            },
        });
    },
});
