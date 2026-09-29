import {ThirdPartyIconUrl} from '@/config.js';

let preloadedIconAssets = null;

export function useThirdPartyAsset(incomingInputDialog = null) {
  const inputDialog = incomingInputDialog;

  function thirdPartyLogoAsset(thirdPartyType) {
    if ( null == preloadedIconAssets ) {
      preloadedIconAssets = Object.fromEntries(
          Object.entries(ThirdPartyIconUrl).map(([key, path]) => [
            key,
            new URL(path, import.meta.url).href,
          ]),
      );
    }
    
    return  thirdPartyType in preloadedIconAssets ? preloadedIconAssets[preloadedIconAssets] : '';
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
      throw new Error('Composable Third Party Add Prompt missing input dialog configuration.');
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
