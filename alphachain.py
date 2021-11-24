import hashlib
import math
import sys
import json
from datetime import datetime


class Alphachain:
    def __init__(self):
        self.chain = []
                    
    # random self-made equation
    def proof_puzzle(self, new_proof, prev_proof):
        res = (((new_proof / (new_proof / 3)) - math.sqrt(prev_proof))**2 - (new_proof)**2)
        return res        
    
    # consensus protocol
    def proof_of_work(self, prev_proof):
        new_proof = 1
        is_proof_found = False
        
        while is_proof_found is False:
            hash_res = hashlib.sha256(str(self.proof_puzzle(new_proof, prev_proof)).encode()).hexdigest()
            print(hash_res)
            if(hash_res[:self.get_mining_diff()] != ('0' * self.get_mining_diff())):
                new_proof += 1
            else:
                is_proof_found = True
        return new_proof

       
    def create_block(self, parent_hash, proof, prev_proof):    
        block_height = len(self.chain)
        timestamp = datetime.today()
        miner = 'unknown'
        block_hash = hashlib.sha256(str(self.proof_puzzle(proof, prev_proof)).encode()).hexdigest()
        block_size = (sys.getsizeof(block_height) + sys.getsizeof(timestamp) + sys.getsizeof(miner) + sys.getsizeof(parent_hash) + sys.getsizeof(proof) + sys.getsizeof(block_hash)) / 1000000
        block = {'block_height': block_height,
                 'timestamp': str(timestamp),
                 'block_size': block_size,
                 'parent_hash': str(parent_hash),
                 'proof': proof,
                 'miner': miner,
                 'block_hash': block_hash}     
        self.chain.append(block)
        return block
  
    def mine_block(self, parent_hash, prev_proof):
        proof = self.proof_of_work(prev_proof)
        block = self.create_block(parent_hash, proof, prev_proof)
        return block
              
    # Will run after every new block is mined and added to the blockchain    
    # Conditions for the blockchain to be considered valid: 
    # 1. all blocks' hashes are correct
    # 2. all blocks' parent hashes = previous blocks' hashes
    # 3. all blocks' size <= 10 MB
    def is_chain_valid(self):
        BLOCK_SIZE_LIMIT = 10
        prev_proof = 0
        parent_hash = self.chain[0]['parent_hash']
        for block in self.chain:
            block_hash = str(hashlib.sha256(str(self.proof_puzzle(block['proof'], prev_proof)).encode()).hexdigest())
            if block_hash[:self.get_mining_diff()] != ('0' * self.get_mining_diff()):
                print('Alphachain has invalid hash on block height ' + str(block['block_height']))
                return False
            if block['parent_hash'] != parent_hash:
                print('Alphachain has invalid chain link on block height ' + str(block['block_height']) + ' and ' + str(block['block_height'] - 1))
                return False
            if block['block_size'] > 10:
                print('Alphachain has block exceded block size limit of ' + BLOCK_SIZE_LIMIT + ' MB on block height ' + block['block_height'])
                return False
            parent_hash = block['block_hash']
            prev_proof = block['proof']
        print('Alphachain is valid\n')
        return True
    
    # higher number = higher difficulty
    def set_mining_diff(self, mining_diff = 4):
        self.mining_diff = mining_diff
    
    def get_mining_diff(self):
        return self.mining_diff
    
    def get_last_block(self):
        return self.chain[-1]
    
    # for data exchange
    def chain_jsonify(self):
        return json.dumps(self.chain, indent = 2)







def mine(mine_count = 1):
    alphachain = Alphachain()   
    # set difficulty number
    alphachain.set_mining_diff(2)
    gen_block = alphachain.mine_block('0000000000000000000000000000000000000000000000000000000000000000', 0)
    print(gen_block)

    for i in range(0, mine_count - 1):
        mined_block = alphachain.mine_block(alphachain.get_last_block()['block_hash'], alphachain.get_last_block()['proof'])
        print(str(mined_block) + '\n')
        alphachain.is_chain_valid()       
    
    print(alphachain.chain_jsonify())

mine(5)
input()

    