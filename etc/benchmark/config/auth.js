import http from 'k6/http';

/**
 * Requests a JWT Auth Token from the Rosalution API using the Client ID and Client Secret. 
 * 
 * @param {string} baseUrl 
 * @param {string} clientId 
 * @param {string} clientSecret 
 * @returns JWT Auth Token for the Rosalution API
 */
export async function rosalutionAuth(baseUrl, clientId, clientSecret) {
  const authUrl = `${baseUrl}/auth/token`
  const authData = `client_id=${clientId}&client_secret=${clientSecret}`
  let responseBody;
  let authResponse;

  try {
    authResponse = http.post(authUrl, authData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });

    responseBody = authResponse.json();
    if ( Object.hasOwn(responseBody, 'access_token') )
      return responseBody['access_token']
    }
  catch {
    throw `Failure to Authenticate with Rosalution API: ${authResponse}`
  }

  return null
}