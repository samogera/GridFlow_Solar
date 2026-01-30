frappe.ui.form.on('GridFlow Device', {
    refresh: function(frm) {
        // Add a custom button to the top of the form
        frm.add_custom_button(__('Mint Carbon Credits'), function() {
            frappe.call({
                method: "gridflow.api.process_stellar_minting",
                args: {
                    device_id: frm.doc.name
                },
                callback: function(r) {
                    if (r.message) {
                        frappe.msgprint(__("Successfully created Batch: " + r.message));
                        frm.reload_doc();
                    }
                }
            });
        }, __("Actions"));
    }
});