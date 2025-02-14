Where Does User Registration Data Go?
Once a user submits their registration form, the data follows this flow:

User submits the form → register.html
Data is sent to backend API → backend/api/submit_user.py
Backend processes & validates the request
User data is stored in the initial database → database/users/users.db
A cron job later transfers the data to Neo4j → backend/cron_jobs/cron_transfer.py
📂 Backend Flow
Step	File Handling It	Purpose
1️⃣ Receive Data	backend/api/submit_user.py	Takes in user registration data from the form
2️⃣ Validate & Store	backend/api/submit_user.py	Checks input, hashes password, inserts into SQLite (users.db)
3️⃣ Transfer to Neo4j	backend/cron_jobs/cron_transfer.py	Periodically moves user data to Neo4j
4️⃣ Graph Relationships	database/neo4j/schema.cypher	Defines how users relate in the knowledge graph
