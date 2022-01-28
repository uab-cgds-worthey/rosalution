import {test, expect} from 'vitest';

import Analyses from '@/models/analyses.js';

test('Queries all the analyses', async () => {
  const analyses = await Analyses.all();
  
  expect(analyses.length).toBe(8);
});
