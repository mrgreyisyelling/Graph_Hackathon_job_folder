export interface Triple {
    entity: string;
    attribute: string;
    value: string;
    version?: string;  // ✅ Ensure this property is included
}
