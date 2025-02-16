import { Plugin, TFile } from "obsidian";
import { load } from "js-yaml"; // ✅ Use js-yaml instead
import { parseTriples } from "./parser";
import { KnowledgeGraphStore } from "./store";
import { TripleView } from "./view"; 

export default class KnowledgeGraphPlugin extends Plugin {
    private store: KnowledgeGraphStore = new KnowledgeGraphStore();

    async onload() {
        console.log("Loading Knowledge Graph Plugin");

        this.registerEvent(this.app.vault.on("rename", async (file) => {
            if (file instanceof TFile) {
                await this.processFile(file);
            }
        }));

        await this.loadKnowledgeGraph();
    }

    async processFile(file: TFile) {
        if (file.extension === "md") {
            const content = await this.app.vault.read(file);
            
            // ✅ Use js-yaml to parse YAML
            const yamlMatch = content.match(/^---\n([\s\S]+?)\n---/);
            if (!yamlMatch) return;

            const yamlData = load(yamlMatch[1]) as any;

            const triples = parseTriples(content);
            this.store.updateTriples(file.path, triples);
            console.log("Extracted Triples:", triples);
        }
    }

    async loadKnowledgeGraph() {
        const files = this.app.vault.getMarkdownFiles();
        for (const file of files) {
            await this.processFile(file);
        }
    }

    onunload() {
        console.log("Unloading Knowledge Graph Plugin");
    }
}