CC = g++

main: main.o ./regex/Regex.o ./regex/Atom.o ./regex/KleeneStar.o ./regex/Concat.o ./regex/Union.o ./regex/Epsilon.o
	$(CC) main.o ./regex/Atom.o ./regex/Regex.o ./regex/KleeneStar.o ./regex/Concat.o ./regex/Union.o

main.o: main.cpp
	$(CC) -c main.cpp

./regex/Regex.o: ./regex/Regex.cpp ./regex/Regex.h
	$(CC) -c ./regex/Regex.cpp

./regex/Atom.o: ./regex/Atom.cpp ./regex/Atom.h ./regex/Regex.h
	$(CC) -c ./regex/Atom.cpp

./regex/KleeneStar.o: ./regex/KleeneStar.cpp ./regex/KleeneStar.h ./regex/Regex.h
	$(CC) -c ./regex/KleeneStar.cpp

./regex/Concat.o: ./regex/Concat.cpp ./regex/Concat.h ./regex/Regex.h
	$(CC) -c ./regex/Concat.cpp

./regex/Union.o: ./regex/Union.cpp ./regex/Union.h ./regex/Regex.h
	$(CC) -c ./regex/Union.cpp

./regex/Epsilon.o: ./regex/Epsilon.cpp ./regex/Epsilon.h ./regex/Regex.h
	$(CC) -c ./regex/Epsilon.cpp
