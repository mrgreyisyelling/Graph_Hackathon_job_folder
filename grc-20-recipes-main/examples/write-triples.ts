import {ID, IPFS, Relation, SYSTEM_IDS, Triple} from "@graphprotocol/grc-20";
import {wallet} from "../src/wallet";

async function publish() {
	const newEntityId = ID.generate();
	const namePropertyId = SYSTEM_IDS.NAME_ATTRIBUTE;

	const tripleOp = Triple.make({
		attributeId: namePropertyId,
		entityId: newEntityId,
		value: {
			type: "TEXT",
			value: "Byron",
		},
	});

	const hash = await IPFS.publishEdit({
		name: "Create Byron Entity",
		author: wallet.account.address,
		ops: [tripleOp],
	});

	console.log("hash", hash);
}

publish();
