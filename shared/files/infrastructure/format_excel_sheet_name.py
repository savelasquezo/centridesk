from re import sub


def format_excel_sheet_name(sheet_name):
    sub_key = sub(r"[*?/:\[\]]", "", sheet_name)
    replaced_key = sub_key.replace('\\', '')

    return replaced_key[:31]
