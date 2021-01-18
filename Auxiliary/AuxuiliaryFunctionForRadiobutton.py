# Create and output radiobutton

from tkinter import *


def output_radiobutton(element, frame_result):
    canvas_result = Canvas(frame_result)
    frame_canvas = Frame(canvas_result)
    scrollbar_result = Scrollbar(frame_result, orient='vertical')

    scrollbar_result['command'] = canvas_result.yview
    canvas_result.configure(yscrollcommand=scrollbar_result.set)

    canvas_result.place(y="0", height='200')
    scrollbar_result.place(y="0", x='150', height='200')
    canvas_result.create_window((0, 0), window=frame_canvas, anchor='nw')

    def conf(event):
        canvas_result.configure(scrollregion=canvas_result.bbox('all'))

    def select(event):
        result = res.get()

    frame_canvas.bind('<Configure>', conf)

    result = ''

    res = StringVar()

    k = 0

    for i in element:
        result_rad = Radiobutton(frame_canvas, text=i, value=i, variable=res, state=NORMAL)
        result_rad.grid(row=k, column=0, sticky='w')
        result_rad.bind('<Double-1>', select)
        k += 1

    print(result)

    #return result
