import { load } from "js-yaml";

/**
 * Parses YAML frontmatter to extract triples (Entity, Attribute, Value).
 */
export function parseTriples(content: string): { entity: string; attribute: string; value: string, isEntity: boolean }[] {
    const yamlMatch = content.match(/^---\n([\s\S]+?)\n---/);
    if (!yamlMatch) return [];

    try {
        const yamlData = load(yamlMatch[1]) as any;
        const entity = yamlData.entity || "Unknown Entity";
        const attributes = yamlData.attributes || [];

        return attributes.map((attr: string) => {
            const [attribute, value] = attr.split(":").map((s) => s.trim());

            // ✅ Ensure attributes are also treated as entities
            const isAttributeEntity = true;

            // ✅ Ensure values are standardized (remove [[ ]])
            const isValueEntity = true;
            const cleanValue = value.replace(/^\[\[/, "").replace(/\]\]$/, ""); // Removes [[ ]]

            return [
                { entity, attribute: "has_attribute", value: attribute, isEntity: isAttributeEntity },
                { entity, attribute, value: cleanValue, isEntity: isValueEntity }
            ];
        }).flat();
    } catch (error) {
        console.error("Failed to parse YAML frontmatter:", error);
        return [];
    }
}
