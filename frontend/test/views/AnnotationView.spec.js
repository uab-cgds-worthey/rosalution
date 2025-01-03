import {expect, describe, it, beforeAll, afterAll, beforeEach} from 'vitest';
import {config, mount} from '@vue/test-utils';
import sinon from 'sinon';

import Analyses from '@/models/analyses.js';
import Annotations from '@/models/annotations.js';
import FileRequests from '@/fileRequests.js';

import AnnotationView from '@/views/AnnotationView.vue';
import AnnotationSection from '@/components/AnnotationView/AnnotationSection.vue';
import AnnotationViewHeader from '@/components/AnnotationView/AnnotationViewHeader.vue';
import TextDataset from '@/components/AnnotationView/TextDataset.vue';
import TagDataset from '@/components/AnnotationView/TagDataset.vue';
import SectionImage from '@/components/SectionImage.vue';

import NotificationDialog from '@/components/Dialogs/NotificationDialog.vue';
import inputDialog from '@/inputDialog.js';
import notificationDialog from '@/notificationDialog.js';

import {FontAwesomeIcon, FontAwesomeLayers} from '@fortawesome/vue-fontawesome';
import {RouterLink} from 'vue-router';

/**
 * Helper mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {analysis_name: 'CPAM0046'};
  const mockRoute = {
    params: {
      id: 1,
    },
  };
  return mount(AnnotationView, {
    props: {...defaultProps, ...props},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
        'font-awesome-layers': FontAwesomeLayers,
        'router-link': RouterLink,
      },
      mocks: {
        $route: mockRoute,
        $router: {
          push: sinon.spy(),
        },
      },
      stubs: {
        AnnotationViewHeader: true,
        FontAwesomeIcon: true,
        FontAwesomeLayers: true,
        RouterLink: true,
      },
    },
  });
}

describe('AnnotationView', () => {
  let wrapper;
  let mockRenderLayout;
  let mockAnnotations;
  let mockGenomicUnits;
  let mockSummaryByName;
  // Future Mock Analysis Annotation Rendering Configuration

  let annotationAttachMock;
  let annotationUpdateMock;
  let annotationRemoveMock;

  let getImageMock;

  let sandbox;

  beforeAll(() => {
    config.global.renderStubDefaultSlot = true;
    sandbox = sinon.createSandbox();

    global['history'] = {
      state: {
        gene: '',
        variant: '',
      },
    },

    mockAnnotations = sandbox.stub(Annotations, 'getAnnotations');
    mockAnnotations.returns(mockAnnotationsForCPAM0002);

    mockGenomicUnits = sandbox.stub(Analyses, 'getGenomicUnits');
    mockGenomicUnits.returns(mockGenomicUnitsForCPAM0002);

    mockSummaryByName = sandbox.stub(Analyses, 'getSummaryByName');
    mockSummaryByName.returns(mockSummaryByNameForCPAM0002);

    mockRenderLayout = sandbox.stub(Analyses, 'getAnnotationConfiguration');
    mockRenderLayout.returns(mockAnnotationRenderLayout);

    annotationAttachMock = sandbox.stub(Annotations, 'attachAnnotationImage');
    annotationUpdateMock = sandbox.stub(Annotations, 'updateAnnotationImage');
    annotationRemoveMock = sandbox.stub(Annotations, 'removeAnnotationImage');

    getImageMock = sandbox.stub(FileRequests, 'getImage');
    getImageMock.returns('data:image/jpeg;base64,/fake-data');

    wrapper = getMountedComponent();
  });

  afterAll(() => {
    config.global.renderStubDefaultSlot = false;
    mockAnnotations.restore();
  });

  it('contains a header with the analysis name', () => {
    const headerComponent = wrapper.findComponent(AnnotationViewHeader);
    expect(headerComponent.props('analysisName')).to.equal('CPAM0046');
  });

  it('renders expected number of sections ', () => {
    const sections = wrapper.findAllComponents(AnnotationSection);
    expect(sections.length).to.equal(17);
  });

  it('renders each section with an Id to be used for an achor', () => {
    const sections = wrapper.findAllComponents(AnnotationSection);
    sections.forEach((section) => {
      expect(section.attributes('id')).to.not.be.empty;
    });
  });

  it('renders text datasets according to configuration', () => {
    const textDatasets = wrapper.findAllComponents(TextDataset);
    expect(textDatasets.length).to.equal(12);
  });

  // Enable this test when tag datasets are added to the configuration
  it.skip('renders tag datasets according to configuration', () => {
    const textDatasets = wrapper.findAllComponents(TagDataset);
    expect(textDatasets.length).to.equal(1);
  });

  it('should update the active genomic units to render annotations for', () => {
    const headerComponent = wrapper.findComponent(AnnotationViewHeader);
    const previousCallCount = mockAnnotations.callCount;
    headerComponent.vm.$emit('changed', {gene: 'LMNA', variant: 'the-best-variant'});
    expect(mockAnnotations.callCount).to.equal(previousCallCount + 1);
    expect(mockAnnotations.calledWith('CPAM0002', 'LMNA', 'the-best-variant'));
  });

  describe('Section headers ought to render datasets according to configuration', () => {
    let geneSection;
    let geneSectionHeader;
    let linkoutElements;

    beforeAll(() => {
      geneSection = wrapper.find('#Gene');
      geneSectionHeader = geneSection.get('[data-test=header-datasets]');
      linkoutElements = geneSectionHeader.findAll('a');
    });

    it('should render each header dataset', () => {
      expect(linkoutElements.length).to.equal(4);
    });

    it('should not render any linkouts if none provided', () => {
      const variantSection = wrapper.find('#Causal_Variant');
      const variantSectionHeader = variantSection.get('[data-test=header-datasets]');
      const noLinkouteElements = variantSectionHeader.findAll('a');
      expect(noLinkouteElements.length).to.equal(0);
    });

    it('should render each linkout to open in a new tab', () => {
      linkoutElements.forEach((linkDomElement) => {
        expect(linkDomElement.attributes('target')).to.equal('_blank');
      });
    });

    it('should render each linkout with an href', () => {
      linkoutElements.forEach((linkDomElement) => {
        expect([
          'https://www.ncbi.nlm.nih.gov/gene?Db=gene&Cmd=DetailsSearch&Term=203547',
          'https://www.ncbi.nlm.nih.gov/gene?Db=gene&Cmd=DetailsSearch&Term=HGNC:22082',
          'https://www.ncbi.nlm.nih.gov/gene?Db=gene&Cmd=DetailsSearch&Term=ENSG00000160131',
        ]).to.include(linkDomElement.attributes('href'));
      });
    });
  });

  describe('Annotation image attachments', () => {
    describe('when an image section does not have an image', () => {
      it('accepts an image to be added as content', async () => {
        const newImageResult = {
          file_id: 'fake-image-id-1',
        };

        annotationAttachMock.returns([newImageResult]);

        const annotationSection = wrapper.findComponent('[id=Gene_Homology]');

        annotationSection.vm.$emit('attach-image', 'GeneHomology_Multi-SequenceAlignment', 'hgvs_variant');

        await wrapper.vm.$nextTick();

        const fakeImage = {data: 'path/to/fake/fakeImage.png'};

        inputDialog.confirmation(fakeImage);

        // Needs to cycle through updating the props in the view and then additional
        // ticks for vuejs to reactively update the supplemental component
        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        const sectionImageComponents = wrapper.findAllComponents(SectionImage);

        expect(sectionImageComponents.length).to.equal(1);
      });

      it('should display a notification if the image fails to upload', async () => {
        annotationAttachMock.throws('Something went wrong when attaching an image. Please seek help.');

        const annotationSection = wrapper.findComponent('[id=Gene_Homology]');
        annotationSection.vm.$emit('attach-image', 'GeneHomology_Multi-SequenceAlignment', 'hgvs_variant');

        await wrapper.vm.$nextTick();

        const fakeImage = {data: 'path/to/fake/fakeImage.png'};
        inputDialog.confirmation(fakeImage);

        // Needs to cycle through updating the props in the view and then additional
        // ticks for vuejs to reactively update the supplemental component
        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        notificationDialog.confirmation();

        await wrapper.vm.$nextTick();

        const failureNotificationDialog = wrapper.findComponent(NotificationDialog);
        expect(failureNotificationDialog.exists()).to.be.true;
      });
    });

    describe('when an image section has an image', () => {
      const initialImageAnnotation = {'file_id': 'fake-image-id-1', 'created_date': 'fake-date'};
      beforeEach(() => {
        const annotationsWithNewEvidence = mockAnnotationsForCPAM0002;
        annotationsWithNewEvidence['GeneHomology_Multi-SequenceAlignment'] = [initialImageAnnotation];
        mockAnnotations.returns(annotationsWithNewEvidence);
        wrapper = getMountedComponent();
      });

      it('allows user to add an image when an image already exists', async () => {
        const newImageResult = {
          file_id: 'fake-image-id-2',
          section: 'GeneHomology_Multi-SequenceAlignment',
        };

        annotationAttachMock.returns([initialImageAnnotation, newImageResult]);

        const annotationSection = wrapper.findComponent('[id=Gene_Homology]');

        annotationSection.vm.$emit('attach-image', 'GeneHomology_Multi-SequenceAlignment', 'hgvs_variant');

        await wrapper.vm.$nextTick();

        const fakeImage = {data: 'path/to/fake/fakeImage.png'};

        inputDialog.confirmation(fakeImage);

        // Needs to cycle through updating the props in the view and then additional
        // ticks for vuejs to reactively update the supplemental component
        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        const sectionImageComponents = wrapper.findAllComponents(SectionImage);

        expect(sectionImageComponents.length).to.equal(2);
      });

      it('allows the user to update an existing image with another image', async () => {
        const newImageResult = {
          file_id: 'fake-image-id-2',
          section: 'GeneHomology_Multi-SequenceAlignment',
        };

        annotationUpdateMock.resolves([newImageResult]);

        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        let sectionImageComponent = wrapper.findComponent(SectionImage);

        expect(sectionImageComponent.exists()).to.be.true;

        sectionImageComponent.vm.$emit(
            'update-annotation-image',
            'fake-image-id-1',
            'GeneHomology_Multi-SequenceAlignment',
            'hgvs_variant',
        );

        await wrapper.vm.$nextTick();

        const fakeImageForUpdate = {data: 'fakeImage.png'};
        inputDialog.confirmation(fakeImageForUpdate);

        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        sectionImageComponent = wrapper.findComponent(SectionImage);
        expect(sectionImageComponent.vm.imageId).to.equal(newImageResult.file_id);
      });

      it('fails to update an existing image with a new image and notifies the user of the error', async () => {
        annotationUpdateMock.throws('Could not update the image annoation. Please seek help.');

        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        const sectionImageComponent = wrapper.findComponent(SectionImage);

        sectionImageComponent.vm.$emit(
            'update-annotation-image',
            'fake-image-id-1',
            'GeneHomology_Multi-SequenceAlignment',
            'hgvs_variant',
        );

        await wrapper.vm.$nextTick();

        const fakeImageForUpdate = {data: 'fakeImage.png'};
        inputDialog.confirmation(fakeImageForUpdate);

        await wrapper.vm.$nextTick();

        notificationDialog.confirmation();

        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        const failureNotificationDialog = wrapper.findComponent(NotificationDialog);
        expect(failureNotificationDialog.exists()).to.be.true;
      });

      it('allows the user to remove an image annotation with input dialog with confirmation', async () => {
        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        const sectionImageComponent = wrapper.findComponent(SectionImage);

        expect(sectionImageComponent.exists()).to.be.true;

        sectionImageComponent.vm.$emit(
            'update-annotation-image',
            'fake-image-id-1',
            'GeneHomology_Multi-SequenceAlignment',
            'hgvs_variant',
        );

        await wrapper.vm.$nextTick();

        inputDialog.delete();

        await wrapper.vm.$nextTick();

        const confirmationDialog = wrapper.findComponent(NotificationDialog);
        expect(confirmationDialog.exists()).to.be.true;

        notificationDialog.confirmation();

        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        const sectionImageComponents = wrapper.findAllComponents(SectionImage);

        expect(sectionImageComponents.length).to.equal(0);
      });

      it('should not remove an image if the remove dialogue was cancelled', async () => {
        annotationRemoveMock.throws('Failed to remove image. Please seek help.');

        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        const sectionImageComponent = wrapper.findComponent(SectionImage);

        sectionImageComponent.vm.$emit(
            'update-annotation-image',
            'fake-image-id-1',
            'GeneHomology_Multi-SequenceAlignment',
            'hgvs_variant',
        );

        await wrapper.vm.$nextTick();

        inputDialog.delete();

        await wrapper.vm.$nextTick();

        notificationDialog.confirmation();

        await wrapper.vm.$nextTick();

        const failureNotificationDialog = wrapper.findComponent(NotificationDialog);
        expect(failureNotificationDialog.exists()).to.be.true;
      });
    });
  });
});

const mockGenomicUnitsForCPAM0002 = {
  'genes': {
    'FOXG1': [
      'NM_005249.5:c.924G>A(p.Trp308Ter)',
      'NM_005249.5:c.256dup(p.Gln86fs)'],
  }, 'variants': [
    'NM_005249.5:c.924G>A(p.Trp308Ter)',
    'NM_005249.5:c.256dup(p.Gln86fs)',
  ],
};

const mockSummaryByNameForCPAM0002 = {
  'name': 'CPAM0002',
  'description': 'Vacuolar myopathy with autophagy, X-linked vacuolar myopathy with autophagy',
  'nominated_by': 'Dr. Person One',
  'latest_status': 'Approved',
  'created_date': '2022-10-09',
  'last_modified_date': '2022-10-09',
  'monday_com': 'https://monday.com',
  'phenotips_com': 'https://phenotips.com',
};

const mockAnnotationsForCPAM0002 = {
  'Entrez Gene Id': 203547,
  'Ensembl Gene Id': 'ENSG00000160131',
  'HGNC_ID': 'HGNC:22082',
  'ClinGen_gene_url':
    'https://www.ncbi.nlm.nih.gov/gene?Db=gene&Cmd=DetailsSearch&Term=HGNC:22082',
  'NCBI_gene_url':
    'https://www.ncbi.nlm.nih.gov/gene?Db=gene&Cmd=DetailsSearch&Term=203547',
  'gnomAD_gene_url':
    'https://www.ncbi.nlm.nih.gov/gene?Db=gene&Cmd=DetailsSearch&Term=ENSG00000160131',
  'COSMIC_gene_url': 'https://www.ncbi.nlm.nih.gov/gene?Db=gene&Cmd=DetailsSearch&Term=ENSG00000160131',
  'OMIM': ['Myopathy, X-linked, With Excessive Autophagy'],
  'HPO': [
    'HP:0001270: Motor delay',
    'HP:0001419: X-linked recessive inheritance',
    'HP:0001371: Flexion contracture',
    'HP:0003391: Gowers sign',
    'HP:0008994: Proximal muscle weakness in lower limbs',
    'HP:0002650: Scoliosis',
    'HP:0003551: Difficulty climbing stairs',
    'HP:0002093: Respiratory insufficiency',
    'HP:0003198: Myopathy',
    'HP:0009046: Difficulty running',
    'HP:0003202: Skeletal muscle atrophy',
    'HP:0001319: Neonatal hypotonia',
    'HP:0003236: Elevated circulating creatine kinase concentration',
    'HP:0002486: Myotonia',
    'HP:0007941: Limited extraocular movements',
  ],
  'Gene Summary':
    'This gene encodes a chaperone for assembly of lysosomal vacuolar ATPase.[provided by RefSeq, Jul 2012]',
  'Rat Gene Identifier': 'RGD:1566155',
  'Mouse Gene Identifier': 'MGI:1914298',
  'Model Systems - Mouse - Automated':
    ` Predicted to be involved in vacuolar proton-transporting V-type ATPase complex assembly. Predicted to be located
    in lysosome. Predicted to be active in endoplasmic reticulum membrane. Human ortholog(s) of this gene implicated in
    X-linked myopathy with excessive autophagy. Orthologous to human VMA21 (vacuolar ATPase assembly factor VMA21).`,
  'Zebrafish Gene Identifier': 'ZFIN:ZDB-GENE-081104-272',
  'Model Systems - Zebrafish - Automated':
    `Predicted to be involved in vacuolar proton-transporting V-type ATPase complex assembly. Predicted to be located
    in ER to Golgi transport vesicle membrane; endoplasmic reticulum membrane; and endoplasmic reticulum-Golgi
    intermediate compartment membrane. Predicted to be integral component of membrane. Human ortholog(s) of this gene
    implicated in X-linked myopathy with excessive autophagy. Orthologous to human VMA21 (vacuolar ATPase assembly
    factor VMA21).`,
  'C-Elegens Gene Identifier': 'WB:WBGene00303105',
  'Model Systems - C-Elegens - Automated':
    `Predicted to be involved in vacuolar proton-transporting V-type ATPase complex assembly. Predicted to be located
    in ER to Golgi transport vesicle membrane; endoplasmic reticulum membrane; and endoplasmic reticulum-Golgi
    intermediate compartment membrane. Predicted to be integral component of membrane. Human ortholog(s) of this gene
    implicated in X-linked myopathy with excessive autophagy. Orthologous to human VMA21 (vacuolar ATPase assembly
      factor VMA21).`,
  'Model Systems - Rat':
    `Predicted to be involved in vacuolar proton-transporting V-type ATPase complex assembly. Predicted to be located
    in lysosome. Predicted to be active in endoplasmic reticulum membrane. Human ortholog(s) of this gene implicated in
    X-linked myopathy with excessive autophagy. Orthologous to human VMA21 (vacuolar ATPase assembly factor VMA21);
    INTERACTS WITH 2,3,7,8-Tetrachlorodibenzofuran; 3-chloropropane-1,2-diol; bisphenol A.`,
  'OMIM_gene_search_url':
    'https://www.omim.org/search?index=entry&start=1&sort=score+desc%2C+prefix_sort+desc&search=VMA21',
  'HPO_gene_search_url':
    'https://hpo.jax.org/app/browse/search?q=VMA21&navFilter=all',
  'CADD': 33,
  'ClinVar_Variantion_Id': '581244',
  'ClinVar_variant_url': 'https://www.ncbi.nlm.nih.gov/clinvar/variation/581244',
  'transcripts': [{
    'Polyphen Prediction': 'possibly_damaging',
    'Impact': 'MODERATE',
    'transcript_id': 'NM_001017980.4',
    'SIFT Prediction': 'deleterious',
    'Polyphen Score': 0.597,
    'SIFT Score': 0.02,
    'Consequences': ['missense_variant', 'splice_region_variant'],
  }, {
    'transcript_id': 'NM_001363810.1',
    'Impact': 'MODERATE',
    'SIFT Prediction': 'deleterious',
    'Polyphen Score': 0.998,
    'SIFT Score': 0.01,
    'Consequences': ['missense_variant', 'splice_region_variant'],
    'Polyphen Prediction': 'probably_damaging',
  }],
};

const mockAnnotationRenderLayout =  [{
  'type': 'section', 'class': '', 'header': 'gene', 'anchor': 'Gene', 'header_datasets': [{
    'dataset': 'ClinGen_gene_url', 'type': 'icon-linkout-dataset',
    'props': {'imageFilename': 'logo-clin-gen.svg', 'altText': 'Clinical Genomic Resource Gene Linkout'},
  }, {
    'dataset': 'NCBI_gene_url', 'type': 'icon-linkout-dataset', 'props': {
      'imageFilename': 'ncbi-logo.png',
      'altText': 'National Center for Biotechnology Information Gene Linkout',
    },
  }, {
    'dataset': 'COSMIC_gene_url', 'type': 'icon-linkout-dataset', 'props': {
      'imageFilename': 'cosmic_logo.png', 'altText': 'Catalogue Of Somatic Mutations In Cancer, COSMIC',
    },
  }, {
    'dataset': 'gnomAD_gene_url', 'type': 'icon-linkout-dataset', 'props': {
      'imageFilename': 'gnomad-logo.png',
      'altText': 'Genome Aggregation Database (gnomAD) for variants from Broad Institute',
    },
  }], 'rows': [{'class': '', 'datasets': [{'dataset': 'Gene Summary', 'type': 'text-dataset', 'props': {}}]}, {
    'class': '', 'datasets': [{
      'dataset': 'OMIM', 'type': 'text-dataset', 'linkout_dataset': 'OMIM_gene_search_url',
      'props': {'label': 'OMIM'},
    }],
  }, {
    'class': '', 'datasets': [{
      'dataset': 'HPO', 'type': 'tag-dataset', 'linkout_dataset': 'HPO_gene_search_url',
      'props': {'label': 'HPO'},
    }],
  }],
}, {
  'type': 'section', 'class': '', 'header': 'variant', 'anchor': 'Variant', 'header_datasets': [{
    'dataset': 'gnomAD_variant_url', 'type': 'icon-linkout-dataset', 'props': {
      'imageFilename': 'gnomad-logo.png',
      'altText': 'Genome Aggregation Database (gnomAD) for genes from Broad Institute',
    },
  }], 'rows': [{
    'class': 'fill-horizontal', 'datasets': [{
      'dataset': 'CADD', 'type': 'score-dataset', 'props': {
        'label': 'CADD', 'minimum': 0, 'maximum': 99, 'bounds': {'lowerBound': 9, 'upperBound': 19},
        'cutoff': 1,
      },
    }, {
      'dataset': 'DITTO', 'type': 'score-dataset', 'props': {
        'label': 'DITTO', 'minimum': 0, 'maximum': 1, 'bounds': {'lowerBound': 0.5, 'upperBound': 0.79},
        'cutoff': 1,
      },
    }, {
      'dataset': 'REVEL', 'type': 'score-dataset', 'props': {
        'label': 'REVEL', 'minimum': 0, 'maximum': 1, 'bounds': {'lowerBound': 0.5, 'upperBound': 0.79},
        'cutoff': 1,
      },
    }, {
      'dataset': 'alphamissense_pathogenicity', 'type': 'score-dataset', 'props': {
        'label': 'AlphaMissense Score', 'minimum': 0, 'maximum': 1,
        'bounds': {'lowerBound': 0.34, 'upperBound': 0.564}, 'cutoff': 1,
      },
    }, {
      'dataset': 'alphamissense_classification', 'type': 'set-dataset', 'props': {
        'label': 'AlphaMissense Pathogenicity',
        'set': [{'value': 'likely_benign', 'classification': 'Likely Benign', 'colour': 'Blue'},
          {'value': 'ambiguous', 'classification': 'Ambiguous', 'colour': 'Yellow'},
          {'value': 'likely_pathogenic', 'classification': 'Likely Pathogenic', 'colour': 'Red'}],
      },
    }],
  }, {
    'datasets': [{
      'dataset': 'ClinVar', 'type': 'clinvar-dataset', 'linkout_dataset': 'ClinVar_variant_url',
      'props': {'label': 'ClinVar'},
    }],
  }, {'datasets': [{'dataset': 'transcripts', 'genomicType': 'hgvs_variant', 'type': 'transcript-datasets'}]}],
}, {
  'type': 'section', 'class': '', 'header': 'Chromosomal Localization', 'anchor': 'Chromosomal_Localization',
  'header_datasets': [],
  'props': {'attachmentDataset': 'Chromosomal_Localization', 'genomicAttachmentType': 'hgvs_variant'}, 'rows': [{
    'class': '', 'datasets': [{
      'dataset': 'Chromosomal_Localization', 'genomicType': 'hgvs_variant', 'type': 'images-dataset',
    }],
  }],
}, {
  'type': 'section', 'class': '', 'header': 'Secondary Structure', 'anchor': 'Secondary_Structure',
  'header_datasets': [],
  'props': {'attachmentDataset': 'Secondary_Structure', 'genomicAttachmentType': 'hgvs_variant'}, 'rows': [{
    'class': '',
    'datasets': [{'dataset': 'Secondary_Structure', 'genomicType': 'hgvs_variant', 'type': 'images-dataset'}],
  }],
}, {
  'type': 'section', 'class': '', 'header': 'Causal Variant In This Locus (ClinVar)', 'anchor': 'Causal_Variant',
  'header_datasets': [],
  'props': {'attachmentDataset': 'Causal_Variant_In_This_Locus_ClinVar',
    'genomicAttachmentType': 'hgvs_variant'}, 'rows': [{
    'class': '', 'datasets': [{
      'dataset': 'Causal_Variant_In_This_Locus_ClinVar', 'genomicType': 'hgvs_variant',
      'type': 'images-dataset',
    }],
  }],
}, {
  'type': 'section', 'class': '', 'header': 'Variant Publications', 'anchor': 'Variant_Publications',
  'header_datasets': [],
  'props': {'attachmentDataset': 'Variant_Publications', 'genomicAttachmentType': 'hgvs_variant'}, 'rows': [{
    'class': '',
    'datasets': [{'dataset': 'Variant_Publications', 'genomicType': 'hgvs_variant', 'type': 'images-dataset'}],
  }],
}, {
  'type': 'section', 'class': '', 'header': 'Gene Homology/Multi-Sequence Alignment', 'anchor': 'Gene_Homology',
  'header_datasets': [],
  'props': {'attachmentDataset': 'GeneHomology_Multi-SequenceAlignment',
    'genomicAttachmentType': 'hgvs_variant'}, 'rows': [{
    'class': '', 'datasets': [{
      'dataset': 'GeneHomology_Multi-SequenceAlignment', 'genomicType': 'hgvs_variant',
      'type': 'images-dataset',
    }],
  }],
}, {
  'type': 'section', 'class': '', 'header': 'Human Gene Expression', 'anchor': 'Human_Gene_Expression',
  'header_datasets': [{
    'dataset': 'GTEx_Human_Gene_Expression_url', 'type': 'icon-linkout-dataset',
    'props': {'imageFilename': 'gtex_logo.png', 'altText': 'GTEx Human Gene Expression URL'},
  }], 'props': {'attachmentDataset': 'Human_Gene_Expression', 'genomicAttachmentType': 'gene'}, 'rows': [{
    'class': '',
    'datasets': [{'dataset': 'Human_Gene_Expression', 'genomicType': 'gene', 'type': 'images-dataset'}],
  }],
}, {
  'type': 'section', 'class': '', 'header': 'Human Gene versus Protein Expression Profile',
  'anchor': 'Human_Gene_versus_Protein_Expression', 'header_datasets': [{
    'dataset': 'Human_Protein_Atlas_Protein_Gene_Search_url', 'type': 'icon-linkout-dataset',
    'props': {'imageFilename': 'protein_atlas_icon.png', 'altText': 'Protein Atlas Gene Search URL'},
  }],
  'props': {'attachmentDataset': 'Human_Gene_versus_Protein_Expression_Profile',
    'genomicAttachmentType': 'gene'}, 'rows': [{
    'class': '', 'datasets': [{
      'dataset': 'Human_Gene_versus_Protein_Expression_Profile', 'genomicType': 'gene',
      'type': 'images-dataset',
    }],
  }],
}, {
  'type': 'section', 'class': '', 'header': 'Model System Expression Profiles', 'anchor': 'Expression_Profiles',
  'header_datasets': [{
    'dataset': 'CoSIA_url', 'type': 'icon-linkout-dataset', 'props': {
      'imageFilename': 'CoSIA_logo.png', 'altText': 'COSIA_LINKOUT',
      'value': 'https://lasseignelab.shinyapps.io/CoSIA/',
    },
  }, {
    'dataset': 'Frog_General_Xenbase_Database_url', 'type': 'icon-linkout-dataset',
    'props': {'imageFilename': 'xenbase_logo.png', 'altText': 'Xenbase Xenopus General Gene Linkout'},
  }], 'props': {'attachmentDataset': 'Model_System_Expression_Profiles', 'genomicAttachmentType': 'gene'},
  'rows': [{
    'class': '', 'datasets': [{
      'dataset': 'Model_System_Expression_Profiles', 'genomicType': 'gene', 'type': 'images-dataset',
    }],
  }],
}, {
  'type': 'section', 'class': '', 'header': 'Orthology', 'anchor': 'Orthology', 'header_datasets': [{
    'dataset': 'Human_Alliance_Genome_url', 'type': 'icon-linkout-dataset',
    'props': {'imageFilename': 'alliance-genome-logo.png', 'altText': 'Human Alliance Genome Linkout'},
  }], 'props': {'attachmentDataset': 'Orthology', 'genomicAttachmentType': 'gene'},
  'rows': [{'class': '', 'datasets': [{'dataset': 'Orthology', 'genomicType': 'gene', 'type': 'images-dataset'}]}],
}, {
  'type': 'section', 'class': '', 'header': 'Rattus norvegicus (Rat) Model System',
  'anchor': 'Rattus_norvegicus_Model_System', 'header_datasets': [{
    'dataset': 'Rat_Alliance_Genome_url', 'type': 'icon-linkout-dataset',
    'props': {'imageFilename': 'alliance-genome-logo.png', 'altText': 'Alliance Genome Linkout'},
  }, {
    'dataset': 'Rat_Rat_Genome_Database_url', 'type': 'icon-linkout-dataset',
    'props': {'imageFilename': 'rat-dataset-logo.png', 'altText': 'Rat Genome Database Linkout'},
  }], 'rows': [{
    'class': '', 'datasets': [{
      'dataset': 'Rat_Alliance_Genome_Automated_Summary', 'type': 'text-dataset',
      'props': {'label': 'AG Summary'},
    }, {
      'dataset': 'Rat_Alliance_Genome_RGD_Summary', 'type': 'text-dataset', 'props': {'label': 'RGD Summary'},
    }, {'dataset': 'Rat_Alliance_Genome_Models', 'type': 'card-dataset'}],
  }],
}, {
  'type': 'section', 'class': '', 'header': 'Mus musculus (Mouse) Model System',
  'anchor': 'Mus_musculus_Model_System', 'header_datasets': [{
    'dataset': 'Mouse_Alliance_Genome_url', 'type': 'icon-linkout-dataset',
    'props': {'imageFilename': 'alliance-genome-logo.png', 'altText': 'Alliance Genome Linkout'},
  }, {
    'dataset': 'Mouse_Mouse_Genome_Database_url', 'type': 'icon-linkout-dataset',
    'props': {'imageFilename': 'mouse-dataset-logo.png', 'altText': 'Mouse Genome Informatics Linkout'},
  }], 'rows': [{
    'class': '', 'datasets': [{
      'dataset': 'Mouse_Alliance_Genome_Automated_Summary', 'type': 'text-dataset',
      'props': {'label': 'AG Summary'},
    }, {
      'dataset': 'Mouse_Alliance_Genome_MGI_Summary', 'type': 'text-dataset',
      'props': {'label': 'MGI Summary'},
    }, {'dataset': 'Mouse_Alliance_Genome_Models', 'type': 'card-dataset'}],
  }],
}, {
  'type': 'section', 'class': '', 'header': 'Danio rerio (Zebrafish) Model System',
  'anchor': 'Danio_rerio_Model_System', 'header_datasets': [{
    'dataset': 'Zebrafish_Alliance_Genome_url', 'type': 'icon-linkout-dataset',
    'props': {'imageFilename': 'alliance-genome-logo.png', 'altText': 'Alliance Genome Linkout'},
  }, {
    'dataset': 'Zebrafish_Zebrafish_Information_Network_url', 'type': 'icon-linkout-dataset', 'props': {
      'imageFilename': 'zebrafish-dataset-logo.png', 'altText': 'Zebrafish Information Network Linkout',
    },
  }], 'rows': [{
    'class': '', 'datasets': [{
      'dataset': 'Zebrafish_Alliance_Genome_Automated_Summary', 'type': 'text-dataset',
      'props': {'label': 'AG Summary'},
    }, {
      'dataset': 'Zebrafish_Alliance_Genome_ZFIN_Summary', 'type': 'text-dataset',
      'props': {'label': 'ZFIN Summary'},
    }, {'dataset': 'Zebrafish_Alliance_Genome_Models', 'type': 'card-dataset'}],
  }],
}, {
  'type': 'section', 'class': '', 'header': 'C. elegans (Roundworm) Model System',
  'anchor': 'C_elegans_Model_System', 'header_datasets': [{
    'dataset': 'C-Elegens_Alliance_Genome_url', 'type': 'icon-linkout-dataset',
    'props': {'imageFilename': 'alliance-genome-logo.png', 'altText': 'Alliance Genome Linkout'},
  }, {
    'dataset': 'C-Elegens_Worm_Base_url', 'type': 'icon-linkout-dataset',
    'props': {'imageFilename': 'c-elegens-dataset-logo.png', 'altText': 'WormBase Linkout'},
  }], 'rows': [{
    'class': '', 'datasets': [{
      'dataset': 'C-Elegens_Alliance_Genome_Automated_Summary', 'type': 'text-dataset',
      'props': {'label': 'AG Summary'},
    }, {
      'dataset': 'C-Elegens_Alliance_Genome_WB_Summary', 'type': 'text-dataset',
      'props': {'label': 'WB Summary'},
    }, {'dataset': 'C-Elegens_Alliance_Genome_Models', 'type': 'card-dataset'}],
  }],
}, {
  'type': 'section', 'class': '', 'header': 'Modelability', 'anchor': 'Modelability', 'header_datasets': [{
    'dataset': 'Gentar_url', 'type': 'icon-linkout-dataset', 'props': {
      'imageFilename': 'gentar_logo.png', 'altText': 'Gentar URL for Modelability',
      'value': 'https://www.gentar.org/',
    },
  }], 'props': {'attachmentDataset': 'Modelability', 'genomicAttachmentType': 'gene'}, 'rows': [{
    'class': '', 'datasets': [{'dataset': 'Modelability', 'genomicType': 'gene', 'type': 'images-dataset'}],
  }],
}, {
  'type': 'section', 'class': '', 'header': 'Druggability', 'anchor': 'Druggability', 'header_datasets': [{
    'dataset': 'Pharos_Target_url', 'type': 'icon-linkout-dataset',
    'props': {'imageFilename': 'pharos_logo.png', 'altText': 'Druggability Target in Pharos'},
  }], 'props': {'attachmentDataset': 'Druggability', 'genomicAttachmentType': 'gene'}, 'rows': [{
    'class': '', 'datasets': [{'dataset': 'Druggability', 'genomicType': 'gene', 'type': 'images-dataset'}],
  }],
}];
