import {expect, describe, it} from 'vitest';
import {shallowMount} from '@vue/test-utils';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import CopyToClipboard from '@/components/CopyToClipboard.vue';

/**
 * helper function that shallow mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {
    copyText: 'NM_170707.3:c.745C>T',
  };

  return shallowMount(CopyToClipboard, {
    props: {...defaultProps, ...props},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
      },
    },
  });
}


describe('CopyToClipboard.vue', () => {
  it('should log text to console when copy button is clicked', async () => {
    let clipboardContents = '';

    window.__defineGetter__('navigator', function() {
      return {
        clipboard: {
          writeText: (text) => {
            clipboardContents = text;
          },
        },
      };
    });

    const wrapper = getMountedComponent();
    await wrapper.trigger('click');

    expect(clipboardContents).to.equal('NM_170707.3:c.745C>T');
  });

  it('should emit a signal that text ws copied', async () => {
    const wrapper = getMountedComponent();
    await wrapper.trigger('click');

    const emittedObjects = wrapper.emitted()['clipboard-copy'][0];
    expect(emittedObjects[0]).to.equal('NM_170707.3:c.745C>T');
  });
});
