import js from '@eslint/js';
import boundaries from 'eslint-plugin-boundaries';
import globals from 'globals';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  { ignores: ['dist', 'src/routeTree.gen.ts'] },
  {
    extends: [js.configs.recommended, ...tseslint.configs.recommended],
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      ecmaVersion: 2022,
      globals: globals.browser,
    },
    plugins: { boundaries },
    settings: {
      'boundaries/elements': [
        { type: 'core', pattern: 'src/core/*' },
        { type: 'ui', pattern: 'src/ui/*' },
        { type: 'pattern', pattern: 'src/pattern/*' },
        { type: 'layouts', pattern: 'src/layouts/*' },
        { type: 'features', pattern: 'src/features/*' },
        { type: 'routes', pattern: 'src/routes/*' },
        { type: 'mocks', pattern: 'src/mocks/*' },
      ],
    },
    rules: {
      'boundaries/element-types': [
        'error',
        {
          default: 'disallow',
          rules: [
            { from: 'core', allow: ['core', 'mocks'] },
            { from: 'ui', allow: ['ui'] },
            { from: 'layouts', allow: ['core', 'ui', 'layouts'] },
            { from: 'pattern', allow: ['core', 'ui', 'pattern'] },
            { from: 'features', allow: ['core', 'ui', 'pattern', 'features'] },
            { from: 'routes', allow: ['core', 'ui', 'pattern', 'layouts', 'features', 'routes'] },
            { from: 'mocks', allow: ['core', 'mocks', 'features'] },
          ],
        },
      ],
    },
  },
  {
    files: ['**/*.test.{ts,tsx}'],
    rules: { 'boundaries/element-types': 'off' },
  },
);
