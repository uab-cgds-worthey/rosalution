export function useThirdPartyAsset(incomingInputDialog = null) {
  const inputDialog = incomingInputDialog;

  function thirdPartyLogoAsset(thirdPartyType) {
    switch (thirdPartyType) {
      case 'monday_com':
        return new URL('/src/assets/monday-avatar-logo.svg', import.meta.url);
      case 'phenotips_com':
        return new URL('/src/assets/phenotips-favicon-96x96.png', import.meta.url);
      case 'wrike_com':
        return new URL('/src/assets/wrike_com.svg', import.meta.url);
      case 'varsome_com':
        return new URL('/src/assets/varsome_logo.png', import.meta.url);
      case 'onedrive_com':
        return new URL('/src/assets/microsoft-onedrive-logo.svg', import.meta.url);
      default:
        return '';
    }
  }

  function thirdPartyLogoStyle(thirdPartyType) {
    switch (thirdPartyType) {
      case 'monday_com':
        return {
          width: '1.875rem', /* 30px */
          height: '1.875rem', /* 30px */
          transform: 'translate(-8px, 0)',
        };
      case 'wrike_com':
      case 'onedrive_com':
      case 'varsome_com':
        return {
          height: '1.75rem', /* 30px */
          transform: 'translate(-2px, 0)',
        };
      case 'phenotips_com':
        return { /* 20px */
          width: '1.25rem',
          height: '1.25rem',
          transform: 'translate(-16px, 0)',
        };
      default:
        return {};
    }
  }

  async function promptAddLinkout(linkType, analysisStoreAttachLinkMethod) {
    if (null == inputDialog) {
      throw new Error('Composable Third Party Add Prompt missing input dilaog configuration.');
    }

    const includeComments = false;
    const includeName = false;
    const thirdPartyLinkData = await inputDialog
        .confirmText('Add')
        .cancelText('Cancel')
        .url(includeComments, includeName)
        .prompt();

    if (!thirdPartyLinkData) {
      return;
    }

    try {
      await analysisStoreAttachLinkMethod(linkType, thirdPartyLinkData.data);
    } catch (error) {
      console.error('Updating analysis with third party link attachment failed', error);
    }
  }

  return {
    thirdPartyLogoAsset,
    thirdPartyLogoStyle,
    promptAddLinkout,
  };
};
