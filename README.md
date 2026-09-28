 Pro Tactical Football Dashboard: Kinematic Pitch Control Sandbox

Overview
This project is an interactive tactical sandbox built to model spatial dominance and passing lane risk using kinematic physics. 

Inspired by **William Spearman's Time-To-Intercept (TTI) model**, this dashboard moves beyond static Voronoi diagrams. It evaluates territorial control by calculating a two-phase kinematic model (reaction time + sprint speed) for all 22 players on the pitch. The resulting tool allows coaches or analysts to drag and drop players in a 2D space to simulate defensive breakdowns, evaluate attacking phases, and estimate the interception probability of specific passing lanes.

Core Features
* **Kinematic Pitch Control:** Computes territorial dominance based on an initial momentum vector, a 0.7-second reaction phase, and a maximum sprint velocity to the target grid.
* **Pass Risk Evaluation:** Discretizes a passing lane into 30 intervals and integrates the TTI for both the defense and attack, constrained by the velocity of the ball (15 m/s for passes, 25 m/s for shots).
* **Interactive Tactical Board:** Built entirely in Python using Matplotlib's event listeners and UI widgets. Drag any player across the pitch to watch the spatial control algorithms update instantaneously.
* **Formation Presets:** Instantly snap the 11v11 teams into standard tactical blocks (4-3-3, 4-4-2, 4-2-3-1) to test structural weaknesses.

The Mathematics
Instead of relying on basic Euclidean distance ($d = \sqrt{\Delta x^2 + \Delta y^2}$), this engine estimates pitch control using a simplified Time-To-Intercept (TTI) model.

1. **Reaction Phase:** $P_{react} = P_{start} + (\vec{v}_{initial} \times t_{react})$
2. **Sprint Phase:** $TTI = t_{react} + \frac{D_{remaining}}{v_{max}}$
3. **Interception Logic:** A defender successfully cuts out a pass if their $TTI$ to a point on the passing lane is strictly less than the closest attacker's $TTI$, **and** strictly less than the ball's travel time to that same point.

Software Architecture (MVC)
The codebase is modularized to separate the heavy mathematics from the rendering logic:
* `physics.py` **(Model):** Handles all spatial mathematics, NumPy vectorization, and SciPy distance matrices. 
* `graphics.py` **(View):** Houses the 2D rendering logic, pitch geometries, and Matplotlib contour generation.
* `main.py` **(Controller):** Manages the application state, UI widgets, and throttles mouse event listeners to prevent lag during drag-and-drop actions.

imitations & Future Scope
* Sandbox Assumptions:** Because this is an interactive sandbox rather than a live tracking-data visualizer, player momentum ($\vec{v}_{initial}$) is currently hardcoded based on the phase of play (e.g., attacking team advances at 2.5 m/s, defending team retreats at 1.5 m/s). 
* Future Integration:** The `physics.py` engine is architected to accept continuous $N \times 4$ matrices (`[x, y, vx, vy]`). The immediate next step for this project is to bypass the interactive UI and feed raw, timestamped Metrica tracking CSVs directly into the engine to generate per-player decision-quality report cards over a full 90-minute match.

Acknowledgments
* The pitch control logic in this project is heavily inspired by the foundational work of **William Spearman** ("Pitch Control in Football").

 How to Run Locally

**1. Clone the repository:**
```bash
git clone [https://github.com/AgastyaGuha/football-tactical-dashboard.git](https://github.com/AgastyaGuha/football-tactical-dashboard.git)
cd football-tactical-dashboard
