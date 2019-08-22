# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 19:28:51 2017

@author: huang
"""

#coding=utf-8

import re
import os
import datetime

def writeFile(file,stocks,BS,day):
    for s in stocks:
        allfile.write('\n')
        allfile.write(day
                      +',"\''+s['code']
                      +'","'+s['name']
                      +'",'+str(float(BS[s['code']]['buy'])-float(BS[s['code']]['sell']))
                      +','+BS[s['code']]['buy']
                      +','+BS[s['code']]['sell']
                      +','+s['偏离值']
                      +',"'+s['成交量']
                      +'","'+s['成交金额(万元)']+'"')

        '''
        allfile.write(day
                      +",'"+s["code"]
                      +"','"+s["name"]
                      +"',"+str(float(BS[s["code"]]["buy"])-float(BS[s["code"]]["sell"]))
                      +","+BS[s["code"]]["buy"]
                      +","+BS[s["code"]]["sell"]
                      +","+s["偏离值"]
                      +",'"+s["成交量"]
                      +"','"+s["成交金额(万元)"]+"'")
        '''
        
path=r'./龙虎榜'
#path=r'./a'
files = os.listdir(path)
files.sort()

nowDayStr = ''
now = datetime.datetime.now()
nowStr = now.strftime("%Y-%m-%d")

allfile = open(r'./沪深龙虎榜统计_'+nowStr+'.csv','w')
allfile.write('"日期","代码","名称","净流入流出","流入","流出","偏离值","成交量","成交金额(万元)"')
for f in files:
    if(os.path.isfile(path+'/'+f) & f.startswith(nowStr) &f.endswith('.txt')):
        #print(path+'/'+f.replace('.txt',''))
        a = f.replace('.txt','').split('_')
        print('读取文件：'+path+'/'+f)
        '''
        if(nowDayStr!=a[0]):
            #print('a')
        else:
            #print('b')
            nowDayStr = a[0]
        '''
        nowDayStr = a[0]
        
        f=open(path+'/'+f,'rt')
        infos = f.readlines()
        f.close()

        if(a[1]=='上证'):
            #continue #test jump
            #上证
            readStocks = 1
            readBS = 0
            readBuy = 0
            readSell = 0
            nowStock = ''
            stocks = []
            BS = dict()
            buy = 0
            sell = 0
            for info in infos:
                
                info = re.sub('\ +', '_',info)
                info = re.sub('\n', '',info)
                
                #print('line:' +info)
                if(readStocks==1 and
                   info.startswith('_2')):
                    break
                if(readStocks==1 and
                   (not info.startswith('_证券代码:')) and
                   info.startswith('_(')):
                    
                    tmp = info.split('_')
                    dictTmp = {'code':tmp[2],'name':tmp[3],'偏离值':tmp[4],'成交量':tmp[5],'成交金额(万元)':tmp[6]}
                    stocks.append(dictTmp)
                    
                elif(readStocks==1 and
                     info.startswith('_证券代码:')):
                    
                    readStocks = 0
                    readBS = 1
                    #continue

                if(readBS==1 and
                   info.startswith('_证券代码')):
                    tmp = info.split('_')
                    #print('code:'+tmp[2])
                    nowStock = tmp[2]
                    readBS = 0
                    readBuy = 1
                    continue
                
                if(readBuy == 1 and
                   info.startswith('_(') and
                   (not info.startswith('_卖出'))):
                    tmp = info.split('_')
                    buy = buy + float(tmp[3])
                    #print('buy:'+str(buy))
                elif(readBuy == 1 and
                   info.startswith('_卖出')):
                    readBuy = 0
                    readSell = 1
                    continue
                
                if(readSell == 1 and
                   info.startswith('_(') and
                   ((not info.startswith('_2')) or
                   (not info.startswith('_证券')))):
                    tmp = info.split('_')
                    sell = sell + float(tmp[3])
                    #print('sell:'+str(sell))
                elif(readSell == 1 and
                   (info.startswith('_2') or
                   info.startswith('_证券'))):
                    readSell = 0
                    if(info.startswith('_证券')):
                        readBS = 1
                        #dictTmp = {nowStock:{'buy':str(buy),'sell':str(sell)}}
                        BS[nowStock]={'buy':str(buy),'sell':str(sell)};
                        buy = 0
                        sell = 0

                        if(readBS==1 and
                           info.startswith('_证券代码')):
                            tmp = info.split('_')
                            #print('code:'+tmp[2])
                            nowStock = tmp[2]
                            readBS = 0
                            readBuy = 1
                            continue
                        
                    else:
                        #dictTmp = {nowStock:{'buy':str(buy),'sell':str(sell)}}
                        BS[nowStock]={'buy':str(buy),'sell':str(sell)};
                        #write to doc
                        #print(stocks[0]['成交金额(万元)'])
                        #print(BS)
                        
                        writeFile(allfile,stocks,BS,nowDayStr);
                        break;
                    
        else:
            #深证，中小创
            
            readStocks = 0
            #readBS = 0
            readBuy = 0
            readSell = 0
            nowStock = ''
            stocks = []
            BS = dict()
            buy = 0
            sell = 0
            threeBlank = 0
            for info in infos:
                
                    
                if(info.startswith('--') and readStocks==1 and len(stocks)>1):
                    readStocks=1
                    readSell=0
                    BS[nowStock]={'buy':str(buy),'sell':str(sell)};
                    buy = 0
                    sell = 0
                    writeFile(allfile,stocks,BS,nowDayStr);
                    break;
                
                #print('-----'+info)
                if(threeBlank==3):
                    threeBlank = 0
                    haveBreaked = True
                else:
                    haveBreaked = False
                
                info = re.sub('\ +', '_',info)
                info = re.sub('\n', '',info)
                
                #print('line:' +info)
                if(info == ''):
                    threeBlank = threeBlank + 1
                    continue
                if((not info.startswith('日涨幅偏离值达到7%的前五只证券')) and
                   readStocks==0 and readBuy==0 and readSell==0):
                    continue
                elif(readStocks==0 and readBuy==0 and readSell==0):
                    
                    if(info.endswith('无')):
                        
                        break
                    readStocks=1
                    continue
                
                if(#haveBreaked and
                   readStocks==1 and
                   len(info.split('(代码'))>1):

                    if(info.startswith('--')):
                        #print(stocks)
                        #print(BS)
                        writeFile(allfile,stocks,BS,nowDayStr);
                        break;
                    #print('1'+info)
                    code = info.split('(代码')[1].split(')')[0]
                    name = info.split('(代码')[0]
                    plz = info.split('涨幅偏离值:')[1].split('_')[0]
                    cjl = info.split('成交量:')[1].split('_')[0]
                    cje = info.split('成交金额:_')[1]#.split('万元')[0]
                    nowStock = code
                    dictTmp = {'code':code,'name':name,'偏离值':plz,'成交量':cjl,'成交金额(万元)':cje}
                    stocks.append(dictTmp)
                    #print(dictTmp)
                    readStocks = 0
                    readBuy = 1
                    continue

                if(readBuy == 1 and info!='' and
                   (not info.startswith('买入金额最大的前5名')) and
                   (not info.startswith('营业部或交易单元名称')) ):
                    #print('1'+info)
                    if(info.startswith('卖出金额最大的前5名')):
                        readBuy=0
                        readSell=1
                        continue
                    else:
                        buy = buy + float(info.split('_')[1]) - float(info.split('_')[2])
                        continue

                if(readSell == 1 and info!='' and
                   (not info.startswith('营业部或交易单元名称')) ):
                    #print('2'+info)
                    
                    if(info.startswith('--')):
                        readStocks=1
                        readSell=0
                        
                        #dictTmp = {nowStock:{'buy':str(buy),'sell':str(sell)}}
                        #print(nowStock)
                        BS[nowStock]={'buy':str(buy),'sell':str(sell)};
                        
                        buy = 0
                        sell = 0
                        #print(stocks)
                        #print(BS)
                        writeFile(allfile,stocks,BS,nowDayStr);
                        break;
                        
                    if(len(info.split('代码'))>1):
                        readStocks=1
                        readSell=0
                        
                        #dictTmp = {nowStock:{'buy':str(buy),'sell':str(sell)}}
                        #print(nowStock)
                        BS[nowStock]={'buy':str(buy),'sell':str(sell)};
                        
                        buy = 0
                        sell = 0

                        #read code
                        #print('2'+info)
                        code = info.split('(代码')[1].split(')')[0]
                        name = info.split('(代码')[0]
                        plz = info.split('涨幅偏离值:')[1].split('_')[0]
                        cjl = info.split('成交量:')[1].split('_')[0]
                        cje = info.split('成交金额:_')[1]#.split('万元')[0]
                        nowStock = code
                        dictTmp = {'code':code,'name':name,'偏离值':plz,'成交量':cjl,'成交金额(万元)':cje}
                        stocks.append(dictTmp)
                        #print(dictTmp)
                        readStocks = 0
                        readBuy = 1
                        continue
                        
                    else:
                        sell = sell - float(info.split('_')[1]) + float(info.split('_')[2])
                        continue
                
        #break


allfile.close();
print('统计完成！'+'文件：'+'./沪深龙虎榜统计_'+nowStr+'.csv')