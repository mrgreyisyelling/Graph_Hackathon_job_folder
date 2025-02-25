import { Relation, Triple } from "@graphprotocol/grc-20";
import { deploySpace } from "./src/deploy-space";
import { publish } from "./src/publish";


async function main() {


    // This creates a new space
    // Every unique node we want to have its own space
    // Its written to establish a unique space for each node

    // So we need to create a variable tied to a unique node identity
    const nodeSpaceId = 'x'; // This needs a function to look up the next node reference for the space
    // how is this looked up - how do we avoid over creating spaces/nodes

    // So spaces need to be searched that are tied to the local area
    // geo location of the node
    // or the node id relations
    // search: this location. We define that as names of streets, addresses, coordinates, and landmarks


    // so part of defining the spaceID is to determine if the location has an existing space and is this an attempt to create a totally new one or add to an existing one
    
    
    const walletAddress = 'x'; // 0x...


    const spaceId = await deploySpace({
		spaceName: nodeSpaceId,
		initialEditorAddress: walletAddress,
	});

	console.log("Your spaceId is:", spaceId);

    const newTriple = Triple.make({
        attributeId: "...",
        entityId: "...",
        value: {
            type: "TEXT",
            value: "",
        },
    });

    const newRelation = Relation.make({
        fromId: "...",
        toId: "...",
        relationTypeId: "...",
    });

    const txHash = await publish({
        spaceId,
        author: "YOUR WALLET ACCOUNT ADDRESS",
        editName: "YOUR EDIT NAME",
        ops: [newTriple, newRelation], // An edit accepts an array of Ops
    });

    console.log("Your transaction hash is:", txHash);
}

main();
