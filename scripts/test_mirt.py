from mirt import MIRT
import json

mirt = MIRT()
data = json.load(open('data/fraction.json'))['student_data']
mirt.training_step(data)
mirt.init_test(set([16, 17, 18, 19, 20]))
mirt.next_item([], [])
