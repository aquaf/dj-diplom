from django import template

register = template.Library()

@register.filter
def word_count(text, word_count):
    words = text.split()
    words_len = len(text.split())
    if words_len > word_count:
        return ' '.join(words[:word_count])