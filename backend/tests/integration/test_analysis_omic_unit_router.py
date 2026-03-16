"""Testing endpoints for adding/updating/removing omic units to an analysis."""

import json
import pytest

def test_adding_omic_unit_to_analysis(client, mock_access_token, mock_repositories, cpam0002_analysis_json, successfully_added_genomic_units):
  """Test adding an omic unit to the analysis"""
  
  new_genomic_unit = {
      'gene': "JAK2",
      'transcript': "NM_004972.3",
      'cdna': "c.1694G>C",
      'protein': "p.Arg565Thr",
      'reason_of_interest': "Find this variant interesting to explore.",
  }

  mock_repositories["analysis"].collection.find_one_and_update.return_value = successfully_added_genomic_units

  response = client.post(
        "/analysis/CPAM0002/genomic_unit",
        headers={"Authorization": "Bearer " + mock_access_token},
        content=json.dumps(new_genomic_unit)
    )
  
  print("This is the response")
  print(response)

  assert response.status_code == 200
  actual_genomic_units = json.loads(response.text)
  assert len(actual_genomic_units) == 2



# Fixtures at the bottom of the file

@pytest.fixture(name="successfully_added_genomic_units")
def fixture_success_adding_genomic_units():
    """Fixture for updated analysis with added genomic unit"""
    return {
          "_id": "fake-mongo-object-id",
          "name": 'CPAM0002',
          "description": 'Vacuolar myopathy with autophagy, X-linked vacuolar myopathy with autophagy',
          "nominated_by": 'Dr. Person One',
          "genomic_units": [
            {
              "gene": 'VMA21',
              "transcripts": [
                {
                  "transcript": 'NM_001017980.3'
                }
              ],
              "variants": [
                {
                  "hgvs_variant": 'NM_001017980.3:c.164G>T',
                  "c_dot": 'c.164G>T',
                  "p_dot": 'p.Gly55Val',
                  "build": 'hg19',
                  'case': [
                    {
                      "field": 'Evidence',
                      "value": [
                        'PVS1',
                        'PM2'
                      ]
                    }
                  ]
                }
              ]
            },
            {
              "gene": 'JAK2',
              "transcripts": [
                {
                  "transcript": 'NM_004972.3'
                },
              ],
              "variants": [
                  {
                    "hgvs_variant": 'NM_004972.3:c.1694G>C',
                    "c_dot": 'c.1694G>C',
                    "p_dot": 'p.Arg565Thr',
                    "build": 'GRCh38',
                    'case': [
                      {
                        "field": 'Reason of Interest',
                        "value": [
                          'Find this variant interesting to explore.'
                        ]
                      }
                    ]
                  },
              ]
            }
          ],
        }