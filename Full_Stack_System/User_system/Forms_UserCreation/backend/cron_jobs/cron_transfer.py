from neo4j import GraphDatabase
import sqlite3

# Connect to Neo4j
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASS = "password"

def transfer_users_to_neo4j():
    conn = sqlite3.connect("../database/users/users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, email, user_type FROM users")
    users = cursor.fetchall()
    conn.close()

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASS))
    with driver.session() as session:
        for user in users:
            session.run(
                "MERGE (u:User {id: $id, name: $name, email: $email, type: $user_type})",
                id=user[0], name=user[1], email=user[2], user_type=user[3]
            )

    driver.close()

if __name__ == "__main__":
    transfer_users_to_neo4j()
