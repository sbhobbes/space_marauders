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
        return Matrix(np.sqrt(self.data @ self.data.transpose()))
        # return Matrix(np.linalg.norm(self.data, axis=0).reshape(-1, 1))


    def get_column_vector(self, column):
        try:
            if isinstance(column, int):
                column_vector = self.data[:, column]

            elif isinstance(column, str):
                column_vector = self.data[:, self.column_mapping[column.lower()]]

            else:
                column_vector = KeyError(f'Expected int representing column index or one of ({self.column_mapping.keys()}), but got {column} instead.')

        except KeyError as e:
            raise KeyError(f'Expected one of ({self.column_mapping.keys()}), but got {column} instead.') from e

        except IndexError as e:
            raise IndexError(f'Expected int representing a column index in 0 to {(self.shape[1])}, but got index {column} instead.') from e

        return column_vector


    def get_row_vector(self, row):
        try:
            if isinstance(row, int):
                row_vector = self.data[row, :]

            elif isinstance(row, str):
                row_vector = self.data[self.row_mapping[row.lower()], :]

            else:
                row_vector = IndexError(f'Expected int representing a row index or onw of ({self.row_mapping.keys()}), but got {row} instead.')

        except KeyError as e:
            raise KeyError(f'Expected one of ({self.row_mapping.keys()}), but got {row} instead.') from e

        except IndexError as e:
            raise IndexError(f'Expected int representing a row index in 0 to {(self.shape[0])}, but got index {row} instead.') from e

        return row_vector


    def row_stack(self, other):
        if not isinstance(other, Matrix):
            raise TypeError(f'Can only row_stack another Matrix object. Got objects of type {type(self)} and {type(other)}')

        if self._data.shape[1] != other.shape[1]:  # Check column compatibility
            raise ValueError(f'Matrices must have the same number of columns for row_stack. Got shapes {self.shape} and {other.shape}')

        stacked_data = np.vstack((self.data, other.data))

        # Handle row names:
        new_row_names = list(self.row_mapping.keys()) + list(other.row_mapping.keys())
        # Ensure unique row names if needed (add logic here if duplicates are a problem)

        # Use combined row names or generate defaults if necessary
        stacked_matrix = Matrix(stacked_data, row_names=new_row_names, column_names=self.column_mapping.keys())

        return stacked_matrix


    def add_row_vector(self, row_vector, **kwargs):
        row_name = kwargs.get('row_name', f'row_{self.data.shape[0]}')
        row_vector = np.array(row_vector).reshape(1, -1)
        new_matrix = self.row_stack(Matrix(row_vector, row_names=[row_name]))
        self._data = new_matrix.data
        self.row_mapping = new_matrix.row_mapping
        self.column_mapping = new_matrix.column_mapping


    def reshape(self, new_shape):
        """Reshapes the matrix.

        Args:
            new_shape (tuple): The desired shape of the reshaped matrix.

        Raises:
            ValueError: If the new shape is incompatible with the 
                        original matrix's data (different number of elements)

        Returns:
            Matrix: A new Matrix object with the reshaped data.
                      Row and column names are reset.
        """
        try:
          reshaped_data = self._data.reshape(new_shape)
        except ValueError as e:
          raise ValueError(f"Cannot reshape matrix from {self.shape} to {new_shape}. The number of elements must remain the same.") from e


        # Reset row and column mappings for reshaped matrix
        new_rows = reshaped_data.shape[0]
        new_cols = reshaped_data.shape[1]

        new_row_names = [f"row_{i}" for i in range(new_rows)]
        new_col_names = [f"column_{j}" for j in range(new_cols)]

        reshaped_matrix = Matrix(reshaped_data, row_names=new_row_names, column_names=new_col_names)

        return reshaped_matrix


    def __sub__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError(f'Can only subtract another Matrix object. Got objects of type {type(self)} and {type(other)}')

        if self._data.shape != other.shape:
            raise ValueError(f'Matrix dimensions must match for subtraction. Got matrices of shape {self.shape} and {other.shape}.')

        result_data = self.data - other.data

        difference_matrix = Matrix(result_data, row_names=self.row_mapping.keys(), column_names=self.column_mapping.keys())

        return difference_matrix


    def __getitem__(self, index):
        return self.data[index]


    def __str__(self):
        return str(self.data)
    # def __str__(self):  # Improved string representation
    #     row_names = list(self.row_mapping.keys())
    #     col_names = list(self.column_mapping.keys())

    #     header = "  ".join(col_names)  # Create column name header
    #     lines = [header]

    #     for i, row in enumerate(self._data):
    #         row_str = f"{row_names[i]:<8} " + "  ".join(map(str, row)) # Left-align row names

    #         lines.append(row_str)

    #     return "\n".join(lines)


    def __repr__(self):
        return str(self.data)


    @property
    def shape(self):
        return self.data.shape


    @property
    def data(self):
        return self._data


    @property
    def empty(self):
        return self.data.size == 0


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


    def get_index_of_smallest_distance(self):
        return np.argmin(self._data)
