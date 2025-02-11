### **Fully Wipe and Reinstall Neo4j**

If Neo4j is misconfigured and you want a **clean reinstall**, follow these steps carefully.

---

## **Step 1: Stop Neo4j**

First, stop the Neo4j service to ensure no processes are running:

```bash
sudo systemctl stop neo4j
```

Check if it's still running:

```bash
ps aux | grep neo4j
```

If you see any Neo4j processes, **force kill them**:

```bash
sudo kill -9 $(pgrep -f neo4j)
```

---

## **Step 2: Uninstall Neo4j**

### **If Installed via APT (Debian/Ubuntu)**

```bash
sudo apt remove --purge neo4j
sudo apt autoremove
```


## **Step 3: Remove All Neo4j Data and Configurations**

To ensure a **fresh installation**, delete all Neo4j-related files:

```bash
sudo rm -rf /var/lib/neo4j
sudo rm -rf /etc/neo4j
sudo rm -rf /var/log/neo4j
sudo rm -rf /usr/share/neo4j
sudo rm -rf /usr/bin/neo4j*
sudo rm -rf /usr/lib/neo4j
```

---

## **Step 4: Reinstall Neo4j**

### **Option 1: Install Neo4j via APT (Recommended for Ubuntu/Debian)**

1. Add the Neo4j repository:
    
    ```bash
    wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
    echo "deb https://debian.neo4j.com stable 5" | sudo tee /etc/apt/sources.list.d/neo4j.list
    ```
    
2. Update the package list and install Neo4j:
    
    ```bash
    sudo apt update
    sudo apt install neo4j
    ```
    

## **Step 5: Start Neo4j**

After installation, start Neo4j:

```bash
sudo systemctl enable neo4j
sudo systemctl start neo4j
```

Check the status:

```bash
sudo systemctl status neo4j
```


---

## **Step 6: Set a New Password**

After installation, open **Neo4j Browser** at:

```
http://localhost:7474
```

- **Login:**
    
    ```
    Username: neo4j
    Password: neo4j
    ```
    
- It will **prompt you to set a new password**.

---

### **Final Check**

Run:

```bash
neo4j status
```

If everything looks good, **you're set up!** 🚀

Let me know if you hit any issues!