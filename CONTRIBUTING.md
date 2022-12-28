# Contributing to Rosalution

:grin: :tada: Thank you for taking the time to contribute! :grin: :tada:

The following is a set of guidelines for contributing to Rosalution.

- [Contributing](#contributing)
  - [Linting and Static Analysis](#linting-and-static-analysis)
- [Reporting Issues](#reporting-issues)
- [Seeking Support](#seeking-support)

---

## Contributing

To get started on contributing to Rosalution:

- Choose an existing feature/bug listed under issues.
  - If the feature/bug is not listed under issues, create the feature request/bug. Only start work on it once request is accepted.
- Fork and create a new branch for your work.
- Submit a pull request with adequete documentation of functionality and changes made. Ensure the PR description clearly describes the problem and solution. Include the relevant issue number if applicable.

### Linting and Static Analysis

Please ensure that your branch passes static analysis when submitting a pull request.

- To run linting in `./frontend/`

  ``` bash
  yarn lint:auto
  ```
  
- To run linting in `./backend/`

  ``` bash
  pylint src tests 
  ```

To reference configuration files:

- General: `./etc/static-analysis`
- Frontend: `./frontend/.eslintrc.js`
- Backend: `./backend/.pylintrc`

---

## Reporting Issues

If you encounter a bug while using the project, we want to hear about it! Here's how to report a bug:

  1. Check the [existing issues](https://github.com/uab-cgds-worthey/rosalution/issues) to see if the bug has already
   been reported.
  2. If the bug has not already been reported, create a new issue by clicking the "New Issue" button on the
   [issues page](https://github.com/uab-cgds-worthey/rosalution/issues).
  3. In the issue template, provide a clear and concise description of the bug, including any error messages that you
   encountered and steps to reproduce the bug.
  4. If possible, include any relevant details such as the version of the project you are using, your operating system,
   and any other relevant information that may help to reproduce and fix the bug.

We will review your issue and work to resolve the bug as soon as possible. Thank you for helping to improve the project!

---

## Seeking Support

For support in setting up and using Rosalution, please feel free to either use Github Issues or contact us via email on cgds@uabmc.edu.
