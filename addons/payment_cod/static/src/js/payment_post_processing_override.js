odoo.define('@your_module/js/payment_post_processing_override', [
    '@web/legacy/js/public/public_widget',
    '@web/core/utils/render',
], function(require) {
    'use strict';

    const publicWidget = require('@web/legacy/js/public/public_widget')[Symbol.for("default")];
    const { renderToElement } = require('@web/core/utils/render');

    // Get the existing PaymentPostProcessing widget
    const PaymentPostProcessing = publicWidget.registry.PaymentPostProcessing;

    // Extend the PaymentPostProcessing Widget
    publicWidget.registry.PaymentPostProcessing = PaymentPostProcessing.extend({
        /**
         * Override _renderTemplate method
         */
        _renderTemplate(xmlid, display_values = {}) {
            this.call('ui', 'unblock');
            const statusContainer = document.querySelector('div[name="o_payment_status_content"]');
            
            if (statusContainer) {
                // Custom logic before rendering
                console.log('Custom _renderTemplate logic');

                // Customize messages based on payment state
                if (display_values.state === 'pending') {
                    display_values.custom_message = "Your payment is still being processed. Please be patient.";
                } else if (display_values.state === 'done') {
                    display_values.custom_message = "Thank you! Your payment was successful.";
                } else if (display_values.state === 'failed') {
                    display_values.custom_message = "Oops! There was an issue with your payment.";
                }

                // Render the template using Odoo's renderToElement utility
                statusContainer.innerHTML = renderToElement(xmlid, display_values).innerHTML;
            } else {
                console.warn('Status Container not found!');
            }
        },
    });
});
