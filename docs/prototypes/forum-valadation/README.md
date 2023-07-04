# Forum Validation Prototype Implementation

This README provides instructions on how to incorporate files related to a forum validation prototype implementation into the main project.

## File Structure

The files are organized in the following way:

- Frontend JavaScript, Vue components, CSS styles, and their corresponding test files.
- End-to-end system test files.

## Instructions

1. **Frontend**
    - `inputDialog.js` should be placed directly under your project's `frontend/src` directory.

    - The Vue components `InputDialog.vue`, `InputDialogAttachUrl.vue`, and `InputDialogUploadFile.vue` should be placed
    inside the directory `src/components/Dialogs/` under your project's `frontend` directory. The path should look like:
    `frontend/src/components/Dialogs/`.

    - CSS styles related to the frontend should be placed in the `styles` directory under your project's `frontend/src`
    directory. The path should look like: `frontend/src/styles/`. Specifically, the file `main.css` should be located
    there.

    - Test files for these components `InputDialog.spec.js`, `InputDialogAttachUrl.spec.js`,
    `InputDialogUploadFile.spec.js` should be placed in `test/components/Dialogs/` under your project's `frontend`
    directory. The path should look like: `frontend/test/components/Dialogs/`.

2. **System-tests**
    - End-to-end test files `case_supporting_evidence.cy.js` and `import_new_case.cy.js` should be placed inside the
    `e2e` directory under the `system-tests` directory in your main project.
    The path should look like: `system-tests/e2e/`.

3. **Testing**
    - To test the frontend components, run `yarn test:unit` in your main project's `frontend` directory.
    - To test the end-to-end system tests, first make sure the application is running locally. Then, run `yarn test:e2e`
    in your main project's `system-tests` directory.

Please ensure you maintain this directory structure for the application to function correctly.

## Notes

- After adding these files, you might need to rebuild the docker containers based on your development environment.
- Make sure to run all the tests to ensure the integration went smoothly.
