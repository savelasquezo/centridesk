from os import remove

from pandas import ExcelWriter

from shared.files.infrastructure.format_excel_sheet_name import format_excel_sheet_name

HEADERS = {
    "en": {'id': 'User ID', 'agent_id': 'Agent ID', 'name': 'Name', 'email': 'Email', 'phone': 'Phone',
           'external_id': 'External ID', 'company': 'Company', 'last_comment_at': 'Last Comment Date',
           'created_at': 'Creation Date', 'updated_at': 'Update Date', 'active': 'Active', 'delegation': 'Delegation',
           'gdpr': 'GDPR', 'gdpr_updated_at': 'GDPR Update Date'},
    "es": {'id': 'Usuario ID', 'agent_id': 'Agente ID', 'name': 'Nombre', 'email': 'Email', 'phone': 'Teléfono',
           'external_id': 'External ID', 'company': 'Empresa', 'last_comment_at': 'Fecha Último Comentario',
           'created_at': 'Fecha Creación', 'updated_at': 'Fecha Actualización', 'active': 'Activo',
           'delegation': 'Delegación', 'gdpr': 'GDPR', 'gdpr_updated_at': 'Fecha Modificación GDPR'},
    "pt": {'id': 'Usuário ID', 'agent_id': 'Agent ID', 'name': 'Nome', 'email': 'Email', 'phone': 'Telefone',
           'external_id': 'ID externo', 'company': 'O negócio', 'last_comment_at': 'Data do último comentário',
           'created_at': 'Data de criação', 'updated_at': 'Modificação de data', 'active': 'Ativo',
           'delegation': 'Delegação', 'gdpr': 'GDPR', 'gdpr_updated_at': 'Data de modificação do GDPR'}
}


class CreateExcelFile:

    def __init__(self, info=None, file_name=None, lang=None):
        self.info = info
        self.file_name = file_name
        self.lang = lang
        self.path = '/tmp'

    def create(self):
        writer = ExcelWriter(
            f"{self.path}/{self.file_name}",
            engine='xlsxwriter',
            datetime_format='yyyy-mm-dd hh:mm:ss'
        )

        columns_name = HEADERS.get(self.lang, HEADERS['en'])

        for key, df in self.info.items():
            sheet_name = format_excel_sheet_name(key)
            columns = (list(df.columns.values.tolist()))
            rename_items = {}
            for col in columns:
                rename_items[col] = columns_name.get(col, col)  # Usar get() para evitar KeyError
            df = df.rename(columns=rename_items)

            # set index of date
            if not df.empty:
                df.set_index(df.columns[0], inplace=True)

            df.to_excel(writer, sheet_name=sheet_name)

            writer.sheets[sheet_name].set_column(0, 0, 20)

            for i, col in enumerate(df.columns):
                column_len = df[col].astype(str).str.len().max() if not df[col].empty else 0
                column_len = min(max(column_len, len(str(col))) + 3, 50)
                writer.sheets[sheet_name].set_column(i + 1, i + 1, column_len)

        writer.close()

    def delete(self):
        remove(f'{self.path}/{self.file_name}')
