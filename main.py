import os
from datetime import datetime, timezone
from pymongo import UpdateOne
from dotenv import load_dotenv
from database import DatabaseManager
from engine import MaritimeEngine

load_dotenv()

def run_pipeline():
    print("=== Démarrage du Pipeline MarocGrain-OSINT ==️ ===")
    
    # 1. Connexion DB & Moteur
    db_manager = DatabaseManager()
    collection = db_manager.get_collection()
    engine = MaritimeEngine(os.getenv("OPENROUTER_API_KEY"))

    # 2. Simulation d'un bulletin portuaire brut (en production, issu du scraping asynchrone)
    raw_bulletin_sample = (
        "Vessel IRON SPIRIT, IMO 9876543, loaded 35000 MT of WHEAT at port of Rouen, "
        "bound for Casablanca MACAS, consignee To Order, ETA 2026-12-05"
    )

    print("[1/3] Analyse et extraction structurée via OpenRouter (Llama-3)...")
    parsed_record = engine.parse_raw_lineup_with_llm(raw_bulletin_sample)
    print(f" -> Enregistrement extrait : {parsed_record}")

    # 3. Validation et filtrage
    if not engine.is_valid_agri_flow(parsed_record):
        print(" -> Enregistrement rejeté par le filtre vectoriel (flux non agricole ou exclu).")
        return

    # 4. Calcul stochastique de congestion (M/M/c)
    # Simulation : arrivée de 0.8 navire/jour, cadence de déchargement de 0.35 navire/jour par quai, 2 postes à quai
    congestion = engine.erlang_c_waiting_time(lambda_arrival=0.8, mu_service=0.35, c_berths=2)
    print(f"[2/3] Métriques de congestion portuaire (Erlang-C) : {congestion}")

    # 5. Persistance NoSQL Idempotente sur MongoDB Atlas
    composite_key = {
        "imo": parsed_record["imo"],
        "origin_port": parsed_record["origin_port"],
        "eta_month": parsed_record["eta_iso"][:7],
    }
    
    payload = {
        **parsed_record,
        "predicted_demurrage": congestion,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }

    operation = UpdateOne(composite_key, {"$set": payload}, upsert=True)
    
    print("[3/3] Écriture transactionnelle sur MongoDB Atlas...")
    result = collection.bulk_write([operation])
    print(f" -> Succès ! Upserted: {result.upserted_count}, Modified: {result.modified_count}")
    print("=== Pipeline exécuté avec succès à 0 DH ===")

if __name__ == "__main__":
    run_pipeline()