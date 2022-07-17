# -*- coding: utf-8 -*-
import time
from req import Seasons
from req import Robot
from req import Mail





if __name__ == "__main__":
    start_time = time.time()

    seasons = Seasons()
    username, password, host, emails = seasons.get_mail_config()
    mail = Mail(username, password, host, emails)
    webdriver_path = seasons.get_robot_config()
    robot = Robot(webdriver_path)

    # seasons.session_tracking(11, "11:00")
    # seasons.render_truck_list()
    run = True
while run:
    mode = None
    while mode == None:
        mode = int(input("MS BYPASS VER 1.0\n"
              "1. Статус катков\n"
              "2. Список катков\n"
              "3. Подписаться на сеанс\n"
              "4. Список пользователей\n"
                         "Режим: "))
        seasons.clear_console()
    if mode == 1:
        seasons.render_truck_status()
        continue
    if mode == 2:
        seasons.render_truck_list()
        continue
    if mode == 3:
        print("ID катка: ", end="")
        truck_id = int(input())
        print("ID пользователя: ", end="")
        person_id = int(input())
        print(seasons.get_sessions(truck_id))
        sessions = seasons.get_sessions(truck_id)
        seasons.render_sessions(truck_id, sessions)
        print("Какое время отслеживать?: ", end="")
        session_time = input()
        print("Сколько человек пойдет кататься?: ", end="")
        persons_count = int(input())
        seasons.session_tracking(truck_id, session_time, person_id, persons_count)
        continue
    if mode == 4:
        seasons.render_persons()
        persons_mode = None
        while persons_mode == None:
            print("1. Добавить\n"
                  "2. Удалить")
            persons_mode = int(input("Режим: "))
        if persons_mode == 1:
            seasons.add_person()
            seasons.save_all_profiles()
            seasons.clear_console()
            print("Пользователь успешно добавлен.")
            seasons.render_persons()
            seasons.pause_console()
            continue
        if persons_mode == 2:
            person_id = int(input('ID пользователя: '))
            seasons.remove_person_by_id(person_id)
            seasons.save_all_profiles()
            seasons.clear_console()
            print("Пользователь удален.")
            seasons.render_persons()
            seasons.pause_console()

    else:
        continue