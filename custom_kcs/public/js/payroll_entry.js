frappe.ui.form.on('Payroll Entry', {

    before_save: function(frm) {
        const selected_customers = [];
        const selected_branches = [];

        $(".cust_cb:checked").each(function() {
            selected_customers.push($(this).val());
        });

        $(".branch_cb:checked").each(function() {
            selected_branches.push($(this).val());
        });

        frm.set_value("selected_customers", JSON.stringify(selected_customers));
        frm.set_value("selected_branches", JSON.stringify(selected_branches));
    },

    onload: function(frm) {
        frappe.ui.form.off('Payroll Entry', 'get_employee_details');
        render_customer_branch_section(frm);
    },
    refresh: function(frm) {
         frappe.ui.form.off('Payroll Entry', 'get_employee_details');
         frappe.ui.form.on('Payroll Entry', {
             get_employee_details: function (frm) {
                 return frappe.call({
                     method: "custom_kcs.src.payroll_entry.get_custom_employees",
                     args: { payroll_entry: frm.doc.name },
                     callback: function (r) {
                         console.log("Custom overridden employee fetch working!", r.message);
                         frm.reload_doc();
                     }
                 });
             }
         });

        frm.add_custom_button(__('Generate Employee Incentives'), () => {
            if (!frm.doc.start_date) {
                frappe.msgprint("⚠️ Please select Start Date first.");
                return;
            }

            frappe.confirm(
                `Are you sure you want to generate Employee Incentives for <b>${frm.doc.start_date}</b>?`,
                () => {
                    frappe.call({
                        method: 'custom_kcs.src.cron.employee_Incentive.generate_employee_incentives_for_all',
                        args: {
                            start_date: frm.doc.start_date
                        },
                        callback: function(r) {
                            if (r.message && r.message.status === "success") {
                                frappe.msgprint(`${r.message.total_created} Employee Incentives created.`);
                            } else {
                                frappe.msgprint('⚠️ Something went wrong while generating incentives.');
                            }
                        }
                    });
                }
            );
        }).addClass('btn-primary');
    }
});


function render_customer_branch_section(frm) {
    if ($('#custom_filter_section').length) return;

    const selected_customers = frm.doc.selected_customers ? JSON.parse(frm.doc.selected_customers) : [];
    const selected_branches = frm.doc.selected_branches ? JSON.parse(frm.doc.selected_branches) : [];

    const target = frm.get_field('employees').wrapper;
    const filter_html = `<div id="custom_filter_section" style="border:1px solid #d1d8dd; padding:15px; margin-bottom: 15px; border-radius:6px">
        <h4 style="margin-top:0; margin-bottom:10px;">Customer and Branch Filter</h4>
        <div id="customer_area"></div>
        <div id="branch_area" style="margin-top: 10px;"></div>
    </div>`;
    $(target).before(filter_html);

    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Customer",
            fields: ["name"]
        },
        callback: function(res) {
            frm.reload_doc();
            setTimeout(() => {
                render_customer_branch_section(frm);
            }, 1000);
            
            const customers = res.message;
            let html = `<label><b>Select Customers:</b></label><br/>`;

            customers.forEach(cust => {
                const checked = selected_customers.includes(cust.name) ? "checked" : "";
                html += `<label><input type='checkbox' class='cust_cb' value='${cust.name}' ${checked}/> ${cust.name}</label><br/>`;
            });

            $("#customer_area").html(html);

            // render branches for initially selected customers
            if (selected_customers.length) {
                fetch_branches_and_render(selected_customers, selected_branches);
            }

            $(".cust_cb").on("change", function () {
                let selected = [];
                $(".cust_cb:checked").each(function () {
                    selected.push($(this).val());
                });

                fetch_branches_and_render(selected, []);
            });
        }
    });
}
function fetch_branches_and_render(customers, preselected_branches=[]) {
    const $branchArea = $("#branch_area");

    if (!customers.length) {
        $branchArea.html("");
        return;
    }

    frappe.call({
        method: "frappe.client.get_list",
        args: {
            doctype: "Branch",
            filters: { client: ["in", customers] },
            fields: ["name", "client"]
        },
        callback: function (res) {
            const branches = res.message;
            const grouped = {};

            branches.forEach(branch => {
                if (!grouped[branch.client]) grouped[branch.client] = [];
                grouped[branch.client].push(branch);
            });

            Object.keys(grouped).forEach(client => {
                if ($(`#branch-box-${client}`).length) return;

                let html = `
                    <div id="branch-box-${client}" class="branch-group" style="border:1px solid #d1d8dd; padding:10px 15px; margin-bottom: 10px; border-radius:6px;">
                        <h5 style="margin-top:0; color: #4C4C4C;">${client}</h5>
                        <div class="branch-cards" style="display:flex; flex-wrap:wrap; gap:10px;">`;

                grouped[client].forEach(branch => {
                    const checked = preselected_branches.includes(branch.name) ? "checked" : "";
                    html += `
                        <label style="display:inline-flex; align-items:center; gap:6px; border:1px solid #ccc; padding:6px 10px; border-radius:4px; min-width:180px;">
                            <input type='checkbox' class='branch_cb' value='${branch.name}' data-client='${branch.client}' style="margin:0;" ${checked}/>
                            <span>${branch.name}</span>
                        </label>`;
                });

                html += `</div></div>`;
                $branchArea.append(html);
            });

            $(".cust_cb").off("change").on("change", function () {
                const client = $(this).val();
                const checked = $(this).is(":checked");

                if (!checked) {
                    $(`#branch-box-${client}`).remove();
                } else {
                    if (!$(`#branch-box-${client}`).length) {
                        fetch_branches_and_render([client]);
                    }
                }
            });

            $(".branch_cb").on("change", function () {
                const selected_branches = [];
                $(".branch_cb:checked").each(function () {
                    selected_branches.push($(this).val());
                });

            });
        }
    });
}


// frappe.ui.form.on('Payroll Entry', {
//     get_employee_details: function (frm) {
//         return frappe.call({
//             doc: frm.doc,
//             method: "fill_employee_details",
//             freeze: true,
//             freeze_message: __("Fetching Employees"),
//         }).then((r) => {
//             if (r.docs?.[0]?.employees) {
//                 frm.dirty();
//                 frm.save();
//             }

//             frm.refresh();

//             if (r.docs?.[0]?.validate_attendance) {
//                 render_employee_attendance(frm, r.message);
//             }

//             frm.scroll_to_field("employees");
//         });
//     }
// });

// frappe.ui.form.on("Payroll Entry", {
    
// });