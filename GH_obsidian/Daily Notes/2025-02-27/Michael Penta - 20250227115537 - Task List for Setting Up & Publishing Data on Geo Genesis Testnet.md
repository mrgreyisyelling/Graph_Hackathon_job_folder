[[Daily note/2025-02-27/2025-02-27-115537.canvas]]
[timelog](file:///home/mike/.var/app/org.gtimelog.GTimeLog/data/gtimelog/timelog.txt)
[Tasklist](file:///home/mike/.var/app/org.gtimelog.GTimeLog/data/gtimelog/tasklist.txt)


[[Michael Penta - 20250227115211 - To set up a wallet and start interacting with the Geo Genesis Testnet]]

### **Task List for Setting Up & Publishing Data on Geo Genesis Testnet**

#### **1. Install and Configure MetaMask (or Any Compatible Wallet)**

- Install MetaMask: [https://metamask.io/](https://metamask.io/)
- Add the **Geo Genesis Testnet** to your wallet:
    - Network Name: **Geogenesis Testnet**
    - RPC URL: **[https://rpc-geo-test-zc16z3tcvf.t.conduit.xyz/](https://rpc-geo-test-zc16z3tcvf.t.conduit.xyz/)**
    - Chain ID: **80451**
    - Currency Symbol: **ETH**

---

#### **2. Get Testnet ETH**

- Request testnet ETH from **Geo Genesis Discord** or **hackathon community**.
- Check if there’s a **Sepolia-Geo bridge** for conversion.

---

#### **3. Deploy a Personal Space**

- Run the following script to deploy a space:

```typescript
import { deploySpace } from "./src/deploy-space";

async function main() {
	const spaceId = await deploySpace({
		spaceName: "YOUR SPACE NAME",
		initialEditorAddress: "0xE412B72837A507427267867c3259e8dF419da59F",
	});

	console.log("Your spaceId is:", spaceId);
}

main();
```

- **Save the `spaceId`**, as you will need it for publishing data.

---

#### **4. Publish Entities to Your Space**

- Modify & run the script to **add data**:

```typescript
import { Relation, Triple } from "@graphprotocol/grc-20";
import { publish } from "./src/publish";

async function main() {
	const spaceId = "YOUR_SPACE_ID";
	const walletAddress = "YOUR WALLET ACCOUNT ADDRESS"; 

	const newTriple = Triple.make({
		attributeId: "ATTRIBUTE_ID",
		entityId: "ENTITY_ID",
		value: {
			type: "TEXT",
			value: "Example Data",
		},
	});

	const newRelation = Relation.make({
		fromId: "ENTITY_ID_1",
		toId: "ENTITY_ID_2",
		relationTypeId: "RELATION_TYPE_ID",
	});

	const txHash = await publish({
		spaceId,
		author: walletAddress,
		editName: "Initial Data Upload",
		ops: [newTriple, newRelation], 
	});

	console.log("Your transaction hash is:", txHash);
}

main();
```

- Replace placeholders (`YOUR_SPACE_ID`, `ATTRIBUTE_ID`, etc.) with real values.

---

#### **5. Verify Published Data**

- Go to the **GeoGenesis Testnet Explorer**:  
    📌 [https://explorer-geo-test-zc16z3tcvf.t.conduit.xyz/](https://explorer-geo-test-zc16z3tcvf.t.conduit.xyz/)
- Search for your **transaction hash** or `spaceId` to confirm changes.

---

#### **6. Reference GRC-20 Repos for More Examples**

- Check these repos for additional code references:
    - [https://github.com/geobrowser/hackathon-template](https://github.com/geobrowser/hackathon-template)
    - [https://github.com/graphprotocol/grc-20-ts](https://github.com/graphprotocol/grc-20-ts)
    - [https://github.com/geobrowser/grc-20-recipes](https://github.com/geobrowser/grc-20-recipes)

---

#### **7. Next Steps**

- Ensure your wallet has **testnet ETH** before publishing.
- Organize entities based on your **schema definitions**.
- Troubleshoot in **Geo Genesis Discord** if any issues arise.

---

This list keeps it clear and actionable. Do you need me to generate any scripts or automate parts of this for you? 🚀