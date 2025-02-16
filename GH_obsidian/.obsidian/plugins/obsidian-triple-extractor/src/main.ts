import { App, Plugin, TFile, Notice, normalizePath } from "obsidian";
import { parseTriples } from "./parser";
import { mergeKnowledgeGraphs } from "./merge";
import { KnowledgeGraphStore } from "./store";
import { Triple } from "./types"; // ✅ Import Triple

export default class KnowledgeGraphPlugin extends Plugin {
    store!: KnowledgeGraphStore;
    processingFiles: Set<string> = new Set(); // Prevent infinite loops

    constructor(app: App, manifest: any) {
        super(app, manifest);
        this.store = new KnowledgeGraphStore();
    }

    async onload() {
        console.log("✅ Loading Knowledge Graph Plugin");

        this.addCommand({
            id: "merge-knowledge-graph",
            name: "Merge External Knowledge Graph",
            callback: async () => {
                const primaryPath = "triples.json";
                const secondaryPath = "merged_triples.json";
                const outputPath = "triples.json";

                await mergeKnowledgeGraphs(this.app, primaryPath, secondaryPath, outputPath);
                new Notice("✅ Knowledge Graph merged successfully.");
            },
        });

        this.registerEvent(
            this.app.vault.on("modify", async (file) => {
                if (file instanceof TFile && file.extension === "md") {
                    await this.processFile(file);
                }
            })
        );
    }

    async processFile(file: TFile) {
        if (this.processingFiles.has(file.path)) {
            console.log(`⚠️ Skipping ${file.path}, already being processed.`);
            return;
        }
        this.processingFiles.add(file.path);

        console.log(`🟢 Processing file: ${file.path}`);
        const content = await this.app.vault.read(file);
        console.log(`📄 File Content:\n${content}`);

        let triples = parseTriples(content);
        console.log("🔍 Extracted Triples:", triples);

        if (triples.length === 0) {
            console.warn(`⚠️ No triples found in ${file.path}.`);
            this.processingFiles.delete(file.path);
            return;
        }

        // ✅ Ensure `version` is included in all triples
        const triplesWithVersion: Triple[] = triples.map(triple => ({
            ...triple,
            version: triple.version || "live_version",
        }));

        // ✅ Deduplicate triples while allowing changes to be tracked
        const uniqueTriples = Array.from(new Map(
            triplesWithVersion.map(triple => [`${triple.entity}-${triple.attribute}-${triple.value}-${triple.version}`, triple])
        ).values());

        await this.saveTriples(uniqueTriples);

        // ✅ Structure data into master/live versions
        const masterData: Record<string, string> = {};
        const liveData: Record<string, string> = {};

        uniqueTriples.forEach((triple) => {
            if (triple.version === "master_version") {
                masterData[triple.attribute] = triple.value;
            } else if (triple.version === "live_version") {
                liveData[triple.attribute] = triple.value;
            }
        });

        const updatedYaml = `---
entity: "${uniqueTriples[0].entity}"
master_version:
${Object.entries(masterData).map(([attr, val]) => `  ${attr}: "${val}"`).join("\n")}
live_version:
${Object.entries(liveData).map(([attr, val]) => `  ${attr}: "${val}"`).join("\n")}
---
`;

        console.log(`📝 Updated YAML:\n${updatedYaml}`);
        await this.app.vault.modify(file, updatedYaml);
        console.log(`✅ YAML updated in ${file.path}`);

        await this.createEntityNotes(uniqueTriples);

        this.processingFiles.delete(file.path);
    }

    async saveTriples(triples: Triple[]) {
        const triplesFilePath = "triples.json";
        const normalizedPath = normalizePath(triplesFilePath);
        let existingTriples: Triple[] = [];
    
        const file = this.app.vault.getAbstractFileByPath(normalizedPath);
        
        if (file instanceof TFile) {
            try {
                const content = await this.app.vault.read(file);
                existingTriples = JSON.parse(content);
                console.log("📂 Loaded existing triples:", existingTriples);
            } catch (error) {
                console.warn(`⚠️ Error reading existing triples: ${error}`);
            }
        } else {
            console.log("⚠️ `triples.json` does not exist, creating new.");
        }
    
        // ✅ Merge new triples, ensuring no duplicates
        const allTriples = [...existingTriples, ...triples];
    
        // ✅ Deduplicate triples by entity, attribute, value, and version
        const uniqueTriples = Array.from(new Map(
            allTriples.map(t => [`${t.entity}-${t.attribute}-${t.value}-${t.version}`, t])
        ).values());
    
        try {
            if (file instanceof TFile) {
                console.log("✏️ Updating `triples.json`...");
                await this.app.vault.modify(file, JSON.stringify(uniqueTriples, null, 2));
            } else {
                console.log("🆕 Creating `triples.json`...");
                await this.app.vault.create(normalizedPath, JSON.stringify(uniqueTriples, null, 2));
            }
            console.log("✅ Triples successfully saved.");
        } catch (err) {
            console.error(`❌ Error writing triples.json: ${err}`);
        }
    }
    
    

    async createEntityNotes(triples: Triple[]) {
        const basePath = "Entities";
    
        try {
            await this.app.vault.createFolder(basePath);
        } catch (err) {
            console.warn(`⚠️ Folder ${basePath} already exists, skipping creation.`);
        }
    
        for (const triple of triples) {
            await this.createOrUpdateFile(`${basePath}/${triple.entity}.md`, `# ${triple.entity}\n`);
            await this.createOrUpdateFile(`${basePath}/${triple.attribute}.md`, `# ${triple.attribute}\n`);
            await this.createOrUpdateFile(`${basePath}/${triple.value}.md`, `# ${triple.value}\n`);
        }
    }
    
    async createOrUpdateFile(filePath: string, content: string) {
        const normalizedPath = normalizePath(filePath);
        const file = this.app.vault.getAbstractFileByPath(normalizedPath);
    
        if (file instanceof TFile) {
            console.log(`✏️ Updating existing file: ${normalizedPath}`);
            let existingContent = await this.app.vault.read(file);
            if (!existingContent.includes(content.trim())) {
                await this.app.vault.modify(file, existingContent + "\n" + content);
            }
        } else {
            try {
                console.log(`🆕 Creating new file: ${normalizedPath}`);
                await this.app.vault.create(normalizedPath, content);
            } catch (err) {
                console.warn(`⚠️ File already exists: ${normalizedPath}, skipping creation.`);
            }
        }
    }
    
}
