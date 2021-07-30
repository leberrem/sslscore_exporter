# -*- encoding: utf-8 -*-
#
# pip install sslscore
# pip install prometheus_client
#

from prometheus_client import start_http_server
from prometheus_client import Gauge
from prometheus_client import REGISTRY, PROCESS_COLLECTOR, PLATFORM_COLLECTOR

import os
import time
import sys
import json
import ssllabs
import httpobscli

def gradeToScore(grade):
  score=0
  if grade[:1] == "A":
      score = 80
  elif grade[:1] == "B":
      score = 65
  elif grade[:1] == "C":
      score = 50
  elif grade[:1] == "D":
      score = 35
  elif grade[:1] == "E":
      score = 20
  elif grade[:1] == "F":
      score = 5

  if grade[1:2] == "+":
    score=score+10

  return score

# -------------------------------------------------------
# Get HTTP Observatory Grade
# -------------------------------------------------------
def getHttpObs():
  sys.stdout.write("Searching HTTP Observatory Grade...\n")

  try:

    httpobscli_return = httpobscli.call(host)

    #sys.stdout.write(json.dumps(httpobscli_return, indent=4, sort_keys=True))

    grade=str(httpobscli_return["grade"])
    score=httpobscli_return["score"]

    sys.stdout.write(host+" => "+grade+"\n")
    GaugeHttpObs.labels(host, grade).set(score)

  except Exception as e:
    sys.stderr.write('error:'+str(e))


# -------------------------------------------------------
# Get SSL Labs Grade
# -------------------------------------------------------
def getSslLabs():
  sys.stdout.write("Searching SSLLabs Grade...\n")

  try:

    ssllabs_return = ssllabs.call(host)
    #sys.stdout.write(json.dumps(ssllabs_return, indent=4, sort_keys=True))
    grade=str(ssllabs_return["endpoints"][0]["grade"])
    score=gradeToScore(grade)

    sys.stdout.write(host+" - "+str(ssllabs_return["endpoints"][0]["ipAddress"])+" => "+str(ssllabs_return["endpoints"][0]["grade"])+"\n")
    GaugeSslLabs.labels(host, grade).set(score)

  except Exception as e:
    sys.stderr.write('error:'+str(e))

# -------------------------------------------------------
# MAIN
# -------------------------------------------------------
def main():

  # Start up the server to expose the metrics.
  start_http_server(port)

  # Generate some requests.
  while True:
      getSslLabs()
      getHttpObs()
      time.sleep(interval)

# -------------------------------------------------------
# RUN
# -------------------------------------------------------

# http port - default 9299
port = int(os.getenv('PORT', 9299))

# Refresh interval between collects in seconds - default 1800 (30 minutes)
interval = int(os.getenv('INTERVAL', 1800))

host = os.getenv('HOST', None)

if not host:
  sys.stderr.write("host key is required please set HOST environment variable.\n")
  exit(1)

# Show init parameters
sys.stdout.write('----------------------\n')
sys.stdout.write('Init parameters\n')
sys.stdout.write('port : ' + str(port) + '\n')
sys.stdout.write('interval : ' + str(interval) + 's\n')
sys.stdout.write('----------------------\n')


# Disable default python metrics
REGISTRY.unregister(PROCESS_COLLECTOR)
REGISTRY.unregister(PLATFORM_COLLECTOR)

# Create gauge
GaugeSslLabs = Gauge('ssllabs_Score', 'Get SSL Labs Score for a host', ['host','grade'])
GaugeHttpObs = Gauge('httpobs_Score', 'Get HTTP Observatory Score for a host', ['host','grade'])

if __name__ == '__main__':
  main()
