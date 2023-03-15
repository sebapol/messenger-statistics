import tkinter
from tkinter import filedialog
from tkcalendar import Calendar
import datetime
import time
import matplotlib.pyplot as plt

import analitics
import dataPreparation


root = tkinter.Tk()
root.title('Messenger Analyzer')
root.iconbitmap('./icon.ico')
root.geometry('1366x768')


def hourly_histogram():
    analitics.hourly_texting_histogram(messages)
    plt.show()
    return None


def daily_histogram():
    analitics.daily_texting_histogram(messages)
    plt.show()
    return None


def monthly_histogram():
    analitics.monthly_texting_histogram(messages)
    plt.show()
    return None


def create_members_labels(parent_label_name, members, column, row, glob, loc):
    exec_txt = f"used_words = tkinter.Label({parent_label_name}, text='Member:')\n" \
               f"used_words.grid(row={row}, column={column})\n"
    for i, f in members:
        exec_txt += f"member{i}_label= tkinter.Label({parent_label_name}, text='{f}', padx=5)\n" \
                    f"member{i}_label.grid(row={row + i + 1}, column={column})\n"
    exec(exec_txt, glob, loc)
    return None


def create_most_used_words_label(parent_label_name, members, column, row, glob, loc):
    exec_txt = f"used_words = tkinter.Label({parent_label_name}, text='Most used words:')\n" \
               f"used_words.grid(row={row}, column={column})\n"
    for i, f in members:
        exec_txt += f"member{i}_words = tkinter.Label({parent_label_name}, " \
                    f"text=analitics.give_most_used_words(grouppedMessages, " \
                    f"'{f}', min_word_length, words_amount), padx=5)\n" \
                    f"member{i}_words.grid(row={row + i + 1}, column={column})\n"
    exec(exec_txt, glob, loc)
    return None


def create_who_text_first_label(parent_label_name, members, column, row, glob, loc):
    exec_txt = f"used_words = tkinter.Label({parent_label_name}, text=f'Who texts first:')\n" \
               f"used_words.grid(row={row}, column={column})\n" \
               f"first_text = analitics.who_text_first(messages, max_response_time)\n"
    for i, f in members:
        exec_txt += f"member{i}_words = tkinter.Label({parent_label_name}," \
                    f"text=first_text['{f}'], padx=5)\n" \
                    f"member{i}_words.grid(row={row + i + 1}, column={column})\n"
    exec(exec_txt, glob, loc)
    return None


def create_avg_message_len_label(parent_label_name, members, column, row, glob, loc):
    exec_txt = f"used_words = tkinter.Label({parent_label_name}, text=f'Average message length:')\n" \
               f"used_words.grid(row={row}, column={column})\n"
    for i, f in members:
        exec_txt += f"member{i}_words = tkinter.Label(analysis_frame, " \
                    f"text=round(analitics.average_message_length(grouppedMessages, '{f}'), 2), padx=5)\n" \
                    f"member{i}_words.grid(row={row + i + 1}, column={column})\n"
    exec(exec_txt, glob, loc)
    return None


def create_response_times_label(parent_label_name, members, column, row, glob, loc):
    exec_txt = f"avg_words = tkinter.Label({parent_label_name}, text=f'Average response time:')\n" \
               f"avg_words.grid(row={row}, column={column})\n" \
               f"median_words = tkinter.Label(analysis_frame, text=f'Median of response time:')\n" \
               f"median_words.grid(row={row}, column={column + 1})\n" \
               f"members_response = analitics.response_times(messages, max_response_time)\n"
    for i, f in members:
        exec_txt += f"member{i}_avg = tkinter.Label({parent_label_name}, " \
                    f"text=analitics.average_response_time(members_response, '{f}'), padx=5)\n" \
                    f"member{i}_avg.grid(row={row + i + 1}, column={column})\n" \
                    f"member{i}_median = tkinter.Label({parent_label_name}, " \
                    f"text=analitics.median_response_time(members_response, '{f}'), padx=5)\n" \
                    f"member{i}_median.grid(row={row + i + 1}, column={column + 1})\n"
    exec(exec_txt, glob, loc)
    return None


def create_message_number_label(parent_label_name, members, column, row, glob, loc):
    exec_txt = f"used_words = tkinter.Label({parent_label_name}, text=f'Number of messages:')\n" \
               f"used_words.grid(row={row}, column={column})\n"
    # todo: zrobić pętlę dla wszystkich użytkowników
    for i, f in members:
        exec_txt += f"member{i}_words = tkinter.Label({parent_label_name}, " \
                    f"text=len(grouppedMessages.get_group('{f}')), padx=5)\n" \
                    f"member{i}_words.grid(row={row + i + 1}, column={column})\n"
    exec(exec_txt, glob, loc)
    return None


def prepare_analysis_options():
    analysis_frame = tkinter.LabelFrame(root, text=f'6: Choose analysis to execute:')
    analysis_frame.pack()
    parent_label_name = 'analysis_frame'
    members = list(enumerate(grouppedMessages.groups))

    # todo: zapytać o ilość słów i ich długość
    min_word_length = 4
    words_amount = 5
    # todo: zapytać o max response time
    max_response_time = datetime.timedelta(hours=12)

    glob = globals()
    loc = locals()

    hourly_histogram_button = tkinter.Button(analysis_frame, text='Show hourly histogram', command=hourly_histogram)
    hourly_histogram_button.grid(row=0, column=0)

    daily_histogram_button = tkinter.Button(analysis_frame, text='Show daily histogram', command=daily_histogram)
    daily_histogram_button.grid(row=0, column=1)

    monthly_histogram_button = tkinter.Button(analysis_frame, text='Show monthly histogram', command=monthly_histogram)
    monthly_histogram_button.grid(row=0, column=2)

    start = time.time()
    col = 0
    row = 1
    create_members_labels(parent_label_name, members, col, row, glob, loc)
    col += 1
    create_message_number_label(parent_label_name, members, col, row, glob, loc)
    col += 1
    create_avg_message_len_label(parent_label_name, members, col, row, glob, loc)
    col += 1
    create_response_times_label(parent_label_name, members, col, row, glob, loc)
    col += 2
    create_who_text_first_label(parent_label_name, members, col, row, glob, loc)
    col += 1
    create_most_used_words_label(parent_label_name, members, col, row, glob, loc)
    col += 1
    print('Execution time:', time.time()- start)
    return None


def prepare_data(chat_members, choose, action_button, membersMenu):
    def accept_start_date():
        global startDate
        startDate = dateMenu.get_date()
        startDate = datetime.datetime.strptime(startDate, '%m/%d/%y')
        lowerLabel['text'] = 'End date:'
        upperLabel = tkinter.Label(dateFrame, text=f'Start date: {startDate.date()}')
        upperLabel.grid(row=0, column=0)
        acceptDateButton.configure(command=acceptEndDate)
        return None

    def acceptEndDate():
        global messages
        global grouppedMessages
        endDate = dateMenu.get_date()
        endDate = datetime.datetime.strptime(endDate, '%m/%d/%y')
        lowerLabel['text'] = f'End date: {endDate.date()}'
        dateMenu.destroy()
        acceptDateButton.destroy()
        messages = dataPreparation.filter_data_by_date(data, startDate, endDate)  # todo: add exceptions handling
        grouppedMessages = dataPreparation.group_data_by_users(messages)
        prepare_analysis_options()
        return None

    action_button['state'] = 'disabled'
    membersMenu['state'] = 'disabled'
    path = chat_members[choose.get()].removesuffix('message_1.json')
    data = dataPreparation.load_message_file_from_directory(path)
    data = dataPreparation.format_data(data)
    dateFrame = tkinter.LabelFrame(root, text=f'5: Choose date range for analysis:')
    dateFrame.pack()
    lowerLabel = tkinter.Label(dateFrame, text='Start date:')
    lowerLabel.grid(row=1, column=0)
    min = data['DateTime'].min()
    max = data['DateTime'].max()
    dateMenu = Calendar(dateFrame, selectmode='day',
                        mindate=min, maxdate=max)
    dateMenu.grid(row=1, column=1)
    acceptDateButton = tkinter.Button(dateFrame, text='Accept date', command=accept_start_date)
    acceptDateButton.grid(row=1, column=2)
    return None


def setData():
    # global chat_members
    global choose
    # global actionButton
    acceptButton['state'] = 'disabled'
    directoryButton['state'] = 'disabled'
    chat_members = dataPreparation.give_chat_members(filepath)
    memberFrame = tkinter.LabelFrame(root, text=f'4: Choose a chat member:')
    memberFrame.pack()
    choose = tkinter.StringVar()
    membersMenu = tkinter.OptionMenu(memberFrame, choose, *chat_members.keys())
    membersMenu.pack()
    actionButton = tkinter.Button(memberFrame,
                                  text='Accept selection',
                                  command=lambda: prepare_data(chat_members, choose, actionButton, membersMenu))
    actionButton.pack()
    return None


def directoryClick():
    global filepath
    try:
        filepath = filedialog.askdirectory(initialdir=open('._lastdir').read(), title='Select a directory')
    except:
        filepath = filedialog.askdirectory(initialdir='./', title='Select a directory')
    with open('._lastdir', 'w') as f:
        f.write(filepath)
    filepathLabel['text'] = filepath
    acceptButton['state'] = 'normal'
    return None


txt = 'Welcome in Messenger Analyzer\n\nAnalyze your Messenger data:\n\n1. Get your Faacebook data: ' \
      'https://www.facebook.com/help/212802592074644/?helpref=uf_share\n' \
      '   Pay attention to chose .json file format\n\n' \
      '2. Unzip your downloaded data\n'

titleLabel = tkinter.Label(root, text=txt)

directoryFrame = tkinter.LabelFrame(root, text='3: Choose a directory to your unzipped data:')
directoryButton = tkinter.Button(directoryFrame, text='Choose directory', command=directoryClick)
filepathFrame = tkinter.LabelFrame(directoryFrame, text=f'Chosen directory:')
filepathLabel = tkinter.Label(filepathFrame, text='')
acceptButton = tkinter.Button(directoryFrame, text='Accept directory', command=setData)
acceptButton['state'] = 'disabled'

titleLabel.pack()
directoryFrame.pack()
directoryButton.pack()
filepathFrame.pack()
filepathLabel.pack()
acceptButton.pack()

root.mainloop()
