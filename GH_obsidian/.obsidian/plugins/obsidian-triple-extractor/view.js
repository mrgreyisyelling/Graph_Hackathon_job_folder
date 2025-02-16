"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.TripleView = exports.VIEW_TYPE_TRIPLE = void 0;
const obsidian_1 = require("obsidian");
exports.VIEW_TYPE_TRIPLE = "triple-view";
class TripleView extends obsidian_1.ItemView {
    constructor(leaf, store) {
        super(leaf);
        this.store = store;
    }
    getViewType() {
        return exports.VIEW_TYPE_TRIPLE;
    }
    getDisplayText() {
        return "Triple Knowledge Graph";
    }
    onOpen() {
        return __awaiter(this, void 0, void 0, function* () {
            const container = this.contentEl;
            container.empty();
            const title = container.createEl("h2", { text: "Extracted Triples" });
            const triplesList = container.createEl("ul");
            this.store.getTriples().forEach(triple => {
                triplesList.createEl("li", { text: `${triple.entity} → ${triple.attribute}: ${triple.value}` });
            });
        });
    }
    onClose() {
        return __awaiter(this, void 0, void 0, function* () {
            // Cleanup if needed
        });
    }
}
exports.TripleView = TripleView;
