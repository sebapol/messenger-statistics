import tkinter
import tkinter.filedialog
import tkinter.messagebox
from tkcalendar import Calendar
import datetime
import matplotlib.pyplot as plt

import analitics
import dataPreparation

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
    for i, f in members:
        exec_txt += f"member{i}_words = tkinter.Label({parent_label_name}, " \
                    f"text=len(grouppedMessages.get_group('{f}')), padx=5)\n" \
                    f"member{i}_words.grid(row={row + i + 1}, column={column})\n"
    exec(exec_txt, glob, loc)
    return None


def set_response_time(parent_label_name, members, col, row, glob, loc):
    def accept_response_time():
        err_label = tkinter.Label(time_window, text='Values must be integers bigger than or equal 0!', fg='red')
        try:
            days = int(days_entry.get())
            assert days >= 0
            days_entry.configure(background='white')
            d_flag = True
        except:
            days_entry.configure(background='red')
            d_flag = False
            err_label.grid(row=2, column=0, columnspan=4)
        try:
            hours = int(hours_entry.get())
            assert hours >= 0
            hours_entry.configure(background='white')
            h_flag = True
        except:
            hours_entry.configure(background='red')
            h_flag = False
            err_label.grid(row=2, column=0, columnspan=4)
        try:
            assert any([days > 0, hours > 0])
            a_flag = True
        except:
            err_label2 = tkinter.Label(time_window, text='At least one value must be bigger than 0!', fg='red')
            err_label2.grid(row=3, column=0, columnspan=4)
            a_flag = False

        if d_flag and h_flag and a_flag:
            loc['max_response_time'] = datetime.timedelta(days=days, hours=hours)
            create_response_times_label(parent_label_name, members, col, row, glob, loc)
            create_who_text_first_label(parent_label_name, members, col + 2, row, glob, loc)
            time_window.destroy()
        return None

    time_window = tkinter.Toplevel()
    time_window.title('Set response time options')
    description = 'Set maximum response time.\n''Message will be consider as response if the time difference between' \
                  ' it and the previous message is less than or equal to setted value.\nIf that difference will be ' \
                  'greater, the sender of that message will be considered as he texted first '
    text_label = tkinter.Label(time_window, text=description)
    days_label = tkinter.Label(time_window, text='Days:')
    hours_label = tkinter.Label(time_window, text='Hours:')

    days_entry = tkinter.Entry(time_window)
    hours_entry = tkinter.Entry(time_window)
    accept_response_button = tkinter.Button(time_window, text='Set response time', command=accept_response_time)

    days_entry.insert(0, loc['max_response_time'].days)
    hours_entry.insert(0, loc['max_response_time'].seconds / 3600)
    text_label.grid(row=0, column=0, columnspan=5)
    days_label.grid(row=1, column=0)
    hours_label.grid(row=1, column=2)

    days_entry.grid(row=1, column=1)
    hours_entry.grid(row=1, column=3)
    accept_response_button.grid(row=1, column=4)

    return None


def clean_column(members, glob, loc):
    exec_txt = ''
    for i, _ in members:
        exec_txt += f"member{i}_words.destroy()\n"
    exec(exec_txt, glob, loc)


def set_most_used_words(parent_label_name, members, col, row, glob, loc):
    def accept_words_options():
        err_label = tkinter.Label(time_window, text='Values must be integers bigger than 0!', fg='red')
        try:
            length = int(length_entry.get())
            assert length > 0
            length_entry.configure(background='white')
            l_flag = True
        except:
            length_entry.configure(background='red')
            l_flag = False
            err_label.grid(row=2, column=0, columnspan=6)
        try:
            amount = int(amount_entry.get())
            assert amount > 0
            amount_entry.configure(background='white')
            a_flag = True
        except:
            amount_entry.configure(background='red')
            a_flag = False
            err_label.grid(row=2, column=0, columnspan=4)

        if l_flag and a_flag:
            loc['min_word_length'] = length
            loc['words_amount'] = amount
            clean_column(members, glob, loc)
            create_most_used_words_label(parent_label_name, members, col, row, glob, loc)
            time_window.destroy()

    time_window = tkinter.Toplevel()
    time_window.title('Set most used words options')
    description = 'Set minimal length and amount of words'
    text_label = tkinter.Label(time_window, text=description)
    length_label = tkinter.Label(time_window, text='Length:')
    amount_label = tkinter.Label(time_window, text='Amount:')

    length_entry = tkinter.Entry(time_window)
    amount_entry = tkinter.Entry(time_window)
    accept_options_button = tkinter.Button(time_window, text='Set options', command=accept_words_options)

    length_entry.insert(0, loc['min_word_length'])
    amount_entry.insert(0, loc['words_amount'])
    text_label.grid(row=0, column=0, columnspan=5)
    length_label.grid(row=1, column=0, sticky=tkinter.W)
    amount_label.grid(row=1, column=2, sticky=tkinter.W)

    length_entry.grid(row=1, column=1, sticky=tkinter.E)
    amount_entry.grid(row=1, column=3, sticky=tkinter.E)
    accept_options_button.grid(row=1, column=4)

    return None


def prepare_analysis_options():
    analysis_frame = tkinter.LabelFrame(root, text=f'6: Analysis:')
    analysis_frame.pack()
    parent_label_name = 'analysis_frame'
    members = list(enumerate(grouppedMessages.groups))

    # todo: zapytać o ilość słów i ich długość
    min_word_length = 4
    words_amount = 5
    max_response_time = datetime.timedelta(hours=12)

    glob = globals()
    loc = locals()

    response_time_button = tkinter.Button(analysis_frame, text='Set response time options',
                                          command=lambda: set_response_time(parent_label_name, members, 3, 1, glob,
                                                                            loc))
    response_time_button.grid(row=0, column=3, columnspan=3, sticky=tkinter.W + tkinter.E)
    most_used_words_button = tkinter.Button(analysis_frame, text='Set most used words options',
                                            command=lambda: set_most_used_words(parent_label_name, members, 6, 1, glob,
                                                                                loc))
    most_used_words_button.grid(row=0, column=6, sticky=tkinter.W + tkinter.E)

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

    row += len(members) + 1
    hourly_histogram_button = tkinter.Button(analysis_frame, text='Show hourly histogram', command=hourly_histogram)
    hourly_histogram_button.grid(row=row, column=0)
    daily_histogram_button = tkinter.Button(analysis_frame, text='Show daily histogram', command=daily_histogram)
    daily_histogram_button.grid(row=row, column=1)
    monthly_histogram_button = tkinter.Button(analysis_frame, text='Show monthly histogram', command=monthly_histogram)
    monthly_histogram_button.grid(row=row, column=2)
    return None


def prepare_data(chat_members, choose, action_button, membersMenu):
    def accept_start_date():
        global startDate
        startDate = dateMenu.get_date()
        startDate = datetime.datetime.strptime(startDate, '%m/%d/%y')
        lowerLabel['text'] = 'End date:'
        dateMenu.selection_set(maximum)
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
    minimum = data['DateTime'].min()
    maximum = data['DateTime'].max()

    dateFrame = tkinter.LabelFrame(root, text=f'5: Choose date range for analysis:')
    dateFrame.pack()
    lowerLabel = tkinter.Label(dateFrame, text='Start date:')
    lowerLabel.grid(row=1, column=0)

    dateMenu = Calendar(dateFrame, selectmode='day', mindate=minimum, maxdate=maximum,
                        year=minimum.year, month=minimum.month, day=minimum.day)
    dateMenu.grid(row=1, column=1)
    acceptDateButton = tkinter.Button(dateFrame, text='Accept date', command=accept_start_date)
    acceptDateButton.grid(row=1, column=2)
    return None


def setData():
    def check_choose():
        if choose.get():
            prepare_data(chat_members, choose, actionButton, membersMenu)
        else:
            tkinter.messagebox.showwarning('No chat member chosen', 'First you have to choose chat member!')
        return None

    try:
        chat_members = dataPreparation.give_chat_members(filepath)
    except dataPreparation.DirectoryException:
        tkinter.messagebox.showerror('Filepath error', 'Wrong file path!\nChoose proper file path.')
        directoryClick()
        return None

    global choose
    acceptButton['state'] = 'disabled'
    directoryButton['state'] = 'disabled'
    memberFrame = tkinter.LabelFrame(root, text=f'4: Choose a chat member:')
    memberFrame.pack()
    choose = tkinter.StringVar()
    membersMenu = tkinter.OptionMenu(memberFrame, choose, *chat_members.keys())
    membersMenu.pack()
    actionButton = tkinter.Button(memberFrame, text='Accept selection', command=check_choose)
    actionButton.pack()
    return None


def directoryClick():
    global filepath
    try:
        filepath = tkinter.filedialog.askdirectory(initialdir=open('._lastdir').read(), title='Select a directory')
    except:
        filepath = tkinter.filedialog.askdirectory(initialdir='./', title='Select a directory')
    with open('._lastdir', 'w') as f:
        f.write(filepath)
    filepathLabel['text'] = filepath
    acceptButton['state'] = 'normal'
    return None


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title('Messenger Analyzer')
    root.iconbitmap('./icon.ico')
    root.geometry('1366x768')

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

    try:
        filepath = open('._lastdir').read()
        filepathLabel['text'] = filepath
    except:
        acceptButton['state'] = 'disabled'

    titleLabel.pack()
    directoryFrame.pack()
    directoryButton.pack()
    filepathFrame.pack()
    filepathLabel.pack()
    acceptButton.pack()

    root.mainloop()
