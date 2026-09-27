import numpy as np
from scipy.spatial.distance import cdist

def get_formation(formation, team='home'):
    if formation == '4-3-3':
        pos = [[-45, 0], [-15, -20], [-25, -10], [-25, 10], [-15, 20], 
               [-5, -15], [-10, 0], [-5, 15], 
               [15, -20], [20, 0], [15, 20]]
    elif formation == '4-4-2':
        pos = [[-45, 0], [-20, -25], [-25, -10], [-25, 10], [-20, 25], 
               [-5, -25], [-10, -10], [-10, 10], [-5, 25], 
               [15, -10], [15, 10]]
    else:
        pos = [[-45, 0], [-20, -25], [-25, -10], [-25, 10], [-20, 25], 
               [-10, -10], [-10, 10], 
               [5, -20], [5, 0], [5, 20], 
               [20, 0]]
        
    pos = np.array(pos, dtype=float)
    if team == 'away':
        pos[:, 0] *= -1 
        pos[:, 1] *= -1
        pos[:, 0] -= 15 
    return pos

def compute_tti_and_risk(home_pos, away_pos, pass_start, pass_end, v_max=5.0):
    x_grid = np.arange(-52.5, 53.5, 1.0)
    y_grid = np.arange(-34.0, 35.0, 1.0)
    xx, yy = np.meshgrid(x_grid, y_grid)
    grid_points = np.column_stack((xx.ravel(), yy.ravel()))
    
    h_dist = cdist(grid_points, home_pos)
    a_dist = cdist(grid_points, away_pos)
    
    h_tti = h_dist / v_max
    a_tti = a_dist / v_max
    
    control_grid = np.where(np.min(h_tti, axis=1) < np.min(a_tti, axis=1), 1, 0).reshape(xx.shape)
    
    t_values = np.linspace(0, 1, 30)
    lane_points = pass_start + np.outer(t_values, (pass_end - pass_start))
    
    lane_h_dist = cdist(lane_points, home_pos)
    lane_a_dist = cdist(lane_points, away_pos)
    
    lane_h_tti = lane_h_dist / v_max
    lane_a_tti = lane_a_dist / v_max
    
    defender_controls = np.min(lane_a_tti, axis=1) < np.min(lane_h_tti, axis=1)
    risk_score = np.sum(defender_controls) / 30.0
    
    return xx, yy, control_grid, lane_points, defender_controls, risk_score