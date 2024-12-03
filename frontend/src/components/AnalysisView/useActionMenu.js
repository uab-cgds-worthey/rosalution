import {ref} from 'vue';
import {StatusType, getWorkflowStatusIcon} from '@/config.js';


/**
 * Builds an actionMenu that can be used for the main header
 * @return {Object} {actionChoices, builder} to return the actions to render and the builder to update the choices
 */
export function useActionMenu() {
  const actionChoices = ref([]);

  const builder = {
    addWorkflowActions: (latest, operation) => {
      if ( latest in StatusType ) {
        for ( const [text, nextEvent, nextStatus] of StatusType[latest].transitions) {
          builder.addMenuAction(text, getWorkflowStatusIcon(nextStatus), () => {
            operation(nextEvent);
          });
        }
      }
    },
    addMenuAction: (text, icon, operation) => {
      actionChoices.value.push({
        icon: icon,
        text: text,
        operation: operation,
      });
    },
    addDivider: () => {
      actionChoices.value.push({divider: true});
    },
    clear: () => {
      actionChoices.value = [];
    },
  };

  return {actionChoices, builder};
}
