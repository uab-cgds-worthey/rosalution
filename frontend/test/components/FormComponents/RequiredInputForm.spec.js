import {expect, describe, it, beforeEach} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import RequiredInputForm from '../../../src/components/FormComponents/RequiredInputForm.vue';

describe('RequiredInputForm.vue', () => {
    let wrapper;

    beforeEach(() => {
        wrapper = shallowMount(RequiredInputForm, {
            data() {
                return {
                    coordinates: [
                        {
                            chromosome: '17',
                            position: '3768176',
                            reference: 'T',
                            alternate: 'AGTGT',
                        },
                        {
                            chromosome: '36',
                            position: '2781',
                            reference: 'GTATAGCA',
                            alternate: 'GTCTATTTT',
                        },
                        {
                            chromosome: '1',
                            position: '37',
                            reference: 'GATTTA',
                            alternate: 'AATTTAGA',
                        },
                        {
                            chromosome: '1',
                            position: '2',
                            reference: 'GAAAAT',
                            alternate: 'GGGTTTAAA',
                        },
                    ]
                };
            },
        });
    });

    it('Vue instance exists and it is an object', () => {
        expect(typeof wrapper).toBe('object');
    });

    it('Adds a table row with data and renders the proper amount of rows', async () => {
        const addCoordinateButton = wrapper.find('[data-test="button-add-coord"]');

        const chromInput = wrapper.find('#chrom');
        const posInput = wrapper.find('#pos');
        const refInput = wrapper.find('#ref');
        const altInput = wrapper.find('#alt');

        chromInput.setValue('9');
        posInput.setValue('19325');
        refInput.setValue('ATGTCATGCC');
        altInput.setValue('T');

        await addCoordinateButton.trigger('click');

        const coordinateTableRows = wrapper.findAll('tr');

        expect(coordinateTableRows.length).to.equal(5);

        // Note: Rows are added at the front of the array and existing items get pushed back
        // this is why we're looking at index 0 even after adding a new row

        const tableColumn = coordinateTableRows.at(0).findAll('td');

        expect(tableColumn.at(0).text()).to.equal('9');
        expect(tableColumn.at(1).text()).to.equal('19325');
        expect(tableColumn.at(2).text()).to.equal('ATGTCATGCC');
        expect(tableColumn.at(3).text()).to.equal('T');
    });

    it('Remove a table row when deleted and renders the proper amount of rows', async () => {
        let coordinateTableRows = wrapper.findAll('tr');
    
        const tableRowButton = coordinateTableRows.at(0).find('button');
    
        expect(coordinateTableRows.length).to.equal(4);
    
        await tableRowButton.trigger('click');
    
        coordinateTableRows = wrapper.findAll('tr');
    
        expect(coordinateTableRows.length).to.equal(3);
      });

      it('Emits the correct form data when the create button is pressed', async () => {
        wrapper = shallowMount(RequiredInputForm);
    
        const createAnalysisButton = wrapper.find('[data-test="button-create-analysis"]');
    
        const nameInput = wrapper.find('#name');
        const descriptionInput = wrapper.find('#description');
    
        nameInput.setValue('Test');
        descriptionInput.setValue('This is a test.');
    
        await createAnalysisButton.trigger('click');
    
        expect(wrapper.emitted().create_analysis[0][0].name).to.equal('Test');
        expect(wrapper.emitted().create_analysis[0][0].description).to.equal('This is a test.');
      });
    
      it('Creates a VCF when the create button is pressed', async () => {
        // This is checking if the createVCF helper function is providing the correct output
        const wrapper = shallowMount(RequiredInputForm);
    
        wrapper.setData({coordinates: [{
          chromosome: '1',
          position: '10',
          reference: 'A',
          alternate: 'T',
        }, {
          chromosome: '2',
          position: '20',
          reference: 'G',
          alternate: 'C',
        }]});
    
        const createAnalysisButton = wrapper.find('[data-test="button-create-analysis"]');
        await createAnalysisButton.trigger('click');

        const emit = wrapper.emitted().create_analysis;

        // Don't know why it's an array within an array, but it is.
        expect(emit[0][0].coordinates.length).toBe(2);
      });
});