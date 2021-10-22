import multiprocessing
import socket
import argparse
import os

def lcs(X, Y, m, n):
    L = [[0 for x in range(n+1)] for x in range(m+1)]
  
    # Following steps build L[m+1][n+1] in bottom up fashion. Note
    # that L[i][j] contains length of LCS of X[0..i-1] and Y[0..j-1] 
    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif X[i-1] == Y[j-1]:
                L[i][j] = L[i-1][j-1] + 1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])
  
    # Following code is used to print LCS
    index = L[m][n]
  
    # Create a character array to store the lcs string
    lcs = [''] * (index+1)
    lcs[index] = ''
  
    # Start from the right-most-bottom-most corner and
    # one by one store characters in lcs[]
    i = m
    j = n
    while i > 0 and j > 0:
  
        # If current character in X[] and Y are same, then
        # current character is part of LCS
        if X[i-1] == Y[j-1]:
            lcs[index-1] = X[i-1]
            i-=1
            j-=1
            index-=1
  
        # If not same, then find the larger of two and
        # go in the direction of larger value
        elif L[i-1][j] > L[i][j-1]:
            i-=1
        else:
            j-=1
  
    return "".join(lcs) 


def handle(conn, address):    
    print('process-%s' % (address,))
    print('pid=',os.getpid())
    # try:
    print('Connected %s at %s' % (conn, address))
    
    #receive subsequence sizes
    m = int(conn.recv(10))
    n = int(conn.recv(10))

    print('len(seq1)=',m)
    print('len(seq2)=',n)

    seq1 = bytearray()
    while len(seq1) < m:
        packet = conn.recv(m - len(seq1))
        if not packet:
            break
        seq1.extend(packet)

    seq2 = bytearray()
    while len(seq2) < n:
        packet = conn.recv(n - len(seq2))
        if not packet:
            break
        seq2.extend(packet)

    seq1 = "".join( chr(x) for x in bytearray(seq1) )
    seq2 = "".join( chr(x) for x in bytearray(seq2) )

    # print('seq1=',seq1)
    # print('seq2=',seq2)

    common = lcs(seq1,seq2,m,n)

    # print('lcs=',common)
    
    size = str(len(common)).zfill(10)
    conn.send(size.encode())
    conn.sendall(common.encode())
    print('finished')

    # except:
    #     print('Problem handling request')
    # finally:
    #     print('Closing socket')
    conn.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Concurrent TCP server')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='tcp server hostname (default 0.0.0.0)')
    parser.add_argument('--port', type=int, default=9000, help='tcp server port number (default 9000)')    
    args = parser.parse_args()
    print(args.host)
    print(args.port)

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind((args.host, args.port))
    socket.listen(5)
    print('tcp concurrent server')

    while True:
        conn, address = socket.accept()
        print('Got connection. Forking process...')
        process = multiprocessing.Process(target=handle, args=(conn, address))
        # process.daemon = True
        process.start()
        print('Started process ', process)
