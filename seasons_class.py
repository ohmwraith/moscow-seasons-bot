class Seasons(object):
    def __init__(self):
        self.trucks_list = self.get_truck_list(self)
        self.path = "https://mftickets.technolab.com.ru/mc/"
        self.config = self.load_config()
        self.email = self.config['mail_username']
        self.persons = []
        try:
            self.persons = self.load_profiles()
        except:
            print(1)

    # ���������� ������ ��� �������� ������ �����
    def get_mail_config(self):
        print(self.config[
            'trusted_email_senders']
)
        return self.config['mail_username'], self.config['mail_password'], self.config['imap_host'], self.config[
            'trusted_email_senders']

    # ���������� ������ ��� �������� ������ ������-��������
    def get_robot_config(self):
        return self.config['webdriver_path']

    # ��������� ������ �� ����� config.ini
    def load_config(self):
        config = {}
        with open('config.ini', 'r') as config_file:
            for line in config_file.readlines():
                if line.find(';') != -1:
                    config[line.split('=', 1)[0].replace(' ', '')] = line.split('=', 1)[1].replace(' ', '').replace(
                        '\n', '').replace('\'', '').replace('\"', '').split(';')
                else:
                    config[line.split('=', 1)[0].replace(' ', '')] = line.split('=', 1)[1].replace(' ', '').replace(
                        '\n', '').replace('\'', '').replace('\"', '')
        return config

    # ��������� ������� �� ����� profiles.json
    def load_profiles(self):
        persons = []
        with io.open('profiles.json', 'r', encoding='utf-8') as file:
            profiles = json.load(file)
            print(profiles)
            id = 1
            for person in profiles:
                persons.append(Person(person[0], person[1], person[2], person[3], person[4]))
                id += 1
            return persons

    # ��������� ���� �������������, ������������� ���� ��������
    def save_all_profiles(self):
        persons_array = []
        for person in self.persons:
            persons_array.append([person.id, person.name, person.birth, person.phone, person.email])

        with io.open('profiles.json', 'w', encoding='utf-8') as f:
            f.write(json.dumps(persons_array, ensure_ascii=False))
            #f.write(json.dumps(seasons.persons, ensure_ascii=False))
            #f.write('\n')

    def add_person(self):
        confirm = False
        while not confirm:
            name = input('���: ')
            birth = input('���� �������� � ������� DD.MM.YYYY: ')
            phone = input('����� �������� (+7XXXXXXXXXX): ')
            email = self.email
            if input('�� �������?(Y/N): ').lower() == 'y':
                confirm = True
        self.persons.append(Person(len(self.persons) + 1, name, birth, phone, email))
        print('Profile ID: {:2.0f} | ������������ {} ������� ��������.'.format(len(self.persons), name))

    def remove_person_by_id(self, person_id):
        for i, person in enumerate(self.persons):
            if person.id == person_id:
                del self.persons[i]
    def render_persons(self):
        if self.persons is not None:
            for person in self.persons:
                print('ID {:2.0f} | {}, {}, {}, {}'.format(person.id, person.name, person.birth, person.phone, person.email))

    def get_person_info(self, person_id):
        for person in self.persons:
            if person.id == person_id:
                return person.name, person.birth, person.phone, person.email

    # ��������� ������ ������ �� ����� TruckList.txt
    @staticmethod
    def get_truck_list(self):
        with open("TruckList.txt", 'r') as trucks:
            file_content = trucks.readlines()
            truck_list = []
            for line in file_content:
                line = line.replace('\n', '')
                truck_list.append(line.split('; ', 1))
            return truck_list

    # ����� �������� �����, ����������� ����� �������� �����, ����� ������� ���������� ������
    @staticmethod

    # ���������, ��������� �� ������, ����������� ��� �������� ����� � �����
    def is_link_safe(self, link):
        if (link.find(self.path) == 0):
            return True
        return False

    # ����� ������, ������� �� ����� ����� � �� ID
    def render_truck_list(self):
        print("[������] ������ ��������� ������:")
        for truck_id in range(0, len(self.trucks_list)):
            print('ID: {:2.0f} | ����� �� {:100} ������: {}'.format(truck_id, self.trucks_list[truck_id][0],
                                                                    self.path + self.trucks_list[truck_id][1]))

    # ����� �������� �����������, ��� ������ �������� ������ ����������� �� �����
    def register_for_session(self, registration_link, person_id, persons_count):
        name, birth, phone, email = self.get_person_info(person_id)
        robot.send_form(registration_link, name, birth, phone, email, persons_count)
        print("[��������] �������� �����������... ", end="")
        mail.get_imap_login()
        while mail.waiting_mail():
            print("�������� ������...\b", end="")
        print("����������� ��������.")
        confirmation_link = None
        while confirmation_link == None:
            confirmation_status, confirmation_link = mail.parse_messages(1)
        robot.go_to_link(confirmation_link)
        print("[��������] ����������� ������������.")
        mail.close_imap()

    # ���������� ��� ������ � �����
    def get_sessions(self, truck_id):
        req = urllib.request.Request(
            "https://mftickets.technolab.com.ru/mc/" + self.trucks_list[truck_id][1],
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
            }
        )
        with urllib.request.urlopen(req) as response:
            response_text = response.read().decode('utf-8')
            soup = BeautifulSoup(response_text, 'html.parser')
            result = []
            for link in soup.find_all('a'):
                result.append([link.get_text(), link.get('title'), link.get('href')])
        return result

    # ���������� ��� ������ � ���������� �������
    def get_available_sessions(self, truck_id):
        req = urllib.request.Request(
            "https://mftickets.technolab.com.ru/mc/" + self.trucks_list[truck_id][1],
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
            }
        )
        with urllib.request.urlopen(req) as response:
            response_text = response.read().decode('utf-8')
            soup = BeautifulSoup(response_text, 'html.parser')
            result = []
            for link in soup.find_all('a'):
                if link.get('href') is not None:
                    result.append([link.get_text(), link.get('title'), link.get('href')])
        return result

    def render_sessions(self, truck_id, sessions):
        print("ID: {:2.0f} | {}, ������ �� �������: ".format(truck_id ,self.trucks_list[truck_id][0]))
        for session in sessions:
            print(f"����� {session[0]}", end=' ')
            if session[2] is None:
                print("���� ���")
            else:
                print("����� ��������")




    # ���������� ��� ������ �� ���� ������
    def get_trucks_status(self):
        truck_status_list = []
        for truck in self.trucks_list:
            req = urllib.request.Request(
                "https://mftickets.technolab.com.ru/mc/" + truck[1],
                data=None,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
                }
            )
            with urllib.request.urlopen(req) as response:
                response_text = response.read().decode('utf-8')
                soup = BeautifulSoup(response_text, 'html.parser')
                result = []
                for link in soup.find_all('a'):
                    result.append([link.get_text(), link.get('title'), link.get('href')])
            truck_status_list.append(result)
        return truck_status_list

    @staticmethod
    def clear_console():
        os.system('cls')

    @staticmethod
    def pause_console():
        os.system('pause')

    # ���������� ������� ��������� ������
    def render_truck_status(self):
        get_status_start_time = time.time()
        truck_list = self.trucks_list
        trucks_status = self.get_trucks_status()
        get_status_end_time = time.time()
        for truck_id in range(0, len(trucks_status)):
            flag = False
            for session in trucks_status[truck_id]:
                if session[2] is not None and session[1] != "���� ���":
                    if not flag:
                        print(f"[�����] ���������� ����� �� {truck_list[truck_id][0]} �� ����� � {session[0]}", end="")
                        flag = True
                    else:
                        print(", " + session[0], end="")

            if flag:
                print(f". �������� �����: https://mftickets.technolab.com.ru/mc/{truck_list[truck_id][1]}")
        print("[�����] �������� ������� ������ {:0.2f}c. ����������...".format(
            get_status_end_time - get_status_start_time))

    # ���������, ���������� �� ������ � ��������� �����
    def check_session(self, truck_id, session_time):
        for session in self.get_sessions(truck_id):
            if session[0] == session_time:
                return True
        return False

    # ����� ������, ����������� ���������� ������ �� �������� ����� �, ��� ������ ���������� �����, ����� ������������
    def session_tracking(self, truck_id, session_time, person_id, persons_count):
        while True:
            for session in self.get_available_sessions(truck_id):
                if session[0] == session_time:
                    winsound.Beep(440, 250)  # frequency, duration
                    register_start_time = time.time()
                    self.register_for_session(session[2], person_id, persons_count)
                    print(
                        "[�����] ��������� ����� �� {:0.2f}�. ��������������� ���� �� {:0.2f}c.\n ���������� ������?(Y/N): ".format(
                            (time.time() - start_time) - (time.time() - register_start_time),
                            time.time() - register_start_time))
                    if input().lower() == "y":
                        continue
                    else:
                        sys.exit()