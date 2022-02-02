import {test, expect, describe, it, beforeEach} from 'vitest';
import {mount, shallowMount} from '@vue/test-utils';

import RequiredInputForm from '../../../src/components/FormComponents/RequiredInputForm.vue';

test('Vue instance exists and it is an object', () => {
    const wrapper = mount(RequiredInputForm, {shallow: true});
    expect(typeof wrapper).toBe('object');
});

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
                }
            }
        });
    });

    it('', () => {

    });
});