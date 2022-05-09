import { describe, it, expect, beforeEach, afterEach } from "vitest";

import User from '@/models/user.js';
import Requests from '@/requests.js'
import sinon from 'sinon';

describe('user.js', () => {
    const sandbox = sinon.createSandbox();
    let mockGetRequest;

    beforeEach(() => {
        mockGetRequest = sandbox.stub(Requests, 'get');
    });

    afterEach(() => {
        sandbox.restore();
    });

    it('Queries the user from the backend session, user is NOT logged in', async () => {
        mockGetRequest.returns({"username": ''})
        const username = await User.getUser();
        expect(username['username']).to.equal('');
    });

    it('Queries the user from the backend session, user is logged in', async () => {
        mockGetRequest.returns({"username": 'UABProvider'})
        const username = await User.getUser();
        expect(username['username']).to.equal('UABProvider');
    });
});