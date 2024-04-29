# OR-Solver

An Operations Research Course Project.

In this Project, we used ``QT 5`` for GUI and ``Gurobi`` as a solver.

The problems we are solving are:

- [Knapsack Problem](#knapsack-problem)
- [Transportation Cost Problem](#transportation-cost-problem)

## Installation

1. Run these commands:

```bash
pip install pygurobi
pip install PyQt5
```

2. Run this command:

```bash
py main.py
```

## Project Structure

These are the Project's **classes**:

- **`HomePage`**:
  - Has buttons to navigate to the Knapsack and Transportation problem solvers.
  - Switch views based on button clicks.
  
- **`KnapsackSolver` and `TransportationSolver`**:
  - Each contains a back button to navigate back to the Home Page.
  - Each presents a UI for a solver.

- **`MainApp`**:
  - Manages a stack of widgets (`QStackedWidget`) which contains all three pages.
  - Controls transitions between these pages using the **stack's index**.

## Knapsack Problem

The **knapsack problem** presents a classic optimization challenge:

Given a set of items each with its own **weight** and **value**, and a knapsack with a **maximum weight capacity**, how do we **maximize** the **total value** of items placed into the knapsack **without surpassing its weight limit**?

This problem finds applications in various fields such as resource allocation, financial portfolio optimization, and even in scheduling tasks.

### Context

Imagine you're planning a hiking trip and can only carry a limited weight in your backpack. You have a list of items, each with its weight and value. Your goal is to select the most valuable combination of items that fit into your backpack without exceeding its weight capacity. This is precisely the knapsack problem in a real-life scenario and the origin of the naming.

### Mathematical Formulation

To tackle this problem mathematically, we define:

- **Items**: \( n \) items, each with a value \( v_i \) and weight \( w_i \).
- **Knapsack Capacity**: Maximum weight \( W \) that the knapsack can carry.

Our **aim** is to decide which items to include in the knapsack to maximize the total value while staying within the weight **constraint**. We can express this as an **integer programming problem**:

- **Decision Variables**: \( x_i \), where \( x_i = 1 \) if item \( i \) is included in the knapsack, and \( x_i = 0 \) otherwise.
- **Objective Function**: Maximize \( \sum_{i=1}^n v_i x_i \), which represents the total value of the selected items.
- **Constraint**: \( \sum_{i=1}^n w_i x_i \leq W \), ensuring the total weight of the selected items doesn't exceed the knapsack's capacity.

### Implementation with Python and Gurobi

Using the Gurobi optimization solver in Python, we can efficiently solve the knapsack problem.

Here's how:

1. **Model Initialization**: We start by creating a Gurobi model.
2. **Variables**: We add **binary decision** (hence the integer programming) variables for each item to indicate whether it's included in the knapsack or not.
3. **Objective Function**: Our goal is to maximize the total value of the selected items.
4. **Constraint**: We impose a constraint to limit the total weight of the selected items.
5. **Optimization and Output**: Finally, we optimize the model and display the solution, revealing the optimal value and the items to include.

## Transportation Cost Problem

***The transportation problem is a type of `linear programming` problem designed to minimize the cost of distributing a product from M sources to N destinations.***

The transportation problem is a classic optimization problem in operations research and logistics that seeks to distribute goods or resources from **multiple origins (supply points)** to **multiple destinations (demand points)** in the most cost-effective way while satisfying supply and demand constraints. This problem is applicable in various scenarios, including logistics, supply chain management, and network design.

### Problem Overview

In the transportation problem, we have:

- A set of sources \( i \) where goods are supplied.
- A set of destinations \( j \) where goods are demanded.
- A supply amount \( s_i \) at each source \( i \).
- A demand amount \( d_j \) at each destination \( j \).
- A cost \( c_{ij} \) associated with transporting one unit of good from source \( i \) to destination \( j \).

The goal is to determine the quantity \( x_{ij} \) of goods to be transported from each source \( i \) to each destination \( j \) such that the total transportation cost is minimized, all demands are satisfied, and supplies are not exceeded.

### Assumptions

- Each source's supply and each destination's demand are known and fixed.
- Transportation costs per unit are known and constant.
- The problem assumes linear costs without economies of scale.

### Mathematical Model

The linear programming formulation of the transportation problem is as follows:

### Objective Function

Minimize the total transportation cost:
\[ \min Z = \sum_{i=1}^{m} \sum_{j=1}^{n} c_{ij} x_{ij} \]
where \( m \) is the number of sources, \( n \) is the number of destinations, \( c_{ij} \) is the cost per unit transported from source \( i \) to destination \( j \), and \( x_{ij} \) is the quantity transported.

### Constraints

1. **Supply Constraints:** Ensure that the total amount transported from each source does not exceed its supply.
   \[ \sum_{j=1}^{n} x_{ij} \leq s_i \quad \forall i \]
2. **Demand Constraints:** Ensure that the total amount transported to each destination meets its demand.
   \[ \sum_{i=1}^{m} x_{ij} = d_j \quad \forall j \]
3. **Non-negativity Constraints:** The quantities transported must be non-negative.
   \[ x_{ij} \geq 0 \quad \forall i, \forall j \]

**For further great explanation also check this [Link](https://www.imsl.com/blog/solving-transportation-problem)**
