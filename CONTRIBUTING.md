# Contributing

The following is a set of guidelines for contributing to the **Decision Optimization Tool**.

The project emphasizes collaboration with universities and research centers to enhance quality and impact.
We highly value your feedback on the implemented features to ensure they meet user needs. Please share your expertise, test our features, and suggest improvements.
Your contributions are crucial for the project's continuous improvement and success.

## Ground Rules

1. We use Ruff code formatting for python and prettier/es-lint for JavaScript/React
1. All code must be testable and unit tested.

## Commits

We strive to keep a consistent and clean git history and all contributions should adhere to the following:

1. All tests should pass on all commits(*)
1. A commit should do one atomic change on the repository
1. The commit message should be descriptive.



We expect commit messages to follow this style:

1. Separate subject from body with a blank line
1. Limit the subject line to 50 characters
1. Capitalize the subject line
1. Do not end the subject line with a period
1. Use the imperative mood in the subject line
1. Wrap the body at 72 characters
1. Use the body to explain what and why vs. how

This list is taken from [here](https://chris.beams.io/posts/git-commit/).

Also, focus on making clear the reasons why you made the change in the first
place — the way things worked before the change (and what was wrong with that),
the way they work now, and why you decided to solve it the way you did. A
commit body is required for anything except very small changes.

(*) Tip for making sure all tests passes, try out --exec while rebasing. You
can then have all tests run per commit in a single command.


[Conventional commits](https://www.conventionalcommits.org/en/v1.0.0/) are expected to be used, with, in summary:

1. **fix**: a commit of the type `fix` patches a bug in your codebase (this correlates with _PATCH_ in Semantic Versioning).
1. **feat**: a commit of the type `feat` introduces a new feature to the codebase (this correlates with _MINOR_ in Semantic Versioning).
1. **BREAKING CHANGE**: a commit that has a footer `BREAKING CHANGE`:, or appends a ` !` after the type/scope, introduces a breaking API change (correlating with _MAJOR_ in Semantic Versioning). A BREAKING CHANGE can be part of commits of any type.
1. types other than `fix:` and `feat:` are allowed, for example* @commitlint/config-conventional* (based on the _Angular convention_) recommends `build:`, `chore:`, `ci:`, `docs:`, `style:`, `refactor:`, `perf:`, `test:`, and others.
1. _footers_ other than `BREAKING CHANGE: <description>` may be provided and follow a convention similar to _git trailer format_.


## Pull Request Scoping

Ideally a pull request will be small in scope, and atomic, addressing precisely
one issue, and mostly result in a single commit. It is however permissible to
fix minor details (formatting, linting, moving, simple refactoring ...) in the
vicinity of your work.

If you find that you want to do lots of changes that are not directly related
to the issue you're working on, create a separate PR for them so as to avoid
noise in the review process.

## Pull Request Process

1. Work on your own fork of the main repo
2. Squash/organize your work into meaningful atomic commits, if possible.
3. Push your commits and make a draft pull request. Describe what the pull request is about and link the issue.
4. Check that your pull request passes all tests.
5. While you wait, carefully review the diff yourself.
6. When all tests have passed and your are happy with your changes, change your
   pull request to "ready for review" and ask for a code review.
7. As a courtesy to the reviewer(s), you may mark commits that react to review
   comments with `fixup` (check out `git commit --fixup`) rather than
   immediately squashing / fixing up and force pushing
8. When the review is concluded, squash whatever still needs squashing, and
   [fast-forward](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/defining-the-mergeability-of-pull-requests/about-protected-branches#require-linear-history) merge.
