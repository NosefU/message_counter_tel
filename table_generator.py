import os

import matplotlib.pyplot as plt


class Table:
    data_colors = [(0, 1, 0.26), (0, 0.73, 1), (1, 0.73, 0)]

    def __init__(self, headers: list, data: list, col_align: list):

        # header colors
        header_colors = ['#ffffff'] * len(headers)

        # rows colors: init
        self._max_values = []
        self._min_values = []
        for column_number in range(2, len(headers)):
            column = [float(row[column_number]) for row in data[:-1]]
            self._max_values.append(max(column))
            self._min_values.append(min(column))

        # rows colors
        self.data_colors = self.data_colors * (len(headers) // len(self.data_colors))
        row_colors = []
        for row_number in range(len(data) - 1):
            row_color = []
            # чередующиеся серые и светло-серые полосы для номера и имени
            color = 0.8 if (row_number + 1) % 2 else 0.95
            color = [(color,) * 3] * 2
            row_color.extend(color)
            # generating heatmaps for data columns from data_color (max value) to white (min value)
            for column_number in range(2, len(headers)):
                current_value = float(data[row_number][column_number])
                cell_color = self._get_cell_color(current_value, column_number)
                row_color.append(cell_color)
            row_colors.append(row_color)

        # total row color
        color = [(0.6,) * 3] * len(headers)
        row_colors.append(color)

        # config plot
        self._init_plot(len(data))

        # add a table
        table = plt.table(cellText=data,
                          cellColours=row_colors,
                          colLabels=headers,
                          colColours=header_colors,
                          colWidths=[0.1, 0.5, 0.15, 0.15, 0.15],
                          cellLoc='left',
                          bbox=[-0.12, -0.115, 1.2, 1.24],
                          loc='center'
                          )

        # config table
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 1.5)

        # prepare column text alignment
        col_align = col_align if col_align else []
        col_align.append(['left'] * len(headers))

        # paint and align cells
        cells = table.get_celld()
        for pos, cell in cells.items():
            cell._edgecolor = (0.8, 0.8, 0.8, 1)  # styling borders color
            if pos[0] == 0:  # styling header
                cell.set_text_props(
                    horizontalalignment='center',
                    fontweight='bold'
                )
            else:  # styling rows
                cell.set_text_props(horizontalalignment=col_align[pos[1]])

            if pos[0] == len(data):  # styling total row
                cell.set_text_props(fontweight='bold')

    @staticmethod
    def _get_shaded_color(max_color: tuple, percent):
        return tuple(color + (1 - color) * (1 - percent) for color in max_color)

    def _get_cell_color(self, current_value, column_number):
        """
        Высчитывает цвет ячейки, исходя из переданного значения:
        от белого (минимальное значение) до соответствующего из data_color (максимальное значение)
        """
        column_color = self.data_colors[column_number - 2]
        min_value = self._min_values[column_number - 2]
        max_value = self._max_values[column_number - 2]
        percent = (current_value - min_value) / (max_value - min_value)
        cell_color = self._get_shaded_color(column_color, percent)
        return cell_color

    @staticmethod
    def _init_plot(rows_count: int):
        # config plot
        fig, ax1 = plt.subplots(figsize=(7, rows_count / 3.5))

        # set up picture: hide axes and diagram box
        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        plt.box(on=None)


    def show(self):
        plt.show()

    def save(self, path: str) -> str:
        """ Сохраняет таблицу в картинку, возвращает полный поуть до картинки """
        plt.savefig(path,
                    bbox_inches='tight',
                    dpi=150
                    )
        return os.path.abspath(path)

