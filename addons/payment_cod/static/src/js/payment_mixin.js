/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { jsonrpc, RPCError } from "@web/core/network/rpc_service";

export default {

    /**
     * Process a COD payment and redirect the customer to the order confirmation page.
     *
     * @private
     * @param {object} processingValues - The processing values of the transaction.
     * @return {void}
     */
    async processCODPayment(processingValues, method_id) {
        console.log('creating order');
        try {
            // Optional: Collect any additional input specific to COD, if needed
            const orderReference = processingValues.reference;
            console.log('orderReference', orderReference);
            // Call the COD endpoint
            await jsonrpc('/payment/cod/confirmation', {
                'reference': orderReference,
                "amount": processingValues.amount,
                "currency_id": processingValues.currency_id,
                "order_id": processingValues.reference,
                "partner_id": processingValues.partner_id,
                "provider_id": processingValues.provider_id,
                "method_id": method_id,

                // Include other COD-specific values if needed
            });

            // Redirect the user to a status or confirmation page
            window.location = '/payment/status';
        } catch (error) {
            if (error instanceof RPCError) {
                // Display an error dialog if there's a payment issue
                this._displayErrorDialog(_t("COD payment processing failed"), error.data.message);
            } else {
                // Handle non-RPC errors by logging them or further troubleshooting
                console.error("Unexpected error during COD processing:", error);
                throw error;
            }
        }
    },

    /**
     * Display an error dialog if payment fails.
     *
     * @param {string} title - The title of the error dialog.
     * @param {string} message - The error message to display.
     * @private
     */
    _displayErrorDialog(title, message) {
        // Implement error dialog logic, e.g., using Odoo's Dialog service
        console.error(`${title}: ${message}`);
    },

};
