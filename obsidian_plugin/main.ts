import { App, Plugin, TFile, Notice } from "obsidian";
import { parseTriples } from "./parser";
import { mergeKnowledgeGraphs } from "./merge";
import { KnowledgeGraphStore } from "./store";

export default class KnowledgeGraphPlugin extends Plugin {
    store!: KnowledgeGraphStore;  // ✅ Declare the property

    constructor(app: App, manifest: any) {
        super(app, manifest);
        this.store = new KnowledgeGraphStore();  // ✅ Initialize in constructor
    }

    async onload() {
        console.log("Loading Knowledge Graph Plugin");

        this.addCommand({
            id: "merge-knowledge-graph",
            name: "Merge External Knowledge Graph",
            callback: async () => {
                const primaryPath = "triples.json";
                const secondaryPath = "merged_triples.json";
                const outputPath = "triples.json";

                await mergeKnowledgeGraphs(this.app, primaryPath, secondaryPath, outputPath);
                new Notice("Knowledge Graph merged successfully.");
            },
        });

        this.registerEvent(
            this.app.vault.on("modify", async (file) => {
                if (file instanceof TFile && file.extension === "md") {
                    console.log(`File modified: ${file.path}`);
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
    
        const triples = parseTriples(content);
        console.log("🔍 Extracted Triples:", triples);
    
        if (triples.length === 0) {
            console.warn(`⚠️ No triples found in ${file.path}.`);
            return;
        }
    
        const masterData: Record<string, string> = {};
        const liveData: Record<string, string> = {};
    
        triples.forEach((triple) => {
            if (triple.version === "master_version") {
                masterData[triple.attribute] = triple.value;
            } else if (triple.version === "live_version") {
                liveData[triple.attribute] = triple.value;
            }
        });
    
        const updatedYaml = `---
entity: "${triples[0].entity}"
master_version:
${Object.entries(masterData).map(([attr, val]) => `  ${attr}: "${val}"`).join("\n")}
live_version:
${Object.entries(liveData).map(([attr, val]) => `  ${attr}: "${val}"`).join("\n")}
---
    `;
    
        console.log(`📝 Updated YAML:\n${updatedYaml}`);
    
        await this.app.vault.modify(file, updatedYaml);
        console.log(`✅ YAML updated in ${file.path}`);
    }
    
}
