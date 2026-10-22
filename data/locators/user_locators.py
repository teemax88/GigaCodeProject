"""User management page locators."""

from dataclasses import dataclass


@dataclass(frozen=True)
class UserLocators:
    """All locators for user management pages."""

    # User list page
    user_list_title: str = "h1"
    add_user_button: str = 'button[data-testid="add-user"]'
    user_table: str = "#user-table"
    user_table_row: str = "#user-table tr"
    search_field: str = "#search-users"
    pagination: str = ".pagination"
    page_number: str = f"{'.pagination'} button"

    # User detail page
    user_detail_title: str = "h1"
    user_name: str = ".user-name"
    user_email: str = ".user-email"
    edit_button: str = 'button[data-testid="edit-user"]'
    delete_button: str = 'button[data-testid="delete-user"]'
    back_button: str = 'a[data-testid="back"]'

    # User form
    form_first_name: str = "#form-first-name"
    form_last_name: str = "#form-last-name"
    form_email: str = "#form-email"
    form_phone: str = "#form-phone"
    form_save: str = 'button[type="submit"]'
    form_cancel: str = 'button[data-testid="cancel"]'
    form_validation_error: str = ".form-error"
    form_success: str = ".form-success"

    # Confirm dialog
    confirm_dialog: str = ".confirm-dialog"
    confirm_dialog_message: str = ".confirm-dialog__message"
    confirm_dialog_confirm: str = '.confirm-dialog button:first-child'
    confirm_dialog_cancel: str = '.confirm-dialog button:last-child'
