#%%
import re
import os
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.interpolate
from pyswarm import pso
from scipy import interpolate
#input
list_of_files=os.listdir('optionsdata/')
#list_of_files=['2023-03-23WEEKLY-expiry_data_BNF_Options.csv']
for filename in list_of_files:
    if True:
        try:
            data=pd.read_csv("optionsdata/"+filename)
            def blue_factor(option_chain,x):
                final_chain=option_chain[(option_chain['StrikeRate']>x-1000) & (option_chain['StrikeRate']<x+1000)]
                strikes=final_chain['StrikeRate']
                p_lastrates=final_chain['LastRate_PE']
                c_lastrates=final_chain['LastRate_CE']
                f_p = interpolate.interp1d(strikes, p_lastrates,kind='quadratic')
                f_c = interpolate.interp1d(strikes, c_lastrates,kind='quadratic')
                return (f_p(x)+f_c(x))/2
    
    
            def triple_indicator(option_chain,x,cv,pv,coi,poi,day_cv,day_pv,day_coi,day_poi,earlier_coi,earlier_poi):
                p_strikerates=np.array(list(option_chain['StrikeRate']))
                c_strikerates=np.array(list(option_chain['StrikeRate']))
                p_lastrate=np.array(list(option_chain['LastRate_PE']))
                c_lastrate=np.array(list(option_chain['LastRate_CE']))
                p_openinterest=np.array(list(option_chain['OpenInterest_PE']))
                c_openinterest=np.array(list(option_chain['OpenInterest_CE']))
                c_volume=np.sum(np.multiply(np.array(list(option_chain['Volume_CE'])),c_lastrate))
                p_volume=np.sum(np.multiply(np.array(list(option_chain['Volume_PE'])),p_lastrate))
                average_p_strike=np.dot(p_strikerates,p_openinterest)/np.sum(p_openinterest)
                average_c_strike=np.dot(c_strikerates,c_openinterest)/np.sum(c_openinterest)
                p1=x-average_p_strike
                c1=average_c_strike-x
                i=np.array(option_chain['StrikeRate'])[0]
                end=np.array(option_chain['StrikeRate'])[-1]
                ss=np.array(option_chain['StrikeRate'])
                def loss_function(v):
                    init_pe=np.dot(p_lastrate,p_openinterest)
                    init_ce=np.dot(c_lastrate,c_openinterest)
                    tmax=ss-v[0]
                    tmax[tmax<0]=0
                    tmin=v[0]-ss
                    tmin[tmin<0]=0
                    end_pe=np.dot(p_openinterest,tmax)
                    end_ce=np.dot(c_openinterest,tmin)
                    data=init_ce-end_ce-init_pe+end_pe
                    return abs(data)
                a,b=pso(func=loss_function,lb=[i],ub=[end],minfunc=0.1)
                x1=x-np.round_(a[0],1)
                factor5=blue_factor(option_chain,x)
    
    
                p_open=np.sum(np.array(list(option_chain['OpenInterest_PE'])))
                c_open=np.sum(np.array(list(option_chain['OpenInterest_CE'])))
                p_oi_change=p_open-earlier_poi
                c_oi_change=c_open-earlier_coi
                c_oi=np.sum(np.multiply(c_oi_change,c_lastrate))
                p_oi=np.sum(np.multiply(p_oi_change,p_lastrate))
                earlier_coi=c_open
                earlier_poi=p_open
    
    
    
                oi_ratio=p_open/c_open
                pp=p_lastrate[np.multiply(p_lastrate!=0, p_openinterest!=0)]
                po=p_openinterest[np.multiply(p_lastrate!=0, p_openinterest!=0)]
                cp=c_lastrate[np.multiply(c_lastrate!=0, c_openinterest!=0)]
                co=c_openinterest[np.multiply(c_lastrate!=0, c_openinterest!=0)]
                a1=np.dot(np.array(pp),np.array(po))
                a2=np.dot(np.array(cp),np.array(co))
                b1=np.dot(np.array(pp),1/np.array(po))
                b2=np.dot(np.array(cp),1/np.array(co))
                aa=a1/a2
                bb=b1/b2
                hightime_indicator= ((2*(c1/p1)*(c1/p1))/(1+(c1/p1)*(c1/p1)))-1
                rosetta_indicator=x1/factor5
                cv,pv=cv+c_volume,pv+p_volume        
                coi,poi=coi+c_oi,poi+p_oi   
                day_cv,day_pv=day_cv+c_volume,day_pv+p_volume
                day_coi,day_poi=day_coi+c_oi,day_poi+p_oi    
                day_cc=day_cv/day_pv
                day_uu=day_coi/day_poi     
                cc=cv/pv
                uu=coi/poi
                volume_indicator=((2*cc*cc)/(1+cc*cc))-1
                day_volume_indicator=((2*day_cc*day_cc)/(1+day_cc*day_cc))-1
                oi_davat=((2*uu*uu)/(1+uu*uu))-1
                day_oi_davat=((2*day_uu*day_uu)/(1+day_uu*day_uu))-1
                rosetta_ratio_indicator=((2*aa*aa)/(1+aa*aa))-1
                lt=np.sum(c_lastrate)/np.sum(p_lastrate)
                #market_ripper_indicator=((2*bb*bb)/(1+bb*bb))-1
                oi_ratio_indicator=((2*oi_ratio*oi_ratio)/(1+oi_ratio*oi_ratio))-1
                final=oi_davat
                final1=hightime_indicator
                final2=oi_ratio_indicator
                final3=rosetta_ratio_indicator
                final4=rosetta_indicator
                final5=volume_indicator
                final6=day_volume_indicator
                final7=day_oi_davat
                final8=((2*lt*lt)/(1+lt*lt))-1
                return  final,final1,final2,final3,final4,final5,final6,final7,final8,cv,pv,coi,poi,day_cv,day_pv,day_coi,day_poi,earlier_coi,earlier_poi
    
    
            def time_to_sec(index):
                a=index[11:]
                u=a.split(':')
                return int(u[0])*60*60+int(u[1])*60-33300
    
            def days_sort(days):
                order=[]
                for i in range(0,len(days)):
                    high=days[i].split('-')
                    order+=[int(high[0])+int(high[1])*30+int(high[2])*360]
                    f=max(order)-np.array(order)
                return f 
    
            list_of_times=[0]
            for i in range(0,375):
                list_of_times+=[list_of_times[-1]+60]


            def data_modifier(filename):
                #print(filename)
                df = filename
                df_banknifty = df[df['Ticker'].str.contains('BANKNIFTY')]
                df_banknifty_lastrate = df_banknifty[df_banknifty['Ticker'] == 'BANKNIFTY']
                df_banknifty_options = df_banknifty[df_banknifty['Ticker'].str.contains('BANKNIFTYWK')]
                from datetime import datetime, date, time
                df_banknifty_options['date_only'] = df_banknifty_options['Date/Time'].apply(lambda date:str(datetime.strptime(date, "%d-%m-%Y %H:%M:%S").date()))
                df_banknifty_grouped_by_time = df_banknifty_options.groupby(['date_only'])
                list_dts_str = list(df_banknifty_grouped_by_time.groups.keys())
                ##Get list of dates
                from datetime import datetime, date, time
                list_dates = list(set(map(lambda date:datetime.strptime(date, "%Y-%m-%d").date() , list_dts_str)))
                max_date = max(list_dates)
                print(max_date)
                final_df_list = []
                days_sort = []
                for group in df_banknifty_grouped_by_time.groups:
                    #current_iter_datetime  = datetime.strptime(group, "%d-%m-%Y %H:%M:%S")
                    current_iter_date = datetime.strptime(group, "%Y-%m-%d").date()
                    start_time = datetime.combine(current_iter_date,time(9,15))
                    days = max_date - current_iter_date
                    #seconds = current_iter_datetime - start_time
                    df = df_banknifty_grouped_by_time.get_group(group)
                    df['day'] = days.days
                    days_sort.append(days.days)
                    df['seconds'] = df['Date/Time'].apply(lambda date : (datetime.strptime(date, "%d-%m-%Y %H:%M:%S") - start_time).seconds)
                    df['CPType'] = df['Ticker'].apply(lambda x: 'CE' if 'CE' in x else 'PE')
                    df['StrikeRate'] = df[['Ticker', 'CPType']].apply(lambda x:int(x[0].split("WK")[1].split(x[1])[0]), axis=1)
                    df.rename(columns={'Close':'LastRate'}, inplace=True)
                    #df['CurrentStrike_BN'] =  df_banknifty_lastrate[df_banknifty_lastrate['Date/Time'] == group]
                    #df['CurrentStrike_BN'] = df_banknifty_lastrate[df_banknifty_lastrate['Date/Time'] == group]
                    #print("Starting new")
                    #print(len(df))
                    df = pd.merge(df, df_banknifty_lastrate[['Date/Time', 'Close']], on = 'Date/Time', how = 'inner')
                    #print(len(df))
                    df['expiry'] = max_date
                    df.reset_index(drop=True, inplace=True)
                    df = df.drop(columns=['Ticker', 'Open', 'High', 'Low', 'date_only', 'Date/Time'])
                    columns_rename = {'Close':'lastrate','Open Interest':'OpenInterest'}
                    df.rename(columns=columns_rename, inplace=True)
                    df.drop_duplicates()
                    columns_rename_ce = {'Volume':'Volume_CE', 'OpenInterest':'OpenInterest_CE', 'LastRate':'LastRate_CE'}
                    columns_rename_pe = {'Volume':'Volume_PE', 'OpenInterest':'OpenInterest_PE', 'LastRate':'LastRate_PE'}
                    ce_data = df[df['CPType'] == 'CE']
                    ce_data.rename(columns=columns_rename_ce, inplace=True)
                    print('Starting a iteration')
                    print(len(ce_data))
                    pe_data = df[df['CPType'] == 'PE']
                    pe_data.rename(columns=columns_rename_pe, inplace=True)
                    print(len(pe_data))
                    print(len(df))
                    df_merged = pd.merge(ce_data,pe_data, on = ['day', 'seconds','StrikeRate', 'lastrate', 'expiry'], how='outer')
                    print(len(df_merged))
                    df_merged.fillna(0, inplace=True)
                    final_df_list.append(df_merged)
                return final_df_list, days_sort,str(max_date)





            def data_modifier2(data):
                h=[*set(list(data['Date/Time']))]
                ok=[]
                for i in range(0,len(h)):
                    ok+=[h[i][:10]]
                days=[*set(ok)]
                index=list(data['Date/Time'])
                final_day_sort=days_sort(days)
                expiry=days[np.argmin(final_day_sort)]
                distinct_data_sets=[]
                for i in range(0,len(days)):
                    filter_index=[]
                    for r in range(0,len(index)):
                        if days[i] in index[r]:
                            filter_index+=[True]
                        else:
                            filter_index+=[False]
                    day_data=data.loc[filter_index]
                    aa={"Volume_CE":[],	"OpenInterest_CE":[],	"LastRate_CE":[],	"StrikeRate":[],	"LastRate_PE":[],	"OpenInterest_PE":[],	"Volume_PE":[],	"expiry":[],	"day":[],	"seconds":[],	"lastrate":[]}
                    day_index=list(np.array(index)[filter_index])
                    pp=[]
                    for j in day_index:
                        pp+=[time_to_sec(j)]
                    seconds_index=np.array(pp)
                    for j in range(0,len(list_of_times)):
                        at_the_time_data=day_data[seconds_index==list_of_times[j]]
                        b_lastrate=at_the_time_data[at_the_time_data['Ticker']=='BANKNIFTY']['Close']
                        if len(b_lastrate)!=0:
                            at_the_time_data=at_the_time_data[at_the_time_data['Open Interest']!=0]
                            at_index=[]
                            for k in range(0,len(at_the_time_data)):
                                if "BANKNIFTY" in list(at_the_time_data['Ticker'])[k] and "E" in list(at_the_time_data['Ticker'])[k]:
                                    at_index+=[True]
                                else:
                                    at_index+=[False]
                            at_the_time_data=at_the_time_data.loc[at_index]
                            strikerate_list=[]
                            hi=list(at_the_time_data['Ticker'])
                            for g in range(0,len(at_the_time_data)):
                                strikerate_list+=[int(re.findall('\d+', hi[g])[0])]
                            def strike_index(strikerate,strike):
                                indexer=[]
                                for a in range(0,len(strikerate)):
                                    if strikerate[a]==strike:
                                        indexer+=[True]
                                    else:
                                        indexer+=[False]
                                return indexer
                            for k in range(0,len(strikerate_list)):
                                req_data=pd.DataFrame(at_the_time_data.loc[strike_index(strikerate_list,strikerate_list[k])])
                                for v in range(0,len(req_data)):
                                    ce_volume,ce_oi,ce_lastrate,pe_volume,pe_oi,pe_lastrate=[0],[0],[0],[0],[0],[0]
                                    if "CE" in list(req_data['Ticker'])[v] :
                                        ce_volume=req_data['Volume']
                                        ce_oi=req_data['Open Interest']
                                        ce_lastrate=req_data['Close']
                                    elif "PE" in list(req_data['Ticker'])[v] :
                                        pe_volume=req_data['Volume']
                                        pe_oi=req_data['Open Interest']
                                        pe_lastrate=req_data['Close']
                                    aa["Volume_CE"]+=[int(list(ce_volume)[0])]
                                    aa["OpenInterest_CE"]+=[int(list(ce_oi)[0])]
                                    aa["LastRate_CE"]+=[float(list(ce_lastrate)[0])]
                                    aa["StrikeRate"]+=[strikerate_list[k]]
                                    aa["LastRate_PE"]+=[float(list(pe_lastrate)[0])]
                                    aa["OpenInterest_PE"]+=[int(list(pe_oi)[0])]
                                    aa["Volume_PE"]+=[int(list(pe_volume)[0])]
                                    aa["expiry"]+=[expiry]
                                    aa["day"]+=[final_day_sort[i]]
                                    aa["seconds"]+=[list_of_times[j]]
                                    aa["lastrate"]+=[float(list(b_lastrate)[0])]
                    yoo=pd.DataFrame(aa).drop_duplicates()
                    distinct_data_sets+=[yoo]
                for temp in range(0,len(distinct_data_sets)):
                    sg=[]
                    for temp2 in distinct_data_sets[temp].index:
                        current_lastrate=float(distinct_data_sets[temp].loc[temp2]['lastrate'])
                        current_strike=int(distinct_data_sets[temp].loc[temp2]['StrikeRate'])
                        call_lastrate=float(distinct_data_sets[temp].loc[temp2]['LastRate_CE'])
                        put_lastrate=float(distinct_data_sets[temp].loc[temp2]['LastRate_PE'])
                        if call_lastrate!=0 and put_lastrate==0: 
                            if current_strike>=current_lastrate:
                                if abs(current_lastrate-current_strike)>call_lastrate:
                                    sg+=[True]
                                else:
                                    sg+=[False]
                            if current_strike<current_lastrate:
                                if current_lastrate-current_strike<call_lastrate:
                                    sg+=[True]
                                else:
                                    sg+=[False]
    
                        if put_lastrate!=0 and call_lastrate==0:
                            if current_strike>=current_lastrate:
                                if  current_strike-current_lastrate<put_lastrate :
                                        sg+=[True]
                                else:
                                    sg+=[False]
                            if current_strike<current_lastrate:
                                if  abs(current_strike-current_lastrate)>put_lastrate :
                                        sg+=[True]
                                else:
                                    sg+=[False]
                        if call_lastrate!=0 and put_lastrate!=0:
                            if current_strike>=current_lastrate:
                                if  current_strike-current_lastrate<put_lastrate and abs(current_lastrate-current_strike)>call_lastrate :
                                    sg+=[True]
                                else:
                                    sg+=[False]
                            if current_strike<current_lastrate:
                                if  abs(current_strike-current_lastrate)>put_lastrate and current_lastrate-current_strike<call_lastrate :
                                    sg+=[True]
                                else:
                                    sg+=[False]
                        if call_lastrate==0 and put_lastrate==0:
                            sg+=[False]
                    distinct_data_sets[temp]=distinct_data_sets[temp].loc[sg]
                return distinct_data_sets,final_day_sort,expiry
            
            ok,days_list,expiry=data_modifier(data)
            #ok,days_list,expiry=data_modifier(data)
            def sort_index(days_list):
                final=np.zeros(np.shape(days_list))
                for i in range(0,len(final)):
                    b=np.argmax(days_list)
                    final[i]=b
                    days_list[b]=-1
                return final
            days_index=sort_index(days_list)
            if len(days_list) == 5:
                days_index = [0,1,2,3,4]
            elif len(days_list) == 4:
                days_index = [0,1,2,3]
            else:
                days_index = [0,1,2]

            lastrate=[]
            final=[]
            final1=[]
            final2=[]
            final3=[]
            final4=[]
            final5=[]
            final6=[]
            final7=[]
            cv=0
            pv=0
            coi,poi=0,0
            timer=[]
            if len(days_index)>5:
                days_index=days_index[-5:]
            for y in days_index:
                day_cv=0
                day_pv=0
                day_coi=0
                day_poi=0
                aa=ok[int(y)]
                list_of_seconds=sorted([*set(list(aa['seconds']))])
                if len(list_of_seconds)!=0:
                    option_chain=aa[aa['seconds']==list_of_seconds[0]].copy()
                    earlier_poi=np.array(list(option_chain['OpenInterest_PE']))
                    earlier_coi=np.array(list(option_chain['OpenInterest_CE']))
                    for second in list_of_seconds:
                        option_chain=aa[aa['seconds']==second].copy()
                        x=float(option_chain['lastrate'].iloc[0])
                        try:
                            final_,final1_,final2_,final3_,final4_,final5_,final6_,final7_,final8_,cv,pv,coi,poi,day_cv,day_pv,day_coi,day_poi,earlier_coi,earlier_poi=triple_indicator(option_chain,x,cv,pv,coi,poi,day_cv,day_pv,day_coi,day_poi,earlier_coi,earlier_poi)
                        except Exception:                                                                                                       
                            pass
                        final=final+[final_]
                        final1=final1+[final1_]
                        final2=final2+[final2_]
                        final3=final3+[final3_]
                        final4=final4+[final4_]
                        final5+=[final5_]
                        final6+=[final6_]
                        final7+=[final7_]
                        #final8+=[final8_]
                        lastrate+=[option_chain['lastrate'].iloc[0]]
                    timer+=list_of_seconds
            fig, ax_left = plt.subplots()
            ax_right = ax_left.twinx()
            ax_left.plot(lastrate[:], color='blue')
            #ax_left.plot(created_lastrate[:], color='violet')
            ax_right.plot(final, color='red')
            #ax_right.plot(final1, color='white')
            ax_right.plot(final6, color='violet')
            ax_right.plot(final7, color='yellow')
            ax_right.plot(final5, color='orange')
            #ax_left.plot(final_put[1:], color='green')
            #ax_left.plot(final_call[1:], color='red')
            #ax_right.plot(np.array(capture2[:]), color='yellow')
            #ax_right.plot(distance_ratio_indicator[:], color='violet')
            plt.show()
            json_file={'market_ripper':final,'hightime':final1,'oi_ratio':final2,'rosetta_ratio':final3,'rosetta':final4,'day_volume_indicator':final6,'day_market_ripper':final7,'lastrate':lastrate[:],'time':timer,'volume_ind':final5}
            import json
            with open(expiry+".json", "w") as outfile:
                json.dump(json_file,outfile)
        except Exception as er:
            print(er)

# %%
