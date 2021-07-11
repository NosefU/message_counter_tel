import os

import matplotlib.pyplot as plt


class Table:
    def __init__(self, headers: list, data: list, col_align: list):

        col_align = col_align if col_align else []
        col_align.append(['left'] * len(headers))

        # header and rows colors
        header_colors = ['#ffffff'] * len(headers)
        row_colors = []
        for i in range(len(data)):
            color = 0.8 if (i + 1) % 2 else 0.95
            color = [(color,) * 3] * len(headers)
            row_colors.append(color)

        # config plot
        fig, ax1 = plt.subplots(figsize=(7, len(data) / 3.5))

        # set up picture: hide axes and diagram box
        ax = plt.gca()
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        plt.box(on=None)

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

        # paint and align cells
        cells = table.get_celld()
        for pos, cell in cells.items():
            cell._edgecolor = (0.8, 0.8, 0.8, 1)
            if pos[0] == 0:
                cell.set_text_props(
                    horizontalalignment='center',
                    # color='w',
                    fontweight='bold'
                )
            else:
                cell.set_text_props(horizontalalignment=col_align[pos[1]])

    def show(self):
        plt.show()

    def save(self, path: str) -> str:
        """ Сохраняет таблицу в картинку, возвращает полный поуть до картинки """
        plt.savefig(path,
                    bbox_inches='tight',
                    dpi=150
                    )
        return os.path.abspath(path)

