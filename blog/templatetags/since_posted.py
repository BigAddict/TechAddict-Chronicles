from datetime import datetime, timezone

from django import template

register = template.Library()


@register.filter
def since_posted(date):
    """Calculate time since a record was posted (hr/day/month/year)."""
    msg = ""
    delta = datetime.now(timezone.utc) - date
    if delta.days == 0:
        hour_diff = round(delta.seconds / 3600)
        msg = f"{hour_diff} hours ago" if hour_diff != 0 else "new"
    elif delta.days < 30:
        msg = f"{delta.days} days ago"
    elif delta.days >= 30 and delta.days <= 365:
        msg = f"{delta.days // 30} month ago"
    else:
        msg = f"{delta.days // 12} year ago"

    return msg
