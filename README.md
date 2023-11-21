# 269382

Build the book
```
jupyter-book build --all .
```

`jupytext`
```
jupytext --set-formats ipynb,myst notebook.ipynb
jupytext --sync notebook.ipynb 
```