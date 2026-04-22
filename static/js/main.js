// ============================================================
// main.js  –  Client-side helpers for Student Performance Analysis and Visualization Dashboard
// ============================================================
// This file is loaded at the bottom of every page via base.html.
// It provides three small utilities:
//   1. Auto-dismiss flash alerts after 5 seconds
//   2. confirmDelete() – shows a browser confirm dialog before delete
//   3. validateMarks() – clamps a marks input between 0 and max
// ============================================================


// ── 1. Auto-dismiss alerts ───────────────────────────────────
// Runs after the full DOM is loaded.
// Finds every .alert that is NOT .alert-info (info alerts stay
// visible because they contain important instructions).
// After 5 000 ms it calls Bootstrap's Alert.close() to fade them out.
document.addEventListener('DOMContentLoaded', function () {

    // Select all alert elements except info-type alerts
    const alerts = document.querySelectorAll('.alert:not(.alert-info)');

    alerts.forEach(function (alert) {
        setTimeout(function () {
            // Bootstrap 5 Alert component – closes with animation
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000); // 5 000 ms = 5 seconds
    });

});


// ── 2. confirmDelete ─────────────────────────────────────────
// Called from delete buttons in templates, e.g.:
//   onclick="return confirmDelete('Delete this student?')"
// Returns true  → the link/form proceeds (delete happens)
// Returns false → the action is cancelled
function confirmDelete(message) {
    // Use the provided message or fall back to a generic one
    return confirm(message || 'Are you sure you want to delete this item?');
}


// ── 3. validateMarks ─────────────────────────────────────────
// Called oninput on marks entry fields, e.g.:
//   oninput="validateMarks(this, 10)"
// Prevents a user from typing a negative number or a number
// higher than the question's maximum marks.
// input   – the <input> element
// maxMarks – the maximum allowed value for that question
function validateMarks(input, maxMarks) {
    const value = parseInt(input.value); // parse current typed value

    if (value < 0) {
        input.value = 0;        // clamp to minimum (0)
    } else if (value > maxMarks) {
        input.value = maxMarks; // clamp to maximum allowed marks
    }
}
