import {getChecksumAddress} from "@graphprotocol/grc-20";

const result = await fetch("https://api-testnet.grc-20.thegraph.com/deploy", {
	method: "POST",
	body: JSON.stringify({
		initialEditorAddress: getChecksumAddress("0xD448EcE561a10075b4C1dC4056288ed3606C55eD"),
		spaceName: "Hackathon example",
	}),
});

const {spaceId} = await result.json();
console.log("SPACE ID", spaceId);
