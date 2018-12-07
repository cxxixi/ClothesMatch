#include <iostream>
#include <vector>
#include <ctime>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <chrono>
#include <iomanip>
#include <unordered_map>
#include <stdio.h>
#include <math.h>

using namespace std;
struct node 
{ 
    double value; 
    int index; 
}; 

bool cmp(struct node a, struct node b) 
{ 
    if(a.value > b.value)
    { 
        return true; 
    } 
    return false; 
} 

unordered_map <int, vector<int>> readItemInfo(string input_file){
	
	ifstream itemsFile;
	itemsFile.open(input_file);

	unordered_map <int, vector<int>> itemInfo;
	string line;
	int counter = 0;
	int item_id, cat_id, term_id;
	string t;
	vector<string> tmp; //to store the string of terms
	vector<int> terms; // first element of terms is the category id, the rest of it are the term ids.
	std::string::size_type sz;

	while(getline(itemsFile, line)) {
    	stringstream ss(line);
    	//cout << line <<endl;
    	tmp.clear();
    	while(getline(ss, t, ' ')){
    		tmp.push_back(t);
    	}
    	item_id = std::stoi(tmp[0], &sz);
    	cat_id = std::stoi(tmp[1], &sz);

    	// cout << item_id << "\t" << cat_id << "\t" << tmp[2] << endl;

    	terms.clear();
    	terms.push_back(cat_id);

    	stringstream st(tmp[2]);
    	// split string into array in int
    	while(getline(st, t, ',')){
    		term_id = std::stoi (t,&sz);
    		terms.push_back(term_id);
   // 		cout << term_id << endl;
     	}
     	// use item_id as key, put "terms" array into hashMap.
     	itemInfo[item_id]=terms;
     	counter ++;
     	//cout << "counter output \t" <<counter << endl;
	}
	return itemInfo;
}

void readFashionFile(string input_file, unordered_map <int, vector<int>> &item_to_menu, unordered_map <int, vector<int>> &menu_to_item){
	ifstream fashionFile;
	fashionFile.open(input_file);

	string line;

	int col_id, item_id;
	string t;
	vector<string> tmp; //to store the string of items
	vector<int> items; 
	std::string::size_type sz;

	while(getline(fashionFile, line)) {
    	stringstream ss(line);
    	//cout << line <<endl;
    	tmp.clear();
    	while(getline(ss, t, ' ')){
    		tmp.push_back(t);
    	}
    	col_id = std::stoi(tmp[0], &sz);

    	// cout << item_id << "\t" << cat_id << "\t" << tmp[2] << endl;

    	items.clear();

    	stringstream st(tmp[1]);
    	// split string into array in int
    	while(getline(st, t, ',')){
    		item_id = std::stoi (t,&sz);
    		item_to_menu[item_id].push_back(col_id);
    		items.push_back(item_id);
     	}
     	menu_to_item[col_id] = items;
     	//cout << "counter output \t" <<counter << endl;
	}
}

unordered_map <int, vector<double>> calcTF(unordered_map <int, vector<int>> itemInfo, unordered_map <int, vector<int>> &itemInfoUnique){
	unordered_map <int, vector<double>> tf;
	vector<double> tmp;
	vector<int> termsOriginal;
	vector<int> termsUnique;
	vector<int> countUnique;
	vector<int> Unique;

	for(auto item : itemInfo){
		tmp.clear();
		termsOriginal.clear();
		termsUnique.clear();
		countUnique.clear();
		Unique.clear();

		// cout << "item number: " << item.first << endl;

		Unique.push_back((item.second)[0]);
		for(int i = 1; i < item.second.size(); i++){
			termsOriginal.push_back((item.second)[i]);
		//	cout << item.second[i] << endl;
		}
		sort(termsOriginal.begin(), termsOriginal.end());
		//	for(int i = 0; i < termsOriginal.size(); i++){
		//		cout << termsOriginal[i] << endl;
		//	}
		int previous = -1;
		for(int i = 0; i < termsOriginal.size(); i++){
			if(termsOriginal[i] == previous){
				countUnique[countUnique.size()-1] ++;
			}
			else{
				countUnique.push_back(1);
				termsUnique.push_back(termsOriginal[i]);
				Unique.push_back(termsOriginal[i]);
			}
			previous = termsOriginal[i];
		}

		int s = termsOriginal.size();

		for(int i = 0; i < termsUnique.size(); i++)
			tmp.push_back(1.0*countUnique[i]/s);
		tf[item.first] = tmp;
		itemInfoUnique[item.first] = Unique;
	}
	/*
	for(int i =0; i < itemInfo[199029].size(); i++)
		cout << itemInfo[199029][i] << "\t";
	cout << endl;

	for(int i =0; i < itemInfoUnique[199029].size(); i++)
		cout << itemInfoUnique[199029][i] << "\t";
	cout << endl;

	cout << itemInfoUnique[199029][0] << "\t";
	for(int i =0; i < tf[199029].size(); i++)
		cout << tf[199029][i] << "\t";
	cout << endl;	
	*/
	return tf;
}

unordered_map <int, vector<double>> calcIDF(unordered_map <int, vector<int>> itemInfoUnique, vector<unordered_map<int, int> > &cat_term_num, vector<int> &cat_num){
	const double E=2.718281828459;
	//unordered_map<int, int> tmp;
	// cat_term_num to store number of each item with specific term in each category
	//vector<unordered_map<int, int> > cat_term_num(700, tmp);
	// cat_num to store number of items in each category
	//vector<int> cat_num(700, 0);
	// calculate cat_num and cat_term_num
	for(auto item : itemInfoUnique){
		int item_id = item.first;
		vector<int> terms = item.second;
		int cat_id = terms[0];
		// if the item belongs to cat_id
		cat_num[cat_id] ++;
		// scan the terms that belong the to item, and update cat_term_num
		for(int i = 1; i < terms.size(); i++ ){
			if(cat_term_num[cat_id].find(terms[i]) == cat_term_num[cat_id].end())
				cat_term_num[cat_id][terms[i]] = 1;
			else
				cat_term_num[cat_id][terms[i]] ++;
		}
	}
	// cout << "OK" << endl;
	// cout << cat_num[70] << endl;
	// cout << cat_term_num[70][15463] << endl;

	unordered_map<int, vector<double> > idf;
	vector<double> ttt;
	for(auto item : itemInfoUnique){
		int item_id = item.first;
		vector<int> terms = item.second;
		int cat_id = terms[0];
		ttt.clear();
		int a, b;
		a = cat_num[cat_id];
	//	cout << cat_id << "\t" << a << endl;
		for(int i = 1; i < terms.size(); i++){
			b = cat_term_num[cat_id][terms[i]];
			ttt.push_back(1.0*(log(1.0*a/b)/log(E)));
		//	ttt.push_back(b);
		}
		idf[item_id] = ttt;
	}
	// cout << cat_num[70] << endl;
	// cout << cat_term_num[70][15463] << endl;
	return idf;
}

unordered_map <int, vector<double>> functionG(unordered_map <int, vector<double>> &tf,  unordered_map <int, vector<double>> &idf){
	const double alpha = 0.008;
	const double beta = 0.07;
	unordered_map <int, vector<double>> gx;

	vector<double> g_values;
	vector<double> tf_values;
	vector<double> idf_values;
	for (auto item : tf){
		g_values.clear();
		tf_values.clear();
		idf_values.clear();

		int item_id = item.first;
		tf_values = item.second;
		idf_values = idf[item_id];

		if(tf_values.size()!=idf_values.size())
			cout << "ERROR!" << endl;
		for(int i = 0; i< tf_values.size(); i++){
			double tt = 1.0 * tf_values[i] * (alpha * idf_values[i] + beta);
			g_values.push_back(tt);
		}
		gx[item_id] = g_values;
	}
	return gx;
}

unordered_map <int, double> getmode(unordered_map <int, vector<double>> &gx){
	unordered_map <int, double> items_mode;
	vector<double> values;
	double modeValue;
	for(auto item : gx){
		values.clear();
		modeValue = 0;
		int key = item.first;
		values = item.second;
		for(int i = 0; i< values.size(); i++){
			modeValue += 1.0*values[i]*values[i];
		}
		modeValue = sqrt(modeValue);
		items_mode[key] = modeValue;
	}
	return items_mode;
}

inline double consine_simlarity(vector<int> terms_x, vector<int> terms_y, vector<double> tfidf_x, vector<double> tfidf_y, double modex, double modey){
	double cos_sim = 0;
	for(int i = 1; i < terms_x.size(); i++){
		for(int j = 1; j < terms_y.size(); j++){
			if(terms_x[i] == terms_y[j])
				cos_sim += tfidf_x[i-1] * tfidf_y[j-1];
		}
	}
	cos_sim = cos_sim/modex;
	cos_sim = cos_sim/modey;
	return cos_sim;
}

inline double fei_unique(int match_key, vector<int> &match_unique, unordered_map <int, vector<int>> &item_to_menu, unordered_map <int, vector<int>> &menu_to_item){
	const double alpha = 0.15;
	const double beta = 1;
	const double E=2.718281828459;
	double result;

	// cout << "match key:" << "\t" <<match_key << endl;
	vector<int> match_items;
	for(int i = 0; i < item_to_menu[match_key].size(); i++){
		int menu_id = item_to_menu[match_key][i];
	//	cout << "menu id:" << "\t" <<menu_id << endl;
		match_items.insert(match_items.end(), menu_to_item[menu_id].begin(), menu_to_item[menu_id].end());
	}

	int previous = -1;
	sort(match_items.begin(), match_items.end());

	for(int i = 0; i < match_items.size(); i++){
		if(match_items[i] == previous || match_items[i] == match_key)
			continue;
		else
			match_unique.push_back(match_items[i]);
		previous = match_items[i];
	}
	result = alpha * log(match_unique.size())/log(E) + beta;
	// cout << "fei(match key):" << "\t" << result << endl;;
	return result;
}

inline double fei(int match_key, unordered_map <int, vector<int>> &item_to_menu, unordered_map <int, vector<int>> &menu_to_item){
	const double alpha = 0.15;
	const double beta = 1;
	const double E=2.718281828459;
	double result;

	vector<int> match_items;
	for(int i = 0; i < item_to_menu[match_key].size(); i++){
		int menu_id = item_to_menu[match_key][i];
		// cout << "match_key: " << match_key << "\t" << "menu id: " << menu_id << endl;
		match_items.insert(match_items.end(), menu_to_item[menu_id].begin(), menu_to_item[menu_id].end());
	}

	int previous = -1;
	sort(match_items.begin(), match_items.end());

	int count = 0;
	for(int i = 0; i < match_items.size(); i++){
		if(match_items[i] == previous || match_items[i] == match_key)
			continue;
		else
			count ++;
		previous = match_items[i];
	}
	result = alpha * log(count)/log(E) + beta;
	// cout << "count " << count << endl;
	// cout << "fei result: " << result << endl;
	return result;
}

inline double match_degree(int x_key, int y_key, unordered_map <int, vector<int>> &item_to_menu, unordered_map <int, vector<int>> &menu_to_item,
	unordered_map <int, vector<double>> &gx, unordered_map <int, double> &items_mode, unordered_map <int, vector<int>> &itemInfoUnique){
	// get all the items that y matches
	vector<int> y_match_unique;
	double fei_y = fei_unique(y_key, y_match_unique, item_to_menu, menu_to_item);
	//vector<double> similarities;
	//vector<double> feiValues;
	double p = 4;
	double q = 0.25;
	double result = 0;

	vector<int> terms_x = itemInfoUnique[x_key];
	double modex = items_mode[x_key];
	vector<double> tfidf_x = gx[x_key];

	// cout << "OK2" << endl;
	for(int i = 0; i < y_match_unique.size(); i++){
	//	cout << i <<"th match: "<< y_match_unique[i] << endl;
		vector<int> terms_y = itemInfoUnique[y_match_unique[i]];
		double modey = items_mode[y_match_unique[i]];
		vector<double> tfidf_y = gx[y_match_unique[i]];

		double sim = consine_simlarity(terms_x, terms_y, tfidf_x, tfidf_y, modex, modey);
		// cout << "sim: " << sim << endl;
		//similarities.push_back(sim);

		double feiV = fei(y_match_unique[i], item_to_menu, menu_to_item);
		//feiValues.push_back(feiV);
		// cout << "feiV: " << feiV << endl;
		result += pow(sim/feiV, p);
	}
	result = pow(result, q);
	result = result * fei_y;
	return result;
}

int main(int argc, char *argv[]) {

	if (argc < 6) {
		cout << "Usage: " << argv[0] << " <dims_items> <fashionFile> <clothesID> <refID> <output>" << endl;
		return 1;
	}
	
	unordered_map <int, vector<int>> itemInfo;
	unordered_map <int, vector<int>> itemInfoUnique;
	unordered_map <int, vector<double>> tf;
	unordered_map <int, vector<double>> idf;
	unordered_map <int, vector<double>> gx;
	unordered_map <int, double> items_mode;

	unordered_map<int, int> tmp;
	vector<unordered_map<int, int> > cat_term_num(700, tmp);
	vector<int> cat_num(700, 0);

	
	itemInfo = readItemInfo(argv[1]);
	tf = calcTF(itemInfo, itemInfoUnique);
	idf = calcIDF(itemInfoUnique, cat_term_num, cat_num);
	gx = functionG(tf, idf);
	items_mode = getmode(gx);
	// clear memory
	itemInfo.clear();
	tf.clear();
	idf.clear();
	cat_term_num.clear();
	cat_num.clear();

	//read in fashion file
	
	unordered_map <int, vector<int>> item_to_menu;
	unordered_map <int, vector<int>> menu_to_item;
	readFashionFile(argv[2], item_to_menu, menu_to_item);
	/*
	cout << menu_to_item[39][0] << "\t" <<menu_to_item[39][menu_to_item[39].size()-1] << endl;
	for(int i = 0; i < item_to_menu[2559648].size(); i++)
		cout << item_to_menu[2559648][i] << endl;

	*/

	ifstream clothesFile;
	clothesFile.open(argv[3]);

	ifstream refFile;
	refFile.open(argv[4]);

	ofstream output;
	output.open(argv[5]);

	string line;
	vector<int> clothesIDs;
	vector<int> refIDs;
	int id;
	std::string::size_type sz;

	while(getline(clothesFile, line)) {
    	// stringstream ss(line);	
		sscanf(line.c_str(), "%d", &id);
    	clothesIDs.push_back(id);
	}

	while(getline(refFile, line)) {
    	// stringstream ss(line);	
		sscanf(line.c_str(), "%d", &id);
    	refIDs.push_back(id);
	}

	int len = refIDs.size();

	for(int i = 0; i < clothesIDs.size(); i++){
		node* result = new node[len];
		for(int j = 0; j < refIDs.size(); j++){
			result[j].index = refIDs[j];
			result[j].value = match_degree(clothesIDs[i], refIDs[j], item_to_menu, menu_to_item, gx, items_mode, itemInfoUnique);
		}
		sort(result, result+len, cmp);
		output << clothesIDs[i] << "\t";
		for(int k = 0; k < std::min(200, len); k++){
			output << result[k].index << ":" << result[k].value << "\t" ;
		}
		output << endl;
		delete [] result;
	}


	int x_key = 29;
	int y_key = 113312;

	double result = match_degree(x_key, y_key, item_to_menu, menu_to_item, gx, items_mode, itemInfoUnique);
	cout << "result is " << result << endl;
}