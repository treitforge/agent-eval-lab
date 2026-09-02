# Contextual actions

## Action hierarchy

One persistent view has no more than one primary action. In the comparison workbench, that action is **Download facts**.

Mark the action with `data-ui-primary="true"`. An automated test can enforce this limit.

Filtering and sorting are not primary page actions. Use a neutral or quiet treatment for an **Apply** or **Reset** control.

## Trial actions

Open trial details when a user selects a row. Keep the selected row visible while the inspector is open.

If a future action changes data, state its effect. Show its disabled state. Do not style all trial actions as primary.

## Row and overflow actions

The trial row opens its details. Use an overflow menu only for uncommon actions.

Do not add a repeated **View** or **Open details** link to each row.

## Destructive and asynchronous actions

- Require confirmation when an action is difficult to reverse.
- Keep progress close to the action that started it.
- Disable duplicate submission while an action is pending.
- Return focus to the source control when a sheet, dialog, or menu closes.
