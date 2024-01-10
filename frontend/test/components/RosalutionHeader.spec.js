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
    third_party_links: [
      {'type': 'monday_com', 'link': 'https://monday.com'},
      {'type': 'phenotips_com', 'link': 'https://phenotips.com'},
    ],
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
    console.log(wrapper.html());
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

  it('should display the proper workflow icon based on the workflow_status prop', () => {
    [
      {
        workflow_status: 'Preparation',
        expected: 'asterisk',
      },
      {
        workflow_status: 'Active',
        expected: 'book-open',
      },
      {
        workflow_status: 'Approved',
        expected: 'check',
      },
    ].forEach((test) => {
      const wrapper = getMountedComponent({workflow_status: test.workflow_status});
      const statusIcon = wrapper.get('font-awesome-icon-stub');
      expect(statusIcon.attributes().icon).to.equal(test.expected);
    });
  });

  it('should display the proper workflow color based on the workflow_status prop', () => {
    [
      {
        workflow_status: 'Preparation',
        expected: 'color: var(--rosalution-status-annotation);',
      },
      {
        workflow_status: 'Active',
        expected: 'color: var(--rosalution-status-active);',
      },
      {
        workflow_status: 'Approved',
        expected: 'color: var(--rosalution-status-approved);',
      },
    ].forEach((test) => {
      const wrapper = getMountedComponent({workflow_status: test.workflow_status});
      const statusIcon = wrapper.get('font-awesome-icon-stub');
      expect(statusIcon.attributes().style).to.equal(test.expected);
    });
  });

  it('should not render any icon when the workflow_status prop is not provided', () => {
    const wrapper = getMountedComponent();
    const statusIcon = wrapper.find('[data-test="status-icon"]');
    expect(statusIcon.exists()).to.be.false;
  });


  it('should render third party links', () => {
    const wrapper = getMountedComponent();

    const thirdPartyLinks = wrapper.findAll('[data-test="third-party-link"]');

    const mondayLink = thirdPartyLinks[0];
    expect(mondayLink.attributes('href')).to.equal('https://monday.com');
    expect(mondayLink.attributes('target')).to.equal('_blank');

    const phenotipsLink = thirdPartyLinks[1];
    expect(phenotipsLink.attributes('href')).to.equal('https://phenotips.com');
    expect(phenotipsLink.attributes('target')).to.equal('_blank');
  });

  it('should not render third party links if empty', () => {
    const wrapper = getMountedComponent({
      third_party_links: [],
    });

    const thirdPartyLink = wrapper.find('[data-test="third-party-link"]');
    expect(thirdPartyLink.exists()).to.be.false;
  });
});
