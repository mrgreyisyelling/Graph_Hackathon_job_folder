import { ItemView, WorkspaceLeaf } from "obsidian";
import { KnowledgeGraphStore } from "./store";

export const VIEW_TYPE_TRIPLE = "triple-view";

export class TripleView extends ItemView {
    private store: KnowledgeGraphStore;

    constructor(leaf: WorkspaceLeaf, store: KnowledgeGraphStore) {
        super(leaf);
        this.store = store;
    }

    getViewType(): string {
        return VIEW_TYPE_TRIPLE;
    }

    getDisplayText(): string {
        return "Triple Knowledge Graph";
    }

    async onOpen(): Promise<void> {
        const container = this.contentEl;
        container.empty();

        const title = container.createEl("h2", { text: "Extracted Triples" });

        const triplesList = container.createEl("ul");
        this.store.getTriples().forEach(triple => {
            triplesList.createEl("li", { text: `${triple.entity} → ${triple.attribute}: ${triple.value}` });
        });
    }

    async onClose(): Promise<void> {
        // Cleanup if needed
    }
}