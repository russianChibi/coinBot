#!/usr/bin/python3
# -*- coding: utf-8 -*-
import config, csv
from binance import  Client,ThreadedWebsocketManager, ThreadedDepthCacheManager
import talib as ta
import matplotlib.pyplot as plt
import numpy as np
from numpy import *  
from datetime import datetime
import pandas as pd
import shrimpy
import yfinance as yf
import numpy
class Strategy:

    def __init__(self, indicator_name, strategy_name, pair, interval, klines,mode1):
        #Name of indicator
#       indicator_name=MACD,RSI,ICHI..
        # strategy_name = folow in src code
        # pair pair in binance: BNBUSDT...
        # interval: time each candles: 1h 1d 1w
        # klines: klines data from  trader.client.get_klines or some thing liske this
        # mode1: 1 = get all spot in the input Data
        #        2 = check if current time is a good spot of not    < only for COMBAT-1 (indicator_name-strategy_name)
        # 
        # indicator_name-strategy_name:
        #             MACD-CROSS**
        #             RSI-7030**
        #                -8020 K NEN DUNG
        #             ICHI-CLOUD**
        #             COMBAT-1: ichi+macd
        self.mode=mode1
        self.indicator = indicator_name
        #Name of strategy being used
        self.strategy = strategy_name
        #Trading pair
        self.pair = pair
        #Trading interval
        self.interval = interval
        #Kline data for the pair on given interval
        self.klines = klines
        #Calculates the indicator
        self.indicator_result = self.calculateIndicator()
        #Uses the indicator to run strategy
        self.strategy_result = self.calculateStrategy()
        if self.strategy_result ==0:
            return 0

    '''
    Calculates the desired indicator given the init parameters
    '''
    def calculateIndicator(self):
        if self.indicator == 'MACD':
            close = [float(entry[4]) for entry in self.klines]
            close_array = np.asarray(close)

            macd, macdsignal, macdhist = ta.MACD(close_array, fastperiod=12, slowperiod=26, signalperiod=9)
            return [macd, macdsignal, macdhist]

        elif self.indicator == 'RSI':
            close = [float(entry[4]) for entry in self.klines]
            close_array = np.asarray(close)

            rsi = ta.RSI(close_array, timeperiod=14)
            return rsi
        elif self.indicator == "BOLBAND":
            df = pd.DataFrame(self.klines,columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Can be ignored'])
            period = 20
            df['SMA']= df['Close'].rolling(window=period).mean()
            df['STD']= df['Close'].rolling(window=period).std()
            df['Upper']= df['SMA']+(df['STD']*2)
            df['Lower']= df['SMA']-(df['STD']*2)
            columnList=['Date', 'Open', 'High', 'Low', 'Close', 'SMA','Upper','Lower']
            bolingerBandsRet = df[columnList].values.tolist()
            return bolingerBandsRet

        elif self.indicator == "ICHI" or self.indicator == "COMBAT":
            # tmpKlines = self.klines
            # for kline in tmpKlines:
            #     kline[0]=datetime.datetime.fromtimestamp(kline[0] / 1e3).strftime("%Y-%m-%d-%H-%M-%S")
                # print(kline[0])
            df = pd.DataFrame(self.klines,columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Can be ignored'])

            del df['Quote asset volume']
            del df['Number of trades']
            del df['Taker buy base asset volume']
            del df['Taker buy quote asset volume']
            del df['Can be ignored']

            # # # Define length of Tenkan Sen or Conversion Line
            cl_period = 9 

            # Define length of Kijun Sen or Base Line
            bl_period = 26  

            # Define length of Senkou Sen B or Leading Span B
            lead_span_b_period = 52  

            # Define length of Chikou Span or Lagging Span
            lag_span_period = 26  

            # Calculate conversion line
            high_20 = df['High'].rolling(cl_period).max()
            low_20 = df['Low'].rolling(cl_period).min()
            df['conversion_line'] = (high_20 + low_20) / 2

            # Calculate based line
            high_60 = df['High'].rolling(bl_period).max()
            low_60 = df['Low'].rolling(bl_period).min()
            df['base_line'] = (high_60 + low_60) / 2
 
            # Calculate leading span A
            df['lead_span_A'] = ((df.conversion_line + df.base_line) / 2).shift(lag_span_period)

            # Calculate leading span B
            high_120 = df['High'].rolling(52).max()
            low_120 = df['High'].rolling(52).min()
            df['lead_span_B'] = ((high_120 + low_120) / 2).shift(lag_span_period)

            # Calculate lagging span
            df['lagging_span'] = df['Close'].shift(-lag_span_period)
            # df.to_csv("a2.csv", sep='\t')
            # retKlines=df.to_numpy().astype(str)

            # df.dropna(inplace=True)
            self.klines=df.to_numpy().copy().astype(str)
            if self.indicator == "COMBAT":
                close = [float(entry[4]) for entry in self.klines]
                close_array = np.asarray(close)
                macd, macdsignal, macdhist = ta.MACD(close_array, fastperiod=12, slowperiod=26, signalperiod=9)

                self.rsiRet = ta.RSI(close_array, timeperiod=14)
                self.macdRet=[macd, macdsignal, macdhist]

                df = pd.DataFrame(self.klines,columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Can be ignored'])
                period = 20
                df['SMA']= df['Close'].rolling(window=period).mean()
                df['STD']= df['Close'].rolling(window=period).std()
                df['Upper']= df['SMA']+(df['STD']*2)
                df['Lower']= df['SMA']-(df['STD']*2)
                columnList=['SMA','Upper','Lower']
                # df[columnList].plot()
                # plt.show()
                self.bolingerBandsRet = df[columnList].values.tolist()

            return self.klines
        else:
            return None


    '''
    Runs the desired strategy given the indicator results
    '''
    def isGreen(self,kline):
        if len(kline)>4:
            if float64(kline[1]) <= float64(kline[4]):
                return 1
            else:
                return 0
        else:
            return 0

    def calculateStrategy(self):
        self.startPoint = 80
        if self.mode==2:
            self.startPoint = len(self.klines)-3
        if self.indicator == 'BOLBAND':
            if self.strategy == 'SMA':

                fig, ax = plt.subplots(1, 1, sharex=True, figsize=(20, 9))

                # df = pd.DataFrame(self.klines,columns=['Date', 'Open', 'High', 'Low', 'Close', 'SMA','Upper','Lower'])
                openP = [float64(entry[1]) for entry in self.indicator_result]
                highP = [float64(entry[2]) for entry in self.indicator_result]
                lowP = [float64(entry[3]) for entry in self.indicator_result]
                closeP = [float64(entry[4]) for entry in self.indicator_result]
                sma = [float64(entry[5]) for entry in self.indicator_result]
                upper = [float64(entry[6]) for entry in self.indicator_result]
                lower = [float64(entry[7]) for entry in self.indicator_result]
                if len(self.klines)< 80:
                    # panic("Tham so dau vao khong du")
                    return 0
                for i in range(self.startPoint,len(self.indicator_result)):
                    if self.isGreen(self.indicator_result[i]):
                        if closeP[i] <=openP[i]*1.02:
                            if (lowP[i] <= sma[i] and sma[i] <= highP[i]):
                                #or (sma[i]<=highP[i]*1.02) or (sma[i]>=lowP[i]*0.98)
                                plt.plot(i, openP[i],'go', linewidth=1)
                                print(self.indicator_result[i])



                idex = [int(a) for a in range(0,len(self.indicator_result))]
                
                ax.plot(idex, openP, linewidth=1)
                ax.plot(idex, sma, linewidth=2)
                ax.plot(idex, upper, linewidth=2)
                ax.plot(idex, lower, linewidth=2)
                plt.legend(loc=0)
                plt.grid()
                plt.show()

                return 1
            else:
                return None
        elif self.indicator == 'RSI':
            if self.strategy == '7030':
                open_time = [int(entry[0]) for entry in self.klines]
                new_time = [datetime.fromtimestamp(time / 1000) for time in open_time]
                self.time = new_time
                result = []
                active_buy = False
                # Runs through each timestamp in order

                for i in range(len(self.indicator_result)):
                    if np.isnan(self.indicator_result[i]):
                        pass
                    # If the RSI is well defined, check if over 70 or under 30
                    else:
                        if float(self.indicator_result[i]) < 30 and active_buy == False:
                            # Appends the timestamp, RSI value at the timestamp, color of dot, buy signal, and the buy price
                            entry = [open_time[i], self.indicator_result[i], 'go', 'BUY', self.klines[i][4]]
                            result.append(entry)
                            active_buy = True
                        elif float(self.indicator_result[i]) > 70 and active_buy == True:
                            # Appends the timestamp, RSI value at the timestamp, color of dot, sell signal, and the sell price
                            entry = [open_time[i], self.indicator_result[i], 'ro', 'SELL', self.klines[i][4]]
                            result.append(entry)
                            active_buy = False
                return result
            elif self.strategy == '8020':
                open_time = [int(entry[0]) for entry in self.klines]
                new_time = [datetime.fromtimestamp(time / 1000) for time in open_time]
                self.time = new_time
                result = []
                active_buy = False
                # Runs through each timestamp in order

                for i in range(len(self.indicator_result)):
                    if np.isnan(self.indicator_result[i]):
                        pass
                    # If the RSI is well defined, check if over 80 or under 20
                    else:
                        if float(self.indicator_result[i]) < 20 and active_buy == False:
                            # Appends the timestamp, RSI value at the timestamp, color of dot, buy signal, and the buy price
                            entry = [open_time[i], self.indicator_result[i], 'go', 'BUY', self.klines[i][4]]
                            result.append(entry)
                            active_buy = True
                        elif float(self.indicator_result[i]) > 80 and active_buy == True:
                            # Appends the timestamp, RSI value at the timestamp, color of dot, sell signal, and the sell price
                            entry = [open_time[i], self.indicator_result[i], 'ro', 'SELL', self.klines[i][4]]
                            result.append(entry)
                            active_buy = False
                return result
        elif self.indicator == 'ICHI' or self.indicator == 'COMBAT':
            '''
            retdata: ichi strategy list[date,open,high,low,close,volume,colsetime,conversionline,baseline,spanA,spanB,lagspan]
            retdata: conbat strategy list[date,open,high,low,close,volume,colsetime,conversionline,baseline,spanA,spanB,lagspan,macd,macd signel]
            '''
            result=[]
            if self.strategy == 'CLOUD' or self.strategy == '1':
                df = pd.DataFrame(self.klines,columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'comversion line', 'base line', 'span a', 'span b', 'lag span'])
                # df.to_csv("a2.csv", sep='\t')

                open_time = [int(entry[0]) for entry in self.klines]
                new_time = [datetime.fromtimestamp(time / 1000) for time in open_time]
                self.time = new_time
                lagSpan = [float64(entry[11]) for entry in self.klines]
                spanB = [float64(entry[10]) for entry in self.klines]
                spanA = [float64(entry[9]) for entry in self.klines]
                baseLine = [float64(entry[8]) for entry in self.klines]
                conversionLine = [float64(entry[7]) for entry in self.klines]
                closePrice = [float64(entry[4]) for entry in self.klines]
                lowPrice = [float64(entry[3]) for entry in self.klines]
                if len(self.klines)< 80:
                    # panic("Tham so dau vao khong du")
                    return 0
                
                for i in range(self.startPoint,len(self.klines)):
                    if (conversionLine[i] >baseLine[i]) \
                    and (conversionLine[i-1] <= baseLine[i-1]):
                        # #print("check==============================\n")
                        baseScore=0
                        if spanB[i] >= spanA[i]:        
                            if conversionLine[i] >= spanA[i] and conversionLine[i] < spanB[i]: #cat trong may
                                baseScore=baseScore+2
                                #print(baseScore)
                                #print("check1 +2")
                            elif conversionLine[i] >= spanB[i]: #cat tren may
                                baseScore=baseScore+3
                                #print(baseScore)
                                #print("check2 +3")
                                lastNode=-1 # downtrend spanA anf B
                                for j1 in range(0,i):
                                    if conversionLine[i-j1] < baseLine[i-j1]:
                                        lastNode=i-j1
                                        break


                                        #?????????
                                # if lastNode>-1:
                                #     if conversionLine[lastNode] > spanB[lastNode]:
                                #         baseScore=baseScore-12
                                #         #print(baseScore)
                                #         #print("check3 -12")
                            elif conversionLine[i] < spanA[i]:   #cat duoi may
                                baseScore=baseScore+0
                                #print(baseScore)
                                #print("check5")

                            # conversionLine da len qua nhieu nen tru kha nang
                            if conversionLine[i]>=spanB[i]*1.1:      
                                baseScore=baseScore-1
                                #print(baseScore)
                                #print("check6 -1")

                            # conversionLine chua cham toi may nen tru kha nang
                            if conversionLine[i]<spanA[i]*0.9:
                                baseScore=baseScore-1
                                #print(baseScore)
                                #print("check7 -1")
                            if closePrice[i]>spanB[i]:                 # gia vuot may
                                baseScore=baseScore+1
                                #print(baseScore)
                                #print("check8 +1")
                            checkNew=0 # downtrend spanA anf B
                            for i123 in range(0,4):
                                if spanB[i-i123] >= spanA[i-i123]:
                                    checkNew=1
                            if checkNew==0:
                                baseScore=baseScore+1
                                #print(baseScore)
                                #print("check9 +1")

                            lastNode=-1     # downtrend spanA anf B
                            tmpMaxSpanB=0
                            for j1 in range(0,i):
                                if spanB[i-j1] < spanA[i-j1]:
                                    if spanB[i-j1] > tmpMaxSpanB:
                                        tmpMaxSpanB = spanB[i-j1]
                                    lastNode=i-j1
                                    break
                            if lastNode>-1:
                                if lastNode >=20:       # kiem tra do dai cua may
                                    baseScore=baseScore+3
                                    #print(baseScore)
                                    #print("check9-1 +3")
                                if lastNode >=35:       # kiem tra do dai cua may
                                    baseScore=baseScore+3
                                    #print(baseScore)
                                    #print("check9-2 +3")

                                if tmpMaxSpanB > spanA[i]*1.1:  # kiem tra do sau cua may
                                    baseScore=baseScore+3
                                    #print(baseScore)
                                    #print("check9-2 +3")
                                if tmpMaxSpanB > spanA[i]*1.2:  # kiem tra do sau cua may
                                    baseScore=baseScore+3
                                    #print(baseScore)
                                    #print("check9-2 +3")
                                if spanA[lastNode]> spanA[i]:
                                    baseScore=baseScore+1
                                    #print(baseScore)
                                    #print("check10 +1")
                                if spanB[lastNode]> spanB[i]:
                                    baseScore=baseScore+1 
                                    #print(baseScore)
                                    #print("check11 +1")
                                if spanA[lastNode] <= conversionLine[i]:
                                    baseScore=baseScore-3
                                    #print(baseScore)
                                    #print("checkA64 -3")

                        elif spanB[i] < spanA[i]:
                            if (conversionLine[i] >= spanB[i] and conversionLine[i] < spanA[i]) or (conversionLine[i] >= spanA[i]):#cat trong may va tren may
                                lastNode=-1
                                for j1 in range(0,i):
                                    if spanB[i-j1] > spanA[i-j1]:
                                        lastNode=i-j1
                                        break

                                if lastNode>-1:
                                    #mây xanh đi lên thì giảm điểm
                                    if spanA[lastNode] < spanA[i]:
                                        baseScore=baseScore-4
                                        #print(baseScore)
                                        #print("check14-A -4")
                                        #mây xanh  quá 5 tiếng thì giảm điể
                                    if lastNode > 5:
                                        baseScore=baseScore-4
                                        #print(baseScore)
                                        #print("check14-B -4")
                                    # if spanA[lastNode] <= conversionLine[i]:
                                    #     baseScore=baseScore-4
                                    #     #print(baseScore)
                                    #     #print("check14 -4")
                                
                            elif conversionLine[i] < spanB[i]:#cat duoi may
                                baseScore=baseScore+1
                                #print(baseScore)
                                #print("check15")
                            if conversionLine[i]>=spanA[i]*1.1:  #conversionLine da len qua nhieu nen tru kha nang
                                baseScore=baseScore-2
                                #print(baseScore)
                                #print("check16 -2")
                            if conversionLine[i]<spanB[i]*0.9:       # conversionLine chua cham toi may nen tru kha nang
                                baseScore=baseScore-1
                                #print(baseScore)
                                #print("check17-1")
                            if closePrice[i]>spanA[i]:          # gia' vuot may
                                baseScore=baseScore+1
                                #print(baseScore)
                                #print("check18 +1")
                            

                        if lagSpan[i-26] >=  closePrice[i-26]:      # laging span vuot gia
                            baseScore=baseScore+1
                            #print(baseScore)
                            #print("check19 +1")

                        if spanB[i-26] >= spanA[i-26]:              # laging span vuot may
                            if lagSpan[i-26] >=spanB[i-26]:
                                baseScore=baseScore+1
                                #print(baseScore)
                                #print("check20 +1")
                        if spanB[i-26] < spanA[i-26]:                # laging span vuot may
                            if lagSpan[i-26] >=spanA[i-26]:
                                baseScore=baseScore+1
                                #print(baseScore)
                                #print("check21 +1")
                        # kiem tra conversionLine di ngang trong 3 tieng
                        if conversionLine[i]==conversionLine[i-1] \
                        and conversionLine[i]==conversionLine[i-2] \
                        and baseLine[i]<= baseLine[i-1] \
                        and baseLine[i]<= baseLine[i-2]:    # vi du 32/8/2021 10g theo www.coinigy.com tvk-usdt 1h
                            baseScore=baseScore-5
                            #print(baseScore)
                            #print("check22 -5")

                        # kiem tra xe gia da tang nhieu hay chua. 10% = 1.1
                        tmpLow=closePrice[i]
                        for i1 in range(0,11):
                            if tmpLow >closePrice[i-i1]:
                                tmpLow = closePrice[i-i1]
                        if closePrice[i] > tmpLow*1.1:
                            baseScore=baseScore-1
                            #print(baseScore)
                            #print("check23 -1")

                        '''
                        add new check if else here !!!!
                        '''
                        if self.strategy == '1':              # start combat with other strategy
                            if len(self.macdRet)==3 and len(self.macdRet[0])==len(self.klines)and len(self.rsiRet)==len(self.klines):
                            # macdRet[0] = macd
                            # macdRet[1] = macd signal
                            # macdRet[2] = macdhist
                                if self.rsiRet[i]>69:               #rsi qua cao
                                    baseScore=baseScore-6
                                    #print(baseScore)
                                    #print("check25 -6")
                                tmpLowRsi=self.rsiRet[i]
                                tmpHighRsi=0
                                coutCadlesHaveRSILowerThanCurrent=0

                               # kiem tra rsi dang giam trong 2 tieng
                                if self.rsiRet[i]<self.rsiRet[i-1] and self.rsiRet[i]<self.rsiRet[i-2]:
                                    baseScore=baseScore-3
                                    #print(baseScore)
                                    #print("check251 -3")

                                 # kiem tra rsi dang la da tang hay da giam trong 7 tieng
                                for a1 in range(0,7):
                                    if tmpLowRsi > self.rsiRet[i-a1]:
                                        coutCadlesHaveRSILowerThanCurrent=coutCadlesHaveRSILowerThanCurrent+1
                                        tmpLowRsi=self.rsiRet[i-a1]
                                    if tmpHighRsi < self.rsiRet[i-a1]:
                                        tmpHighRsi=self.rsiRet[i-a1]
                                # print("tmpLowRsi="+str(tmpLowRsi)+"curRSI "+str(self.rsiRet[i]))
                                # print("coutCadlesHaveRSILowerThanCurrent="+str(coutCadlesHaveRSILowerThanCurrent))
                                if tmpHighRsi>self.rsiRet[i]*1.06:
                                    baseScore=baseScore-6
                                    #print(baseScore)
                                    #print("check26 -6")
                                elif tmpLowRsi*1.15<=self.rsiRet[i] and coutCadlesHaveRSILowerThanCurrent>2:
                                    baseScore=baseScore+3
                                    #print(baseScore)
                                    #print("check27 +3")

                                tmpCheck=0
                                # #print(baseScore)
                                # kiem tra macd co lon hon duong macd sinal khong, vi tri cua no va da giao nhau lau chua
                                if (self.macdRet[0][i] <= self.macdRet[1][i]):
                                    baseScore=baseScore-1
                                    #print(baseScore)
                                    ##print("check28 -1")
                                    # if (self.macdRet[1][i]-self.macdRet[0][i])>(self.macdRet[1][i-1]-self.macdRet[0][i-1]) or (self.macdRet[1][i]-self.macdRet[0][i])>(self.macdRet[1][i-2]-self.macdRet[0][i-2]):
                                    #     baseScore=baseScore-5
                                        # #print("check4-A")
                                elif (self.macdRet[0][i] > self.macdRet[1][i]):
                                    baseScore=baseScore+1
                                    #print(baseScore)
                                    ##print("check29 +1")
                                    if self.macdRet[1][i] <0:
                                        baseScore=baseScore+1
                                        #print(baseScore)
                                        #print("check30 +1")

                                    if self.macdRet[0][i] >0 and  self.macdRet[1][i] >0:
                                        for i12 in range(0,7):
                                            if self.macdRet[0][i-i12] < self.macdRet[1][i-i12]:
                                                tmpCheck=1
                                                break
                                        if tmpCheck==1:
                                            baseScore=baseScore+1
                                            #print(baseScore)
                                            #print("check31 +1")
                                        elif tmpCheck==0:
                                            baseScore=baseScore-6
                                            #print(baseScore)
                                            #print("check32 -6")

                        # print("======================== "+str(baseScore))

                        if float64(self.bolingerBandsRet[i][0]) < float64(closePrice[i]):           # nho hon duong sma cua bolinger band
                            # print(self.bolingerBandsRet[i][0])
                            # print(closePrice[i])
                            if baseScore>2:
                                entry = [open_time[i],closePrice[i], baseScore,conversionLine[i],'go']
                                result.append(entry)
                            else:
                                entry = [open_time[i],closePrice[i], baseScore,conversionLine[i],'ro']
                                result.append(entry)

                return result  #<<[time,closeprice,score at that price,conversionLine, color]
        else:
            return None


    '''
    Getter for the strategy result
    '''

    def getIndicatorResult(self):
        return self.indicator_result

    def getStrategyResult(self):
        return self.strategy_result

    '''
    Getter for the klines
    '''
    def getKlines(self):
        return self.klines

    '''
    Getter for the trading pair
    '''
    def getPair(self):
        return self.pair

    '''
    Getter for the trading interval
    '''
    def getInterval(self):
        return self.interval

    '''
    Getter for the time list
    '''
    def getTime(self):
        return self.time

    '''
    Plots the desired indicator with strategy buy and sell points
    '''
    def plotIndicator(self):
        open_time = [int(entry[0]) for entry in self.klines]
        new_time = [datetime.fromtimestamp(time / 1000) for time in open_time]
        plt.style.use('dark_background')
        for entry in self.strategy_result:
            plt.plot(entry[0], entry[1], entry[2])
        if self.indicator == 'MACD':
            plt.plot(new_time, self.indicator_result[0], label='MACD')
            plt.plot(new_time, self.indicator_result[1], label='MACD Signal')
            plt.plot(new_time, self.indicator_result[2], label='MACD Histogram')

        elif self.indicator == 'RSI':
            plt.plot(new_time, self.indicator_result, label='RSI')

        else:
            pass

        title = self.indicator + " Plot for " + self.pair + " on " + self.interval
        plt.title(title)
        plt.xlabel("Open Time")
        plt.ylabel("Value")
        plt.legend()
        plt.show()

    def plotIndicatorTest(self):

        open_time = [int(entry[0]) for entry in self.klines]
        lagSpan = [float64(entry[11]) for entry in self.klines]
        spanB = [float64(entry[10]) for entry in self.klines]
        spanA = [float64(entry[9]) for entry in self.klines]
        baseLine = [float64(entry[8]) for entry in self.klines]
        conversionLine = [float64(entry[7]) for entry in self.klines]
        closePrice = [float64(entry[4]) for entry in self.klines]
        new_time = [datetime.fromtimestamp(time / 1000) for time in open_time]
        fig, ax = plt.subplots(1, 1, sharex=True, figsize=(20, 9))
        ax.plot(new_time, closePrice, linewidth=2,label="closePrice")
        ax.plot(new_time, spanA,label="spanA")
        ax.plot(new_time, spanB,label="spanB")
        # ax.plot(new_time, lagSpan,label="lagSpan")

        ax.plot(new_time, conversionLine,label="conversionLine")
        ax.plot(new_time, baseLine,label="baseLine")
        cout =1
        for entry in self.strategy_result:
            print(str(cout))
            print(entry)
            cout =1+cout
            plt.plot(datetime.fromtimestamp(entry[0] / 1000), entry[3], entry[4])

        ax.fill_between(new_time, spanA, spanB,color='lightgreen')
        
        plt.legend(loc=0)
        plt.grid()
        plt.show()
