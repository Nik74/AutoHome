from tkinter import ttk


# to sort the table by column when clicking in column
def treeview_sort_column(treeview: ttk.Treeview, column, reverse: bool):
    try:
        data_list = [
            (int(treeview.set(k, column)), k) for k in treeview.get_children("")
        ]
    except Exception:
        data_list = [(treeview.set(k, column), k) for k in treeview.get_children("")]

    data_list.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(data_list):
        treeview.move(k, "", index)

    # reverse sort next time
    treeview.heading(
        column=column,
        text=column,
        command=lambda _col=column: treeview_sort_column(treeview, _col, not reverse),
    )
