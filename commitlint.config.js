module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [
      2, // 0 = disable, 1 = warning, 2 = error
      'always',
      [
        'feat', // new feature
        'fix', // bug fix
        'docs', // documentation changes
        'style', // code style changes (formatting, etc)
        'refactor', // code refactoring without adding new features or fixing bugs
        'test', // adding or updating tests
        'chore', // maintenance tasks (e.g., dependency updates)
        'ci' // continuous integration changes
      ],
    ],
    'type-case': [2, 'always', 'lower-case'], // enforce lowercase types
    'subject-case': [2, 'never', ['sentence-case']], // no sentence case in the subject
    'subject-full-stop': [2, 'never', '.'], // no period at the end of the subject
    'header-max-length': [2, 'always', 72], // max length of the commit header
  },
};
