import pandas as pd
import matplotlib.pyplot as plt

# Read the "result.csv" file
df = pd.read_csv(r"C:\Users\Victor\OneDrive\Documents\GitHub\AIImageAnalysis\Laser_Line_Detection\results\04112023 Tong KO 5787 5713\04112023 Tong KO 5787 5713\Dish1 KO 5713 COMPLETED\FOV4 6 cells 50mW\output\output\result.csv")

# Get the column names of the output cells
output_columns = [col for col in df.columns if col.startswith("output_cell")]

# Plot the data for each output cell
for col in output_columns:
    plt.plot(df["timeDelta"], df[col], label=col)

# Set the x-axis and y-axis labels
plt.xlabel("Time Delta")
plt.ylabel("Brightness")

# Add a legend
plt.legend()

# Save the plot as an image
plt.savefig(r"C:\Users\Victor\OneDrive\Documents\GitHub\AIImageAnalysis\Laser_Line_Detection\results\04112023 Tong KO 5787 5713\04112023 Tong KO 5787 5713\Dish1 KO 5713 COMPLETED\FOV4 6 cells 50mW\output\output\graph.png")

# Show the plot
plt.show()