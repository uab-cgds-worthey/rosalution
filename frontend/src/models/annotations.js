// import Requests from '@/requests.js';
export default {
  async getAnnotations(analysisName, gene, variant) {
    // const baseUrl = '/rosalution/api/';
    // const urlQuery = 'analysis/' + analysisName;
    // return await Requests.get(baseUrl + urlQuery);
    return annotationsTemporary;
  },
};


const annotationsTemporary = {
  'Gene Description': `This gene encodes a chaperone for assembly of lysosomal vacuolar ATPase.[provided by RefSeq,
    Jul 2012]`,
  'Entrez Gene Id': 203547,
  'OMIM': ['Myopathy, X-linked, With Excessive Autophagy'],
  'HPO': `HP:0001270:Motor delay, HP:0001419:X-linked recessive inheritance
    HP:0001371:Flexion contracture, HP:0003391:Gowers sign, HP:0008994:Proximal
    muscle weakness in lower limbs, HP:0002650:Scoliosis, HP:0003551:
    Difficulty climbing stairs, HP:0002093: Respiratory insufficiency,
    HP:0003198: Myopathy, HP:0009046: Difficulty running, HP:0003202:
    Skeletal muscle atrophy, HP:0001319: Neonatal hypotonia,HP:0003236:
    Elevated circulating creatine kinase concentration, HP:0002486:Myotonia
    HP:0007941: Limited extraocular movements`,
  'Rat - RGD': `Predicted to be involved in vacuolar proton-transporting V-type ATPase complex assembly. Predicted to
    be located in lysosome. Predicted to be active in endoplasmic reticulum membrane. Human ortholog(s) of this gene
    implicated in X-linked myopathy with excessive autophagy. Orthologous to human VMA21 (vacuolar ATPase assembly
      factor VMA21); INTERACTS WITH 2,3,7,8-Tetrachlorodibenzofuran; 3-chloropropane-1,2-diol; bisphenol A."`,
  'Mouse - Automated': `Predicted to be involved in vacuolar proton-transporting V-type ATPase complex assembly.
  Predicted to be located in lysosome. Predicted to be active in endoplasmic reticulum membrane. Human ortholog(s)
  of this gene implicated in X-linked myopathy with excessive autophagy. Orthologous to human VMA21 (vacuolar ATPase
    assembly factor VMA21).`,
  'Zebrafish - Automated': `Predicted to be involved in vacuolar proton-transporting V-type ATPase complex assembly.
    Predicted to be located in ER to Golgi transport vesicle membrane; endoplasmic reticulum membrane; and endoplasmic
    reticulum-Golgi intermediate compartment membrane. Predicted to be integral component of membrane. Human
    ortholog(s) of this gene implicated in X-linked myopathy with excessive autophagy. Orthologous to human
    VMA21 (vacuolar ATPase assembly factor VMA21).`,
  'C-Elegens - Automated': `Predicted to be involved in vacuolar proton-transporting V-type ATPase complex assembly.
    Predicted to be located in cytoplasm. Predicted to be active in endoplasmic reticulum membrane. Human ortholog(s)
    of this gene implicated in X-linked myopathy with excessive autophagy. Orthologous to several human genes including
    VMA21 (vacuolar ATPase assembly factor VMA21).`,
  'Druggability': {
    'target': {
      'name': 'Vacuolar ATPase assembly integral membrane protein VMA21',
      'tdl': 'Tdark',
      'fam': 'Enzyme',
      'sym': 'VMA21',
      'description':
        'This gene encodes a chaperone for assembly of lysosomal vacuolar ATPase.[provided by RefSeq, Jul 2012]',
      'novelty': 0.46129032,
    },
  },
  'CADD': 33,
  'Phylop100': 6.373,
  'Clinvar': {
    'interpretation': 'VUS',
    'variant': 'NM_001017980.4(VMA21):c.164G>T (p.Gly55Val)',
    'dates': '2018-02-16',
    'thingy': 'X-linked myopathy with excessive autophagy',
  },
  'transcripts': [{
    'transcript': 'NM_001017980.3',
    'impact': 'Moderate',
    'cDNA change': 'c.164G>T',
    'AA Change': 'G55V (p.Gl55Val)',
    'Consequences': ['missense_variant', 'splice_region_variant'],
    'SIFT': 'deleterious',
    'Polyphen': 'possibly_damaging',
  }, {
    'transcript': 'NM_001363810.1',
    'impact': 'Moderate',
    'cDNA change': 'c.329G>T',
    'AA Change': 'G110V (p.Gly110Val)',
    'Consequences': ['missense_variant', 'splice_region_variant'],
    'SIFT': 'deleterious',
    'Polyphen': 'probably_damaging',
  }],
};
