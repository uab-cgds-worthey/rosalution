import {expect, describe, it} from 'vitest';

import toast from '@/toast.js';

describe('a reactive toast', () => {
  describe('the that displays info', () => {
    it('assigns message to the toast', () => {
      toast.info('hello world info');
      expect(toast.state.message).to.equal('hello world info');
    });

    it('can do multiple toasts one after another', () => {
      toast.info('hello world first time');
      expect(toast.state.active).to.be.true;
      expect(toast.state.message).to.equal('hello world first time');
      toast.cancel();

      toast.info('hello world 2');
      expect(toast.state.active).to.be.true;
      expect(toast.state.message).to.equal('hello world 2');
      toast.cancel();
    });
  });

  describe('the that displays an error', () => {
    it('assigns message to the toast', () => {
      toast.error('hello world error');
      expect(toast.state.message).to.equal('hello world error');
    });
  });

  describe('the that displays a success', () => {
    it('assigns message to the toast', () => {
      toast.error('hello world successs');
      expect(toast.state.message).to.equal('hello world successs');
    });
  });

  describe('displays different multiple and different prompts', () => {
    it('assigns message to the toast', () => {
      toast.info('hello world first time');
      expect(toast.state.active).to.be.true;
      expect(toast.state.message).to.equal('hello world first time');
      toast.cancel();

      toast.error('hello world error');
      expect(toast.state.active).to.be.true;
      expect(toast.state.message).to.equal('hello world error');
      toast.cancel();
    });
  });

  it('makes it inactive when the toast is closed ', () => {
    toast.info('hello world').then(async ()=>{
      expect(toast.state.active).to.be.false;
    });
    expect(toast.state.active).to.be.true;
    setTimeout(toast.cancel, 100);
  });

  it('resets on close', () => {
    toast.info('Just letting you know this happened.').then(()=>{
      expect(toast.state.message).to.be.empty;
    });
  });
});
