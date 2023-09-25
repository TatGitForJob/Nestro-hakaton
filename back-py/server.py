from cleanapi import server
import os

url_tail = ''

server.start('http', 8080, '', 'src/handlers', 'src', path_to_log='src/log')