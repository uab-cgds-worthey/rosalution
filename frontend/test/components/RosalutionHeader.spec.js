import {expect, describe, it, beforeAll, afterAll} from 'vitest';
import {config, shallowMount} from '@vue/test-utils';

import sinon from 'sinon';

import RosalutionHeader from '@/components/RosalutionHeader.vue';

import {FontAwesomeIcon} from '@fortawesome/vue-fontawesome';
import {RouterLink} from 'vue-router';

/**
 * Helper mounts and returns the rendered component
 * @param {props} props props for testing to overwrite default props
 * @return {VueWrapper} returns a shallow mounted using props
 */
function getMountedComponent(props) {
  const defaultProps = {
    username: '',
  };

  return shallowMount(RosalutionHeader, {
    props: {...defaultProps, ...props},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
        'router-link': RouterLink,
      },
      mocks: {
        $route: {
          path: '/rosalution/account',
          push: sinon.spy(),
        },
      },
    },
  });
}

beforeAll(() => {
  config.global.renderStubDefaultSlot = true;
});

afterAll(() => {
  config.global.renderStubDefaultSlot = false;
});

describe('RosalutionHeaderComponent.vue', () => {
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

  it('should render the menu actions drop-down menu if actions are provided', () => {
    const wrapper = getMountedComponent({
      actions: [{text: 'Action1'}, {text: 'Action2'}, {text: 'Action3'}],
    });

    const dropDownMenu = wrapper.find('[data-test=user-menu]');
    expect(dropDownMenu.exists()).to.be.true;
  });

  it('should not render menu actions drop down if no actions are provided', () => {
    const wrapper = getMountedComponent();
    const dropDownMenu = wrapper.find('[data-test=user-menu]');
    expect(dropDownMenu.exists()).to.be.false;
  });

  it('should properly display the username in the upper right hand corner', async () => {
    const wrapper = getMountedComponent({
      username: 'UABProvider',
    });
    const userMenuWrapper = wrapper.find('[data-test=user-text]');

    expect(userMenuWrapper.text()).to.contain('UABProvider');
  });

  it('should route to the AccountView when the username is clicked', async () => {
    const wrapper = getMountedComponent({
      username: 'UABProvider',
    });

    const usernameLink = wrapper.find('[data-test="user-text"]');
    usernameLink.trigger('click');

    await wrapper.vm.$nextTick();

    expect(wrapper.vm.$route.path).to.equal('/rosalution/account');
  });

  it('should display the proper workflow icon based on the workflow_status prop', async () => {
    const wrapper = getMountedComponent({ workflow_status: 'Annotation' });
    let statusIcons = wrapper.findAllComponents({ name: 'FontAwesomeIcon' });
    let statusIcon = statusIcons[0];
    expect(statusIcon.props('icon')).to.equal('asterisk');

    await wrapper.setProps({ workflow_status: 'Ready' });
    statusIcons = wrapper.findAllComponents({ name: 'FontAwesomeIcon' });
    statusIcon = statusIcons[0];
    expect(statusIcon.props('icon')).to.equal('clipboard-check');

    await wrapper.setProps({ workflow_status: 'Active' });
    statusIcons = wrapper.findAllComponents({ name: 'FontAwesomeIcon' });
    statusIcon = statusIcons[0];
    expect(statusIcon.props('icon')).to.equal('book-open');

    await wrapper.setProps({ workflow_status: 'Approved' });
    statusIcons = wrapper.findAllComponents({ name: 'FontAwesomeIcon' });
    statusIcon = statusIcons[0];
    expect(statusIcon.props('icon')).to.equal('check');

    await wrapper.setProps({ workflow_status: 'On-Hold' });
    statusIcons = wrapper.findAllComponents({ name: 'FontAwesomeIcon' });
    statusIcon = statusIcons[0];
    expect(statusIcon.props('icon')).to.equal('pause');

    await wrapper.setProps({ workflow_status: 'Declined' });
    statusIcons = wrapper.findAllComponents({ name: 'FontAwesomeIcon' });
    statusIcon = statusIcons[0];
    expect(statusIcon.props('icon')).to.equal('x');
  });

  it('should display the proper workflow color based on the workflow_status prop', async () => {
    const wrapper = getMountedComponent({ workflow_status: 'Annotation' });
    let statusIcons = wrapper.findAllComponents({ name: 'FontAwesomeIcon' });
    let statusIcon = statusIcons[0];
    expect(statusIcon.attributes('style')).to.equal('color: var(--rosalution-status-annotation);');

    await wrapper.setProps({ workflow_status: 'Ready' });
    statusIcons = wrapper.findAllComponents({ name: 'FontAwesomeIcon' });
    statusIcon = statusIcons[0];
    expect(statusIcon.attributes('style')).to.equal('color: var(--rosalution-status-ready);');

    await wrapper.setProps({ workflow_status: 'Active' });
    statusIcons = wrapper.findAllComponents({ name: 'FontAwesomeIcon' });
    statusIcon = statusIcons[0];
    expect(statusIcon.attributes('style')).to.equal('color: var(--rosalution-status-active);');

    await wrapper.setProps({ workflow_status: 'Approved' });
    statusIcons = wrapper.findAllComponents({ name: 'FontAwesomeIcon' });
    statusIcon = statusIcons[0];
    expect(statusIcon.attributes('style')).to.equal('color: var(--rosalution-status-approved);');

    await wrapper.setProps({ workflow_status: 'On-Hold' });
    statusIcons = wrapper.findAllComponents({ name: 'FontAwesomeIcon' });
    statusIcon = statusIcons[0];
    expect(statusIcon.attributes('style')).to.equal('color: var(--rosalution-status-on-hold);');

    await wrapper.setProps({ workflow_status: 'Declined' });
    statusIcons = wrapper.findAllComponents({ name: 'FontAwesomeIcon' });
    statusIcon = statusIcons[0];
    expect(statusIcon.attributes('style')).to.equal('color: var(--rosalution-status-declined);');
  });
});
