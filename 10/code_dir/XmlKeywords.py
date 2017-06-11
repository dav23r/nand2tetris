
def xmlKeywordsConvert(value):
    if value == '<': value = '&lt;'
    if value == '>': value = '&gt;'
    if value == '&': value = '&amp;'
    return value


