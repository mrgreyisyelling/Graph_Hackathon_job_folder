import { App, TFile, normalizePath } from "obsidian";
import { Triple } from "./types";  // ✅ Import the Triple interface

export async function mergeKnowledgeGraphs(app: App, primaryPath: string, secondaryPath: string, outputPath: string) {
    const primaryFile = app.vault.getAbstractFileByPath(normalizePath(primaryPath));
    const secondaryFile = app.vault.getAbstractFileByPath(normalizePath(secondaryPath));

    if (!(primaryFile instanceof TFile) || !(secondaryFile instanceof TFile)) {
        console.error("Could not find knowledge graph files.");
        return;
    }

    const primaryData: Triple[] = JSON.parse(await app.vault.read(primaryFile));
    const secondaryData: Triple[] = JSON.parse(await app.vault.read(secondaryFile));

    let mergedData: Triple[] = [];

    primaryData.forEach((triple: Triple) => {
        const existingTriple = secondaryData.find((t: Triple) => t.entity === triple.entity && t.attribute === triple.attribute);

        if (!existingTriple) {
            mergedData.push(triple);
        } else if (existingTriple.value !== triple.value) {
            mergedData.push({ entity: triple.entity, attribute: triple.attribute, value: triple.value, version: "master_version" });
            mergedData.push({ entity: triple.entity, attribute: triple.attribute, value: existingTriple.value, version: "live_version" });
        } else {
            mergedData.push(triple);
        }
    });

    const outputFile = app.vault.getAbstractFileByPath(normalizePath(outputPath));
    if (outputFile instanceof TFile) {
        await app.vault.modify(outputFile, JSON.stringify(mergedData, null, 2));
    } else {
        await app.vault.create(normalizePath(outputPath), JSON.stringify(mergedData, null, 2));
    }

    console.log(`Merged knowledge graph saved to ${outputPath}`);
}
