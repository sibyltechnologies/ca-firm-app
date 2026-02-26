import frappe


def before_save(doc, method):
    """Called before any CA Engagement save"""
    _auto_set_status_from_progress(doc)


def on_submit(doc, method):
    """Called when engagement is submitted"""
    pass  # Handled in controller


def on_cancel(doc, method):
    """Called when engagement is cancelled"""
    pass  # Handled in controller


def _auto_set_status_from_progress(doc):
    if doc.progress_percent == 100 and doc.status not in ("Completed", "Cancelled", "Billed"):
        doc.status = "Completed"
    elif doc.progress_percent == 0 and doc.status == "In Progress":
        pass  # don't auto-revert
