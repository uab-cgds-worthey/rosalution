import {expect, describe, it, beforeAll, afterAll} from 'vitest';
import {config, shallowMount} from '@vue/test-utils';
import sinon from 'sinon';

import Header from '@/components/Header.vue';

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

  return shallowMount(Header, {
    props: {...defaultProps, ...props},
    global: {
      components: {
        'font-awesome-icon': FontAwesomeIcon,
        'router-link': RouterLink,
      },
      mocks: {
        $route: {
          push: sinon.spy(),
        },
        $router: {
          push: sinon.spy(),
        },
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
    const pushSpy = sinon.spy();
    const wrapper = getMountedComponent({
      username: 'UABProvider',
    });
    const userMenuWrapper = wrapper.find('[data-test=user-text]');
      console.log(userMenuWrapper);
    await userMenuWrapper.trigger('click');
    expect(pushSpy.calledWith('/rosalution/account')).to.be.true;
  });

});
