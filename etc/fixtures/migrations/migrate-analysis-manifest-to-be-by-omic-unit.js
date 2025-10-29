const usage = `
mongosh /tmp/database/migrate-analysis-manifest-to-be-by-omic-unit.js
    Script Options:
        help: if true print this help message
        databaseName: different name of the database if needed

    Generates an annotation manifest for each Rosalution analysis and updates
    genomic unit annotations with matching dataset source and version.  
    
    docker exec -it rosalution-rosalution-db-1 mongosh --file /tmp/fixtures/migrate-analysis-manifest-to-be-by-omic-unit.js
    mongosh --host localhost --port 27017 --file /tmp/fixtures/migrations/migrate-analysis-manifest-to-be-by-omic-unit.js --eval="databaseName='rosalution_db'"
`

help = process.argv.includes('help')

if (help) {
    print(usage);
    quit(1);
}

if (typeof databaseName === 'undefined') {
    databaseName = "rosalution_db";
} else if (typeof databaseName !== 'string') {
    print("databaseName must be a string");
    quit(1);
}

db = db.getSiblingDB(databaseName);

let yourDate = new Date()
yourDateString = yourDate.toISOString().split('T')[0].split('T')[0]

const transcriptDataset = [
    'transcript_id',
    'Polyphen Prediction',
    'Polyphen Score',
    'SIFT Prediction',
    'SIFT Score',
    'Consequences',
    'Impact'
]

const datasets_by_type = {
    'hgvs_variant': [
  'hgvs_variant_without_transcript_version',
  'SpliceAI_variant_linkout',
  'transcript_without_version',
  'ENSEMBL_VARIANT_HGVS_VARIANT_CALL_CACHE',
  'transcript_id',
  'ensembl_vep_vcf_string',
  'ClinVar_Variant_Id',
  'gnomAD_variant_url',
  'Polyphen Prediction',
  'Polyphen Score',
  'SIFT Prediction',
  'SIFT Score',
  'Consequences',
  'CADD',
  'alphamissense_classification',
  'alphamissense_pathogenicity',
  'Impact',
  'revel',
  'opencravat_search_variant_vcf_string',
  'chrom',
  'pos',
  'spliceai_acceptor_loss',
  'spliceai_donor_loss',
  'spliceai_donor_gain',
  'spliceai_acceptor_gain',
  'Ensembl_Transcript_Id',
  'gnomAD4',
  'DITTO',
  'ClinVar_variant_url',
  'ClinVar_Variantion_Id',
],
    'gene': [
  'Frog_General_Xenbase_Database_url',
  'HGNC_GENE_NAMES_CALL_CACHE',
  'ANIMAL_MODEL_IDS_VIA_AUTOCOMPLETE_ALLIANCE_GENOME_CACHE',
  'Ensembl Gene Id',
  'HGNC_ID',
  'Rat Gene Identifier',
  'Mouse Gene Identifier',
  'Zebrafish Gene Identifier',
  'Entrez Gene Id',
  'Gene Summary',
  'HPO_NCBI_GENE_ID',
  'HPO_GENE_CALL_CACHE',
  'ZEBRAFISH_SUMMARY_ALLIANCE_GENOME_CACHE',
  'MOUSE_SUMMARY_ALLIANCE_GENOME_CACHE',
  'OMIM',
  'HPO',
  'Mouse_Alliance_Genome_Automated_Summary',
  'Mouse_Alliance_Genome_MGI_Summary',
  'Zebrafish_Alliance_Genome_Automated_Summary',
  'Zebrafish_Alliance_Genome_ZFIN_Summary',
  'Mouse_Mouse_Genome_Database_url',
  'Zebrafish_Zebrafish_Information_Network_url',
  'RAT_SUMMARY_ALLIANCE_GENOME_CACHE',
  'Rat_Alliance_Genome_Automated_Summary',
  'Rat_Alliance_Genome_RGD_Summary',
  'Rat_Rat_Genome_Database_url',
  'COSMIC_gene_url',
  'Mouse_Alliance_Genome_Models',
  'Zebrafish_Alliance_Genome_Models',
  'Rat_Alliance_Genome_Models',
  'NCBI_gene_url',
  'gnomAD_gene_url',
  'Mouse_Alliance_Genome_url',
  'OMIM_gene_search_url',
  'HPO_gene_search_url',
  'ClinGen_gene_url',
  'C-Elegens Gene Identifier',
  'C-Elegens_Alliance_Genome_Automated_Summary',
  'C-Elegens_Alliance_Genome_WB_Summary',
  'C-Elegens_Alliance_Genome_Models',
  'Rat_Alliance_Genome_url',
  'Human_Alliance_Genome_url',
  'Zebrafish_Alliance_Genome_url',
  'C-Elegens_Alliance_Genome_url',
  'C-Elegens_Worm_Base_url',
  'GTEx_Human_Gene_Expression_url',
  'Human_Protein_Atlas_Protein_Gene_Search_url',
  'Pharos_Target_url'
],
}


function getAnalysisGenomicUnits(genomicUnits) {
  function getHgvsVariants(variants) {
    return variants.flatMap( variant => [variant.hgvs_variant && { 'hgvs_variant': variant.hgvs_variant}]);
  }
  return genomicUnits.flatMap( unit => ('variants' in unit ? [{'gene': unit['gene'] }, ...getHgvsVariants(unit['variants'])]: unit['gene']))
}

function compareManifestEntry(dataset, entry, other) {
    if( ![entry, other].every(item => dataset in item) ) {
        return false;
    }
    
    return entry?.[dataset]['data_source'] == other?.[dataset]['data_source']&& 
        entry?.[dataset]['version']== other?.[dataset]['version']
}

datasets = new Set()

try {

//   const analyses = db.analyses.find({'name': 'CCTS_Case_1'});
  const analyses = db.analyses.find();

//   var incCheck = 0;

  analyses.forEach(element => {
    // incCheck +=1

    // if (incCheck >50) {
    //     return;
    // }
    if( 'manifest' in element) {
        // element['manifest'].forEach(originalEntry => {
        //     Object.keys(originalEntry).forEach( datasetname => datasets.add(datasetname))
        // })

        const omic_units = []
        for (unit of element['genomic_units']) {
            if ('gene' in unit) {
                omic_units.push({'type': 'gene', 'unit': unit['gene']})
            }
            
            if ('variants' in unit) {
                for (variant of unit['variants']) {
                    omic_units.push({'type': 'hgvs_variant', 'unit': variant['hgvs_variant']})
                }       
            }
        }

        const original_manifest = element['manifest']
        const new_manifest = []
        for( unit of omic_units) {
            const unitsManifest = {
                'unit': unit['unit'],
                'manifest': []
            }

            for (originalEntry of original_manifest) {
                const datasetName = Object.keys(originalEntry)
                const name = datasetName[0]
                if(datasets_by_type[unit['type']].includes(...datasetName)) {
                    if (!unitsManifest['manifest'].some( migratedEntry => compareManifestEntry(name, migratedEntry, originalEntry) )) {
                        if(unitsManifest['manifest'].some( migratedEntry => name in migratedEntry) ) {
                            // print(['DUPLICATE', unit['type'], unit['unit'], transcriptDataset.includes(name), name, originalEntry[name]['data_source'], originalEntry[name]['version']].join(','))
                            continue
                        }
                        const findQuery = {}
                        if( transcriptDataset.includes(name) ) {
                            findQuery[unit['type']] = unit['unit']
                            findQuery[`transcripts.annotations.${name}`] = { $exists: true }
                            findQuery[`transcripts.annotations.${name}.data_source`] = originalEntry[name]['data_source']
                            findQuery[`transcripts.annotations.${name}.version`] = originalEntry[name]['version']
                        } else {
                            findQuery[unit['type']] = unit['unit']
                            findQuery[`annotations.${name}`] = { $exists: true }
                            findQuery[`annotations.${name}.data_source`] = originalEntry[name]['data_source']
                            findQuery[`annotations.${name}.version`] = originalEntry[name]['version']
                        }

                        const annotationCount = db.genomic_units.countDocuments(findQuery)
                        if( annotationCount > 0) {
                            // print(['SAVED', unit['type'], unit['unit'], transcriptDataset.includes(name), name, originalEntry[name]['data_source'], originalEntry[name]['version']].join(','))
                            unitsManifest['manifest'].push(originalEntry)
                        } else {
                            // print(['MISSING', unit['type'], unit['unit'], transcriptDataset.includes(name), name, originalEntry[name]['data_source'], originalEntry[name]['version']].join(','))
                        }
                    }
                }
            }
            new_manifest.push(unitsManifest)
        }

        new_manifest.map((originalEntry => {
            print({'analysis': element['name'], 'unit': originalEntry['unit'], 'amount': originalEntry['manifest'].length})
            // print(originalEntry['manifest'])
        }))

        element['manifest'] = new_manifest

        db.analyses.updateOne(
            {'_id': element._id},
            {$set: element}
        );
    }
  });

//   print(datasets)
} catch (err) {
  console.log(err.stack);
  console.log(usage);
  quit(1);
}
