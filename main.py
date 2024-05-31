from simulation import Simulator
import numpy as np
import sys
import os
np.random.seed(8)


def output_mrt2file(simulator, filename):
    response_time = {"0": [], "1": [], "r0": []}
    for job in simulator.departed_jobs:
        response_time[job.real_category].append(job.departure_time - job.arrival_time)
    m_r_0, m_r_1 = np.array(response_time["0"]).mean(), np.array(response_time["1"]).mean()
    with open(filename, "w") as f:
        f.write(f"{m_r_0:.4f} {m_r_1:.4f}")


def output_dep2file(simulator, filename):
    with open(filename, "w") as f:
        for job in simulator.departed_jobs:
            f.write(f"{job.arrival_time:.4f} {job.departure_time:.4f} {job.real_category}\n")


def main(s):
    out_folder = 'output'
    config_folder = 'config'
    mode_file = os.path.join(config_folder, 'mode_' + s + '.txt')
    para_file = os.path.join(config_folder, 'para_' + s + '.txt')
    interarrival_file = os.path.join(config_folder, 'interarrival_' + s + '.txt')
    service_file = os.path.join(config_folder, 'service_' + s + '.txt')

    dep_file = os.path.join(out_folder, 'dep_' + s + '.txt')
    mrt_file = os.path.join(out_folder, 'mrt_' + s + '.txt')

    sim = Simulator(mode_file, para_file, interarrival_file, service_file)
    sim.simulate()
    output_dep2file(sim, dep_file)
    output_mrt2file(sim, mrt_file)


if __name__ == "__main__":
    main(sys.argv[1])
