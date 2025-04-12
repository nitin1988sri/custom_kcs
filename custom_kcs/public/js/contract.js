frappe.ui.form.on('Contract', {
    onload: function(frm) {
        frm.fields_dict.contract_branches.grid.get_field('branch').get_query = function(doc, cdt, cdn) {
            let party_name = doc.party_name;
            if (!party_name) {
                frappe.msgprint("Please select a Party Name first.");
                return;
            }
            return {
                filters: {
                    client: party_name
                }
            };
        };
    }
});


frappe.ui.form.on("Contract Addendum", {
    form_render: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        setTimeout(() => {
            const $btn = $(`[data-name="${cdn}"]`).find(".btn-attach:disabled");
            if ($btn.length) {
                $btn.removeAttr("disabled");
                $btn.attr("title", "Upload file");
            }
        }, 300);
    }
});



