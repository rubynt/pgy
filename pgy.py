import sys, os, subprocess
import numpy as np
from comp import *


mod = 17
def compile_latex(p: str):
    cwd = os.getcwd()
    subprocess.Popen(f"pdflatex {cwd}/{p}".split(' '), start_new_session=True).wait()


rems = (lambda v: v[:-1, np.newaxis] ** (v - 1))(np.arange(1,mod+1)) % mod

fn = 'test.tex'
#fd = open(sys.argv[1], 'w')
fd = open(fn, 'w')
fd.write(r'''
\documentclass{article}
\usepackage[a4paper, total={6.4in, 10in}]{geometry}
\usepackage{amsmath}
\usepackage{parskip}
\usepackage{tikz}
\usetikzlibrary{tikzmark}
\begin{document}
''')

fd.write(rf'''
\begin{{table}}
\begin{{tabular}}{{{('c|'*(mod+1))[:-1]}}}
''')
#np.vectorize()(a)
print(rems)
cs = list(map(comp_fun(len, set), (rems[1:, 1:])))
table_content = ['']
table_content += [' & '.join([f'(mod {mod})'] + [f'a^{{{n}}}' for n in range(mod)]) + '\\\\\n']
for irem, a in enumerate(rems[1:, 1:]):
    sify = []
    final = f'{irem+2} & 1 & '
    if cs[irem] < 4:
        sify = list(map(str,a))
    else:
        h = 0
        for i,v in enumerate(a):
            # print(f'{i}%{cs[irem]} = {(i)%cs[irem]}' + ('Hit'
            #                                                 if ( (i)%cs[irem] in (0, cs[irem]-1)) else
            #                                                 'Pass'))
            if ( (i)%cs[irem] in (0, cs[irem]-1)) :
                sify += [rf'\tikzmarknode{{n{irem}{h}}}{{{v}}}']
                h += 1
            else:
                sify += [str(v)]
    final += ' & '.join(sify)
    final += rf' \\{'\n'}'
    table_content += [final]
    
fd.write(' \\hline \n'.join(table_content))
    
fd.write(r'''
\end{tabular}
\end{table}
''')
fd.write(r'''
\begin{tikzpicture}[remember picture,overlay,
  highlight/.style={draw=red,rounded corners, thin, 
                    minimum width=1em,minimum height=2.5ex},
  note/.style={font=\small,red,text width=3cm},
  ]
''')
for i, n in enumerate(cs):
    if n>=4:
        for k in range((mod-1)//n):
            fd.write(rf'''
  \draw[highlight] ([yshift=1.8ex,xshift=-1.2em]pic cs:n{i}{2*k}) 
                   rectangle ([yshift=-0.4ex,xshift=0.4em]pic cs:n{i}{2*k+1}) ;
''')
fd.write(r'''
\end{tikzpicture}
''')

fd.write(r'''
\end{document}
''')
fd.close()

#compile_latex(fn)
