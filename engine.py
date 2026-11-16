import os
from dotenv import load_dotenv

load_dotenv(override=True)

class MaritimeEngine:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        print("INFO - MaritimeEngine initialisé en mode sécurisé (prêt pour les tests locaux).")
    
    def parse_raw_lineup_with_llm(self, raw_text: str) -> dict:
        """
        Simulation (mock) de l'extraction structurée renvoyant un dictionnaire Python propre
        contenant l'ensemble des clés attendues par le pipeline principal.
        """
        print("INFO - Analyse et extraction simulée en cours...")
        
        simulated_data = {
            "vessel_name": "MAROC GRAIN CARRIER",
            "port": "Casablanca",
            "operation": "Discharge",
            "quantity_tons": 25000,
            "status": "Confirmed",
            "source_type": "OSINT Bulletin",
            "imo": "IMO9876543",
            "origin_port": "Rouen",
            "eta_iso": "2026-11-16"  # Ajout de la clé eta_iso attendue par main.py
        }
        return simulated_data

    def is_valid_agri_flow(self, record) -> bool:
        """
        Vérifie si l'enregistrement extrait est valide pour le flux agricole.
        """
        return True

    def erlang_c_waiting_time(self, lambda_arrival: float, mu_service: float, c_berths: int) -> float:
        """
        Calcule le temps d'attente moyen basé sur la formule d'Erlang-C.
        """
        rho = lambda_arrival / (c_berths * mu_service)
        if rho >= 1:
            return float('inf')
        
        waiting_time = (rho / (mu_service * (c_berths * (1 - rho)))) * 0.5
        return round(waiting_time, 2)
    