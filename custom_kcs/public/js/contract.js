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
    },
    party_name(frm) {
        if (frm.doc.party_name) {
            frappe.call({
                method: "custom_kcs.src.contract.generate_contract_code",
                args: {
                    party_name: frm.doc.party_name
                },
                callback: function(r) {
                    if (r.message) {
                        frm.set_value("contract_code", r.message);
                    }
                }
            });
        }
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

   




