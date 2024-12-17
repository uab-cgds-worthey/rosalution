import stylistic from '@stylistic/eslint-plugin-js';

export default [{
  plugins: {
    '@stylistic/js': stylistic,
  },
  rules: {
    // Possible Errors
    'no-cond-assign': 'off',
    'no-irregular-whitespace': 'error',
    'no-unexpected-multiline': 'error',

    // Best Practices
    'curly': ['error', 'multi-line'],
    'guard-for-in': 'error',
    'no-caller': 'error',
    'no-extend-native': 'error',
    'no-extra-bind': 'error',
    'no-invalid-this': 'off',
    'no-multi-str': 'error',
    'no-new-wrappers': 'error',
    'no-throw-literal': 'error',
    'no-with': 'error',
    'prefer-promise-reject-errors': 'error',

    // Variables
    'no-unused-vars': ['error', {args: 'none'}],

    // Stylistic
    '@stylistic/js/array-bracket-newline': 'off',
    '@stylistic/js/array-bracket-spacing': ['error', 'never'],
    '@stylistic/js/array-element-newline': 'off',
    '@stylistic/js/block-spacing': ['error', 'never'],
    '@stylistic/js/brace-style': 'error',
    'camelcase': ['error', {properties: 'never'}],
    '@stylistic/js/comma-dangle': ['error', 'always-multiline'],
    '@stylistic/js/comma-spacing': 'error',
    '@stylistic/js/comma-style': 'error',
    '@stylistic/js/computed-property-spacing': 'error',
    '@stylistic/js/eol-last': 'error',
    '@stylistic/js/func-call-spacing': 'error',
    '@stylistic/js/indent': [
      'error', 2, {
        'CallExpression': {
          'arguments': 2,
        },
        'FunctionDeclaration': {
          'body': 1,
          'parameters': 2,
        },
        'FunctionExpression': {
          'body': 1,
          'parameters': 2,
        },
        'MemberExpression': 2,
        'ObjectExpression': 1,
        'SwitchCase': 1,
        'ignoredNodes': [
          'ConditionalExpression',
        ],
      },
    ],
    '@stylistic/js/key-spacing': 'error',
    '@stylistic/js/keyword-spacing': 'error',
    '@stylistic/js/linebreak-style': 'error',
    '@stylistic/js/max-len': ['error', {
      code: 120,
      tabWidth: 2,
      ignoreUrls: true,
      ignorePattern: 'goog.(module|require)',
    }],
    'new-cap': 'error',
    'no-array-constructor': 'error',
    '@stylistic/js/no-mixed-spaces-and-tabs': 'error',
    '@stylistic/js/no-multiple-empty-lines': ['error', {max: 2}],
    'no-new-object': 'error',
    '@stylistic/js/no-tabs': 'error',
    '@stylistic/js/no-trailing-spaces': 'error',
    '@stylistic/js/object-curly-spacing': 'error',
    'one-var': ['error', {
      var: 'never',
      let: 'never',
      const: 'never',
    }],
    '@stylistic/js/operator-linebreak': ['error', 'after'],
    '@stylistic/js/padded-blocks': ['error', 'never'],
    '@stylistic/js/quote-props': ['error', 'consistent'],
    '@stylistic/js/quotes': ['error', 'single', {allowTemplateLiterals: true}],
    '@stylistic/js/semi': 'error',
    '@stylistic/js/semi-spacing': 'error',
    '@stylistic/js/space-before-blocks': 'error',
    '@stylistic/js/space-before-function-paren': ['error', {
      asyncArrow: 'always',
      anonymous: 'never',
      named: 'never',
    }],
    '@stylistic/js/spaced-comment': ['error', 'always'],
    '@stylistic/js/switch-colon-spacing': 'error',

    // ECMA 2022 rulesets
    '@stylistic/js/arrow-parens': ['error', 'always'],
    'constructor-super': 'error',
    '@stylistic/js/generator-star-spacing': ['error', 'after'],
    'no-new-symbol': 'error',
    'no-this-before-super': 'error',
    'no-var': 'error',
    'prefer-const': ['error', {destructuring: 'all'}],
    'prefer-rest-params': 'error',
    'prefer-spread': 'error',
    'rest-spread-spacing': 'error',
    'yield-star-spacing': ['error', 'after'],
  },
}];
