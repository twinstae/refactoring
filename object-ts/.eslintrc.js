module.exports = {
  parser: '@typescript-eslint/parser', // ESLint 파서를 지정한다.
  extends: [
    'plugin:@typescript-eslint/recommended', // @typescript-eslint/eslint-plugin 규칙을 사용한다.
    'plugin:prettier/recommended',
  ],
  parserOptions: {
    ecmaVersion: 2018, // 모던 ES의 파싱을 허용한다.
    sourceType: 'module', // import의 사용을 허용한다.
  },
}
