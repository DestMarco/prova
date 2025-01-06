from configparser import ConfigParser
import json
from flask import Flask, request, jsonify
import psycopg2
from datetime import datetime

app = Flask(__name__)

def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    if parser.has_section(section):
        return {param[0]: param[1] for param in parser.items(section)}
    raise Exception(f"Section {section} not found in the {filename} file")

def connesione_db():
    # Connessione al database
    return psycopg2.connect(
        host="localhost",
        database="societa_immobiliare",
        user="boh",
        password="boh"
    )

@app.route('/cerca_casa_vendita', methods=['POST'])
def cerca_casa_vendita():
    params = request.json 
    indirizzo = params.get('indirizzo')
    prezzo_max = params.get('prezzo_max')
    
    # Connessione al DB
    con = connesione_db()
    cur = con.cursor()
    
    # Esecuzione della query
    cur.execute("""
        SELECT * FROM case_in_vendita 
        WHERE indirizzo LIKE %s AND prezzo <= %s AND stato = 'LIBERO'
    """, (f"%{indirizzo}%", prezzo_max))
    
    case = cur.fetchall()  
    cur.close()
    con.close()
    
    # Restituisci le case trovate come JSON
    return jsonify(case)

@app.route('/vendi_casa', methods=['POST'])
def vendi_casa():
    params = request.json
    catastale = params['catastale']
    filiale_venditrice = params['filiale_venditrice']
    prezzo_vendita = params['prezzo_vendita']
    
    con = connesione_db()
    cur = con.cursor()
    
    # Esegui la query per inserire la vendita
    cur.execute("""
        INSERT INTO vendite_casa (catastale, data_vendita, filiale_proponente, filiale_venditrice, prezzo_vendita)
        VALUES (%s, %s, (SELECT filiale_proponente FROM case_in_vendita WHERE catastale = %s), %s, %s)
    """, (catastale, datetime.now(), catastale, filiale_venditrice, prezzo_vendita))
    
    con.commit()
    cur.close()
    con.close()
    
    # Restituisci una risposta di successo
    return jsonify({"status": "success", "message": "Vendita registrata"})

@app.route('/report_marketing', methods=['POST'])
def report_marketing():
    params = request.json
    data_inizio = params['data_inizio']
    data_fine = params['data_fine']
    
    con = connesione_db()
    cur = con.cursor()
    
    # Esegui la query per il report
    cur.execute("""
        SELECT 
            f.nome AS filiale, 
            TO_CHAR(vc.data_vendita, 'YYYY-MM') AS mese, 
            COUNT(vc.catastale) AS numero_vendite,
            COUNT(ac.catastale) AS numero_affitti
        FROM 
            filiali f
        LEFT JOIN vendite_casa vc ON vc.filiale_proponente = f.partita_iva AND vc.data_vendita BETWEEN %s AND %s
        LEFT JOIN affitti_casa ac ON ac.filiale_proponente = f.partita_iva AND ac.data_affitto BETWEEN %s AND %s
        GROUP BY f.nome, mese
        ORDER BY f.nome, mese;
    """, (data_inizio, data_fine, data_inizio, data_fine))
    
    report = cur.fetchall()
    cur.close()
    con.close()
    
    # Formatta i risultati in una lista di dizionari
    result = [
        {"filiale": row[0], "mese": row[1], "numero_vendite": row[2], "numero_affitti": row[3]}
        for row in report
    ]
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
