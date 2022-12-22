import numpy as np
import matplotlib.pyplot as plt

w1 = 1
w2 = 2.5

E_t = 2
y_wall = -0.5
x_wall = -0.5
x_t = -0.8
y_t = -0.6
m = (y_t - y_wall)/(x_wall - x_t)

# calc the slope coordinates
x_slope = np.linspace(start=x_t, stop=x_wall, num=100)
y_slope = y_wall + m*(x_slope-x_t)

corrds_slope = [(x_slope[i],y_slope[i]) for i in range(len(x_slope))]


# for loop for all the point


theta_2_wall = list()
q_2_i_list = list()
e_2 = list()

for corr in corrds_slope:
    E_1_min = 0.5 * (w1 ** 2) * (corr[0] ** 2)
    E_2_min = 0.5 * (w2 ** 2) * (corr[1] ** 2)
    E_1_range = np.linspace(start=E_1_min, stop=E_t - E_2_min, num=100)
    for e in E_1_range:
        q_1_i = np.sqrt(2*e)/w1
        q_2_i = corr[1]/(np.cos((w2/w1)*(np.arccos(corr[0]/q_1_i))))
        e_t = 0.5*(w1**2)*(q_1_i**2)+0.5*(w1**2)*(q_2_i**2)
        theta_wall = np.pi/2-np.arctan(corr[1]/q_2_i)

        if np.abs(E_t-e_t) < 0.1:
            print("interesting")
        if np.abs(E_t-e_t) < 0.1:
            print(f'corr is {corr} and e2 is {e_t-e}')
            q_2_i_list.append(q_2_i)
            theta_2_wall.append(theta_wall)
            e_2_tmp = (e_t-e)/w2
            e_2.append(e_2_tmp)
        # else:
        #     print("not even one")
#check for ine point:

fig = plt.figure(figsize=(8, 5)) # create a figure
ax1 = fig.add_subplot(1, 1 ,1) # create a subplot of certain size
ax1.scatter(theta_2_wall, e_2, )
ax1.set_title("Frame of second 33")

plt.show()

print("check")

