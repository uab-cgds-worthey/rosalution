import stylistic from '@stylistic/eslint-plugin';

export default [{
  name: 'cgds',
  plugins: {
    '@stylistic': stylistic,
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
    '@stylistic/array-bracket-newline': 'off',
    '@stylistic/array-bracket-spacing': ['error', 'never'],
    '@stylistic/array-element-newline': 'off',
    '@stylistic/block-spacing': ['error', 'never'],
    '@stylistic/brace-style': 'error',
    'camelcase': ['error', {properties: 'never'}],
    '@stylistic/comma-dangle': ['error', 'always-multiline'],
    '@stylistic/comma-spacing': 'error',
    '@stylistic/comma-style': 'error',
    '@stylistic/computed-property-spacing': 'error',
    '@stylistic/eol-last': 'error',
    '@/func-call-spacing': 'error',
    '@stylistic/indent': [
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
    '@stylistic/key-spacing': 'error',
    '@stylistic/keyword-spacing': 'error',
    '@stylistic/linebreak-style': 'error',
    '@stylistic/max-len': ['error', {
      code: 120,
      tabWidth: 2,
      ignoreUrls: true,
      ignorePattern: 'goog.(module|require)',
    }],
    'new-cap': 'error',
    'no-array-constructor': 'error',
    '@stylistic/no-mixed-spaces-and-tabs': 'error',
    '@stylistic/no-multiple-empty-lines': ['error', {max: 2}],
    'no-object-constructor': 'error',
    '@stylistic/no-tabs': 'error',
    '@stylistic/no-trailing-spaces': 'error',
    '@stylistic/object-curly-spacing': 'error',
    'one-var': ['error', {
      var: 'never',
      let: 'never',
      const: 'never',
    }],
    '@stylistic/operator-linebreak': ['error', 'after'],
    '@stylistic/padded-blocks': ['error', 'never'],
    '@stylistic/quote-props': ['error', 'consistent'],
    '@stylistic/quotes': ['error', 'single', {'allowTemplateLiterals': 'always'}],
    '@stylistic/semi': 'error',
    '@stylistic/semi-spacing': 'error',
    '@stylistic/space-before-blocks': 'error',
    '@stylistic/space-before-function-paren': ['error', {
      asyncArrow: 'always',
      anonymous: 'never',
      named: 'never',
    }],
    '@stylistic/spaced-comment': ['error', 'always'],
    '@stylistic/switch-colon-spacing': 'error',

    // ECMA 2023 rulesets
    'no-new-native-nonconstructor': 'error',

    // ECMA 2022 rulesets
    '@stylistic/arrow-parens': ['error', 'always'],
    'constructor-super': 'error',
    '@stylistic/generator-star-spacing': ['error', 'after'],
    'no-this-before-super': 'error',
    'no-var': 'error',
    'prefer-const': ['error', {destructuring: 'all'}],
    'prefer-rest-params': 'error',
    'prefer-spread': 'error',
    '@stylistic/rest-spread-spacing': 'error',
    '@stylistic/yield-star-spacing': ['error', 'after'],
  },
}];
