from qmatrix import QMatrix

Q = [
    [1, 0],
    [0, 1],
    [1, 1]
]

model = QMatrix(nb_competences=2, Q=Q, slip=[0] * 3, guess=[0] * 3)
model.generate_student_data(100, [0.6, 0.8])
