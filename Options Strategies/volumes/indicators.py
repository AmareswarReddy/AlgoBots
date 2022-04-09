#%%
import numpy as np
def indicators(data):
    def EMA(data,a):
        data['MAC'] = 0
        close = data['Close'].copy()
        ema = data['MAC'].copy()
        ema.iloc[a-1] = close.iloc[0:a].sum()/a
        for i in range(a,ema.size):
            ema.iloc[i]=(close.iloc[i]-ema.iloc[i-1])*(2/(a+1))+ema.iloc[i-1]
        del data['MAC']
        return ema         
    def macd_signal(data):
        data['MACD_signal'] = 0
        close = data['MACD'].copy()
        macd_signal = data['MACD_signal'].copy()
        macd_signal.iloc[50-1] = close.iloc[41:50].sum()/9
        for i in range(50,macd_signal.size):
            macd_signal.iloc[i]=(close.iloc[i]-macd_signal.iloc[i-1])*(2/(9+1))+macd_signal.iloc[i-1]
        return macd_signal
    def RSI(data,period):
        data['RSI'] = 0
        data['aa']=0
        close = data['Close'].copy()
        rsi = data['RSI'].copy()
        aa = data['aa'].copy()
        aa.iloc[1:]=close.iloc[:-1]
        bb=close-aa
        bb.iloc[0]=0
        i=period+1
        first_14= bb.iloc[i-period:i]
        U = first_14.loc[first_14>0].sum()
        U_count = len(first_14.loc[first_14>0])
        L = first_14.loc[first_14<0].sum()
        L_count = len(first_14.loc[first_14<0])
        U_average = U/U_count
        L_average = -L/L_count
        k = (U_average)/(L_average)
        rsi.iloc[i] = 100-(100/(1+k))
        for i in range(16,close.size):
            last= bb.iloc[i]
            U_new = last*(last>0)
            L_new = last*(last<0)
            U_average = (U_average*(period-1)+U_new)/period
            L_average = (L_average*(period-1)-L_new)/period
            k = (U_average)/(L_average)
            rsi.iloc[i] = 100-(100/(1+k))
        del data['aa']
        return rsi
    def MFI(data):
        data['MFI'] = 0
        data['aa']=0
        close = data['Close'].copy()  # only volume now
        mfi = data['MFI'].copy()
        aa = data['aa'].copy()
        aa.iloc[1:]=close.iloc[:-1]
        bb=(close-aa)
        bb.iloc[0]=0 
        bb=bb*data['Volume'] #bb in the place of 1 for volume*close
        i=15
        first_14= bb.iloc[i-14:i]
        U = first_14.loc[first_14>0].sum()
        U_count = len(first_14.loc[first_14>0])
        L = first_14.loc[first_14<0].sum()
        L_count = len(first_14.loc[first_14<0])
        U_average = U/U_count
        L_average = -L/L_count
        k = (U_average)/(L_average)
        mfi.iloc[i] = 100-(100/(1+k))
        for i in range(16,close.size):
            last= bb.iloc[i]
            U_new = last*(last>0)
            L_new = last*(last<0)
            U_average = (U_average*13+U_new)/14
            L_average = (L_average*13-L_new)/14
            k = (U_average)/(L_average)
            mfi.iloc[i] = 100-(100/(1+k))
        del data['aa']
        return mfi
    def SMA(data,a):
        data['SMAC'] = 0
        close = data['Close'].copy()
        sma = data['SMAC'].copy()
        for i in range(a,sma.size):
            sma.iloc[i] = close.iloc[i-a+1:i+1].sum()/a
        del data['SMAC']
        return sma
    def ICHIMOKU(data):
        data['ICHIMOKU_TEN'] = 0 #9 DAYS (HIGH+LOW)/2
        data['ICHIMOKU_KIN'] = 0 #26 DAYS (HIGH+LOW)/2
        data['ICHIMOKU_TREND']=0 # CURRENT PRICE AT -26 DAYS
        data['ICHIMOKU_L1'] = 0  #(TEN+KIN)/2 AT +26 DAYS
        data['ICHIMOKU_L2']=0 # 52 DAYS (HIGH+LOW)/2 AT +26 DAYS
        for i in range(80,len(data['Close'])):
            data['ICHIMOKU_TEN'].iloc[i] = (data['High'].iloc[i-9:i].max()+data['Low'].iloc[i-9:i].min())/2
            data['ICHIMOKU_KIN'].iloc[i] = (data['High'].iloc[i-26:i].max()+data['Low'].iloc[i-26:i].min())/2
            data['ICHIMOKU_TREND'].iloc[i-26]= data['Close'].iloc[i]
            data['ICHIMOKU_L1'].iloc[i] = data['ICHIMOKU_TEN'].iloc[i-26]+data['ICHIMOKU_KIN'].iloc[i-26]
            data['ICHIMOKU_L2'].iloc[i] = (data['High'].iloc[i-52-26:i-26].max()+data['Low'].iloc[i-52-26:i-26].min())/2
        return data
    def  ELDER_IMPULSE(data):
        data['MA'] = 0
        close = data['Close'].copy()
        impulse = data['MA'].copy()
        e1=EMA(data,13)
        mh1=data['MACD_hist'].copy()
        for i in range(100,len(close)):
            if ((e1.iloc[i]>e1.iloc[i-1])and(mh1.iloc[i]>mh1.iloc[i-1])):
                impulse.iloc[i] = 1
            elif ((e1.iloc[i]<e1.iloc[i-1])and(mh1.iloc[i]<mh1.iloc[i-1])):
                impulse.iloc[i] = -1
            else:
                impulse.iloc[i] = 0
        del data['MA']
        return impulse
    def OBV(data):
        data['M'] = 0
        close = data['Close'].copy()
        volume=data['Volume'].copy()
        obv = data['M'].copy()
        obv.iloc[0]=0
        for i in range(1,len(close)):
            if (close.iloc[i-1]>close.iloc[i]):
                obv.iloc[i]=obv.iloc[i-1]-volume.iloc[i]
            elif(close.iloc[i-1]<close.iloc[i]):
                obv.iloc[i]=obv.iloc[i-1]+volume.iloc[i]
            else:
                obv.iloc[i]=obv.iloc[i-1]
        del data['M']
        return obv
    def ATR(data,a):
        data['TR'] = 0
        data['ATR'] = 0
        close = data['Close'].copy()
        high = data['High'].copy()
        low = data['Low'].copy()
        tr = data['TR'].copy()
        atr = data['ATR'].copy()
        for i in range(1,len(close)):
            tr.iloc[i] = max([abs(high.iloc[i]-low.iloc[i]),abs(high.iloc[i]-close.iloc[i-1]),abs(low.iloc[i]-close.iloc[i-1])])
        for i in range(a+1,len(close)):
            atr.iloc[i] = ((atr.iloc[i-1]*(a-1))+tr.iloc[i])/a
        del data['TR']
        return atr
    def VORTEX(data): #along with sma
        data['+VM'] = 0
        data['-VM'] = 0
        data['+VM14'] =0
        data['-VM14'] =0
        data['TR'] = 0
        close = data['Close'].copy()
        high = data['High'].copy()
        low = data['Low'].copy()
        tr = data['TR'].copy()
        for i in range(1,len(close)):
            tr.iloc[i] = max([abs(high.iloc[i]-low.iloc[i]),abs(high.iloc[i]-close.iloc[i-1]),abs(low.iloc[i]-close.iloc[i-1])])
        for i in range(1,len(data['Close'])):
            data['+VM'].iloc[i] = abs(data['High'].iloc[i]-data['Low'].iloc[i-1])
            data['-VM'].iloc[i] = abs(data['Low'].iloc[i]-data['High'].iloc[i-1])
        for i in range(20,len(data['Close'])):
            data['+VM14'].iloc[i] = data['+VM'].iloc[i-14:i].sum()/ tr.iloc[i-14:i].sum()
            data['-VM14'].iloc[i] = data['-VM'].iloc[i-14:i].sum()/ tr.iloc[i-14:i].sum()
        del data['+VM']
        del data['-VM']
        del data['TR']
        return data
    def RSI_DIVERGANCE(data,min_cp,min_r,max_cp,max_r,div_len):
        data['RSI_D'] = 0
        rsi_div = data['RSI_D'].copy()
        price_lows =[]
        rsi_lows = []
        # price_lows
        for i in range(0,data['Close'].size):
            if ((i==0) and (data['Close'].iloc[i]<data['Close'].iloc[i+1])):
                price_lows.append(data['Close'].iloc[i])
            elif ((i==data['Close'].size-1) and (data['Close'].iloc[i]<data['Close'].iloc[i-1])):
                price_lows.append(data['Close'].iloc[i])
            elif (data['Close'].iloc[i-1]>data['Close'].iloc[i]<data['Close'].iloc[i+1]):
                price_lows.append(data['Close'].iloc[i])
            else:
                price_lows.append(-1)
        # rsi_lows
        for i in range(0,data['RSI'].size):
            if ((i==0) and (data['RSI'].iloc[i]<data['RSI'].iloc[i+1])):
                rsi_lows.append(data['RSI'].iloc[i])
            elif ((i==data['RSI'].size-1) and (data['RSI'].iloc[i]<data['RSI'].iloc[i-1])):
                rsi_lows.append(data['RSI'].iloc[i])
            elif (data['RSI'].iloc[i-1]>data['RSI'].iloc[i]<data['RSI'].iloc[i+1]):
                rsi_lows.append(data['RSI'].iloc[i])
            else:
                rsi_lows.append(-1)
        min_prices=[]
        min_rsi=[]
        for i in range(0,len(price_lows)):
            if ((-1<price_lows[i]<min_cp)and(-1<rsi_lows[i]<min_r)):
                min_prices.append(price_lows[i])
                min_rsi.append(rsi_lows[i])
            else:
                min_prices.append(-1)
                min_rsi.append(-1)
        min_prices=np.array(min_prices)
        min_rsi=np.array(min_rsi)
        div_len=int(div_len)
        for i in range(div_len,len(price_lows)):
            lp=min_prices[i-div_len:i][min_prices[i-div_len:i]>-1]
            lr=min_rsi[i-div_len:i][min_rsi[i-div_len:i]>-1]
            if len(lp)>1:
                if ((lp[-1]<lp[0]) and (lr[-1]>lr[0])):
                    rsi_div.iloc[i-1]=1
                
        #price_highs
        price_highs =[]
        rsi_highs = []
        for i in range(0,data['Close'].size):
            if ((i==0) and (data['Close'].iloc[i]>data['Close'].iloc[i+1])):
                price_highs.append(data['Close'].iloc[i])
            elif ((i==data['Close'].size-1) and (data['Close'].iloc[i]>data['Close'].iloc[i-1])):
                price_highs.append(data['Close'].iloc[i])
            elif (data['Close'].iloc[i-1]<data['Close'].iloc[i]>data['Close'].iloc[i+1]):
                price_highs.append(data['Close'].iloc[i])
            else:
                price_highs.append(9999)
        # rsi_highs
        for i in range(0,data['RSI'].size):
            if ((i==0) and (data['RSI'].iloc[i]>data['RSI'].iloc[i+1])):
                rsi_highs.append(data['RSI'].iloc[i])
            elif ((i==data['RSI'].size-1) and (data['RSI'].iloc[i]>data['RSI'].iloc[i-1])):
                rsi_highs.append(data['RSI'].iloc[i])
            elif (data['RSI'].iloc[i-1]<data['RSI'].iloc[i]>data['RSI'].iloc[i+1]):
                rsi_highs.append(data['RSI'].iloc[i])
            else:
                rsi_highs.append(101)
        max_prices=[]
        max_rsi=[]
        for i in range(0,len(price_highs)):
            if ((9999>price_highs[i]>max_cp)and(101>rsi_highs[i]>max_r)):
                max_prices.append(price_highs[i])
                max_rsi.append(rsi_highs[i])
            else:
                max_prices.append(9999)
                max_rsi.append(101)
        max_prices=np.array(max_prices)
        max_rsi=np.array(max_rsi)
        for i in range(div_len,len(price_highs)):
            hp=max_prices[i-div_len:i][max_prices[i-div_len:i]<9999]
            hr=max_rsi[i-div_len:i][max_rsi[i-div_len:i]<101]
            if len(hp)>1:
                if ((hp[-1]>hp[0]) and (hr[-1]<hr[0])):
                    rsi_div.iloc[i-1]=-1
        return rsi_div
    data['MFI'] = MFI(data)
    data['RSI']=RSI(data,9)
    data['EMA200'] = EMA(data,200)
    data['OBV'] = OBV(data)
    data['ATR'] = ATR(data,14)
    data = VORTEX(data)
    #data['RSI_D'] =  RSI_DIVERGANCE(data,min_cp=200,min_r=30,max_cp=0,max_r=70,div_len=10)    
    return data  

# %%
