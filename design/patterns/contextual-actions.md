# Contextual actions

## Action hierarchy

One persistent view has at most one prominent primary action. In the main workbench that action
is **Discover repositories**. Mark the action with `data-ui-primary="true"` so the audit can
enforce the budget.

Filtering and sorting update the list but are not competing page-level primary actions. Use a
neutral or quiet treatment for explicit “Apply” or “Reset” controls when immediate updates are
not appropriate.

## Selection actions

Show **Queue analysis** only when one or more selected candidates are eligible. Place it in a
contextual selection bar with the selection count. The bar may replace or sit immediately next
to table controls, but must not become another permanent page header.

When candidate detail is open, acceptance, hold, and rejection are semantic review actions.
Make their consequences and disabled states explicit. Do not style all of them as primary or
place multiple full-width solid buttons together.

## Row and overflow actions

The row or repository name opens detail. Reserve overflow menus for uncommon actions that do
not deserve a persistent column. Do not add repetitive “Explore,” “View,” or “Open details”
links.

## Destructive and asynchronous actions

- Require context or confirmation proportional to reversibility.
- Keep progress close to the initiating action and reflect long-running jobs in the activity
  region.
- Disable duplicate submission while an action is pending.
- Return focus to a useful control when a sheet, dialog, or menu closes.
