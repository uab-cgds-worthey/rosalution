export function isDatasetAvailable(datasetValue) {
  return !(
    datasetValue == undefined ||
    datasetValue == '.' ||
    datasetValue == 'null' ||
    datasetValue == null ||
    datasetValue == ''
  );
};

/**
 * Calculates styling for score bar according to configuration.
 *
 * @param {number} value
 * @param {Object} configuration
 * @param {Object} styles
 * @returns {Object} The fill width, css styling, and colors configuration for the bar.
 */
export function useScoreBarCalculations(value, configuration, styles) {
  const {minimum, maximum, bounds, cutoff}  = configuration;

  const scoreFillValue = (parseFloat(Math.abs(minimum) + value) /
    (Math.abs(minimum) + Math.abs(maximum)));

  const scoreFillWidthPercentage = Math.floor(Math.abs(scoreFillValue) * 100) + '%';

  let scoreStyling = styles.nominalColours;

  function withinBounds(score) {
    return score > bounds.lowerBound && score < bounds.upperBound;
  }
  function belowBounds(score) {
    return score > bounds.upperBound;
  }

  const datasetBarAttributes = {};

  if (!isDatasetAvailable(value)) {
    datasetBarAttributes['class'] = 'dataset-bar-fill-unavailable';
    scoreStyling = styles.unavailableColours;
  } else if (cutoff) {
    let score = 0;
    score = value / cutoff;
    if (withinBounds(score)) {
      scoreStyling = styles.closeToThresholdColours;
    } else if (belowBounds(score)) {
      scoreStyling = styles.outOfThresholdColours;
    }

    datasetBarAttributes['style'] = {
      'background-color': scoreStyling.backgroundColour,
    };
  }

  return {
    scoreFillWidthPercentage: scoreFillWidthPercentage,
    datasetBarAttributes: datasetBarAttributes,
    scoreStyling: scoreStyling,
  };
};

/**
 * Calculates styling for the section item of a set.
 *
 * @param {String} datasetValue The dataset's value to be diplayed
 * @param {Object} set
 * @returns {Array} The list of each set item's rendering key, css styling, and content
 */
export function useSetBarCalculations(datasetValue, set) {
  function calculateWidth(value) {
    const width = 100;

    if (value == datasetValue) {
      return `${width * .75}%`;
    }
    return `${ (width / set.length) / 2}%`;
  };

  function setItemStyle(item) {
    const style = {
      'background-color': 'var(--rosalution-grey-300)',
      'opacity': 1,
    };


    if (item.colour == 'Red') {
      style['background-color'] = 'var(--rosalution-red-200)';
    } else if (item.colour == 'Blue') {
      style['background-color'] = 'var(--rosalution-blue-200)';
    } else if (item.colour == 'Yellow') {
      style['background-color'] = 'var(--rosalution-yellow-200)';
    } else if (item.colour == 'Green') {
      style['background-color'] = 'var(--rosalution-green-200)';
    }

    style['width'] = calculateWidth(item.value);

    return (item.value == datasetValue) ? style : {...style, 'opacity': 0.5};
  };

  function classificationText(setItem) {
    return (setItem.value == datasetValue) ? setItem.classification : '';
  };

  const setItemsStyling = set.map( (item, index) => {
    return {
      key: `${datasetValue}-${index}`,
      style: setItemStyle(item),
      content: classificationText(item),
    };
  });

  return setItemsStyling;
};
