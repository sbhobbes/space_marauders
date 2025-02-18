import numpy as np


class Matrix:
    def __init__(self, data: list, row_names: list = None, column_names: list = None):
        self._data = np.array(data)
        row_names = row_names if row_names is not None else [f'row_{i}' for i in range(self._data.shape[0])]
        column_names = column_names if column_names is not None else [f'column_{i}' for i in range(self._data.shape[1])]
        self.column_mapping = {name: index for index, name in enumerate(column_names)}
        self.row_mapping = {name: index for index, name in enumerate(row_names)}


    def transpose(self):
        return Matrix(
            self._data.transpose(),
            row_names=self.column_mapping.keys(),
            column_names=self.row_mapping.keys()
        )


    def calculate_distance(self):
        return Matrix(np.sqrt(self._data @ self._data.transpose()))


    def get_column_vector(self, column):
        try:
            if isinstance(column, int):
                column_vector = self._data[:, column]

            elif isinstance(column, str):
                column_vector = self._data[:, self.column_mapping[column.lower()]]

            else:
                column_vector = KeyError(f'Expected int representing column index or one of ({self.column_mapping.keys()}), but got {column} instead.')

        except KeyError as e:
            raise KeyError(f'Expected one of ({self.column_mapping.keys()}), but got {column} instead.') from e

        except IndexError as e:
            raise IndexError(f'Expected int representing a column index in 0 to {(self._data.shape[1])}, but got index {column} instead.') from e

        return column_vector


    def get_row_vector(self, row):
        try:
            if isinstance(row, int):
                row_vector = self._data[row, :]

            elif isinstance(row, str):
                row_vector = self._data[self.row_mapping[row.lower()], :]

            else:
                row_vector = IndexError(f'Expected int representing a row index or onw of ({self.row_mapping.keys()}), but got {row} instead.')

        except KeyError as e:
            raise KeyError(f'Expected one of ({self.row_mapping.keys()}), but got {row} instead.') from e

        except IndexError as e:
            raise IndexError(f'Expected int representing a row index in 0 to {(self._data.shape[0])}, but got index {row} instead.') from e

        return row_vector


    def __sub__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError(f'Can only subtract another Matrix object. Got objects of type {type(self)} and {type(other)}')

        if self._data.shape != other._data.shape:
            raise ValueError(f'Matrix dimensions must match for subtraction. Got matrices of shape {self._data.shape} and {other._data.shape}.')

        result_data = self._data - other._data

        difference_matrix = Matrix(result_data, row_names=self.row_mapping.keys(), column_names=self.column_mapping.keys())

        return difference_matrix


    def __getitem__(self, index):
        return self._data[index]


    def __str__(self):
        return str(self._data)


    def __repr__(self):
        return str(self._data)


    @property
    def shape(self):
        return self._data.shape


class PositionMatrix(Matrix):
    def __init__(self, data, row_names=None):
        row_names = row_names if row_names is not None else [f'row_{i}' for i in range(len(data))]
        super().__init__(data, row_names=row_names, column_names=['x_position', 'y_position'])


    def get_x(self):
        return self.get_column_vector(0)


    def get_y(self):
        return self.get_column_vector(1)


class VelocityMatrix(Matrix):
    def __init__(self, data, row_names=None):
        row_names = row_names if row_names is not None else [f'row_{i}' for i in range(len(data))]
        super().__init__(data, row_names=row_names, column_names=['direction', 'speed'])


    def get_direction(self):
        return self.get_column_vector(0)


    def get_speed(self):
        return self.get_column_vector(1)


class DifferenceMatrix(Matrix):
    def __init__(self, matrix_a, matrix_b):
        difference = matrix_a - matrix_b
        super().__init__(difference._data)


class DistanceMatrix(Matrix):
    def __init__(self, matrix):
        distance = matrix.calculate_distance()
        super().__init__(distance._data)


    def get_distances(self):
        return np.diagonal(self._data).reshape(-1, 1)
