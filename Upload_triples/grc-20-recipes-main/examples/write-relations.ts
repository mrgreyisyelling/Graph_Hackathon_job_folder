import {CONTENT_IDS, ID, IPFS, Relation, SYSTEM_IDS, Triple} from "@graphprotocol/grc-20";
import {wallet} from "../src/wallet";

async function publish() {
	const newEntityId = ID.generate();
	const rolesPropertyId = CONTENT_IDS.ROLES_ATTRIBUTE;

	const relationOp = Relation.make({
		fromId: "7ZeobHhZ67ZK6Cs3AVnrHt",
		toId: "KaaQs3TTB83xEXkvYTQK5n", // Software engineer
		relationTypeId: rolesPropertyId,
	});

	const hash = await IPFS.publishEdit({
		name: "Give entity name of role",
		author: wallet.account.address,
		ops: [relationOp],
	});

	console.log("hash", hash);
}

publish(); // Byron - Roles -> Software Engineer
