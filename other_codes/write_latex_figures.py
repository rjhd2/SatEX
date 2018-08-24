#this programme writes latex codes.
python_indices = ['TXx', 'TNx', 'TXn', 'TNn', 'DTR', 'FD', 'TR']
climpact_indices = ['csdi', 'id', 'su', 'tn10p', 'tn90p', 'tnn', 'tnx', 'tx10p', 'tx90p', 'txn', 'txx', 'wsdi']
climpact_indices = ['csdi', 'id', 'su', 'tn10p', 'tn90p', 'tnn',  'tx10p', 'tx90p', 'txn',  'wsdi']

ghcndex_climpact_indices = ['CSDI', 'ID',  'SU',  'TN10p', 'TN90p',  'TNn', 
              'TX10p', 'TX90p','TXn',  'WSDI']

REGIONS = ['SPAIN', 'GERMANY', 'MOROCCO']
#REGION = 'SPAIN'
MINMAX = ['min', 'max']

for MIN_OR_MAX in MINMAX:
    '''
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
    '''
    '''
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

    '''


    #2x3 subfigures

    '''
    with open('python_indices_2x3_subfigures'+MIN_OR_MAX+'_'+REGION+'.txt', 'w') as f:
        for INAME in python_indices:
            f.write('\n\n\n')
            f.write('\\begin{figure}\n\centering\n')

            f.write('\\begin{subfigure}[b]{0.3\\textwidth}\n\centering\n')
            f.write('\\includegraphics[trim=0 -100 0 0,clip,width=\\textwidth]{/scratch/vportge/plots/Python_Indices/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+INAME+'_with_trend_ANN_'+REGION+'.png}')
            f.write('\n\\end{subfigure}\n\hfill\n')

            f.write('\\begin{subfigure}[b]{0.32\\textwidth}\n\centering\n')
            f.write('\\includegraphics[trim=90 60 70 0,clip,width=\\textwidth]{/scratch/vportge/plots/Python_Indices/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+INAME+'_1991-2004_map_of_trend_'+REGION+'.png}')
            f.write('\n\\end{subfigure}\n\hfill\n')

            f.write('\\begin{subfigure}[b]{0.32\\textwidth}\n\centering\n')
            f.write('\\includegraphics[trim=90 60 70 0,clip,width=\\textwidth]{/scratch/vportge/plots/Python_Indices/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+INAME+'_2005-2015_map_of_trend_'+REGION+'.png}')
            f.write('\n\\end{subfigure}\n')
            f.write('\\vskip\\baselineskip\n')

            f.write('\\begin{subfigure}[b]{0.3\\textwidth}\n\centering\n')
            f.write('\\includegraphics[trim=0 -100 0 0,clip,width=\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+INAME+'_time_series_GHCNDEX_with_trend_annually_'+REGION+'.png}')
            f.write('\n\\end{subfigure}\n')
            f.write('\hfill\n')

            f.write('\\begin{subfigure}[b]{0.32\\textwidth}\n\centering\n')
            f.write('\\includegraphics[trim=90 60 70 0,clip,width=\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+INAME+'_1991-2004_map_of_trend_'+REGION+'_'+MIN_OR_MAX+'.png}')
            f.write('\n\\end{subfigure}\n')
            f.write('\hfill\n')

            f.write('\\begin{subfigure}[b]{0.32\\textwidth}\n\centering\n')
            f.write('\\includegraphics[trim=90 60 70 0,clip,width=\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+INAME+'_2005-2015_map_of_trend_'+REGION+'_'+MIN_OR_MAX+'.png}')
            f.write('\n\\end{subfigure}\n')

            f.write('\caption[]\n{\small '+INAME+' }\n \label{fig:'+INAME+'_'+MIN_OR_MAX +'}\n')
            f.write('\\end{figure}')
   


    with open('climpact_indices_2x3_subfigures'+MIN_OR_MAX+'.txt', 'w') as f:
        for REGION in REGIONS:
            for i in range(len(climpact_indices)):
                ICLIMP = climpact_indices[i]
                IGHCNDEX = ghcndex_climpact_indices[i]  
                f.write('\n\n\n')
                f.write('\\begin{figure}\n')
                f.write('\\includegraphics[trim=70 40 55 10,clip,width=0.49\\textwidth]{"/scratch/vportge/plots/Climpact/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+ICLIMP+'_CM SAF_map_averaged_'+REGION+'"}')
                f.write('\\includegraphics[trim=70 40 55 10,clip,width=0.49\\textwidth]{"/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+IGHCNDEX+'_GHCNDEX_map_averaged_'+REGION+'"}')
                f.write('\caption[]\n{\small '+IGHCNDEX+' }\n \label{fig:average_'+IGHCNDEX+'_'+MIN_OR_MAX +'}\n')
                f.write('\\end{figure}')


                f.write('\n\n\n')
                f.write('\\begin{figure}\n')
                f.write('\\includegraphics[trim=90 60 70 10,clip,width=0.49\\textwidth]{/scratch/vportge/plots/Climpact/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+ICLIMP+'_with_trend_ANN_'+REGION+'.png}')
                f.write('\\includegraphics[trim=90 60 70 10,clip,width=0.49\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+IGHCNDEX+'_time_series_GHCNDEX_with_trend_annually_'+REGION+'.png}')
                f.write('\\vskip\\baselineskip\n')

                f.write('\\begin{subfigure}[b]{0.49\\textwidth}\n\centering\n')
                f.write('\\includegraphics[trim=90 60 70 10,clip,width=\\textwidth]{/scratch/vportge/plots/Climpact/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+ICLIMP+'_1991-2004_map_of_trend_'+REGION+'.png}')
                f.write('\n\\end{subfigure}\n\hfill\n')

                f.write('\\begin{subfigure}[b]{0.49\\textwidth}\n\centering\n')
                f.write('\\includegraphics[trim=90 60 70 10,clip,width=\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+IGHCNDEX+'_1991-2004_map_of_trend_'+REGION+'_'+MIN_OR_MAX+'.png}')
                f.write('\n\\end{subfigure}\n')
                f.write('\\vskip\\baselineskip\n')

                f.write('\\begin{subfigure}[b]{0.49\\textwidth}\n\centering\n')
                f.write('\\includegraphics[trim=90 60 70 10,clip,width=\\textwidth]{/scratch/vportge/plots/Climpact/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+ICLIMP+'_2005-2015_map_of_trend_'+REGION+'.png}')
                f.write('\n\\end{subfigure}\n\hfill\n')

                f.write('\\begin{subfigure}[b]{0.49\\textwidth}\n\centering\n')
                f.write('\\includegraphics[trim=90 60 70 10,clip,width=\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+IGHCNDEX+'_2005-2015_map_of_trend_'+REGION+'_'+MIN_OR_MAX+'.png}')
                f.write('\n\\end{subfigure}\n')

                f.write('\caption[]\n{\small '+IGHCNDEX+' }\n \label{fig:'+IGHCNDEX+'_'+MIN_OR_MAX +'}\n')
                f.write('\\end{figure}')
    '''
    with open('indices_average_2x3_subfigures'+MIN_OR_MAX+'.txt', 'w') as f:
        for REGION in REGIONS:
            f.write('\n\subsection{'+REGION+'}')
            for INAME in python_indices:
                
                f.write('\n\n\n')
                f.write('\\begin{figure}\n')
                f.write('\\includegraphics[trim=70 40 55 10,clip,width=0.49\\textwidth]{"/scratch/vportge/plots/Python_Indices/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+INAME+'_CM SAF_map_averaged_'+REGION+'"}')
                f.write('\\includegraphics[trim=70 40 55 10,clip,width=0.49\\textwidth]{"/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+INAME+'_GHCNDEX_map_averaged_'+REGION+'"}')
                f.write('\n\caption[]\n{\small '+INAME+' }\n \label{fig:average_'+INAME+'_'+MIN_OR_MAX +'}\n')
                f.write('\\end{figure}')
                '''

                f.write('\n\n\n')
                f.write('\\begin{figure}\n')
                f.write('\\includegraphics[trim=0 0 0 0 ,clip,width=0.49\\textwidth]{/scratch/vportge/plots/Python_Indices/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+INAME+'_with_trend_ANN_'+REGION+'.png}')
                f.write('\\includegraphics[trim=0 0 0 0 ,clip,width=0.49\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+INAME+'_time_series_GHCNDEX_with_trend_annually_'+REGION+'.png}')
                f.write('\\vskip\\baselineskip\n')

                f.write('\\begin{subfigure}[b]{0.49\\textwidth}\n\centering\n')
                f.write('\\includegraphics[trim=90 60 70 10,clip,width=\\textwidth]{/scratch/vportge/plots/Python_Indices/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+INAME+'_1991-2004_map_of_trend_'+REGION+'.png}')
                f.write('\n\\end{subfigure}\n\hfill\n')

                f.write('\\begin{subfigure}[b]{0.49\\textwidth}\n\centering\n')
                f.write('\\includegraphics[trim=90 60 70 10,clip,width=\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+INAME+'_1991-2004_map_of_trend_'+REGION+'_'+MIN_OR_MAX+'.png}')
                f.write('\n\\end{subfigure}\n')
                f.write('\\vskip\\baselineskip\n')

                f.write('\\begin{subfigure}[b]{0.49\\textwidth}\n\centering\n')
                f.write('\\includegraphics[trim=90 60 70 10,clip,width=\\textwidth]{/scratch/vportge/plots/Python_Indices/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+INAME+'_2005-2015_map_of_trend_'+REGION+'.png}')
                f.write('\n\\end{subfigure}\n\hfill\n')

                f.write('\\begin{subfigure}[b]{0.49\\textwidth}\n\centering\n')
                f.write('\\includegraphics[trim=90 60 70 10,clip,width=\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+INAME+'_2005-2015_map_of_trend_'+REGION+'_'+MIN_OR_MAX+'.png}')
                f.write('\n\\end{subfigure}\n')

                f.write('\caption[]\n{\small '+INAME+' }\n \label{fig:'+INAME+'_'+MIN_OR_MAX +'_'+REGION+'}\n')
                f.write('\\end{figure}')
                '''

            for i in range(len(climpact_indices)):
                ICLIMP = climpact_indices[i]
                IGHCNDEX = ghcndex_climpact_indices[i]  
                
                f.write('\n\n\n')
                f.write('\\begin{figure}\n')
                f.write('\\includegraphics[trim=70 40 55 10,clip,width=0.49\\textwidth]{"/scratch/vportge/plots/Climpact/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+ICLIMP+'_CM SAF_map_averaged_'+REGION+'"}')
                f.write('\\includegraphics[trim=70 40 55 10,clip,width=0.49\\textwidth]{"/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+IGHCNDEX+'_GHCNDEX_map_averaged_'+REGION+'"}')
                f.write('\n\caption[]\n{\small '+IGHCNDEX+' }\n \label{fig:average_'+IGHCNDEX+'_'+MIN_OR_MAX +'}\n')
                f.write('\\end{figure}')
                '''

                f.write('\n\n\n')
                f.write('\\begin{figure}\n')
                f.write('\\includegraphics[trim=0 0 0 0 ,clip,width=0.49\\textwidth]{/scratch/vportge/plots/Climpact/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+ICLIMP+'_with_trend_ANN_'+REGION+'.png}')
                f.write('\\includegraphics[trim=0 0 0 0 ,clip,width=0.49\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+IGHCNDEX+'_time_series_GHCNDEX_with_trend_annually_'+REGION+'.png}')
                f.write('\\vskip\\baselineskip\n')

                f.write('\\begin{subfigure}[b]{0.49\\textwidth}\n\centering\n')
                f.write('\\includegraphics[trim=90 60 70 10,clip,width=\\textwidth]{/scratch/vportge/plots/Climpact/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+ICLIMP+'_1991-2004_map_of_trend_'+REGION+'.png}')
                f.write('\n\\end{subfigure}\n\hfill\n')

                f.write('\\begin{subfigure}[b]{0.49\\textwidth}\n\centering\n')
                f.write('\\includegraphics[trim=90 60 70 10,clip,width=\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+IGHCNDEX+'_1991-2004_map_of_trend_'+REGION+'_'+MIN_OR_MAX+'.png}')
                f.write('\n\\end{subfigure}\n')
                f.write('\\vskip\\baselineskip\n')

                f.write('\\begin{subfigure}[b]{0.49\\textwidth}\n\centering\n')
                f.write('\\includegraphics[trim=90 60 70 10,clip,width=\\textwidth]{/scratch/vportge/plots/Climpact/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+ICLIMP+'_2005-2015_map_of_trend_'+REGION+'.png}')
                f.write('\n\\end{subfigure}\n\hfill\n')

                f.write('\\begin{subfigure}[b]{0.49\\textwidth}\n\centering\n')
                f.write('\\includegraphics[trim=90 60 70 10,clip,width=\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+IGHCNDEX+'_2005-2015_map_of_trend_'+REGION+'_'+MIN_OR_MAX+'.png}')
                f.write('\n\\end{subfigure}\n')

                f.write('\caption[]\n{\small '+IGHCNDEX+' }\n \label{fig:'+IGHCNDEX+'_'+MIN_OR_MAX +'_'+REGION+'}\n')
                f.write('\\end{figure}')
                '''



    with open('longer_warm_window_'+MIN_OR_MAX+'.txt', 'w') as f:

        for REGION in REGIONS:
            f.write('\n\FloatBarrier\n\subsection{'+REGION+'}')
            for INAME in python_indices:
                MIN_OR_MAX_PYT = 'max'
                
                f.write('\n\n\n')
                f.write('\\begin{figure}\n')
                f.write('\\includegraphics[trim=70 40 55 10,clip,width=0.49\\textwidth]{"/scratch/vportge/plots/warm_window_10_3/Python_Indices/'+MIN_OR_MAX_PYT+'_LST_in_cold_window/'+REGION+'/'+INAME+'_CM SAF_map_averaged_'+REGION+'"}')
                f.write('\\includegraphics[trim=70 40 55 10,clip,width=0.49\\textwidth]{"/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+INAME+'_GHCNDEX_map_averaged_'+REGION+'"}')
                f.write('\n\caption[]\n{\small '+INAME+' }\n \label{fig:average_'+INAME+'_'+MIN_OR_MAX +'}\n')
                f.write('\\end{figure}')
                '''

                f.write('\n\n\n')
                f.write('\\begin{figure}\n')
                f.write('\\includegraphics[trim=0 0 0 0 ,clip,width=0.49\\textwidth]{/scratch/vportge/plots/warm_window_10_3/Python_Indices/'+MIN_OR_MAX_PYT+'_LST_in_cold_window/'+REGION+'/'+INAME+'_with_trend_ANN_'+REGION+'.png}')
                f.write('\\includegraphics[trim=0 0 0 0 ,clip,width=0.49\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+INAME+'_time_series_GHCNDEX_with_trend_annually_'+REGION+'.png}')
                f.write('\\vskip\\baselineskip\n')

                f.write('\\begin{subfigure}[b]{0.49\\textwidth}\n\centering\n')
                f.write('\\includegraphics[trim=90 60 70 10,clip,width=\\textwidth]{/scratch/vportge/plots/warm_window_10_3/Python_Indices/'+MIN_OR_MAX_PYT+'_LST_in_cold_window/'+REGION+'/'+INAME+'_1991-2004_map_of_trend_'+REGION+'.png}')
                f.write('\n\\end{subfigure}\n\hfill\n')

                f.write('\\begin{subfigure}[b]{0.49\\textwidth}\n\centering\n')
                f.write('\\includegraphics[trim=90 60 70 10,clip,width=\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+INAME+'_1991-2004_map_of_trend_'+REGION+'_'+MIN_OR_MAX+'.png}')
                f.write('\n\\end{subfigure}\n')
                f.write('\\vskip\\baselineskip\n')

                f.write('\\begin{subfigure}[b]{0.49\\textwidth}\n\centering\n')
                f.write('\\includegraphics[trim=90 60 70 10,clip,width=\\textwidth]{/scratch/vportge/plots/warm_window_10_3/Python_Indices/'+MIN_OR_MAX_PYT+'_LST_in_cold_window/'+REGION+'/'+INAME+'_2005-2015_map_of_trend_'+REGION+'.png}')
                f.write('\n\\end{subfigure}\n\hfill\n')

                f.write('\\begin{subfigure}[b]{0.49\\textwidth}\n\centering\n')
                f.write('\\includegraphics[trim=90 60 70 10,clip,width=\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+INAME+'_2005-2015_map_of_trend_'+REGION+'_'+MIN_OR_MAX+'.png}')
                f.write('\n\\end{subfigure}\n')

                f.write('\caption[]\n{\small '+INAME+' }\n \label{fig:'+INAME+'_'+MIN_OR_MAX +'_'+REGION+'}\n')
                f.write('\\end{figure}')
                '''

            for i in range(len(climpact_indices)):
                ICLIMP = climpact_indices[i]
                IGHCNDEX = ghcndex_climpact_indices[i]  
                
                f.write('\n\n\n')
                f.write('\\begin{figure}\n')
                f.write('\\includegraphics[trim=70 40 55 10,clip,width=0.49\\textwidth]{"/scratch/vportge/plots/warm_window_10_3/Climpact/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+ICLIMP+'_CM SAF_map_averaged_'+REGION+'"}')
                f.write('\\includegraphics[trim=70 40 55 10,clip,width=0.49\\textwidth]{"/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+IGHCNDEX+'_GHCNDEX_map_averaged_'+REGION+'"}')
                f.write('\n\caption[]\n{\small '+IGHCNDEX+' }\n \label{fig:average_'+IGHCNDEX+'_'+MIN_OR_MAX +'}\n')
                f.write('\\end{figure}')
                '''

                f.write('\n\n\n')
                f.write('\\begin{figure}\n')
                f.write('\\includegraphics[trim=0 0 0 0 ,clip,width=0.49\\textwidth]{/scratch/vportge/plots/warm_window_10_3/Climpact/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+ICLIMP+'_with_trend_ANN_'+REGION+'.png}')
                f.write('\\includegraphics[trim=0 0 0 0 ,clip,width=0.49\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+IGHCNDEX+'_time_series_GHCNDEX_with_trend_annually_'+REGION+'.png}')
                f.write('\\vskip\\baselineskip\n')

                f.write('\\begin{subfigure}[b]{0.49\\textwidth}\n\centering\n')
                f.write('\\includegraphics[trim=90 60 70 10,clip,width=\\textwidth]{/scratch/vportge/plots/warm_window_10_3/Climpact/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+ICLIMP+'_1991-2004_map_of_trend_'+REGION+'.png}')
                f.write('\n\\end{subfigure}\n\hfill\n')

                f.write('\\begin{subfigure}[b]{0.49\\textwidth}\n\centering\n')
                f.write('\\includegraphics[trim=90 60 70 10,clip,width=\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+IGHCNDEX+'_1991-2004_map_of_trend_'+REGION+'_'+MIN_OR_MAX+'.png}')
                f.write('\n\\end{subfigure}\n')
                f.write('\\vskip\\baselineskip\n')

                f.write('\\begin{subfigure}[b]{0.49\\textwidth}\n\centering\n')
                f.write('\\includegraphics[trim=90 60 70 10,clip,width=\\textwidth]{/scratch/vportge/plots/warm_window_10_3/Climpact/'+MIN_OR_MAX+'_LST_in_cold_window/'+REGION+'/'+ICLIMP+'_2005-2015_map_of_trend_'+REGION+'.png}')
                f.write('\n\\end{subfigure}\n\hfill\n')

                f.write('\\begin{subfigure}[b]{0.49\\textwidth}\n\centering\n')
                f.write('\\includegraphics[trim=90 60 70 10,clip,width=\\textwidth]{/scratch/vportge/plots/GHCNDEX/'+REGION+'/'+IGHCNDEX+'_2005-2015_map_of_trend_'+REGION+'_'+MIN_OR_MAX+'.png}')
                f.write('\n\\end{subfigure}\n')

                f.write('\caption[]\n{\small '+IGHCNDEX+' }\n \label{fig:'+IGHCNDEX+'_'+MIN_OR_MAX +'_'+REGION+'}\n')
                f.write('\\end{figure}')
                '''
