import rpy2.robjects as robjects
from calc import get_train_checksum
import numpy as np

r = robjects.r


class RPyInterface:
    def __init__(self):
        pass

    def get_prefix(self):
        return ''

    def compute_all_errors(self, p, row_mask, col_mask):
        se = (p - self.data) ** 2
        print('min se', se[row_mask, col_mask].min())
        print('max se', se[row_mask, col_mask].max())
        print('max se', se[row_mask, col_mask].mean())
        rmse = se[row_mask, col_mask].mean() ** 0.5
        print('Train RMSE:', rmse)
        ll = np.log(1 - abs(p - self.data))
        mnll = -ll[row_mask, col_mask].mean()
        print('Train mean NLL:', mnll)
        acc = np.round(p) == self.data
        print('Train mean accuracy:', acc[row_mask, col_mask].mean())

    def prepare_data(self, data, row_mask, col_mask):
        self.data = data
        self.nb_students, self.nb_questions = data.shape
        train_data_by_row = data.reshape(-1)
        row = np.copy(train_data_by_row)
        r_train_data = r.matrix(robjects.IntVector(train_data_by_row), nrow=self.nb_students, byrow=True)
        for i, j in zip(row_mask, col_mask):
            row[i * self.nb_questions + j] = 2  # To compute checksum
            r_train_data.rx[i + 1, j + 1] = robjects.NA_Integer
        self.checksum = get_train_checksum(self.get_prefix(), row)
        r_train_data.colnames = robjects.StrVector(['Q%d' % i for i in range(1, self.nb_questions + 1)])
        return r_train_data


if __name__ == '__main__':
    rpyi = RPyInterface()
    data = np.round(np.random.random((4, 5)))
    print(data)
    row_mask = [1, 2]
    col_mask = [3, 3]
    r_train_data = rpyi.prepare_data(data, row_mask, col_mask)
    p = 0.9 * np.ones((4, 5))
    rpyi.compute_all_errors(p, row_mask, col_mask)
