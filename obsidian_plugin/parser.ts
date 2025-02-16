import { load } from "js-yaml";
import { Triple } from "./types";  // ✅ Import the Triple interface

export function parseTriples(content: string): Triple[] {
    console.log("🛠 Parsing Content:", content);
    try {
        const yamlMatch = content.match(/^---\n([\s\S]+?)\n---/);
        if (!yamlMatch) {
            console.warn("⚠️ No YAML block found!");
            return [];
        }

        const yamlData = load(yamlMatch[1]) as any;
        console.log("📂 Parsed YAML Data:", yamlData);

        if (!yamlData.entity || !yamlData.live_version) {
            console.warn("⚠️ Missing entity or live_version in YAML.");
            return [];
        }

        let triples: Triple[] = [];
        for (const [attribute, value] of Object.entries(yamlData.live_version)) {
            if (typeof value === "string") { 
                triples.push({
                    entity: yamlData.entity,
                    attribute,
                    value,
                    version: "live_version",  // ✅ Always include a `version`
                });
            } else {
                console.warn(`⚠️ Skipping attribute ${attribute} because it's not a string.`);
            }
        }

        console.log("✅ Extracted Triples:", triples);
        return triples;
    } catch (error) {
        console.error("❌ Error parsing triples:", error);
        return [];
    }
}
