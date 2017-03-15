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

class Frame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super(Frame, self).__init__(parent, *args, **kwargs)
        self.parent = parent

    def layout_for_size(width, height):
        raise NotImplementedError()


class OutputTextUI(Frame):
    def __init__(self, parent, *args, **kwargs):
        super(OutputTextUI, self).__init__(parent, *args, **kwargs)

        self.font = self._font_with_size(1)
        self.line_color = '#000000'
        self.line_height_scale = .05
        self._text = ''
        self._line_width_min = 0

        self.label = tk.Label(self)
        self.label.pack()

        self.line = tk.Canvas(self, bg=self.line_color, highlightthickness=0, borderwidth=0)
        self.line.pack()

    def layout_for_size(self, width, height):
        line_height = max(int(height * self.line_height_scale), 2)
        self.line.config(bg=self.line_color, height=line_height)

        label_height = height - line_height
        self.font = self._font_with_size(label_height)

        self._line_width_min = label_height

        self.set_text(self._text)

    def set_text(self, text):
        self._text = text
        self.label.config(text=text, font=self.font)

        line_width = max(self.font.measure(text), self._line_width_min)
        self.line.config(width=line_width)

    def _font_with_size(self, size):
        return tkfont.Font(root=self, family='MagdaCleanMono', size=size, weight='bold')


class OutputPromptUI(Frame):
    def __init__(self, parent, *args, **kwargs):
        super(OutputPromptUI, self).__init__(parent, *args, **kwargs)

        self.canvas = tk.Canvas(self, highlightthickness=0, borderwidth=0)
        self.canvas.pack(fill='both', expand=True)

        self.canvas_shape = None

        self.color = '#ff0023'

    def layout_for_size(self, width, height):
        self.canvas.config(width=width, height=height)
        self._update_canvas_for_size(width, height)

    def _update_canvas_for_size(self, width, height):
        if self.canvas_shape:
            self.canvas.delete(self.canvas_shape)
            self.canvas_shape = None

        x_center = width // 2
        prompt_height = height
        prompt_width = int((4 / 3) * prompt_height)

        v0 = (x_center, 0)
        v1 = (x_center - prompt_width//2, prompt_height)
        v2 = (x_center + prompt_width//2, prompt_height)
        self.canvas_shape = self.canvas.create_polygon(v0, v1, v2, fill=self.color)


class OutputUI(Frame):
    def __init__(self, parent, *args, **kwargs):
        super(OutputUI, self).__init__(parent, *args, **kwargs)

        self.text = OutputTextUI(self)
        self.prompt = OutputPromptUI(self)

        self.text.pack(pady=5)
        self.prompt.pack()

    def layout_for_size(self, width, height):
        height_text = int(height * .6)
        height_prompt = int(height * .4)
        self.text.layout_for_size(width, height_text)
        self.prompt.layout_for_size(width, height_prompt)


class SamaritanUI(Frame):
    def __init__(self, parent, *args, **kwargs):
        super(SamaritanUI, self).__init__(parent, *args, **kwargs)
        self.bind('<Configure>', self.event_resize)

        self.output = OutputUI(self)
        self.output.place(in_=self, anchor='c', relx=.5, rely=.5)

        self.output_width_scale = .1
        self.output_height_scale = .1
        self.output_width_min = 80
        self.output_height_min = 60

    def event_resize(self, event):
        self.layout_for_size(event.width, event.height)

    def layout_for_size(self, width, height):
        output_width = max(int(width * self.output_width_scale),
                           self.output_width_min)
        output_height = max(int(height * self.output_height_scale),
                            self.output_height_min)
        self.output.layout_for_size(output_width, output_height)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Samaritan')
    root.geometry('800x600')
    SamaritanUI(root).pack(fill='both', expand=True)
    root.mainloop()
