 Pro Tactical Football Dashboard: Kinematic Pitch Control & Pass Risk Engine

Overview
Most football analytics portfolios rely on static charts and simple event counting. This project takes it a step further by building a **Physics-Informed Tactical Engine** from scratch. 

Using **William Spearman's Time-To-Intercept (TTI)** model and linear algebra, this interactive dashboard evaluates spatial dominance, calculates the exact mathematical risk of a passing lane, and models expected shot-block probabilities in real-time.

Built using a strict **Model-View-Controller (MVC)** architecture, the application provides a highly responsive UI where coaches or analysts can drag and drop players to simulate defensive breakdowns and attacking phases.

Core Features
* **Live Pitch Control:** Computes territorial dominance based on kinematics (reaction time + maximum velocity), not just static Voronoi distances.
* **Parametric Pass Risk Evaluation:** Evaluates passing lanes by discretizing the trajectory into 30 mathematical "breadcrumbs" and running a TTI integration to find the exact probability of interception.
* **Expected Block Probability:** Treats shots as high-velocity passes to the goal center `(52.5, 0)` to dynamically calculate how well the defense has closed down the shooting angle.
* **Interactive Drag-and-Drop:** Built using Matplotlib event listeners. Drag any player across the pitch to watch the spatial control algorithms update instantaneously.
* **Tactical Formation Presets:** Instantly snap the 11v11 teams into standard tactical blocks (4-3-3, 4-4-2, 4-2-3-1) to test structural weaknesses.

The Mathematics (The Engine)
Instead of relying on basic Euclidean distance ($d = \sqrt{\Delta x^2 + \Delta y^2}$), this engine uses a kinematic Time-To-Intercept (TTI) model.

1. **Reaction Phase:** $P_{react} = P_{current} + (V \times t_{react})$
2. **Sprint Phase:** $TTI = t_{react} + \frac{D_{remaining}}{v_{max}}$
3. **Passing Lane Integration:** The pass is modeled as a parametric line segment $P(t) = P_{start} + t(P_{end} - P_{start})$. TTI is calculated for all 22 players at 30 discrete intervals along $t$. If $\min(TTI_{Defense}) < \min(TTI_{Attack})$ at a specific point, that segment is flagged as highly vulnerable.

Software Architecture (MVC)
The codebase is fully modularized for O(1) readability and scalable execution:
* `physics.py` **(Model):** Handles all heavy spatial mathematics, NumPy vectorization, and SciPy distance matrices. Purely data-driven.
* `graphics.py` **(View):** Houses the 2D rendering logic, pitch geometries, and aesthetics.
* `main.py` **(Controller):** Manages the application state, 11v11 configurations, Matplotlib UI widgets, and mouse event listeners.

