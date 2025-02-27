from neo4j import GraphDatabase
import sqlite3
import os

# Connect to Neo4j
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "password"

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "../../database/users/users.db")

def transfer_relationships_to_neo4j():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT user_a, user_b, relationship_type FROM relationships")
    relationships = cursor.fetchall()
    conn.close()

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
    with driver.session() as session:
        for rel in relationships:
            session.run(
                "MATCH (a:User {id: $user_a}), (b:User {id: $user_b}) "
                "MERGE (a)-[r:"+rel[2]+"]->(b)",
                user_a=rel[0], user_b=rel[1]
            )

    driver.close()

if __name__ == "__main__":
    transfer_relationships_to_neo4j()
