from qmatrix import QMatrix

q = QMatrix()
q.load('qmatrix-fake')
q.init_test(set())
print(q.p_test)
q.next_item([], [])
q.estimate_parameters([0], [0])
print(q.next_item([0], []))
q.estimate_parameters([0, 3], [0, 1])
print(q.next_item([0], []))
q.estimate_parameters([0, 3, 1], [0, 1, 1])
print(q.next_item([0], []))
print(q.p_test)

q.generate_student_data(20, [0.7] * 3)
