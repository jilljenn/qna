from mirt import MIRT
from genma import GenMA
from qmatrix import QMatrix
from conf import dataset_name, nb_competences_values, STUDENT_FOLD, QUESTION_FOLD
from my_io import IO, Dataset, say

q = QMatrix()
# q.load('qmatrix-custom')
q.load('qmatrix-%s' % dataset_name)
mirt = MIRT(q=q)

genma = GenMA(dim=8)

files = IO()
dataset = Dataset(dataset_name, files)
dataset.load_subset()

mirt.compute_all_errors(dataset)
genma.compute_all_errors(dataset)
