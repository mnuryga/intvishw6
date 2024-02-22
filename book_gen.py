import numpy as np

def main():
	day = 0
	for i in range(100):
		print(f'\"Book {i}\",{day},{np.random.randint(low=10_000, high=350_000)},{int(np.clip(np.random.normal(loc=20_000, scale=10_000),5_000, 50_000))}')
		day += np.random.randint(low=0, high=6)

if __name__ == '__main__':
	main()