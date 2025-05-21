from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)  # Autorise toutes les origines

# Paramètres de connexion à la même base PostgreSQL sur Render
DB_HOST     = "dpg-cvq353bipnbc73cil1og-a.frankfurt-postgres.render.com"
DB_NAME     = "pokefeuille_sql_base"
DB_USER     = "pokefeuille_sql_base_user"
DB_PASSWORD = "rm0IWPFUkWbFi8OQdU6d6LrHD7pKwDJx"

def connect_db():
    return psycopg2.connect(
        host     = DB_HOST,
        database = DB_NAME,
        user     = DB_USER,
        password = DB_PASSWORD,
        sslmode  = 'require'
    )

@app.route('/health', methods=['GET'])
def health():
    # Permet au keep-alive et au monitoring de vérifier que le service est up
    return "OK", 200

@app.route('/api/items_scelles', methods=['GET'])
def get_items_scelles():
    conn = connect_db()
    cur  = conn.cursor()

    # Sélectionnez ici tous les champs de votre table items_scelles
    cur.execute("""
        SELECT
          id_items,
          serie_en,
          extension_en,
          serie_fr,
          extension_fr,
          id_extension,
          categorie,
          item_nom_fr,
          item_nom_en,
          prix,
          image_url
        FROM items_scelles
        ORDER BY id_items;
    """)

    cols = [desc[0] for desc in cur.description]
    data = [dict(zip(cols, row)) for row in cur.fetchall()]

    cur.close()
    conn.close()
    return jsonify(data)

if __name__ == "__main__":
    # Écoute sur 0.0.0.0 et port configuré par Render ou 5001 pour différencier
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
