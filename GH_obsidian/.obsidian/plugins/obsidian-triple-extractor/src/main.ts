import { App, Plugin, TFile, Notice } from "obsidian";
import { parseTriples } from "./parser";
import { mergeKnowledgeGraphs } from "./merge";
import { KnowledgeGraphStore } from "./store";
import { Triple } from "./types";

export default class KnowledgeGraphPlugin extends Plugin {
    store!: KnowledgeGraphStore;  // ✅ Declare the property

    constructor(app: App, manifest: any) {
        super(app, manifest);
        this.store = new KnowledgeGraphStore();  // ✅ Initialize in constructor
    }

    async onload() {
        console.log("🟢 Loading Knowledge Graph Plugin");

        // ✅ Register merge command
        this.addCommand({
            id: "merge-knowledge-graph",
            name: "Merge External Knowledge Graph",
            callback: async () => {
                const primaryPath = "triples.json"; // Local KG
                const secondaryPath = "merged_triples.json"; // External KG
                const outputPath = "triples.json"; // Save merged KG

                await mergeKnowledgeGraphs(this.app, primaryPath, secondaryPath, outputPath);
                new Notice("✅ Knowledge Graph merged successfully.");
            },
        });

        // ✅ Register event for processing file modifications
        this.registerEvent(
            this.app.vault.on("modify", async (file) => {
                if (file instanceof TFile && file.extension === "md") {
                    console.log(`📄 File modified: ${file.path}`);
                    await this.processFile(file);
                }
            })
        );
    }

    async processFile(file: TFile) {
        console.log(`🟢 Processing file: ${file.path}`);

        if (file.extension !== "md") {
            console.log("❌ Skipping non-Markdown file.");
            return;
        }

        const content = await this.app.vault.read(file);
        console.log(`📄 File Content:\n${content}`);

        let triples = parseTriples(content);
        console.log("🔍 Extracted Triples:", triples);

        if (triples.length === 0) {
            console.warn(`⚠️ No triples found in ${file.path}.`);
            return;
        }

        // ✅ Ensure `version` is always set (default: "live_version")
        const triplesWithVersion: Triple[] = triples.map(triple => ({
            ...triple,
            version: triple.version ?? "live_version",  // If undefined, set default
        }));

        await this.saveTriples(triplesWithVersion);

        const masterData: Record<string, string> = {};
        const liveData: Record<string, string> = {};

        triplesWithVersion.forEach((triple) => {
            if (triple.version === "master_version") {
                masterData[triple.attribute] = triple.value;
            } else {
                liveData[triple.attribute] = triple.value;  // Default to "live_version"
            }
        });

        // ✅ Ensure YAML structure is valid
        const masterBlock = Object.keys(masterData).length
            ? `master_version:\n${Object.entries(masterData).map(([attr, val]) => `  ${attr}: "${val}"`).join("\n")}\n`
            : "";
        
        const liveBlock = Object.keys(liveData).length
            ? `live_version:\n${Object.entries(liveData).map(([attr, val]) => `  ${attr}: "${val}"`).join("\n")}\n`
            : "";

        const updatedYaml = `---
entity: "${triples[0].entity}"
${masterBlock}${liveBlock}---
`;

        console.log(`📝 Updated YAML:\n${updatedYaml}`);

        await this.app.vault.modify(file, updatedYaml);
        console.log(`✅ YAML updated in ${file.path}`);
    }


    async saveTriples(triples: Triple[]) {
        const triplesPath = "triples.json";
        const file = this.app.vault.getAbstractFileByPath(triplesPath);

        let existingTriples: Triple[] = [];
        if (file instanceof TFile) {
            try {
                const data = await this.app.vault.read(file);
                existingTriples = JSON.parse(data);
            } catch (error) {
                console.warn("⚠️ Could not read existing triples, creating a new file.");
            }
        }

        // Merge new triples into existing ones
        const mergedTriples = [...existingTriples, ...triples];

        if (file instanceof TFile) {
            await this.app.vault.modify(file, JSON.stringify(mergedTriples, null, 2));
        } else {
            await this.app.vault.create(triplesPath, JSON.stringify(mergedTriples, null, 2));
        }

        console.log("✅ Triples saved.");
    }

    onunload() {
        console.log("🛑 Unloading Knowledge Graph Plugin");
    }
}
