import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
from physics import compute_tti_and_risk, get_formation
from graphics import draw_2d_pitch

class ProTacticalDashboard:
    def __init__(self):
        self.home_pos = get_formation('4-3-3', team='home')
        self.away_pos = get_formation('4-4-2', team='away')
        
        self.pass_start = self.home_pos[9] 
        self.pass_end = self.home_pos[10]  
        self.selected_player = None 
        self.drag_threshold = 3.0   
        self.action_mode = 'Drag Player' 
        
        self.fig = plt.figure(figsize=(14, 8))
        self.fig.patch.set_facecolor('#1e1e1e')
        self.ax_pitch = plt.axes([0.05, 0.05, 0.7, 0.9])
        
        self.ax_mode = plt.axes([0.8, 0.65, 0.15, 0.2], facecolor='#2b2b2b')
        self.ax_mode.set_title("Coaching Tool", color='white', fontweight='bold')
        self.radio_mode = RadioButtons(self.ax_mode, ('Drag Player', 'Draw Pass', 'Draw Shot'), activecolor='#2980b9')
        
        for label in self.radio_mode.labels:
            label.set_color('white')
            
        self.radio_mode.on_clicked(self.set_mode)
        
        self.ax_form = plt.axes([0.8, 0.35, 0.15, 0.2], facecolor='#2b2b2b')
        self.ax_form.set_title("Home Formation", color='white', fontweight='bold')
        self.radio_form = RadioButtons(self.ax_form, ('4-3-3', '4-4-2', '4-2-3-1'), activecolor='#ff4d4d')
        
        for label in self.radio_form.labels:
            label.set_color('white')
            
        self.radio_form.on_clicked(self.set_formation)

        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        
        self.update_board()

    def set_mode(self, label):
        self.action_mode = label
        
    def set_formation(self, label):
        self.home_pos = get_formation(label, team='home')
        self.update_board()

    def update_board(self):
        self.ax_pitch.clear()
        draw_2d_pitch(self.ax_pitch)
        
        xx, yy, control_grid, lane, def_controls, risk = compute_tti_and_risk(
            self.home_pos, self.away_pos, self.pass_start, self.pass_end
        )
        
        self.ax_pitch.contourf(xx, yy, control_grid, levels=[-0.5, 0.5, 1.5], colors=['#2980b9', '#c0392b'], alpha=0.4)
        self.ax_pitch.plot([self.pass_start[0], self.pass_end[0]], [self.pass_start[1], self.pass_end[1]], color='white', linestyle='--', zorder=4)
        
        safe_pts, risky_pts = lane[~def_controls], lane[def_controls]
        if len(safe_pts) > 0:
            self.ax_pitch.scatter(safe_pts[:,0], safe_pts[:,1], color='#00e676', s=40, zorder=5)
        if len(risky_pts) > 0:
            self.ax_pitch.scatter(risky_pts[:,0], risky_pts[:,1], color='#ff1744', marker='X', s=50, zorder=5)
            
        self.ax_pitch.scatter(self.home_pos[:,0], self.home_pos[:,1], color='#ff4d4d', s=120, edgecolors='white', lw=1.5, zorder=6)
        self.ax_pitch.scatter(self.away_pos[:,0], self.away_pos[:,1], color='#3498db', s=120, edgecolors='white', lw=1.5, zorder=6)
        
        if self.action_mode == 'Draw Shot':
            title = f"Expected Block Probability: {risk * 100:.1f}%"
            self.ax_pitch.plot(52.5, 0, marker='*', color='gold', markersize=15, zorder=7)
        else:
            title = f"Pass Interception Risk: {risk * 100:.1f}%"
            
        self.ax_pitch.set_title(title, color='white', fontsize=16, fontweight='bold', pad=15)
        self.fig.canvas.draw()

    def on_press(self, event):
        if event.inaxes != self.ax_pitch: return
        click_pos = np.array([event.xdata, event.ydata])
        
        if self.action_mode == 'Drag Player':
            h_dists = np.linalg.norm(self.home_pos - click_pos, axis=1)
            if np.min(h_dists) < self.drag_threshold:
                self.selected_player = ('home', np.argmin(h_dists))
                return
            a_dists = np.linalg.norm(self.away_pos - click_pos, axis=1)
            if np.min(a_dists) < self.drag_threshold:
                self.selected_player = ('away', np.argmin(a_dists))
                
        elif self.action_mode in ['Draw Pass', 'Draw Shot']:
            h_dists = np.linalg.norm(self.home_pos - click_pos, axis=1)
            self.pass_start = self.home_pos[np.argmin(h_dists)]
            
            if self.action_mode == 'Draw Shot':
                self.pass_end = np.array([52.5, 0])
            else:
                self.pass_end = click_pos
            self.update_board()

    def on_motion(self, event):
        if event.inaxes != self.ax_pitch: return
        
        if self.action_mode == 'Drag Player' and self.selected_player:
            team, idx = self.selected_player
            if team == 'home': self.home_pos[idx] = [event.xdata, event.ydata]
            else: self.away_pos[idx] = [event.xdata, event.ydata]
            self.update_board()
            
        elif self.action_mode == 'Draw Pass' and event.button == 1:
            self.pass_end = np.array([event.xdata, event.ydata])
            self.update_board()

    def on_release(self, event):
        self.selected_player = None

if __name__ == "__main__":
    dashboard = ProTacticalDashboard()
    plt.show()