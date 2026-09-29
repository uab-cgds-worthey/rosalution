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
        return new URL('/src/assetsvarsome_logo.png', import.meta.url);
      default:
        return '';
    }
  }

  async function promptAddLinkout(linkType, analysisStoreAttachLinkMethod) {
    if (null == inputDialog) {
      throw new Error('Composable missing Input Dialog configuration');
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
    promptAddLinkout,
  };
};
