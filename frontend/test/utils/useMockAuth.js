import {ref} from 'vue';
import sinon from 'sinon';


export const mockUsername = ref('shippo');
export const mockAuthWritePermissions = ref(false);
export const mockLogout = sinon.fake();

export const useAuthMock = sinon.stub().returns({
  username: mockUsername,
  hasWritePermission: mockAuthWritePermissions,
  logout: mockLogout,
});
