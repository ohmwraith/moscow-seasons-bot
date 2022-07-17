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

    # Возвращает конфиг для создания класса почты
    def get_mail_config(self):
        print(self.config[
            'trusted_email_senders']
)
        return self.config['mail_username'], self.config['mail_password'], self.config['imap_host'], self.config[
            'trusted_email_senders']

    # Возвращает конфиг для создания класса робота-браузера
    def get_robot_config(self):
        return self.config['webdriver_path']

    # Загружает конфиг из файла config.ini
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

    # Загружает профили из файла profiles.json
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

    # Сохраняет всех пользователей, перезаписывая файл профилей
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
            name = input('ФИО: ')
            birth = input('Дата рождения в формате DD.MM.YYYY: ')
            phone = input('Номер телефона (+7XXXXXXXXXX): ')
            email = self.email
            if input('Вы уверены?(Y/N): ').lower() == 'y':
                confirm = True
        self.persons.append(Person(len(self.persons) + 1, name, birth, phone, email))
        print('Profile ID: {:2.0f} | Пользователь {} успешно добавлен.'.format(len(self.persons), name))

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

    # Загружает список катков из файла TruckList.txt
    @staticmethod
    def get_truck_list(self):
        with open("TruckList.txt", 'r') as trucks:
            file_content = trucks.readlines()
            truck_list = []
            for line in file_content:
                line = line.replace('\n', '')
                truck_list.append(line.split('; ', 1))
            return truck_list

    # Метод ожидания почты, применяется после отправки формы, чтобы вовремя обработать письмо
    @staticmethod

    # Проверяет, безопасна ли ссылка, применяется для входящих писем в почте
    def is_link_safe(self, link):
        if (link.find(self.path) == 0):
            return True
        return False

    # Метод режима, выводит на экран катки с их ID
    def render_truck_list(self):
        print("[СЕЗОНЫ] Список доступных катков:")
        for truck_id in range(0, len(self.trucks_list)):
            print('ID: {:2.0f} | Каток на {:100} Ссылка: {}'.format(truck_id, self.trucks_list[truck_id][0],
                                                                    self.path + self.trucks_list[truck_id][1]))

    # Метод процесса регистрации, при вызове проходит полная регистрация на сеанс
    def register_for_session(self, registration_link, person_id, persons_count):
        name, birth, phone, email = self.get_person_info(person_id)
        robot.send_form(registration_link, name, birth, phone, email, persons_count)
        print("[МЕНЕДЖЕР] Ожидание приглашения... ", end="")
        mail.get_imap_login()
        while mail.waiting_mail():
            print("Ожидание письма...\b", end="")
        print("Приглашение получено.")
        confirmation_link = None
        while confirmation_link == None:
            confirmation_status, confirmation_link = mail.parse_messages(1)
        robot.go_to_link(confirmation_link)
        print("[МЕНЕДЖЕР] Регистрация подтверждена.")
        mail.close_imap()

    # Возвращает все сессии с катка
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

    # Возвращает все сессии с свободными местами
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
        print("ID: {:2.0f} | {}, сеансы на сегодня: ".format(truck_id ,self.trucks_list[truck_id][0]))
        for session in sessions:
            print(f"Сеанс {session[0]}", end=' ')
            if session[2] is None:
                print("Мест нет")
            else:
                print("Места доступны")




    # Возвращает все сессии со всех катков
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

    # Отображает текущее состояние катков
    def render_truck_status(self):
        get_status_start_time = time.time()
        truck_list = self.trucks_list
        trucks_status = self.get_trucks_status()
        get_status_end_time = time.time()
        for truck_id in range(0, len(trucks_status)):
            flag = False
            for session in trucks_status[truck_id]:
                if session[2] is not None and session[1] != "Мест нет":
                    if not flag:
                        print(f"[ПОИСК] Обнаружены места на {truck_list[truck_id][0]} на сеанс в {session[0]}", end="")
                        flag = True
                    else:
                        print(", " + session[0], end="")

            if flag:
                print(f". Страница катка: https://mftickets.technolab.com.ru/mc/{truck_list[truck_id][1]}")
        print("[ПОИСК] Проверка статуса заняла {:0.2f}c. Обновление...".format(
            get_status_end_time - get_status_start_time))

    # Проверяет, существует ли сессия в указанное время
    def check_session(self, truck_id, session_time):
        for session in self.get_sessions(truck_id):
            if session[0] == session_time:
                return True
        return False

    # Метод режима, отслеживает конкретную сессию на заданном катке и, как только появляется место, сразу регистрирует
    def session_tracking(self, truck_id, session_time, person_id, persons_count):
        while True:
            for session in self.get_available_sessions(truck_id):
                if session[0] == session_time:
                    winsound.Beep(440, 250)  # frequency, duration
                    register_start_time = time.time()
                    self.register_for_session(session[2], person_id, persons_count)
                    print(
                        "[ОТЧЕТ] Обнаружил сеанс за {:0.2f}с. Зарегистрировал тебя за {:0.2f}c.\n Продолжить работу?(Y/N): ".format(
                            (time.time() - start_time) - (time.time() - register_start_time),
                            time.time() - register_start_time))
                    if input().lower() == "y":
                        continue
                    else:
                        sys.exit()