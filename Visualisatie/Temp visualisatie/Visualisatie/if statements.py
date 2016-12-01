def move_vehicle(vehicles, archive, queue):
    children = []
    for table_queue in queue.items:
        for vehicle in vehicles:
            if vehicle.orientation == 'hor' and vehicle.col_v > 0:
                if table_queue[vehicle.row_v][vehicle.col_v - 1] == ' ':
                    vehicle.col_v -= 1
                    new_table = table_retriever(vehicles, 6)
                    for i in queue.items:
                        if new_table == i:
                            vehicle.col_v += 1
                            continue
                    visualize(new_table, 6, 6)

                    children.append(new_table)

            elif vehicle.orientation == 'hor' and vehicle.col_v + vehicle.length <= 5:
                if table_queue[vehicle.row_v][vehicle.col_v + vehicle.length+1] == ' ':
                    vehicle.col_v += 1
                    new_table = table_retriever(vehicles, 6)
                    for i in queue.items:
                        if new_table == i:
                            vehicle.col_v -= 1
                            continue
                    visualize(new_table, 6, 6)

                    children.append(new_table)

            if vehicle.orientation == 'ver' and vehicle.row_v > 0:
                if table_queue[vehicle.row_v - 1][vehicle.col_v] == ' ':
                    vehicle.row_v -= 1
                    new_table = table_retriever(vehicles, 6)
                    for i in queue.items:
                        if new_table == i:
                                vehicle.row_v += 1
                                continue
                    visualize(new_table, 6, 6)

                    children.append(new_table)

            elif vehicle.orientation == 'ver' and vehicle.row_v + vehicle.length <= 5:
                if table_queue[vehicle.row_v + vehicle.length+1][vehicle.col_v] == ' ':
                    vehicle.row_v += 1
                    new_table = table_retriever(vehicles, 6)
                    for i in queue.items:
                        if new_table == i:
                            vehicle.row_v -= 1
                            continue
                    visualize(new_table, 6, 6)

                    children.append(new_table)


        myfunc()
#    for i in range(len(table)):
#        for j in range(len(table)):
#             print table[i][j]
    return children


def visualize(table, width, height):
    canvas = Tkinter.Tk()
    for r in range(width):
        for c in range(height):
            if table[r][c][0] in CAR_ID:
                Tkinter.Label(canvas, text=(table[r][c]), borderwidth=20, background=CAR_ID[table[r][c][0]]).grid(row=r, column=c)
            else:
                Tkinter.Label(canvas, text=(table[r][c]), borderwidth=20, background=TRUCKS_ID[table[r][c][0]]).grid(row=r, column=c)
    canvas.mainloop()