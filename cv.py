from conf import STUDENT_FOLD, QUESTION_FOLD
from datetime import datetime
from my_io import Dataset, IO
from qmatrix import QMatrix
from chrono import Chrono
from irt import IRT
from mirt import MIRT
from mhrm import MHRM
from zero import Zero
import random
import numpy as np


HIDDEN_RATE = 0.1


def prepare_prng(nb_students, nb_questions):
	nb_hidden = round(HIDDEN_RATE * nb_questions)
	u0 = 0
	a = 4685763
	b = 47831
	n = 47564875
	u = [u0]
	for i in range(nb_hidden * nb_students):
		u.append(((a * u[-1] + b) % n) % nb_questions)
	return u


chrono = Chrono()
files = IO()
for dataset_name in ['berkeley']:
	dataset = Dataset(dataset_name, files)
	q = QMatrix()
	#q.load('qmatrix-%s' % dataset_name)
	models = [Zero(), IRT()]  # [IRT()]#, MIRT(dim=2), MIRT(dim=3), MIRT(q=q)]  # , MHRM(dim=2), 
	dataset.load_subset()
	print(dataset)
	for i_exp in range(STUDENT_FOLD):
		# train_subset = dataset.train_subsets[i_exp]
		# test_subset = dataset.test_subsets[i_exp]
		for j_exp in range(QUESTION_FOLD):
			# validation_index = set(dataset.validation_question_sets[j_exp])
			files.update(i_exp, j_exp)
			for model in models:
				print(model.name)
				begin = datetime.now()
				print(begin)
				data = np.array(dataset.data)
				nb_students, nb_questions = data.shape
				nb_hidden = round(HIDDEN_RATE * nb_questions)
				chrono.save('prepare data')
				u = prepare_prng(nb_students, nb_questions)
				chrono.save('prepare prng')
				row_mask = []
				col_mask = []
				for i in range(nb_students):
					row_mask.extend([i] * nb_hidden)
					col_mask.extend(u[nb_hidden * i:nb_hidden * (i + 1)])
				# test_dataset = [[dataset.data[i][j] for j in dataset.question_subset] for i in test_subset]
				chrono.save('prepare mask')
				model.r_data = model.prepare_data(data, row_mask, col_mask)
				chrono.save('prepare rdata')
				print(model.checksum)
				# model.load()
				model.training_step()
				chrono.save('train')
				p = model.compute_all_predictions()
				model.compute_train_test_error(p)
				print(datetime.now())
			break
		break
