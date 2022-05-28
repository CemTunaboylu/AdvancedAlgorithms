def from_lps_table(s:str):
        lps = [-1]
        i = 0
        for j in range(1,len(s)):
                while i>0 and s[i] != s[j]: i = lps[i-1]

                if s[i] == s[j]: i +=1
                
                lps.append(i-1)

        return lps
"""
 lps = [0]
 (i=0,j=1)lps = [0,0]
 (i=0,j=2)lps = [0,0,1] (lps[j]=i since i=0)
 (i=1,j=3)lps = [0,0,1,2] (lps[j]=i+1 since i>0)
 (i=2,j=4)lps = [0,0,1,2] (i=lps[i-1]=0 since i>0)
 (i=0,j=4)lps = [0,0,1,2] (lps[j]=i since =0)
"""

from icecream import ic
def occurs(s:str, l:str)->int:
        lps = from_lps_table(s)
        j = -1
        for i,symbol in enumerate(l): 
                if j == (len(s)-1): return True
                # as long as j is not -1, backtrack j 
                while j>-1 and s[j+1] != symbol: 
                        j = lps[j]
                if s[j+1] == symbol:
                        j += 1
                
        return j == ((len(s)-1))
""" 
s, l = "abab|d", "ababab|d|"
LPS = [-1, -1, 0, 1, -1] , len(s) = 5

(j=-1) s[j+1] == 'a' ✔️ 
(j=0)  s[j+1] == 'b' ✔️ 
(j=1) s[j+1] == 'a' ✔️ 
(j=2)  s[j+1] == 'b' ✔️ 
(j=3) s[j+1] == 'a' X ->  j > -1 ✔️ and s[j+1] != 'a' ✔️  -> j = lps[3] -> 1
                    (j=1) j > -1 ✔️ and s[2] != 'a' ✔️ 
              
(j=2)  s[j+1] == 'b' ✔️
(j=3)  s[j+1] == 'd' ✔️

j=4
"""


if __name__ == "__main__":
        s = "ababd"
        ls = ["ababd", "abababd" , "abacababd", "ababcabcabababd", "ababcabcabababababcabcabababd"]
        i = 0
        for i,l in enumerate(ls):
                r = occurs(s, l)
                assert r == True
                print(f"Test{i}  ✔️")
        fs = [ "ababababab", "abdabd", "ababc", "ababcabcabababababcabcabababababcabcabababababcabcababab" ]
        for f in fs:
                i += 1
                r = occurs(s, f)
                assert r == False
                print(f"Test{i}  ✔️")
