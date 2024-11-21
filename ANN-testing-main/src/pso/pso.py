from helper_functions.pso_helpers import update_velocity, calculate_fitness
import numpy as np

def particle_swarm_optimisation(y_pred, y_train, dimensions, particles, layers):
    iterations = 0
    cognitive_weight = 1.1

    # The absolute best position & fitness seen by any particle
    best = {
        'weights': [],
        'fitness': float('inf')
    }

    # To track particle positions for visualization
    particle_positions = []

    while iterations < 10:
        current_positions = []
        for idx, particle in enumerate(particles):
            for j, weight in enumerate(particle['weights']):
                fitness = calculate_fitness(y_pred, y_train, layers, particle)

                if best['fitness'] == float('inf') or fitness < best['fitness']:
                    best['weights'] = particle['weights']
                    best['fitness'] = fitness
                    particle['personal_best'][j] = particle['weights']
                    particle['personal_best_fitness'] = fitness

                for dimension in range(dimensions):
                    updated_velocity = update_velocity(
                        particle['velocities'][j],
                        cognitive_weight,
                        weight[j],
                        weight,
                        particle['personal_best'][j][j],
                        particle['personal_best'][j][j],
                        best['weights']
                    )

                    particle['velocities'][j] += updated_velocity
                    particle['weights'][j] += updated_velocity

            # Store the first two dimensions of the weights for visualization
            current_positions.append(particle['weights'][0].ravel()[:2])
        
        particle_positions.append(np.array(current_positions))
        iterations += 1

    return best, particle_positions