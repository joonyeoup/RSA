from BitVector import BitVector
from PrimeGenerator import PrimeGenerator
import sys
import math

class RSA():
    def __init__(self, e) -> None:
        self.e = e 
        self.n = None 
        self.d = None 
        self.p = None 
        self.q = None
    # You are free to have other RSA class methods you deem necessary for your solution
        
    def keygen (self, output1, output2) -> None:
        pee = PrimeGenerator(bits = 128)
        qew = PrimeGenerator(bits = 128)

        p = pee.findPrime()
        q = qew.findPrime()
        e = self.e

        pbv = BitVector(intVal = p, size = 128)
        qbv = BitVector(intVal = q, size = 128)

        # print (pbv)   
        # print (qbv)   
        P = pbv.int_val()
        Q = qbv.int_val()
        tot = (P - 1) * (Q - 1)
        # print (P)
        # print (Q)
        # print (math.gcd (e, P) == 1)
        # print (math.gcd (e, Q) == 1)

        if math.gcd (e, tot) != 1:
            self.keygen (output1, output2)
    
        with open (output1, 'w') as file:
            file.write(str(P))
        with open (output2, 'w') as file:
            file.write(str(Q))
        
    def encrypt(self, plaintext:str, ciphertext:str) -> None: 
        # your implemenation goes here
        with open ('p.txt', 'r') as file: 
            p = int(file.read())
        with open ('q.txt', 'r') as file:
            q = int(file.read()) 

        n = p * q
        e = self.e

        bv = BitVector(filename = plaintext)

        while bv.more_to_read:
            block = bv.read_bits_from_file(128)
            block.pad_from_left(128)

            if block.length() < 256:
                block.pad_from_right(256 - block.length())   

            # print (block)
            M = block.int_val()
            C = pow (M, e, n)
            # print (BitVector(intVal = C))
            # print ('C', C.bit_length())

            result = BitVector(intVal = C, size = 256)
            final = result.get_bitvector_in_hex()
                        
            with open (ciphertext, 'a') as file:
                file.write(final)
                
        # file.close()            
        return None

    def decrypt(self, ciphertext:str, recovered_plaintext:str) -> None:
        with open ('p.txt', 'r') as file: 
            p = int(file.read())
        with open ('q.txt', 'r') as file:
            q = int(file.read()) 

        n = p * q
        e = self.e
        tot = (p - 1) * (q - 1)
        ebv = BitVector(intVal = e)
        d = ebv.multiplicative_inverse(BitVector(intVal = tot))
        D = d.int_val()

        hex_string = open(ciphertext, 'r').read()
        binary_string = bytes.fromhex(hex_string) # convert to binary

        with open ('new_cipher.txt', 'wb') as file:
            file.write(binary_string) # store the binary file into a new file to create a correct Bitvector

        # print (((e * d.int_val()) % tot) == 1)
        bv = BitVector(filename = 'new_cipher.txt')

        while bv.more_to_read:
            block = bv.read_bits_from_file(256)

            if block.length() < 256:
                block.pad_from_right(256 - block.length())

            C = block.int_val()
            Vp = pow(C, D, p)
            Vq = pow(C, D, q)

            qbv = BitVector(intVal = q)
            pbv = BitVector(intVal = p)

            invp = qbv.multiplicative_inverse(pbv)
            invq = pbv.multiplicative_inverse(qbv)

            # print (invp.int_val() * q % p == 1)
            Xp = invp.int_val() * q
            Xq = invq.int_val() * p
            M = (Vp * Xp + Vq * Xq) % n
            # print (M)
            # print (M == pow(C, D, n))
            # print (M.bit_length()) 
            result = BitVector(intVal = M, size = 256)
            # print (result.length ())
            final = result[128:] 
        
            with open (recovered_plaintext, 'a') as file:
                file.write(final.get_bitvector_in_ascii())
        
        # file.close()
        return None
    
if __name__ == "__main__": 
    cipher = RSA(e=65537) 

    if sys.argv[1] == "-e":
        cipher.encrypt(plaintext=sys.argv[2], ciphertext=sys. argv[5])

    elif sys.argv[1] == "-g":
        cipher.keygen(output1 = sys.argv[2], output2 = sys.argv[3])

    elif sys.argv[1] == "-d": 
        cipher.decrypt(ciphertext=sys.argv[2],recovered_plaintext=sys.argv[5] )