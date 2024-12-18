import re

def snake_case_to_name(name):
    name = name.lower()
    name = re.sub(r'_', ' ', name)
    name = name.title()
    return name

def name_to_snake_case(name):
    name = name.lower()
    name = re.sub(r' ', '_', name)
    return name
