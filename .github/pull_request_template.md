# Pull Request Template

Thank you for contributing to Rosalution! 😁

<!--- This project only accepts pull requests related to open issues -->
<!--- If suggesting a new feature or change, please discuss it in an issue first -->
<!--- If fixing a bug, there should be an issue describing it with steps to reproduce -->

Any contributions to this repository should follow the
 [Contributing Guidelines](https://github.com/uab-cgds-worthey/rosalution/blob/main/CONTRIBUTING.md)
 and [Code of Conduct](https://github.com/uab-cgds-worthey/rosalution/blob/main/CODE_OF_CONDUCT.md).

<!-- Pull Request template begins here -->
<!-- Delete everything from beginning of file to here -->
## Checklist before requesting a review

- [ ] I have performed a self-review of my code.
- [ ] My code follows the style guidelines enforced by static analysis tools.
- [ ] If it is a core feature, I have added thorough tests.
- [ ] My changes generate no new warnings.
- [ ] New and existing unit tests pass locally with my changes.
- [ ] New or existing JSON is formatted using JQ
- [ ] I have updated the CHANGELOG to note of any product updates that will be going in with this pull request.

<!-- Delete the tasks from the above list that are Not Applicable for your pull request -->

## Pull Request Details

Issue Number ______ - [Issue Title](Link to Issue here)
<!-- Note: Title your Pull Request with an appropriate title corresponding to the Issue title -->
Changes made:

- Describe changes you made in bullet points
- ........
- ......

**To Review:**
<!-- Make a to do list of things to check for to approve the pull request -->
<!-- Modify the below list as appropriate by editing and deleting text that is not applicable-->

- [ ] Static Analysis by Reviewer
- [ ] The changes made to < describe purpose of change > are working as intended/rendered correctly.
  To check this run the following commands:

  ``` bash
  < Recommended command (s) provided here, modify as needed. >
  ....
  docker compose down
  docker system prune -a --volumes
  docker compose up --build -d
  ```

    - Visit <https://local.rosalution.cgds/rosalution/login>. Login as `developer`.
    - Remaining instructions to review changes.

- [ ] List any other checks needed to be reviewed.
- [ ] All Github Actions checks have passed.

<!-- Delete below header if Screenshots are NOT included -->
### Screenshots (if appropriate)

<!-- Delete below Note AFTER assigning label to your Pull Request -->
Note: Assign a label to your pull request corresponding to the Issue label if applicable.
