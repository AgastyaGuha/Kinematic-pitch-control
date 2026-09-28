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

def render_tactical_overlay(ax, action_mode, home_pos, away_pos, pass_start, pass_end, 
                            xx=None, yy=None, control_grid=None, 
                            lane=None, def_controls=None, risk=0.0, fast_mode=False):
    
    if not fast_mode and control_grid is not None:
        ax.contourf(xx, yy, control_grid, levels=[-0.5, 0.5, 1.5], colors=['#2980b9', '#c0392b'], alpha=0.4)
        ax.plot([pass_start[0], pass_end[0]], [pass_start[1], pass_end[1]], color='white', linestyle='--', zorder=4)
        
        safe_pts, risky_pts = lane[~def_controls], lane[def_controls]
        if len(safe_pts) > 0:
            ax.scatter(safe_pts[:,0], safe_pts[:,1], color='#00e676', s=40, zorder=5)
        if len(risky_pts) > 0:
            ax.scatter(risky_pts[:,0], risky_pts[:,1], color='#ff1744', marker='X', s=50, zorder=5)
            
    ax.scatter(home_pos[:,0], home_pos[:,1], color='#ff4d4d', s=120, edgecolors='white', lw=1.5, zorder=6)
    ax.scatter(away_pos[:,0], away_pos[:,1], color='#3498db', s=120, edgecolors='white', lw=1.5, zorder=6)
    
    if not fast_mode:
        if action_mode == 'Draw Shot':
            title = f"Expected Block Probability: {risk * 100:.1f}%"
            ax.plot(52.5, 0, marker='*', color='gold', markersize=15, zorder=7)
        else:
            title = f"Pass Interception Risk: {risk * 100:.1f}%"
        ax.set_title(title, color='white', fontsize=16, fontweight='bold', pad=15)
    else:
        ax.set_title("Recalculating...", color='#f1c40f', fontsize=16, fontweight='bold', pad=15)
