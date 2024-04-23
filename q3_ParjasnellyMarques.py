import mysql.connector


mydb = (lambda: mysql.connector.connect(
    host="localhost",
    user="root",
    password="6172"))()
crs = (lambda: mydb.cursor(dictionary=True))()


def exec_sql_cmd(cmd):
    print(f"Executando comando: {cmd}")
    crs.execute(cmd)
    return crs.fetchall()


# Gera string comandos sql
create_table = lambda table, attrs: f"CREATE TABLE IF NOT EXISTS {table} ({attrs});"
create_db = lambda db_name: f"CREATE DATABASE IF NOT EXISTS {db_name};"
drop_db = lambda db_name: f"DROP DATABASE {db_name};"
drop_table = lambda table: f"DROP TABLE {table} );"
use_db = lambda db_name: f"USE {db_name};"
select = lambda attrs, table, where_cond: f"SELECT {attrs} FROM {table} WHERE {where_cond};\n" if where_cond != "" else f"SELECT {attrs} FROM {table};"
insert = lambda attrs, table, values: f"INSERT INTO {table} ({attrs}) VALUES ({values});"
delete = lambda table, where_cond: f"DELETE FROM {table} WHERE {where_cond};\n" if where_cond != "" else f"DELETE FROM {table};"


# Iniciando e pupulando Banco de dados
dbname = lambda: "AV2_q3_Parjasnelly"

# Dicionário para as tabelas
tables = lambda: {
    "USERS": "id int, name varchar(255), country varchar(255), id_console int",
    "VIDEOGAMES": "id_console int, name varchar(255), id_company int, release_date date",
    "GAMES": "id_game int, title varchar(255), genre varchar(255), release_date date, id_console int",
    "COMPANY": "id_company int , name varchar(255), country varchar(255)",
}

# Dicionário para a tabela USERS
users_data = lambda: [
    {"id": 1, "name": "'João'", "country": "'Brasil'", "id_console": 1},
    {"id": 2, "name": "'Maria'", "country": "'EUA'", "id_console": 2},
    {"id": 3, "name": "'Pedro'", "country": "'Espanha'", "id_console": 1},
    {"id": 4, "name": "'Ana'", "country": "'Portugal'", "id_console": 3},
    {"id": 5, "name": "'Lucas'", "country": "'Brasil'", "id_console": 2}]

# Dicionário para a tabela VIDEOGAMES
consoles_data = lambda: [
    {"id_console": 1, "name": "'Playstation 4'", "id_company": 1, "release_date": "'2013-11-15'"},
    {"id_console": 2, "name": "'Nintendo Switch'", "id_company": 2, "release_date": "'2017-03-03'"},
    {"id_console": 3, "name": "'Xbox Series X'", "id_company": 3, "release_date": "'2020-11-10'"},
    {"id_console": 4, "name": "'Playstation 5'", "id_company": 1, "release_date": "'2020-11-12'"},
    {"id_console": 5, "name": "'Xbox One'", "id_company": 3, "release_date": "'2013-11-22'"}]

# Dicionário para a tabela GAMES
games_data = lambda: [
    {"id_game": 1, "title": "'God of War'", "genre": "'Ação'", "release_date": "'2018-04-20'", "id_console": 1},
    {"id_game": 2, "title": "'The Legend of Zelda: Breath of the Wild'", "genre": "'Aventura'",
     "release_date": "'2017-03-03'", "id_console": 2},
    {"id_game": 3, "title": "'FIFA 22'", "genre": "'Esporte'", "release_date": "'2021-10-01'", "id_console": 3},
    {"id_game": 4, "title": "'Assassins Creed Valhalla'", "genre": "'Ação/Aventura'", "release_date": "'2020-11-10'",
     "id_console": 1},
    {"id_game": 5, "title": "'Super Mario Odyssey'", "genre": "'Plataforma'", "release_date": "'2017-10-27'",
     "id_console": 2}]

# Dicionário para a tabela COMPANY
company_data = lambda: [
    {"id_company": 1, "name": "'Sony'", "country": "'Japão'"},
    {"id_company": 2, "name": "'Nintendo'", "country": "'Japão'"},
    {"id_company": 3, "name": "'Microsoft'", "country": "'EUA'"}]
# Cria database
exec_sql_cmd(drop_db(dbname()))

exec_sql_cmd(create_db(dbname()))

exec_sql_cmd(use_db(dbname()))

# Cria tabelas
generate_tables = lambda tables: [exec_sql_cmd(create_table(table, tables[table])) for table in tables]
generate_tables(tables())

# popula tabelas
populate_tables = lambda array, table: [
    exec_sql_cmd(insert(', '.join(map(str, dic.keys())), table, ', '.join(map(str, dic.values())))) for dic in array]

populate_tables(users_data(), "users")
populate_tables(consoles_data(), "videogames")
populate_tables(games_data(), "games")
populate_tables(company_data(), "company")
mydb.commit()


# exemplos de select
print("Resultado:", exec_sql_cmd(select("*", "users", "country = 'Brasil'")), "\n")
print("Resultado:",exec_sql_cmd(select("*", "videogames", "name = 'Playstation 4'")), "\n")
print("Resultado:",exec_sql_cmd(select("title, genre", "games", "id_console = 2")), "\n")
print("Resultado:",exec_sql_cmd(select("name, country", "company", "country = 'EUA'")), "\n")

# exemplos de delete

print("Resultado:", exec_sql_cmd(select("*", "users", "country = 'Espanha'")), "\n")
print("Resultado:", exec_sql_cmd(delete("users", "country = 'Espanha'")), "\n")

print("Resultado:", exec_sql_cmd(select("*", "users", "country = 'Países Baixos'")), "\n")

print("Resultado:", exec_sql_cmd(delete("videogames", "name = 'Xbox Series X'")), "\n")
print("Resultado:", exec_sql_cmd(delete("company", "country = 'Japão'")), "\n")

# fechando conexão
mydb.close()
