import numpy as np
import sys

print(sys.version)

def hello_world():

	num = np.random.randint(low=1, high=100, size=1)[0]
	print(f'This is the {num}th hello world')

def main():
	hello_world()

if __name__ == '__main__':
	main()
