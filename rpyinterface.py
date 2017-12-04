import rpy2.robjects as robjects
from rpy2.rinterface import NA_Integer
from calc import get_train_checksum
import numpy as np
import pickle

r = robjects.r


class RPyInterface:
    def __init__(self):
        pass

    def get_prefix(self):
        return ''

    def load(self):
        pass

    def save(self):
        with open('backup/' + self.checksum + '.pickle', 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    def prepare_data(self, data, row_mask=[], col_mask=[]):
        self.data = data
        self.test_rows = row_mask
        self.test_cols = col_mask
        self.nb_students, self.nb_questions = data.shape
        train_data = np.copy(data)
        # Remove test entries from train
        train_data[row_mask, col_mask] = -1
        train_data_by_row = train_data.reshape(-1)
        r_train_data = r.matrix(robjects.IntVector(train_data_by_row), nrow=self.nb_students, byrow=True)
        r_train_data.rx[r_train_data.ro == -1] = robjects.NA_Integer
        self.checksum = get_train_checksum(self.get_prefix(), train_data_by_row)
        r_train_data.colnames = robjects.StrVector(['Q%d' % i for i in range(1, self.nb_questions + 1)])
        return r_train_data

    def compute_train_test_error(self, p):
        all_pairs = set([(i, j) for i in range(self.nb_students) for j in range(self.nb_questions)])
        test_pairs = set(zip(self.test_rows, self.test_cols))
        train_pairs = list(all_pairs - test_pairs)
        self.train_rows, self.train_cols = zip(*train_pairs)
        self.compute_errors_on_subset(p, self.train_rows, self.train_cols, name='Train')
        if self.test_rows:
            self.compute_errors_on_subset(p, self.test_rows, self.test_cols)

    def compute_errors_on_subset(self, p, rows, cols, name='Test'):
        se = (p - self.data) ** 2
        rmse = se[rows, cols].mean() ** 0.5
        print('%s RMSE:' % name, rmse)
        ll = np.log(1 - abs(p - self.data))
        mnll = -ll[rows, cols].mean()
        print('%s mean NLL:' % name, mnll)
        acc = np.round(p) == self.data
        print('%s mean accuracy:' % name, acc[rows, cols].mean())


if __name__ == '__main__':
    rpyi = RPyInterface()
    data = np.round(np.random.random((4, 5)))
    print(data)
    rows = [1, 2]
    cols = [3, 3]
    r_train_data = rpyi.prepare_data(data, rows, cols)
    p = 0.9 * np.ones((4, 5))
    rpyi.compute_train_test_error(p)
