import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
import os

# Specify the file path
file_path = r'.\Test 1\No variance\Test1_latency_0.05_variance_0_trial_1.csv'

# Verify if file exists
if not os.path.exists(file_path):
    raise FileNotFoundError(f"Could not find the CSV file at: {file_path}")

# Read the CSV file
print(f"Reading data from: {file_path}")
df = pd.read_csv(file_path)

# Create figure and axis objects with a black background
plt.rcParams['figure.facecolor'] = 'black'
plt.rcParams['axes.facecolor'] = 'black'
plt.rcParams['axes.edgecolor'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['text.color'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'

fig, ax = plt.subplots(figsize=(12, 6))

# Initialize lists to store the plotted data
time_data = []
forceA_data = []
forceB_data = []

def animate(frame):
    # Clear the current plot
    ax.clear()
    
    # Add data points up to the current frame
    time_data.append(df['Time'][frame])
    forceA_data.append(df['ForceA'][frame])
    forceB_data.append(df['ForceB'][frame])
    
    # Plot the data
    ax.plot(time_data, forceA_data, label='Force A', color='#00ff00', linewidth=2)
    ax.plot(time_data, forceB_data, label='Force B', color='#ff4444', linewidth=2)
    
    # Set labels and title
    ax.set_xlabel('Time (s)', fontsize=10)
    ax.set_ylabel('Force', fontsize=10)
    ax.set_title('Real-time Force Measurements', fontsize=12, pad=10)
    
    # Add legend with white text
    ax.legend(loc='upper right', framealpha=0.8)
    
    # Set grid
    ax.grid(True, linestyle='--', alpha=0.3, color='gray')
    
    # Set y-axis limits based on the data range
    ax.set_ylim(min(df['ForceA'].min(), df['ForceB'].min()) - 10,
                max(df['ForceA'].max(), df['ForceB'].max()) + 10)
    
    # Set x-axis limits to show a moving window
    if frame > 50:  # Show last 50 points
        ax.set_xlim(time_data[-50], time_data[-1])
    
    # Add timestamp
    ax.text(0.02, 0.98, f'Time: {time_data[-1]:.2f}s', 
            transform=ax.transAxes, color='white', 
            bbox=dict(facecolor='black', alpha=0.5))

try:
    print("Creating animation...")
    # Create the animation
    ani = animation.FuncAnimation(fig, animate, frames=len(df),
                                interval=50, repeat=False)

    print("Saving animation to GIF...")
    # Initialize the writer for saving the animation
    writer = PillowWriter(fps=20)

    # Get the base name of the input file without extension
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    # Create output path with same name as input but with .gif extension
    output_path = os.path.join(os.path.dirname(file_path), f"{base_name}.gif")
    
    ani.save(output_path, writer=writer)
    print(f"Animation saved to: {output_path}")

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    # Close the figure to free up memory
    plt.close()
    print("Script finished executing")