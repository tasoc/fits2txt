
all:
	pyi-makespec --onefile --specpath . fits2txt/fits2txt.py
	# Add some thing at the top of the generated spec file
	echo "import sys; sys.setrecursionlimit(10000)" | cat - fits2txt.spec > fits2txt.tmp.spec && mv fits2txt.tmp.spec fits2txt.spec
	pyinstaller --onefile fits2txt.spec