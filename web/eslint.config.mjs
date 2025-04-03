import react from "eslint-plugin-react";
import globals from "globals";
import path from "node:path";
import { fileURLToPath } from "node:url";
import js from "@eslint/js";
import { FlatCompat } from "@eslint/eslintrc";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const compat = new FlatCompat({
  baseDirectory: __dirname,
  recommendedConfig: js.configs.recommended,
  allConfig: js.configs.all,
});

export default [
  {
    ignores: [
      "**/*.config.js",
      "**/*.config.base.js",
      "**/*.test.tsx",
      "**/dist",
    ],
  },
  ...compat.extends(
    "prettier",
    "eslint:recommended",
    "plugin:react/jsx-runtime",
    "plugin:react/recommended"
  ),

  {
    files: ["**/*.{js,mjs,cjs,jsx}"],
  },

  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
      },
    },
  },

  {
    plugins: {
      react,
    },

    settings: {
      react: {
        version: "18.3.0",
      },
    },

    rules: {
      "no-unused-vars": "off",
      "react/display-name": "off",
      "react/no-unescaped-entities": "off",
      "react/prop-types": "off",
      "react/react-in-jsx-scope": "off",
      "react/no-unknown-property": "off",
      "react/no-direct-mutation-state": "off",
      "react/require-render-return": "off",
      "react/no-string-refs": "off",
      "react/jsx-uses-react": "error",
      "react/jsx-no-undef": "off",
      "react/jsx-uses-vars": "error",
      "react/no-danger-with-children": "off",
    },
  },
];
