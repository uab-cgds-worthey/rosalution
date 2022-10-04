import {expect, describe, it} from 'vitest';

import dialog from '@/dialog.js';

describe('dialog reactive', () => {
  describe('the dialog.alert()', () => {
    it('assigns message to the dialog', () => {
      dialog.alert('hello world');
      expect(dialog.state.message).to.equal('hello world');
    });

    it('waits until user closes it to be inactive', () => {
      dialog.alert('hello world').then(async ()=>{
        expect(dialog.state.active).to.be.false;
      });
      expect(dialog.state.active).to.be.true;
      setTimeout(dialog.confirmation, 100);
    });

    it('can do multiple alerts one after another', () => {
      dialog.alert('hello world');
      expect(dialog.state.active).to.be.true;
      expect(dialog.state.message).to.equal('hello world');
      dialog.confirmation();

      dialog.alert('hello world 2');
      expect(dialog.state.active).to.be.true;
      expect(dialog.state.message).to.equal('hello world 2');
      dialog.confirmation();
    });
  });

  describe(('dialog.confirm()'), () => {
    it('can be canceled', () => {
      dialog.confirm('are you sure').then((confirmed)=>{
        expect(confirmed).to.be.false;
      });
      dialog.cancel();
    });

    it('dialog.confirm() can be confirmed', () => {
      dialog.confirm('are you sure').then((confirmed) => {
        expect(confirmed).to.be.true;
      });
      dialog.confirmation();
    });
  });

  it('options can be chained', () => {
    dialog
        .title('Dialog title')
        .confirmText('Delete')
        .cancelText('Dont delete')
        .confirm('Why are you deleting this thing>').then((userInput)=>{
          expect(userInput).to.be.true;
        });
    expect(dialog.state.title).toBe('Dialog title');
    expect(dialog.state.confirmText).toBe('Delete');
    expect(dialog.state.cancelText).toBe('Dont delete');
    dialog.confirmation();
  });

  it('resets on close', () => {
    dialog
        .title('Dialog title')
        .confirmText('Delete')
        .cancelText('Dont delete')
        .confirm('Why are you deleting this thing>').then((userInput)=>{
          expect(dialog.state.title).to.be.empty;
          expect(dialog.state.confirmText).to.equal('Ok');
          expect(dialog.state.cancelText).to.equal('Cancel');
        });
    dialog.confirmation();
  });
});
