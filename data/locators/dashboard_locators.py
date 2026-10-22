"""Dashboard page locators."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DashboardLocators:
    """All locators for dashboard page."""

    # Main elements
    dashboard_title: str = "h1"
    welcome_message: str = ".welcome-message"

    # Stats cards
    stats_card: str = ".stat-card"
    stats_card_value: str = f"{'.stat-card'} .value"
    stats_card_label: str = f"{'.stat-card'} .label"

    # Charts
    chart_container: str = ".chart-container"
    chart_canvas: str = "canvas"

    # Recent activity
    activity_list: str = ".activity-list"
    activity_item: str = f"{'.activity-list'} .activity-item"
    activity_timestamp: str = f"{'.activity-item'} .timestamp"

    # Quick actions
    quick_action: str = ".quick-action"
    quick_action_button: str = f"{'.quick-action'} button"
