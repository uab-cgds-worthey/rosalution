import {expect, describe, it, beforeAll, afterAll} from 'vitest';
import {config, shallowMount} from '@vue/test-utils';

import Header from '@/components/Header.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import {RouterLink} from 'vue-router';

/**
 * helper function that shadllow mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {
    username: '',
  };

  return shallowMount(Header, {
    props: {...defaultProps, ...props},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
        'router-link': RouterLink,
      },
    },
  });
}

beforeAll(() => {
  config.renderStubDefaultSlot = true;
});

afterAll(() => {
  config.renderStubDefaultSlot = false;
});

describe('HeaderComponent.vue', () => {
  it('should display application title by default', () => {
    const wrapper = getMountedComponent();
    const headerTextLink = wrapper.find('[data-test="header-title-text"]');
    expect(headerTextLink.html()).to.contains('rosalution');
  });

  it('should display the applications name in the title position by default', () => {
    const wrapper = getMountedComponent();
    const headerTextLink = wrapper.get('[data-test="header-title-text"]');
    expect(headerTextLink.text()).to.equal('rosalution');
  });

  it('should provide a anchor to return to the top of the page', () => {
    const wrapper = getMountedComponent();
    const headerTextLink = wrapper.get('[data-test="header-title-text"]');
    expect(headerTextLink.attributes('href')).to.contain('#top');
  });

  it('should render the menu actions icon if actions are provided', () => {
    const wrapper = getMountedComponent({
      actions: ['Action1', 'Action2', 'Action3'],
    });

    const icon = wrapper.find('font-awesome-icon-stub');
    expect(icon.exists()).to.be.true;
  });

  it('should not render the menu actions icon if no actions are provided, but user icon should exist', () => {
    const wrapper = getMountedComponent();
    const icons = wrapper.findAllComponents('font-awesome-icon-stub');
    expect(icons.length).to.equal(1);
  });

  it('should properly display the username in the upper right hand corner', async () => {
    const wrapper = getMountedComponent({
      username: 'UABProvider',
    });
    const userMenuWrapper = wrapper.find('[data-test=user-text]');

    expect(userMenuWrapper.text()).to.contain('UABProvider');
  });
});
