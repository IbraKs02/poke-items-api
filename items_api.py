from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import os

app = Flask(__name__)
CORS(app)  # Autorise toutes les origines

# Paramètres de connexion à PostgreSQL sur Render
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
    return "OK", 200

@app.route('/api/items_scelles', methods=['GET'])
def get_items_scelles():
    conn = connect_db()
    cur  = conn.cursor()

    # INNER JOIN entre items_scelles et jcc_extensions sur id_extension
    cur.execute("""
        SELECT
          i.*,                        -- tous les champs de items_scelles
          j.identifiant_edition,
          j.nom_edition_en,
          j.nom_edition_fr,
          j.url_edition,
          j.identifiant_extension,
          j.nom_extension_en,
          j.nom_extension_fr,
          j.url_extension
        FROM items_scelles AS i
        INNER JOIN jcc_extensions AS j
          ON TRIM(i.id_extension) = TRIM(j.identifiant_extension)
        ORDER BY i.id_items;
    """)

    # Récupération des noms de colonnes (i.* puis j.*)
    cols = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    data = [dict(zip(cols, row)) for row in rows]

    cur.close()
    conn.close()
    return jsonify(data)

if __name__ == "__main__":
    # Écoute sur 0.0.0.0 et port défini (Render injecte PORT)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
