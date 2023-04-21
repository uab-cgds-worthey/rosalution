import {describe, it, expect, beforeEach, afterEach} from 'vitest';

import FileRequests from '@/fileRequests.js';
import Requests from '@/requests.js';

import sinon from 'sinon';

describe('fileRequests.js', () => {
  const sandbox = sinon.createSandbox();

  let mockGetImageRequest;

  beforeEach(() => {
    mockGetImageRequest = sandbox.stub(Requests, 'getImage');
  });

  afterEach(() => {
    sandbox.restore();
  });

  it('fetches a file from gridfs with a given id', async () => {
    const expectedUrl = '/rosalution/api/analysis/download/fake-file-id-1';
    const expectedReturn = 'it worked';

    mockGetImageRequest.returns(expectedReturn);

    const actualReturned = await FileRequests.getImage('fake-file-id-1');

    expect(actualReturned).to.equal(expectedReturn);
    expect(mockGetImageRequest.calledWith(expectedUrl)).to.be.true;
  });
});
