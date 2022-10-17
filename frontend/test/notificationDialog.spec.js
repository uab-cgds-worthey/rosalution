import {expect, describe, it} from 'vitest';

import notificationDialog from '@/notificationDialog.js';

describe('notificationDialog reactive', () => {
  describe('the notificationDialog.alert()', () => {
    it('assigns message to the notificationDialog', () => {
      notificationDialog.alert('hello world');
      expect(notificationDialog.state.message).to.equal('hello world');
    });

    it('waits until user closes it to be inactive', () => {
      notificationDialog.alert('hello world').then(async ()=>{
        expect(notificationDialog.state.active).to.be.false;
      });
      expect(notificationDialog.state.active).to.be.true;
      setTimeout(notificationDialog.confirmation, 100);
    });

    it('can do multiple alerts one after another', () => {
      notificationDialog.alert('hello world');
      expect(notificationDialog.state.active).to.be.true;
      expect(notificationDialog.state.message).to.equal('hello world');
      notificationDialog.confirmation();

      notificationDialog.alert('hello world 2');
      expect(notificationDialog.state.active).to.be.true;
      expect(notificationDialog.state.message).to.equal('hello world 2');
      notificationDialog.confirmation();
    });
  });

  describe(('notificationDialog.confirm()'), () => {
    it('can be canceled', () => {
      notificationDialog.confirm('are you sure').then((confirmed)=>{
        expect(confirmed).to.be.false;
      });
      notificationDialog.cancel();
    });

    it('notificationDialog.confirm() can be confirmed', () => {
      notificationDialog.confirm('are you sure').then((confirmed) => {
        expect(confirmed).to.be.true;
      });
      notificationDialog.confirmation();
    });
  });

  it('options can be chained', () => {
    notificationDialog
        .title('Dialog title')
        .confirmText('Delete')
        .cancelText('Dont delete')
        .confirm('Why are you deleting this thing>').then((userInput)=>{
          expect(userInput).to.be.true;
        });
    expect(notificationDialog.state.title).toBe('Dialog title');
    expect(notificationDialog.state.confirmText).toBe('Delete');
    expect(notificationDialog.state.cancelText).toBe('Dont delete');
    notificationDialog.confirmation();
  });

  it('resets on close', () => {
    notificationDialog
        .title('Dialog title')
        .confirmText('Delete')
        .cancelText('Dont delete')
        .confirm('Why are you deleting this thing>').then((userInput)=>{
          expect(notificationDialog.state.title).to.be.empty;
          expect(notificationDialog.state.confirmText).to.equal('Ok');
          expect(notificationDialog.state.cancelText).to.equal('Cancel');
        });
    notificationDialog.confirmation();
  });
});
