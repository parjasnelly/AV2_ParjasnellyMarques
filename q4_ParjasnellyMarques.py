# Tabelas
USERS = lambda: ("USERS", ["id", "name", "country", "id_console"])
GAMES = lambda: ("GAMES", ["id_game", "title", "genre", "release_date", "id_console"])
VIDEOGAMES = lambda: ("VIDEOGAMES", ["id_console", "name", "id_company", "release_date"])
COMPANY = lambda: ("COMPANY", ["id_company", "name", "country"])

select = lambda attrs, table, where_cond: f"SELECT {attrs} FROM {table} WHERE {where_cond}" if where_cond != "" else f"SELECT {attrs} FROM {table}"
find_id = lambda t1, t2: [e for e in t1[1] if e in t2[1] and "id" in e][0]
inner_join_where = lambda where_cond: f" WHERE {where_cond}" if where_cond != "" else ""
gen_inner_join = lambda tabelas, attrs, where_cond: select(attrs, tabelas[0][0], "") + "".join([f" INNER JOIN {tabelas[ind][0]} ON {tabelas[ind-1][0]}.{find_id(tabelas[ind - 1], tabelas[ind])} = {tabelas[ind][0]}.{find_id(tabelas[ind - 1], tabelas[ind])}" for ind,x in enumerate(tabelas[:-1], 1)]) + inner_join_where(where_cond)


def main():
    # Exemplo de uso
    print(gen_inner_join([GAMES(), VIDEOGAMES(), COMPANY()], "*", ""))
    print(gen_inner_join([USERS(), GAMES(), VIDEOGAMES(), COMPANY()], "*", "USERS.id_console = 2"))
    print(select("title, genre", "games", "id_console = 2"))
    print(select("name, country", "company", "country = 'EUA'"))
    print(select("*", "company", ""))


# Verifica se o arquivo foi importado ou executado diretamente
check_import = lambda: main() if __name__ == '__main__' else None
check_import()
