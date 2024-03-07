import sqlite3

conn = sqlite3.connect("bd_shop.db")


def obtenir_produit_techno():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produit_techno")
    rows = cursor.fetchall()
    return rows


def obtenir_produit_techno_id(id):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM produit_techno WHERE id=?", (id,))
    rows = cursor.fetchone()
    if rows:
        return {"id": rows[0], "libellé_produit": rows[1], "catégorie": rows[2], "description": rows[3], "marque": rows[4], "prix": rows[5]}
    else:
        return None


def ajouter_produit_techno(libellé_produit, catégorie, description, marque, prix):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO produit_techno (libellé_produit, catégorie, description, marque, prix) VALUES (?, ?, ?, ?, ?)",
            (libellé_produit, catégorie, description, marque, prix),
        )
        conn.commit()
        return cursor.lastrowid
    except:
        return False


def modifier_produit_techno(id, libellé_produit, catégorie, description, marque, prix):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE produit_techno SET libellé_produit=?, catégorie=?, description=?, marque=?, prix=? WHERE id=?",
            (libellé_produit, catégorie, description, marque, prix, id),
        )
        conn.commit()
        return True
    except:
        return False
def supprimer_produit_techno(id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM produit_techno WHERE id=?", (id,))
        conn.commit()
        return True
    except:
        return False

    
