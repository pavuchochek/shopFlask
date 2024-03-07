from flask import Flask, request
from flask_restx import Api, Resource, fields
import db_client_produit

app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="Api boutiques en ligne",
    description="L'api pour gerer le futur stock de stickers",
)

namespace_entity = api.namespace(
    "Produit alimentaire", description="Produits alim. operations"
)
produit_alim_model = api.model(
    "Produit alimentaire",
    {
        "id": fields.Integer(readOnly=True, description="The entity unique identifier"),
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
        "id": fields.Integer(readOnly=True, description="The entity unique identifier"),
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


@namespace_entity.route("/produit_alimentaire/<int:id>")
class ProduitAlimQueries(Resource):

    @namespace_entity.doc("Obtenir un produit alimentaire avec son id")
    @namespace_entity.marshal_with(produit_alim_model)
    @namespace_entity.response(404, "Produit non trouvée")
    @namespace_entity.response(200, "Produit trouvée")
    def get(self, id):
        entity = {"id": id, "libellé_produit": "Entité 1"}
        entity = db_client_produit.obtenir_entite_bd(id)
        return entity

    @namespace_entity.doc("Ajouter une nouvelle entité")
    @namespace_entity.expect(produit_alim_model)
    @namespace_entity.response(201, "Entité créée")
    @namespace_entity.response(400, "Mauvaise requête")
    def post(self, id):
        if "libellé_produit" not in api.payload or api.payload["libellé_produit"] == "":
            return "Libellé non trouvé ou vide", 400
        label = api.payload["libellé_produit"]
        success = db_client_produit.ajouter_entite_bd(id, label)
        if success:
            print(f"Entite {id} {label} ajoutée")
            return id, 201
        else:
            print(f"L'entité {id} {label} n'a pas pu être ajoutée")
            return id, 401

    @namespace_entity.doc("Supprimer une entité")
    @namespace_entity.response(204, "Entité supprimée")
    def delete(self, id):
        success = db_client_produit.supprimer_entite_bd(id)
        if success:
            return (f"Entite {id} supprimée"), 204
        else:
            return (f"L'entité {id} n'a pas pu être supprimée"), 401

    @namespace_entity.expect(entity_model)
    @namespace_entity.doc("Mettre à jour une entité")
    @namespace_entity.response(204, "Entité mise à jour")
    @namespace_entity.response(400, "Mauvaise requête")
    def put(self, id):
        if "libellé_produit" not in api.payload or api.payload["libellé_produit"] == "":
            return "Libellé non trouvé ou vide", 400
        label = api.payload["libellé_produit"]
        success = db_client_produit.mettre_a_jour_entite_bd(id, label)
        if success:
            return (f"Entite {id} mise à jour"), 204
        else:
            return (f"L'entité {id} n'a pas pu être mise à jour"), 401


@namespace_entity.route("/produit_alimentaire/")
class EntityList(Resource):
    @namespace_entity.doc("Liste des entités")
    @namespace_entity.marshal_list_with(produit_alim_model)
    def get(self):
        entities = [
            {"id": 1, "libellé_produit": "Entité 1"},
            {"id": 2, "libellé_produit": "Entité 2"},
        ]
        entities = db_client_produit.obtenir_entites_bd()
        return entities


@namespace_entity.route("/produit_techno/<int:id>")
class ProduitsTechno(Resource):
    @namespace_entity.doc("Obtenir un produit techno avec son id")
    @namespace_entity.marshal_with(produit_techno_model)
    @namespace_entity.response(404, "Produit techno non trouvé")
    @namespace_entity.response(200, "Produit techno trouvé")
    def get(self, id):
        produit = {"id": id, "libellé_produit": "Produit 1"}
        produit = db_client_produit.obtenir_produit_bd(id)
        return produit

    @namespace_entity.doc("Ajouter un nouveau produit techno")
    @namespace_entity.expect(produit_techno_model)
    @namespace_entity.response(201, "Produit techno créé")
    @namespace_entity.response(400, "Mauvaise requête")
    def post(self, id):
        if "libellé_produit" not in api.payload or api.payload["libellé_produit"] == "":
            return "Libellé non trouvé ou vide", 400
        label = api.payload["libellé_produit"]
        success = db_client_produit.ajouter_produit_bd(id, label)
        if success:
            print(f"Produit {id} {label} ajouté")
            return id, 201
        else:
            print(f"Le produit {id} {label} n'a pas pu être ajouté")
            return id, 401

    @namespace_entity.doc("Supprimer un produit techno")
    @namespace_entity.response(204, "Produit techno supprimé")
    def delete(self, id):
        success = db_client_produit.supprimer_produit_bd(id)
        if success:
            return (f"Produit {id} supprimé"), 204
        else:
            return (f"Le produit {id} n'a pas pu être supprimé"), 401

    @namespace_entity.expect(produit_techno_model)
    @namespace_entity.doc("Mettre à jour un produit techno")
    @namespace_entity.response(204, "Produit techno mis à jour")
    @namespace_entity.response(400, "Mauvaise requête")
    def put(self, id):
        if "libellé_produit" not in api.payload or api.payload["libellé_produit"] == "":
            return "Libellé non trouvé ou vide", 400
        label = api.payload["libellé_produit"]
        success = db_client_produit.mettre_a_jour_produit_bd(id, label)
        if success:
            return (f"Produit {id} mis à jour"), 204
        else:
            return (f"Le produit {id} n'a pas pu être mis à jour"), 401


app.run(debug=True)
