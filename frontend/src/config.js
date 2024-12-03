import {EventType} from './enums';

const DEFAULT_TRANSITIONS = [
  ['Approve', EventType.APPROVE, 'Approved'],
  ['Hold', EventType.HOLD, 'On-Hold'],
  ['Decline', EventType.DECLINE, 'Declined'],
];

const StatusType = Object.freeze({
  'Preparation': {
    icon: 'asterisk',
    color: '--rosalution-status-annotation',
    actionText: 'Mark Ready',
    transitions: [['Mark Ready', EventType.READY, 'Ready']],
  },
  'Ready': {
    icon: 'clipboard-check',
    color: '--rosalution-status-ready',
    transitions: [['Mark Active', EventType.OPEN, 'Active']],
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

/**
 * Helper method that returns the Icon for a Workflow status. If none exist for
 * that status a question mark is returned.
 *
 * @param {String} status the workflow status
 * @return {String} the string value of the icon in that workflow
 */
function getWorkflowStatusIcon(status) {
  if ( status in StatusType ) {
    return StatusType[status].icon;
  }

  return 'question';
}

export {StatusType, getWorkflowStatusIcon};
