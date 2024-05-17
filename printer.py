import matplotlib.pyplot as plt

def plot_rewards(file_path):
    # Leer las recompensas desde el archivo
    with open(file_path, "r") as f:
        rewards = [float(line.strip()) for line in f.readlines()]

    # Graficar las recompensas
    plt.figure(figsize=(10, 5))
    plt.plot(rewards, label='Recompensa por episodio')
    plt.xlabel('Episodios')
    plt.ylabel('Recompensa Total')
    plt.title('Evolución de la Recompensa por Episodio')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    plot_rewards("rewards.txt")
