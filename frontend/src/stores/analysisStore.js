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
    Analyses.downloadAnalysisAttachment(attachmentToDownload.attachment_id, attachmentToDownload.name);
  },

  clear() {
    this.analysis = {
      name: '',
      sections: [],
    };

    this.updatedContent = {};
  },

  // -----------------------------------
  // Edit Operations
  // -----------------------------------

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
      sections: updatedSections,
    };

    this.forceUpdate(updated);
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

  // -----------------------------------
  // Section Images
  // -----------------------------------

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
      await Analyses.attachSectionAttachment(this.analysis.name, section, field, attachment);
    const sectionWithReplacedField = this.replaceFieldInSection(section, updatedSectionField);
    this.replaceAnalysisSection(sectionWithReplacedField);
  },

  async removeSectionAttachment(section, field, attachmentId) {
    const updatedSectionField =
      await Analyses.removeSectionAttachment(this.analysis.name, section, field, attachmentId);

    const sectionWithReplacedField = this.replaceFieldInSection(section, updatedSectionField);
    this.replaceAnalysisSection(sectionWithReplacedField);
  },

  // -----------------------------------
  // Section Attachments
  // -----------------------------------

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

  async addDiscussionPost(newPostContent, newPostAttachments=[]) {
    console.log(newPostContent);
    const discussions = await Analyses.postNewDiscussionPost(this.analysis.name, newPostContent, newPostAttachments);
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

  findDiscussionPost(postId) {
    const discussion = this.analysis.discussions.find((post) => {
      return post.post_id === postId;
    });

    return discussion;
  },

  async setAnalysisDiscussions(discussions) {
    this.analysis.discussions = discussions;
  },

  async addDiscussionReply(postId, newReplyContent) {
    const discussions = await Analyses.postNewDiscussionReply(this.analysis.name, postId, newReplyContent);
    this.analysis.discussions = discussions;
  },

  async editDiscussionReply(postId, replyId, replyContent) {
    const discussions = await Analyses.editDiscussionReply(this.analysis.name, postId, replyId, replyContent);
    this.analysis.discussions = discussions;
  },

  async deleteDiscussionReply(postId, replyId) {
    const discussions = await Analyses.deleteDiscussionReply(this.analysis.name, postId, replyId);
    this.analysis.discussions = discussions;
  },

  // -----------------------------------
  // Analysis Attachments
  // -----------------------------------

  async addAnalysisAttachment(attachment) {
    const updatedAnalysisAttachments = await Analyses.attachAnalysisAttachment(
        this.analysis.name,
        attachment,
    );
    this.analysis.attachments.splice(0);
    this.analysis.attachments.push(
        ...updatedAnalysisAttachments,
    );
  },

  async updateAnalysisAttachment(updatedAttachment) {
    const updatedAnalysisAttachments = await Analyses.updateAnalysisAttachment(
        this.analysis.name,
        updatedAttachment,
    );
    this.analysis.attachments.splice(0);
    this.analysis.attachments.push(
        ...updatedAnalysisAttachments,
    );
  },

  async removeAnalysisAttachment(attachmentToDelete) {
    await Analyses.removeAnalysisAttachment(
        this.analysis.name,
        attachmentToDelete.attachment_id,
    );
    const attachmentIndex = this.analysis.attachments.findIndex((attachment) => {
      return attachment.name == attachmentToDelete.name;
    });

    this.analysis.attachments.splice(attachmentIndex, 1);
  },

  // -----------------------------------
  // Analysis Operations
  // -----------------------------------

  forceUpdate(updatedAnalysis) {
    Object.assign(this.analysis, updatedAnalysis);
  },
});
