#include <iostream>
#include <vector>

using namespace std;

vector<int> form_lps_table(const string& pattern){
	vector<int> lps( pattern.size() );
	int i=0, j=1;
        lps[0] = 0;
	for (; j < pattern.size(); j++){
		while (i>0 && pattern[i]!=pattern[j]) i = lps[i-1];

		if (pattern[i] == pattern[j]) i++; 
	                        lps[j] = i;
	        	}
	return lps;
}


int main(){
        string p = "ababd";
        vector<int> lps = form_lps_table(p);
        for (int i=0; i < lps.size(); i++) cout << lps[i] ;
        cout << endl;
        return 0;
}