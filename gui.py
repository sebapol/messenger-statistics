import tkinter
import tkinter.filedialog
import tkinter.messagebox
from tkcalendar import Calendar
import datetime
import matplotlib.pyplot as plt

import analytics
import dataPreparation


def hourly_histogram():
    analytics.hourly_texting_histogram(messages)
    plt.show()
    return None


def daily_histogram():
    analytics.daily_texting_histogram(messages)
    plt.show()
    return None


def monthly_histogram():
    analytics.monthly_texting_histogram(messages)
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
    exec_txt = f"used_words_head = tkinter.Label({parent_label_name}, text='Most used words:')\n" \
               f"used_words_head.grid(row={row}, column={column})\n"
    for i, f in members:
        exec_txt += f"member{i}_used_words = tkinter.Label({parent_label_name}, " \
                    f"text=analytics.give_most_used_words(grouped_messages, " \
                    f"'{f}', min_word_length, words_amount), padx=5)\n" \
                    f"member{i}_used_words.grid(row={row + i + 1}, column={column})\n"
    exec(exec_txt, glob, loc)
    return None


def create_who_text_first_label(parent_label_name, members, column, row, glob, loc):
    exec_txt = f"used_words = tkinter.Label({parent_label_name}, text=f'Who texts first:')\n" \
               f"used_words.grid(row={row}, column={column})\n" \
               f"first_text = analytics.who_text_first(messages, max_response_time)\n"
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
                    f"text=round(analytics.average_message_length(grouped_messages, '{f}'), 2), padx=5)\n" \
                    f"member{i}_words.grid(row={row + i + 1}, column={column})\n"
    exec(exec_txt, glob, loc)
    return None


def create_response_times_label(parent_label_name, members, column, row, glob, loc):
    exec_txt = f"avg_words = tkinter.Label({parent_label_name}, text=f'Average response time:')\n" \
               f"avg_words.grid(row={row}, column={column})\n" \
               f"median_words = tkinter.Label(analysis_frame, text=f'Median of response time:')\n" \
               f"median_words.grid(row={row}, column={column + 1})\n" \
               f"members_response = analytics.response_times(messages, max_response_time)\n"
    for i, f in members:
        exec_txt += f"member{i}_avg = tkinter.Label({parent_label_name}, " \
                    f"text=analytics.average_response_time(members_response, '{f}'), padx=5)\n" \
                    f"member{i}_avg.grid(row={row + i + 1}, column={column})\n" \
                    f"member{i}_median = tkinter.Label({parent_label_name}, " \
                    f"text=analytics.median_response_time(members_response, '{f}'), padx=5)\n" \
                    f"member{i}_median.grid(row={row + i + 1}, column={column + 1})\n"
    exec(exec_txt, glob, loc)
    return None


def create_message_number_label(parent_label_name, members, column, row, glob, loc):
    exec_txt = f"used_words = tkinter.Label({parent_label_name}, text=f'Number of messages:')\n" \
               f"used_words.grid(row={row}, column={column})\n"
    for i, f in members:
        exec_txt += f"member{i}_words = tkinter.Label({parent_label_name}, " \
                    f"text=len(grouped_messages.get_group('{f}')), padx=5)\n" \
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
        except (AssertionError, ValueError):
            days_entry.configure(background='red')
            d_flag = False
            err_label.grid(row=2, column=0, columnspan=4)
        try:
            hours = int(hours_entry.get())
            assert hours >= 0
            hours_entry.configure(background='white')
            h_flag = True
        except (AssertionError, ValueError):
            hours_entry.configure(background='red')
            h_flag = False
            err_label.grid(row=2, column=0, columnspan=4)
        try:
            assert any([days > 0, hours > 0])
            a_flag = True
        except (AssertionError, UnboundLocalError):
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
    hours_entry.insert(0, round(loc['max_response_time'].seconds / 3600))
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
        exec_txt += f"member{i}_used_words.destroy()\n"
    exec(exec_txt, glob, loc)


def set_most_used_words(parent_label_name, members, col, row, glob, loc):
    def accept_words_options():
        err_label = tkinter.Label(time_window, text='Values must be integers bigger than 0!', fg='red')
        try:
            length = int(length_entry.get())
            assert length > 0
            length_entry.configure(background='white')
            l_flag = True
        except (AssertionError, ValueError):
            length_entry.configure(background='red')
            l_flag = False
            err_label.grid(row=2, column=0, columnspan=6)
        try:
            amount = int(amount_entry.get())
            assert amount > 0
            amount_entry.configure(background='white')
            a_flag = True
        except (AssertionError, ValueError):
            amount_entry.configure(background='red')
            a_flag = False
            err_label.grid(row=2, column=0, columnspan=4)

        if l_flag and a_flag:
            loc['min_word_length'] = length
            loc['words_amount'] = amount
            clean_column(members, glob, loc)
            create_most_used_words_label(parent_label_name, members, col, row, glob, loc)
            time_window.destroy()
        return None

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
    members = list(enumerate(grouped_messages.groups))

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


def prepare_data(chat_members, choose, action_button, members_menu):
    def accept_start_date():
        global start_date
        start_date = date_menu.get_date()
        start_date = datetime.datetime.strptime(start_date, '%m/%d/%y')
        lower_label['text'] = 'End date:'
        date_menu.selection_set(maximum)
        upper_label = tkinter.Label(date_frame, text=f'Start date: {start_date.date()}')
        upper_label.grid(row=0, column=0)
        accept_date_button.configure(command=accept_end_date)
        return None

    def accept_end_date():
        global messages
        global grouped_messages
        end_date = date_menu.get_date()
        end_date = datetime.datetime.strptime(end_date, '%m/%d/%y')
        lower_label['text'] = f'End date: {end_date.date()}'
        date_menu.destroy()
        accept_date_button.destroy()
        try:
            messages = dataPreparation.filter_data_by_date(data, start_date, end_date)
            grouped_messages = dataPreparation.group_data_by_users(messages)
            prepare_analysis_options()
        except (ValueError, KeyError) as e:
            date_frame.destroy()
            tkinter.messagebox.showerror('Wrong date range!', f'{e}\n\nSet different time range')
            prepare_data(chat_members, choose, action_button, members_menu)
        return None

    action_button['state'] = 'disabled'
    members_menu['state'] = 'disabled'
    path = chat_members[choose.get()].removesuffix('message_1.json')
    data = dataPreparation.load_message_file_from_directory(path)
    data = dataPreparation.format_data(data)
    minimum = data['DateTime'].min()
    maximum = data['DateTime'].max()

    date_frame = tkinter.LabelFrame(root, text=f'5: Choose date range for analysis:')
    date_frame.pack()
    lower_label = tkinter.Label(date_frame, text='Start date:')
    lower_label.grid(row=1, column=0)

    date_menu = Calendar(date_frame, selectmode='day', mindate=minimum, maxdate=maximum,
                         year=minimum.year, month=minimum.month, day=minimum.day)
    date_menu.grid(row=1, column=1)
    accept_date_button = tkinter.Button(date_frame, text='Accept date', command=accept_start_date)
    accept_date_button.grid(row=1, column=2)
    return None


def set_data():
    def check_choose():
        if choice.get():
            prepare_data(chat_members, choice, action_button, members_menu)
        else:
            tkinter.messagebox.showwarning('No chat member chosen', 'First you have to choose chat member!')
        return None

    try:
        chat_members = dataPreparation.give_chat_members(filepath)
    except dataPreparation.DirectoryException:
        tkinter.messagebox.showerror('Filepath error', 'Wrong file path!\nChoose proper file path.')
        directory_click()
        return None

    global choice
    acceptButton['state'] = 'disabled'
    directoryButton['state'] = 'disabled'
    member_frame = tkinter.LabelFrame(root, text=f'4: Choose a chat member:')
    member_frame.pack()
    choice = tkinter.StringVar()
    members_menu = tkinter.OptionMenu(member_frame, choice, *chat_members.keys())
    members_menu.pack()
    action_button = tkinter.Button(member_frame, text='Accept selection', command=check_choose)
    action_button.pack()
    return None


def directory_click():
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
    directoryButton = tkinter.Button(directoryFrame, text='Choose directory', command=directory_click)
    filepathFrame = tkinter.LabelFrame(directoryFrame, text=f'Chosen directory:')
    filepathLabel = tkinter.Label(filepathFrame, text='')
    acceptButton = tkinter.Button(directoryFrame, text='Accept directory', command=set_data)

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
