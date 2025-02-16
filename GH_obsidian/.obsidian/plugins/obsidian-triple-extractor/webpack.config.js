const path = require("path");

module.exports = {
    entry: {
        main: "./src/main.ts",
        merge: "./src/merge.ts",  // ✅ Explicitly add merge.ts
        parser: "./src/parser.ts",  // ✅ Explicitly add parser.ts
        store: "./src/store.ts",  // ✅ Explicitly add store.ts
    },
    output: {
        path: path.resolve(__dirname, "dist"),
        filename: "[name].js",
        libraryTarget: "commonjs",
    },
    resolve: {
        extensions: [".ts", ".js"],
    },
    module: {
        rules: [
            {
                test: /\.ts$/,
                use: "ts-loader",
                exclude: /node_modules/,
            },
        ],
    },
    externals: {
        obsidian: "commonjs obsidian",
    },
};
