from BitVector import BitVector
import sys
import math
from PrimeGenerator import PrimeGenerator # code provided by Professor Avikak
from solve_pRoot import solve_pRoot # code provided by Professor Avikak

class RSA():
    def __init__(self, e) -> None:
        self.e = e 
        self.n = None 
        self.d = None 
        self.p = None 
        self.q = None
    
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
    
    def encrypt(self, plaintext:str, ciphertext1:str, ciphertext2:str, ciphertext3:str, modulus:str) -> None: 
        # your implemenation goes here
        self.keygen(output1 = 'P1.txt', output2 = 'Q1.txt')
        self.keygen(output1 = 'P2.txt', output2 = 'Q2.txt')
        self.keygen(output1 = 'P3.txt', output2 = 'Q3.txt')

        with open ('P1.txt', 'r') as file: 
            p1 = int(file.read())
        with open ('Q1.txt', 'r') as file:
            q1 = int(file.read()) 

        with open ('P2.txt', 'r') as file:
            p2 = int(file.read())
        with open ('Q2.txt', 'r') as file:
            q2 = int(file.read())

        with open ('P3.txt', 'r') as file:
            p3 = int(file.read())
        with open ('Q3.txt', 'r') as file:
            q3 = int(file.read())

        n1 = p1 * q1
        n2 = p2 * q2
        n3 = p3 * q3

        e = self.e

        with open (modulus, 'a') as file:
                file.write('n1: ' + str(n1) + '\n' + 'n2: ' + str(n2) + '\n' + 'n3: ' + str(n3))

        bv = BitVector(filename = plaintext)

        while bv.more_to_read:

            block = bv.read_bits_from_file(128)     
            if block.length() < 128:
                block.pad_from_right(128 - block.length())   

            block.pad_from_left(128)

            M = block.int_val()
            C1 = pow(M, e, n1)
            C2 = pow(M, e, n2)
            C3 = pow(M, e, n3)

            result1 = BitVector(intVal = C1, size = 256)
            final1 = result1.get_bitvector_in_hex()

            result2 = BitVector(intVal = C2, size = 256)
            final2 = result2.get_bitvector_in_hex()

            result3 = BitVector(intVal = C3, size = 256)
            final3 = result3.get_bitvector_in_hex()
                        
            with open (ciphertext1, 'a') as file:
                file.write(final1)
            with open (ciphertext2, 'a') as file:
                file.write(final2)
            with open (ciphertext3, 'a') as file:
                file.write(final3)

            
        # file.close()    
        return None

    def crack (self, ciphertext1: str, ciphertext2: str, ciphertext3: str, modulus: str, cracked: str) -> None:
        
        with open (modulus, 'r') as file:
            n1 = int(file.readline().split()[1])
            n2 = int(file.readline().split()[1])
            n3 = int(file.readline().split()[1])
        
        # print (n1)
        # print (n2)
        # print (n3)
        N = n1 * n2 * n3

        hex1 = open(ciphertext1, 'r').read()
        hex2 = open(ciphertext2, 'r').read()
        hex3 = open(ciphertext3, 'r').read()

        binary1 = bytes.fromhex(hex1)
        binary2 = bytes.fromhex(hex2)
        binary3 = bytes.fromhex(hex3)

        with open ('new_cipher1.txt', 'wb') as file:
            file.write(binary1)

        with open ('new_cipher2.txt', 'wb') as file:
            file.write(binary2)

        with open ('new_cipher3.txt', 'wb') as file:
            file.write(binary3)

        bv1 = BitVector(filename = 'new_cipher1.txt')
        bv2 = BitVector(filename = 'new_cipher2.txt')
        bv3 = BitVector(filename = 'new_cipher3.txt')

        while bv1.more_to_read and bv2.more_to_read and bv3.more_to_read:

            C1 = bv1.read_bits_from_file(256)
            C2 = bv2.read_bits_from_file(256)
            C3 = bv3.read_bits_from_file(256)

            if C1.length() < 256:
                C1.pad_from_right(256 - C1.length())

            if C2.length() < 256:
                C2.pad_from_right(256 - C2.length())
                
            if C3.length() < 256:
                C3.pad_from_right(256 - C3.length())

            c1 = C1.int_val()
            c2 = C2.int_val()
            c3 = C3.int_val()

            M1 = n2 * n3
            # print (M1)
            M2 = n1 * n3
            # print (M2)
            M3 = n1 * n2
            # print (M3)

            BV1 = BitVector(intVal = M1)
            BV2 = BitVector(intVal = M2)
            BV3 = BitVector(intVal = M3)

            Bv1 = BitVector(intVal = n1)
            Bv2 = BitVector(intVal = n2)
            Bv3 = BitVector(intVal = n3)

            invM1 = BV1.multiplicative_inverse(Bv1)
            invM2 = BV2.multiplicative_inverse(Bv2)
            invM3 = BV3.multiplicative_inverse(Bv3)

            # print (invM1.int_val())
            # print (invM2.int_val())
            # print (invM3.int_val())

            X = (c1 * M1 * invM1.int_val() + c2 * M2 * invM2.int_val() + c3 * M3 * invM3.int_val()) % N
            result = solve_pRoot (3, X)

            final = BitVector(intVal = result, size = 256)
            printed_final = final[128:]

            with open (cracked, 'a') as file:
                file.write(printed_final.get_bitvector_in_ascii())

        return None

if __name__ == "__main__": 
    cipher = RSA(e = 3)

    if sys.argv[1] == "-e":
        cipher.encrypt(plaintext=sys.argv[2], ciphertext1=sys. argv[3], ciphertext2=sys.argv[4], ciphertext3=sys.argv[5], modulus = sys.argv[6])
    elif sys.argv[1] == "-g":
        cipher.keygen(output1 = sys.argv[2], output2 = sys.argv[3])
    elif sys.argv[1] == "-c":
        cipher.crack(ciphertext1=sys.argv[2], ciphertext2=sys.argv[3], ciphertext3=sys.argv[4], modulus=sys.argv[5], cracked = sys.argv[6])