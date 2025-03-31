from collections.abc import Iterable


class MysqlQueryConstructor:

    def __init__(self, db=None, table=None):
        self.db = db
        self.table = table

    def select(self, opts: list, conditions=None, order=None, limit=None, page=None, logic_operator='and'):
        items = ', '.join(opts)
        conditions_string = self.__format_select_conditions(conditions, logic_operator)
        order_string = self.__format_order(order)
        limit_string = self.__format_limit(limit, page)

        return f"select {items} from `{self.db}`.`{self.table}` " \
               f"{conditions_string}" \
               f"{order_string}" \
               f"{limit_string};"

    def select_query(self, opts: list, query: list, order=None, limit=None, page=None):
        items = ', '.join(opts)
        query_string = self.__format_select_query(query)
        order_string = self.__format_order(order)
        limit_string = self.__format_limit(limit, page)

        return f"select {items} from `{self.db}`.`{self.table}` " \
               f"{query_string}" \
               f"{order_string}" \
               f"{limit_string};"

    def insert(self, opt: dict):
        items = ', '.join(opt.keys())
        values = ', '.join(["%s"] * len(opt.values()))
        return f"insert into `{self.db}`.`{self.table}` " \
               f"({items}) values ({values});"

    def update(self, values: dict, conditions=None):
        opts_string = self.__format_equals(values)
        conditions_string = self.__format_conditions(conditions)

        return f"update `{self.db}`.`{self.table}` " \
               f"set {opts_string} " \
               f"{conditions_string};"

    def delete(self, conditions: dict):
        conditions_string = self.__format_conditions(conditions)
        return f"delete from `{self.db}`.`{self.table}` " \
               f"{conditions_string};"

    @staticmethod
    def __format_conditions(conditions: dict):
        conditions_string = ""
        if conditions:
            cond = []
            for k, v in conditions.items():
                value = f"'{v['value']}'" if isinstance(v['value'], str) else v['value']
                cond.append(f"{k} {v['op']} {value}")

            conditions_string = f"where {' and '.join(cond)} "
        return conditions_string

    @staticmethod
    def __format_select_query(query: list):
        query_string = ''
        cond = []
        for q in query:
            if q['type'] == 'condition':
                value = f"'{q['value']}'" if isinstance(q['value'], str) else q['value']
                cond.append(f"{q['field']} {q['condition']} {value}")
            elif q['type'] == 'operator':
                cond.append(q['operator'])

            query_string = f"where {' '.join(cond)} "
        return query_string

    @staticmethod
    def __format_select_conditions(conditions: dict, logic_operator: str = 'and'):
        conditions_string = ""
        if conditions:
            cond = []
            for k, v in conditions.items():
                if v['value']:
                    op = v['op']
                    if isinstance(v['value'], str):
                        value = f"'{v['value']}'"

                    elif isinstance(v['value'], Iterable):
                        value = tuple(v['value'])
                        if len(value) == 1:
                            value = str(value).replace(',', '')

                    else:
                        value = v['value']
                else:
                    op = 'is' if v['op'] == '=' else v['op']
                    value = 'NULL'
                cond.append(f"{k} {op} {value}")

            conditions_string = f' {logic_operator} '.join(cond)
            conditions_string = f"where {conditions_string} "
        return conditions_string

    @staticmethod
    def __format_equals(values: dict):
        opts = [f"{key} = %s" for key in values.keys()]
        return ', '.join(opts)

    @staticmethod
    def __format_limit(limit: int, page: int):
        offset = None
        if limit and page:
            offset = limit * (page - 1) if page and limit else None
        return f"limit {offset}, {limit} " if limit and offset else f"limit {limit} " if limit else ""

    @staticmethod
    def __format_order(order: str):
        order_str = ', '.join(order) if order else ""
        return f"order by {order_str} " if order_str else ""
