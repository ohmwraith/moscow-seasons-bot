# -*- coding: utf-8 -*-
import time
from req import Service
from req import Seasons
from req import Robot
from req import Mail


if __name__ == "__main__":
    start_time = time.time()
    service = Service()
    seasons, mail, robot = service.initialize_components()
