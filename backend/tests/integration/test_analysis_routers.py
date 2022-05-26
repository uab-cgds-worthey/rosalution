"""Analysis Routes Intergration test"""

def test_get_analyses(client, mock_access_token):
    """Testing that the correct number of analyses were returned and in the right order"""
    # database_collections['analysis'].find()
    # database_collections['analysis'].find.return_value = {'trash': 'json'}

    response = client.get('/analysis/', headers={'Authorization': 'Bearer ' + mock_access_token})

    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[2]['name'] == 'CPAM0053'

def test_get_analyses_unauthorized(client):
    """ Tries to get the analyses from the endpoint, but is unauthorized. Does not provide valid token """
    response = client.get('/analysis/')

    assert response.status_code == 401

def test_get_analysis_summary(client, mock_access_token):
    """Testing if the analysis summary endpoint returns all of the analyses available"""
    response = client.get('/analysis/summary', headers={'Authorization': 'Bearer ' + mock_access_token})
    assert len(response.json()) == 5
