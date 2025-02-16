export interface Triple {
    entity: string;
    attribute: string;
    value: string;
    version?: string;  // Optional because some triples might not have it initially
}
