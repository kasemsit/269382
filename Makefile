build:
	jupyter-book build --all ./
clean:
	rm -f notebook/data.xlsx 
	rm -f notebook/online_retail.xlsx 
	rm -f notebook/ggez.csv 
	rm -f notebook/lnwzaa55+.csv	
	rm -f notebook/iris.zip 	
	rm -rf notebook/iris_data
	rm -f notebook/myapple_1.csv 
	rm -f notebook/myapple_2.csv
	rm -rf _build/
	jupyter-book clean ./ --all
deploy:
	ghp-import -n -p -f _build/html