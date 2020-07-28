import tkinter as tk
from typing import Union, List, Dict


# from commands import FileMenuCommands as menu_c

# MainWindow = tk.Tk()
# MainWindow.title("Tracker")
# MainWindow.geometry("1000x600+1700+150")
# MainWindow["padx"] = 10
# MainWindow["pady"] = 5


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tracker")
        self.geometry("1000x600+500+150")
        self["padx"] = 10
        self["pady"] = 5


class MenuFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        kwargs["borderwidth"] = 2
        super().__init__(parent, **kwargs)


class MenuBar(tk.Menu):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

    def add_cascade_(self, menu):
        self.add_cascade(label="File", menu=menu)


class FileMenu(tk.Menu):
    def __init__(self, parent, **kwargs):
        kwargs["tearoff"] = 0
        super().__init__(parent, **kwargs)

        self.add_command(label='Track', command=self.track_command)
        self.add_command(label='Open', command=self.open_command)

    def track_command(self):
        pass

    def open_command(self):
        pass


class TrackingFrame(tk.Frame):
    frame_names = ["frame_1", "frame_2", "frame_3"]

    def __init__(self, parent, **kwargs):
        kwargs["borderwidth"] = 2
        kwargs["bg"] = "blue"
        super().__init__(parent, **kwargs)
        self.frames = {}
        self.max_frames = len(__class__.frame_names)
        self.frame_row_start = None
        self.frame_column_start = None

    def create_inner_frames(self, starting_row: int, starting_column: int, **kwargs):
        self.frame_row_start = starting_row
        self.frame_column_start = starting_column
        self.add_frames(starting_row, starting_column, **kwargs)

    def add_frames(self, starting_row, starting_column, **kwargs):
        frames = __class__.frame_names
        self.frames = {name: tk.Frame(self, **kwargs) for name in frames}
        self.grid_frames(starting_row, starting_column)

    def grid_frames(self, starting_row, starting_column):
        count = 0
        for frames in self.frames.values():
            frames.grid(row=starting_row + count, column=starting_column,
                        rowspan=5, columnspan=2)
            count += 6


class TrkEntryGroup:
    def __init__(self, parents: list):
        self.parents: List[tk.Frame] = parents      # List of frame objects
        self.width = 15     # No of characters
        self.border_width = 2
        self.labels = ["Tracking No", "Carrier", "Item Description", "Alias"]
        self.entry_objects: List[Dict[str, tk.Entry]] = []
        self.default_grid = [(3, 1)]

    # Generate Entries
    def generate(self):
        # Create entry widgets for each frame
        # Populate entry_objects list
        for frame in self.parents:
            dict_ = {}
            count = 0
            for _ in self.labels:
                dict_[self.labels[count]] = tk.Entry(master=frame, width=self.width,
                                                     borderwidth=self.border_width)
                count += 1
            self.entry_objects.append(dict_)
        return self.label_entries()

    # Label Entries in form of placeholders
    def label_entries(self):
        # Inserts label placeholders in the entry boxes
        for frames in self.entry_objects:
            count_2 = 0
            for entry in frames.values():
                entry.insert(7, self.labels[count_2])
                count_2 += 1

        return self.auto_grid()

    # Arrange inner frames on TrackingFrame
    def auto_grid(self):
        starting_row = 3
        starting_column = 2
        inner_count = 0
        outer_count = 0

        for frames in self.entry_objects:
            for entry in frames.values():
                entry.grid(row=starting_row + inner_count,
                           column=starting_column)
                inner_count += 1
            outer_count += inner_count + 2
            inner_count = outer_count







mainWindow = MainWindow()

menuFrame = MenuFrame(mainWindow)
menuFrame.grid(row=0, column=1, rowspan=1, columnspan=7, sticky="ns")

menu_bar = MenuBar(menuFrame)
fileMenu = FileMenu(menu_bar)
menu_bar.add_cascade_(fileMenu)

trackingFrame = TrackingFrame(mainWindow)
trackingFrame.grid(row=2, column=1, rowspan=19, columnspan=2, sticky="ns")
trackingFrame.create_inner_frames(3, 2)

trk_info_entries = TrkEntryGroup([frames for frames in trackingFrame.frames.values()])
trk_info_entries.generate()

mainWindow.config(menu=menu_bar)
mainWindow.mainloop()



#
#
#
# # Menu Frame
# menuFrame = tk.Frame(MainWindow, borderwidth=2)

#
# # Menu Bar
# menu_bar = tk.Menu(menuFrame)
# file_menu = tk.Menu(menu_bar, tearoff=0)
# file_menu.add_command(label='Track', command=menu_c().file_command)
# file_menu.add_command(label='Open', command=menu_c().file_command)
# menu_bar.add_cascade(label="File", menu=file_menu)
#
#
# # Tracking Frame
# trackingFrame = tk.Frame(MainWindow, borderwidth=2, bg="blue")
# trackingFrame.grid(row=3, column=1, rowspan=18, columnspan=2, sticky="ns")
#
#
# class ShpInfoGroup:
#     def __init__(self, master):
#         self.parent = trackingFrame
#         self.width = 15
#         self.border_width = 2
#         self.labels = ["Tracking No", "Carrier", "Item Description", "Alias"]
#         self.entry_objects = {}
#         self.default_grid = [(3, 1)]
#         self.generate()
#
#     def generate(self):
#         count = 0
#         for name in self.labels:
#             self.entry_objects[self.labels[count]] = tk.Entry(master=self.parent,
#                                                               width=self.width,
#                                                               borderwidth=self.border_width)
#             count += 1
#
#         for label, object_ in self.entry_objects.items():
#             object_.insert(7, label)
#
#         return self.auto_grid()
#
#     def auto_grid(self, starting_row: int = None, starting_column: int = None):
#         count = 0
#         if starting_row and starting_column is None:
#             for obj in self.entry_objects.values():
#                 for row, column in self.default_grid:
#                     obj.grid(row=self.default_grid[row + count],
#                              column=self.default_grid[column])
#                     count += 1
#
#
#
#
#
#
#
#
#
# # trk_no_input = tk.Entry(trackingFrame, width=15, borderwidth=2)
# # carrier_input = tk.Entry(trackingFrame, width=15, borderwidth=2)
# # item_desc_input = tk.Entry(trackingFrame, width=15, borderwidth=2)
# # alias_input = tk.Entry(trackingFrame, width=15, borderwidth=2)
# #
# # trk_no_input.grid(row=3, column=4)
# # carrier_input.grid(row=4, column=4)
# # item_desc_input.grid(row=5, column=4)
# # alias_input.grid(row=6, column=4)
# #
# # shp_list = ["Tracking No:", "Carrier", "Item Description", "Alias"]
#
# # Info Frame
# infoFrame = tk.Frame(MainWindow, borderwidth=2, bg="red")
# infoFrame.grid(row=3, column=4, rowspan=18, columnspan=4)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# def run_tracker():
#     MainWindow.mainloop()
#
#
# if __name__ == "__main__":
#     trk_pane = ShpInfoGroup()
#     trk_pane.generate()
#
#     MainWindow.config(menu=menu_bar)
#     run_tracker()
