import matplotlib.pyplot as plt

def draw_2d_pitch(ax, background_color='#2b2b2b', line_color='white'):
    ax.set_facecolor(background_color)
    ax.plot([-52.5, 52.5, 52.5, -52.5, -52.5], [-34, -34, 34, 34, -34], color=line_color, lw=2) 
    ax.plot([0, 0], [-34, 34], color=line_color, lw=2)
    ax.add_patch(plt.Circle((0, 0), 9.15, color=line_color, fill=False, lw=2))
    ax.plot([-52.5, -36, -36, -52.5], [-20.16, -20.16, 20.16, 20.16], color=line_color, lw=2)
    ax.plot([52.5, 36, 36, 52.5], [-20.16, -20.16, 20.16, 20.16], color=line_color, lw=2)
    ax.plot([-52.5, -47, -47, -52.5], [-9.16, -9.16, 9.16, 9.16], color=line_color, lw=2)
    ax.plot([52.5, 47, 47, 52.5], [-9.16, -9.16, 9.16, 9.16], color=line_color, lw=2)
    
    ax.set_xlim(-55, 55)
    ax.set_ylim(-37, 37)
    ax.set_xticks([])
    ax.set_yticks([])