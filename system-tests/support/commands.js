// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
Cypress.Commands.add('resetDatabase', () => {
  return cy.exec(`docker compose exec -T rosalution-db mongosh /tmp/fixtures/seed.js`);
});


Cypress.Commands.add('startDb', () => {
// Create EventSource for SSE endpoint
  const eventSource = new EventSource('http://127.0.0.1:8000/coordinates');

  eventSource.onopen = () => {
      console.log('EventSource connected');
  }

  eventSource.addEventListener('closeEvent', function (event) {
      console.log('EventSource Closed');
      eventSource.close()
  });

  // eventSource can have event listeners based on the type of event.
  // By default for message type of event it have the onmessage method which can be used directly or this same can be
  // achieved through explicit eventlisteners
  eventSource.addEventListener('locationUpdate', function (event) {
      coords = JSON.parse(event.data);
      console.log('LocationUpdate', coords);
      updateCoordinates(coords)
      eventSource.close()
  });

  // In case of any error, if eventSource is not closed explicitly then client will retry the connection a new call to
  // backend will happen and the cycle will go on.
  eventSource.onerror = (error) => {
      console.error('EventSource failed', error)
      eventSource.close()
  }

  // Function to update and display coordinates
  function updateCoordinates(coordinates) {
      // Create a new paragraph element for each coordinate and append it
      const paragraph = document.createElement('p');
      paragraph.textContent = `Latitude: ${coordinates.lat}, Longitude: ${coordinates.lng}`;
      coordinatesElement.appendChild(paragraph);
  }
  cy.request({
    method: 'POST',
    url: '/api/dev/dbTransaction',
    body: {
      username: username,
      password: 'secret',
    },
  });
});

Cypress.Commands.add('login', (username) => {
  const sessionAlias = username;

  cy.session(sessionAlias, () => {
    cy.request({
      method: 'POST',
      url: '/api/dev/loginDev',
      form: true,
      body: {
        username: username,
        password: 'secret',
      },
    });

    cy.getCookie('rosalution_TOKEN').should('exist');
  }, {
    cacheAcrossSpecs: true,
  });
});
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })
