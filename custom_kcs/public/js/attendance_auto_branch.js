frappe.ui.form.on('Attendance', {
  onload: frm => try_autofill(frm),
  employee: frm => try_autofill(frm),
  attendance_date: frm => try_autofill(frm)
});

async function try_autofill(frm) {
  if (!frm.doc.employee || !frm.doc.attendance_date) return;

  frm.toggle_display('branch', true);  
  frm.toggle_display('shift', true);

  frm.set_df_property('branch', 'read_only', 0);
  frm.set_df_property('shift', 'read_only', 0);

  frm.dashboard?.clear_headline();

  frappe.call({
    method: 'custom_kcs.src.attendance_helpers.resolve_effective_branch_shift',
    args: {
      employee_id: frm.doc.employee,
      attendance_date: frm.doc.attendance_date
    }
  }).then(r => {
    if (!r || !r.message) return;
    const data = r.message;

    if (data.branch) frm.set_value('branch', data.branch);
    if (data.shift)  frm.set_value('shift',  data.shift);

    const tag = data.mode === 'OVERTIME' ? 'Overtime' :
                data.mode === 'BRANCH_SWITCH' ? 'Branch Switch' : 'Primary';

    frm.dashboard?.set_headline(
      `<span class="indicator ${data.mode==='OVERTIME'?'red':(data.mode==='BRANCH_SWITCH'?'orange':'blue')}">` +
      `${frappe.utils.escape_html(tag)} for ${frappe.datetime.str_to_user(frm.doc.attendance_date)}</span>`
    );
  }).catch(e => {
    // silent log
    console.error('Auto-branch populate failed', e);
  });
}
