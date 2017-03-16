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

def rgb_to_hex(rgb_val):
    return '#{:02x}{:02x}{:02x}'.format(rgb_val[0], rgb_val[1], rgb_val[2])

def hex_to_rgb(hex_val):
    hex_val = hex_val.lstrip('#')
    lv = len(hex_val)
    return tuple(int(hex_val[i:i+lv//3], 16) for i in range(0, lv, lv//3))

def blend_colors(foreground, opacity, background):
    (r1, g1, b1) = hex_to_rgb(foreground)
    (r2, g2, b2) = hex_to_rgb(background)

    r = int(r1 * opacity + r2 * (1 - opacity))
    g = int(g1 * opacity + g2 * (1 - opacity))
    b = int(b1 * opacity + b2 * (1 - opacity))
    rgb_result = (r, g, b)

    return rgb_to_hex(rgb_result)

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

        self._blink = False
        self._blink_color = self.color
        self._blink_opacity = 1.0

    def layout_for_size(self, width, height):
        self.canvas.config(width=width, height=height)
        self._update_canvas_for_size(width, height)

    def start_blinking(self):
        if not self._blink:
            self._blink = True
            self._timer_blink()

    def stop_blinking(self):
        if self._blink:
            self._blink = False
            self._timer_blink()

    def _timer_blink(self):
        if self._blink:
            self._blink_opacity -= .10
            if self._blink_opacity < -1.0:
                self._blink_opacity = 1.0
            self._blink_color = blend_colors(self.color, abs(self._blink_opacity), '#ffffff')
            self.canvas.after(30, self._timer_blink)
        else:
            self._blink_opacity = 1.0
            self._blink_color = self.color
        self.canvas.itemconfig(self.canvas_shape, fill=self._blink_color)

    def _update_canvas_for_size(self, width, height):
        if self.canvas_shape:
            self.canvas.delete(self.canvas_shape)
            self.canvas_shape = None

        prompt_color = self._blink_color if self._blink else self.color

        x_center = width // 2
        prompt_height = height
        prompt_width = int((4 / 3) * prompt_height)

        v0 = (x_center, 0)
        v1 = (x_center - prompt_width//2, prompt_height)
        v2 = (x_center + prompt_width//2, prompt_height)
        self.canvas_shape = self.canvas.create_polygon(v0, v1, v2, fill=prompt_color)


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
        self.output.prompt.start_blinking()

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
