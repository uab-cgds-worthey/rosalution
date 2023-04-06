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
import SectionImage from '@/components/SectionImage.vue';

import NotificationDialog from '@/components/Dialogs/NotificationDialog.vue';

import inputDialog from '@/inputDialog.js';
import notificationDialog from '@/notificationDialog.js';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';

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
      },
    },
  });
}

describe('AnnotationView', () => {
  let wrapper;
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

    mockAnnotations = sandbox.stub(Annotations, 'getAnnotations');
    mockAnnotations.returns(mockAnnotationsForCPAM0002);

    mockGenomicUnits = sandbox.stub(Analyses, 'getGenomicUnits');
    mockGenomicUnits.returns(mockGenomicUnitsForCPAM0002);

    mockSummaryByName = sandbox.stub(Analyses, 'getSummaryByName');
    mockSummaryByName.returns(mockSummaryByNameForCPAM0002);
    
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
    expect(sections.length).to.equal(7);
  });

  it('renders each section with an Id to be used for an achor', () => {
    const sections = wrapper.findAllComponents(AnnotationSection);
    sections.forEach((section) => {
      expect(section.attributes('id')).to.not.be.empty;
    });
  });

  it('renders text datasets according to configuration', () => {
    const textDatasets = wrapper.findAllComponents(TextDataset);
    expect(textDatasets.length).to.equal(9);
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
      geneSectionHeader = geneSection.get('.annotations');
      linkoutElements = geneSectionHeader.findAll('a');
    });

    it('should render each header dataset', () => {
      expect(linkoutElements.length).to.equal(3);
    });

    it('should not render any linkouts if none provided', () => {
      const variantSection = wrapper.find('#Variant');
      const variantSectionHeader = variantSection.get('.annotations');
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
      it.only('accepts an image to be added as content', async () => {
        const newImageResult = {
          image_id: 'fake-image-id-1',
          section: 'Gene Homology/Multi-Sequence Alignment',
        }

        annotationAttachMock.returns(newImageResult);

        const annotationSection = wrapper.findComponent('[id=Gene_Homology]')

        // console.log(annotationSection)

        annotationSection.vm.$emit('attach-image', 'Gene Homology/Multi-Sequence Alignment', 'hgvs_variant');

        await wrapper.vm.$nextTick();

        const fakeImage = {data: 'path/to/fake/fakeImage.png'};

        inputDialog.confirmation(fakeImage);

        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        const reRenderedAnnotationSection = wrapper.findComponent('[id=Gene_Homology]');

        // console.log(wrapper.vm.annotations);

        const imageDatasetComponents = reRenderedAnnotationSection.findComponent(ImageDataset)

        // console.log(imageDatasetComponents.vm.value)
      });
    });

    describe('when an image section has an image', () => {
      it('allows user to remove image content with input dialog with confirmation', () => {

      });
    });
  });

  describe('Annotation image attachments', () => {
    describe('when an image section does not have an image', () => {
      it('accepts an image to be added as content', async () => {
        const newImageResult = {
          image_id: 'fake-image-id-1',
          section: 'Gene Homology/Multi-Sequence Alignment',
        };

        annotationAttachMock.returns(newImageResult);

        const annotationSection = wrapper.findComponent('[id=Gene_Homology]');

        annotationSection.vm.$emit('attach-image', 'Gene Homology/Multi-Sequence Alignment', 'hgvs_variant');

        await wrapper.vm.$nextTick();

        const fakeImage = {data: 'path/to/fake/fakeImage.png'};

        inputDialog.confirmation(fakeImage);

        // Needs to cycle through updating the props in the view and then additional
        // ticks for vuejs to reactively update the supplemental component
        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        const tinyImageDatasetComponents = wrapper.findAllComponents(TinyImageDataset);

        expect(tinyImageDatasetComponents.length).to.equal(1);
      });

      it('should display a notification if the image fails to upload', async () => {
        annotationAttachMock.throws('Something went wrong when attaching an image. Please seek help.');

        const annotationSection = wrapper.findComponent('[id=Gene_Homology]');
        annotationSection.vm.$emit('attach-image', 'Gene Homology/Multi-Sequence Alignment', 'hgvs_variant');

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
      beforeEach(() => {
        const imageAnnotation = {'file_id': 'fake-image-id-1', 'created_date': 'fake-date'};

        const annotationsWithNewEvidence = mockAnnotationsForCPAM0002;
        annotationsWithNewEvidence['Gene Homology/Multi-Sequence Alignment'] = [imageAnnotation];
        mockAnnotations.returns(annotationsWithNewEvidence);
        wrapper = getMountedComponent();
      });

      it('allows user to add an image when an image already exists', async () => {
        const newImageResult = {
          image_id: 'fake-image-id-2',
          section: 'Gene Homology/Multi-Sequence Alignment',
        };

        annotationAttachMock.returns(newImageResult);

        const annotationSection = wrapper.findComponent('[id=Gene_Homology]');

        annotationSection.vm.$emit('attach-image', 'Gene Homology/Multi-Sequence Alignment', 'hgvs_variant');

        await wrapper.vm.$nextTick();

        const fakeImage = {data: 'path/to/fake/fakeImage.png'};

        inputDialog.confirmation(fakeImage);

        // Needs to cycle through updating the props in the view and then additional
        // ticks for vuejs to reactively update the supplemental component
        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        const tinyImageDatasetComponents = wrapper.findAllComponents(TinyImageDataset);

        expect(tinyImageDatasetComponents.length).to.equal(2);
      });

      it('allows the user to update an existing image with another image', async () => {
        const newImageResult = {
          image_id: 'fake-image-id-2',
          section: 'Gene Homology/Multi-Sequence Alignment',
        };

        annotationUpdateMock.resolves(newImageResult);

        let tinyImageDatasetComponent = wrapper.findComponent(TinyImageDataset);

        expect(tinyImageDatasetComponent.exists()).to.be.true;

        tinyImageDatasetComponent.vm.$emit(
            'update-annotation-image',
            'fake-image-id-1',
            'Gene Homology/Multi-Sequence Alignment',
        );

        await wrapper.vm.$nextTick();

        const fakeImageForUpdate = {data: 'fakeImage.png'};
        inputDialog.confirmation(fakeImageForUpdate);

        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        tinyImageDatasetComponent = wrapper.findComponent(TinyImageDataset);

        expect(tinyImageDatasetComponent.vm.imageId).to.equal(newImageResult.image_id);
      });

      it('fails to update an existing image with a new image and notifies the user of the error', async () => {
        annotationUpdateMock.throws('Could not update the image annoation. Please seek help.');

        const tinyImageDatasetComponent = wrapper.findComponent(TinyImageDataset);

        tinyImageDatasetComponent.vm.$emit(
            'update-annotation-image',
            'fake-image-id-1',
            'Gene Homology/Multi-Sequence Alignment',
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
        const tinyImageDatasetComponent = wrapper.findComponent(TinyImageDataset);

        expect(tinyImageDatasetComponent.exists()).to.be.true;

        tinyImageDatasetComponent.vm.$emit(
            'update-annotation-image',
            'fake-image-id-1',
            'Gene Homology/Multi-Sequence Alignment',
        );

        await wrapper.vm.$nextTick();

        inputDialog.delete();

        await wrapper.vm.$nextTick();

        const confirmationDialog = wrapper.findComponent(NotificationDialog);
        expect(confirmationDialog.exists()).to.be.true;

        notificationDialog.confirmation();

        await wrapper.vm.$nextTick();
        await wrapper.vm.$nextTick();

        const tinyImageDatasetComponents = wrapper.findAllComponents(TinyImageDataset);

        expect(tinyImageDatasetComponents.length).to.equal(0);
      });

      it('should not remove an image if the remove dialogue was cancelled', async () => {
        annotationRemoveMock.throws('Failed to remove image. Please seek help.');

        const tinyImageDatasetComponent = wrapper.findComponent(TinyImageDataset);

        tinyImageDatasetComponent.vm.$emit(
            'update-annotation-image',
            'fake-image-id-1',
            'Gene Homology/Multi-Sequence Alignment',
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

  describe('Annotation image attachments', () => {
    describe('when an image section does not have an image', () => {
      it('accepts an image to be added as content', async () => {
        const newImageResult = {
          image_id: 'fake-image-id-1',
          section: 'Gene Homology/Multi-Sequence Alignment',
        };

        annotationAttachMock.returns(newImageResult);

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
      beforeEach(() => {
        const imageAnnotation = {'file_id': 'fake-image-id-1', 'created_date': 'fake-date'};

        const annotationsWithNewEvidence = mockAnnotationsForCPAM0002;
        annotationsWithNewEvidence['GeneHomology_Multi-SequenceAlignment'] = [imageAnnotation];
        mockAnnotations.returns(annotationsWithNewEvidence);
        wrapper = getMountedComponent();
      });

      it('allows user to add an image when an image already exists', async () => {
        const newImageResult = {
          image_id: 'fake-image-id-2',
          section: 'GeneHomology_Multi-SequenceAlignment',
        };

        annotationAttachMock.returns(newImageResult);

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
          image_id: 'fake-image-id-2',
          section: 'GeneHomology_Multi-SequenceAlignment',
        };

        annotationUpdateMock.resolves(newImageResult);

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

        expect(sectionImageComponent.vm.imageId).to.equal(newImageResult.image_id);
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
  'Gene Homology/Multi-Sequence Alignment': [],
};
