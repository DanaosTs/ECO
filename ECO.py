from functools import partial
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.metrics import dp
from cryptography.fernet import Fernet
from urllib.parse import unquote
from kivy.clock import mainthread
from bs4 import BeautifulSoup
from functools import partial
import threading, os, datetime, re, time, requests, subprocess, sys

file_explr = os.path.expanduser('~' + "/Desktop/University").replace("\\","/")

kv = '''
<TabbedPanelHeader>:
    background_color: {'normal': (1, 1, 1, 0.4), 'down': (61/255, 147/255, 252/255, 255/255)} [self.state]
    font_size: '16sp'

<Button>
    background_color: {'normal': (1, 1, 1, 0.4), 'down': (61/255, 147/255, 252/255, 255/255)} [self.state]

<MyLayout>
    id: my_widget
    do_default_tab: False
    tab_width: root.width/3 - 1.5
    background_color: 0.1, 0.1, 0.1, 1
    TabbedPanelItem:
        do_default_tab: False
        text: "Files"
        BoxLayout:   
            orientation: "vertical"
            size: root.width, root.height
            padding: 5
            spacing: 0
            FileChooserListView:
                show_hidden: True
                id: filechooser
                path: "''' + file_explr +'''"
                on_selection: my_widget.selected(filechooser.selection)
    
    TabbedPanelItem:
        id: download_tab
        text: "Download"

        GridLayout:
            cols: 1
            rows: 2
            padding: 5
            spacing: 5

            ScrollView:
                size_hint_y: 0.8
                effect_cls: "ScrollEffect"
                scroll_wheel_distance: 60
                bar_width: 10
                do_scroll_x:False
                scroll_type:['bars']
                BoxLayout:
                    orientation: "vertical"
                    size_hint: 1, None
                    padding: 0, 15, 0, 3
                    spacing: 15
                    id: boxlayout
                    size_hint_y: None
                    height: self.minimum_height
            
            FloatLayout:
                size_hint: 0.1, 0.1
                Button:
                    id: DownloadButton
                    size_hint: 0.4, 0.8
                    text: "Start Download"
                    pos_hint: {'center_x':0.5, 'y': 0.1}
                    on_press:
                        root.startDownload()

                
    
    TabbedPanelItem:
        text: "Login Information"
        id: info_tab

        GridLayout:
            cols: 1
            rows: 7
            padding: 75, 25, 75, 0
            spacing: 3
            Label:
                text:'Username'
                size_hint: None, None
                height: 25
            TextInput:
                id: username
                hint_text:'Type your username...'
                on_text: app.process()
                size_hint: 1, None
                height: 35
            Label:
                text:'Password'
                size_hint: None, None
                height: 25
            TextInput:
                id: password
                password: True
                height: 35
                hint_text:'Type your password...'
                size_hint: 1, None
                height: 35
            Label:
                text:'Semester'
                size_hint: None, None
                height: 25
            TextInput:
                id: semester
                height: 35
                hint_text:'Type your semester...'
                size_hint: 1, None
                height: 35
            FloatLayout:
                size_hint: 1, 0.01
                Button:
                    text: "Save Login Information"
                    size_hint: None, None
                    height: 45
                    pos_hint: {'center_x':0.5, 'y': 0.5}
                    width: 400
                    on_press:
                        root.buttonPress()

'''

Builder.load_string(kv)

class textinp(Widget):
    pass

LOGIN = "https://eclass.uth.gr"

def Encrypt(name, password, semester, self):

    if name and password and semester:

        if self.dt.month < 3:
            y_of_enroll = self.dt.year - int(semester) // 2 - 1
        else:
            y_of_enroll = self.dt.year - int(semester) // 2

        os_path = os.path.expanduser('~')

        try:
            os.makedirs(os_path + "/FKey")
            os.makedirs(os_path + "/Encrypted")
        except FileExistsError:
            pass
        
        key = Fernet.generate_key()

        with open(os_path + "/FKey/" +  'filekey.key', 'wb') as filekey:
            filekey.write(key)
            fernet = Fernet(key)

        with open(os_path + "/Encrypted/" + 'encrypted.txt', 'wb') as enc:
            enc.write(fernet.encrypt(name.encode()))
            enc.write("\n".encode())
            enc.write(fernet.encrypt(password.encode()))
            enc.write("\n".encode())
            enc.write(fernet.encrypt(str(y_of_enroll).encode()))
            enc.write("\n".encode())

    else:

        popup("There are missing fields", 260, 180)
        

def popup(message, width, height):

    layout = GridLayout(cols= 1, padding = 0)

    popupLabel = Label(text=message)
    closeButton = Button(text='Close', size_hint=(0.6, None),size=(width * 0.25, height * 0.25),pos_hint= {'center_x':0.5})

    layout.add_widget(popupLabel)
    layout.add_widget(closeButton)

    popupWindow = Popup(title="Attention",content=layout, size_hint=(None, None), size=(width, height), auto_dismiss=False)

    closeButton.bind(on_press = popupWindow.dismiss)

    popupWindow.open()

def Decrypt():
    
    d_list = []
    os_path = os.path.expanduser('~')

    try:
        with open(os_path + "/FKey/" +  "filekey.key", "rb") as key_file:
            key = key_file.read()

        fernet = Fernet(key)

        with open(os_path + "/Encrypted/" +  "encrypted.txt", "rb") as enc_file:
            lines = enc_file.readlines()
            for x in lines:
                d_list.append(fernet.decrypt(x).decode())
    except:
        FileExistsError

    return d_list

class MyLayout(TabbedPanel):

    running = False

    dt = datetime.datetime.now()

    count = 0

    def buttonPress(self):
        Encrypt(self.ids.username.text, self.ids.password.text, self.ids.semester.text, self)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(partial(self.switch, self.ids.download_tab), 0)
    
    def selected(self, filename):
        try:
            if sys.platform == 'linux':
                subprocess.call(["xdg-open", filename[0]])
            else:
                os.startfile(filename[0])
        except:
            pass
    
    def switch(self, tab, *args):
        self.switch_to(tab)


##############################################################################################################################################################################################

    def startDownload(self):

        def download_thread(creds):


            @mainthread
            def skipped(message,dpval,BoldState,UnderState,textColor):
                label = Label(text=message, size_hint_y=None, height=dp(dpval), padding = [0, 0, 0, 4], bold = BoldState, underline = UnderState, color = textColor)
                self.ids.boxlayout.add_widget(label)
                Clock.tick_draw()

            @mainthread
            def status_popup(Status_message, width, height):
                popup(Status_message, width, height)

            @mainthread
            def progbar(response, path, info):
                label = Label(text=info, size_hint_y=None, height=dp(10), padding = [0, 8, 0, 0])
                progress_bar = ProgressBar(max=10, size_hint_y=None, height=dp(10), size_hint_x = 0.9, pos_hint = {'center_x':0.5})
                progress_label = Label(text= '0%', size_hint_y=None, height=dp(10), padding = [0, 0, 0, 8])

                self.ids.boxlayout.add_widget(label)
                self.ids.boxlayout.add_widget(progress_bar)
                self.ids.boxlayout.add_widget(progress_label)

                Clock.tick_draw()

                def download_thread(response, path):

                    start = time.perf_counter()
                    total_size = int(response.headers.get('content-length', 0))
                    block_size = 8192
                    bytes_downloaded = 0
                    
                    with open(path, "wb") as f:
                        for data in response.iter_content(block_size):
                            bytes_downloaded += len(data)
                            f.write(data)
                            progress = int(bytes_downloaded / total_size * 100)
                            progress_bar.value = progress / 10
                            progress_label.text = f'{progress}% ({round(bytes_downloaded/1000000,2)}/{round(total_size/1000000,2)}MB) {round(bytes_downloaded//(time.perf_counter() - start)/1000000, 2)}/MBps'

                    response.close()

                # Clock.schedule_interval(self.ids.filechooser._update_files, t)

                threading.Thread(target=download_thread, args=(response, path)).start()

            os_path = os.path.expanduser('~')
            uni_path = os_path + "/Desktop/University/"

            cookies = {}

            payload = {
                "uname": creds[0],
                "pass": creds[1],
                "submit": ""
            }

            year = int(creds[2])
            y=self.dt.year
            m=self.dt.month

            if m > 8:
                semester = str((y-year)*2 + 1)
            elif m < 3:
                semester = str((y-year)*2 - 1)
            else:
                semester = str((y-year)*2)

            try:
                os.makedirs(uni_path + semester + "ο Εξάμηνο/")
            except FileExistsError:
                pass
            
            table = []
            courses_ID = []
            courses_name = []

            with requests.Session() as s:
            
                s.get(LOGIN)

                cookies_init = s.cookies.get_dict()

                s.post(LOGIN, data=payload)

                for x in s.cookies:
                    cookies[x.name] = x.value

                if cookies_init == cookies:
                    status_popup("Login was unsuccessful, please update your\nauthentication credentials under Login Information.", 400, 200)
                else:

                    self.running = True

                    self.ids.DownloadButton.text = "Cancel Download"

                    web = s.get("https://eclass.uth.gr/main/my_courses.php",
                            cookies=cookies)

                    soup = BeautifulSoup(web.content, 'html.parser')

                    for link in soup.findAll('a', {'class': 'lesson-title-link'}):
                        courses_name.append(link.string.strip())
                        table.append(link)

                    final_names = [x.replace('/', '-') for x in courses_name]

                    directories = [re.search('\"(.*)\"', str(z)).group(1)
                                for z in table]

                    for x in directories:
                        courses_ID.append(x.split('/')[-2])

                def scrape_links(website, course, course_name, init_fold):
                    final_dir = []
                    folders = []
                    dirs = []
                    soup = BeautifulSoup(requests.get(website, cookies=cookies).content, 'html.parser')

                    if (init_fold):
                        download_message = "Folder: " + init_fold[1:] + "  File: "
                        try:
                            os.mkdir(uni_path + semester + "ο Εξάμηνο/" + course_name + init_fold)
                        except FileExistsError:
                            pass
                    else:
                        download_message = "File: "
                        
                    hrefs = soup.findAll('a', {'href': re.compile(
                        r'/modules/document/index\.php\?course='+course+r'&openDir=/[a-zA-Z0-9]')})

                    for text in hrefs:
                        if (text.string and not (re.match('Τύπος', text.string) or re.match('Ημερομηνία', text.string))):
                            folders.append(text.string)

                    dirs = [re.search('\"(.*)\"', str(x)).group(1).replace('amp;', '') for x in hrefs]

                    for y in dirs:
                        if not (re.search(r'&sort', y)):
                            final_dir.append(y)

                    for files in soup.find_all(True, {'class': ['fileURL fileModal', "fileURL"]}):
                        file_name = unquote(str(files.get('href')).rsplit('/', 1)[-1])
                        # Αφαίρεση μη έγκυρων χαρακτήρων από το όνομα του αρχείου
                        no_slash_test_string = str(files.string).replace('/','-')
                        no_slash_file_name = file_name.replace('/', '-')
                        ending = str(files.get('href')).rsplit('.', 1)[-1]
                        final_path = uni_path + semester + "ο Εξάμηνο/" + course_name + init_fold + "/"
                        if(not os.path.exists(final_path + no_slash_test_string + "." + ending) | os.path.exists(final_path + no_slash_file_name)):
                            lec = requests.get(files.get('href'), cookies=cookies, stream=True)
                            if(files.get('href')).rsplit('.', 1)[-1] == files.get('title').rsplit('.', 1)[-1]:
                                path = final_path + no_slash_file_name
                                info = download_message + no_slash_file_name
                            else:
                                path = final_path + no_slash_test_string + "." + ending
                                info = download_message + no_slash_test_string + "." + ending
                            thread = threading.Thread(target=progbar, args=(lec, path, info))
                        else:
                            message = "Skipped: " + files.string
                            thread = threading.Thread(target=skipped, args=(message,5,False,False,[1,1,1,0.65],))
                        
                        if self.Cancel:
                            break
                        
                        thread.start()

                        self.ids.boxlayout.height = self.ids.boxlayout.minimum_height
                    
                    if not self.Cancel:
                        for x, y in zip(final_dir, folders):
                            n_name = init_fold + "/" + y
                            n_url = "https://eclass.uth.gr" + x
                            scrape_links(n_url, course, course_name, n_name)

            try:
                
                for x, y in zip(courses_ID, final_names):
                    try:
                        os.makedirs(uni_path + semester + "ο Εξάμηνο/" + y)
                    except FileExistsError:
                        pass
                    if self.Cancel:
                        break
                    skipped(y,20,True,True,[106/255, 90/255, 205/255, 1])
                    scrape_links("https://eclass.uth.gr/modules/document/index.php?course="+x+"&openDir=/", x, y, "")

                if self.Cancel:
                    status_popup("Download has been cancelled.",225, 150)
                else:
                    status_popup("Download Complete.",225, 150)
                self.running = False
                self.ids.DownloadButton.text = "Download"

            except:
                pass

            print(self.count)

        creds = Decrypt()
        thread = threading.Thread(target=download_thread, args=(creds,))

        if creds:
            if not self.running:
                self.Cancel = False
                thread.start()
            else:
                self.Cancel = True
        else:
            # Αν δεν υπάρχει αρχείο για τα στοιχεία
            popup("Please navigate to the Login Information tab.", 400, 200)


class Application(App):

    def build(self):
        self.title = 'E-Class Organizer'
        self.icon = "ECOIcon.ico"
        return MyLayout()

    def process(self):
        pass

Application().run()