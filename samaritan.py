# Copyright (c) 2017 Devin Gund
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

import tkinter as tk
import tkinter.font as tkfont

class OutputDisplay(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # Label for displaying output text
        self.textlabel = tk.Label(self, text='SAMARITAN')
        self.textlabel.pack(fill='x', expand=True)

        # Underline for the text
        self.textline = tk.Canvas(self, bg='#000000', height=2, highlightthickness=0, borderwidth=0)
        self.textline.pack(pady=7, fill='x', expand=True)

        # Prompt triangle
        self.prompt = tk.Canvas(self, highlightthickness=0, borderwidth=0)
        self.prompt.pack(fill='x', expand=True)
        self.prompt.bind('<Configure>', self.event_resize_prompt)

    def textlabel_font_with_size(self, size):
        return tkfont.Font(root=self, family='MagdaCleanMono', size=size, weight='bold')

    def layout_for_size(self, width, height):
        # Textline attributes
        textline_height = 2

        # Textlabel attributes
        half_height = (height - textline_height) // 2
        textlabel_height = max(half_height, 25)
        textlabel_font = self.textlabel_font_with_size(textlabel_height)

        # Prompt attributes
        prompt_height = textlabel_height

        self.textline.config(height=textline_height, width=width)
        self.textlabel.config(font=textlabel_font)
        self.prompt.config(height=prompt_height, width=width)

    def event_resize_prompt(self, event):
        self.prompt.delete('all')
        x_center = event.width // 2
        prompt_height = event.height
        prompt_width = int((4 / 3) * prompt_height)

        v0 = (x_center, 0)
        v1 = (x_center - prompt_width//2, prompt_height)
        v2 = (x_center + prompt_width//2, prompt_height)
        self.prompt.create_polygon(v0, v1, v2, fill='#ff0023')


class SamaritanUI(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.bind('<Configure>', self.event_resize)

        self.output_display = OutputDisplay(self)
        self.output_display.place(in_=self, anchor='c', relx=.5, rely=.5)

    def event_resize(self, event):
        self.layout_for_size(event.width, event.height)

    def layout_for_size(self, width, height):
        output_display_width = width // 10
        output_display_height = height // 10
        self.output_display.layout_for_size(output_display_width, output_display_height)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Samaritan')
    root.geometry('800x600')
    SamaritanUI(root).pack(fill='both', expand=True)
    root.mainloop()
