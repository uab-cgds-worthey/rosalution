import {describe, it, beforeEach, expect} from 'vitest';
import {mount} from '@vue/test-utils';
import sinon from 'sinon';

import AnalysisCreateView from '../../src/views/AnalysisCreateView.vue';
import Analyses from '../../src/models/analyses.js';

const inputFixture = {
  name: 'Test Name',
  description: 'Test Description',
  coordinates: {
    chromosome: 'Test Chromosome',
    position: 'Test Position',
    reference: 'Test Reference',
    alternate: 'Test Alternate',
  },
};

describe('AnalysisCreate.vue', () => {
  let wrapper;

  beforeEach(() => {
    wrapper = mount(AnalysisCreateView);
  });

  it('renders a vue instance', () => {
    expect(typeof wrapper).toBe('object');
  });

  describe('Displays each part of the form to create an Analysis', () => {
    it('Displays Required Input Form', () => {
      const reqInputForm = wrapper.find('[data-test=required-input-form]');

      expect(reqInputForm.exists()).toBe(true);
    });

    it('Supplemental Form List', () => {
      const supplementalFormList = wrapper.find('[data-test=supplemental-form-list]');

      expect(supplementalFormList.exists()).toBe(true);
    });

    it('Should compile form data to save analysis', async () => {
      const saveAnalysisSpy = sinon.spy(Analyses, 'saveAnalysis');

      await wrapper.vm.createUpdateAnalysis(inputFixture);

      expect(saveAnalysisSpy.called).toBe(true);
    });
  });
});
