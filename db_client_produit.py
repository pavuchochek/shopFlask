import sqlite3

conn = sqlite3.connect("bd_shop.db", check_same_thread=False)


def obtenir_produit_alimentaire():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produit_alimentaire")
    produits=[]
    for row in cursor:
        produits.append({"id": row[0], "libellé_produit": row[1], "catégorie": row[2], "prix": row[3]})
    return produits


def obtenir_produit_alimentaire_id(id):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM produit_alimentaire WHERE id=?", (id,))
    rows = cursor.fetchone()
    if rows :
        return {"id": rows[0], "libellé_produit": rows[1], "catégorie": rows[2], "prix": rows[3]}
    else:
        return None


def ajouter_produit_alimentaire(libellé_produit, catégorie, prix):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO produit_alimentaire (libellé_produit, catégorie, prix) VALUES (?, ?, ?)",
            (libellé_produit, catégorie, prix),
        )
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(e)
        return False


def modifier_produit_alimentaire(id, libellé_produit, catégorie, prix):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE produit_alimentaire SET libellé_produit=?, catégorie=?, prix=? WHERE id=?",
            (libellé_produit, catégorie, prix, id),
        )
        conn.commit()
        return True
    except:
        return False


def supprimer_produit_alimentaire(id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produit_alimentaire WHERE id=?", (id,))
        conn.commit()
        return True
    except:
        return False
