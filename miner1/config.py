'''CONFIGURING PORTS, NUMBER OF ZEROES FOR CALCULATING NONCE,
STANDARD ROUNDS FOR APS SCHEDULING FOR MINING AND BLOCKS DATA TYPES FOR CONSTRUCTOR'''

CHAINDATA_DIR = 'chaindata/'
NUM_ZEROS = 6

PEERS = [
    'http://localhost:5000/',
    'http://localhost:5001/',
    'http://localhost:5002/',
    'http://localhost:5003/',
    ]

BLOCK_VAR = {'index': int, 'nonce': int, 'hash': str, 'prev_hash': str, 'timestamp': int}

STANDARD_ROUNDS = 100000

