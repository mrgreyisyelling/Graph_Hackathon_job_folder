import { load } from "js-yaml";
import { Triple } from "./types";  // ✅ Import the Triple interface

export function parseTriples(content: string) {
    console.log("🛠 Parsing Content:", content);
    try {
        const yamlMatch = content.match(/^---\n([\s\S]+?)\n---/);
        if (!yamlMatch) {
            console.warn("⚠️ No YAML block found!");
            return [];
        }

        const yamlData = load(yamlMatch[1]) as any;
        console.log("📂 Parsed YAML Data:", yamlData);

        if (!yamlData.entity) {
            console.warn("⚠️ Missing entity in YAML.");
            return [];
        }

        let triples: Triple[] = [];

        // ✅ If `live_version` exists, extract triples from there
        if (yamlData.live_version) {
            for (const [attribute, value] of Object.entries(yamlData.live_version)) {
                if (typeof value === "string") {
                    triples.push({ entity: yamlData.entity, attribute, value, version: "live_version" });
                } else {
                    console.warn(`⚠️ Skipping attribute ${attribute} (not a string).`);
                }
            }
        }

        // ✅ If `attributes` exists (fallback), extract triples from there
        if (yamlData.attributes && Array.isArray(yamlData.attributes)) {
            yamlData.attributes.forEach((attr: string) => {
                const [attribute, value] = attr.split(":").map(s => s.trim());
                if (attribute && value) {
                    triples.push({ entity: yamlData.entity, attribute, value, version: "live_version" });
                }
            });
        }

        console.log("✅ Extracted Triples:", triples);
        return triples;
    } catch (error) {
        console.error("❌ Error parsing triples:", error);
        return [];
    }
}
