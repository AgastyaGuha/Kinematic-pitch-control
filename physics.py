import numpy as np
from scipy.spatial.distance import cdist

def get_formation(formation, team='home'):
    if formation == '4-3-3':
        pos = [[-45, 0], [-15, -20], [-25, -10], [-25, 10], [-15, 20], 
               [-5, -15], [-10, 0], [-5, 15], [15, -20], [20, 0], [15, 20]]
    elif formation == '4-4-2':
        pos = [[-45, 0], [-20, -25], [-25, -10], [-25, 10], [-20, 25], 
               [-5, -25], [-10, -10], [-10, 10], [-5, 25], [15, -10], [15, 10]]
    else:
        pos = [[-45, 0], [-20, -25], [-25, -10], [-25, 10], [-20, 25], 
               [-10, -10], [-10, 10], [5, -20], [5, 0], [5, 20], [20, 0]]
        
    pos = np.array(pos, dtype=float)
    
    vx = np.full((11, 1), 2.5) if team == 'home' else np.full((11, 1), 1.5)
    vy = np.zeros((11, 1))
    
    if team == 'away':
        pos[:, 0] *= -1 
        pos[:, 0] -= 15 
        
    return np.hstack((pos, vx, vy))

def compute_tti_and_risk(home_state, away_state, pass_start, pass_end, v_max=5.0, t_react=0.7, v_ball=15.0):
    h_pos, h_vel = home_state[:, 0:2], home_state[:, 2:4]
    a_pos, a_vel = away_state[:, 0:2], away_state[:, 2:4]
    
    h_p_react = h_pos + (h_vel * t_react)
    a_p_react = a_pos + (a_vel * t_react)

    x_grid = np.arange(-52.5, 53.5, 1.0)
    y_grid = np.arange(-34.0, 35.0, 1.0)
    xx, yy = np.meshgrid(x_grid, y_grid)
    grid_points = np.column_stack((xx.ravel(), yy.ravel()))
    
    h_dist = cdist(grid_points, h_p_react)
    a_dist = cdist(grid_points, a_p_react)
    
    h_tti = t_react + (h_dist / v_max)
    a_tti = t_react + (a_dist / v_max)
    
    control_grid = np.where(np.min(h_tti, axis=1) < np.min(a_tti, axis=1), 1, 0).reshape(xx.shape)
    
    p_start_xy = pass_start[:2]
    p_end_xy = pass_end[:2]
    
    t_values = np.linspace(0, 1, 30)
    lane_points = p_start_xy + np.outer(t_values, (p_end_xy - p_start_xy))
    
    lane_h_dist = cdist(lane_points, h_p_react)
    lane_a_dist = cdist(lane_points, a_p_react)
    
    lane_h_tti = t_react + (lane_h_dist / v_max)
    lane_a_tti = t_react + (lane_a_dist / v_max)
    
    ball_dist = np.linalg.norm(lane_points - p_start_xy, axis=1)
    t_ball = ball_dist / v_ball
    
    min_h_tti = np.min(lane_h_tti, axis=1)
    min_a_tti = np.min(lane_a_tti, axis=1)
    
    defender_controls = (min_a_tti < min_h_tti) & (min_a_tti < t_ball)
    risk_score = np.sum(defender_controls) / 30.0
    
    return xx, yy, control_grid, lane_points, defender_controls, risk_score
