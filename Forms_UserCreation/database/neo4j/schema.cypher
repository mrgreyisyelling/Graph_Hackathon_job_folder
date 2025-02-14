// Create a User node
MERGE (u:User {id: $id, name: $name, email: $email, type: $user_type});
