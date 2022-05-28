def rabin_karp(long:str, short:str)->int: 
    num_chars = 128 # ascii

    def rabin_fingerprint(hash_in:str, new_start_index:int, hash_val:int=0):
        end = new_start_index+len(short)
        print(f"Hashing : '{hash_in[new_start_index:end]}'")
        if hash_val > 0:
            rem_val = ord(hash_in[new_start_index-1]) * num_chars**(len(short)-1)
            print(f"rem val : {rem_val}")
            print(f"hash_val - rem_val : {hash_val - rem_val}")
            hash_val = (hash_val - rem_val)*num_chars + ord(hash_in[end])
        else: # hash from scratch
            hash_val = sum([ (ord(hash_in[i])) * num_chars**(len(short)-1-i) for i in range(0, len(short)) ])
        print(f" w/ hash:{hash_val}")
        return hash_val

    search_hash = rabin_fingerprint(short, 0)
    print(f"Search hash : {search_hash}")
    h = 0
    for i in range(0, len(long)-len(short)):
        h = rabin_fingerprint(long, i, h)
        if h == search_hash: 
            print(f"Checking {long[i:len(short)+i]}")
            if long[i:len(short)+i] == short:
                print(F"Match : {long[i:len(short)+i]} == {short}")
                return i
            
    return -1

        

long, short = 'doe are hearing me', 'ear'
rabin_karp(long ,short)