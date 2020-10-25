// toCSV.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//

#include <iostream>
#include <regex>
#include <fstream>
#include <string>


int main()
{
	std::ifstream fin("ss.txt");
	std::ofstream citysp("city.txt");
	std::ofstream zapis("zap.txt");
	std::regex zap("([0-9]{2}) "
		"([A-Z][a-z][a-z]) "
		"- "
		"([0-9]{2}) "
		"([A-Z][a-z][a-z]) "
		"(1?[ ]*2?[ ]*3?[ ]*4?[ ]*5?[ ]*6?[ ]*7?[ ]*) "
		"([0-9][0-9]:[0-9][0-9])\\+?[-]?1? "
		"([0-9][0-9]:[0-9][0-9])\\+?[-]?1? "
		"(([A-Z]{2}[0-9]{1,4})\\*?) "
		"([A-Za-z0-9]{3}) "
		"(([0-9]{1,2})H([0-9]{1,2})M)"
	);
	std::regex oper("Operated by: (.*)");
	std::regex test("(FROM:|TO:) ([A-Za-z ]*)[ \f\n\r\t\v]?,"
		"[ \f\n\r\t\v]?([A-Za-z ]*)?[ \f\n\r\t\v]?"
		"([A-Za-z]{3})");
	std::cmatch result;
	std::string provString;
	std::string str;
	std::string from;
	std::string to;
	//bool f;
	int i = 0;
	while (!((fin.bad())||(fin.eof())||(fin.fail())))
	{
		std::cout << i++ << std::endl;
		getline(fin,provString);
		if (std::regex_match(provString.c_str(), zap))
		{
			std::regex_search(provString.c_str(), result, zap);
			zapis << std::endl;
			zapis << from << ";" << to << ";" << result[1] << ";" << result[2] << ";" << result[3] << ";" << result[4] << ";" << result[5] << ";" << result[6] << ";" << result[7] << ";" << result[9] << ";" << result[10] << ";" << result[12] << ";" << result[13];
		}
		if (std::regex_match(provString.c_str(), oper))
		{
			std::regex_search(provString.c_str(), result, oper);
			zapis << ";" << result[1];
		}
		if (std::regex_match(provString.c_str(), test))
		{
			std::regex_search(provString.c_str(), result, test);
			std::string a = result[3];
			if (a.size() != 0)
				a.erase(a.size() - 1);
			else
				a = result[2];
			citysp << result[2] << ";" << a << ";" << result[4] << std::endl;
			if (result[1] == "TO:")
				to = result[4];
			else
				from = result[4];
		}

	}

//
	
	
	
    
}

// Запуск программы: CTRL+F5 или меню "Отладка" > "Запуск без отладки"
// Отладка программы: F5 или меню "Отладка" > "Запустить отладку"

// Советы по началу работы 
//   1. В окне обозревателя решений можно добавлять файлы и управлять ими.
//   2. В окне Team Explorer можно подключиться к системе управления версиями.
//   3. В окне "Выходные данные" можно просматривать выходные данные сборки и другие сообщения.
//   4. В окне "Список ошибок" можно просматривать ошибки.
//   5. Последовательно выберите пункты меню "Проект" > "Добавить новый элемент", чтобы создать файлы кода, или "Проект" > "Добавить существующий элемент", чтобы добавить в проект существующие файлы кода.
//   6. Чтобы снова открыть этот проект позже, выберите пункты меню "Файл" > "Открыть" > "Проект" и выберите SLN-файл.
