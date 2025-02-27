// Create a User node
MERGE (u:User {id: $id, name: $name, email: $email, type: $user_type});

// Create relationships between users
MATCH (a:User {id: $user_a}), (b:User {id: $user_b})
MERGE (a)-[r:$relationship_type]->(b);
