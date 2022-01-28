import {test, expect} from 'vitest';

import Analyses from '@/models/analyses.js';

test('Queries all the analyses', async () => {
  const analyses = await Analyses.all();
  console.log(analyses);

  expect(1).toBe(1);
});
