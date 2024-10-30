import {reactive} from 'vue';

import Analyses from '@/models/analyses.js';

export const analysisStore = reactive({
  analysis: {
    name: '',
    sections: [],
  },
  updatedContent: {},

  analysisName() {
    return this.analysis?.name;
  },

  latestStatus() {
    return this.analysis?.latest_status;
  },

  async getAnalysis(analysisName) {
    this.analysis = await Analyses.getAnalysis(analysisName);
  },

  downloadAttachment(attachmentToDownload) {
    Analyses.downloadSupportingEvidence(attachmentToDownload.attachment_id, attachmentToDownload.name);
  },

  /**
   * User Edit Operations
   */

  addUpdatedContent(header, field, value) {
    if (!(header in this.updatedContent)) {
      this.updatedContent[header] = {};
    }
  
    this.updatedContent[header][field] = value;
  },

  async saveChanges() {
    const updatedSections = await Analyses.updateAnalysisSections(
        this.analysis.name,
        this.updatedContent,
    );

    const updated = {
      sections: updatedSections
    }

    this.forceUpdate(updated)
    // this.analysis.sections.splice(0);
    // this.analysis.sections.push(...updatedSections);
    this.updatedContent = {};
  },

  cancelChanges() {
    this.updatedContent = {};
  },

  async pushEvent(eventType) {
    const updatedAnalysis = await Analyses.pushAnalysisEvent(this.analysisName(), eventType);
    this.forceUpdate(updatedAnalysis);
  },

  async attachThirdPartyLink(thirdParty, data) {
    const updatedAnalysis = await Analyses.attachThirdPartyLink(this.analysis.name, thirdParty, data);

    analysisStore.forceUpdate(updatedAnalysis);
  },

  /**
   * Section Images
   */

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

  /**
   * Section Attachments
   */

  async attachSectionAttachment(section, field, attachment) {
    const updatedSectionField =
      await Analyses.attachSectionSupportingEvidence(this.analysis.name, section, field, attachment);
    const sectionWithReplacedField = this.replaceFieldInSection(section, updatedSectionField);
    this.replaceAnalysisSection(sectionWithReplacedField);
  },

  async removeSectionAttachment(section, field, attachmentId) {
    const updatedSectionField =
      await Analyses.removeSectionAttachment(this.analysis.name, section, field, attachmentId);

    const sectionWithReplacedField = this.replaceFieldInSection(section, updatedSectionField);
    this.replaceAnalysisSection(sectionWithReplacedField);
  },

  /**
   * Section Operations
   */

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

  /**
   * Discussions
   */

  async addDiscussionPost(newPostContent) {
    const discussions = await Analyses.postNewDiscussionThread(this.analysis.name, newPostContent);
    this.analysis.discussions = discussions;
  },

  async editDiscussionPost(postId, postContent) {
    const discussions = await Analyses.editDiscussionThreadById(this.analysis.name, postId, postContent);
    this.analysis.discussions = discussions;
  },

  async deleteDiscussionPost(postId) {
    const discussions = await Analyses.deleteDiscussionThreadById(this.analysis.name, postId);
    this.analysis.discussions = discussions;
  },

  /**
   * Analysis Attachments
   */

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

  /**
   * Analysis Operations
   */

  forceUpdate(updatedAnalysis) {
    Object.assign(this.analysis, updatedAnalysis);
  },
});
