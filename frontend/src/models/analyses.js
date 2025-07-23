import {EventType} from '@/enums.js';
import Requests from '@/requests.js';

export default {

  EventType,

  async all() {
    const baseUrl = '/rosalution/api/';
    const urlQuery = 'analysis/summary';
    const analysesSummary = await Requests.get(baseUrl + urlQuery);
    return analysesSummary;
  },

  async getSummaryByName(analysisName) {
    const url = `/rosalution/api/analysis/${analysisName}/summary`;
    const analysisSummary = await Requests.get(url);
    return analysisSummary;
  },

  async getAnalysis(analysisName) {
    const baseUrl = '/rosalution/api/';
    const urlQuery = 'analysis/' + analysisName;
    const body = await Requests.get(baseUrl + urlQuery);
    return body;
  },

  async getGenomicUnits(analysisName) {
    const url = `/rosalution/api/analysis/${analysisName}/genomic_units`;
    const genomicUnits = await Requests.get(url);
    return genomicUnits;
  },

  async pushAnalysisEvent(analysisName, eventType) {
    const url = `/rosalution/api/analysis/${analysisName}/event/${eventType}`;
    return await Requests.put(url);
  },

  async getAnnotationConfiguration(analysisName) {
    return await Requests.get('/rosalution/api/render-layout/annotations');
  },

  /**
   * Requests to upload the JSON required for creating a new analysis in Rosalution
   * with a unique analysis name.
   * @param {File} file The JSON for creating the new Analysis
   * @return {Object} Returns the new complete analysis created within Rosalution
   */
  async importNewAnalysis(file) {
    const url = '/rosalution/api/analysis';

    const fileUploadFormData = {
      'phenotips_file': file,
    };

    return Requests.postForm(url, fileUploadFormData);
  },

  /**
   * Provides {@link updatedSections} of updated text fields within sections in
   * the analysis {@link analysisName}.
   * @param {string} analysisName The unique name of the Analysis to update
   * @param {Object} updatedSections The list of updated fields from within
   *                                 their corresponding sections
   * @return {Object[]} Array of all of the sections, including the updated
   * ones, within the Analysis
   */
  async updateAnalysisSections(analysisName, updatedSections) {
    const sectionsToUpdate = [];
    for (const [sectionName, field] of Object.entries(updatedSections)) {
      const analysisSection = {
        header: sectionName,
        content: [],
      };

      for ( const [fieldName, fieldValue] of Object.entries(field)) {
        analysisSection.content.push({
          fieldName: fieldName,
          value: fieldValue,
        });
      }
      sectionsToUpdate.push(analysisSection);
    }
    const url = `/rosalution/api/analysis/${analysisName}/sections/batch`;
    return await Requests.post(url, sectionsToUpdate);
  },

  async getSectionImage(fileId) {
    const url = `/rosalution/api/analysis/download/${fileId}`;
    return await Requests.getImage(url);
  },

  /**
   * Attaches {@link image} to {@link field} within {@link sectionName}
   * the analysis {@link analysisName}.
   * @param {string} analysisName The unique name of the analysis to update
   * @param {string} sectionName The name of the section within the analysis
   * @param {string} field The identifiying field within the section
   * @param {File}   image the image data to be uploaded
   * @return {Object} Returns the updated field with the image attachment id
   */
  async attachSectionImage(analysisName, sectionName, field, image) {
    const url = `/rosalution/api/analysis/${analysisName}/sections?row_type=image`;

    const section = {
      'header': sectionName,
      'content': [],
    };
    section.content.push({
      'fieldName': field,
    });
    const attachmentForm = {
      'upload_file': image,
      'updated_section': JSON.stringify(section),
    };

    const updatedAnalysisSections = await Requests.postForm(url, attachmentForm);

    return updatedAnalysisSections.find((section) => {
      return section.header == sectionName;
    })?.content.find((row) => {
      return row.field == field;
    });
  },

  async attachSectionAttachment(analysisName, sectionName, field, attachment) {
    let attachmentForm = null;
    let url = `/rosalution/api/analysis/${analysisName}/sections?row_type=`;

    const section = {
      'header': sectionName,
      'content': [],
    };

    if (attachment.type == 'file') {
      section.content.push({
        'fieldName': field,
      });

      attachmentForm = {
        'upload_file': attachment.data,
        'updated_section': JSON.stringify(section),
      };

      url += 'document';
    } else if ( attachment.type == 'link') {
      section.content.push({
        'fieldName': field,
        'linkName': attachment.name,
        'link': attachment.data,
      });

      attachmentForm = {
        'updated_section': JSON.stringify(section),
      };

      url += 'link';
    }

    if (null == attachmentForm) {
      throw new Error(`Attachment ${attachment} type is invalid.`);
    }

    const updatedSections = await Requests.postForm(url, attachmentForm);
    return updatedSections.find((section) => {
      return section.header == sectionName;
    })?.content.find((row) => {
      return row.field == field;
    });
  },

  async updateSectionImage(analysisName, sectionName, field, oldFileId, image) {
    const section = {
      'header': sectionName,
      'content': [],
    };
    section.content.push({
      'fieldName': field,
    });
    const attachmentForm = {
      'upload_file': image,
      'updated_section': JSON.stringify(section),
    };

    const url = `/rosalution/api/analysis/${analysisName}/sections/${oldFileId}?row_type=image`;

    const updatedAnalysisSections = await Requests.putForm(url, attachmentForm);

    return updatedAnalysisSections.find((section) => {
      return section.header == sectionName;
    })?.content.find((row) => {
      return row.field == field;
    });
  },

  async removeSectionAttachment(analysisName, sectionName, fieldName, oldSectionAttachmentId) {
    const url = `/rosalution/api/analysis/${analysisName}/sections/${oldSectionAttachmentId}`;
    const updatedSections = await Requests.delete(url);
    return updatedSections.find((section) => {
      return section.header == sectionName;
    })?.content.find((row) => {
      return row.field == fieldName;
    });
  },

  async attachAnalysisAttachment(analysisName, attachment) {
    const attachmentForm = {};
    const url = `/rosalution/api/analysis/${analysisName}/attachment`;

    if (!['file', 'link'].includes(attachment.type)) {
      throw new Error(`Attachment ${attachment} type is invalid.`);
    }

    const newAttachment = {
      'comments': attachment.comments ? attachment.comments : '  ', /** Required for now, inserting empty string */
    };

    if (attachment.type == 'file') {
      attachmentForm['upload_file'] = attachment.data;
    } else if ( attachment.type == 'link') {
      newAttachment['link_name'] = attachment.name;
      newAttachment['link'] = attachment.data;
    }

    attachmentForm['new_attachment'] = JSON.stringify(newAttachment);

    return await Requests.postForm(url, attachmentForm);
  },

  async updateAnalysisAttachment(analysisName, attachment) {
    const url = `/rosalution/api/analysis/${analysisName}/attachment/${attachment.attachment_id}`;

    const updatedAttachment = {
      name: attachment.name,
      ...('link' == attachment.type) && {data: attachment.data},
      comments: attachment.comments,
    };

    return await Requests.putForm(url, updatedAttachment);
  },

  async removeAnalysisAttachment(analysisName, attachmentId) {
    const url = `/rosalution/api/analysis/${analysisName}/attachment/${attachmentId}`;
    const success = await Requests.delete(url);
    return success;
  },

  async downloadAnalysisAttachment(attachmentId, attachmentFile) {
    const url = `/rosalution/api/analysis/download/${attachmentId}`;
    const fileData = {'filename': attachmentFile};
    return Requests.getDownload(url, fileData);
  },

  async attachThirdPartyLink(analysisName, linkType, link) {
    const url = `/rosalution/api/analysis/${analysisName}/attach/${linkType}`;
    const attachmentForm = {
      'link': link,
    };
    return await Requests.putForm(url, attachmentForm);
  },

  // Posting a Discussion Thread and corresponding attachments together
  async postNewDiscussionPost(analysisName, postContent, postAttachments=[]) {
    const url = `/rosalution/api/analysis/${analysisName}/discussions`;

    const attachmentsList = [];
    const fileList = [];
    for (const attachment of postAttachments) {
      const discussionAttachment = {
        ...attachment,
      };

      if (attachment.type == 'file' && !('attachment_id' in attachment) ) {
        fileList.push(attachment.data);
        delete discussionAttachment.data;
        discussionAttachment['name'] = attachment.data.name;
      }

      if ( 'comments' in attachment ) {
        delete discussionAttachment.comments;
      }

      attachmentsList.push(discussionAttachment);
    }

    const attachmentForm = {
      'discussion_content': postContent,
      'attachments': JSON.stringify({
        'attachments': attachmentsList,
      }),
      ...(fileList.length !== 0) && ({'attachment_files': fileList}),
    };

    const success = await Requests.postForm(url, attachmentForm);
    return success;
  },

  async editDiscussionThreadById(analysisName, postId, postContent) {
    const url = `/rosalution/api/analysis/${analysisName}/discussions/${postId}`;

    const attachmentForm = {'discussion_content': postContent};

    const success = await Requests.putForm(url, attachmentForm);

    return success;
  },

  async deleteDiscussionThreadById(analysisName, postId) {
    const url = `/rosalution/api/analysis/${analysisName}/discussions/${postId}`;

    const success = await Requests.delete(url);

    return success;
  },

  async postNewDiscussionReply(analysisName, postId, newReplyContent) {
    const url = `/rosalution/api/analysis/${analysisName}/discussions/${postId}/thread/`;

    const discussionThread = {
      'post_id': postId,
      'discussion_reply_content': newReplyContent,
    };

    const success = await Requests.postForm(url, discussionThread);

    return success;
  },

  async editDiscussionReply(analysisName, postId, replyId, replyContent) {
    const url = `/rosalution/api/analysis/${analysisName}/discussions/${postId}/thread/${replyId}`;

    const attachmentForm = {'discussion_reply_content': replyContent};

    const success = await Requests.postForm(url, attachmentForm);

    return success;
  },

  async deleteDiscussionReply(analysisName, postId, replyId) {
    const url = `/rosalution/api/analysis/${analysisName}/discussions/${postId}/thread/${replyId}`;

    const success = await Requests.delete(url);

    return success;
  },
};
