import os
from config import *
import utils
import sync
import argparse
import time
import random

def mine_first_block():
  first_block = utils.create_new_block_from_prev(prev_block=None, data='First block.')
  first_block.update_self_hash()
  while str(first_block.hash[0:NUM_ZEROS]) != '0' * NUM_ZEROS:
    first_block.nonce += 1
    first_block.update_self_hash()
  assert first_block.is_valid()
  return first_block

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description='Generating Blockchain')
  parser.add_argument('--first', '-f', dest='first', default=False, action='store_true', help='generate the first node ourselves')
  parser.add_argument('--port', '-p', default='5000',
                    help='what port we will run the node on')
  args = parser.parse_args()

  if not os.path.exists(CHAINDATA_DIR):
    os.mkdir(CHAINDATA_DIR)

  if args.first:
    if os.listdir(CHAINDATA_DIR) == []:      
      first_block = mine_first_block()
      first_block.self_save()
      filename = "%s/data.txt" % CHAINDATA_DIR
      line1 = str(random.randint(30,40))
      line2 = str(random.randint(70,100))
      ts = str(time.time())
      with open(filename, 'w') as data_file:
        data_file.write('Block mined by node on port %s' % args.port)
        data_file.write('mod_id , temp : '+line1+' , pulse : '+line2+' , long : 28.63 , lat : 77.37 , 0 , timestamp : '+ts)
    else:
      print "Chaindata directory already has files. If you want to generate a first block, delete files and rerun"
  else:
    sync.sync(save=True)

