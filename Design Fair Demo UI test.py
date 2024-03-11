import matplotlib.pyplot as plt
import numpy as np

from matplotlib.widgets import Button, Slider

max_dissonance = 1
min_dissonance = 0

# Define initial parameters
init_dissonance1 = min_dissonance
init_dissonance2 = max_dissonance/3
init_dissonance3 = 2*max_dissonance/3
init_dissonance4 = max_dissonance
init_dissonance5 = min_dissonance

# Create the figure and the line that we will manipulate
fig, ax = plt.subplots()
line, = ax.plot([0,1,2,3,4], [init_dissonance1, init_dissonance2, init_dissonance3, init_dissonance4, init_dissonance5], lw=2)

# adjust the main plot to make room for the sliders
fig.subplots_adjust(bottom=0.5)

SliderWidth = 0.0225
SliderHeight = 0.3
FirstSliderXpos = 0.15
SliderSpacing = 0.155
SliderYpos = 0.1

# Make Sliders.
axDis1 = fig.add_axes([FirstSliderXpos, SliderYpos, SliderWidth, SliderHeight])
dis_slider1 = Slider(
    ax=axDis1,
    label="",
    valmin=min_dissonance,
    valmax=max_dissonance,
    valinit=init_dissonance1,
    orientation="vertical"
)

axDis2 = fig.add_axes([FirstSliderXpos+((2-1) * (SliderWidth + SliderSpacing)), SliderYpos, SliderWidth, SliderHeight])
dis_slider2 = Slider(
    ax=axDis2,
    label="",
    valmin=min_dissonance,
    valmax=max_dissonance,
    valinit=init_dissonance2,
    orientation="vertical"
)

axDis3 = fig.add_axes([FirstSliderXpos+((3-1) * (SliderWidth+SliderSpacing)), SliderYpos, SliderWidth, SliderHeight])
dis_slider3 = Slider(
    ax=axDis3,
    label="",
    valmin=min_dissonance,
    valmax=max_dissonance,
    valinit=init_dissonance3,
    orientation="vertical"
)

axDis4 = fig.add_axes([FirstSliderXpos+((4-1) * (SliderWidth+SliderSpacing)), SliderYpos, SliderWidth, SliderHeight])
dis_slider4 = Slider(
    ax=axDis4,
    label="",
    valmin=min_dissonance,
    valmax=max_dissonance,
    valinit=init_dissonance4,
    orientation="vertical"
)

axDis5 = fig.add_axes([FirstSliderXpos+((5-1) * (SliderWidth+SliderSpacing)), SliderYpos, SliderWidth, SliderHeight])
dis_slider5 = Slider(
    ax=axDis5,
    label="",
    valmin=min_dissonance,
    valmax=max_dissonance,
    valinit=init_dissonance5,
    orientation="vertical"
)

# The function to be called anytime a slider's value changes
def update(val):
    line.set_ydata([dis_slider1.val, dis_slider2.val, dis_slider3.val, dis_slider4.val, dis_slider5.val])
    fig.canvas.draw_idle()

# register the update function with each slider
dis_slider1.on_changed(update)
dis_slider2.on_changed(update)
dis_slider3.on_changed(update)
dis_slider4.on_changed(update)
dis_slider5.on_changed(update)

# Create a `matplotlib.widgets.Button` to reset the sliders to initial values.
generateAx = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(generateAx, 'Generate', hovercolor='0.975')

def generate(event):
    print([dis_slider1.val, dis_slider2.val, dis_slider3.val, dis_slider4.val, dis_slider5.val])

button.on_clicked(generate)

plt.show()