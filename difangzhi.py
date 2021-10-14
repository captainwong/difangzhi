import re
import os
import time
import requests
from bs4 import BeautifulSoup


class difangzhi:
    def __init__(self, ch, a, name, baseurl):
        self.ch = ch
        self.a = a
        self.name = name
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        self.baseurl = baseurl
        self.f = open(name + ".md", "w", encoding='utf-8')

    def build_url(self, a, ch, rec = None):
        return self.baseurl + "&K=" + self.ch + "&A=" + str(a) + ("&rec="+rec if rec else '') +  "&run=" + ("13" if rec else '12')

    def index(self):
        try:
            url = self.build_url(self.a, self.ch)
            res = requests.get(url, headers = {'user-agent' : self.user_agent})
            if res.status_code == 200:
                text = res.content
                text = text.decode('gbk', 'ignore')
                self.parse_data(text)
        except Exception as e:
            print('请求异常({})'.format(e))

    def write_chapter(self, chapter, title, data):
        if data.startswith(title):
            self.f.write('#' * (len(chapter) + 1) + ' ' + data + "\r\n")
        else:
            self.f.write('#' * (len(chapter) + 1) + ' ' + title + "\r\n")
            self.f.write(data + "\r\n")
        self.f.flush()
        pass

    def parse_chapter(self, data):
        soup = BeautifulSoup(data, "html.parser")
        divs = soup.find_all("div", class_='txt')
        if len(divs) > 0:
            return divs[0].text.strip()        
        return None

    def download_chapter(self, chapter, title, url):
        try:
            res = requests.get(url, headers = {'user-agent' : self.user_agent})
            if res.status_code == 200:
                text = res.content
                text = text.decode('gbk', 'ignore')
                data = self.parse_chapter(text)
                if data:
                    self.write_chapter(chapter, title, data)
                else:
                    self.write_chapter(chapter, title, title)

        except Exception as e:
            print('请求异常({})'.format(e))

    def get_rec(self, href):
        tag = 'javascript:sf(' + str(self.a) + ','
        index = href.find(tag)
        if index >= 0:
            i2 = href.find(',', len(tag))
            if i2 > index:
                rec = href[len(tag):i2]
                return rec
        return None

    def parse_data(self, html):
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all("a")
        for tag in links:
            #print(str(tag))
            if 'name' in tag.attrs:
                aname = tag.attrs['name']
                index = aname.find(self.ch)
                if index == 0:
                    chapter = aname[len(self.ch):]
                    title = tag.text.strip()
                    rec = self.get_rec(tag.attrs['href'])
                    if rec:
                        url = self.build_url(self.a, aname, rec)
                        print(chapter, title, url)
                        self.download_chapter(chapter, title, url)
                    else:
                        print("error, find rec failed", tag.attrs['href'])
                    #return


if __name__ == '__main__':
    #d = difangzhi('CH9', 3, u'东明县志（1986--2005）', 'http://lib.sdsqw.cn/bin/mse.exe?')
    #d.index()

    d = difangzhi('CH9', 1, u'东明县志', 'http://lib.sdsqw.cn/bin/mse.exe?')
    d.index()

    #d.download_chapter('1', u'魅力东明', 'http://lib.sdsqw.cn/bin/mse.exe?COLLCC=4108678863&K=CH91&A=3&rec=1&run=12')
    #d.parse_chapter('')
    #return

    html = """

<html>
	<head>
		<title>全文检索</title>
		<META HTTP-EQUIV="Content-Type" content="text/html; charset=gb2312">
		<style type='text/css'> <!-- A{text-decoration:none;color:#0000ff}
	a:hover{text-decoration:underline;color:#ff00FF}
	text{text-decoration: none;color:#00ffff}
	//--></style>
		<SCRIPT>
<!--
function sf(a,rec,by){//打开一条纪录run=13
var sern0="aa";
sern0=self.location.pathname+"?";
sern1="seachword="+escape(seachword);
sern1+="&K="+K;
sern1+="&A="+a;
sern1+="&rec="+rec;
sern1+="&run="+13;
//alert(sern0+sern1);
//self.location=sern0+sern1;//在自己的窗口内显示
show_rec=window.open(sern0+sern1,"show_rec","width=770,height=580,toolbar=yes,directories=yes,location=yes,status=yes,scrollbars=yes,menubar=yes,resizable=yes");
show_rec.focus();//打开新的窗口聚焦在前面
return;
}
function sp(list1,totle){ //run=11
var sern0="aa";
sern0=self.location.pathname+"?";
sern1="seachword="+escape(seachword);
sern1+="&K="+K;
sern1+="&A="+A;
sern1+="&rec="+rec;
if(list1<=1) list1=1;
if(list1>totle) list1=totle;
sern1+="&list="+list1;
//if(page=="") page=100;
sern1+="&page="+page;
sern1+="&run="+12;
//alert(sern0+sern1);
self.location=sern0+sern1;//在自己的窗口内显示
//show_rec=window.open(sern0+sern1,"show_rec","width=770,height=580,toolbar=yes,directories=yes,location=yes,status=yes,scrollbars=yes,menubar=yes,resizable=yes");
//show_rec.focus();//打开新的窗口聚焦在前面
return;
}
function listk(kk,aa){//打开一个库目录run=12
var sern0="aa";
sern0=self.location.pathname+"?";
sern1="seachword="+escape(seachword);
sern1+="&K="+kk;
sern1+="&A="+aa;
//sern1+="&rec="+rec;
sern1+="&run="+12+"#0";
//alert(sern0+sern1);
//self.location=sern0+sern1;//在自己的窗口内显示
show_list=window.open(sern0+sern1,"serch");
show_list.focus();//打开新的窗口聚焦在前面
return;
}


function Button1_onclick() {
//alert(escape(document.SER.Text1.value));
//document.SER.Text1.value+=unescape((document.SER.Text1.value))
//alert(unescape((document.SER.Text1.value)));
//return;
	if (document.SER.Text1.value=='')
		{
			alert("请输入检索词");
			return;
		}
		if(document.SER.Select1.value=="0") ss="/ftr/ftr.htm";
		else ss="/bin/mse.exe";
	ss+="?&seachword=";
		ss+=escape(document.SER.Text1.value);
	ss+="&K=";
		if(document.SER.Select1.value=='') ss+=K;
		else ss+=document.SER.Select1.value;
	ss+="&run=";//功能检索run=11
		ss+=document.SER.Hidden1.value;
	ss+="&list=";//列出当前页
		ss+=document.SER.Hidden2.value;
	ss+="&page=";//列出当前页
		ss+=document.SER.Hidden3.value;

//parent.frames[0].location=ss;
show_serch=window.open(ss,"serch");
show_serch.focus();//打开新的窗口聚焦在前面
//window.open(ss,"serch");  
//window.location.replace(ss);
return;
}


function on(){//初始值
sern0=self.location.pathname+"?";
sern1=seachword;
document.SER.Text1.value=sern1;
document.SER.Select1.value=K;
//alert(sern0+sern1);
return;
}
//-->
		</SCRIPT>
	</head>
	<body bgcolor="#edf0f5" onLoad="on();">
		
            
		<div align="center">	
        <table border="0" width="775" cellspacing="0" cellpadding="0" ID="Table2">
          <tr>
            <td width="129">
            <a href="http://lib.sdsqw.cn/ftr/ftr.htm" target="home"><img border="0" src="/images/01.gif" width="129" height="121"></a></td>
            <td width="156">
            <a href="http://lib.sdsqw.cn/ftr/ftr.htm" target="home"><img border="0" src="/images/02.gif" width="156" height="121"></a></td>
            <td width="335"><a href="http://lib.sdsqw.cn/ftr/ftr.htm" target="home"><img border="0" src="/images/03.gif" width="335" height="121"></a></td>
            <td width="156"><a href="http://lib.sdsqw.cn/ftr/ftr.htm" target="home"><img border="0" src="/images/04.gif" width="156" height="121"></a></td>
          </tr>
        </table> 
        </div>	<p align='center'>	
		<FORM name="SER" action="/bin/mse.exe" method="get">
			<table border="0" width="605" cellspacing="0" cellpadding="0" bgcolor="#99ccff" ID="Table1">
				<tr>
					<td width="106">请输入检索词
					</td>
					<td width="149">
						<INPUT name="Text1" type="text">
					</td>
					<td width="128">
						<SELECT name="Select1">
							<OPTION value="0" selected>全部</OPTION>
				<OPTION value="a">首轮省志</OPTION>
				<OPTION value="d00">山东年鉴</OPTION>
				<OPTION value="g0">二轮省志</OPTION>
				<OPTION value="f063">山东地情资料</OPTION>
				<OPTION value="fa01">山东方志文献</OPTION>
				<OPTION value="zzmj">诸子名家库
				</OPTION>
						</SELECT>
						<INPUT name="Hidden1" type="hidden" value="11" size="1"> <INPUT name="Hidden3" type="hidden" value="20" size="1">
						<INPUT name="Hidden2" type="hidden" value="1" size="1">
					</td>
					<td width="53">
						<INPUT id="Button1" onclick="return Button1_onclick()" type="button" value="检索" name="Button">
					</td>
					<td width="159">
					</td>
				</tr>
			</table>
		</FORM>
<SCRIPT>
seachword='';
K='ch9';
A='3';
run='12';
list='';
page='';
rec='';
</SCRIPT>

  
<br><br> 	   <TABLE borderColorDark=#73A6DD cellPadding=2 bgColor=#E6F0FF borderColorLight=#73A6DD border=1> 			<tr><tr><td width='600'colspan='5'bgcolor='#B8D1F3'><p align='center'> 东明县情资料库</td></tr>

</tr><tr><td width='200'><A HREF=javascript:listk('ch9','1')>  1 东明县志 </A></td> <td width='200'><A HREF=javascript:listk('ch9','2')>  2 东明人物 </A></td> <td width='200'><A HREF=javascript:listk('ch9','3')>  3 东明县志（1986--2005） </A></td> <td width='200'><A HREF=javascript:listk('ch9','4')>  4 东明年鉴（2013） </A></td> <td width='200'><A HREF=javascript:listk('ch9','5')>  5 东明年鉴（2014） </A></td> 

</tr><tr><td width='200'><A HREF=javascript:listk('ch9','6')>  6 东明年鉴（2015） </A></td> <td width='200'><A HREF=javascript:listk('ch9','7')>  7 东明民俗 </A></td> <td width='200'><A HREF=javascript:listk('ch9','8')>  8 东明风物 </A></td> <td width='200'><A HREF=javascript:listk('ch9','9')>  9 东明年鉴（2016） </A></td> <td width='200'><A HREF=javascript:listk('ch9','10')>  10 东明艺文 </A></td> 

</tr><tr><td width='200'><A HREF=javascript:listk('ch9','11')>  11 东明年鉴（2017） </A></td> <td width='200'><A HREF=javascript:listk('ch9','12')>  12 东明县便民实用手册 </A></td> <td width='200'><A HREF=javascript:listk('ch9','13')>  13 东明年鉴（2018） </A></td> <td width='200'><A HREF=javascript:listk('ch9','14')>  14 东明年鉴（2019） </A></td> <td width='200'>　</td> </tr></table><a name=0 id=0>　</a><br>当前资料是 东明县情资料库 <b>东明县志（1986--2005）</b>  全库目录 
<br><br><hr>
<br><A HREF=javascript:sf(3,1,'CH91') NAME='CH91'>魅力东明</A>
<br><A HREF=javascript:sf(3,2,'CH92') NAME='CH92'>东明县地方史志编纂委员会暨《东明县志》编审人员</A>
<br><A HREF=javascript:sf(3,3,'CH921') NAME='CH921'>　东明县地方史志编纂委员会</A>
<br><A HREF=javascript:sf(3,4,'CH922') NAME='CH922'>　《东明县志》编审人员</A>
<br><A HREF=javascript:sf(3,5,'CH93') NAME='CH93'>序</A>
<br><A HREF=javascript:sf(3,6,'CH94') NAME='CH94'>凡例</A>
<br><A HREF=javascript:sf(3,7,'CH95') NAME='CH95'>概 述</A>
<br><A HREF=javascript:sf(3,8,'CH96') NAME='CH96'>大事记</A>
<br><A HREF=javascript:sf(3,9,'CH9601') NAME='CH9601'>　1986年</A>
<br><A HREF=javascript:sf(3,10,'CH9602') NAME='CH9602'>　1987年</A>
<br><A HREF=javascript:sf(3,11,'CH9603') NAME='CH9603'>　1988年</A>
<br><A HREF=javascript:sf(3,12,'CH9604') NAME='CH9604'>　1989年</A>
<br><A HREF=javascript:sf(3,13,'CH9605') NAME='CH9605'>　1990年</A>
<br><A HREF=javascript:sf(3,14,'CH9606') NAME='CH9606'>　1991年</A>
<br><A HREF=javascript:sf(3,15,'CH9607') NAME='CH9607'>　1992年</A>
<br><A HREF=javascript:sf(3,16,'CH9608') NAME='CH9608'>　1993年</A>
<br><A HREF=javascript:sf(3,17,'CH9609') NAME='CH9609'>　1994年</A>
<br><A HREF=javascript:sf(3,18,'CH9610') NAME='CH9610'>　1995年</A>
<br><A HREF=javascript:sf(3,19,'CH9611') NAME='CH9611'>　1996年</A>
<br><A HREF=javascript:sf(3,20,'CH9612') NAME='CH9612'>　1997年</A>
<br><A HREF=javascript:sf(3,21,'CH9613') NAME='CH9613'>　1998年</A>
<br><A HREF=javascript:sf(3,22,'CH9614') NAME='CH9614'>　1999年</A>
<br><A HREF=javascript:sf(3,23,'CH9615') NAME='CH9615'>　2000年</A>
<br><A HREF=javascript:sf(3,24,'CH9616') NAME='CH9616'>　2001年</A>
<br><A HREF=javascript:sf(3,25,'CH9617') NAME='CH9617'>　2002年</A>
<br><A HREF=javascript:sf(3,26,'CH9618') NAME='CH9618'>　2003年</A>
<br><A HREF=javascript:sf(3,27,'CH9619') NAME='CH9619'>　2004年</A>
<br><A HREF=javascript:sf(3,28,'CH9620') NAME='CH9620'>　2005年</A>
<br><A HREF=javascript:sf(3,29,'CH97') NAME='CH97'>第一编  区域  环境</A>
<br><A HREF=javascript:sf(3,30,'CH971') NAME='CH971'>　第一章  建置  区划</A>
<br><A HREF=javascript:sf(3,31,'CH9711') NAME='CH9711'>　　第一节  地理位置</A>
<br><A HREF=javascript:sf(3,32,'CH9712') NAME='CH9712'>　　第二节  建置沿革</A>
<br><A HREF=javascript:sf(3,33,'CH9713') NAME='CH9713'>　　第三节  行政区划</A>
<br><A HREF=javascript:sf(3,34,'CH9714') NAME='CH9714'>　　第四节  县城</A>
<br><A HREF=javascript:sf(3,35,'CH972') NAME='CH972'>　第二章  自然环境</A>
<br><A HREF=javascript:sf(3,36,'CH9721') NAME='CH9721'>　　第一节  地  质</A>
<br><A HREF=javascript:sf(3,37,'CH97211') NAME='CH97211'>　　　一、构造</A>
<br><A HREF=javascript:sf(3,38,'CH97212') NAME='CH97212'>　　　二、地层</A>
<br><A HREF=javascript:sf(3,39,'CH9722') NAME='CH9722'>　　第二节  地  貌</A>
<br><A HREF=javascript:sf(3,40,'CH97221') NAME='CH97221'>　　　一、地貌特征</A>
<br><A HREF=javascript:sf(3,41,'CH97222') NAME='CH97222'>　　　二、地貌类型及分布</A>
<br><A HREF=javascript:sf(3,42,'CH9723') NAME='CH9723'>　　第三节  土壤植被</A>
<br><A HREF=javascript:sf(3,43,'CH97231') NAME='CH97231'>　　　一、土壤类型及分布</A>
<br><A HREF=javascript:sf(3,44,'CH97232') NAME='CH97232'>　　　二、土壤质量</A>
<br><A HREF=javascript:sf(3,45,'CH97233') NAME='CH97233'>　　　三、植被</A>
<br><A HREF=javascript:sf(3,46,'CH9724') NAME='CH9724'>　　第四节  气  候</A>
<br><A HREF=javascript:sf(3,47,'CH97241') NAME='CH97241'>　　　一、气候特征</A>
<br><A HREF=javascript:sf(3,48,'CH97242') NAME='CH97242'>　　　二、日照</A>
<br><A HREF=javascript:sf(3,49,'CH97243') NAME='CH97243'>　　　三、气温</A>
<br><A HREF=javascript:sf(3,50,'CH97244') NAME='CH97244'>　　　四、风和气压</A>
<br><A HREF=javascript:sf(3,51,'CH97245') NAME='CH97245'>　　　五、降水</A>
<br><A HREF=javascript:sf(3,52,'CH97246') NAME='CH97246'>　　　六、地温</A>
<br><A HREF=javascript:sf(3,53,'CH97247') NAME='CH97247'>　　　七、湿度与蒸发</A>
<br><A HREF=javascript:sf(3,54,'CH97248') NAME='CH97248'>　　　八、霜期与冻土</A>
<br><A HREF=javascript:sf(3,55,'CH97249') NAME='CH97249'>　　　九、气候在动植物方面的体现</A>
<br><A HREF=javascript:sf(3,56,'CH9725') NAME='CH9725'>　　第五节  河  流</A>
<br><A HREF=javascript:sf(3,57,'CH97251') NAME='CH97251'>　　　一、黄河</A>
<br><A HREF=javascript:sf(3,58,'CH97252') NAME='CH97252'>　　　二、洙赵新河水系</A>
<br><A HREF=javascript:sf(3,59,'CH97253') NAME='CH97253'>　　　三、东鱼河水系</A>
<br><A HREF=javascript:sf(3,60,'CH9726') NAME='CH9726'>　　第六节  自然资源</A>
<br><A HREF=javascript:sf(3,61,'CH97261') NAME='CH97261'>　　　一、土地资源</A>
<br><A HREF=javascript:sf(3,62,'CH97262') NAME='CH97262'>　　　二、水资源</A>
<br><A HREF=javascript:sf(3,63,'CH97263') NAME='CH97263'>　　　三、生物资源</A>
<br><A HREF=javascript:sf(3,64,'CH97264') NAME='CH97264'>　　　四、矿产资源</A>
<br><A HREF=javascript:sf(3,65,'CH9727') NAME='CH9727'>　　第七节  自然灾害</A>
<br><A HREF=javascript:sf(3,66,'CH97271') NAME='CH97271'>　　　一、旱灾</A>
<br><A HREF=javascript:sf(3,67,'CH97272') NAME='CH97272'>　　　二、洪涝灾</A>
<br><A HREF=javascript:sf(3,68,'CH97273') NAME='CH97273'>　　　三、风灾</A>
<br><A HREF=javascript:sf(3,69,'CH97274') NAME='CH97274'>　　　四、雹灾</A>
<br><A HREF=javascript:sf(3,70,'CH97275') NAME='CH97275'>　　　五、病虫灾害</A>
<br><A HREF=javascript:sf(3,71,'CH97276') NAME='CH97276'>　　　六、局温灾害</A>
<br><A HREF=javascript:sf(3,72,'CH97277') NAME='CH97277'>　　　七、霜冻灾害</A>
<br><A HREF=javascript:sf(3,73,'CH973') NAME='CH973'>　第三章  环境保护</A>
<br><A HREF=javascript:sf(3,74,'CH9731') NAME='CH9731'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,75,'CH9732') NAME='CH9732'>　　第二节  环境状况</A>
<br><A HREF=javascript:sf(3,76,'CH9733') NAME='CH9733'>　　第三节  环境监测</A>
<br><A HREF=javascript:sf(3,77,'CH9734') NAME='CH9734'>　　第四节  污染防治</A>
<br><A HREF=javascript:sf(3,78,'CH9735') NAME='CH9735'>　　第五节  环境管理</A>
<br><A HREF=javascript:sf(3,79,'CH9736') NAME='CH9736'>　　第六节  环保宣传教育</A>
<br><A HREF=javascript:sf(3,80,'CH98') NAME='CH98'>第二编  人  口</A>
<br><A HREF=javascript:sf(3,81,'CH981') NAME='CH981'>　第一章  人口状况</A>
<br><A HREF=javascript:sf(3,82,'CH9811') NAME='CH9811'>　　第一节  人口数量</A>
<br><A HREF=javascript:sf(3,83,'CH9812') NAME='CH9812'>　　第二节  人口分布与密度</A>
<br><A HREF=javascript:sf(3,84,'CH982') NAME='CH982'>　第二章  人口构成</A>
<br><A HREF=javascript:sf(3,85,'CH9821') NAME='CH9821'>　　第一节  民族构成</A>
<br><A HREF=javascript:sf(3,86,'CH9822') NAME='CH9822'>　　第二节  性别构成</A>
<br><A HREF=javascript:sf(3,87,'CH9823') NAME='CH9823'>　　第三节  文化构成</A>
<br><A HREF=javascript:sf(3,88,'CH9824') NAME='CH9824'>　　第四节  行业职业构成</A>
<br><A HREF=javascript:sf(3,89,'CH9825') NAME='CH9825'>　　第五节  年龄构成</A>
<br><A HREF=javascript:sf(3,90,'CH9826') NAME='CH9826'>　　第六节  姓氏构成</A>
<br><A HREF=javascript:sf(3,91,'CH9827') NAME='CH9827'>　　第七节  婚姻家庭</A>
<br><A HREF=javascript:sf(3,92,'CH983') NAME='CH983'>　第三章  人口变动</A>
<br><A HREF=javascript:sf(3,93,'CH9831') NAME='CH9831'>　　第一节  自然变动</A>
<br><A HREF=javascript:sf(3,94,'CH9832') NAME='CH9832'>　　第二节  机械变动</A>
<br><A HREF=javascript:sf(3,95,'CH9833') NAME='CH9833'>　　第三节  流动人口</A>
<br><A HREF=javascript:sf(3,96,'CH984') NAME='CH984'>　第四章  人口控制</A>
<br><A HREF=javascript:sf(3,97,'CH9841') NAME='CH9841'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,98,'CH9842') NAME='CH9842'>　　第二节  政策规定</A>
<br><A HREF=javascript:sf(3,99,'CH98421') NAME='CH98421'>　　　晚婚晚育</A>
<br><A HREF=javascript:sf(3,100,'CH98422') NAME='CH98422'>　　　避孕节育</A>
<br><A HREF=javascript:sf(3,101,'CH98423') NAME='CH98423'>　　　奖励扶助</A>
<br><A HREF=javascript:sf(3,102,'CH9843') NAME='CH9843'>　　第三节  宣传教育</A>
<br><A HREF=javascript:sf(3,103,'CH9844') NAME='CH9844'>　　第四节  技术服务</A>
<br><A HREF=javascript:sf(3,104,'CH9845') NAME='CH9845'>　　第五节  优生优育</A>
<br><A HREF=javascript:sf(3,105,'CH99') NAME='CH99'>第三编  基础设施建设</A>
<br><A HREF=javascript:sf(3,106,'CH991') NAME='CH991'>　第一章  城乡建设</A>
<br><A HREF=javascript:sf(3,107,'CH9911') NAME='CH9911'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,108,'CH9912') NAME='CH9912'>　　第二节  城乡规划</A>
<br><A HREF=javascript:sf(3,109,'CH9913') NAME='CH9913'>　　第三节  县城建设</A>
<br><A HREF=javascript:sf(3,110,'CH99131') NAME='CH99131'>　　　―、道路  桥梁</A>
<br><A HREF=javascript:sf(3,111,'CH99132') NAME='CH99132'>　　　二、供排水</A>
<br><A HREF=javascript:sf(3,112,'CH99133') NAME='CH99133'>　　　三、环境卫生</A>
<br><A HREF=javascript:sf(3,113,'CH99134') NAME='CH99134'>　　　四、城区绿化</A>
<br><A HREF=javascript:sf(3,114,'CH99135') NAME='CH99135'>　　　五、城区照明</A>
<br><A HREF=javascript:sf(3,115,'CH9914') NAME='CH9914'>　　第四节  城建管理</A>
<br><A HREF=javascript:sf(3,116,'CH9915') NAME='CH9915'>　　第五节  村镇建设</A>
<br><A HREF=javascript:sf(3,117,'CH9916') NAME='CH9916'>　　第六节  房地产业</A>
<br><A HREF=javascript:sf(3,118,'CH99161') NAME='CH99161'>　　　一、城镇住房制度</A>
<br><A HREF=javascript:sf(3,119,'CH99162') NAME='CH99162'>　　　二、房地产开发</A>
<br><A HREF=javascript:sf(3,120,'CH99163') NAME='CH99163'>　　　三、房地产管理</A>
<br><A HREF=javascript:sf(3,121,'CH9917') NAME='CH9917'>　　第七节 建筑业</A>
<br><A HREF=javascript:sf(3,122,'CH99171') NAME='CH99171'>　　　一、建筑设计</A>
<br><A HREF=javascript:sf(3,123,'CH99172') NAME='CH99172'>　　　二、建筑设备</A>
<br><A HREF=javascript:sf(3,124,'CH99173') NAME='CH99173'>　　　三、建筑队伍</A>
<br><A HREF=javascript:sf(3,125,'CH99174') NAME='CH99174'>　　　四、建筑管理</A>
<br><A HREF=javascript:sf(3,126,'CH992') NAME='CH992'>　第二章  交  通</A>
<br><A HREF=javascript:sf(3,127,'CH9921') NAME='CH9921'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,128,'CH9922') NAME='CH9922'>　　第二节  交通设施</A>
<br><A HREF=javascript:sf(3,129,'CH99221') NAME='CH99221'>　　　一、公  路</A>
<br><A HREF=javascript:sf(3,130,'CH99222') NAME='CH99222'>　　　二、桥梁  涵洞  渡口</A>
<br><A HREF=javascript:sf(3,131,'CH99223') NAME='CH99223'>　　　三、车站</A>
<br><A HREF=javascript:sf(3,132,'CH9923') NAME='CH9923'>　　第三节  公路运输</A>
<br><A HREF=javascript:sf(3,133,'CH99231') NAME='CH99231'>　　　一、客运</A>
<br><A HREF=javascript:sf(3,134,'CH99232') NAME='CH99232'>　　　二、货运</A>
<br><A HREF=javascript:sf(3,135,'CH9924') NAME='CH9924'>　　第四节  公路管理</A>
<br><A HREF=javascript:sf(3,136,'CH99241') NAME='CH99241'>　　　一、运政管理</A>
<br><A HREF=javascript:sf(3,137,'CH99242') NAME='CH99242'>　　　二、路政管理</A>
<br><A HREF=javascript:sf(3,138,'CH99243') NAME='CH99243'>　　　三、公路养护</A>
<br><A HREF=javascript:sf(3,139,'CH99244') NAME='CH99244'>　　　四、水运管理</A>
<br><A HREF=javascript:sf(3,140,'CH9925') NAME='CH9925'>　　第五节  交通安全管理</A>
<br><A HREF=javascript:sf(3,141,'CH99251') NAME='CH99251'>　　　一、交通安全设施设备</A>
<br><A HREF=javascript:sf(3,142,'CH99252') NAME='CH99252'>　　　二、机动车辆及驾驶员管理</A>
<br><A HREF=javascript:sf(3,143,'CH99253') NAME='CH99253'>　　　三、路面交通秩序管理</A>
<br><A HREF=javascript:sf(3,144,'CH99254') NAME='CH99254'>　　　四、交通事故处理</A>
<br><A HREF=javascript:sf(3,145,'CH9926') NAME='CH9926'>　　第六节  铁  路</A>
<br><A HREF=javascript:sf(3,146,'CH99261') NAME='CH99261'>　　　一、新石铁路东明段</A>
<br><A HREF=javascript:sf(3,147,'CH99262') NAME='CH99262'>　　　二、火车站</A>
<br><A HREF=javascript:sf(3,148,'CH99263') NAME='CH99263'>　　　三、铁路桥</A>
<br><A HREF=javascript:sf(3,149,'CH993') NAME='CH993'>　第三章  邮  电</A>
<br><A HREF=javascript:sf(3,150,'CH9931') NAME='CH9931'>　　第一节  邮政</A>
<br><A HREF=javascript:sf(3,151,'CH99311') NAME='CH99311'>　　　—、邮政机构</A>
<br><A HREF=javascript:sf(3,152,'CH99312') NAME='CH99312'>　　　二、邮政设施设备</A>
<br><A HREF=javascript:sf(3,153,'CH99313') NAME='CH99313'>　　　三、邮政网络</A>
<br><A HREF=javascript:sf(3,154,'CH99314') NAME='CH99314'>　　　四、邮政业务</A>
<br><A HREF=javascript:sf(3,155,'CH9932') NAME='CH9932'>　　第二节  电  信</A>
<br><A HREF=javascript:sf(3,156,'CH9933') NAME='CH9933'>　　第三节  移动通信</A>
<br><A HREF=javascript:sf(3,157,'CH994') NAME='CH994'>　第四章  电  力</A>
<br><A HREF=javascript:sf(3,158,'CH9941') NAME='CH9941'>　　第一节  供电机构</A>
<br><A HREF=javascript:sf(3,159,'CH9942') NAME='CH9942'>　　第二节  发  电</A>
<br><A HREF=javascript:sf(3,160,'CH9943') NAME='CH9943'>　　第三节  电力网站建设</A>
<br><A HREF=javascript:sf(3,161,'CH9944') NAME='CH9944'>　　第四节  供  电</A>
<br><A HREF=javascript:sf(3,162,'CH9945') NAME='CH9945'>　　第五节  用  电</A>
<br><A HREF=javascript:sf(3,163,'CH995') NAME='CH995'>　第五章  水  利</A>
<br><A HREF=javascript:sf(3,164,'CH9951') NAME='CH9951'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,165,'CH9952') NAME='CH9952'>　　第二节  农田灌溉</A>
<br><A HREF=javascript:sf(3,166,'CH9953') NAME='CH9953'>　　第三节  农田水利基本建设</A>
<br><A HREF=javascript:sf(3,167,'CH9954') NAME='CH9954'>　　第四节  水务管理</A>
<br><A HREF=javascript:sf(3,168,'CH9955') NAME='CH9955'>　　第五节  水土保持</A>
<br><A HREF=javascript:sf(3,169,'CH9956') NAME='CH9956'>　　第六节  农村自来水工程</A>
<br><A HREF=javascript:sf(3,170,'CH996') NAME='CH996'>　第六章  黄  河</A>
<br><A HREF=javascript:sf(3,171,'CH9961') NAME='CH9961'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,172,'CH9962') NAME='CH9962'>　　第二节  河道概况</A>
<br><A HREF=javascript:sf(3,173,'CH9963') NAME='CH9963'>　　第三节  堤防工程</A>
<br><A HREF=javascript:sf(3,174,'CH9964') NAME='CH9964'>　　第四节  险工及控导工程</A>
<br><A HREF=javascript:sf(3,175,'CH9965') NAME='CH9965'>　　第五节  引黄工程</A>
<br><A HREF=javascript:sf(3,176,'CH9966') NAME='CH9966'>　　第六节  宽河道治理</A>
<br><A HREF=javascript:sf(3,177,'CH9A') NAME='CH9A'>第四编  农  业</A>
<br><A HREF=javascript:sf(3,178,'CH9A1') NAME='CH9A1'>　第一章  农村经济体制改革</A>
<br><A HREF=javascript:sf(3,179,'CH9A11') NAME='CH9A11'>　　第一节  农业管理机构改革</A>
<br><A HREF=javascript:sf(3,180,'CH9A12') NAME='CH9A12'>　　第二节  农村土地使用制度改革</A>
<br><A HREF=javascript:sf(3,181,'CH9A13') NAME='CH9A13'>　　第三节  农村经营管理改革</A>
<br><A HREF=javascript:sf(3,182,'CH9A14') NAME='CH9A14'>　　第四节  农业产业化</A>
<br><A HREF=javascript:sf(3,183,'CH9A2') NAME='CH9A2'>　第二章  种植业</A>
<br><A HREF=javascript:sf(3,184,'CH9A21') NAME='CH9A21'>　　第一节  种植业结构</A>
<br><A HREF=javascript:sf(3,185,'CH9A22') NAME='CH9A22'>　　第二节  粮食油料作物</A>
<br><A HREF=javascript:sf(3,186,'CH9A23') NAME='CH9A23'>　　第三节  棉  花</A>
<br><A HREF=javascript:sf(3,187,'CH9A24') NAME='CH9A24'>　　第四节  蔬  菜</A>
<br><A HREF=javascript:sf(3,188,'CH9A25') NAME='CH9A25'>　　第五节  西  瓜</A>
<br><A HREF=javascript:sf(3,189,'CH9A26') NAME='CH9A26'>　　第六节  种  子</A>
<br><A HREF=javascript:sf(3,190,'CH9A27') NAME='CH9A27'>　　第七节  肥  料</A>
<br><A HREF=javascript:sf(3,191,'CH9A28') NAME='CH9A28'>第八节  种植制度</A>
<br><A HREF=javascript:sf(3,192,'CH9A29') NAME='CH9A29'>　　第九节  主要病虫害防治</A>
<br><A HREF=javascript:sf(3,193,'CH9A3') NAME='CH9A3'>　第三章  林果业</A>
<br><A HREF=javascript:sf(3,194,'CH9A31') NAME='CH9A31'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,195,'CH9A32') NAME='CH9A32'>　　第二节  林业资源</A>
<br><A HREF=javascript:sf(3,196,'CH9A33') NAME='CH9A33'>　　第三节  植树造林</A>
<br><A HREF=javascript:sf(3,197,'CH9A34') NAME='CH9A34'>　　第四节  林场苗圃</A>
<br><A HREF=javascript:sf(3,198,'CH9A35') NAME='CH9A35'>　　第五节  经济林</A>
<br><A HREF=javascript:sf(3,199,'CH9A36') NAME='CH9A36'>　　第六节  林业管理</A>
<br><A HREF=javascript:sf(3,200,'CH9A4') NAME='CH9A4'>　第四章  畜牧业</A>
<br><A HREF=javascript:sf(3,201,'CH9A41') NAME='CH9A41'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,202,'CH9A42') NAME='CH9A42'>　　第二节  畜禽饲养</A>
<br><A HREF=javascript:sf(3,203,'CH9A43') NAME='CH9A43'>　　第三节  饲草饲料</A>
<br><A HREF=javascript:sf(3,204,'CH9A44') NAME='CH9A44'>　　第四节  疫病防治</A>
<br><A HREF=javascript:sf(3,205,'CH9A5') NAME='CH9A5'>　第五章  水产业</A>
<br><A HREF=javascript:sf(3,206,'CH9A51') NAME='CH9A51'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,207,'CH9A52') NAME='CH9A52'>　　第二节  水产开发</A>
<br><A HREF=javascript:sf(3,208,'CH9A53') NAME='CH9A53'>　　第三节  水产种植</A>
<br><A HREF=javascript:sf(3,209,'CH9A54') NAME='CH9A54'>　　第四节  水产养殖</A>
<br><A HREF=javascript:sf(3,210,'CH9A55') NAME='CH9A55'>　　第五节  捕捞与渔政执法</A>
<br><A HREF=javascript:sf(3,211,'CH9A6') NAME='CH9A6'>　第六章  农业机械</A>
<br><A HREF=javascript:sf(3,212,'CH9A61') NAME='CH9A61'>　　第一节  机械设备</A>
<br><A HREF=javascript:sf(3,213,'CH9A62') NAME='CH9A62'>　　第二节  农机经营管理</A>
<br><A HREF=javascript:sf(3,214,'CH9A63') NAME='CH9A63'>　　第三节  农机科技</A>
<br><A HREF=javascript:sf(3,215,'CH9A64') NAME='CH9A64'>　　第四节  农机服务</A>
<br><A HREF=javascript:sf(3,216,'CH9A7') NAME='CH9A7'>　第七章  农业开发</A>
<br><A HREF=javascript:sf(3,217,'CH9A71') NAME='CH9A71'>　　第一节  农业综合开发</A>
<br><A HREF=javascript:sf(3,218,'CH9A72') NAME='CH9A72'>　　第二节  农业扶贫开发</A>
<br><A HREF=javascript:sf(3,219,'CH9B') NAME='CH9B'>第五编  工业  油区</A>
<br><A HREF=javascript:sf(3,220,'CH9B1') NAME='CH9B1'>　第一章  工业体制改革</A>
<br><A HREF=javascript:sf(3,221,'CH9B11') NAME='CH9B11'>　　第一节  管理体制改革</A>
<br><A HREF=javascript:sf(3,222,'CH9B12') NAME='CH9B12'>　　第二节  经营体制改革</A>
<br><A HREF=javascript:sf(3,223,'CH9B13') NAME='CH9B13'>　　第三节  产权制度改革</A>
<br><A HREF=javascript:sf(3,224,'CH9B2') NAME='CH9B2'>　第二章  化  工</A>
<br><A HREF=javascript:sf(3,225,'CH9B21') NAME='CH9B21'>　　第一节  经营体制</A>
<br><A HREF=javascript:sf(3,226,'CH9B22') NAME='CH9B22'>　　第二节  技术改造</A>
<br><A HREF=javascript:sf(3,227,'CH9B23') NAME='CH9B23'>　　第三节  主要化工产品</A>
<br><A HREF=javascript:sf(3,228,'CH9B24') NAME='CH9B24'>　　第四节  重点企业</A>
<br><A HREF=javascript:sf(3,229,'CH9B3') NAME='CH9B3'>　第三章  轻工  纺织</A>
<br><A HREF=javascript:sf(3,230,'CH9B31') NAME='CH9B31'>　　第一节  经营体制</A>
<br><A HREF=javascript:sf(3,231,'CH9B32') NAME='CH9B32'>　　第二节  技术改造</A>
<br><A HREF=javascript:sf(3,232,'CH9B33') NAME='CH9B33'>　　第三节  主要轻工纺织产品</A>
<br><A HREF=javascript:sf(3,233,'CH9B34') NAME='CH9B34'>　　第四节  重点企业</A>
<br><A HREF=javascript:sf(3,234,'CH9B4') NAME='CH9B4'>　第四章  农副产品加工</A>
<br><A HREF=javascript:sf(3,235,'CH9B41') NAME='CH9B41'>　　第一节  粮棉油及食品加工</A>
<br><A HREF=javascript:sf(3,236,'CH9B42') NAME='CH9B42'>　　第二节  造纸及纸制品业</A>
<br><A HREF=javascript:sf(3,237,'CH9B43') NAME='CH9B43'>　　第三节  木材加工</A>
<br><A HREF=javascript:sf(3,238,'CH9B5') NAME='CH9B5'>　第五章  机电  材料</A>
<br><A HREF=javascript:sf(3,239,'CH9B51') NAME='CH9B51'>　　第一节  机械  电器</A>
<br><A HREF=javascript:sf(3,240,'CH9B53') NAME='CH9B53'>　　第二节  基础材料</A>
<br><A HREF=javascript:sf(3,241,'CH9B6') NAME='CH9B6'>　第六章  乡镇民营企业</A>
<br><A HREF=javascript:sf(3,242,'CH9B61') NAME='CH9B61'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,243,'CH9B62') NAME='CH9B62'>　　第二节  乡镇企业</A>
<br><A HREF=javascript:sf(3,244,'CH9B63') NAME='CH9B63'>　　第三节  民营企业</A>
<br><A HREF=javascript:sf(3,245,'CH9B64') NAME='CH9B64'>　　第四节  经济园区</A>
<br><A HREF=javascript:sf(3,246,'CH9B65') NAME='CH9B65'>　　第五节  民营企业选介</A>
<br><A HREF=javascript:sf(3,247,'CH9B7') NAME='CH9B7'>　第七章  油  区</A>
<br><A HREF=javascript:sf(3,248,'CH9B71') NAME='CH9B71'>　　第一节  机  构</A>
<br><A HREF=javascript:sf(3,249,'CH9B72') NAME='CH9B72'>　　第二节  勘探开发</A>
<br><A HREF=javascript:sf(3,250,'CH9B73') NAME='CH9B73'>　　第三节  设施建设</A>
<br><A HREF=javascript:sf(3,251,'CH9B74') NAME='CH9B74'>　　第四节  支油工作</A>
<br><A HREF=javascript:sf(3,252,'CH9C') NAME='CH9C'>第六编  商业贸易</A>
<br><A HREF=javascript:sf(3,253,'CH9C1') NAME='CH9C1'>　第一章  商业</A>
<br><A HREF=javascript:sf(3,254,'CH9C11') NAME='CH9C11'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,255,'CH9C12') NAME='CH9C12'>　　第二节  商业体制改革</A>
<br><A HREF=javascript:sf(3,256,'CH9C13') NAME='CH9C13'>　　第三节  商品经营</A>
<br><A HREF=javascript:sf(3,257,'CH9C14') NAME='CH9C14'>　　第四节  饮食服务</A>
<br><A HREF=javascript:sf(3,258,'CH9C15') NAME='CH9C15'>　　第五节  经营管理</A>
<br><A HREF=javascript:sf(3,259,'CH9C16') NAME='CH9C16'>　　第六节  个体私营商业</A>
<br><A HREF=javascript:sf(3,260,'CH9C2') NAME='CH9C2'>　第二章  市  场</A>
<br><A HREF=javascript:sf(3,261,'CH9C21') NAME='CH9C21'>　　第一节  专业市场</A>
<br><A HREF=javascript:sf(3,262,'CH9C22') NAME='CH9C22'>　　第二节  商场</A>
<br><A HREF=javascript:sf(3,263,'CH9C23') NAME='CH9C23'>　　第三节  集贸市场</A>
<br><A HREF=javascript:sf(3,264,'CH9C24') NAME='CH9C24'>　　第四节  夜  市</A>
<br><A HREF=javascript:sf(3,265,'CH9C3') NAME='CH9C3'>　第三章  物资流通</A>
<br><A HREF=javascript:sf(3,266,'CH9C31') NAME='CH9C31'>　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,267,'CH9C32') NAME='CH9C32'>　第二节  物资体制改革</A>
<br><A HREF=javascript:sf(3,268,'CH9C33') NAME='CH9C33'>　　第三节  物资经营</A>
<br><A HREF=javascript:sf(3,269,'CH9C34') NAME='CH9C34'>　　第四节  物资管理</A>
<br><A HREF=javascript:sf(3,270,'CH9C4') NAME='CH9C4'>　第四章  供  销</A>
<br><A HREF=javascript:sf(3,271,'CH9C41') NAME='CH9C41'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,272,'CH9C42') NAME='CH9C42'>　　第二节  供销体制改革</A>
<br><A HREF=javascript:sf(3,273,'CH9C43') NAME='CH9C43'>　　第三节  农业生产资料经营</A>
<br><A HREF=javascript:sf(3,274,'CH9C44') NAME='CH9C44'>　　第四节  生活资料经营</A>
<br><A HREF=javascript:sf(3,275,'CH9C45') NAME='CH9C45'>　　第五节  物品收购</A>
<br><A HREF=javascript:sf(3,276,'CH9C5') NAME='CH9C5'>　第五章  粮油贸易</A>
<br><A HREF=javascript:sf(3,277,'CH9C51') NAME='CH9C51'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,278,'CH9C52') NAME='CH9C52'>　　第二节  粮油经营体制改革</A>
<br><A HREF=javascript:sf(3,279,'CH9C53') NAME='CH9C53'>　　第三节  粮油购销</A>
<br><A HREF=javascript:sf(3,280,'CH9C54') NAME='CH9C54'>　　第四节  粮油仓储与调拨</A>
<br><A HREF=javascript:sf(3,281,'CH9C6') NAME='CH9C6'>　第六章  棉花经营</A>
<br><A HREF=javascript:sf(3,282,'CH9C61') NAME='CH9C61'>　　第一节  体  制</A>
<br><A HREF=javascript:sf(3,283,'CH9C62') NAME='CH9C62'>　　第二节  棉花购销</A>
<br><A HREF=javascript:sf(3,284,'CH9C7') NAME='CH9C7'>　第七章  医药经营</A>
<br><A HREF=javascript:sf(3,285,'CH9C71') NAME='CH9C71'>　　第一节  体  制</A>
<br><A HREF=javascript:sf(3,286,'CH9C72') NAME='CH9C72'>　　第二节  医药购销</A>
<br><A HREF=javascript:sf(3,287,'CH9C73') NAME='CH9C73'>　　第三节  经营网点</A>
<br><A HREF=javascript:sf(3,288,'CH9C8') NAME='CH9C8'>　第八章  石油经营</A>
<br><A HREF=javascript:sf(3,289,'CH9C81') NAME='CH9C81'>　　第一节  体  制</A>
<br><A HREF=javascript:sf(3,290,'CH9C82') NAME='CH9C82'>　　第二节  石油购销</A>
<br><A HREF=javascript:sf(3,291,'CH9C83') NAME='CH9C83'>　　第三节  经营网点与管理</A>
<br><A HREF=javascript:sf(3,292,'CH9C9') NAME='CH9C9'>　第九章  烟草经营</A>
<br><A HREF=javascript:sf(3,293,'CH9C91') NAME='CH9C91'>　　第一节  体  制</A>
<br><A HREF=javascript:sf(3,294,'CH9C92') NAME='CH9C92'>　　第二节  烟草购销</A>
<br><A HREF=javascript:sf(3,295,'CH9C93') NAME='CH9C93'>　　第三节  烟草经营网点与管理</A>
<br><A HREF=javascript:sf(3,296,'CH9CA') NAME='CH9CA'>　第十章  盐业经营</A>
<br><A HREF=javascript:sf(3,297,'CH9CA1') NAME='CH9CA1'>　　第一节  体  制</A>
<br><A HREF=javascript:sf(3,298,'CH9CA2') NAME='CH9CA2'>　　第二节  盐业经营与管理</A>
<br><A HREF=javascript:sf(3,299,'CH9CB') NAME='CH9CB'>　第十一章  外  贸</A>
<br><A HREF=javascript:sf(3,300,'CH9CB1') NAME='CH9CB1'>　　第一节  体  制</A>
<br><A HREF=javascript:sf(3,301,'CH9CB2') NAME='CH9CB2'>　　第二节  出口贸易</A>
<br><A HREF=javascript:sf(3,302,'CH9CC') NAME='CH9CC'>　第十二章  招商引资</A>
<br><A HREF=javascript:sf(3,303,'CH9CC1') NAME='CH9CC1'>　　第一节  政策环境</A>
<br><A HREF=javascript:sf(3,304,'CH9CC2') NAME='CH9CC2'>　　第二节  重要活动及成果</A>
<br><A HREF=javascript:sf(3,305,'CH9CD') NAME='CH9CD'>　第十三章  地方名特产品</A>
<br><A HREF=javascript:sf(3,306,'CH9CD1') NAME='CH9CD1'>　　第一节  地方名牌</A>
<br><A HREF=javascript:sf(3,307,'CH9CD2') NAME='CH9CD2'>　　第二节  地方名产</A>
<br><A HREF=javascript:sf(3,308,'CH9CD3') NAME='CH9CD3'>　　第三节  地方名吃</A>
<br><A HREF=javascript:sf(3,309,'CH9D') NAME='CH9D'>第七编  财税  金融</A>
<br><A HREF=javascript:sf(3,310,'CH9D1') NAME='CH9D1'>　第一章  财  政</A>
<br><A HREF=javascript:sf(3,311,'CH9D11') NAME='CH9D11'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,312,'CH9D12') NAME='CH9D12'>　　第二节  财政体制</A>
<br><A HREF=javascript:sf(3,313,'CH9D13') NAME='CH9D13'>　　第三节  财政收入</A>
<br><A HREF=javascript:sf(3,314,'CH9D14') NAME='CH9D14'>　　第四节  财政支出</A>
<br><A HREF=javascript:sf(3,315,'CH9D15') NAME='CH9D15'>　　第五节  财政管理</A>
<br><A HREF=javascript:sf(3,316,'CH9D16') NAME='CH9D16'>　　第六节  国有资产管理</A>
<br><A HREF=javascript:sf(3,317,'CH9D2') NAME='CH9D2'>　第二章  税  务</A>
<br><A HREF=javascript:sf(3,318,'CH9D21') NAME='CH9D21'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,319,'CH9D22') NAME='CH9D22'>　　第二节  税制税种</A>
<br><A HREF=javascript:sf(3,320,'CH9D23') NAME='CH9D23'>　　第三节  税收管理</A>
<br><A HREF=javascript:sf(3,321,'CH9D24') NAME='CH9D24'>　　第四节  税务稽查</A>
<br><A HREF=javascript:sf(3,322,'CH9D3') NAME='CH9D3'>　第三章  金融</A>
<br><A HREF=javascript:sf(3,323,'CH9D31') NAME='CH9D31'>　　第一节  银行机构</A>
<br><A HREF=javascript:sf(3,324,'CH9D32') NAME='CH9D32'>　　第二节  金融管理体制改革</A>
<br><A HREF=javascript:sf(3,325,'CH9D33') NAME='CH9D33'>　　第三节  货  币</A>
<br><A HREF=javascript:sf(3,326,'CH9D34') NAME='CH9D34'>　　第四节  存  款</A>
<br><A HREF=javascript:sf(3,327,'CH9D35') NAME='CH9D35'>　　第五节  贷  款</A>
<br><A HREF=javascript:sf(3,328,'CH9D36') NAME='CH9D36'>　　第六节  结  算</A>
<br><A HREF=javascript:sf(3,329,'CH9D37') NAME='CH9D37'>　　第七节  债  券</A>
<br><A HREF=javascript:sf(3,330,'CH9D38') NAME='CH9D38'>　　第八节  监督管理</A>
<br><A HREF=javascript:sf(3,331,'CH9D4') NAME='CH9D4'>　第四章  保  险</A>
<br><A HREF=javascript:sf(3,332,'CH9D41') NAME='CH9D41'>　　第一节  财产保险</A>
<br><A HREF=javascript:sf(3,333,'CH9D42') NAME='CH9D42'>　　第二节  人寿保险</A>
<br><A HREF=javascript:sf(3,334,'CH9E') NAME='CH9E'>第八编  经济管理</A>
<br><A HREF=javascript:sf(3,335,'CH9E1') NAME='CH9E1'>　第一章  计  划</A>
<br><A HREF=javascript:sf(3,336,'CH9E11') NAME='CH9E11'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,337,'CH9E12') NAME='CH9E12'>　　第二节  管理体制</A>
<br><A HREF=javascript:sf(3,338,'CH9E13') NAME='CH9E13'>　　第三节  计划编制</A>
<br><A HREF=javascript:sf(3,339,'CH9E14') NAME='CH9E14'>　　第四节  计划实施</A>
<br><A HREF=javascript:sf(3,340,'CH9E15') NAME='CH9E15'>　　第五节  计划固定资产投资项目</A>
<br><A HREF=javascript:sf(3,341,'CH9E2') NAME='CH9E2'>　第二章  统  计</A>
<br><A HREF=javascript:sf(3,342,'CH9E21') NAME='CH9E21'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,343,'CH9E22') NAME='CH9E22'>　　第二节  统计调查</A>
<br><A HREF=javascript:sf(3,344,'CH9E23') NAME='CH9E23'>　　第三节  统计执法及服务</A>
<br><A HREF=javascript:sf(3,345,'CH9E24') NAME='CH9E24'>　　第四节  统计信息自动化</A>
<br><A HREF=javascript:sf(3,346,'CH9E3') NAME='CH9E3'>　第三章  审  计</A>
<br><A HREF=javascript:sf(3,347,'CH9E31') NAME='CH9E31'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,348,'CH9E32') NAME='CH9E32'>　　第二节  国家审计</A>
<br><A HREF=javascript:sf(3,349,'CH9E33') NAME='CH9E33'>　　第三节  内部审计</A>
<br><A HREF=javascript:sf(3,350,'CH9E34') NAME='CH9E34'>　　第四节  社会审计</A>
<br><A HREF=javascript:sf(3,351,'CH9E35') NAME='CH9E35'>　　第五节  经济责任审计</A>
<br><A HREF=javascript:sf(3,352,'CH9E4') NAME='CH9E4'>　第四章  物  价</A>
<br><A HREF=javascript:sf(3,353,'CH9E41') NAME='CH9E41'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,354,'CH9E42') NAME='CH9E42'>　　第二节  价格管理</A>
<br><A HREF=javascript:sf(3,355,'CH9E43') NAME='CH9E43'>　　第三节  收费管理</A>
<br><A HREF=javascript:sf(3,356,'CH9E44') NAME='CH9E44'>　　第四节  物价监督检查</A>
<br><A HREF=javascript:sf(3,357,'CH9E45') NAME='CH9E45'>　　第五节  价格信息</A>
<br><A HREF=javascript:sf(3,358,'CH9E46') NAME='CH9E46'>　　第六节  价格认证</A>
<br><A HREF=javascript:sf(3,359,'CH9E5') NAME='CH9E5'>　第五章  工商行政管理</A>
<br><A HREF=javascript:sf(3,360,'CH9E51') NAME='CH9E51'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,361,'CH9E52') NAME='CH9E52'>　　第二节  市场监督管理</A>
<br><A HREF=javascript:sf(3,362,'CH9E53') NAME='CH9E53'>　　第三节  工商企业登记管理</A>
<br><A HREF=javascript:sf(3,363,'CH9E54') NAME='CH9E54'>　　第四节  经济合同管理</A>
<br><A HREF=javascript:sf(3,364,'CH9E55') NAME='CH9E55'>　　第五节  商标广告管理</A>
<br><A HREF=javascript:sf(3,365,'CH9E56') NAME='CH9E56'>　　第六节  经济监督检查</A>
<br><A HREF=javascript:sf(3,366,'CH9E57') NAME='CH9E57'>　　第七节  消费者权益保护</A>
<br><A HREF=javascript:sf(3,367,'CH9E6') NAME='CH9E6'>　第六章  质量技术监督</A>
<br><A HREF=javascript:sf(3,368,'CH9E61') NAME='CH9E61'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,369,'CH9E62') NAME='CH9E62'>　　第二节  计量管理</A>
<br><A HREF=javascript:sf(3,370,'CH9E63') NAME='CH9E63'>　　第三节  质量监督管理</A>
<br><A HREF=javascript:sf(3,371,'CH9E64') NAME='CH9E64'>　　第四节  标准化管理</A>
<br><A HREF=javascript:sf(3,372,'CH9E65') NAME='CH9E65'>　　第五节  特种设备安全监察</A>
<br><A HREF=javascript:sf(3,373,'CH9E7') NAME='CH9E7'>　　第七章  食品药品监督</A>
<br><A HREF=javascript:sf(3,374,'CH9E71') NAME='CH9E71'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,375,'CH9E72') NAME='CH9E72'>　　第二节  食品药品综合管理</A>
<br><A HREF=javascript:sf(3,376,'CH9E8') NAME='CH9E8'>　第八章  安全生产监督</A>
<br><A HREF=javascript:sf(3,377,'CH9E81') NAME='CH9E81'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,378,'CH9E82') NAME='CH9E82'>　　第二节  法律法规宣传</A>
<br><A HREF=javascript:sf(3,379,'CH9E83') NAME='CH9E83'>　　第三节  安全生产综合管理</A>
<br><A HREF=javascript:sf(3,380,'CH9E9') NAME='CH9E9'>　第九章  国土资源</A>
<br><A HREF=javascript:sf(3,381,'CH9E91') NAME='CH9E91'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,382,'CH9E92') NAME='CH9E92'>　　第二节  土地使用制度改革</A>
<br><A HREF=javascript:sf(3,383,'CH9E93') NAME='CH9E93'>　　第三节  土地调查规划评估</A>
<br><A HREF=javascript:sf(3,384,'CH9E94') NAME='CH9E94'>　　第四节  土地保护</A>
<br><A HREF=javascript:sf(3,385,'CH9E95') NAME='CH9E95'>　　第五节  土地执法</A>
<br><A HREF=javascript:sf(3,386,'CH9F') NAME='CH9F'>第九编  综合政务</A>
<br><A HREF=javascript:sf(3,387,'CH9F1') NAME='CH9F1'>　第一章  人  事</A>
<br><A HREF=javascript:sf(3,388,'CH9F11') NAME='CH9F11'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,389,'CH9F12') NAME='CH9F12'>　　第二节  编制管理</A>
<br><A HREF=javascript:sf(3,390,'CH9F13') NAME='CH9F13'>　　第三节  干部管理</A>
<br><A HREF=javascript:sf(3,391,'CH9F14') NAME='CH9F14'>　　第四节  职称管理</A>
<br><A HREF=javascript:sf(3,392,'CH9F15') NAME='CH9F15'>　　第五节  人才交流</A>
<br><A HREF=javascript:sf(3,393,'CH9F16') NAME='CH9F16'>　　第六节  工资福利</A>
<br><A HREF=javascript:sf(3,394,'CH9F17') NAME='CH9F17'>　　第七节  考核奖惩</A>
<br><A HREF=javascript:sf(3,395,'CH9F2') NAME='CH9F2'>　第二章  劳  动</A>
<br><A HREF=javascript:sf(3,396,'CH9F21') NAME='CH9F21'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,397,'CH9F22') NAME='CH9F22'>　　第二节  管理体制改革</A>
<br><A HREF=javascript:sf(3,398,'CH9F23') NAME='CH9F23'>　　第三节  劳动管理</A>
<br><A HREF=javascript:sf(3,399,'CH9F24') NAME='CH9F24'>　　第四节  劳动工资</A>
<br><A HREF=javascript:sf(3,400,'CH9F25') NAME='CH9F25'>　　第五节  就业与再就业</A>
<br><A HREF=javascript:sf(3,401,'CH9F26') NAME='CH9F26'>　　第六节  劳动监察</A>
<br><A HREF=javascript:sf(3,402,'CH9F3') NAME='CH9F3'>　第三章  民  政</A>
<br><A HREF=javascript:sf(3,403,'CH9F31') NAME='CH9F31'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,404,'CH9F32') NAME='CH9F32'>　　第二节  基层政权建设</A>
<br><A HREF=javascript:sf(3,405,'CH9F33') NAME='CH9F33'>　　第三节  退伍兵安置</A>
<br><A HREF=javascript:sf(3,406,'CH9F34') NAME='CH9F34'>　　第四节  优抚拥军</A>
<br><A HREF=javascript:sf(3,407,'CH9F35') NAME='CH9F35'>　　第五节  民政管理</A>
<br><A HREF=javascript:sf(3,408,'CH9G') NAME='CH9G'>第十编  政党  群团</A>
<br><A HREF=javascript:sf(3,409,'CH9G1') NAME='CH9G1'>　第一章  中国共产党东明县委员会</A>
<br><A HREF=javascript:sf(3,410,'CH9G11') NAME='CH9G11'>　　第一节  组织机构</A>
<br><A HREF=javascript:sf(3,411,'CH9G12') NAME='CH9G12'>　　第二节  党员代表大会</A>
<br><A HREF=javascript:sf(3,412,'CH9G13') NAME='CH9G13'>　　第三节  县委重大决策</A>
<br><A HREF=javascript:sf(3,413,'CH9G14') NAME='CH9G14'>　　第四节  组织建设</A>
<br><A HREF=javascript:sf(3,414,'CH9G15') NAME='CH9G15'>　　第五节  宣  传</A>
<br><A HREF=javascript:sf(3,415,'CH9G16') NAME='CH9G16'>　　第六节  统  战</A>
<br><A HREF=javascript:sf(3,416,'CH9G17') NAME='CH9G17'>　　第七节  党校教育</A>
<br><A HREF=javascript:sf(3,417,'CH9G2') NAME='CH9G2'>　第二章  纪检监察</A>
<br><A HREF=javascript:sf(3,418,'CH9G21') NAME='CH9G21'>　　第一节  机  构</A>
<br><A HREF=javascript:sf(3,419,'CH9G22') NAME='CH9G22'>　　第二节  信访举报</A>
<br><A HREF=javascript:sf(3,420,'CH9G23') NAME='CH9G23'>　　第三节  案件查处</A>
<br><A HREF=javascript:sf(3,421,'CH9G24') NAME='CH9G24'>　　第四节  党风廉政建设</A>
<br><A HREF=javascript:sf(3,422,'CH9G25') NAME='CH9G25'>　　第五节  纠风正纪</A>
<br><A HREF=javascript:sf(3,423,'CH9G26') NAME='CH9G26'>　　第六节  政务公开</A>
<br><A HREF=javascript:sf(3,424,'CH9G27') NAME='CH9G27'>　　第七节  执法监察</A>
<br><A HREF=javascript:sf(3,425,'CH9G3') NAME='CH9G3'>　第三章  群众团体</A>
<br><A HREF=javascript:sf(3,426,'CH9G31') NAME='CH9G31'>　　第一节  工人联合会</A>
<br><A HREF=javascript:sf(3,427,'CH9G32') NAME='CH9G32'>　　第二节  共产主义青年团</A>
<br><A HREF=javascript:sf(3,428,'CH9G33') NAME='CH9G33'>　　第三节  妇女联合会</A>
<br><A HREF=javascript:sf(3,429,'CH9G34') NAME='CH9G34'>　　第四节  科学技术协会</A>
<br><A HREF=javascript:sf(3,430,'CH9G35') NAME='CH9G35'>　　第五节  残疾人联合会</A>
<br><A HREF=javascript:sf(3,431,'CH9G36') NAME='CH9G36'>　　第六节  工商业者联合会</A>
<br><A HREF=javascript:sf(3,432,'CH9H') NAME='CH9H'>第十一编  政权  政协</A>
<br><A HREF=javascript:sf(3,433,'CH9H1') NAME='CH9H1'>　第一章  东明县人民代表大会</A>
<br><A HREF=javascript:sf(3,434,'CH9H11') NAME='CH9H11'>　　第一节  人民代表大会常务委员会</A>
<br><A HREF=javascript:sf(3,435,'CH9H12') NAME='CH9H12'>　　第二节  历届人民代表大会</A>
<br><A HREF=javascript:sf(3,436,'CH9H13') NAME='CH9H13'>　　第三节  工作监督</A>
<br><A HREF=javascript:sf(3,437,'CH9H14') NAME='CH9H14'>　　第四节  法律监督</A>
<br><A HREF=javascript:sf(3,438,'CH9H15') NAME='CH9H15'>　　第五节  代表工作</A>
<br><A HREF=javascript:sf(3,439,'CH9H2') NAME='CH9H2'>　第二章  东明县人民政府</A>
<br><A HREF=javascript:sf(3,440,'CH9H21') NAME='CH9H21'>　　第一节  领导成员</A>
<br><A HREF=javascript:sf(3,441,'CH9H22') NAME='CH9H22'>　　第二节  组织机构</A>
<br><A HREF=javascript:sf(3,442,'CH9H23') NAME='CH9H23'>　　第三节  会议制度</A>
<br><A HREF=javascript:sf(3,443,'CH9H24') NAME='CH9H24'>　　第四节  政府决策</A>
<br><A HREF=javascript:sf(3,444,'CH9H25') NAME='CH9H25'>　　第五节  政府办公室工作</A>
<br><A HREF=javascript:sf(3,445,'CH9H26') NAME='CH9H26'>　　第六节  政府法制</A>
<br><A HREF=javascript:sf(3,446,'CH9H27') NAME='CH9H27'>　　第七节  外事  侨务</A>
<br><A HREF=javascript:sf(3,447,'CH9H28') NAME='CH9H28'>　　第八节  行政审批</A>
<br><A HREF=javascript:sf(3,448,'CH9H29') NAME='CH9H29'>　　第九节  信  访</A>
<br><A HREF=javascript:sf(3,449,'CH9H2A') NAME='CH9H2A'>　　第十节  老  龄</A>
<br><A HREF=javascript:sf(3,450,'CH9H3') NAME='CH9H3'>　第三章  政协东明县委员会</A>
<br><A HREF=javascript:sf(3,451,'CH9H31') NAME='CH9H31'>　　第一节  政协东明县委员会构成</A>
<br><A HREF=javascript:sf(3,452,'CH9H32') NAME='CH9H32'>　　第二节  历届政协会议</A>
<br><A HREF=javascript:sf(3,453,'CH9H33') NAME='CH9H33'>　　第三节  政治协商</A>
<br><A HREF=javascript:sf(3,454,'CH9H34') NAME='CH9H34'>　　第四节  民主监督</A>
<br><A HREF=javascript:sf(3,455,'CH9I') NAME='CH9I'>第十二编  军事  政法</A>
<br><A HREF=javascript:sf(3,456,'CH9I1') NAME='CH9I1'>　第一章  军  事</A>
<br><A HREF=javascript:sf(3,457,'CH9I11') NAME='CH9I11'>　　第一节  军事建制</A>
<br><A HREF=javascript:sf(3,458,'CH9I12') NAME='CH9I12'>　　第二节  军事训练</A>
<br><A HREF=javascript:sf(3,459,'CH9I13') NAME='CH9I13'>　　第三节  政治工作</A>
<br><A HREF=javascript:sf(3,460,'CH9I14') NAME='CH9I14'>　　第四节  后勤保障</A>
<br><A HREF=javascript:sf(3,461,'CH9I15') NAME='CH9I15'>　　第五节  拥政爱民</A>
<br><A HREF=javascript:sf(3,462,'CH9I16') NAME='CH9I16'>　　第六节  国防教育</A>
<br><A HREF=javascript:sf(3,463,'CH9I17') NAME='CH9I17'>　　第七节  人民防空</A>
<br><A HREF=javascript:sf(3,464,'CH9I18') NAME='CH9I18'>　　第八节  兵  役</A>
<br><A HREF=javascript:sf(3,465,'CH9I19') NAME='CH9I19'>　　第九节  驻  军</A>
<br><A HREF=javascript:sf(3,466,'CH9I2') NAME='CH9I2'>　第二章  公  安</A>
<br><A HREF=javascript:sf(3,467,'CH9I21') NAME='CH9I21'>　　第一节  机  构</A>
<br><A HREF=javascript:sf(3,468,'CH9I22') NAME='CH9I22'>　　第二节  打击犯罪</A>
<br><A HREF=javascript:sf(3,469,'CH9I23') NAME='CH9I23'>　　第三节  治安管理</A>
<br><A HREF=javascript:sf(3,470,'CH9I24') NAME='CH9I24'>　　第四节  监所管理</A>
<br><A HREF=javascript:sf(3,471,'CH9I25') NAME='CH9I25'>　　第五节  消  防</A>
<br><A HREF=javascript:sf(3,472,'CH9I26') NAME='CH9I26'>　　第六节 “110”报警服务</A>
<br><A HREF=javascript:sf(3,473,'CH9I3') NAME='CH9I3'>　第三章  检  察</A>
<br><A HREF=javascript:sf(3,474,'CH9I31') NAME='CH9I31'>　　第一节  机  构</A>
<br><A HREF=javascript:sf(3,475,'CH9I32') NAME='CH9I32'>　　第二节  反贪污贿赂</A>
<br><A HREF=javascript:sf(3,476,'CH9I33') NAME='CH9I33'>　　第三节  查办渎职犯罪</A>
<br><A HREF=javascript:sf(3,477,'CH9I34') NAME='CH9I34'>　　第四节  刑事检察</A>
<br><A HREF=javascript:sf(3,478,'CH9I35') NAME='CH9I35'>　　第五节  监所检察</A>
<br><A HREF=javascript:sf(3,479,'CH9I36') NAME='CH9I36'>　　第六节  控告申诉</A>
<br><A HREF=javascript:sf(3,480,'CH9I37') NAME='CH9I37'>　　第七节  民事行政检察</A>
<br><A HREF=javascript:sf(3,481,'CH9I4') NAME='CH9I4'>　第四章  审  判</A>
<br><A HREF=javascript:sf(3,482,'CH9I41') NAME='CH9I41'>　　第一节  机  构</A>
<br><A HREF=javascript:sf(3,483,'CH9I42') NAME='CH9I42'>　　第二节  立 案</A>
<br><A HREF=javascript:sf(3,484,'CH9I43') NAME='CH9I43'>　　第三节  刑事审判</A>
<br><A HREF=javascript:sf(3,485,'CH9I44') NAME='CH9I44'>　　第四节  民事审判</A>
<br><A HREF=javascript:sf(3,486,'CH9I45') NAME='CH9I45'>　　第五节  经济审判</A>
<br><A HREF=javascript:sf(3,487,'CH9I46') NAME='CH9I46'>　　第六节  行政审判</A>
<br><A HREF=javascript:sf(3,488,'CH9I47') NAME='CH9I47'>　　第七节 案件执行</A>
<br><A HREF=javascript:sf(3,489,'CH9I48') NAME='CH9I48'>　　第八节  审判监督</A>
<br><A HREF=javascript:sf(3,490,'CH9I5') NAME='CH9I5'>　第五章  司  法</A>
<br><A HREF=javascript:sf(3,491,'CH9I51') NAME='CH9I51'>　　第一节  机 构</A>
<br><A HREF=javascript:sf(3,492,'CH9I52') NAME='CH9I52'>　　第二节  普法教育</A>
<br><A HREF=javascript:sf(3,493,'CH9I53') NAME='CH9I53'>　　第三节  民事调解</A>
<br><A HREF=javascript:sf(3,494,'CH9I54') NAME='CH9I54'>　　第四节  法律援助</A>
<br><A HREF=javascript:sf(3,495,'CH9I55') NAME='CH9I55'>　　第五节  公 证</A>
<br><A HREF=javascript:sf(3,496,'CH9I56') NAME='CH9I56'>　　第六节  律 师</A>
<br><A HREF=javascript:sf(3,497,'CH9I57') NAME='CH9I57'>　　第七节  基层司法</A>
<br><A HREF=javascript:sf(3,498,'CH9I58') NAME='CH9I58'>　　第八节  "148"法律服务</A>
<br><A HREF=javascript:sf(3,499,'CH9J') NAME='CH9J'>第十三编  科教  文卫</A>
<br><A HREF=javascript:sf(3,500,'CH9J1') NAME='CH9J1'>　第一章  科学技术</A>
<br><A HREF=javascript:sf(3,501,'CH9J11') NAME='CH9J11'>　　第一节  机构与队伍</A>
<br><A HREF=javascript:sf(3,502,'CH9J12') NAME='CH9J12'>　　第二节  科技活动</A>
<br><A HREF=javascript:sf(3,503,'CH9J13') NAME='CH9J13'>　　第三节  科技成果</A>
<br><A HREF=javascript:sf(3,504,'CH9J14') NAME='CH9J14'>　　第四节  科技服务</A>
<br><A HREF=javascript:sf(3,505,'CH9J15') NAME='CH9J15'>　　第五节  科技管理</A>
<br><A HREF=javascript:sf(3,506,'CH9J16') NAME='CH9J16'>　　第六节  气象监测服务</A>
<br><A HREF=javascript:sf(3,507,'CH9J2') NAME='CH9J2'>　第二章  教  育</A>
<br><A HREF=javascript:sf(3,508,'CH9J21') NAME='CH9J21'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,509,'CH9J22') NAME='CH9J22'>　　第二节  教育体制改革</A>
<br><A HREF=javascript:sf(3,510,'CH9J23') NAME='CH9J23'>　　第三节  基础教育</A>
<br><A HREF=javascript:sf(3,511,'CH9J24') NAME='CH9J24'>　　第四节  成人教育</A>
<br><A HREF=javascript:sf(3,512,'CH9J25') NAME='CH9J25'>　　第五节  职业教育</A>
<br><A HREF=javascript:sf(3,513,'CH9J26') NAME='CH9J26'>　　第六节  社会力量办学</A>
<br><A HREF=javascript:sf(3,514,'CH9J27') NAME='CH9J27'>　　第七节  教师队伍</A>
<br><A HREF=javascript:sf(3,515,'CH9J28') NAME='CH9J28'>　　第八节  教育行政</A>
<br><A HREF=javascript:sf(3,516,'CH9J29') NAME='CH9J29'>　　第九节  学校基础设施</A>
<br><A HREF=javascript:sf(3,517,'CH9J2A') NAME='CH9J2A'>　　第十节  对外交流与合作</A>
<br><A HREF=javascript:sf(3,518,'CH9J2B') NAME='CH9J2B'>　　第十一节  县属重点中学</A>
<br><A HREF=javascript:sf(3,519,'CH9J3') NAME='CH9J3'>　第三章  文  化</A>
<br><A HREF=javascript:sf(3,520,'CH9J31') NAME='CH9J31'>　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,521,'CH9J32') NAME='CH9J32'>　　第二节  文学艺术</A>
<br><A HREF=javascript:sf(3,522,'CH9J33') NAME='CH9J33'>　　第三节  文化娱乐</A>
<br><A HREF=javascript:sf(3,523,'CH9J34') NAME='CH9J34'>　　第四节  文化设施</A>
<br><A HREF=javascript:sf(3,524,'CH9J35') NAME='CH9J35'>　　第五节  文物管理</A>
<br><A HREF=javascript:sf(3,525,'CH9J36') NAME='CH9J36'>　　第六节  文化市场管理</A>
<br><A HREF=javascript:sf(3,526,'CH9J4') NAME='CH9J4'>　　第四章  文物胜迹</A>
<br><A HREF=javascript:sf(3,527,'CH9J41') NAME='CH9J41'>　　第一节  文物收藏</A>
<br><A HREF=javascript:sf(3,528,'CH9J42') NAME='CH9J42'>　　第二节  文化遗址</A>
<br><A HREF=javascript:sf(3,529,'CH9J43') NAME='CH9J43'>　　第三节  文化遗迹</A>
<br><A HREF=javascript:sf(3,530,'CH9J44') NAME='CH9J44'>　　第四节  墓  葬</A>
<br><A HREF=javascript:sf(3,531,'CH9J45') NAME='CH9J45'>　　第五节  碑  刻</A>
<br><A HREF=javascript:sf(3,532,'CH9J46') NAME='CH9J46'>　　第六节  革命烈士纪念碑</A>
<br><A HREF=javascript:sf(3,533,'CH9J47') NAME='CH9J47'>　　第七节  公  园</A>
<br><A HREF=javascript:sf(3,534,'CH9J5') NAME='CH9J5'>　　第五章  史志  档案</A>
<br><A HREF=javascript:sf(3,535,'CH9J51') NAME='CH9J51'>　　第一节  党  史</A>
<br><A HREF=javascript:sf(3,536,'CH9J52') NAME='CH9J52'>　　第二节  县  志</A>
<br><A HREF=javascript:sf(3,537,'CH9J53') NAME='CH9J53'>　　第三节  档  案</A>
<br><A HREF=javascript:sf(3,538,'CH9J6') NAME='CH9J6'>　第六章  广播电视</A>
<br><A HREF=javascript:sf(3,539,'CH9J61') NAME='CH9J61'>　　第一节  机  构</A>
<br><A HREF=javascript:sf(3,540,'CH9J62') NAME='CH9J62'>　　第二节  新闻工作</A>
<br><A HREF=javascript:sf(3,541,'CH9J63') NAME='CH9J63'>　　第三节  广  播</A>
<br><A HREF=javascript:sf(3,542,'CH9J64') NAME='CH9J64'>　　第四节  电  视</A>
<br><A HREF=javascript:sf(3,543,'CH9J65') NAME='CH9J65'>　　第五节  有线电视网络传输</A>
<br><A HREF=javascript:sf(3,544,'CH9J7') NAME='CH9J7'>　　第七章  体  育</A>
<br><A HREF=javascript:sf(3,545,'CH9J71') NAME='CH9J71'>　　第一节  管理机构</A>
<br><A HREF=javascript:sf(3,546,'CH9J72') NAME='CH9J72'>　　第二节  体育设施</A>
<br><A HREF=javascript:sf(3,547,'CH9J73') NAME='CH9J73'>　　第三节  群众体育</A>
<br><A HREF=javascript:sf(3,548,'CH9J74') NAME='CH9J74'>　　第四节  竞技体育</A>
<br><A HREF=javascript:sf(3,549,'CH9J75') NAME='CH9J75'>　　第五节  武  术</A>
<br><A HREF=javascript:sf(3,550,'CH9J76') NAME='CH9J76'>　　第六节  体育学校</A>
<br><A HREF=javascript:sf(3,551,'CH9J77') NAME='CH9J77'>　　第七节  体育产业</A>
<br><A HREF=javascript:sf(3,552,'CH9J8') NAME='CH9J8'>　第八章  卫  生</A>
<br><A HREF=javascript:sf(3,553,'CH9J81') NAME='CH9J81'>　　第一节  机  构</A>
<br><A HREF=javascript:sf(3,554,'CH9J82') NAME='CH9J82'>　　第二节  管理体制改革</A>
<br><A HREF=javascript:sf(3,555,'CH9J83') NAME='CH9J83'>　　第三节  医  疗</A>
<br><A HREF=javascript:sf(3,556,'CH9J84') NAME='CH9J84'>　　第四节  医政管理</A>
<br><A HREF=javascript:sf(3,557,'CH9J85') NAME='CH9J85'>　　第五节  妇幼保健</A>
<br><A HREF=javascript:sf(3,558,'CH9J86') NAME='CH9J86'>　　第六节  疾病预防控制</A>
<br><A HREF=javascript:sf(3,559,'CH9J87') NAME='CH9J87'>　　第七节  公共卫生</A>
<br><A HREF=javascript:sf(3,560,'CH9J88') NAME='CH9J88'>　　第八节  卫生监督</A>
<br><A HREF=javascript:sf(3,561,'CH9K') NAME='CH9K'>第十四编  社会生活</A>
<br><A HREF=javascript:sf(3,562,'CH9K1') NAME='CH9K1'>　第一章  居民生活</A>
<br><A HREF=javascript:sf(3,563,'CH9K11') NAME='CH9K11'>　　第一节  城镇居民生活</A>
<br><A HREF=javascript:sf(3,564,'CH9K12') NAME='CH9K12'>　　第二节  农村居民生活</A>
<br><A HREF=javascript:sf(3,565,'CH9K2') NAME='CH9K2'>　　第二章  社会保障</A>
<br><A HREF=javascript:sf(3,566,'CH9K21') NAME='CH9K21'>　第一节  社会福利</A>
<br><A HREF=javascript:sf(3,567,'CH9K22') NAME='CH9K22'>　　第二节  社会救助</A>
<br><A HREF=javascript:sf(3,568,'CH9K23') NAME='CH9K23'>　　第三节  社会保险</A>
<br><A HREF=javascript:sf(3,569,'CH9K3') NAME='CH9K3'>　第三章  精神文明建设</A>
<br><A HREF=javascript:sf(3,570,'CH9K31') NAME='CH9K31'>　　第一节  思想道德教育</A>
<br><A HREF=javascript:sf(3,571,'CH9K32') NAME='CH9K32'>　　第二节  文明创建活动</A>
<br><A HREF=javascript:sf(3,572,'CH9K33') NAME='CH9K33'>　　第三节  文明风尚</A>
<br><A HREF=javascript:sf(3,573,'CH9K4') NAME='CH9K4'>　第四章  宗  教</A>
<br><A HREF=javascript:sf(3,574,'CH9K41') NAME='CH9K41'>　　第一节  伊斯兰教</A>
<br><A HREF=javascript:sf(3,575,'CH9K42') NAME='CH9K42'>　　第二节  基督教</A>
<br><A HREF=javascript:sf(3,576,'CH9K43') NAME='CH9K43'>　　第三节  天主教</A>
<br><A HREF=javascript:sf(3,577,'CH9K5') NAME='CH9K5'>　　第五章  民  俗</A>
<br><A HREF=javascript:sf(3,578,'CH9K51') NAME='CH9K51'>　　第一节  日常生活习俗</A>
<br><A HREF=javascript:sf(3,579,'CH9K52') NAME='CH9K52'>　　第二节  生产习俗</A>
<br><A HREF=javascript:sf(3,580,'CH9K53') NAME='CH9K53'>　　第三节  岁时节日</A>
<br><A HREF=javascript:sf(3,581,'CH9K54') NAME='CH9K54'>　　第四节  社交礼仪</A>
<br><A HREF=javascript:sf(3,582,'CH9K55') NAME='CH9K55'>　　第五节  婚丧喜庆</A>
<br><A HREF=javascript:sf(3,583,'CH9K56') NAME='CH9K56'>　　第六节  陋习禁忌</A>
<br><A HREF=javascript:sf(3,584,'CH9K6') NAME='CH9K6'>　　第六章  方  言</A>
<br><A HREF=javascript:sf(3,585,'CH9K61') NAME='CH9K61'>　　第一节  语音特点</A>
<br><A HREF=javascript:sf(3,586,'CH9K62') NAME='CH9K62'>　　第二节  方言词汇</A>
<br><A HREF=javascript:sf(3,587,'CH9K63') NAME='CH9K63'>　　第三节  歌  谣</A>
<br><A HREF=javascript:sf(3,588,'CH9K64') NAME='CH9K64'>　　第四节  谚  语</A>
<br><A HREF=javascript:sf(3,589,'CH9K65') NAME='CH9K65'>　　第五节  歇后语</A>
<br><A HREF=javascript:sf(3,590,'CH9L') NAME='CH9L'>第十五编  乡村简述</A>
<br><A HREF=javascript:sf(3,591,'CH9L1') NAME='CH9L1'>　第一章  乡镇开发区概述</A>
<br><A HREF=javascript:sf(3,592,'CH9L11') NAME='CH9L11'>　　第一节  开发区</A>
<br><A HREF=javascript:sf(3,593,'CH9L12') NAME='CH9L12'>　　第二节  城关镇</A>
<br><A HREF=javascript:sf(3,594,'CH9L13') NAME='CH9L13'>　　第三节  东明集镇</A>
<br><A HREF=javascript:sf(3,595,'CH9L14') NAME='CH9L14'>　　第四节  刘楼镇</A>
<br><A HREF=javascript:sf(3,596,'CH9L15') NAME='CH9L15'>　　第五节  陆圈镇</A>
<br><A HREF=javascript:sf(3,597,'CH9L16') NAME='CH9L16'>　　第六节  三春集镇</A>
<br><A HREF=javascript:sf(3,598,'CH9L17') NAME='CH9L17'>　　第七节  大屯镇</A>
<br><A HREF=javascript:sf(3,599,'CH9L18') NAME='CH9L18'>　　第八节  马头镇</A>
<br><A HREF=javascript:sf(3,600,'CH9L19') NAME='CH9L19'>　　第九节  小井乡</A>
<br><A HREF=javascript:sf(3,601,'CH9L1A') NAME='CH9L1A'>　　第十节  菜园集乡</A>
<br><A HREF=javascript:sf(3,602,'CH9L1B') NAME='CH9L1B'>　　第十一节  沙窝乡</A>
<br><A HREF=javascript:sf(3,603,'CH9L1C') NAME='CH9L1C'>　　第十二节  焦园乡</A>
<br><A HREF=javascript:sf(3,604,'CH9L1D') NAME='CH9L1D'>　　第十三节  武胜桥乡</A>
<br><A HREF=javascript:sf(3,605,'CH9L1E') NAME='CH9L1E'>　　第十四节  长兴集乡</A>
<br><A HREF=javascript:sf(3,606,'CH9L2') NAME='CH9L2'>　第二章  村庄选介</A>
<br><A HREF=javascript:sf(3,607,'CH9L21') NAME='CH9L21'>　　第一节  开发区辖村</A>
<br><A HREF=javascript:sf(3,608,'CH9L22') NAME='CH9L22'>　　第二节  城关镇辖村</A>
<br><A HREF=javascript:sf(3,609,'CH9L23') NAME='CH9L23'>　　第三节  东明集镇辖村</A>
<br><A HREF=javascript:sf(3,610,'CH9L24') NAME='CH9L24'>　　第四节  刘楼镇辖村</A>
<br><A HREF=javascript:sf(3,611,'CH9L25') NAME='CH9L25'>　　第五节  陆圈镇辖村</A>
<br><A HREF=javascript:sf(3,612,'CH9L26') NAME='CH9L26'>　　第六节  三春集镇辖村</A>
<br><A HREF=javascript:sf(3,613,'CH9L27') NAME='CH9L27'>　　第七节  大屯镇辖村</A>
<br><A HREF=javascript:sf(3,614,'CH9L28') NAME='CH9L28'>　　第八节  马头镇辖村</A>
<br><A HREF=javascript:sf(3,615,'CH9L29') NAME='CH9L29'>　　第九节  小井乡辖村</A>
<br><A HREF=javascript:sf(3,616,'CH9L2A') NAME='CH9L2A'>　　第十节  菜园集乡辖村</A>
<br><A HREF=javascript:sf(3,617,'CH9L2B') NAME='CH9L2B'>　　第十一节  沙窝乡辖村</A>
<br><A HREF=javascript:sf(3,618,'CH9L2C') NAME='CH9L2C'>　　第十二节  焦园乡辖村</A>
<br><A HREF=javascript:sf(3,619,'CH9L2D') NAME='CH9L2D'>　　第十三节  武胜桥乡辖村</A>
<br><A HREF=javascript:sf(3,620,'CH9L2E') NAME='CH9L2E'>　　第十四节  长兴集乡辖村</A>
<br><A HREF=javascript:sf(3,621,'CH9M') NAME='CH9M'>人物</A>
<br><A HREF=javascript:sf(3,622,'CH9M1') NAME='CH9M1'>　一、人物传（略)</A>
<br><A HREF=javascript:sf(3,623,'CH9M11') NAME='CH9M11'>　　(一）历史人物选萃</A>
<br><A HREF=javascript:sf(3,624,'CH9M12') NAME='CH9M12'>　　(二）新立传人物</A>
<br><A HREF=javascript:sf(3,625,'CH9M2') NAME='CH9M2'>　二、人物简介</A>
<br><A HREF=javascript:sf(3,626,'CH9M21') NAME='CH9M21'>　　(一)领导干部</A>
<br><A HREF=javascript:sf(3,627,'CH9M22') NAME='CH9M22'>　　(二）专业技术人员及国家级荣誉</A>
<br><A HREF=javascript:sf(3,628,'CH9M3') NAME='CH9M3'>　三、劳动模范人物表</A>
<br><A HREF=javascript:sf(3,629,'CH9M4') NAME='CH9M4'>　四、副县、正科级单位主要负责人任职情况表</A>
<br><A HREF=javascript:sf(3,630,'CH9M41') NAME='CH9M41'>　　县政府部门</A>
<br><A HREF=javascript:sf(3,631,'CH9M42') NAME='CH9M42'>　　市、县双重管理单位</A>
<br><A HREF=javascript:sf(3,632,'CH9M43') NAME='CH9M43'>　　乡、镇、区</A>
<br><A HREF=javascript:sf(3,633,'CH9N') NAME='CH9N'>附录</A>
<br><A HREF=javascript:sf(3,634,'CH9N1') NAME='CH9N1'>　―、历史大事纪要</A>
<br><A HREF=javascript:sf(3,635,'CH9N2') NAME='CH9N2'>　二、重要文献辑录</A>
<br><A HREF=javascript:sf(3,636,'CH9N21') NAME='CH9N21'>　　(一）报刊发表重要文章</A>
<br><A HREF=javascript:sf(3,637,'CH9N22') NAME='CH9N22'>　　(二）县委、县政府重要文件</A>
<br><A HREF=javascript:sf(3,638,'CH9N23') NAME='CH9N23'>　　(三）历史研究成果辑存</A>
<br><A HREF=javascript:sf(3,639,'CH9N3') NAME='CH9N3'>　三、东明历代名家主要著作一览表</A>
<br><A HREF=javascript:sf(3,640,'CH9N4') NAME='CH9N4'>　四、诗词选萃</A>
<br><A HREF=javascript:sf(3,641,'CH9N5') NAME='CH9N5'>　五、东明部分传统生产生活用具</A>
<br><A HREF=javascript:sf(3,642,'CH9N6') NAME='CH9N6'>　六、明清圣旨</A>
<br><A HREF=javascript:sf(3,643,'CH9N7') NAME='CH9N7'>　七、前志勘误表</A><hr><!--总用时93 ms--></BODY>

</HTML>


    """
    d.parse_data(html)