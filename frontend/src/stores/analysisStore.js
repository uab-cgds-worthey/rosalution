import {reactive} from 'vue';

import Analyses from '@/models/analyses.js';

export const analysisStore = reactive({
  analysis: {
    name: '',
    sections: [],
  },
  updatedContent: {},

  analysisName() {
    // console.log(`AnalysisStore:analysisName = ${this.analysis?.name}`)
    return this.analysis?.name;
  },

  latestStatus() {
    // console.log(`AnalysisStore:latestStatus = ${this.analysis?.latest_status || 'Preparation'}`)
    return this.analysis?.latest_status;
  },
  async getAnalysis(analysisName) {
    // console.log(`AnalysisStore::getAnalysis - FROM MODEL BEGIN`)
    this.analysis = await Analyses.getAnalysis(analysisName);
    // console.log(`AnalysisStore::getAnalysis - FROM MODEL END`)
  },

  async saveChanges() {
    const updatedSections = await Analyses.updateAnalysisSections(
        this.analysis.name,
        this.updatedContent,
    );
    this.analysis.sections.splice(0);
    this.analysis.sections.push(...updatedSections);
    this.updatedContent = {};
  },

  cancelChanges() {
    this.updatedContent = {};
  },

  async pushEvent(eventType) {
    const updatedAnalysis = await Analyses.pushAnalysisEvent(this.analysisName(), eventType);
    this.forceUpdate(updatedAnalysis);
  },

  async attachSectionImage(sectionName, field, attachment) {
    const updatedSectionField = await Analyses.attachSectionImage(
        this.analysis.name,
        sectionName,
        field,
        attachment.data,
    );

    const sectionWithReplacedField = this.replaceFieldInSection(sectionName, updatedSectionField);
    this.replaceAnalysisSection(sectionWithReplacedField);
  },

  async updateSectionImage(fileId, sectionName, field, attachment) {
    const updatedSectionField = await Analyses.updateSectionImage(
        this.analysis.name,
        sectionName,
        field,
        fileId,
        attachment.data,
    );

    const sectionWithReplacedField = this.replaceFieldInSection(sectionName, updatedSectionField);
    this.replaceAnalysisSection(sectionWithReplacedField);
  },

  async removeSectionImage(fileId, sectionName, field) {
    const updatedSectionField = await Analyses.removeSectionAttachment(this.analysis.name, sectionName, field, fileId);

    const sectionWithReplacedField = this.replaceFieldInSection(sectionName, updatedSectionField);
    this.replaceAnalysisSection(sectionWithReplacedField);
  },

  replaceFieldInSection(sectionName, updatedField) {
    const sectionToUpdate = this.analysis.sections.find((section) => {
      return section.header == sectionName;
    });

    const fieldToUpdate = sectionToUpdate.content.find((row) => {
      return row.field == updatedField['field'];
    });

    fieldToUpdate.value = updatedField.value;

    return sectionToUpdate;
  },

  replaceAnalysisSection(sectionToReplace) {
    const originalSectionIndex = this.analysis.sections.findIndex(
        (section) => section.header == sectionToReplace.header,
    );
    this.analysis.sections.splice(originalSectionIndex, 1, sectionToReplace);
  },

  async addAttachment(attachment) {
    const updatedAnalysisAttachments = await Analyses.attachSupportingEvidence(
        this.analysis.name,
        attachment,
    );
    this.analysis.supporting_evidence_files.splice(0);
    this.analysis.supporting_evidence_files.push(
        ...updatedAnalysisAttachments,
    );
  },

  async updateAttachment(updatedAttachment) {
    const updatedAnalysisAttachments = await Analyses.updateSupportingEvidence(
        this.analysis.name,
        updatedAttachment,
    );
    this.analysis.supporting_evidence_files.splice(0);
    this.analysis.supporting_evidence_files.push(
        ...updatedAnalysisAttachments,
    );
  },

  async removeAttachment(attachmentToDelete) {
    await Analyses.removeSupportingEvidence(
        this.analysis.name,
        attachmentToDelete.attachment_id,
    );
    const attachmentIndex = this.analysis.supporting_evidence_files.findIndex((attachment) => {
      return attachment.name == attachmentToDelete.name;
    });

    this.analysis.supporting_evidence_files.splice(attachmentIndex, 1);
  },

  forceUpdate(updatedAnalysis) {
    // console.log(`AnalysisStore:forceUpdate - CALLED`)
    this.analysis = {...this.analysis, ...updatedAnalysis};
  },
});
