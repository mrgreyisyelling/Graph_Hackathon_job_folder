"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.parseTriples = parseTriples;
const js_yaml_1 = require("js-yaml");
/**
 * Parses YAML frontmatter to extract triples (Entity, Attribute, Value).
 */
function parseTriples(content) {
    const yamlMatch = content.match(/^---\n([\s\S]+?)\n---/);
    if (!yamlMatch)
        return [];
    try {
        const yamlData = (0, js_yaml_1.load)(yamlMatch[1]);
        const entity = yamlData.entity || "Unknown Entity";
        const attributes = yamlData.attributes || [];
        return attributes.map((attr) => {
            const [attribute, value] = attr.split(":").map((s) => s.trim());
            return { entity, attribute, value };
        });
    }
    catch (error) {
        console.error("Failed to parse YAML frontmatter:", error);
        return [];
    }
}
