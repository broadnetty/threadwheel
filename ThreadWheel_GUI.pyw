#!.\venv\Scripts\pythonw.exe
from tableparser import parser as ps
import PySimpleGUI as sg
import sqlite3
import textwrap

'''
for thread in ps().parse_to_list():
    if thread['status'] != 'Closed':
        print(thread)'''

headings = [ 'Case', 'Status', 'Topic', 'Case owner', 'Active person', 'Date created', 'Date modified' ]

reverse_order = False

try:
    agent = ps()

except Exception as e:
    layout=[[sg.Text(textwrap.wrap('Error: ' + str(e), 200), size=(50,None))],[sg.Button('Ok')]]
    window = sg.Window('Error', layout, element_justification='c')
    while True:
        event, values = window.read()
        break
    window.close()
    exit(1)

layout = [[sg.Table(values=agent.get_table_data(), headings=headings, max_col_width=75,
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
          [sg.Button('Show all'), sg.Button('Filter'), sg.Text('By owner: '),sg.Combo(agent.get_engineers_list(), default_value='All', key='filter_engineer'),
           sg.Text('By status: '), sg.Combo(agent.get_status_list(), default_value='All', key='filter_status')],
          [sg.Sizegrip()]]

# ------ Create Window ------
window = sg.Window('Thread Wheel', layout,
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

    if event == 'Show all':
        window['-TABLE-'].update(values=agent.refresh_data())

    if '-TABLE-' in str(event) and '+CLICKED+' in str(event):
        if event[2][0] == -1:
            agent.sort_by_column(event[2][1],reverse=reverse_order)
            reverse_order = True if not reverse_order else False
            window['-TABLE-'].update(values=agent.get_table_data())

    if event == 'Change Colors':
        window['-TABLE-'].update(row_colors=((8, 'white', 'red'), (9, 'green')))

    if event == 'Filter':
        filters = {3: values['filter_engineer'], 1: values['filter_status']}
        window['-TABLE-'].update(values=agent.get_crossfiltered_data(filters))

window.close()

