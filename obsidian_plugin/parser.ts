import { load } from "js-yaml";
import { Triple } from "./types";  // ✅ Import the Triple interface

export function parseTriples(content: string): Triple[] {
    const yamlMatch = content.match(/^---\n([\s\S]+?)\n---/);
    if (!yamlMatch) return [];

    try {
        const yamlData = load(yamlMatch[1]) as any;
        const entity = yamlData.entity || "Unknown Entity";
        const attributes = yamlData.attributes || [];

        return attributes.map((attr: string) => {
            const [attribute, value] = attr.split(":").map((s) => s.trim());
            const cleanValue = value.replace(/^\[\[/, "").replace(/\]\]$/, ""); // Removes [[ ]]

            return [
                { entity, attribute: "has_attribute", value: attribute, version: "master_version" },
                { entity, attribute, value: cleanValue, version: "live_version" }
            ];
        }).flat();
    } catch (error) {
        console.error("Failed to parse YAML frontmatter:", error);
        return [];
    }
}
