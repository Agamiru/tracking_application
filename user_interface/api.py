# API


"""
Common Entities: Space, Relative Position, Widget settings,
positions = above, below, beside_right, beside_left, row, col

main_window = MainWindow()

menuFrame = main_window.add_Frame(**kwargs)
menuFrame.grid(row=0, column=1, rowspan=1, columnspan=7, sticky="ns")

menuBar = menuFrame.add_menu(**kwargs)
fileMenu = menuBar.add_menu(**kwargs)
fileMenu.commands

trackingFrame = mainWindow.add_frame(row_span, col_span, **kwargs)
trackingFrame.set_widget(**kwargs)
trackingFrame.position(below, menuFrame, 1)
trackingFrame.spatial_rows_configure()
trackingFrame.spatial_cols_configure()

entryFrameGroup = trackingFrame.add_group(entry, how_many, col_span)
entryFrameGroup.set_widget(**kwargs)
entryFrameGroup.spatial_rows_configure()

# add_to_group (space options): available_space, positions

button1 = add_to_group(group, available_space
button1.

trackingEntries = entryFrames.add_entry(how_many, **kwargs)


"""