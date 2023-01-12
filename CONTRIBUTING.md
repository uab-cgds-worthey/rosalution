# Contributing Guidelines

:grin: :tada: Thank you for taking the time to contribute! :grin: :tada:

The following is a set of guidelines for contributing to Rosalution.

- [Contributing](#contributing)
    - [Linting and Static Analysis](#linting-and-static-analysis)
- [Reporting Issues](#reporting-issues)
- [Seeking Support](#seeking-support)

---

## Contributing

To get started on contributing to Rosalution:

- Follow our [Code of Conduct](https://github.com/uab-cgds-worthey/rosalution/blob/main/CODE_OF_CONDUCT.md)
- Read these **Contributing Guidelines** to completion
- Choose an existing feature/bug listed under issues.
    - If the feature/bug is not listed under issues, create a new issue by clicking the **"New Issue"** button on the
       [issues page](https://github.com/uab-cgds-worthey/rosalution/issues) and click "Get started" for a
       "🧬 New feature proposal".  
       Only start work on it once request is reviewed and accepted.
- Fork and create a new branch for your work.
- Submit a pull request with adequate documentation of functionality and changes made.
Ensure the PR description clearly describes the problem and solution. Include the relevant issue number if applicable.

### Linting and Static Analysis

Please ensure that your branch passes static analysis when submitting a pull request.
GitHub Actions are configured to automate these operations upon a git push into GitHub.

- To run linting in `./frontend/`

  ``` bash
  yarn lint:auto
  ```
  
- To run linting in `./backend/`

  ``` bash
  pylint src tests 
  ```

- To run linting for markdown `.md` files

  We use a dependency called markdownlint.
  For installation/setup instructions, refer to [markdownlint's Github repo](https://github.com/DavidAnson/markdownlint).
  Please reference our configuration files for additional linting rules.

To reference configuration files:

- General & Markdown: `./etc/static-analysis/`
- Frontend: `./frontend/.eslintrc.js`
- Backend: `./backend/.pylintrc`

---

## Reporting Issues

If you encounter a bug while using the project, we want to hear about it! Here's how to report a bug:

  1. Check the [existing issues](https://github.com/uab-cgds-worthey/rosalution/issues) to see if the bug has already
   been reported.
  2. If the bug has not already been reported, create a new issue by clicking the "New Issue" button on the
   [issues page](https://github.com/uab-cgds-worthey/rosalution/issues) and click "Get started" for a "🐞 Bug Report".
  3. In the 🐞 Bug Report template, provide a clear and concise description of the bug, including any error messages
   that you encountered and steps to reproduce the bug in a specific environment.
  4. If possible, include any relevant details such as the version of the project you are using, your operating system,
   and any other relevant information that may help to reproduce and fix the bug.

We will review your issue and work to resolve the bug as soon as possible. Thank you for helping to improve the project!

---

## Seeking Support

For support in setting up and using Rosalution, please feel free to either use GitHub Issues or contact us via email on cgds@uabmc.edu.
