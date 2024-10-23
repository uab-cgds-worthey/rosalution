import {EventType} from './enums';

const DEFAULT_TRANSITIONS = [['Approve', EventType.APPROVE], ['Hold', EventType.HOLD], ['Decline', EventType.DECLINE]];

export const StatusType = Object.freeze({
  'Preparation': {
    icon: 'asterisk',
    color: '--rosalution-status-annotation',
    actionText: 'Mark Ready',
    transitions: [['Mark Ready', EventType.READY]],
  },
  'Ready': {
    icon: 'clipboard-check',
    color: '--rosalution-status-ready',
    transitions: [['Mark Active', EventType.OPEN]],
  },
  'Active': {
    icon: 'book-open',
    color: '--rosalution-status-active',
    transitions: DEFAULT_TRANSITIONS,
  },
  'Approved': {
    icon: 'check',
    color: '--rosalution-status-approved',
    transitions: DEFAULT_TRANSITIONS,
  },
  'On-Hold': {
    icon: 'pause',
    color: '--rosalution-status-on-hold',
    transitions: DEFAULT_TRANSITIONS,
  },
  'Declined': {
    icon: 'x',
    color: '--rosalution-status-declined',
    transitions: DEFAULT_TRANSITIONS,
  },
});
