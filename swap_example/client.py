import socket
import argparse
from datetime import datetime
from random import choice
import random
import time

def rand_dna(length):
    random.seed(datetime.now())
    DNA=""
    for count in range(length):
        DNA+=choice("CGTA")
    return DNA

def print_diff(c, x, y, i, j):
    if i >= 0 and j >= 0 and x[i] == y[j]:
        print_diff(c, x, y, i-1, j-1)
        print("  " + x[i])
    elif j >= 0 and (i == 0 or c[i][j-1] >= c[i-1][j]):
        print_diff(c, x, y, i, j-1)
        print("+ " + y[j])
    elif i >= 0 and (j == 0 or c[i][j-1] < c[i-1][j]):
        print_diff(c, x, y, i-1, j)
        print("- " + x[i])
    else:
        print("")

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='TCP client')
    parser.add_argument('--host', type=str, help='tcp server hostname')
    # parser.add_argument('--ip', type=str, help='tcp client ip')
    parser.add_argument('--port', type=int, help='tcp server port number')    
    # parser.add_argument('--s1', type=str, default='AGGTAB', help='sequence1 (max length=999999999)')    
    # parser.add_argument('--s2', type=str, default='GXTXAYB', help='sequence2 (max length=999999999)')    
    parser.add_argument('--s1-len', type=str, help='length of sequence1 (max length=999999999)')    
    parser.add_argument('--s2-len', type=str, help='length of sequence2 (max length=999999999)')    
    args = parser.parse_args()
    
    t1 = time.time()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # sock.bind((args.ip, 0))
    sock.connect((args.host, args.port))
    # seq1 = args.s1
    # seq2 = args.s2

    seq1 = rand_dna(int(args.s1_len))
    seq2 = rand_dna(int(args.s2_len))

    # with open('seq1.txt','w') as fp:
        # fp.write(seq1)

    # with open('seq2.txt','w') as fp:
        # fp.write(seq2)

    print(seq1)
    print(seq2)

    if len(seq1) > 999999999:
        seq1 = seq1[:999999999]
    if len(seq2) > 999999999:
        seq2 = seq2[:999999999]
    
    sock.send(str(len(seq1)).zfill(10).encode())
    sock.send(str(len(seq2)).zfill(10).encode())

    sock.sendall(seq1.encode())
    sock.sendall(seq2.encode())

    m = int(sock.recv(10))    
    lcs = bytearray()
    while len(lcs) < m:
        packet = sock.recv(m - len(lcs))
        if not packet:
            break
        lcs.extend(packet)

    lcs_str = "".join( chr(x) for x in bytearray(lcs) )

    #print('lcs=',lcs_str)

    t2 = time.time()
    print('time: %f s' % (t2 -t1))

    # with open('common.txt','w') as fp:
        # fp.write(lcs_str)

    # c = len(lcs_str)
    # print_diff(c, seq1, seq2, len(seq1)-1, len(seq2)-1)      

    sock.close()
