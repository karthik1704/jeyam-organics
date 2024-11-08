/** @odoo-module **/

import paymentForm from '@payment/js/payment_form';
import paymentMixin from '@payment_cod/js/payment_mixin';

console.log("Hi");

paymentForm.include({
    // events: Object.assign({}, publicWidget.Widget.prototype.events, {
    //     'click button[name="o_payment_submit_button"]': '_prepareInlineForm',
    // }),

    


    // #=== DOM MANIPULATION ===#

    /**
     * Prepare the inline form for Cash on Delivery.
     *
     * @override method from @payment/js/payment_form
     * @private
     * @param {number} providerId - The id of the selected payment option's provider.
     * @param {string} providerCode - The code of the selected payment option's provider.
     * @param {number} paymentOptionId - The id of the selected payment option
     * @param {string} paymentMethodCode - The code of the selected payment method, if any.
     * @param {string} flow - The online payment flow of the selected payment option.
     * @return {void}
     */
    async _prepareInlineForm(providerId, providerCode, paymentOptionId, paymentMethodCode, flow) {
        if (providerCode !== 'cod') {
            this._super(...arguments);
            return;
        }

        console.log(providerCode, "prepareInlineForm")

        // For COD, we simply set the flow to 'direct' since no API call is needed.
        this._setPaymentFlow('direct');

        // Optionally, you can display specific UI components for COD here.
        const codMessage = document.createElement('div');
        codMessage.innerHTML = '<p>Cash on Delivery - Payment will be collected upon delivery.</p>';
        this.$('.payment-form').append(codMessage);
    },

    // #=== PAYMENT FLOW ===#

    /**
     * Simulate a feedback from a COD provider and redirect the customer to the status page.
     *
     * @override method from payment.payment_form
     * @private
     * @param {string} providerCode - The code of the selected payment option's provider.
     * @param {number} paymentOptionId - The id of the selected payment option.
     * @param {string} paymentMethodCode - The code of the selected payment method, if any.
     * @param {object} processingValues - The processing values of the transaction.
     * @return {void}
     */
    async _processDirectFlow(providerCode, paymentOptionId, paymentMethodCode, processingValues) {
        if (providerCode !== 'cod') {
            this._super(...arguments);
            return;
        }

        console.log(providerCode)
    
        // For COD, we directly confirm the payment
        // Here, you can simulate a successful payment confirmation.
        const orderConfirmed = true; // Simulate the order confirmation logic
        paymentMixin.processCODPayment(processingValues);
        if (orderConfirmed) {
            // Redirect to the success page
            window.location.href = '/payment/success';
        } else {
            // Redirect to the failure page
            window.location.href = '/payment/failure';
        }
    },

    async _processRedirectFlow(providerCode, paymentOptionId, paymentMethodCode, processingValues) {
        // if (providerCode !== 'cod') {
        //     this._super(...arguments);
        //     return;
        // }
        console.log('providerCode', providerCode);
        console.log(processingValues);
        console.log(paymentMethodCode)
        console.log(paymentOptionId)
    
        // For COD, we directly confirm the payment
        // Here, you can simulate a successful payment confirmation.
        const orderConfirmed = true; // Simulate the order confirmation logic
        paymentMixin.processCODPayment(processingValues, paymentOptionId);
        // if (orderConfirmed) {
        //     // Redirect to the success page
        //     window.location.href = '/payment/cod/confirmation';
        // } else {
        //     // Redirect to the failure page
        //     window.location.href = '/payment/failure';
        // }
    },

});
