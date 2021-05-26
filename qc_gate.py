import cmath, math
from numpy import matrix

class QuantumGates:
    """
    This class defines all the Quantum Gate operation 
    available.
    """
    # Qubit transformation matrices

    # Identity Matrix
    I = matrix([[1, 0],
                [0, 1]])

    # Hadamard Gate
    H = 1 / math.sqrt(2) * matrix([[1, 1],
                                   [1, -1]])
    # PauliX
    X = matrix([[0, 1],
                [1, 0]])
    # PauliY
    Y = matrix([[0, -1j],
                [1j, 0]])

    # PauliZ
    Z = matrix([[1, 0],
                [0, -1]])
    S = matrix([[1, 0],
                [0, 1j]])  # Phase
    T = matrix([[1, 0],
                [0, cmath.exp(1j * (cmath.pi / 4))]])  # PI/8
    sN = 1 / cmath.sqrt(2) * matrix([[1, -1],
                                     [1, 1]])  # Sqrt Not

    def __init__(self):
        pass
