#!/usr/bin/python3
# -*- coding: utf-8 -*-
import config, csv, strategy
from binance import  Client,ThreadedWebsocketManager, ThreadedDepthCacheManager
import talib as ta
import matplotlib.pyplot as plt
import numpy as np
from numpy import *  
from datetime import datetime
import pandas as pd
from datetime import datetime
import time
import os
import argparse
from binance.enums import *
debugProfit=0
debugSell=1
class Trader:
    def __init__(self):
        self.symbols=['']
        self.connect()
        self.draw=False
        self.tien=float64(0)
        # a1 = open("log/boughtCoin.txt","a")
        # a1.close()
        # print("1234")
        # boughtCoinData =open("log/boughtCoin.txt","r").readline()
        # print(boughtCoinData)
        # for line in boughtCoinData:
        #     if len(line)>4 and len(line.split("|"))==10:
        #         line = line.split("|")
        #         print(line[6])
        #         self.tien=self.tien-float64(line[6])

    """ Creates Binance client """
    def connect(self):
        self.client = Client(config.api_key, config.api_secret)

    """Lay tat ca cac cap tien co the giao dich voi usdt"""
    def getAllPair(self):
        exchange_info = self.client.get_exchange_info()
        tmpSymbols=""
        blackList=open("blackList.txt","r").read()
        for s in exchange_info['symbols']:
            tmp=s['symbol']
            # if "USD" in tmp[-3:] or "SDT" in tmp[-3:]:
            if tmp not in blackList and "USDT" in tmp[-4:] and "BUSDT" not in tmp and "BULLUSDT" not in tmp and "BEARUSDT" not in tmp and "UPUSDT" not in tmp and "DOWNUSDT" not in tmp and "USDS" not in tmp:
                tmpSymbols+=tmp+"--"
        tmpSymbols=tmpSymbols[:-2]
        self.symbols =  tmpSymbols.split("--")
        return self.symbols


    """Tinh indicator va ghi ra file. Chi su dung voi release mode"""
    def startCalculated(self,pair1,interval1,retFileName,curreentTimeOrNot,metricSan,baolau):
        # metricSan: diem thap nhat co the lay
        self.trading_pair=pair1
        self.interval=interval1

        klines = self.client.get_klines(symbol=self.trading_pair,interval=self.interval)            # for 500 candles
        # klines=self.client.get_historical_klines(self.trading_pair, Client.KLINE_INTERVAL_1HOUR,"13 April, 2021","27 JULY, 2021") # for a range of time
        if len(klines)<=80:
            return 0
        tmpKlines = klines.copy()
        if curreentTimeOrNot==2:         # all current hour
            ichiStrategy =strategy.Strategy("COMBAT","1",self.trading_pair,self.interval,tmpKlines,2)
        elif curreentTimeOrNot==1:              # all time
            ichiStrategy =strategy.Strategy("COMBAT","1",self.trading_pair,self.interval,tmpKlines,1)           

        ###write to file
        retFile = open(retFileName,"a")
        retFile.close()

        ret = ichiStrategy.getStrategyResult()
        with open(retFileName, 'r') as original: dataOld = original.read()
        with open(retFileName, 'r') as original2: dataOldLines = original2.readlines()
        if len(ret)>0:
            for data in ret:
                if int(data[2]) >= metricSan:
                    checkExist=0
                    if str(data[0])+"|pair="+pair1 in dataOld:
                        checkExist=1
                    for line in dataOldLines:
                        if pair1 in line:
                            line = line.replace("\n","").replace("xxxxxx","")
                            if len(line.split("|"))>2:
                                oldTime = float64(line.split("|")[0])
                                curTime = float64(data[0])
                                if (curTime - oldTime)/1000 < 36000*float64(baolau):
                                    checkExist=1
                                    print(str(data[0])+"|pair="+pair1+"|closePrice="+str(data[1])+"|metric="+str(data[2]))
                    if checkExist==0:
                        dataOld = str(data[0])+"|pair="+pair1+"|closePrice="+str(data[1])+"|metric="+str(data[2])+"\n"+dataOld
        with open(retFileName, 'w') as modified: modified.write(dataOld)
        return 

    """Tinh indicator va ghi ra file. Chi su dung voi test mode"""
    def startCalculatedInTimeRange(self,pair1,interval1,retFileName,curreentTimeOrNot,metricSan,time1,time2):   

        # metricSan: diem thap nhat co the lay
        self.trading_pair=pair1
        self.interval=interval1

        # klines = self.client.get_klines(symbol=self.trading_pair,interval=self.interval)            # for 500 candles
        klines=self.client.get_historical_klines(self.trading_pair, Client.KLINE_INTERVAL_1HOUR,time1,time2) # for a range of time
        if len(klines)<=80:
            return 0
        tmpKlines = klines.copy()
        if curreentTimeOrNot==2:         
            ichiStrategy =strategy.Strategy("COMBAT","1",self.trading_pair,self.interval,tmpKlines,2)   # current hour
        elif curreentTimeOrNot==1:             
            ichiStrategy =strategy.Strategy("COMBAT","1",self.trading_pair,self.interval,tmpKlines,1)    # all time  


        if self.draw:
            ichiStrategy.plotIndicatorTest()

        ###write to file
        retFile = open(retFileName,"a")
        retFile.close()

        ret = ichiStrategy.getStrategyResult()
        with open(retFileName, 'r') as original: dataOld = original.read()
        if len(ret)>0:
            for data in ret:
                if int(data[2]) >= metricSan:
                    checkExist=0
                    if str(data[0])+"|pair="+pair1 in dataOld:
                        checkExist=1
                    if checkExist==0:
                        dataOld = str(data[0])+"|pair="+pair1+"|closePrice="+str(data[1])+"|metric="+str(data[2])+"\n"+dataOld
        with open(retFileName, 'w') as modified: modified.write(dataOld)
        return 

    def checka1(self):
        # def startCalculated(self,pair1,interval1,retFileName,curreentTimeOrNot,metricSan,baolau):


        self.trading_pair="TVKUSDT"
        self.interval="1h"

        klines = self.client.get_klines(symbol=self.trading_pair,interval=self.interval)            # for 500 candles
        # klines=self.client.get_historical_klines(self.trading_pair, Client.KLINE_INTERVAL_1HOUR,"13 April, 2021","27 JULY, 2021") # for a range of time

        tmpKlines = klines.copy()
        bb =strategy.Strategy("BOLBAND","SMA",self.trading_pair,self.interval,tmpKlines,1)


    def checkForBuy(self,indicatorFile,sba1,baoLau):
        """
        sba1 luong usdt thaop nhat cho moi lenh
        baolau: chuki 1 lenh
        """
        sba = float64(sba1)

        curFreeUSDT = float64(self.client.get_asset_balance(asset='USDT')['free'])
        if curFreeUSDT < sba*1.7:
            return

        a1 = open("log/boughtCoin.txt","a")
        a1.close()
        inputData = open(indicatorFile,"r").readlines()
        retIndicator = open(indicatorFile,"w")
        
        for data in inputData:
            tmpData = data
            # print(tmpData)
            if "xxxxx" in tmpData:
                # lenh da duoc mua nen bo qua
                retIndicator.write(tmpData)
                continue
            elif len(data.split("|"))==4:
                data =data.replace("\n","").replace("pair=","").replace("closePrice=","").replace("metric=","").split("|")
                if "USDT" in data[1]:
                    # print("check11")
                    startTime = data[0]
                    pair=data[1]
                    buyPrice = float64(data[2])
                    metric = data[3]
                    
                    curPrice = float64(self.client.get_symbol_ticker(symbol=pair)['price'])
                    boughtCoin=open("log/boughtCoin.txt","r").read()
                    if pair in boughtCoin:
                        # pair nay da duoc va dang duoc theo doi nen k mua lai
                        # retIndicator.write(tmpData) khong can vi ta se xoa bo luon
                        continue
                    # print("curPrice="+str(curPrice))
                    # print("buyPrice="+str(buyPrice*1.02))
                    # print("sba*1.6="+str(sba*1.6))
                    curTime = time.time()
                    tmpStartTime = float64(startTime)/1000
                    if curTime > (tmpStartTime+3600*float64(baoLau)/2):
                        # print(check1)
                        # 1 so truong hop k du so du usdt de mua va khi cos du thi qua thoi gian cycle nen bo qua lenh
                        retIndicator.write("xxxxxx"+tmpData)

                    elif curFreeUSDT >=sba*1.7 and curPrice <= buyPrice*1.02:

                        # kiem tra trong khoang thoi gian tu luc pair vao queue thi gia da vuot > 3% hay chua. neu vuot roi thi khong mua nua
                        klines = self.client.get_klines(symbol=pair,interval=self.interval)
                        countToCheck=-1
                        for i1 in range(0,len(klines)):
                            if float64(data[0])<= float64(klines[i1][0]):
                                countToCheck=i1
                                break
                        checkVuotGia=-1
                        if countToCheck>-1:
                            for i2 in range(countToCheck,len(klines)):
                                if float64(klines[i2][2]) > buyPrice*1.03:
                                    checkVuotGia=1
                        if checkVuotGia==1:
                            retIndicator.write("xxxxxx"+tmpData)
                            continue

                        # print("check2")
                        ret = self.buyAnyThings(pair,sba)
                        # print(ret)
                        if len(ret) <4 and len(ret.split("|"))!=3:
                            open("log/boughtCoin.txt","a").write("\n******Loi khi mua "+str(sba)+"$ "+str(pair)+" curPrice="+str(curPrice)+" freeUSDT="+str(curFreeUSDT)+" ma loi="+str(ret)+"\n")
                            retIndicator.write(tmpData)
                            continue
                        #ret[gia,so luong, so tien usd]
                        ret=ret.split("|")
                        buySellData = str(time.time())+"|"+pair+"|"+str(ret[0])+"|"+str(metric)+"|"+str(ret[1])+"|0|"+str(ret[2])+"|0|0|0" 
                        # buySellData = str(time.time())+"|"+pair+"|"+str(curPrice)+"|"+str(metric)+"|"+str(round(float64(100/float64(curPrice)),10))+"|0|100|0|0|0"   
                        # sua lai str(round(float64(100/float64(closePrice)),10)) de dung voi du kia mua ban
                        self.tien=self.tien-float64(ret[2])
                        open("log/boughtCoin.txt","a").write(buySellData+"\n")
                        open("log/logBuy.txt","a").write("BUY:"+pair+"|Price:"+str(curPrice)+"|amount:"+str(ret[2])+"$\n")

                        # bat dau mua khi luong free usdt thoa man nhu cau va gia hien tai <= gia da tinh toan*1.02
                        retIndicator.write("xxxxxx"+tmpData)
                    else:
                        # quay lai queue
                        retIndicator.write(tmpData)

        retIndicator.close()
    def checkForSell(self,boughtCoinFile, baoLau):
        t1 = open(boughtCoinFile,"a")
        t1.close()
        datas = open(boughtCoinFile,"r").readlines()

        # 1631356647.17683|TLMUSDT|0.2148|19|558.7025853058884|0.221244|120.0|-1|1|0
        # 1631356647.3359523|AAVEUSDT|324.0|19|0.3704084978447807|333.72|120.0|-1|1|0
        # backup lai data de phong truong hop function nay bi crash.
        retboughtCoin = open(boughtCoinFile,"w")

        for data in datas:
            bkData = data
            try:
                if debugSell==1:
                    print(data)
                data = data.replace("\n","").replace("pair=","").replace("closePrice=","").replace("metric=","").split("|")

                startTime = float64(data[0])
                pair=data[1]
                buyPrice = float64(data[2])
                metric = data[3]
                amount = float64(data[4])
                hopePrice = float64(data[5])
                money = float64(data[6])
                state = int(data[7])
                solantbg=int(data[8])
                solanban=int(data[9])
                curPrice = float64(self.client.get_symbol_ticker(symbol=pair)['price'])

                baoLau=int(baoLau)

                curTime = float64(time.time())
                if curTime >=startTime+3600*baoLau:

                    if float(curPrice)*amount<11:
                        if debugSell==1:
                            print("Khong the ban 100% vif so luong < 11")
                        state == -4 # da ban
                        self.tien=self.tien+float64(curPrice*amount)
                        open("log/logSell.txt","a").write("******Loi khi ban 100 phan tram "+pair+"|Price:"+str(curPrice)+"|amount:"+str(amount)+"$|Khong the ban nong do so du < 11$\n")
                    else:
                        ret = self.sellAnyThings(pair,amount,1)
                        if debugSell==1:
                            print("Ban het vi vuot cycle")
                            print(ret)
                        """
                        return:
                        ret[so token da ban, so tien usd nhan duoc]
                        """
                        if len(ret.split("|")) !=2:
                            open("log/logSell.txt","a").write("\n******Loi khi ban 100 phan tram "+str(amount)+" "+str(pair)+" "+ret+"\n")
                            continue
                        open("log/logSell.txt","a").write("SELL:"+pair+"|Price:"+str(curPrice)+"|amount:"+str(ret[1])+"$|Ban Nong vi het thoi gian\n")
                        self.tien=self.tien+float64(ret[1])
                        state == -4 # da ban
                    continue

                controlData = open("control.txt","r").read()
                if "sell:"+pair.replace("\n","") in controlData:
                    ret = self.sellAnyThings(pair,amount,1)
                    if debugSell==1:
                        print("Ban het vi vuot cycle")
                        print(ret)
                    """
                    return:
                    ret[so token da ban, so tien usd nhan duoc]
                    """
                    if len(ret.split("|")) !=2:
                        open("log/logSell.txt","a").write("\n******Loi khi ban 100 phan tram "+str(amount)+" "+str(pair)+" "+ret+"\n")
                        continue
                    open("log/logSell.txt","a").write("SELL:"+pair+"|Price:"+str(curPrice)+"|amount:"+str(ret[1])+"$|Ban Nong vi het thoi gian\n")
                    self.tien=self.tien+float64(ret[1])
                    state == -4 # da ban
                    continue

                if state == -4:
                    # bo qua vi da ban het roi
                    continue
                if hopePrice == float64(0):
                    hopePrice=float64(buyPrice*1.03)

                lo=0.0
                lo = (buyPrice-curPrice)/buyPrice
                curFreeUSDT = float64(self.client.get_asset_balance(asset='USDT')['free'])
                if lo >0:
                    if solanban>0:
                        if float(curPrice)*amount<11:
                            state == -4 # da ban
                            self.tien=self.tien+float64(curPrice*amount)
                            open("log/logSell.txt","a").write("******Loi khi ban 100 phan tram khi dao chieu "+pair+"|Price:"+str(curPrice)+"|amount:"+str(amount)+"$|Khong the ban nong do so du < 11$\n")
                        else:   
                            ret = self.sellAnyThings(pair,amount,1)
                            if debugSell==1:
                                print("Cat lo vi dao chieu")
                                print(ret)
                            """
                            return:
                            ret[so token da ban, so tien usd nhan duoc]
                            """
                            if len(ret.split("|")) !=2:
                                open("log/logSell.txt","a").write("\nLoi khi ban 100 phan tram "+str(amount)+" "+str(pair)+" "+ret+"\n")
                                continue
                            ret = ret.split("|")
                            open("log/logSell.txt","a").write("SELL:"+pair+"|Price:"+str(curPrice)+"|amount:"+str(ret[1])+"$|Cat lo vi dao chieu\n")
                            self.tien=self.tien+float64(ret[1])
                            money=money-float64(ret[1])
                            amount=0
                            hopePrice = 0.0
                            state=-4
                    # if debugProfit==1:
                    #     print("lo = "+str(lo))
                    elif lo <=0.06 and lo >=0.04 and solantbg==0:
                        
                        sba1=float(money)*0.25
                        if sba1<11:
                            sba1=11
                        if curFreeUSDT < sba1:
                            continue
                        else:
                            ret = self.buyAnyThings(pair,sba1)
                            if debugSell==1:
                                print("TBG KHI LO 4%")
                                print(ret)
                            # ret[gia,so luong, so tien usd]
                            if len(ret.split("|")) !=3:
                                open("log/boughtCoin.txt","a").write("\nLoi khi mua "+str(sba1)+"$ "+str(pair)+" freeUSDT="+str(curFreeUSDT)+" "+ret+"\n")
                                continue
                            ret = ret.split("|")
                            open("log/logBuy.txt","a").write("BUY:"+pair+"|Price:"+str(ret[0])+"|amount:"+str(ret[2])+"$|TBG khi Lo 4%\n")
                            self.tien=self.tien-float64(ret[2])
                            solantbg=1
                            state = -1
                            amount = amount+float64(ret[1])
                            money = money+float64(ret[2])

                    elif lo <=0.1 and lo >=0.09 and solantbg==1:
                        
                        sba1=float(money)*0.25
                        if sba1<11:
                            sba1=11
                        if curFreeUSDT < sba1:
                            continue
                        else:
                            ret = self.buyAnyThings(pair,sba1)
                            if debugSell==1:
                                print("TBG KHI LO 9%")
                                print(ret)

                            # ret[gia,so luong, so tien usd]
                            if len(ret.split("|")) !=3:
                                open("log/boughtCoin.txt","a").write("\nLoi khi mua "+str(sba1)+"$ "+str(pair)+" freeUSDT="+str(curFreeUSDT)+" "+ret+"\n")
                                retIndicator.write(tmpData)
                                continue
                            ret = ret.split("|")
                            open("log/logBuy.txt","a").write("BUY:"+pair+"|Price:"+str(ret[0])+"|amount:"+str(ret[2])+"$|TBG khi Lo 9%\n")
                            self.tien=self.tien-float64(ret[2])
                            solantbg=2
                            state = -2
                            amount = amount+float64(ret[1])
                            money = money+float64(ret[2])

                    elif lo >=0.13:
                        ret = self.sellAnyThings(pair,amount,1)
                        if debugSell==1:
                            print("Cat lo vi tut 13%")
                            print(ret)
                        """
                        return:
                        ret[so token da ban, so tien usd nhan duoc]
                        """
                        if len(ret.split("|")) !=2:
                            open("log/logSell.txt","a").write("\nLoi khi ban 100 phan tram "+str(amount)+" "+str(pair)+" "+ret+"\n")
                            continue
                        ret = ret.split("|")
                        open("log/logSell.txt","a").write("SELL:"+pair+"|Price:"+str(curPrice)+"|amount:"+str(ret[1])+"$|Cat lo vi gia tut 13%\n")
                        self.tien=self.tien+float64(ret[1])
                        money=money-float64(ret[1])
                        amount=0
                        hopePrice = 0.0
                        state=-4
                else:

                    if curPrice >= hopePrice and state<1:
                        ret = self.sellAnyThings(pair,amount,0.3)
                        if debugSell==1:
                            print("Ban 30% khi lai 3%")
                            print(ret)
                        """
                        return:
                        ret[so token da ban, so tien usd nhan duoc]
                        """
                        if len(ret.split("|")) !=2:
                            open("log/logSell.txt","a").write("\nLoi khi ban 30% phan tram "+str(amount)+" "+str(pair)+" "+ret+"\n")
                            continue
                        ret = ret.split("|")
                        open("log/logSell.txt","a").write("SELL:"+pair+"|Price:"+str(curPrice)+"|amount:"+str(ret[1])+"$|Ban 30% khi lai 3%\n")
                        self.tien=self.tien+float64(ret[1])
                        money=money-float64(ret[1])
                        amount=amount-float64(ret[0])
                        hopePrice = (hopePrice*1.06)/1.03
                        state=1
                        solanban=solanban+1


                    elif curPrice >= hopePrice and state==1:
                        ret = self.sellAnyThings(pair,amount,0.3)
                        if debugSell==1:
                            print("Ban 30% khi lai 6%")
                            print(ret)
                        """
                        return:
                        ret[so token da ban, so tien usd nhan duoc]
                        """
                        if len(ret.split("|")) !=2:
                            open("log/logSell.txt","a").write("\nLoi khi ban 30% phan tram "+str(amount)+" "+str(pair)+" "+ret+"\n")
                            continue
                        ret = ret.split("|")
                        open("log/logSell.txt","a").write("SELL:"+pair+"|Price:"+str(curPrice)+"|amount:"+str(ret[1])+"$|Ban 30% khi lai 6%\n")
                        self.tien=self.tien+float64(ret[1])
                        money=money-float64(ret[1])
                        amount=amount-float64(ret[0])
                        hopePrice = (hopePrice*1.1)/1.06
                        state=2
                        solanban=solanban+1


                    elif curPrice >= hopePrice and state==2:

                        ret = self.sellAnyThings(pair,amount,0.5)
                        if debugSell==1:
                            print("Ban 50% khi lai 10%")
                            print(ret)
                        """
                        return:
                        ret[so token da ban, so tien usd nhan duoc]
                        """
                        if len(ret.split("|")) !=2:
                            open("log/logSell.txt","a").write("\nLoi khi ban 50% phan tram "+str(amount)+" "+str(pair)+" "+ret+"\n")
                            continue
                        ret = ret.split("|")
                        open("log/logSell.txt","a").write("SELL:"+pair+"|Price:"+str(curPrice)+"|amount:"+str(ret[1])+"$|Ban 50% khi lai 10%\n")
                        self.tien=self.tien+float64(ret[1])
                        money=money-float64(ret[1])
                        amount=amount-float64(ret[0])
                        hopePrice = (hopePrice*1.14)/1.1
                        state=3
                        solanban=solanban+1

                    elif curPrice >= hopePrice and state==3:
                        
                        ret = self.sellAnyThings(pair,amount,1)
                        if debugSell==1:
                            print("Ban 50% khi lai 14%")
                            print(ret)
                        """
                        return:
                        ret[so token da ban, so tien usd nhan duoc]
                        """
                        if len(ret.split("|")) !=2:
                            open("log/logSell.txt","a").write("\nLoi khi ban 50% phan tram "+str(amount)+" "+str(pair)+" "+ret+"\n")
                            continue
                        ret = ret.split("|")
                        open("log/logSell.txt","a").write("SELL:"+pair+"|Price:"+str(curPrice)+"|amount:"+str(ret[1])+"$|Ban 50% khi lai 14%\n")
                        self.tien=self.tien+float64(ret[1])
                        money=money-float64(ret[1])
                        amount=amount-float64(ret[0])
                        hopePrice = 0
                        state=-4
                        solanban=solanban+1

                if state != -4:
                    data1 = str(startTime)+"|"+str(pair)+"|"+str(buyPrice)+"|"+str(metric)+"|"+str(amount)+"|"+str(hopePrice)+"|"+str(money)+"|"+str(state)+"|"+str(solantbg)+"|"+str(solanban)
                    retboughtCoin.write(data1+"\n")
            except:
                open("log/logFail.txt","a").write(bkData)
                retboughtCoin.write(bkData)

        retboughtCoin.close()
        logTien = open("log/logTien.txt","a").write(str(self.tien)+"\n")


    def sellAnyThings(self,pair,amount,percent):
        """
        return:
        ret[so token da ban, so tien usd nhan duoc]
        """
        amount = float64(amount)
        percent = float64(percent)
        if percent >1.0:
            percent=1.0
        ret=""
        if "USDT" not in pair[-4:]:
            ret="1"
            return ret
        tokenName = pair[:-4]
        curFreeToken = float64(self.client.get_asset_balance(asset=tokenName)['free'])

        # print(amount)
        if amount > curFreeToken:
            amount = curFreeToken

        info = self.client.get_symbol_info(pair)
        minAmount = float(info['filters'][2]['minQty'])
        a1 = int(1/minAmount)
        quantity= int(float64(amount)*float64(percent)/minAmount)/a1
        order=""
        # print(quantity)
        try:
            order = self.client.order_market_sell(symbol=pair,quantity=quantity)
        except:
            return "2"
        # print(order)
        ret = str(order['executedQty'])+"|"+str(order['cummulativeQuoteQty'])
        return ret

    def buyAnyThings(self,pair,maxM):
        """
        maxM = bulget de mua
        return:
        ret[gia,so luong, so tien usd]
        """
        maxM=float64(maxM)
        curFreeUSDT = float64(self.client.get_asset_balance(asset='USDT')['free'])
        if curFreeUSDT <=maxM:
            ret="1"
            return ret
        ret=""
        order=""
        maxMoney = maxM
        freeUSDT = float64(self.client.get_asset_balance(asset='USDT')['free'])
        eth_price = float64(self.client.get_symbol_ticker(symbol=pair)['price'])
        info = self.client.get_symbol_info(pair)
        minAmount = float(info['filters'][2]['minQty'])
        if minAmount>1:
            return "2"

        a1 = int(1/minAmount)
        quantity=int(float64(maxMoney/eth_price)/minAmount)
        quantity = quantity/a1
        
        try:
            order = self.client.order_market_buy(symbol=pair,quantity=quantity)
        except:
            return "3"
        ret = str(float64(order['cummulativeQuoteQty'])/float64(quantity))+"|"+str(quantity)+"|"+str(order['cummulativeQuoteQty'])
        return ret

    def testCheckForSell(self,data,tokenPrice,banong=0):

        data = data.replace("pair=","").replace("closePrice=","").replace("metric=","").split("|")
        # print(data)
        startTime = data[0]
        pair=data[1]
        buyPrice = float64(data[2])
        metric = data[3]
        amount = float64(data[4])
        hopePrice = float64(data[5])
        money = float64(data[6])
        state = int(data[7])
        solantbg=int(data[8])
        solanban=int(data[9])
        curPrice = float64(tokenPrice)
            
        if hopePrice == float64(0):
            hopePrice=float64(buyPrice*1.03)

        lo=0.0

        lo = (buyPrice-curPrice)/buyPrice

        if banong==1:
            if debugProfit==1:
                print("111Ban nong ")
            money=money-amount*curPrice
            self.tien=self.tien+amount*curPrice
            amount=0
            state == -4 # da ban
            return str(startTime)+"|"+str(pair)+"|"+str(buyPrice)+"|"+str(metric)+"|"+str(amount)+"|"+str(hopePrice)+"|"+str(money)+"|"+str(state)+"|"+str(solantbg)+"|"+str(solanban)
      
        if lo >0:
            if solanban>0:
                if debugProfit==1:
                    print("111Ban het vi Dao chieu")
                money=money-amount*curPrice
                self.tien=self.tien+amount*curPrice
                amount=0
                hopePrice = 0.0
                state=-4
            if debugProfit==1:
                print("lo = "+str(lo))
            if lo <=0.03 and solantbg==0:
                if debugProfit==1:
                    print("111 TBG 20%")
                self.tien=self.tien-money*0.2
                solantbg=1
                state = -1
                amount = amount+money*0.2/curPrice
                money = money+money*0.2
            elif lo >0.03 and  lo <=0.05 and state == -1 and solantbg==1:
                if debugProfit==1:
                    print("111 TBG 20%")
                self.tien=self.tien-money*0.2
                solantbg=2
                state = -2
                amount = amount+money*0.2/curPrice
                money = money+money*0.2
            elif lo >=0.09 and lo < 0.1 and state == -2 and solantbg==2:
                solantbg=3
                if debugProfit==1:
                    print("111 TBG 10%")
                self.tien=self.tien-money*0.1
                state = -3
                amount = amount+money*0.1/curPrice
                money = money+money*0.1
            elif lo >=0.13 and state <= -2:
                if debugProfit==1:
                    print("111Cat lo")
                self.tien=self.tien+amount*curPrice
                money=money-amount*curPrice
                amount=0
                state = -4 # da ban
        else:

            if curPrice >= hopePrice and state<1:
                self.tien=self.tien+amount*curPrice*0.2
                if debugProfit==1:
                    print("111Ban 20% khi tang 3%")
                solanban=solanban+1
                money=money-amount*curPrice*0.2
                amount=amount*0.8
                hopePrice = (hopePrice*1.05)/1.03
                if debugProfit==1:
                    print("111hopePrice="+str(hopePrice))
                state=1
            elif curPrice >= hopePrice and state==1:
                self.tien=self.tien+amount*curPrice*0.2
                if debugProfit==1:
                    print("111Ban 20% khi tang 5%")
                solanban=solanban+1
                money=money-amount*curPrice*0.2
                amount=amount*0.8
                hopePrice = (hopePrice*1.07)/1.05
                state=2
            elif curPrice >= hopePrice and state==2:
                self.tien=self.tien+amount*curPrice*0.2
                if debugProfit==1:
                    print("111Ban 20% khi tang 7%")
                solanban=solanban+1
                money=money-amount*curPrice*0.2
                amount=amount*0.8
                hopePrice = (hopePrice*1.1)/1.07
                state=3
            elif curPrice >= hopePrice and state==3:
                if debugProfit==1:
                    print("111Ban 50% khi tang 10%")
                self.tien=self.tien+amount*curPrice*0.5
                solanban=solanban+1
                money=money-amount*curPrice*0.5
                amount=amount*0.5
                hopePrice = (hopePrice*1.15)/1.01
                state=4
            elif curPrice >= hopePrice and state==4:
                self.tien=self.tien+amount*curPrice
                if debugProfit==1:
                    print("111Ban het khi tang 15%")
                money=money-amount*curPrice
                amount=0
                hopePrice = 0.0
                state=-4
            
        return str(startTime)+"|"+str(pair)+"|"+str(buyPrice)+"|"+str(metric)+"|"+str(amount)+"|"+str(hopePrice)+"|"+str(money)+"|"+str(state)+"|"+str(solantbg)+"|"+str(solanban)

    """tinh toan % lenh thang, lai bao nhieu % khi su dung chien thuajt mua ban hien tai, tim so lo co the chap nhan duoc de dat toi lenh thang"""
    def checkIndicatorRet(self,indicatorFileName,baseScore,profit,stoploss,baonhieutieng):
        # phantram: lai toi thieu: 1,01 = 1%
        # bao nhieu ngay; kiem tra trong bao nhieu ngay
        
        count1=1 # tong so lenh
        count2=1 # tong so lenh thang
        checkIchiIntersect=0

        tongTien=0.0
        lines = open(indicatorFileName,"r").readlines();
        reducePercent=0
        a3=0
        a5=0
        a10=0
        a20=0
        a30=0
        a40=0
        a50=0

        a0a=0
        a3a=0
        a5a=0
        a10a=0
        a20a=0
        a15a=0
        a25a=0
        a30a=0

        t5=0
        t10=0
        t15=0
        t20=0
        t30=0
        t40=0
        t50=0
        t60=0
        profitFile = open("profit.txt","w")
        win = open("win1.txt","w")
        lose = open("lose1.txt","w")
        blackList=open("blackList.txt","r").read()
        for line in lines:

            
            tmp1=line.replace("\n","")
            line = line.replace("pair=","").replace("closePrice=","").replace("metric=","").split("|")

            if len(line)== 4:
                startTime = line[0]
                pair=line[1]
                if pair in blackList:
                    continue
                closePrice = line[2]
                metric = line[3]

                if int(metric)<baseScore:
                    continue
                count1=count1+1

                now = datetime.fromtimestamp(int(startTime) / 1000)
                startTimeStr = now.strftime("%d %B, %Y")
                tmpNow = now
                endTime = int(startTime)+3600000*baonhieutieng+3600000*24
                now = datetime.fromtimestamp(endTime / 1000)
                endTimeStr = now.strftime("%d %B, %Y")

                
                klines=self.client.get_historical_klines(pair, Client.KLINE_INTERVAL_15MINUTE,startTimeStr,endTimeStr)

                # ichiStrategy =strategy.Strategy("ICHI","","",'1h',klines,2)
                # ichiStrategyRet=ichiStrategy.getIndicatorResult()


                tmpMaxPrice=float64(0)
                tmpLowPrice=float64(closePrice)*10
                
                coutToMax=0
                pos=0
                for i in range(0,len(klines)):
                    if startTime == str(klines[i][0]):
                        pos=i
                        break
                
                buySellData = tmp1+"|"+str(round(float64(100/float64(closePrice)),10))+"|0|100|0|0|0"
                self.tien=self.tien-100
                for i in range(pos,4*baonhieutieng):
                    if i >= len(klines):
                        if buySellData.split("|")[7]  != "-4":
                            if debugProfit==1:
                                print("Ban nong 1")
                            buySellData = self.testCheckForSell(buySellData,klines[i-1][2],1)
                        break
                    # tim gia cao nhat trong khoang tg dduoc dinh san
                    

                    if float64(klines[i][2]) >=tmpMaxPrice:
                        tmpMaxPrice=float64(klines[i][2])
                        coutToMax=i
                        
                    buySellData=buySellData.replace("\n","")
                    
                    if buySellData.split("|")[7]  != "-4":
                        buySellData = self.testCheckForSell(buySellData,klines[i][2],0)
                        if debugProfit==1:
                            print(str(klines[i][4])+"   "+buySellData)
                    if i == 4*baonhieutieng-1:
                        if buySellData.split("|")[7] != "-4":
                            if debugProfit==1:
                                print(buySellData[buySellData.rfind("|")+1:])
                                print(buySellData)
                                print("Ban nong 2")
                            buySellData = self.testCheckForSell(buySellData,klines[i-1][2],1)

                profitFile.write(buySellData+"\n")   
                tongTien =  tongTien+round(float64(buySellData.split("|")[6]),10)


                checkTmp1=0
                if coutToMax >0:
                    for i1 in range (pos,coutToMax):
                        if tmpLowPrice>=float64(klines[i1][4]):
                            tmpLowPrice=float64(klines[i1][4])

                    #     if ichiStrategyRet[i1][7]ichiStrategyRet[i1][8]:
                    #         checkTmp1=1

                    # if checkTmp1 ==1:
                    #     checkIchiIntersect=checkIchiIntersect+1

                    lai = (tmpMaxPrice-float64(closePrice))/float64(closePrice)
                    lo = (float64(closePrice)-tmpLowPrice)/float64(closePrice) 
                    if lai >= profit and lo <=stoploss:
                        count2=count2+1 # so lenh thang
                        win.write(pair+"  date = "+tmpNow.strftime("%d %B %Y %H %M")+" start = "+str(closePrice)+ " low = "+str(tmpLowPrice)+" high = "+str(tmpMaxPrice)+" metric = "+str(metric)+"\n")
                        if lai >=0.5:
                            a50=a50+1
                        elif lai >=0.4:
                            a40=a40+1
                        elif lai >=0.3:
                            a30=a30+1
                        elif lai >=0.2:
                            a20=a20+1
                        elif lai >=0.1:
                            a10=a10+1
                        elif lai >=0.05:
                            a5=a5+1
                        elif lai >=0.03:
                            a3=a3+1

                        if lo >=0.20:
                            a30a=a30a+1
                        elif lo >=0.15:
                            a25a=a25a+1
                        elif lo >=0.13:
                            a20a=a20a+1
                        elif lo >=0.1:
                            a15a=a15a+1
                        elif lo >=0.08:
                            a10a=a10a+1
                        elif lo >=0.05:
                            a5a=a5a+1
                        elif lo > 0:
                            a3a=a3a+1
                        else:
                            a0a = a0a+1

                        # thoi gian cham max
                        coutToMax2 = coutToMax-pos
                        if coutToMax2 >=60:
                            t60=t60+1
                        elif coutToMax2 >=50:
                            t50=t50+1
                        elif coutToMax2 >=40:
                            t40=t40+1
                        elif coutToMax2 >=30:
                            t30=t30+1
                        elif coutToMax2 >=20:
                            t20=t20+1
                        elif coutToMax2 >=15:
                            t15=t15+1
                        elif coutToMax2 >=10:
                            t10=t10+1
                        else:
                            t5 = t5+1

                        print("===================================================")
                        print(str(count2)+"/"+str(count1))
                        print(float64(count2/count1))
                        print("Lai="+str(tongTien))
                        print("Tong tien ="+str(self.tien))
                        print("lai 3 % ="+str(a3))
                        print("lai 5 % ="+str(a5))
                        print("lai 10 % ="+str(a10))
                        print("lai 20 % ="+str(a20))
                        print("lai 30 % ="+str(a30))
                        print("lai 40 % ="+str(a40))
                        print("lai 50 % ="+str(a50))
                        print("\n")
                        print("Khong lo ="+str(a0a))
                        print("lo 0-5 % ="+str(a3a))
                        print("lo 5-8 % ="+str(a5a))
                        print("lo 8-10 % ="+str(a10a))
                        print("lo 10-13 % ="+str(a15a))
                        print("lo 13-15 % ="+str(a20a))
                        print("lo 15-20 % ="+str(a25a))
                        print("lo >20 % ="+str(a30a))
                        print("\n")
                        print("0-10 ="+str(t5))
                        print("t10 ="+str(t10))
                        print("t15 ="+str(t15))
                        print("t20 ="+str(t20))
                        print("t30 ="+str(t30))
                        print("t40 ="+str(t40))
                        print("t50 ="+str(t50))
                        print("t60 ="+str(t60))
                    else:
                        lose.write(pair+"  date = "+tmpNow.strftime("%d %B %Y %H %M")+" start = "+str(closePrice)+ " low = "+str(tmpLowPrice)+" high = "+str(tmpMaxPrice)+" metric = "+str(metric)+"\n")
        print("ty le thang = "+str(float64(count2/count1)))
        lose.close()
        win.close()  
        profitFile.close()

    def panic(self):
        pairs = self.getAllPair()
        allPair=""
        for a1 in pairs:
            if a1[-4:]=="USDT":
                allPair=allPair+"--"+a1
        

        balans = self.client.get_account()['balances']
        for balan in balans:
            if float64(balan['free'])>float64(0) and  "USDT" not in balan['asset'] and  "BNB" not in balan['asset']:
                newPair =balan['asset']+"USDT"
                if newPair in allPair:
                    freeToken = float64(balan['free'])
                    tokenPrice = float64(self.client.get_symbol_ticker(symbol=newPair)['price'])
                    tokenToUSDT = freeToken*tokenPrice
                    if tokenToUSDT > float64(11):
                        print(newPair)
                        self.sellAnyThings(newPair,float64(balan['free']),1)
        # print(balan)
        # for pair in self.getAllPair():
        #     if pair[-4:]=="USDT":
        #         token = pair[:-4]
        #         freeToken = float64(self.client.get_asset_balance(asset=token)['free'])
        #         tokenPrice = float64(self.client.get_symbol_ticker(symbol=pair)['price'])
        #         tokenToUSDT = freeToken*tokenPrice
        #         print(tokenToUSDT)
        #         if tokenToUSDT > float64(11):
        #             print(pair)

    def analysisLog(self,releaseIndicatorFile,reportFile):
        indicatorData = open(releaseIndicatorFile,"r").readlines()
        boughtCoinData = open("log/boughtCoin.txt").readlines()
        logBuyData = open("log/logBuy.txt").readlines()
        logSellData = open("log/logSell.txt").readlines()
        logTienData = open("log/logTien.txt").readlines()
        retData =""
        now = datetime.fromtimestamp(time.time())
        c = now.strftime("%H:%M:%S  %d/%m/%Y")
        retData+=str(c)+"\n"
        retData+="Current coin pair:"+"\n"
        for line in boughtCoinData:
            retData+=line+"\n"


        retData+="Queu indicator:"+"\n"
        for line in indicatorData:
            if len(line)>2 and "xxx" not in line:
                retData+=line+"\n"
        retData+="----------------------------"+"\n"
        retData+="Current profit:"+"\n"
        curMoney = float64(0)
        for line in boughtCoinData:
            line = line.split("|")
            if len(line)>3:
                pair = line[1]
                amount = line[4]
                curPrice = float64(self.client.get_symbol_ticker(symbol=pair)['price'])
                mon1 = curPrice*float64(amount)
                curMoney=curMoney+mon1
        for line in logBuyData:
            line = line.split("|")
            if len(line)>2:
                curMoney=curMoney-float64(line[2].replace("\n","").replace("$","").replace("amount:",""))

        for line in logSellData:
            line = line.split("|")
            if len(line)>2:
                curMoney=curMoney+float64(line[2].replace("\n","").replace("$","").replace("amount:",""))
        retData+=str(curMoney)+"\n"
        retData+="----------------------------"+"\n"
        retData+="Buy status:"+"\n"
        countMua=0
        countCatLoGiaTut13=0
        countTBG=0
        countDaoChieu=0
        for line in logBuyData:
            line = line.replace("\n","").split("|")
            if len(line)==3:
                countMua=countMua+1
            elif len(line)==4:
                if "TBG" in line[3]:
                    countTBG=countTBG+1
        retData+="So indicator da mua:"+str(countMua)+"\n"
        retData+="     So lan trung binh gia:"+str(countTBG)+"\n"
        retData+="----------------------------"+"\n"
        retData+="Sell status:"+"\n"

        hettg=0
        khongthe=0
        daochieu=0
        tut13=0
        lai3=0
        lai6=0
        lai10=0
        lai14=0
        for line in logSellData:
            line = line.replace("\n","")
            if line.count("|")>2:
                if "het thoi gian" in line:
                    hettg=hettg+1
                if "Khong the" in line:
                    khongthe=khongthe+1
                if "dao chieu" in line:
                    daochieu=daochieu+1
                if "tut 13%" in line:
                    tut13=tut13+1
                if "lai 3%" in line:
                    lai3=lai3+1
                if "lai 6%" in line:
                    lai6=lai6+1
                if "lai 10%" in line:
                    lai10=lai10+1
                if "lai 14%" in line:
                    lai14=lai14+1

        retData+="   Good new:"+"\n"
        retData+="     lai3:"+str(lai3)+"\n"
        retData+="     lai6:"+str(lai6)+"\n"
        retData+="     lai10:"+str(lai10)+"\n"
        retData+="     lai14:"+str(lai14)+"\n"
        retData+="     hettg:"+str(hettg)+"\n"
        retData+="\n   Bad new:"+"\n"
        retData+="     Loi:"+str(khongthe)+"\n"
        retData+="     daochieu:"+str(daochieu)+"\n"
        retData+="     cat lo vi tut 13%:"+str(tut13)+"\n"
        if "zzzz" == reportFile:
            print(retData)
        else:
            open(reportFile,"w").write(retData)

def main():
    parser = argparse.ArgumentParser(description="Example for store true & false")
    parser.add_argument('-mo','-mode', choices=['release', 'testStratergy', 'testIndicator', 'testAll', 'testBuy', 'analysisLog', 'panic'], dest="mode", action="store",required=1)
    parser.add_argument('-it','-indicatorfiletest', dest="indicatorFileTest", action="store",default="indicatorTest.txt")
    parser.add_argument('-ir','-indicatorfilerelease', dest="indicatorFileRelease", action="store",default="indicatorRelease.txt")
    parser.add_argument('-me','-metric', dest="metric",help="metric for each indicator", action="store",default="19")
    parser.add_argument('-kh','-klineHour', dest="kh",help="time each kline. 1H,15M....", action="store",default="1h")
    parser.add_argument('-tr','-timerange',help="time range for mode test. format: \"1 JAN, 2020++1 JAN, 2021\"", dest="timerange", action="store")
    parser.add_argument('-pa','-pair', dest="pair",help="Binance pair: BTCUSDT,DEGOUSDT...", action="store")

    parser.add_argument('-sba','-startbuyamount', dest="sba",help="so tien cho moi lenh", action="store",default="60")
    parser.add_argument('-lp','-logPath', dest="logPath",help="thu muc luu log cua truong trinh", action="store",default=".")
    parser.add_argument('-stl','-stoploss', dest="stl",help="stoploss for indicator check and buy sell token. example: 0.15 = 15/100", action="store",default="0.15")
    parser.add_argument('-pf','-profit', dest="pf",help="profit for indicator check and buy sell token. example: 0.03 = 3/100", action="store",default="0.03")
    parser.add_argument('-cy','-cycle', dest="cycle",help="cycle for each buy and sell token. example: 72 = 72 hours", action="store",default="72")
    parser.add_argument('-ar','-analysisreport',dest="ar",help="analysis report file", action="store",default="zzzz")
    parser.add_argument('-pl','-plot',dest="pl",help="plot buy spot on map", action="store_true",default=False)
    args = parser.parse_args()
    os.system("mkdir log")
    trader = Trader()
    if args.mode == "release":
        
        count =1
        symbols = trader.getAllPair()
        a1 = open("control.txt","a")
        a1.close()
        while True:
            data1 = open("control.txt","r").read()
            if "stopFindIndicator" not in data1:
                try:
                    for symbol in symbols:
                        print(symbol)
                        if len(symbol)>1:
                            trader.startCalculated(symbol,args.kh,args.indicatorFileRelease,2,int(args.metric),int(args.cycle))
                except:
                    ...

            for i in range(0,30):
                if "stopBuy" not in data1:
                    print("checkForBuy Call")
                    try:
                        trader.checkForBuy(args.indicatorFileRelease,args.sba,args.cycle)
                    except:
                        time.sleep(15)
                if "stopSell" not in data1:
                    print("checkForSell Call")         
                    trader.checkForSell("log/boughtCoin.txt",args.cycle)
                time.sleep(30)
        # trader.checkForBuy(args.indicatorFileRelease,args.sba,args.cycle) 

    elif args.mode == "testStratergy" or args.mode == "testAll":
        if args.timerange != None:
            print(args.timerange)
            open(args.indicatorFileTest,"w")
            
            timerange1=args.timerange.split("++")
            print(args.pair)
            print("123")
            if args.pair == None:
                for symbol in trader.getAllPair():
                    print(symbol)
                    if len(symbol)>1:
                        trader.startCalculatedInTimeRange(symbol,args.kh,args.indicatorFileTest,1,int(args.metric),timerange1[0],timerange1[1])
            if args.pair != None:
                print(args.pair )
                trader.draw = args.pl

                trader.startCalculatedInTimeRange(args.pair,args.kh,args.indicatorFileTest,1,int(args.metric),timerange1[0],timerange1[1])
            if args.mode == "testAll":
                trader.checkIndicatorRet(args.indicatorFileTest,int(args.metric),float64(args.pf),float64(args.stl),int(args.cycle))
        if args.timerange == None:
            print("need -timerange option: -tr \"1 JAN, 2021++1 FEB, 2021\"")
        
    elif args.mode == "testIndicator":
        trader.checkIndicatorRet(args.indicatorFileTest,int(args.metric),float64(args.pf),float64(args.stl),int(args.cycle))
    elif args.mode == "testBuy":
        # print(trader.buyAnyThings("BNBUSDT",11))
        # print(trader.sellAnyThings("TVKUSDT",100,1))
        trader.checka1()
    elif args.mode == "analysisLog":
        os.chdir(args.logPath)
        if args.ar=="zzzz":
            trader.analysisLog(args.indicatorFileRelease,args.ar)
        else:
            while True:
                try:
                    trader.analysisLog(args.indicatorFileRelease,args.ar)
                except:
                    ...
                print("checkRun")
                time.sleep(5*60) 
    elif args.mode == 'panic':
        trader.panic()
        
if __name__ == "__main__":
    main()