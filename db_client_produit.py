import sqlite3
conn=sqlite3.connect('bd_shop.db')

def obtenir_produit_alimentaire():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produit_alimentaire")
    rows = cursor.fetchall()
    return rows
