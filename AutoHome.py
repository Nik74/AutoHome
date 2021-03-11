# This program was created for Vasily and his work in the service

import AppWindow
import Logs
import SQLite

Logs.logger.debug("Program is started")

AppWindow.AppWindow()

SQLite.conn.close()
