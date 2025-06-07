import psycopg2
from typing import List, Dict, Any
import os

class DatabaseManager:
    _instance = None
    _initialized = False

    def __new__(cls, db_url: str = None):
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, db_url: str = None):
        """Initialise le gestionnaire de base de données une seule fois"""
        if not self._initialized:
            self.db_url = db_url or os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/med_sys")
            self.conn = None
            print(f"🔧 Initialisation de DatabaseManager avec l'URL: {self.db_url}")
            self._connect()
            self._initialized = True

    def _connect(self):
        """Établit la connexion à la base de données"""
        print("🔄 Tentative de connexion à la base de données...")
        try:
            self.conn = psycopg2.connect(self.db_url)
            print("✅ Connexion à la base de données PostgreSQL réussie!")
        except Exception as e:
            print(f"❌ Erreur de connexion à la base de données: {e}")
            self.conn = None

    def get_doctors_by_specialty(self, specialty: str, limit: int = 5) -> List[Dict[str, Any]]:
        doctors = []

        # Format the specialty to match the enum format
        def format_specialty(s: str) -> str:
            # Convertir en minuscules et enlever les accents
            return s.lower().strip()

        formatted_specialty = format_specialty(specialty)
        print(f"🔍 Recherche des médecins pour la spécialité: {formatted_specialty}")
        
        if not self.conn:
            print("❌ Pas de connexion à la base de données")
            return []
        
        try:
            with self.conn.cursor() as cur:
                query = """
                SELECT
                    d.id,
                    d.first_name,
                    d.last_name,
                    d.specialty,
                    u.email,
                    u.phone,
                    u.address,
                    COUNT(c.id) AS consultation_count
                FROM
                    doctors AS d
                LEFT JOIN
                    consultations AS c ON d.id = c.doctor_id
                LEFT JOIN
                    users AS u ON d.user_id = u.id
                WHERE
                    d.specialty = %s::doctors_specialty_enum
                GROUP BY
                    d.id, d.first_name, d.last_name, d.specialty, u.email, u.phone, u.address
                ORDER BY
                    consultation_count DESC
                LIMIT %s;
                """
                cur.execute(query, (formatted_specialty, limit))
                results = cur.fetchall()

                for row in results:
                    doctors.append({
                        "id": row[0],
                        "first_name": row[1],
                        "last_name": row[2],
                        "specialty": row[3],
                        "email": row[4],
                        "phone": row[5],
                        "address": row[6],
                        "consultation_count": row[7]
                    })
        except Exception as e:
            print(f"❌ Erreur lors de la récupération des médecins: {e}")
            return []

        return doctors

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
            print("👋 Connexion à la base de données fermée")

if __name__ == "__main__":
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/med_sys")
    
    with DatabaseManager(DATABASE_URL) as db_manager:
        cardiologues = db_manager.get_doctors_by_specialty("cardiologue")
        print("\nCardiologues trouvés (triés par consultations):")
        if cardiologues:
            for doc in cardiologues:
                print(doc)
        else:
            print("Aucun cardiologue trouvé.")
            
        pediatres = db_manager.get_doctors_by_specialty("pediatre")
        print("\nPédiatres trouvés (triés par consultations):")
        if pediatres:
            for doc in pediatres:
                print(doc)
        else:
            print("Aucun pédiatre trouvé.") 