from flask import Flask, request
from flask_restx import Api, Resource, fields
import db_client_produit
import db_client_produit_techno

app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="Api boutiques en ligne",
    description="L'api pour gerer le futur stock de stickers",
)

namespace_entity = api.namespace(
    "produits_alimentaires", description="Produits alim. operations"
)
produit_alim_model = api.model(
    "Produit alimentaire",
    {
        "libellé_produit": fields.String(
            required=True, description="Le nom du produit"
        ),
        "catégorie": fields.String(
            required=True, description="La catégorie du produit"
        ),
        "prix": fields.Float(required=True, description="Le prix du produit"),
    },
)
produit_techno_model = api.model(
    "Produit technologique",
    {
        "libellé_produit": fields.String(
            required=True, description="Le nom du produit"
        ),
        "catégorie": fields.String(
            required=True, description="La catégorie du produit"
        ),
        "description": fields.String(
            required=True, description="La description du produit"
        ),
        "marque": fields.String(required=True, description="La marque du produit"),
        "prix": fields.Float(required=True, description="Le prix du produit"),
    },
)


@namespace_entity.route("/<int:id>")
class ProduitAlimQueries(Resource):

    @namespace_entity.doc("Obtenir un produit alimentaire avec son id")
    @namespace_entity.marshal_with(produit_alim_model)
    @namespace_entity.response(404, "Produit non trouvée")
    @namespace_entity.response(200, "Produit trouvée")
    def get(self, id):
        entity = {"id": id, "libellé_produit": "Entité 1"}
        entity = db_client_produit.obtenir_produit_alimentaire_id(id)
        if entity is None:
            return (f"Entité {id} non trouvée"), 404
        return entity

    

    @namespace_entity.doc("Supprimer une entité")
    @namespace_entity.response(204, "Entité supprimée")
    def delete(self, id):
        success = db_client_produit.supprimer_produit_alimentaire(id)
        if success:
            return (f"Entite {id} supprimée"), 204
        else:
            return (f"L'entité {id} n'a pas pu être supprimée"), 401

    @namespace_entity.expect(produit_alim_model)
    @namespace_entity.doc("Mettre à jour une entité")
    @namespace_entity.response(204, "Entité mise à jour")
    @namespace_entity.response(400, "Mauvaise requête")
    def put(self, id):
        if "libellé_produit" not in api.payload or api.payload["libellé_produit"] == "":
            return "Libellé non trouvé ou vide", 400
        label = api.payload["libellé_produit"]
        categorie = api.payload["catégorie"]
        prix = api.payload["prix"]
        success = db_client_produit.modifier_produit_alimentaire(id,label,categorie, prix)
        if success:
            return (f"Entite {id} mise à jour"), 204
        else:
            return (f"L'entité {id} n'a pas pu être mise à jour"), 401


@namespace_entity.route("/")
class EntityList(Resource):
    @namespace_entity.doc("Liste des entités")
    @namespace_entity.marshal_list_with(produit_alim_model)
    def get(self):
        entities = [
            {"id": 1, "libellé_produit": "Entité 1"},
            {"id": 2, "libellé_produit": "Entité 2"},
        ]
        entities = db_client_produit.obtenir_produit_alimentaire()
        print(entities)
        return entities,200
    @namespace_entity.doc("Ajouter une nouvelle entité")
    @namespace_entity.expect(produit_alim_model)
    @namespace_entity.response(201, "Entité créée")
    @namespace_entity.response(400, "Mauvaise requête")
    def post(self):
        if "libellé_produit" not in api.payload or api.payload["libellé_produit"] == "":
            return "Libellé non trouvé ou vide", 400
        label = api.payload["libellé_produit"]
        categorie = api.payload["catégorie"]
        prix = api.payload["prix"]
        success = db_client_produit.ajouter_produit_alimentaire(label, categorie, prix)
        if success:
            print(f"Entite {success} {label} ajoutée")
            return 201
        else:
            print(f"L'entité {label} n'a pas pu être ajoutée")
            return 401


produit_techno = api.namespace(
    "produits_techno", description="Produits techno operations"
)


@produit_techno.route("/<int:id>")
class ProduitsTechno(Resource):
    @produit_techno.doc("Obtenir un produit techno avec son id")
    @produit_techno.marshal_with(produit_techno_model)
    @produit_techno.response(404, "Produit techno non trouvé")
    @produit_techno.response(200, "Produit techno trouvé")
    def get(self, id):
        produit = {"id": id, "libellé_produit": "Produit 1"}
        produit = db_client_produit_techno.obtenir_produit_techno_id(id)
        if produit is None:
            return (f"Produit {id} non trouvé"), 404
        return produit

    

    @produit_techno.doc("Supprimer un produit techno")
    @produit_techno.response(204, "Produit techno supprimé")
    def delete(self, id):
        success = db_client_produit.supprimer_produit_techno(id)
        if success:
            return (f"Produit {id} supprimé"), 204
        else:
            return (f"Le produit {id} n'a pas pu être supprimé"), 401

    @produit_techno.expect(produit_techno_model)
    @produit_techno.doc("Mettre à jour un produit techno")
    @produit_techno.response(204, "Produit techno mis à jour")
    @produit_techno.response(400, "Mauvaise requête")
    def put(self, id):
        if "libellé_produit" not in api.payload or api.payload["libellé_produit"] == "":
            return "Libellé non trouvé ou vide", 400
        label = api.payload["libellé_produit"]
        categorie = api.payload["catégorie"]
        description = api.payload["description"]
        marque = api.payload["marque"]
        prix = api.payload["prix"]
        success = db_client_produit.modifier_produit_techno(id, label, categorie, description, marque, prix)
        if success:
            return (f"Produit {id} mis à jour"), 204
        else:
            return (f"Le produit {id} n'a pas pu être mis à jour"), 401
@produit_techno.route("/")
class ProduitsTechnoAll(Resource):
    @produit_techno.doc("Tout les produits techno")
    @produit_techno.marshal_list_with(produit_techno_model)
    def get(self):
        produits = db_client_produit_techno.obtenir_produit_techno()
        print(produits)
        return produits
    
    @produit_techno.doc("Ajouter un nouveau produit techno")
    @produit_techno.expect(produit_techno_model)
    @produit_techno.response(201, "Produit techno créé")
    @produit_techno.response(400, "Mauvaise requête")
    def post(self):
        if "libellé_produit" not in api.payload or api.payload["libellé_produit"] == "":
            return "Libellé non trouvé ou vide", 400
        label = api.payload["libellé_produit"]
        categorie = api.payload["catégorie"]
        description = api.payload["description"]
        marque = api.payload["marque"]
        prix = api.payload["prix"]
        success = db_client_produit_techno.ajouter_produit_techno(label, categorie, description, marque, prix)
        if success:
            print(f"Produit  {label} ajouté")
            return 201
        else:
            print(f"Le produit {label} n'a pas pu être ajouté")
            return 401

app.run(debug=True)
