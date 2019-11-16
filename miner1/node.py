import requests
import os
import json
import sys
import apscheduler
from flask import Flask, jsonify, request
import argparse

from block import Block
import mine
import sync
import utils
from config import *
import time
import random

''' SCRIPT FOR RUNNING ON SERVER'''

node = Flask(__name__)

sync.sync(save=True) 

from apscheduler.schedulers.background import BackgroundScheduler
sched = BackgroundScheduler(standalone=True)


''' SHOWING THE BLOCKCHAIN DATA '''
@node.route('/blockchain.json', methods=['GET'])
def blockchain():
  
  local_chain = sync.sync_local() 
  json_blocks = json.dumps(local_chain.block_list_dict())
  return json_blocks


''' CHECKING IF THE BLOCK WHICH IS IN MINING PROCESS IS ALREADY MINED BY OTHER NODE OR NOT !!! '''  

@node.route('/mined', methods=['POST'])
def mined():
  possible_block_dict = request.get_json()
  print possible_block_dict
  print sched.get_jobs()
  print sched

  sched.add_job(mine.validate_possible_block, args=[possible_block_dict], id='validate_possible_block') #add the block again

  return jsonify(received=True)

if __name__ == '__main__':

  #args!
  parser = argparse.ArgumentParser(description='JBC Node')
  parser.add_argument('--port', '-p', default='5000',
                    help='what port we will run the node on')
  parser.add_argument('--mine', '-m', dest='mine', action='store_true')
  args = parser.parse_args()
  line1 = str(random.randint(30,40))
  line2 = str(random.randint(70,100))
  ts = str(time.time())
  filename = '%sdata.txt' % (CHAINDATA_DIR)
  #with open(filename, 'w') as data_file:
  #data_file.write('Block mined by node on port %s' % args.port)
  #data_file.write(' , mod_id , temp : '+line1+' , pulse : '+line2+' , long : 28.63 , lat : 77.37 , 0 , timestamp : '+ts)
  mine.sched = sched 
  if args.mine:    
    sched.add_job(mine.mine_for_block, kwargs={'rounds':STANDARD_ROUNDS, 'start_nonce':0}, id='mining') #add the block again
    sched.add_listener(mine.mine_for_block_listener, apscheduler.events.EVENT_JOB_EXECUTED)#, args=sched)

  sched.start()
  node.run(host='127.0.0.1', port=5000)

