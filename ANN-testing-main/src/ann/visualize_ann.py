import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx

# === ANN Visualization ===

def visualize_network(layers, nodes):
    """
    Visualizes the structure of the neural network.
    """
    G = nx.DiGraph()
    pos = {}
    node_idx = 0

    # Add nodes and positions
    for layer_idx in range(layers + 1):
        num_nodes = nodes if layer_idx < layers else 1
        for i in range(num_nodes):
            G.add_node(node_idx)
            pos[node_idx] = (layer_idx, i)
            node_idx += 1

    # Add edges
    node_idx = 0
    for layer_idx in range(layers):
        for i in range(nodes):
            for j in range(nodes if layer_idx < layers - 1 else 1):
                G.add_edge(node_idx + i, node_idx + nodes + j)
        node_idx += nodes

    # Draw the graph
    nx.draw(
        G,
        pos,
        with_labels=False,
        node_size=500,
        node_color="skyblue",
        edge_color="gray",
        arrowsize=10,
    )
    plt.title("ANN Architecture", fontsize=16)
    plt.show()

# === Loss Over Iterations ===

def visualize_loss(losses):
    """
    Plots loss over iterations.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(losses, label="Loss", color="red", marker="o")
    plt.xlabel("Iteration")
    plt.ylabel("Loss (MSE)")
    plt.title("Loss Over Iterations")
    plt.legend()
    plt.grid(True)
    plt.show()

# === Particle Optimization Visualization ===

def animate_particles(particles, dimensions, num_frames=20, solution_area=(0.5, 0.5)):
    """
    Animates particles moving in parameter space during PSO.

    Parameters:
    - particles: List of particle dictionaries containing weights and other properties.
    - dimensions: Dimensionality of the parameter space.
    - num_frames: Number of animation frames.
    - solution_area: Tuple (x, y) specifying the area particles converge to.
    """
    # Initialize particle positions as a uniform grid
    grid_size = int(np.ceil(np.sqrt(len(particles))))  # Grid size to fit particles
    x_positions = np.linspace(-1, 1, grid_size)
    y_positions = np.linspace(-1, 1, grid_size)
    grid = np.array([(x, y) for x in x_positions for y in y_positions])
    positions = grid[:len(particles)]  # Take as many positions as there are particles

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.set_title("Particle Swarm Optimization", fontsize=16)

    # Plot solution area for reference
    ax.scatter(*solution_area, color="blue", s=100, label="Solution Area", zorder=2)
    sc = ax.scatter(positions[:, 0], positions[:, 1], c="red", label="Particles", zorder=3)

    ax.legend()

    def update(frame):
        nonlocal positions
        # Move particles closer to the solution area
        positions += (np.array(solution_area) - positions) * 0.1 + np.random.uniform(-0.02, 0.02, positions.shape)
        sc.set_offsets(positions)
        return sc,

    ani = FuncAnimation(fig, update, frames=num_frames, interval=200, blit=True)
    plt.show()

# === Data Flow Visualization ===

def visualize_data_flow(data, layers, particle):
    """
    Visualizes the activation of neurons during the forward pass.
    """
    output = data
    activations = [output]

    # Forward pass
    for i in range(layers):
        weights = particle["weights"][i]
        bias = particle["biases"][i]
        ws = np.dot(output, weights) + bias
        output = np.maximum(0, ws)  # ReLU activation
        activations.append(output)

    # Plot activations
    fig, axes = plt.subplots(1, layers + 1, figsize=(16, 4))
    for i, activation in enumerate(activations):
        ax = axes[i]
        ax.imshow(
            activation.T,
            aspect="auto",
            cmap="coolwarm",
            interpolation="none",
        )
        ax.set_title(f"Layer {i} Activations")
        ax.set_xlabel("Samples")
        ax.set_ylabel("Neurons")
    plt.tight_layout()
    plt.show()
