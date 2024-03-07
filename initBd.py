import sqlite3
conn=sqlite3.connect('bd_shop.db')
conn.execute('''CREATE TABLE IF NOT EXISTS produit_techno
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                libellé_produit TEXT NOT NULL,
                catégorie TEXT NOT NULL,
                prix FLOAT NOT NULL);''')
print("Table produit_techno créée avec succès")
conn.execute('''CREATE TABLE IF NOT EXISTS produit_alimentaire
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                libellé_produit TEXT NOT NULL,
                catégorie TEXT NOT NULL,
                description TEXT NOT NULL,
                marque TEXT NOT NULL,
                prix FLOAT NOT NULL);''')
print("Table produit_alimentaire créée avec succès")
conn.commit()
conn.close()