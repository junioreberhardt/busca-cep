import unicodedata


def normal_text(txt):
    if not txt:
        return ''
    nfkd = unicodedata.normalize('NFD', txt)
    just_ascii = nfkd.encode('ascii', 'ignore').decode('utf-8')
    return just_ascii.lower()


def format_cep(cep_string):
    cep_no_format = cep_string.replace('-', '').strip()

    if len(cep_no_format) == 8:
        return f'{cep_no_format[:-3]}-{cep_no_format[-3:]}'

    return cep_string
