#this programme writes latex codes.
python_indices = ['TXx', 'TNx', 'TXn', 'TNn', 'DTR', 'FD', 'TR']
climpact_indices = ['csdi', 'id', 'su', 'tn10p', 'tn90p', 'tnn', 'tnx', 'tx10p', 'tx90p', 'txn', 'txx', 'wsdi']
ghcndex_climpact_indices = ['CSDI', 'ID',  'SU',  'TN10p', 'TN90p',  'TNn',  'TNx',
              'TX10p', 'TX90p','TXn', 'TXx', 'WSDI']


REGION = 'SPAIN'

MIN_OR_MAX = 'max'

with open('python_indices_'+MIN_OR_MAX+'_'+REGION+'.txt', 'w') as f:
    for INAME in python_indices:
        f.write('\n\n\n')
        f.write('\\begin{figure*}\n\centering\n\\begin{subfigure}[b]{0.475\\textwidth}\n\centering\n')
        f.write('\\includegraphics[width=\\textwidth]{/scratch/vportge/plots/Python_Indices/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+INAME+'_map_of_trend_'+REGION+'.png}')
        f.write('\caption[]{{\small CM SAF LST}}\n\\end{subfigure}\n\hfill\n')

        f.write('\\begin{subfigure}[b]{0.475\\textwidth}\n\centering\n')
        f.write('\\includegraphics[width=\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+INAME+'_map_of_trend_'+REGION+'.png}')
        f.write('\caption[]{{\small GHCNDEX}}\n\\end{subfigure}\n')
        f.write('\\vskip\\baselineskip\n')

        f.write('\\begin{subfigure}[b]{0.475\\textwidth}\n\centering\n')
        f.write('\\includegraphics[width=\\textwidth]{/scratch/vportge/plots/Python_Indices/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+INAME+'_with_trend_ANN_'+REGION+'.png}')
        f.write('\caption[]{{\small CM SAF LST}}\n\\end{subfigure}\n')
        f.write('\quad\n')

        f.write('\\begin{subfigure}[b]{0.475\\textwidth}\n\centering\n')
        f.write('\\includegraphics[width=\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+INAME+'_time_series_GHCNDEX_with_trend_annually_'+REGION+'.png}')
        f.write('\caption[]{{\small GHCNDEX}}\n\\end{subfigure}\n')

        f.write('\caption[]\n{\small '+INAME+' }\n \label{fig:'+INAME+'_'+MIN_OR_MAX +'}\n')
        f.write('\\end{figure*}')


with open('climpact_indices_'+MIN_OR_MAX+'_'+REGION+'.txt', 'w') as f:
    for i in range(len(climpact_indices)):
        ICLIMP = climpact_indices[i]
        IGHCNDEX = ghcndex_climpact_indices[i]

        f.write('\n\n\n')
        f.write('\\begin{figure*}\n\centering\n\\begin{subfigure}[b]{0.475\\textwidth}\n\centering\n')
        f.write('\\includegraphics[width=\\textwidth]{/scratch/vportge/plots/Climpact/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+ICLIMP+'_map_of_trend_'+REGION+'.png}')
        f.write('\caption[]{{\small CM SAF LST}}\n\\end{subfigure}\n\hfill\n')

        f.write('\\begin{subfigure}[b]{0.475\\textwidth}\n\centering\n')
        f.write('\\includegraphics[width=\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+IGHCNDEX+'_map_of_trend_'+REGION+'.png}')
        f.write('\caption[]{{\small GHCNDEX}}\n\\end{subfigure}\n')
        f.write('\\vskip\\baselineskip\n')

        f.write('\\begin{subfigure}[b]{0.475\\textwidth}\n\centering\n')
        f.write('\\includegraphics[width=\\textwidth]{/scratch/vportge/plots/Climpact/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+ICLIMP+'_with_trend_ANN_'+REGION+'.png}')
        f.write('\caption[]{{\small CM SAF LST}}\n\\end{subfigure}\n')
        f.write('\quad\n')

        f.write('\\begin{subfigure}[b]{0.475\\textwidth}\n\centering\n')
        f.write('\\includegraphics[width=\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+IGHCNDEX+'_time_series_GHCNDEX_with_trend_annually_'+REGION+'.png}')
        f.write('\caption[]{{\small GHCNDEX}}\n\\end{subfigure}\n')

        f.write('\caption[]\n{\small '+IGHCNDEX+' }\n \label{fig:'+IGHCNDEX+'_'+MIN_OR_MAX +'}\n')
        f.write('\\end{figure*}')




#2x3 subfigures


with open('python_indices_2x3_subfigures'+MIN_OR_MAX+'_'+REGION+'.txt', 'w') as f:
    for INAME in python_indices:
        f.write('\n\n\n')
        f.write('\\begin{figure}\n\centering\n')

        f.write('\\begin{subfigure}[b]{0.3\\textwidth}\n\centering\n')
        f.write('\\includegraphics[width=\\textwidth]{/scratch/vportge/plots/Python_Indices/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+INAME+'_with_trend_ANN_'+REGION+'.png}')
        f.write('\caption[]{{\small CM SAF LST}}\n\\end{subfigure}\n\hfill\n')

        f.write('\\begin{subfigure}[b]{0.3\\textwidth}\n\centering\n')
        f.write('\\includegraphics[width=\\textwidth]{/scratch/vportge/plots/Python_Indices/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+INAME+'_2005-2015_map_of_trend_'+REGION+'.png}')
        f.write('\caption[]{{\small CM SAF LST}}\n\\end{subfigure}\n\hfill\n')

        f.write('\\begin{subfigure}[b]{0.3\\textwidth}\n\centering\n')
        f.write('\\includegraphics[width=\\textwidth]{/scratch/vportge/plots/Python_Indices/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+INAME+'_2005-2015_map_of_trend_'+REGION+'.png}')
        f.write('\caption[]{{\small CM SAF LST}}\n\\end{subfigure}\n')
        f.write('\\vskip\\baselineskip\n')

        f.write('\\begin{subfigure}[b]{0.3\\textwidth}\n\centering\n')
        f.write('\\includegraphics[width=\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+INAME+'_time_series_GHCNDEX_with_trend_annually_'+REGION+'.png}')
        f.write('\caption[]{{\small GHCNDEX}}\n\\end{subfigure}\n')
        f.write('\quad\n')

        f.write('\\begin{subfigure}[b]{0.3\\textwidth}\n\centering\n')
        f.write('\\includegraphics[width=\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+INAME+'_1991-2004_map_of_trend_'+REGION+'.png}')
        f.write('\caption[]{{\small GHCNDEX}}\n\\end{subfigure}\n')
        f.write('\quad\n')

        f.write('\\begin{subfigure}[b]{0.3\\textwidth}\n\centering\n')
        f.write('\\includegraphics[width=\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+INAME+'_2005-2015_map_of_trend_'+REGION+'.png}')
        f.write('\caption[]{{\small GHCNDEX}}\n\\end{subfigure}\n')

        f.write('\caption[]\n{\small '+INAME+' }\n \label{fig:'+INAME+'_'+MIN_OR_MAX +'}\n')
        f.write('\\end{figure}')



'''
                {{\small CM SAF LST}}    
                %\label{fig:mean and std of net14}
        \end{subfigure}
        \hfill

        \begin{subfigure}[b]{0.475\textwidth}  
                \centering 
                \includegraphics[width=\textwidth]{/scratch/vportge/plots/GHCNDEX/GERMANY/TXn_map_of_trend_GERMANY.png}
                \caption[]%
                {{\small GHCNDEX }}    
                %\label{fig:mean and std of net24}
        \end{subfigure}
        \vskip\baselineskip
        \begin{subfigure}[b]{0.475\textwidth}   
                \centering 
                \includegraphics[width=\textwidth]{/scratch/vportge/plots/Python_Indices/min_LST_in_cold_window/GERMANY/TXn_with_trend_ANN_GERMANY.png}
                \caption[]%
                {{\small CM SAF LST}}    
                %\label{fig:mean and std of net34}
        \end{subfigure}
        \quad
        \begin{subfigure}[b]{0.475\textwidth}   
                \centering 
                \includegraphics[width=\textwidth]{/scratch/vportge/plots/GHCNDEX/GERMANY/TXn_time_series_GHCNDEX_with_trend_annually_GERMANY.png}
                \caption[]%
                {{\small GHCNDEX}}    
                %\label{fig:mean and std of net44}
        \end{subfigure}
        %\caption[ The average and standard deviation of critical parameters ]
        {\small TXn } 
        \label{fig:TXn}
\end{figure*}
'''