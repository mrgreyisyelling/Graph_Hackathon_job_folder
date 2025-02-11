Your **Neo4j version** likely requires a **different password reset syntax**. Let's fix it.

---

### **1. Check Your Neo4j Version**

Run:

```cypher
CALL dbms.components();
```

- If your version is **Neo4j 4.x or later**, use `ALTER CURRENT USER` (but with `FROM` syntax).
- If your version is **3.x**, you need to use `CALL dbms.security.changePassword`.

---

### **2. Correct Password Change Command**

Try this instead:

```cypher
ALTER CURRENT USER SET PASSWORD FROM 'old-password' TO 'new-password';
```

**Replace** `'old-password'` with your **current password**, and `'new-password'` with the new one.

- If you **forgot** the old password, follow **Step 4** below.

---

### **3. If `ALTER CURRENT USER` Doesn't Work**

For **Neo4j 3.x**, use:

```cypher
CALL dbms.security.changePassword('new-password');
```

---

### **4. If You Forgot the Old Password**

If you **don’t remember the old password**, manually **reset it**:

#### **Step 1: Stop Neo4j**

```bash
neo4j stop
```

or

```bash
sudo systemctl stop neo4j
```

#### **Step 2: Delete the Password File**

```bash
sudo rm /var/lib/neo4j/data/dbms/auth
```

#### **Step 3: Restart Neo4j**

```bash
neo4j start
```

or

```bash
sudo systemctl start neo4j
```

#### **Step 4: Log in With Default Credentials**

Now, log in using:

```
Username: neo4j
Password: neo4j
```

You **will be forced to set a new password**.

---

### **Final Check**

Try logging in again using:

```
neo4j -username neo4j -password new-password
```

If you're still stuck, let me know what error you're getting! 🚀