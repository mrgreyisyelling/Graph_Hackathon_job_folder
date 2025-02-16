"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.KnowledgeGraphStore = void 0;
class KnowledgeGraphStore {
    constructor() {
        this.triples = new Map();
    }
    updateTriples(filePath, newTriples) {
        this.triples.set(filePath, newTriples);
    }
    getTriples() {
        return Array.from(this.triples.values()).flat();
    }
    clear() {
        this.triples.clear();
    }
}
exports.KnowledgeGraphStore = KnowledgeGraphStore;
