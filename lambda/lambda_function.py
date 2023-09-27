import logging
import ask_sdk_core.utils as ask_utils
from ask_sdk_model.er.dynamic import UpdateBehavior, EntityListItem, Entity, EntityValueAndSynonyms
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.dialog import DynamicEntitiesDirective
from urllib.request import urlopen
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_intent_name, get_supported_interfaces
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_model.interfaces.alexa.presentation.apl import RenderDocumentDirective
from datetime import datetime
import json
import math

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
sales_data = []
whaty=['turn over','sales','sale','production','productions','turnover']
wheny=['weekend','today','todays','yesterday','week','weeks','weekly','month','months','monthly','quarter','quarters','year','years','months','weeks','january','last']
whichy=['bottom','top','high','higher','highest','low','lower','lowest','average','compare','comparison']
proy=['material','product','by-product','sku','item']
add1=[]
add2=[]
add3=[]
whoy=[]
whatyy=-1
whenyy=-1
whichyy=-1
whoyy=-1
re_one=False

APL_DOCUMENT_ID = "first_try"

APL_DOCUMENT_TOKEN = "documentToken"

DATASOURCE = {
    "cardsLayoutTemplateData": {
        "type": "object",
        "properties": {
            "backgroundImage": "",
            "headerTitle": "Aeonx Digital",
            "headerSubtitle": "ETL Project",
            "headerAttributionImage": "https://www.aeonx.digital/wp-content/uploads/2022/03/42.png",
            "primaryText": "Welcome to ETL Project ! You can ask related to Sales ",
            "listItems": [
                {
                    "thumbnailImage": "https://www.aeonx.digital/wp-content/uploads/2022/12/About-Us-scaled.jpg"
                }
            ]
        }
    }
}

class fetch_dataHandler:
    def data_fetching_sales_new():
        url = "https://mitsonpar.github.io/json/data/datas.json"
        response = urlopen(url)
        data = json.loads(response.read())
        if len(sales_data)==0:
            mee=fetch_dataHandler.check_initials(data)
            helpy=''
            if len(mee)==1:
                helpy=data[mee[0]]
            elif len(mee)==2:
                helpy=data[mee[0]][mee[1]]
            elif len(mee)==3:
                helpy=data[mee[0]][mee[1]][mee[2]]
            for i in helpy:
                list_string=map(str,list(i.values()))
                ds=list(map(str.lower,list_string))
                sales_data.append(ds)
        return sales_data
    def check_initials(data):
        me=[]
        first=0
        second=0
        third=0
        keys=''
        for key in data:
            keys=key
            first=first+1
        if first==1:
            me.append(keys)
            for key in data[me[0]]:
                keys=key
                second=second+1
        if second==1:
            me.append(keys)
            for key in data[me[0]][me[1]]:
                keys=key
                third=third+1
        return me
    def last_date_prowise_new(checky,any,whos,whenss,whoss,whatss,whichss):
        if whoss!=-1:
            val=whos[whoss]
        app = []
        dty=[]
        qty=[]
        datey=0
        tempy=0
        first=0
        bully=False
        sully=False
        this_vary=False
        last_vary=False
        compare_vary=False
        here = 0
        here2 = 0
        here_qty2 = 0
        here_qty = 0
        diff = 0
        splitted_word = any.split(' ',-1)
        for io in splitted_word:
            if 'this'==io:
                this_vary=True
            elif 'last'==io:
                last_vary=True
            if whichy[9]==io or whichy[10]==io:
                compare_vary=True
        curr_date=datetime.today().strftime('%Y%m%d')
        #Find current date as last date in data
        for io in checky:
            for jo in io:
                ffor=jo[:3]
                ffors=jo[4:6]
                fforss=jo[6:8]
                if whoss!=-1:
                    if jo==val:
                        bully=True
                        if tempy>datey:
                            datey=tempy
                            tempy=0
                    if jo.isnumeric() and len(jo)==8 and int(ffor)==202 and int(ffors)<13 and int(fforss)<32:
                        if bully==True:
                            if datey<int(jo):
                                datey=int(jo)
                        else:
                            if datey<int(jo):
                                tempy=int(jo)
                            
                else:
                    if jo.isnumeric() and len(jo)==8 and int(ffor)==202 and int(ffors)<13 and int(fforss)<32:
                        if datey<int(jo):
                            datey=int(jo)
                first=first+1
            first=0
            bully=False
            tempy=0
        e_date=str(datey)
        s_date=''
        ee_date=str(datey)
        ss_date=''
        this_years=e_date[0:4]
        this_months=e_date[4:6]
        this_dates=e_date[6:8]
        this_year=int(this_years)
        this_month=int(this_months)
        this_date=int(this_dates)
        monthy=False
        #CREATE PERIOD - yesterday data
        if whenss==3:
            if compare_vary==True:
                ee_date=str(this_year)+str(this_month)+str(this_date)
            new_date=this_date-1
            if new_date==0:
                new_date=30
            if new_date<10:
                e_date=str(this_year)+str(this_month)+'0'+str(new_date)
            else:
                e_date=str(this_year)+str(this_month)+str(new_date)
        # this week data
        elif whenss==4 or whenss==5 or whenss==6:
            if compare_vary==True:
                this_vary=True
                last_vary=True
            if this_vary==True or last_vary==False:
                new_date=this_date-6
                if new_date<0:
                    if this_month>1:
                        this_month=this_month-1
                        monthy=True
                        new_date=30+new_date
                    else:
                        this_month=12
                        new_date=30+new_date
                else:
                    if new_date<10:
                        if compare_vary==True:
                            ss_date=str(this_year)+str(this_month)+'0'+str(new_date)
                        else:
                            s_date=str(this_year)+str(this_month)+'0'+str(new_date)
                    else:
                        if compare_vary==True:
                            ss_date=str(this_year)+str(this_month)+str(new_date)
                        else:
                            s_date=str(this_year)+str(this_month)+str(new_date)
            #changed elif to if
            if last_vary==True:
                new_date=this_date-13
                new_end_date=this_date-7
                if new_date<=0:
                    if this_month>1:
                        if monthy!=True:
                            this_month=this_month-1
                        new_date=30+new_date
                    else:
                        this_month=12
                        new_date=30+new_date
                elif new_end_date<0:
                    if this_month>1:
                        this_month=this_month-1
                        new_end_date=30+new_end_date
                    else:
                        this_month=12
                        new_end_date=30+new_end_date
                if this_month<10:
                    new_month='0'+str(this_month)
                else:
                    new_month=this_month
                if new_date<10:
                    new_date='0'+str(new_date)
                if new_end_date<10:
                    new_end_date='0'+str(new_end_date)
                s_date=str(this_year)+str(new_month)+str(new_date)
                e_date=str(this_year)+str(new_month)+str(new_end_date)
        #this month data
        elif whenss==7 or whenss==8 or whenss==9:
            if compare_vary==True:
                this_vary=True
                last_vary=True
            if this_vary==True or last_vary==False:
                if compare_vary==True:
                    ss_date=int(str(this_year)+str(this_month)+'01')
                else:
                    s_date=int(str(this_year)+str(this_month)+'01')
                this_vary=False
            if last_vary==True:
                new_month=str(this_month-1)
                if int(new_month)<10:
                    new_month='0'+new_month
                s_date=int(str(this_year)+new_month+'01')
                e_date=int(str(this_year)+new_month+'30')
        #quarter data
        elif whenss==10 or whenss==11:
            if compare_vary==True:
                this_vary=True
                last_vary=True
            if this_vary==True or last_vary==False:
                if this_month>0 and this_month<=3:
                    s_date=int(str(this_year)+'01'+'01')
                    e_date=int(str(this_year)+'03'+'31')
                elif this_month>3 and this_month<=6:
                    s_date=int(str(this_year)+'04'+'01')
                    e_date=int(str(this_year)+'06'+'31')
                elif this_month>6 and this_month<=9:
                    s_date=int(str(this_year)+'07'+'01')
                    e_date=int(str(this_year)+'09'+'30')
                elif this_month>9 and this_month<=12:
                    s_date=int(str(this_year)+'10'+'01')
                    e_date=int(str(this_year)+'12'+'31')
                if compare_vary==True:
                    ss_date=s_date
                    ee_date=e_date
                this_vary=False
            if last_vary==True:
                new_month=str(this_month-1)
                if this_month>0 and this_month<=3:
                    s_date=int(str(this_year-1)+'10'+'01')
                    e_date=int(str(this_year-1)+'12'+'31')
                elif this_month>3 and this_month<=6:
                    s_date=int(str(this_year)+'01'+'01')
                    e_date=int(str(this_year)+'03'+'31')
                elif this_month>6 and this_month<=9:
                    s_date=int(str(this_year)+'04'+'01')
                    e_date=int(str(this_year)+'06'+'31')
                elif this_month>9 and this_month<=12:
                    s_date=int(str(this_year)+'07'+'01')
                    e_date=int(str(this_year)+'09'+'30')
                last_vary=False
        # year data   
        elif whenss==12 or whenss==13:
            if compare_vary==True:
                this_vary=True
                last_vary=True
            if this_vary==True or last_vary==False:
                if compare_vary==True:
                    ss_date=int(str(this_year)+'01'+'01')
                else:
                    s_date=int(str(this_year)+'01'+'01')
            if last_vary==True:
                new_year=this_year-1
                s_date=str(new_year)+'01'+'01'
                e_date=str(new_year)+'12'+'31'
        elif whenss==1:
            s_date=''
            ss_date=''
        # fetching final output
        app_two=[]
        qty_two=[]
        dty_two=[]
        temp_datey=''
        gully=False
        stored=False
        store=''
        qty_store=''
        qty_stored=False
        for io in checky:
            for jo in io:
                #for prowise
                if whoss>-1:
                    if jo==val:
                        bully=True
                    ffor=jo[:3]
                    ffors=jo[4:6]
                    fforss=jo[6:8]
                    if jo.isnumeric():
                        if len(jo)==8 and int(ffor)==202 and int(ffors)<13 and int(fforss)<32:
                            # if bully==True:
                            if s_date!='' and int(jo)>=int(s_date) and int(jo)<=int(e_date):
                                sully=True
                                temp_datey=jo
                                # dty.append(jo)
                            if s_date=='' and int(jo)==int(e_date):
                                sully=True
                                temp_datey=jo
                                # dty.append(jo)
                            if ss_date!='' and int(jo)>=int(ss_date) and int(jo)<=int(ee_date):
                                gully=True
                                temp_datey=jo
                                # dty_two.append(jo)
                            elif ss_date=='' and int(jo)==int(ee_date):
                                gully=True
                                temp_datey=jo
                                # dty_two.append(jo)
                    if first==12:
                        qty_store=jo 
                        qty_stored=False
                    if first==14:
                        store=jo 
                        stored=False
                    if sully==True and bully==True:
                        dty.append(temp_datey)
                        if store!='' and stored==False and qty_store!='' and qty_stored==False:
                            another=round(float(store))
                            app.append(another)
                            stored=True
                            store=''
                            qty.append(float(qty_store))
                            qty_store=''
                            qty_stored=True
                            bully=False
                            sully=False
                    if gully==True and bully==True:
                        dty_two.append(temp_datey)
                        if store!='' and stored==False and qty_store!='' and qty_stored==False:
                            another=round(float(store))
                            app_two.append(another)
                            stored=True
                            store=''
                            qty_two.append(float(qty_store))
                            qty_store=''
                            qty_stored=True
                            bully=False
                            gully=False
                #not for prowise
                else:
                    ffor=jo[:3]
                    ffors=jo[4:6]
                    fforss=jo[6:8]
                    if jo.isnumeric():
                        if len(jo)==8 and int(ffor)==202 and int(ffors)<13 and int(fforss)<32:
                            if s_date!='' and int(jo)>=int(s_date) and int(jo)<=int(e_date):
                                sully=True
                                dty.append(jo)
                            elif s_date=='' and int(jo)==int(e_date):
                                sully=True
                                dty.append(jo)
                            if ss_date!='' and int(jo)>=int(ss_date) and int(jo)<=int(ee_date):
                                gully=True
                                dty_two.append(jo)
                            elif ss_date=='' and int(jo)==int(ee_date):
                                gully=True
                                dty_two.append(jo)
                    if first==12:
                        qty_store=jo 
                        qty_stored=False
                    if first==14:
                        store=jo 
                        stored=False
                    if sully==True:
                        if store!='' and stored==False and qty_store!='' and qty_stored==False:
                            another=round(float(store))
                            app.append(another)
                            stored=True
                            store=''
                            qty.append(float(qty_store))
                            qty_store=''
                            qty_stored=True
                            sully=False
                    if gully==True:
                        if store!='' and stored==False and qty_store!='' and qty_stored==False:
                            another=round(float(store))
                            app_two.append(another)
                            stored=True
                            store=''
                            qty_two.append(float(qty_store))
                            qty_store=''
                            qty_stored=True
                            gully=False
                first=first+1
            first=0
            store=''
            bully=False
            sully=False
            gully=False
        # ddt=len(set(dty))
        # ddt_new=len(set(dty_two))
        # if whichss==2 or whichss==3 or whichss==4:
        #     if len(app)>0 or len(app_two)>0:
        #         if compare_vary==True:
        #             if len(app)>0:
        #                 gy = max(app)
        #                 ceh = app.index(gy)
        #                 here= max(app)
        #                 here_qty =str(qty[ceh])
        #             else:
        #                 here=0
        #                 here_qty=0
        #             if len(app_two)>0:
        #                 sy = max(app_two)
        #                 seh = app_two.index(sy)
        #                 here2= max(app_two)
        #                 here_qty2 =str(qty_two[seh])
        #             else:
        #                 here2=0
        #                 here_qty2=0
        #             diff = here2-here
        #         else:
        #             gy=max(app)
        #             ceh=app.index(gy)
        #             here = max(app)
        #             here_qty =str(qty[ceh])
        #     else:
        #         here='You dont have data for the period you mentioned'
        # elif whichss==5 or whichss==6 or whichss==7:
        #     if len(app)>0 or len(app_two)>0:
        #         if compare_vary==True:
        #             if len(app)>0:
        #                 gy = min(app)
        #                 ceh = app.index(gy)
        #                 here= min(app)
        #                 here_qty =str(qty[ceh])
        #             else:
        #                 here=0
        #                 here_qty=0
        #             if len(app_two)>0:     
        #                 sy = min(app_two)
        #                 seh = app_two.index(sy)
        #                 here2= min(app_two)
        #                 here_qty2 =str(qty_two[seh])
        #             else:
        #                 here2=0
        #                 here_qty2=0
        #             diff = here2-here
        #         else:
        #             gy=min(app)
        #             ceh=app.index(gy)
        #             here = min(app)
        #             here_qty =str(qty[ceh])
        #     else:
        #         here='You dont have data for the period you mentioned'
        # elif whichss==8:
        #     if len(app)>0 or len(app_two)>0:
        #         if compare_vary==True:
        #             if len(app)>0:
        #                 here = sum(app)/ddt
        #                 here_qty =str(sum(qty)/ddt)
        #             else:
        #                 here = 0
        #                 here_qty=0
        #             if len(app_two)>0:
        #                 here2 = sum(app_two)/ddt_new
        #                 here_qty2 = str(sum(qty_two)/ddt_new)
        #             else:
        #                 here2 = 0
        #                 here_qty2= 0
        #             diff = here2 - here
        #         else:
        #             here = sum(app)/ddt
        #             here_qty =str(sum(qty)/ddt)
        #     else:
        #         here='You dont have data for the period you mentioned'
        # elif whichss==1:
        #     if len(app)>0 or len(app_two)>0:
        #         sorted_op=sorted(app, reverse=True)
        #         check=False
        #         #find number of top
        #         loopy=0
        #         here=''
        #         for io in splitted_word:
        #             if check==True:
        #                 loopy=int(io)
        #                 check=False
        #                 break
        #             if 'top'==io:
        #                 check=True
        #         if int(loopy)>0 and len(sorted_op)>int(loopy):
        #             last=0
        #             for ko in sorted_op:
        #                 if last==0:
        #                     here= str(ko)
        #                 elif last<loopy:
        #                     here= here+', '+str(ko)
        #                 last=last+1
        #         else:
        #             here='You forget to add top 3 or 5 or 10 !'
        #     else:
        #         here='You dont have data for the period you mentioned'
        # else:
        #     if len(app)>0 or len(app_two)>0:
        #         if compare_vary==True:
        #             if len(app)>0:
        #                 here= sum(app)
        #                 here_qty =str(math.fsum(qty))
        #             else:
        #                 here=0
        #                 here_qty=0
        #             if len(app_two)>0:
        #                 here2= sum(app_two)
        #                 here_qty2 = str(math.fsum(qty_two))
        #             else:
        #                 here2=0
        #                 here_qty2=0
        #             diff = here2-here
        #         else:
        #             here=sum(app)
        #             here_qty=str(math.fsum(qty))
        #     else:
        #         here=' You dont have data for the period you mentioned'
        # here=str(len(qty_two))+'-'+str(len(app_two))+'-'+str(len(app))+'-'+str(len(qty))
        # here =  str(s_date)+str(e_date)+'-'+ str(ss_date)+str(ee_date)
        return str(len(app))
        # str(s_date),str(e_date),fetch_dataHandler.qty_formatter(str(here)),fetch_dataHandler.qty_formatter(here_qty),str(ss_date),str(ee_date),fetch_dataHandler.qty_formatter(str(here2)),fetch_dataHandler.qty_formatter(here_qty2),fetch_dataHandler.qty_formatter(str(diff)),str(compare_vary)
    def date_formatter(dateyt):
        year=dateyt[:4]
        month=dateyt[4:6]
        date=dateyt[6:8]
        months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        month=months[int(month)-1]
        return date+"-"+month+"-"+year
    def qty_formatter(qty):
        h=float(qty)
        d = str(h - int(h))
        c=str(int(h))
        if len(c)>=6:
            set=3
        elif len(c)<6 and len(c)>=4:
            set=4
        elif len(c)<4 and len(c)>=3:
            set=5
        elif len(c)<3:
            set=6
        e=d[0:set]
        g=str(float(c)+float(e))
        return g
    def retrieve_user_words(che,valu,lreone,lwhaty,lwhatyy,lwhoy,lwhoyy,lwheny,lwhenyy,lwhichy,lwhichyy,ladd1,ladd2,ladd3):
        # if valu.rfind('.') > -1:
        #     valu = valu[:valu.rfind('.')] + '' + valu[valu.rfind('.') + 1: ]
        #     valu =valu.replace(". ","")
        splitted_word = valu.split(' ',-1)
        finalg=[]
        ladd0 = splitted_word
        for ho in ladd0:
            finalg.append(ho.lower())
        #collecting staticless data first
        for ho in finalg:
            if ho not in (whaty+ wheny+ whichy+ proy):
                ladd1.append(ho)
        tes=len(ladd1)
        firsty=0
        ko=0
        oky=''
        for xo in range(0,tes):
            ko=ko+1
            if oky=='':
                oky=ladd1[xo]
            else:
                oky=oky+' '+ladd1[xo]
            if ko!=1:
                ladd2.append(oky.lower())
                oky=ladd1[xo]
        ko=0
        oky=''
        for xo in range(0,tes):
            ko=ko+1
            if oky=='':
                oky=ladd1[xo]
            else:
                oky=oky+' '+ladd1[xo] 
            if ko>2:
                ladd3.append(oky.lower())
                oky=ladd1[xo-1]+' '+ladd1[xo]
        #comparing data from query
        for io in splitted_word:
            firsty=0
            for jo in lwhaty:
                if jo==io:
                    lwhatyy=firsty
                firsty=firsty+1
            firsty=0
            for so in lwheny:
                if so==io:
                    lwhenyy=firsty
                firsty=firsty+1
            firsty=0
            for lo in lwhichy:
                if lo==io:
                    if firsty<9:
                        lwhichyy=firsty
                firsty=firsty+1
        for ko in che:
            for koo in ko:
                for jo in ladd1:
                    if jo.lower()==koo.lower():
                        if jo not in lwhoy:
                            lwhoy.append(koo.lower())
                for kos in ladd2:
                    if kos.lower()==koo.lower():
                        if kos not in lwhoy:
                            lwhoy.append(koo.lower())
                for kooo in ladd3:
                    if kooo.lower()==koo.lower():
                        if kooo not in lwhoy:
                            lwhoy.append(koo.lower())
                firsty=firsty+1
            if len(whoy)>0:
                lwhoyy=len(whoy)-1
        return lwhatyy,lwhoyy,lwhenyy,lwhichyy,lwhoy,ladd1,ladd2,ladd3
    def which_calls(che,any,local_reone,whaty,whatyy,whoy,whoyy,wheny,whenyy,whichy,whichyy):
        myvar='You can ask only related to sales and production'
        if whatyy!=-1 and whoyy!=-1 and whenyy!=-1 and whichyy!=-1: 
            #1234
            s_date,e_date,here,qty,ss_date,ee_date,here2,qty2,diff,comp = fetch_dataHandler.last_date_prowise_new(che,any,whoy,whenyy,whoyy,whatyy,whichyy)
            if comp=='True':
                if s_date=='':
                    period1=' on '+fetch_dataHandler.date_formatter(e_date)
                    period2=' on '+fetch_dataHandler.date_formatter(ee_date)
                else:
                    period1=' on '+fetch_dataHandler.date_formatter(s_date)+' to '+fetch_dataHandler.date_formatter(e_date)
                    period2=' on '+fetch_dataHandler.date_formatter(ss_date)+' to '+fetch_dataHandler.date_formatter(ee_date)
                myvar=whichy[whichyy].capitalize() +' '+whichy[10]+' '+whaty[whatyy].capitalize() +" of "+ whoy[whoyy].capitalize() +" for " +period1+" quantity is "+qty+" MT and NET Value INR is "+here+" and "+period2+" quantity is "+qty2+" MT and NET Value INR is "+here2+" and difference of NET Value INR is "+diff+"."
            else:
                if s_date=='':
                    period=' on '+fetch_dataHandler.date_formatter(e_date)
                else:
                    period=' between '+fetch_dataHandler.date_formatter(s_date)+' to '+fetch_dataHandler.date_formatter(e_date)
                myvar=whichy[whichyy].capitalize() +" "+whaty[whatyy].capitalize() +" of "+ whoy[whoyy].capitalize() +" for " +wheny[whenyy]+period+" quantity is "+qty+" MT and NET Value INR is "+here+"."
            local_reone=True
        elif whoyy!=-1 and whenyy!=-1 and whichyy!=-1:
            #234
            myvar='Can you please confirm you want data of sales or production ?'
            local_reone=False
        elif whatyy!=-1 and whoyy!=-1 and whenyy!=-1:
            #123
            myvar=fetch_dataHandler.last_date_prowise_new(che,any,whoy,whenyy,whoyy,whatyy,whichyy)
            # s_date,e_date,here,qty,ss_date,ee_date,here2,here_qty2,diff,comp = fetch_dataHandler.last_date_prowise_new(che,any,whoy,whenyy,whoyy,whatyy,whichyy)
            # if comp=='True':
            #     if s_date=='':
            #         period1=' on '+fetch_dataHandler.date_formatter(e_date)
            #         period2=' on '+fetch_dataHandler.date_formatter(ee_date)
            #     else:
            #         period1=' on '+fetch_dataHandler.date_formatter(s_date)+' to '+fetch_dataHandler.date_formatter(e_date)
            #         period2=' on '+fetch_dataHandler.date_formatter(ss_date)+' to '+fetch_dataHandler.date_formatter(ee_date)
            #     myvar=whaty[whatyy].capitalize() +" of "+ whoy[whoyy].capitalize() +" for " +period2+" quantity is "+here_qty2+" MT and NET Value INR is "+here2+" and "+period1+" quantity is "+qty+" MT and NET Value INR is "+here+" and difference of NET Value INR is "+diff+"."
            # else:
            #     if s_date=='':
            #         period=' on '+fetch_dataHandler.date_formatter(e_date)
            #     else:
            #         period=' between '+fetch_dataHandler.date_formatter(s_date)+' to '+fetch_dataHandler.date_formatter(e_date)
            #     myvar=whaty[whatyy].capitalize() +" of "+ whoy[whoyy].capitalize() +" for " +wheny[whenyy]+period+" quantity is "+qty+" MT and NET Value INR is "+here+"."
            local_reone=True
        elif whatyy!=-1 and whoyy!=-1 and whichyy!=-1:
            #124
            myvar='Can you please confirm you want data of Highest, Lowest, Top 10 or Average ?'
            local_reone=False
        elif whatyy!=-1 and whenyy!=-1 and whichyy!=-1:
            #134
            s_date,e_date,here,qty,ss_date,ee_date,here2,here_qty2,diff,comp = fetch_dataHandler.last_date_prowise_new(che,any,whoy,whenyy,whoyy,whatyy,whichyy)
            if comp=='True':
                if s_date=='':
                    period1=' on '+fetch_dataHandler.date_formatter(e_date)
                    period2=' on '+fetch_dataHandler.date_formatter(ee_date)
                else:
                    period1=' on '+fetch_dataHandler.date_formatter(s_date)+' to '+fetch_dataHandler.date_formatter(e_date)
                    period2=' on '+fetch_dataHandler.date_formatter(ss_date)+' to '+fetch_dataHandler.date_formatter(ee_date)
                myvar=whichy[whichyy].capitalize() +' '+whichy[10]+' '+whaty[whatyy].capitalize() +" for " +period1+" quantity is "+qty+" MT and NET Value INR is "+here+" and "+period2+" quantity is "+here_qty2+" MT and NET Value INR is "+here2+" and difference of NET Value INR is "+diff+"."
            else:
                if s_date=='':
                    period=' on '+fetch_dataHandler.date_formatter(e_date)
                else:
                    period=' between '+fetch_dataHandler.date_formatter(s_date)+' to '+fetch_dataHandler.date_formatter(e_date)
                myvar=whichy[whichyy].capitalize() +" "+whaty[whatyy].capitalize() +" for " +wheny[whenyy]+period+" quantity is "+qty+" MT and NET Value INR is "+here+"." 
            local_reone=True
        elif whatyy!=-1 and whoyy!=-1:
            #12
            myvar='Can you please confirm you want data of today, yesterday, this month or this year ?'
            local_reone=False
        elif whatyy!=-1 and whenyy!=-1:
            #13
            # myvar = fetch_dataHandler.last_date_prowise_new(che,any,whoy,whenyy,whoyy,whatyy,whichyy)
            s_date,e_date,here,qty,ss_date,ee_date,here2,here_qty2,diff,comp = fetch_dataHandler.last_date_prowise_new(che,any,whoy,whenyy,whoyy,whatyy,whichyy)
            if comp=='True':
                if s_date=='':
                    period1=' on '+fetch_dataHandler.date_formatter(e_date)
                    period2=' on '+fetch_dataHandler.date_formatter(ee_date)
                else:
                    period1=' on '+fetch_dataHandler.date_formatter(s_date)+' to '+fetch_dataHandler.date_formatter(e_date)
                    period2=' on '+fetch_dataHandler.date_formatter(ss_date)+' to '+fetch_dataHandler.date_formatter(ee_date)
                myvar=whaty[whatyy].capitalize() +" for " +period2+" quantity is "+here_qty2+" MT and NET Value INR is "+here2+" and "+period1+" quantity is "+qty+" MT and NET Value INR is "+here+" and difference of NET Value INR is "+diff+"."
            else:
                if s_date=='':
                    period=' on '+fetch_dataHandler.date_formatter(e_date)
                else:
                    period=' between '+fetch_dataHandler.date_formatter(s_date)+' to '+fetch_dataHandler.date_formatter(e_date)
                myvar=whaty[whatyy].capitalize() +" for " +wheny[whenyy]+period+" quantity is "+qty+" MT and NET Value INR is "+here+"."
            local_reone=True
        elif whatyy!=-1 and whichyy!=-1:
            #14
            myvar='Can you please confirm you want data of today, yesterday, this month or this year ?'
            local_reone=False
        elif whoyy!=-1 and whichyy!=-1:
            #24
            myvar='Can you please confirm you want data of sales or production ?'
            local_reone=False
        elif whoyy!=-1 and whenyy!=-1:
            #23
            myvar='Can you please confirm you want data of sales or production ?'
            local_reone=False
        elif whichyy!=-1 and whenyy!=-1:
            #34
            myvar='Can you please confirm you want data of sales or production ?'
            local_reone=False
        elif whatyy!=-1:
            #1
            myvar='Can you please confirm you want data of which product e.g. Bentonite or Proppant ?'
            local_reone=False
        elif whoyy!=-1:
            #2
            myvar='Can you please confirm you want data of today, yesterday, this month or this year ?'
            local_reone=False
        elif whenyy!=-1:
            #3
            myvar='Can you please confirm you want data of Highest, Lowest, Top 10 or Average ?'
            local_reone=False
        elif whichyy!=-1:
            #4
            myvar='Can you please confirm you want data of sales or production ?'
            local_reone=False
        return local_reone,myvar

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        whatyy=-1
        whenyy=-1
        whichyy=-1
        whoyy=-1
        add1.clear()
        add2.clear()
        add3.clear()
        speak_output = "Welcome, you can ask company sales and production data. "
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)
    def supports_apl(self, handler_input):
        # Checks whether APL is supported by the User's device
        supported_interfaces = get_supported_interfaces(
            handler_input)
        return supported_interfaces.alexa_presentation_apl != None
    def launch_screen(self, handler_input):
        # Only add APL directive if User's device supports APL
        if self.supports_apl(handler_input):
            handler_input.response_builder.add_directive(
                RenderDocumentDirective(
                    token=APL_DOCUMENT_TOKEN,
                    document={
                        "type": "Link",
                        "src": f"doc://alexa/apl/documents/{APL_DOCUMENT_ID}"
                    },
                    datasources=DATASOURCE
                )
            )
    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"
        self.launch_screen(handler_input)
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
class passwordIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        
        return ask_utils.is_intent_name("passwordIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        any = slots["slotty"].value
        whaty.append(any)
        speak_output = any+ " added to the slots !"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response
class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response
class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True
    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class openaiIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("openaiIntent")(handler_input)

    def handle(self, handler_input):
        global re_one,whoy,whoyy,whaty,whatyy,whichy,whichyy,wheny,whenyy,add1,add2,add3
        checks=fetch_dataHandler.data_fetching_sales_new()
        slots = handler_input.request_envelope.request.intent.slots
        any = slots["hack"].value
        #splitting words below
        whatyy,whoyy,whenyy,whichyy,whoy,add1,add2,add3= fetch_dataHandler.retrieve_user_words(checks,any,re_one,whaty,whatyy,whoy,whoyy,wheny,whenyy,whichy,whichyy,add1,add2,add3)
        re_one,outputy=fetch_dataHandler.which_calls(checks,any,re_one,whaty,whatyy,whoy,whoyy,wheny,whenyy,whichy,whichyy)
        speak_output = " "+outputy
        # str(whatyy)+' '+str(whoyy)+' '+str(whenyy)+' '+str(whichyy)+' '+str(whoy)+' '+str(add1)
        if re_one:
            whatyy=-1
            whoyy=-1
            whenyy=-1
            whichyy=-1
            add1.clear()
            add2.clear()
            add3.clear()
            whoy.clear()
            re_one=False
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(passwordIntentHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(openaiIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()