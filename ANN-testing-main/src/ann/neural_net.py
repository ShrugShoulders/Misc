# Packages
import random
import pandas as pd
import numpy as np
import time
import os

# Custom Helpers
from activation_functions.activation_functions import relu
from helper_functions.helpers import train_test_split, mse, mae
from helper_functions.pso_helpers import init_informants
from pso.pso import particle_swarm_optimisation

# Visualize The ANN
from ann.visualize_ann import visualize_network, visualize_loss, animate_particles, visualize_data_flow

def predict(layers, nodes, swarm_size=3):
    # Data Pre-Processing
    data = pd.read_csv(os.path.join(os.path.dirname(__file__), '..', 'data', 'concrete_data.csv'))

    # Inputs
    x = data[
        ['cement', 'blast_furnace_slag', 'fly_ash', 'water', 'superplasticizer', 'coarse_aggregate', 'fine_aggregate ',
         'age']].values.copy()
    dimensions = x.shape[1]

    # Output
    y = data[['concrete_compressive_strength']].values.copy()

    # Animate particles instead of visualizing network structure
    particles = []
    max_weight = 0.3
    min_weight = -0.3
    for j in range(swarm_size):
        particle = {
            'weights': [],
            'weights_output': np.random.uniform(min_weight, max_weight, (nodes, 1)),
            'biases': [],
            'velocities': [],
            'bias_velocities': np.random.uniform(-0.1, 0.1, dimensions),
            'fitness': 9999,
            'personal_best': [],
            'personal_best_fitness': 9999,
            'informants': []
        }

        prev_layer_nodes = dimensions
        for i in range(layers):
            weights = np.random.uniform(min_weight, max_weight, (prev_layer_nodes, nodes))
            biases = np.full(nodes, 0.1)
            velocities = np.random.uniform(-0.3, 0.3, (prev_layer_nodes, nodes))
            personal_best = np.zeros((prev_layer_nodes, nodes))

            particle['weights'].append(weights)
            particle['biases'].append(biases)
            particle['velocities'].append(velocities)
            particle['personal_best'].append(personal_best)

            prev_layer_nodes = nodes

        particles.append(particle)

    animate_particles(particles, dimensions)  # Call animate_particles here

    # Initialise Informants
    particles = init_informants(particles)

    # Train, Test Split
    x_train, x_test = train_test_split(x)
    y_train, y_test = train_test_split(y)

    # Misc Params
    num_iterations = 10000
    start_time = time.time()
    np.random.seed(1)

    # Loss Tracking
    losses = []

    for i in range(num_iterations):
        forward_pass_output = x_train

        for idx, particle in enumerate(particles):
            # PSO
            pso_output = particle_swarm_optimisation(forward_pass_output, [], dimensions, particles, layers)
            particle['weights'] = pso_output['weights']

        # Track loss for visualization
        best_particle = min(particles, key=lambda p: p['fitness'])
        predictions = forward_pass(x_train, layers, best_particle)
        loss = mse(y_train, predictions)
        losses.append(loss)

    # Visualize training loss curve
    visualize_loss(losses)

    # Visualize data flow of the best particle
    visualize_data_flow(x_train, layers, best_particle)

    # Output final results
    result = mse(y_train, predictions)
    result_mae = mae(y_train, predictions)
    print('Training time: ', str(time.time() - start_time))
    print('Mean Squared Error (MSE):', result)
    print('Mean Absolute Error (MAE):', result_mae)

# Forward Pass
# Takes in Input Data, Weights and Biases
def forward_pass(data, layers, particle):
    output = data
    for i in range(layers):
        weights = particle['weights'][i]
        bias = particle['biases'][i]
        ws = np.dot(output, weights) + bias
        output = relu(ws)

    return np.dot(output, particle['weights_output']) + particle['biases'][-1][layers]