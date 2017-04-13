from conf import dataset_name
from my_io import Dataset


dataset = Dataset(dataset_name)
dataset.get_subset()
dataset.save_subset()
