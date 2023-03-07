from tkinter import *
from tkinter import filedialog
from tkcalendar import Calendar
import datetime
import matplotlib.pyplot as plt

import analitics
import dataPreparation
import locale
locale.setlocale(locale.LC_ALL, 'pl_PL')


root = Tk()
root.title('Messenger Analyzer')
root.iconbitmap('./icon.ico')
root.geometry('1080x720')

def hourlyHistogram():
    analitics.hourlyTextingHistogram(messages)
    plt.show()
    return None

def dailyHistogram():
    analitics.dailyTextingHistogram(messages)
    plt.show()
    return None

def monthlyHistogram():
    analitics.monthlyTextingHistogram(messages)
    plt.show()
    return None

def prepareAnalysisOptions():
    analysisFrame = LabelFrame(root, text=f'6: Choose analysis to execute:')
    analysisFrame.pack()
    memberLabel = Label(analysisFrame, text=f'Member: {choose.get()}', padx=5)
    memberLabel.grid(row=0,column=1)
    me = [f for f in grouppedMessages.groups if f != choose.get()][0]
    memberLabel2 = Label(analysisFrame, text=f'Member: {me}', padx=5)
    memberLabel2.grid(row=0, column=2)

    usedWords = Label(analysisFrame, text=f'Most used words:')
    usedWords.grid(row=1, column=0)
    memberWords = Label(analysisFrame, text=analitics.showMostUsedWords(grouppedMessages, choose.get(), 3, 5), padx=5)
    memberWords.grid(row=1, column=1)
    member2Words = Label(analysisFrame, text=analitics.showMostUsedWords(grouppedMessages, me, 3, 5), padx=5)
    member2Words.grid(row=1, column=2)

    maxResponseTime = datetime.timedelta(hours=12)
    usedWords = Label(analysisFrame, text=f'Who texts first:')
    usedWords.grid(row=2, column=0)
    memberWords = Label(analysisFrame,text=analitics.whoTextFirst(messages, maxResponseTime)[choose.get()], padx=5)
    memberWords.grid(row=2, column=1)
    member2Words = Label(analysisFrame, text=analitics.whoTextFirst(messages, maxResponseTime)[me], padx=5)
    member2Words.grid(row=2, column=2)

    usedWords = Label(analysisFrame, text=f'Average message length:')
    usedWords.grid(row=3, column=0)
    memberWords = Label(analysisFrame,
                        text=analitics.averageMessageLength(grouppedMessages, choose.get()), padx=5)
    memberWords.grid(row=3, column=1)
    member2Words = Label(analysisFrame, text=analitics.averageMessageLength(grouppedMessages, me), padx=5)
    member2Words.grid(row=3, column=2)

    myResponse = analitics.responseTimes(messages, me, maxResponseTime)
    memberResponse = analitics.responseTimes(messages, choose.get(), maxResponseTime)

    usedWords = Label(analysisFrame, text=f'Average response time:')
    usedWords.grid(row=4, column=0)
    memberWords = Label(analysisFrame,
                        text=analitics.averageResponseTime(memberResponse), padx=5)
    memberWords.grid(row=4, column=1)
    member2Words = Label(analysisFrame,
                         text=analitics.averageResponseTime(myResponse), padx=5)
    member2Words.grid(row=4, column=2)

    usedWords = Label(analysisFrame, text=f'Median of response time:')
    usedWords.grid(row=5, column=0)
    memberWords = Label(analysisFrame,
                        text=analitics.medianResponseTime(memberResponse),
                        padx=5)
    memberWords.grid(row=5, column=1)
    member2Words = Label(analysisFrame,
                         text=analitics.medianResponseTime(myResponse), padx=5)
    member2Words.grid(row=5, column=2)

    usedWords = Label(analysisFrame, text=f'Number of messages:')
    usedWords.grid(row=6, column=0)
    memberWords = Label(analysisFrame, text=len(grouppedMessages.get_group(choose.get())), padx=5)
    memberWords.grid(row=6, column=1)
    member2Words = Label(analysisFrame, text=len(grouppedMessages.get_group(me)), padx=5)
    member2Words.grid(row=6, column=2)

    hourlyHistogramButton = Button(analysisFrame, text='Show hourly histogram', command=hourlyHistogram)
    hourlyHistogramButton.grid(row=7, column=0)

    dailyHistogramButton = Button(analysisFrame, text='Show daily histogram', command=dailyHistogram)
    dailyHistogramButton.grid(row=7, column=1)

    monthlyHistogramButton = Button(analysisFrame, text='Show monthly histogram', command=monthlyHistogram)
    monthlyHistogramButton.grid(row=7, column=2)
    return None

def prepareData(chat_members, choose, actionButton):

    def acceptStartDate():
        global startDate
        startDate = dateMenu.get_date()
        startDate = datetime.datetime.strptime(startDate, '%m/%d/%y')
        lowerLabel['text'] = 'End date:'
        upperLabel = Label(dateFrame, text=f'Start date: {startDate.date()}')
        upperLabel.grid(row=0, column=0)
        acceptDateButton.configure(command = acceptEndDate)
        return None

    def acceptEndDate():
        global messages
        global grouppedMessages
        endDate = dateMenu.get_date()
        endDate = datetime.datetime.strptime(endDate, '%m/%d/%y')
        lowerLabel['text'] = f'End date: {endDate.date()}'
        dateMenu.destroy()
        acceptDateButton.destroy()
        messages = dataPreparation.filterDataByDate(data, startDate, endDate)
        grouppedMessages = dataPreparation.groupDataByUsers(messages)
        prepareAnalysisOptions()
        return None

    actionButton['state'] = 'disabled'
    path = chat_members[choose.get()].removesuffix('message_1.json')
    data = dataPreparation.loadMessageFilesFromDirectory(path)
    data = dataPreparation.formatData(data)
    dateFrame = LabelFrame(root, text=f'5: Choose date range for analysis:')
    dateFrame.pack()
    lowerLabel = Label(dateFrame, text='Start date:')
    lowerLabel.grid(row=1,column=0)
    min = data['DateTime'].min()
    max = data['DateTime'].max()
    dateMenu = Calendar(dateFrame, selectmode = 'day',
               mindate=min, maxdate=max)
    dateMenu.grid(row=1, column=1)
    acceptDateButton = Button(dateFrame, text='Accept date', command=acceptStartDate)
    acceptDateButton.grid(row=1, column=2)
    return None

def setData():
    #global chat_members
    global choose
    #global actionButton
    acceptButton['state'] = 'disabled'
    chat_members = dataPreparation.giveChatMembers(filepath)
    memberFrame = LabelFrame(root, text=f'4: Choose a chat member:')
    memberFrame.pack()
    choose = StringVar()
    membersMenu = OptionMenu(memberFrame, choose, *chat_members.keys())
    membersMenu.pack()
    actionButton = Button(memberFrame, text='Accept selection', command=lambda: prepareData(chat_members, choose, actionButton))
    actionButton.pack()
    return None

def directoryClick():
    global filepath
    try:
        filepath = filedialog.askdirectory(initialdir=open('.my_script_lastdir').read(), title='Select a directory')
    except:
        filepath = filedialog.askdirectory(initialdir='./', title='Select a directory')
    with open('.my_script_lastdir', 'w') as f:
        f.write(filepath)
    filepathLabel['text'] = filepath
    acceptButton['state'] = 'normal'
    return None


titleLabel = Label(root, text = 'Welcome in Messenger Analyzer\n\nAnalyze your Messenger data:\n'
                                '\n1. Get your Faacebook data (https://www.facebook.com/help/212802592074644/?helpref=uf_share)\n'
                                '   Pay attention to chose .json file format\n'
                                '\n2. Unzip your downloaded data\n')

directoryFrame = LabelFrame(root, text = '3: Choose a directory to your unzipped data:')
directoryButton = Button(directoryFrame, text='Choose directory', command=directoryClick)
filepathFrame = LabelFrame(directoryFrame, text = f'Chosen directory:')
filepathLabel = Label(filepathFrame, text='')
acceptButton = Button(directoryFrame, text='Accept directory', command=setData)
acceptButton['state'] = 'disabled'

titleLabel.pack()
directoryFrame.pack()
directoryButton.pack()
filepathFrame.pack()
filepathLabel.pack()
acceptButton.pack()


root.mainloop()
