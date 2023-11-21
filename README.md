# 269382

Build the book
```
jupyter-book build --all .
```

Update the book's website
```
ghp-import -n -p -f _build/html
```

`jupytext`
```
jupytext --set-formats ipynb,myst notebook.ipynb
jupytext --sync notebook.ipynb 
```