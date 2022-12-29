import numpy as np
import matplotlib.pyplot as plt
from straight_space_animation import twoD_Harmonic_separable_hamiltonian, dynamics, Step, Trimmed_step

h_initial_conditions = {
    'current_q1': 400,
    'current_q2': -250,
    'w1': 1,
    'w2': 2,
    'res': (800, 800)
}
coords_firstHit = list()
coords_SecondtHit = list()
step = Step()
for i in range(-400, 401):
    stop_iteration = 0
    num_of_hits = 0
    # print(i)
    h_initial_conditions['current_q2'] = i
    h = twoD_Harmonic_separable_hamiltonian(**h_initial_conditions)

    while True:
        dynamics(hamiltonian=h, obstacle=step)

        if stop_iteration > 5000:
            break
        if step.hit_flag:
            if num_of_hits == 0:
                J_2 = 0.5 * h.w2 * (h_initial_conditions['current_q2'] ** 2)
                if h_initial_conditions['current_q2'] == h.previous_q2:
                    theta_wall = np.pi
                else:
                    theta_wall = (np.pi / 2) - np.arctan(
                        h.previous_q2 / np.sqrt(h_initial_conditions['current_q2'] ** 2 - h.previous_q2 ** 2))
                coords_firstHit.append((J_2, theta_wall, h.previous_q1, h.previous_q2, i))
                num_of_hits += 1
            else:
                J_2 = 0.5 * h.w2 * (h_initial_conditions['current_q2'] ** 2)
                if h_initial_conditions['current_q2'] == h.previous_q2:
                    theta_wall = np.pi
                else:
                    theta_wall = (np.pi / 2) - np.arctan(
                        h.previous_q2 / np.sqrt(h_initial_conditions['current_q2'] ** 2 - h.previous_q2 ** 2))
                coords_SecondtHit.append((J_2, theta_wall, h.previous_q1, h.previous_q2, i))
                break
        stop_iteration += 1

J_vertical1 = [val[0] for val in coords_firstHit if val[2] == step.x_right]
theta_vertical1 = [val[1] for val in coords_firstHit if val[2] == step.x_right]
text_J_vertical1 = [f'({val[2]:.1f},{val[3]:.1f})' for val in coords_firstHit if val[2] == step.x_right]
text_J_initial_vertical1 = [f'({val[4]:.1f})' for val in coords_firstHit if val[2] == step.x_right]

J_horizontal1 = [val[0] for val in coords_firstHit if val[3] == step.y_up]
theta_horizontal1 = [val[1] for val in coords_firstHit if val[3] == step.y_up]

J_vertical2 = [val[0] for val in coords_SecondtHit if val[2] == step.x_right]
theta_vertical2 = [val[1] for val in coords_SecondtHit if val[2] == step.x_right]
text_J_vertical2 = [f'({val[2]:.1f},{val[3]:.1f})' for val in coords_SecondtHit if val[2] == step.x_right]
text_J_initial_vertical2 = [f'({val[4]:.1f})' for val in coords_SecondtHit if val[2] == step.x_right]

J_horizontal2 = [val[0] for val in coords_SecondtHit if val[3] == step.y_up]
theta_horizontal2 = [val[1] for val in coords_SecondtHit if val[3] == step.y_up]

#sanity check
x1 = [val[2] for val in coords_SecondtHit]
y1 = [val[3] for val in coords_SecondtHit]

x2 = [val[2] for val in coords_SecondtHit]
y2 = [val[3] for val in coords_SecondtHit]

fig = plt.figure(figsize=(16, 5))  # create a figure
ax1 = fig.add_subplot(1, 2, 1)  # create a subplot of certain size
ax1.scatter(x1, y1, c='r')
ax1.set_title("first hit")

ax2 = fig.add_subplot(1, 2, 2)
ax2.scatter(x2, y2, c='b')
ax2.set_title("second hit")
plt.show()


fig = plt.figure(figsize=(16, 5))  # create a figure
ax1 = fig.add_subplot(1, 2, 1)  # create a subplot of certain size
ax1.scatter(theta_vertical1, J_vertical1, c='r')
# for i, txt in enumerate(text_J_vertical1):
#     ax1.annotate(txt, (theta_vertical1[i], J_vertical1[i]))

ax1.scatter(theta_horizontal1, J_horizontal1, c='b')
ax1.set_title("first hit")

ax2 = fig.add_subplot(1, 2, 2)
ax2.scatter(theta_vertical2, J_vertical2, c='r')
# for i, txt in enumerate(text_J_initial_vertical2):
#     ax2.annotate(txt, (theta_vertical2[i], J_vertical2[i]))
ax2.scatter(theta_horizontal2, J_horizontal2, c='b')
ax2.set_title("second hit")
plt.show()


coords_trim_firstHit = list()
coords_trim_SecondtHit = list()

step = Trimmed_step()
for i in range(-400, 401):
    stop_iteration = 0
    num_of_hits = 0
    # print(i)
    h_initial_conditions['current_q2'] = i
    h = twoD_Harmonic_separable_hamiltonian(**h_initial_conditions)

    while True:
        dynamics(hamiltonian=h, obstacle=step)

        if stop_iteration > 5000:
            break
        if step.hit_flag:
            if num_of_hits == 0:
                J_2 = 0.5 * h.w2 * (h_initial_conditions['current_q2'] ** 2)
                if h_initial_conditions['current_q2'] == h.previous_q2:
                    theta_wall = np.pi
                else:
                    theta_wall = (np.pi / 2) - np.arctan(
                        h.previous_q2 / np.sqrt(h_initial_conditions['current_q2'] ** 2 - h.previous_q2 ** 2))
                coords_trim_firstHit.append((J_2, theta_wall, h.previous_q1, h.previous_q2))
                num_of_hits += 1
            else:
                E_2 = 0.5*(h.current_p2**2)+0.5*((h.w2*h.current_q2)**2)
                J_2 = E_2/h.w2
                q2_max = np.sqrt(2*E_2/h.w2)
                if q2_max == h.previous_q2:
                    theta_wall = np.pi
                else:
                    theta_wall = (np.pi / 2) - np.arctan(
                        h.previous_q2 / np.sqrt(q2_max ** 2 - h.previous_q2 ** 2))
                coords_trim_SecondtHit.append((J_2, theta_wall, h.previous_q1, h.previous_q2))
                break

        stop_iteration += 1

x1_trim = [val[2] for val in coords_trim_firstHit]
y1_trim = [val[3] for val in coords_trim_firstHit]

x2_trim = [val[2] for val in coords_trim_SecondtHit]
y2_trim = [val[3] for val in coords_trim_SecondtHit]

fig = plt.figure(figsize=(16, 5))  # create a figure
ax1 = fig.add_subplot(1, 2, 1)  # create a subplot of certain size
ax1.scatter(x1_trim, y1_trim, c='r')
ax1.legend(['hits locations'])
ax1.set_xlabel('x1')
ax1.set_ylabel('y1')

ax2 = fig.add_subplot(1, 2, 2)  # create a subplot of certain size
ax2.scatter(x2_trim, y2_trim, c='r')
ax2.legend(['hits locations'])
ax2.set_xlabel('x2')
ax2.set_ylabel('y2')

plt.show()

J_vertical1 = [val[0] for val in coords_trim_firstHit if val[2] == step.x_right]
theta_vertical1 = [val[1] for val in coords_trim_firstHit if val[2] == step.x_right]

J_horizontal1 = [val[0] for val in coords_trim_firstHit if val[3] == step.y_up]
theta_horizontal1 = [val[1] for val in coords_trim_firstHit if val[3] == step.y_up]

J_slope1 = [val[0] for val in coords_trim_firstHit if ((val[3] != step.y_up) and (val[2] != step.x_right))]
theta_slope1 = [val[1] for val in coords_trim_firstHit if ((val[3] != step.y_up) and (val[2] != step.x_right))]

J_vertical2 = [val[0] for val in coords_trim_SecondtHit if val[2] == step.x_right]
theta_vertical2 = [val[1] for val in coords_trim_SecondtHit if val[2] == step.x_right]

J_horizontal2 = [val[0] for val in coords_trim_SecondtHit if val[3] == step.y_up]
theta_horizontal2 = [val[1] for val in coords_trim_SecondtHit if val[3] == step.y_up]

J_slope2 = [val[0] for val in coords_trim_SecondtHit if ((val[3] != step.y_up) and (val[2] != step.x_right))]
theta_slope2 = [val[1] for val in coords_trim_SecondtHit if ((val[3] != step.y_up) and (val[2] != step.x_right))]

fig = plt.figure(figsize=(16, 5))
ax1 = fig.add_subplot(1, 2, 1)  # create a subplot of certain size
ax1.scatter(theta_vertical1, J_vertical1, c='r')
ax1.scatter(theta_horizontal1, J_horizontal1, c='b')
ax1.scatter(theta_slope1, J_slope1, c='g')
ax1.legend(['vertical side', 'horizontal side', 'slope side'])
ax1.set_xlabel('theta1')
ax1.set_ylabel('J1')


ax2 = fig.add_subplot(1, 2, 2)  # create a subplot of certain size
ax2.scatter(theta_vertical2, J_vertical2, c='r')
ax2.scatter(theta_horizontal2, J_horizontal2, c='b')
ax2.scatter(theta_slope2, J_slope2, c='g')
ax2.legend(['vertical side', 'horizontal side', 'slope side'])
ax2.set_xlabel('theta2')
ax2.set_ylabel('J2')

plt.show()
print("new_map")



#
# w1 = 1
# w2 = 1
#
# E_t = 1
# y_wall = -3
# x_wall = -3
# x_t = -1
# y_t = -1
# m = (y_t - y_wall) / (x_wall - x_t)
#
# # calc the slope coordinates
# x_slope = np.linspace(start=x_t, stop=x_wall, num=1000)
# y_slope = y_wall + m * (x_slope - x_t)
# corrds_slope = [(x_slope[i], y_slope[i]) for i in range(len(x_slope))]
#
# # upper wall coords_firstHit
# x_upper_wall = np.linspace(start=-1, stop=x_t, num=1000)
# upper_wall_coords = [(x_upper_wall[i], y_wall) for i in range(len(x_upper_wall))]
#
# # vertical wall coords_firstHit
# y_vertical_wall = np.linspace(start=-1, stop=y_t, num=1000)
# vertical_wall_coords = [(x_wall, y_vertical_wall[i]) for i in range(len(y_vertical_wall))]
#
#
# # for loop for all the point
#
#
# def get_correct_energies_and_angles(coordinates, total_energy):
#     theta = list()
#     q_2_i_list = list()
#     e_2 = list()
#     for corr in coordinates:
#         E_1_min = 0.5 * (w1 ** 2) * (corr[0] ** 2)
#         E_2_min = 0.5 * (w2 ** 2) * (corr[1] ** 2)
#         if (total_energy - E_2_min) < E_1_min:
#             continue
#         E_1_range = np.linspace(start=E_1_min, stop=total_energy - E_2_min, num=100)
#         for e in E_1_range:
#             q_1_i = np.sqrt(2 * e) / w1
#             q_2_i = np.abs(corr[1] / (np.cos((w2 / w1) * (np.arccos(corr[0] / q_1_i)))))
#             e_t = (0.5 * (w1 ** 2) * (q_1_i ** 2)) + (0.5 * (w1 ** 2) * (q_2_i ** 2))
#             theta_wall = (np.pi / 2) - np.arctan(corr[1] / q_2_i)
#
#             if np.abs(total_energy - e_t) < 0.01:
#                 print(f'corr is {corr} and e2 is {e_t - e}')
#                 q_2_i_list.append(q_2_i)
#                 theta.append(theta_wall)
#                 e_2_tmp = (total_energy - e) / w2
#                 e_2.append(e_2_tmp)
#
#     return theta, e_2, q_2_i_list
#
#     # else:
#     #     print("not even one")
#
#
# # check for ine point:
#
# theta_slope, e_2_slope, q_2_i_list_slope = get_correct_energies_and_angles(corrds_slope, E_t)
# theta_upper_wall, e_2_upper_wall, q_2_i_list_upper_wall = get_correct_energies_and_angles(upper_wall_coords, E_t)
# theta_vertical_wall, e_2_vertical_wall, q_2_i_list_vertical_wall = get_correct_energies_and_angles(vertical_wall_coords,
#                                                                                                    E_t)
#
# fig = plt.figure(figsize=(8, 5))  # create a figure
# ax1 = fig.add_subplot(1, 1, 1)  # create a subplot of certain size
# ax1.scatter(q_2_i_list_slope, e_2_slope, c='r')
# ax1.scatter(q_2_i_list_upper_wall, e_2_upper_wall, c='b')
# ax1.scatter(q_2_i_list_vertical_wall, e_2_vertical_wall, c='g')
# ax1.set_title("Frame of second 33")
# # ax1.set_xlim(0, np.pi)
# ax1.set_ylim(0, E_t / w2)
# plt.show()
#
# print("check")
#
# # ###############################################
# # ####    for fix q1 ############################
#
#
# q1_m = 5
#
#
# def get_for_fix_q1(coordinates, q1_fix):
#     theta = list()
#     q_2_i_list = list()
#     e_2 = list()
#
#     for corr in coordinates:
#         q_2_i = (corr[1] / (np.cos((w2 / w1) * (np.arccos(corr[0] / q1_fix)))))
#         J_2 = 0.5 * (w2) * (q_2_i ** 2)
#         if J_2 >10:
#             continue
#
#         theta_wall = (np.pi / 2) - np.arctan(corr[1] /np.sqrt(q_2_i**2 - corr[1]**2))
#         q_2_i_list.append(q_2_i)
#         theta.append(theta_wall)
#         e_2.append(J_2)
#
#     return theta, e_2, q_2_i_list
#
#
# theta_slope, e_2_slope, q_2_i_list_slope = get_for_fix_q1(corrds_slope, q1_m)
# theta_upper_wall, e_2_upper_wall, q_2_i_list_upper_wall = get_for_fix_q1(upper_wall_coords, q1_m)
# theta_vertical_wall, e_2_vertical_wall, q_2_i_list_vertical_wall = get_for_fix_q1(vertical_wall_coords,
#                                                                                   q1_m)
#
# fig = plt.figure(figsize=(8, 5))  # create a figure
# ax1 = fig.add_subplot(1, 1, 1)  # create a subplot of certain size
# ax1.scatter(theta_slope, e_2_slope, c='r')
# ax1.scatter(theta_upper_wall, e_2_upper_wall, c='b')
# ax1.scatter(theta_vertical_wall, e_2_vertical_wall, c='g')
# ax1.set_title("Frame of second 33")
# ax1.set_xlim(0, np.pi)
# # ax1.set_ylim(0, E_t / w2)
# plt.show()
