import { TripleView } from "./view"; 
import { Plugin, TFile, normalizePath } from "obsidian";
import { load } from "js-yaml"; // ✅ Use js-yaml instead
import { parseTriples } from "./parser";
import { KnowledgeGraphStore } from "./store";

export default class KnowledgeGraphPlugin extends Plugin {
    private store: KnowledgeGraphStore = new KnowledgeGraphStore();
    private outputFile = "triples.json"; // ✅ Path for output file

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
            const triples = parseTriples(content);
    
            // ✅ Store relationships
            this.store.updateTriples(file.path, triples);
            console.log("Extracted Triples:", triples);
    
            // ✅ Create placeholder notes for all detected entities
            await this.createEntities(triples);
    
            // ✅ Add links to extracted entities in the note
            await this.insertEntityLinks(file, content, triples);
    
            // ✅ Write triples to file
            await this.saveTriplesToFile();
        }
    }

    async saveTriplesToFile() {
        const path = normalizePath(this.outputFile);
        let storedTriples = this.store.getTriples();
    
        // ✅ Remove duplicate triples
        const uniqueTriples = Array.from(
            new Map(storedTriples.map(triple => [JSON.stringify(triple), triple])).values()
        );
        
        // ✅ Convert to JSON
        const jsonData = JSON.stringify(uniqueTriples, null, 2);
    
        // ✅ Write to a local file in Obsidian
        try {
            let file = this.app.vault.getAbstractFileByPath(path);
            if (file instanceof TFile) {
                await this.app.vault.modify(file, jsonData);
            } else {
                await this.app.vault.create(path, jsonData);
            }
            console.log(`Triples saved to ${path}`);
        } catch (err) {
            console.error("Failed to save triples:", err);
        }
    }
    

    async loadKnowledgeGraph() {
        const files = this.app.vault.getMarkdownFiles();
        for (const file of files) {
            await this.processFile(file);
        }
    }

    async insertEntityLinks(file: TFile, content: string, triples: any[]) {
        // Extract entities from the triples
        const linkedEntities = new Set();
    
        triples.forEach(triple => {
            linkedEntities.add(triple.attribute); // Attributes are now entities
            linkedEntities.add(triple.value);     // Values are also entities
        });
    
        // Convert to [[WikiLinks]]
        const entityLinks = Array.from(linkedEntities)
            .map(entity => `[[${entity}]]`)
            .join("\n");
    
        // Check if links already exist to prevent duplicates
        if (content.includes(entityLinks)) {
            console.log(`Entity links already exist in ${file.path}, skipping update.`);
            return;
        }
    
        // Append links to the bottom of the file
        const updatedContent = `${content.trim()}\n\n## Related Entities\n${entityLinks}`;
    
        // Write back to the file
        await this.app.vault.modify(file, updatedContent);
        console.log(`Updated ${file.path} with entity links.`);
    }

    async createEntities(triples: any[]) {
        for (const triple of triples) {
            const entityName = triple.value; // Ensuring values become entities
            const attributeName = triple.attribute; // Ensuring attributes become entities
    
            // ✅ Create notes for entities (values) & ensure they exist as triples
            await this.ensureEntityNote(entityName);
            await this.addEntityTriple(entityName);
    
            // ✅ Create notes for attributes & ensure they exist as triples
            await this.ensureEntityNote(attributeName);
            await this.addEntityTriple(attributeName);
        }
    }

    async addEntityTriple(entityName: string) {
        const selfTriple = { entity: entityName, attribute: "is_entity", value: entityName };
        
        // ✅ Check if it already exists to avoid duplicates
        const existingTriples = this.store.getTriples();
        const alreadyExists = existingTriples.some(
            (t) => t.entity === entityName && t.attribute === "is_entity"
        );
    
        if (!alreadyExists) {
            console.log(`Adding self-triple for ${entityName}`);
            this.store.updateTriples(entityName, [selfTriple]);
            await this.saveTriplesToFile();
        }
    }
    

    /**
     * Ensures a note exists for a given entity or attribute.
     * If it doesn’t exist, creates it with a default YAML frontmatter.
     */
    async ensureEntityNote(entityName: string) {
        const entityFilePath = normalizePath(`${entityName}.md`);
        let file = this.app.vault.getAbstractFileByPath(entityFilePath);
    
        if (!file) {
            console.log(`Creating entity note: ${entityName}`);
            const defaultYaml = `---\nentity: "${entityName}"\nattributes: []\n---\n\n`;
            await this.app.vault.create(entityFilePath, defaultYaml);
        }
    }

    onunload() {
        console.log("Unloading Knowledge Graph Plugin");
    }
}