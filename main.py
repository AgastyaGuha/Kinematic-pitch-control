import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
from physics import compute_tti_and_risk, get_formation
from graphics import draw_2d_pitch, render_tactical_overlay

class ProTacticalDashboard:
    def __init__(self):
        self.home_pos = get_formation('4-3-3', team='home')
        self.away_pos = get_formation('4-4-2', team='away')
        
        self.pass_start = self.home_pos[9] 
        self.pass_end = self.home_pos[10]  
        self.selected_player = None 
        self.drag_threshold = 3.0   
        self.action_mode = 'Drag Player' 
        self.is_dragging = False 
        
        self.fig = plt.figure(figsize=(14, 8))
        self.fig.patch.set_facecolor('#1e1e1e')
        self.ax_pitch = plt.axes([0.05, 0.05, 0.7, 0.9])
        
        self.ax_mode = plt.axes([0.8, 0.65, 0.15, 0.2], facecolor='#2b2b2b')
        self.ax_mode.set_title("Coaching Tool", color='white', fontweight='bold')
        self.radio_mode = RadioButtons(self.ax_mode, ('Drag Player', 'Draw Pass', 'Draw Shot'), activecolor='#2980b9')
        for label in self.radio_mode.labels: label.set_color('white')
        self.radio_mode.on_clicked(self.set_mode)
        
        self.ax_form = plt.axes([0.8, 0.35, 0.15, 0.2], facecolor='#2b2b2b')
        self.ax_form.set_title("Home Formation", color='white', fontweight='bold')
        self.radio_form = RadioButtons(self.ax_form, ('4-3-3', '4-4-2', '4-2-3-1'), activecolor='#ff4d4d')
        for label in self.radio_form.labels: label.set_color('white')
        self.radio_form.on_clicked(self.set_formation)

        self.fig.canvas.mpl_connect('button_press_event', self.on_press)
        self.fig.canvas.mpl_connect('button_release_event', self.on_release)
        self.fig.canvas.mpl_connect('motion_notify_event', self.on_motion)
        
        self.update_board(fast_mode=False)

    def set_mode(self, label):
        self.action_mode = label
        if label == 'Draw Shot':
            self.pass_end = np.array([52.5, 0, 0, 0])
        self.update_board(fast_mode=False)
        
    def set_formation(self, label):
        self.home_pos = get_formation(label, team='home')
        self.pass_start = self.home_pos[9]
        self.update_board(fast_mode=False)

    def update_board(self, fast_mode=False):
        self.ax_pitch.clear()
        draw_2d_pitch(self.ax_pitch)
        
        if fast_mode:
            render_tactical_overlay(self.ax_pitch, self.action_mode, self.home_pos, self.away_pos, 
                                    self.pass_start, self.pass_end, fast_mode=True)
        else:
            v_ball = 25.0 if self.action_mode == 'Draw Shot' else 15.0
            
            xx, yy, control_grid, lane, def_controls, risk = compute_tti_and_risk(
                self.home_pos, self.away_pos, self.pass_start, self.pass_end, v_ball=v_ball
            )
            render_tactical_overlay(self.ax_pitch, self.action_mode, self.home_pos, self.away_pos, 
                                    self.pass_start, self.pass_end, xx, yy, control_grid, 
                                    lane, def_controls, risk, fast_mode=False)
        
        self.fig.canvas.draw_idle()

    def on_press(self, event):
        if event.inaxes != self.ax_pitch: return
        click_pos = np.array([event.xdata, event.ydata])
        
        if self.action_mode == 'Drag Player':
            h_dists = np.linalg.norm(self.home_pos[:, :2] - click_pos, axis=1)
            if np.min(h_dists) < self.drag_threshold:
                self.selected_player = ('home', np.argmin(h_dists))
                self.is_dragging = True
                return
            a_dists = np.linalg.norm(self.away_pos[:, :2] - click_pos, axis=1)
            if np.min(a_dists) < self.drag_threshold:
                self.selected_player = ('away', np.argmin(a_dists))
                self.is_dragging = True
                
        elif self.action_mode in ['Draw Pass', 'Draw Shot']:
            h_dists = np.linalg.norm(self.home_pos[:, :2] - click_pos, axis=1)
            if np.min(h_dists) < self.drag_threshold:
                self.pass_start = self.home_pos[np.argmin(h_dists)]
                
            if self.action_mode == 'Draw Pass':
                self.pass_end = np.array([event.xdata, event.ydata, 0.0, 0.0])
            elif self.action_mode == 'Draw Shot':
                self.pass_end = np.array([52.5, 0.0, 0.0, 0.0])
                
            self.update_board(fast_mode=False)

    def on_motion(self, event):
        if event.inaxes != self.ax_pitch: return
        
        # Allows player dragging
        if self.action_mode == 'Drag Player' and self.is_dragging and self.selected_player is not None:
            team, idx = self.selected_player
            if team == 'home': 
                self.home_pos[idx, 0:2] = [event.xdata, event.ydata]
            else: 
                self.away_pos[idx, 0:2] = [event.xdata, event.ydata]
            self.update_board(fast_mode=True) 

        # Allows dragging the pass line across the pitch dynamically
        elif self.action_mode == 'Draw Pass' and event.button == 1:
            self.pass_end = np.array([event.xdata, event.ydata, 0.0, 0.0])
            self.update_board(fast_mode=False)

    def on_release(self, event):
        if self.is_dragging:
            self.is_dragging = False
            self.selected_player = None
            self.update_board(fast_mode=False)

if __name__ == "__main__":
    dashboard = ProTacticalDashboard()
    plt.show()
