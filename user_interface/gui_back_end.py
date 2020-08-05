import tkinter as tk
from typing import Union, List, Dict, NewType, Tuple

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
        self.geometry("1000x600+1500+150")
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

    # Types
    L = Tuple[int, int]     # row, column pairs
    T = Tuple[Tuple[int, int], Tuple[int, int]]     # first and last row/column pairs

    def __init__(self, parent, frame_row_start=3, column_row_start=2, **kwargs):
        kwargs["borderwidth"] = 2
        kwargs["bg"] = "blue"
        super().__init__(parent, **kwargs)
        self.frames: Dict[str, tk.Frame] = {}
        self.max_frames = len(__class__.frame_names)
        self.frame_row_start = frame_row_start
        self.frame_column_start = column_row_start
        self.spatial_rows: List[int] = []
        self.spatial_columns: List[int] = []

    # populates self.frames dict with generated frames
    def create_inner_frames(self, **kwargs):
        frames = __class__.frame_names
        self.frames = {name: tk.Frame(self, **kwargs) for name in frames}

    def grid_inner_frames(self):
        starting_row = self.frame_row_start
        starting_column = self.frame_column_start

        count = 0
        # other_rows = []
        for frames in self.frames.values():
            frames.grid(row=starting_row + count, column=starting_column,
                        rowspan=5, columnspan=2)
            count += 6
            # other_rows.append((count + starting_row) - 1)

    # Rows and Columns for space
    # Populates spatial_rows and spatial_cols
    def spatial_rows_cols(self):
        # Rows
        top_row = self.frame_row_start - 1
        other_rows = []
        index = top_row
        for _ in __class__.frame_names:
            new_val = index + 6
            other_rows.append(new_val)
            index = new_val

        self.spatial_rows.append(top_row)
        print(f"other_rows: {other_rows}")
        for row in other_rows:
            self.spatial_rows.append(row)

        # Columns
        starting_column = self.frame_column_start
        left_col = starting_column - 1
        right_col = starting_column + 2     # 2 = column_span
        self.spatial_columns.append(left_col)
        self.spatial_columns.append(right_col)
        print(f"spatial_rows: {self.spatial_rows}\nspatial_columns: {self.spatial_columns}")

    def return_first_and_last(self) -> T:
        rows = (self.spatial_rows[0], self.spatial_rows[-1])
        columns = (self.spatial_columns[0], self.spatial_columns[-1])

        return rows, columns

    def batch_spatial_row_col_configure(self, minsize: L,
                                        weight: L = None, pad: L = None):
        self.spatial_rows_cols()

        row_kwargs, col_kwargs = {}, {}
        row_kwargs["minsize"], col_kwargs["minsize"] = minsize[0], minsize[1]

        row_kwargs["weight"] = weight[0] if weight else None
        row_kwargs["pad"] = pad[0] if pad else None
        col_kwargs["weight"] = weight[1] if weight else None
        col_kwargs["pad"] = pad[1] if pad else None

        print(f"row_kwargs: {row_kwargs}\ncol_kwargs: {col_kwargs}")

        self.configure_row(row_kwargs, self.spatial_rows)
        self.configure_column(col_kwargs, self.spatial_columns)

    def configure_row(self, kwargs: Dict, rows: List[int]):
        for row in rows:
            self.rowconfigure(row, **kwargs)

    def configure_column(self, kwargs: Dict, cols: List[int]):
        for col in cols:
            self.columnconfigure(col, **kwargs)

    def spatial_row_configure(self, rows: List[int], minsize: int,
                              weight: int = None, pad: int = None):
        row_kwargs = {}
        if not self.spatial_rows:
            self.spatial_rows_cols()
        for row in rows:
            if row in self.spatial_rows:
                row_kwargs["minsize"], row_kwargs["weight"] = minsize, weight
                row_kwargs["pad"] = pad
            else:
                raise ValueError(f"Row must be one of these {self.spatial_rows}")
            self.configure_row(row_kwargs, rows)

    def spatial_column_configure(self, cols: List[int], minsize: int,
                                 weight: int = None, pad: int = None):
        col_kwargs = {}
        if not self.spatial_columns:
            self.spatial_rows_cols()

        for col in cols:
            if col in self.spatial_columns:
                col_kwargs["minsize"], col_kwargs["weight"] = minsize, weight
                col_kwargs["pad"] = pad
            else:
                raise ValueError(f"Col must be one of these {self.spatial_columns}")
            self.configure_column(col_kwargs, cols)

    def configure_inner_frames(self):
        self.create_inner_frames()
        self.grid_inner_frames()


class TrkEntryGroup:
    def __init__(self, parents: list):
        self.parents: List[tk.Frame] = parents      # List of frame objects
        self.width = 15     # No of characters
        self.border_width = 2
        self.labels = ["Tracking No", "Carrier", "Item Description", "Alias"]
        self.entry_objects: List[Dict[str, tk.Entry]] = []
        self.default_grid = [(3, 1)]

    # Generate Entries
    def generate(self, parent_frame: tk.Frame, **kwargs):
        # Create entry widgets for each frame
        # Populate entry_objects list
        kwargs["width"] = kwargs.get("width", self.width)
        kwargs["borderwidth"] = kwargs.get("borderwidth", self.border_width)

        for frame in self.parents:
            dict_ = {}
            count = 0
            for _ in self.labels:
                dict_[self.labels[count]] = tk.Entry(master=frame, **kwargs)
                count += 1
            self.entry_objects.append(dict_)
        return self.label_entries(parent_frame)

    # Label Entries in form of placeholders
    def label_entries(self, parent_frame: tk.Frame):
        # Inserts label placeholders in the entry boxes
        for frames in self.entry_objects:
            count_2 = 0
            for entry in frames.values():
                entry.insert(7, self.labels[count_2])
                count_2 += 1

        return self.auto_grid(parent_frame)

    # Arrange inner frames on TrackingFrame
    def auto_grid(self, parent_frame: tk.Frame):
        starting_row = parent_frame.frame_row_start
        starting_column = parent_frame.frame_column_start
        inner_count = 0
        outer_count = 0

        for frames in self.entry_objects:
            for entry in frames.values():
                entry.grid(row=starting_row + inner_count,
                           column=starting_column)
                inner_count += 1
            outer_count += inner_count + 2
            inner_count = outer_count

