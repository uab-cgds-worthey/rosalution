"""Testing endpoints for adding/updating/removing omic units to an analysis."""

import json
import pytest

def test_adding_omic_unit_to_analysis(client, mock_access_token, mock_repositories, cpam0002_analysis_json):
  """Test adding an omic unit to the analysis"""

  def valid_query_side_effect(*args, **kwargs):  # pylint: disable=unused-argument
        find, query = args  # pylint: disable=unused-variable
        analysis = cpam0002_analysis_json
        analysis['genomic_units'].append(query['$push']['genomic_units'])
        analysis['_id'] = 'fake-mongo-object-id'
        return analysis
  
  new_genomic_unit = {
      'gene': "JAK2",
      'transcripts': "NM_004972.3",
      'cdna': "c.1694G>C",
      'protein': "p.Arg565Thr",
      'reason_of_interest': "Find this variant interesting to explore.",
  }

  mock_repositories["analysis"].collection.find_one_and_update.side_effect = valid_query_side_effect

  response = client.post(
        "/analysis/CPAM0002/genomic_unit",
        headers={"Authorization": "Bearer " + mock_access_token},
        data={'new_genomic_unit': json.dumps(new_genomic_unit)}
    )

  assert response.status_code == 200
  actual_genomic_units = json.loads(response.text)
  assert len(actual_genomic_units) == 2