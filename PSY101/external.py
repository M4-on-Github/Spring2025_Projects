import matplotlib.pyplot as plt

# Data
visits = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 18]
undergraduate_sample = [4.12, 3.88, 4.49, 4.17, 3.75, 3.68, 5.66, 2.73, 4.65, 3.23, None, None]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(visits, undergraduate_sample, marker='o', label='Undergraduate Sample')

# Adding titles and labels
plt.title('Posttest Stress Response Averaged by Visits')
plt.xlabel('Number of Visits')
plt.ylabel('Stress Response')
plt.legend()
plt.grid(True)

# Show plot
plt.show()
