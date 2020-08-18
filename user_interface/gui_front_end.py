from gui_back_end import (
    MainWindow, MenuFrame, MenuBar, FileMenu,TrackingFrame,
    TrkEntryGroup,
)

mainWindow = MainWindow()

# Menu Frame
menuFrame = MenuFrame(mainWindow)
menuFrame.grid(row=0, column=1, rowspan=1, columnspan=7, sticky="ns")

# Menu Bar
menu_bar = MenuBar(menuFrame)
fileMenu = FileMenu(menu_bar)
menu_bar.add_cascade_(fileMenu)

# Tracking Frame
trackingFrame = TrackingFrame(mainWindow)
trackingFrame.batch_spatial_row_col_configure((10, 10))

# Top, bottom, Left, Right config for Tracking Frame spatial rows/cols
f_and_l = trackingFrame.return_first_and_last()
trackingFrame.spatial_row_configure((f_and_l[0]), 30)
trackingFrame.spatial_column_configure((f_and_l[1]), 10)

trackingFrame.grid(row=2, column=1, rowspan=19, columnspan=2, sticky="ns")
trackingFrame.configure_inner_frames()

# Tracking Info Entries
trk_info_entries = TrkEntryGroup([frames for frames in trackingFrame.frames.values()])
trk_info_entries.generate(trackingFrame, width="20")

mainWindow.config(menu=menu_bar)
mainWindow.mainloop()
