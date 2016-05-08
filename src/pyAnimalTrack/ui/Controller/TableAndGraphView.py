from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class TableAndGraphView:

    def __init__(self, table_view, selection_dropdown, graph_frame, graph_key_frame, draw_graph):
        self.table_view = table_view
        self.selection_dropdown = selection_dropdown
        self.draw_graph = draw_graph

        # Programatically create the graph widget, as it is not available in the designer
        # Also create a separate graph to display the legend without resizing issues
        self.figure = plt.figure(facecolor='none')
        self.legendFigure = plt.figure(facecolor='none')
        self.canvas = FigureCanvas(self.figure)
        self.legendCanvas = FigureCanvas(self.legendFigure)
        graph_frame.addWidget(self.canvas)
        graph_key_frame.addWidget(self.legendCanvas)
        # The plot, used on the graph
        self.plot = self.figure.add_subplot(111)
        self.plot.hold(False)
        self.legendPlot = self.legendFigure.add_axes([-0.2,0,-0.045,0.85])
        self.legendPlot.hold(False)

    def after_init(self):
        self.table_view.selectionModel().selectionChanged.connect(self.change_selected_combo_column)
        self.selection_dropdown.currentIndexChanged.connect(self.draw_graph)

        # TODO: Do we want this to happen? Unsure
    def change_selected_combo_column(self, selected, deselected):
        """ When the selected data cell changes, update the combobox that controls the parameters.

            :param selected: PyQt5. The cells that were selected.
            :param deselected: PyQt5. The cells that were deselected.
            :returns: void
        """
        self.selection_dropdown.setCurrentIndex(selected.indexes()[0].column())