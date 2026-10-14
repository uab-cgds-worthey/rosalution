import {describe, it, expect} from 'vitest';

import sinon from 'sinon';

import inputDialog from '@/inputDialog.js';
import {useThirdPartyAsset} from '@/composables/useThirdPartyAsset.js';

describe('useThirdPartyAsset', () => {
  describe(('controlls the prompt add linkout input dialog'), () => {
    it('throws exception when no input dialog provided for composable to prompt user with', async () => {
      const expectedType = 'wrike_com';

      const mockThirdPartySaveMethod = sinon.fake.resolves(true);

      const {promptAddLinkout} = useThirdPartyAsset();
      await expect(() => promptAddLinkout(expectedType, mockThirdPartySaveMethod))
          .rejects.toThrow('Composable Third Party Add Prompt missing input dilaog configuration.');
    });

    it('succesfully confirms and calls save method', async () => {
      const expectedType = 'wrike_com';
      const expectedLinkString = 'https://www.fake.link.forever';
      const expectedData = {
        data: expectedLinkString,
      };
      const mockThirdPartySaveMethod = sinon.fake.resolves(true);

      expect(inputDialog.state.active).to.be.false;

      const {promptAddLinkout} = useThirdPartyAsset(inputDialog);
      promptAddLinkout(expectedType, mockThirdPartySaveMethod);

      expect(inputDialog.state.active).to.be.true;

      await inputDialog.confirmation(expectedData);

      expect(inputDialog.state.active).to.be.false;
      expect(mockThirdPartySaveMethod.calledOnce).to.be.true;

      const actualCallArguments = mockThirdPartySaveMethod.args[0];
      expect(actualCallArguments[0]).to.equal(expectedType);
      expect(actualCallArguments[1]).to.equal(expectedLinkString);
    });
    it('cancels and does not save link when dialog canceled', async () => {
      const mockThirdPartySaveMethod = sinon.fake.resolves(true);

      expect(inputDialog.state.active).to.be.false;

      const {promptAddLinkout} = useThirdPartyAsset(inputDialog);
      const expectedType = 'wrike_com';
      promptAddLinkout(expectedType, mockThirdPartySaveMethod);

      expect(inputDialog.state.active).to.be.true;
      await inputDialog.cancel();

      expect(inputDialog.state.active).to.be.false;
      expect(mockThirdPartySaveMethod.notCalled).to.be.true;
    });
  });
});
