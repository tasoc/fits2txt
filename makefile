
all:
	pyi-makespec fits2txt/fits2txt.py
	# Add some thing at the top of the generated spec file
	#echo "import sys; sys.setrecursionlimit(10000)"
	pyinstaller --onefile fits2txt.spec