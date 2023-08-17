/**
 * Wraps the browser's history.state attribute so that it can be mocked
 * @return {Object} the browsers state object from history
 */
export default {
  async historyState() {
    return history.state;
  },
};

