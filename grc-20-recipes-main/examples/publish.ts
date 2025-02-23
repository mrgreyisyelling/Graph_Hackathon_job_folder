import {wallet} from "../src/wallet";

async function publishData(spaceId: string, cid: string) {
	const result = await fetch(`https://api-testnet.grc-20.thegraph.com/space/${spaceId}/edit/calldata`, {
		method: "POST",
		body: JSON.stringify({
			cid: cid,
			// Optionally specify TESTNET or MAINNET. Defaults to MAINNET
			network: "TESTNET",
		}),
	});

	const {to, data} = await result.json();

	const txResult = await wallet.sendTransaction({
		to: to,
		value: 0n,
		data: data,
	});

	console.log("txResult", txResult);
}

publishData("AkxRvuV9ytxF1cKbS4VVTN", "ipfs://bafkreiabnc3kdcomwn2ismqqkkglj4sxme6a6mdzb2z6xf7ecaldjc7klm");
