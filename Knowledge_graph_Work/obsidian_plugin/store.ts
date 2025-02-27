export class KnowledgeGraphStore {
    private triples: Map<string, { entity: string; attribute: string; value: string }[]> = new Map();

    updateTriples(filePath: string, newTriples: { entity: string; attribute: string; value: string }[]): void {
        this.triples.set(filePath, newTriples);
    }

    getTriples(): { entity: string; attribute: string; value: string }[] {
        return Array.from(this.triples.values()).flat();
    }

    clear(): void {
        this.triples.clear();
    }
}