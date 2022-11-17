import sqlite3 as sq


class DataBase:
    con = sq.Connection

    def open_connect(self):
        self.con = sq.connect('database/alco_bot_db.db')

    def close_connect(self):
        self.con.close()

    def create_table(self, name, fields='', fields_params='', foreign_keys='', foreign_table_keys='',
                     foreign_table_fields=''):
        count_fields = len(fields)
        cur = self.con.cursor()
        cur.execute(f'DROP TABLE IF EXISTS {name}')
        if count_fields == 1:
            cur.execute(f'CREATE TABLE IF NOT EXISTS {name} ({fields[0]} {fields_params[0]})')
        elif count_fields > 1:
            str_result = f'CREATE TABLE IF NOT EXISTS {name} ('
            for i in range(count_fields):
                if i == count_fields - 1:
                    str_result += f'{fields[i]} {fields_params[i]}'
                else:
                    str_result += f'{fields[i]} {fields_params[i]}, '
            if len(foreign_keys) == 1:
                str_result += f', FOREIGN KEY ({foreign_keys[0]}) REFERENCES {foreign_table_keys[0]}' \
                              f' ({foreign_table_fields[0]})'
            if len(foreign_keys) > 1:
                for j in range(len(foreign_keys)):
                    str_result += f', FOREIGN KEY ('
                    str_result += f'{foreign_keys[j]}) REFERENCES {foreign_table_keys[j]} ({foreign_table_fields[j]})'
            str_result += ')'
            cur.execute(str_result)

    def delete_table(self, name, f_id):
        cur = self.con.cursor()
        cur.execute(f'DELETE FROM {name} WHERE id = {f_id}')
        self.con.commit()

        # cur.execute(f'DROP TABLE IF EXISTS {name}')

    def select_table(self, name, is_where=0, is_all=0, fields='', table_keys='', fields_keys='', and_or=''):
        count_fields = len(fields)
        cur = self.con.cursor()
        if is_where == 0:
            if is_all == 1:
                cur.execute(f'SELECT * FROM {name}')
            elif is_all == 0:
                if count_fields == 1:
                    cur.execute(f'SELECT {fields[0]} FROM {name}')
                elif count_fields > 1:
                    str_result = 'SELECT '
                    for i in range(count_fields):
                        if i == count_fields - 1:
                            str_result += fields[i] + ' '
                        else:
                            str_result += fields[i] + ', '
                    str_result += f'FROM {name}'
                    cur.execute(str_result)
        elif is_where == 1:
            if is_all == 1:
                if len(table_keys) == 1:
                    cur.execute(f'SELECT * FROM {name} WHERE {table_keys[0]} = "{fields_keys[0]}"')
                elif len(table_keys) > 1 and and_or == '':
                    pass
                elif len(table_keys) > 1 and and_or == ' AND ':
                    str_result = f'SELECT * FROM {name} WHERE '
                    for i in range(len(table_keys)):
                        if i == len(table_keys) - 1:
                            str_result += f'{table_keys[i]} = {fields_keys[i]}'
                        else:
                            str_result += f'{table_keys[i]} = {str(fields_keys[i])} {and_or}'
                    cur.execute(str_result)
            elif is_all == 0:
                if len(table_keys) == 1:
                    if count_fields == 1:
                        cur.execute(f'SELECT {fields[0]} FROM {name} WHERE {table_keys[0]} = "{fields_keys[0]}"')
                    elif count_fields > 1:
                        str_result = 'SELECT '
                        for i in range(count_fields):
                            if i == count_fields - 1:
                                str_result += fields[i] + ' '
                            else:
                                str_result += fields[i] + ', '
                        str_result += f'FROM {name} WHERE {table_keys[0]} = {fields_keys[0]}'
                        cur.execute(str_result)
                elif len(table_keys) > 1:
                    if count_fields == 1:
                        str_result = f'SELECT {fields[0]} FROM {name} WHERE '
                        for i in range(len(table_keys)):
                            if i == len(table_keys) - 1:
                                str_result += f'{table_keys[i]} = {fields_keys[i]}'
                            else:
                                str_result += f'{table_keys[i]} = {fields_keys[i]} ' + and_or[i]
                        cur.execute(str_result)
                    elif count_fields > 1:
                        str_result = f'SELECT '
                        for i in range(count_fields):
                            if i == count_fields - 1:
                                str_result += fields[i] + ' '
                            else:
                                str_result += fields[i] + ', '
                        str_result += f'FROM {name} WHERE '
                        for j in range(len(table_keys)):
                            if j == len(table_keys) - 1:
                                str_result += f'{table_keys[j]} = {fields_keys[j]}'
                            else:
                                str_result += f'{table_keys[j]} = {fields_keys[j]} ' + and_or[j]
                        cur.execute(str_result)
        result = cur.fetchall()
        return result

    def insert_table(self, name, fields='', fields_values=''):
        count_fields = len(fields)
        cur = self.con.cursor()
        if count_fields == 1:
            cur.execute(f'INSERT INTO {name} ({fields[0]}) VALUES ("{fields_values[0]}")')
            self.con.commit()
        elif count_fields > 1:
            str_result = f'INSERT INTO {name} ('
            for i in range(count_fields):
                if i == count_fields - 1:
                    str_result += fields[i]
                else:
                    str_result += fields[i] + ', '
            str_result += ') VALUES ('
            for j in range(count_fields):
                if j == count_fields - 1:
                    str_result += '"' + fields_values[j] + '"'
                else:
                    str_result += '"' + fields_values[j] + '"' + ', '
            str_result += ')'
            cur.execute(str_result)
            self.con.commit()

    def update_table(self, name, fields='', fields_new_values='', table_keys='', fields_keys='', and_or=''):
        count_fields = len(fields)
        cur = self.con.cursor()
        if count_fields == 1:
            if len(table_keys) == 1:
                cur.execute(f'UPDATE {name} SET {fields[0]} = "{fields_new_values[0]}" WHERE {table_keys[0]}'
                            f' = {fields_keys[0]}')
                self.con.commit()
            elif len(table_keys) > 1:
                str_result = f'UPDATE {name} SET {fields[0]} = "{fields_new_values[0]}" WHERE '
                for j in range(len(table_keys)):
                    if j == len(table_keys) - 1:
                        str_result += f'{table_keys[j]} = {fields_keys[j]}'
                    else:
                        str_result += f'{table_keys[j]} = {fields_keys[j]} ' + and_or[j]
                        cur.execute(str_result)
                        self.con.commit()
            self.con.commit()
        elif count_fields > 1:
            str_result = f'UPDATE {name} SET '
            for i in range(count_fields):
                if i == count_fields - 1:
                    str_result += f'{fields[i]} = "{fields_new_values[i]}"'
                else:
                    str_result += f'{fields[i]} = "{fields_new_values[i]}", '
            if len(table_keys) == 1:
                str_result += f'WHERE {table_keys[0]} = {fields_keys[0]}'
                cur.execute(str_result)
                self.con.commit()
            elif len(table_keys) > 1:
                str_result += 'WHERE '
                for j in range(len(table_keys)):
                    if j == len(table_keys) - 1:
                        str_result += f'{table_keys[j]} = {fields_keys[j]}'
                    else:
                        str_result += f'{table_keys[j]} = {fields_keys[j]} ' + and_or[j]
                        cur.execute(str_result)
                        self.con.commit()
