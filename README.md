 MarocGrain-OSINT : Pipeline Maritime & Modélisation de Congestion Portuaire

Pipeline automatisé d'ingestion de données OSINT maritimes (`bulk lineups`) dédié à l'analyse des flux agricoles et à la prédiction de la congestion portuaire au Maroc.

 Architecture du Système

Le projet repose sur une architecture modulaire et robuste :
1. **Moteur d'Extraction (`MaritimeEngine`)** : Interface d'extraction structurée (compatible LLM / OpenRouter avec mécanisme de simulation/mock sécurisé pour les tests locaux).
2. **Recherche Opérationnelle (Files d'Attente)** : Modélisation mathématique par la formule d'**Erlang-C** ($M/M/c$) pour évaluer le facteur d'utilisation des postes à quai et le risque de saturation.
3. **Persistance des Données** : Pipeline transactionnel connectant le moteur à une base de données **MongoDB** (gestion des index, intégrité et opérations d'upsert).


 Modélisation Mathématique (Erlang-C)
Le système évalue le facteur d'utilisation des postes à quai $\rho$ :
$$\rho = \frac{\lambda}{c \cdot \mu}$$
* $\lambda$ : Taux d'arrivée des navires.
* $\mu$ : Taux de service (déchargement).
* $c$ : Nombre de postes à quai disponibles.

 Installation & Démarrage Rapide

1. **Cloner le dépôt :**
   ```bash
   git clone [https://github.com/mahfoudrakhaoui/maroc-grain-osint.git](https://github.com/mahfoudrakhaoui/maroc-grain-osint.git)
   cd maroc-grain-osint
