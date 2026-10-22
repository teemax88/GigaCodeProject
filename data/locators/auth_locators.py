"""Authentication page locators."""

from dataclasses import dataclass


@dataclass(frozen=True)
class AuthLocators:
    """All locators for authentication pages."""

    # Login page
    username_field: str = "#username"
    password_field: str = "#password"
    login_button: str = 'button[type="submit"]'
    error_message: str = ".error-message"
    forgot_password_link: str = 'a[href*="forgot"]'
    remember_me_checkbox: str = "#remember-me"
    register_link: str = 'a[href*="register"]'
    login_page_title: str = "h1"

    # Register page
    register_page_title: str = "h1"
    first_name_field: str = "#first-name"
    last_name_field: str = "#last-name"
    email_field: str = "#email"
    confirm_password_field: str = "#confirm-password"
    register_button: str = 'button[type="submit"]'
    terms_checkbox: str = "#terms"
    terms_link: str = 'a[href*="terms"]'
    success_message: str = ".success-message"

    # Password reset
    reset_email_field: str = "#reset-email"
    reset_button: str = 'button[type="submit"]'
    back_to_login_link: str = 'a[href*="login"]'

    # Common
    navigation_menu: str = "#main-nav"
    user_avatar: str = ".user-avatar"
    logout_button: str = 'button[data-testid="logout"]'
