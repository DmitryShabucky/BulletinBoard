from django import template


register = template.Library()

@register.filter()
def status_false(post):
    count_status_false = post.replies.filter(status=False)
    return len(count_status_false)

@register.filter()
def post_new_reply_exists(post):
    new_reply_exists = post.replies.filter(status=False)
    return new_reply_exists