import numpy as np
import matplotlib.pyplot as plt

m_a = 5.972 * (10 ** 24)
m_b = 1.989 * (10 ** 30)
g = 6.674 * (10 ** -11)

cor_a = np.array([-1.5 * (10 ** 8), 0, 0])
cor_b = np.array([0, 0, 0])
v_a = np.array([0, -1.1 * 10 ** 6, 0])
v_b = np.array([0, 0, 0])

r = np.linalg.norm(cor_a - cor_b)
f = g * (m_a * m_b) / (r ** 2)

dt = 1

positions_a = [cor_a]
positions_b = [cor_b]

while np.linalg.norm(cor_a) < (10 ** 10) and r > (10 ** 6):
    r = np.linalg.norm(cor_a - cor_b)
    f = g * (m_a * m_b) / (r ** 2)
    a_a = (cor_b - cor_a) / r * f / m_a
    v_a += a_a * dt
    cor_a = cor_a + v_a * dt
    positions_a.append(cor_a)
# convert positions to arrays for plotting
positions_a = np.array(positions_a)
positions_b = np.array(positions_b)

# plot the trajectory
plt.plot(positions_a[:, 0], positions_a[:, 1], label='Object A', color='white')
plt.scatter(positions_b[:, 0], positions_b[:, 1], color='yellow', label='Object B')
plt.xlabel('x position (m)')
plt.ylabel('y position (m)')
plt.title('Trajectory of Object A around Object B')
plt.legend()
plt.grid()
plt.show()
