module.exports = {
    root: true,
    env: {
        node: true,
    },
    extends: ["plugin:vue/essential", "eslint:recommended"],
    parserOptions: {
        parser: "babel-eslint",
    },
    rules: {
        "no-console": process.env.NODE_ENV === "production" ? "off" : "off",
        "no-unused-vars": process.env.NODE_ENV === "production" ? "off" : "off",
        "no-debugger": process.env.NODE_ENV === "production" ? "off" : "off",
        "no-undef": process.env.NODE_ENV === "production" ? "off" : "off",
    },
    overrides: [
        {
            files: [
                "**/__tests__/*.{j,t}s?(x)",
                "**/tests/unit/**/*.spec.{j,t}s?(x)",
            ],
            env: {
                mocha: true,
            },
        },
    ],
};
