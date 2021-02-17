from django import template

register = template.Library()

@register.simple_tag
def increment_value(val):
    return val + 1

@register.filter
def modulo(val, modulo_val):
    return val % modulo_val

@register.filter
def return_value_from_matrix(matrix, index):
    return matrix[index // 9][index % 9]

@register.simple_tag
def return_value(val):
    return val
