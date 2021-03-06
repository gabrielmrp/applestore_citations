# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 16:40:23 2021

@author: Gabriel Mascarenhas

Objetivo: Substituir a tarefa do profissional de coleta de dados atualizados 
sobre aplicativos de música e livros
"""
import pandas as pd
from sqlalchemy import create_engine
import sqlite3
import twitter_api
from prettytable import PrettyTable
import generate_credentials


""" Leitura dos dados e identificação das colunas """ 
df = pd.read_csv('AppleStore.csv')


dictionary_of_columns =  {
        "id" : "Identificação do App",
        "track_name" : "Nome",
        "size_bytes" : "Tamanho em Bytes",
        "currency" : "Moeda",
        "price" : "Valor na Apple Store",
        "rating_count_tot" : "Qtde de Avaliações",
        "rating_count_ver" : "Qtde de Avaliações última versão",
        "user_rating" : "Avaliação Média",
        "user_rating_ver" : "Avaliação Média da última versão",
        "ver" : "Última Versão",
        "cont_rating" : "Classificação Indicativa",
        "prime_genre" : "Gênero do App"
    }

"""1. Identifique a Aplicação da categoria News, que tiver a
maior quantidade de avaliações rating_count_tot."""

df_news = df[df['prime_genre']=='News']

rating_news_top_index = df_news['rating_count_tot'].sort_values(ascending=False).head(1).index

rating_news_top_appname = df_news.loc[rating_news_top_index,'track_name'].to_list()[0]
 

"""2. Identificar quais são as 10 Aplicações do gênero Music
e Book que possuem a maior quantidade de
avaliações no arquivo csv apple_store."""

df_music_or_book = df[(df['prime_genre']=='Music')|(df['prime_genre']=='Book')]

rating_music_or_book_top_index =  df_music_or_book['rating_count_tot'].sort_values(ascending=False).head(10).index

rating_music_or_book_top_appnames =  df_music_or_book.loc[rating_music_or_book_top_index.to_list(),'track_name'].to_list()

"""3. Após encontrar a aplicação do tipo News utilize a sua
API , para identificar quais das 10 aplicações do tipo
Music e Book, possuem o maior número de citações
nessa API.
"""

df_top_10_music_or_book = df.loc[rating_music_or_book_top_index,:]

"""
Chama a API do Twitter para capturar o número de citações (menções à pagina) das aplicações
Para gerar novas credenciais altere o arquivo generate_credentials.py e descomente o trecho abaixo
"""

#generate_credentials.generate()

citations = twitter_api.get_citations(df_top_10_music_or_book.track_name.tolist())

df_top_10_music_or_book['n_citacoes'] = df_top_10_music_or_book.track_name.map(citations)


"""O output esperado é a criação de um CSV, um JSON e uma
base de dados local com as respectivas colunas: id,
track_name, n_citacoes, size_bytes, price, prime_genre. Os
dados relativos às Aplicações estão disponíveis no arquivo
abaixo. Arquivo de dados:"""


output = df.loc[rating_music_or_book_top_index,:][['id','track_name','size_bytes','price','prime_genre']]
output['n_citacoes']=df_top_10_music_or_book['n_citacoes']
 
output =  output[['id','track_name', 'n_citacoes','size_bytes','price','prime_genre']].reset_index(drop=True)

""" Criação do arquivo CSV """
output.to_csv(r'output.csv')


""" Criação do arquivo JSON """
output.to_json(r'output.json')


""" Criação da base de dados local sqlite """

engine = create_engine('sqlite:///output.db', echo=True)
sqlite_connection = engine.connect()

sqlite_table = "AppleStore"
 
output.to_sql(sqlite_table, sqlite_connection, if_exists='replace')
sqlite_connection.close()

"""Conferência da Base de dados interna"""
 
def check_database(sqlite_table,sqlite_database):
    con = sqlite3.connect(sqlite_database+".db")
    cur = con.cursor()
    
    ptable = PrettyTable()
    
    ptable.field_names = [i[1] for i in cur.execute('PRAGMA table_info('+sqlite_table+');')]
    
    for row in cur.execute('SELECT * FROM '+sqlite_table+';'):
        ptable.add_row(row)
    print(ptable)
    con.close()
    
""" Remover o comentário para checar a tabela dentro da base de dados """    
# check_databse(sqlite_table,"output")