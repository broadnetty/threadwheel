from tableparser import parser as ps
import PySimpleGUI as sg

'''
for thread in ps().parse_to_list():
    if thread['status'] != 'Closed':
        print(thread)'''
datarows = ps().parse_to_list()
headings = [ key for key in datarows[0] ]

def resfresh_data():
    datarows = ps().parse_to_list()

    data=[]


    for row in datarows:
        set=[]
        for key in row:
            set.append(row[key])
        data.append(set)

    return data

layout = [[sg.Table(values=resfresh_data(), headings=headings, max_col_width=75,
                    auto_size_columns=True,
                    # cols_justification=('left','center','right','c', 'l', 'bad'),       # Added on GitHub only as of June 2022
                    display_row_numbers=False,
                    justification='left',
                    num_rows=30,
                    #alternating_row_color='lightblue',
                    key='-TABLE-',
                    #selected_row_colors='red on yellow',
                    enable_events=True,
                    expand_x=False,
                    expand_y=True,
                    vertical_scroll_only=False,
                    enable_click_events=True)],
          [sg.Button('Read'), sg.Button('Change Colors'), sg.Button('Refresh')],
          [sg.Text('Read = read which rows are selected')],
          [sg.Text('Change Colors = Changes the colors of rows 8 and 9'), sg.Sizegrip()]]

# ------ Create Window ------
window = sg.Window('The Table Element', layout,
                   # ttk_theme='clam',
                   # font='Helvetica 25',
                   resizable=True
                   )

# ------ Event Loop ------
while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED:
        break

    if event == 'Refresh':
        window['-TABLE-'].update(values=resfresh_data())
    if event == 'Change Colors':
        window['-TABLE-'].update(row_colors=((8, 'white', 'red'), (9, 'green')))

window.close()

