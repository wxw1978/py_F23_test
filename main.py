 #! usr/bin/python 
 #coding=utf-8 

 # # # # # # # # # # # # # # # # # # # # 
# # # # # # # # # # # # # # # # # # # # 
import wx
import random
import com_work

#---------------------------------------------------------------------------
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

#---------------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        self.freezeing = False

        self.R2 = None
        self.R3_version = None

        self.R2_timeouts = 0
        self.R2_errors = 0

        b = wx.Button(self, -1, "同步 R0 R1", (650, 47+10))
        self.Bind(wx.EVT_BUTTON, self.OnClickGet_R0_R1, b)


        wx.StaticText(self, -1, "【软件版本】R3:", (20, 5+10), (140, -1), wx.ALIGN_RIGHT).SetForegroundColour('Blue')
        # ---------------------
        wx.StaticText(self, -1, "保留 R2-7:",        (20, 47+10), (140, -1), wx.ALIGN_RIGHT)
        wx.StaticText(self, -1, "后拉摄像头 R2-6:",   (20, 47+30), (140, -1), wx.ALIGN_RIGHT)
        wx.StaticText(self, -1, "重力感应开机 R2-5:",  (20, 47+50), (140, -1), wx.ALIGN_RIGHT)
        wx.StaticText(self, -1, "倒车信号 R2-4:",     (20, 47+70), (140, -1), wx.ALIGN_RIGHT)
        wx.StaticText(self, -1, "SD卡检测 R2-3:",     (20, 47+90), (140, -1), wx.ALIGN_RIGHT)
        wx.StaticText(self, -1, "USB 检测 R2-2:",    (20, 47+110), (140, -1), wx.ALIGN_RIGHT)
        wx.StaticText(self, -1, "电源键开机 R2-1:",   (20, 47+130), (140, -1), wx.ALIGN_RIGHT)
        wx.StaticText(self, -1, "雷达数据 R2-0:",     (20, 47+150), (140, -1), wx.ALIGN_RIGHT)
        wx.StaticText(self, -1, "  雷达数据:",        (20, 47+180), (140, -1), wx.ALIGN_RIGHT)
        b = wx.Button(self, -1, "清除", (104, 47+200), (50,-1))
        self.Bind(wx.EVT_BUTTON, self.OnClickClearRadar, b)

        self.cR3 = wx.StaticText(self, -1, "无数据", (170, 5+10), (520, -1), wx.ALIGN_LEFT)
        self.cR3.SetBackgroundColour('WHEAT');  self.cR3.SetForegroundColour('Blue')
        # ---------------------
        self.cR2_7 = wx.StaticText(self, -1, "无数据", (170, 47+10), (120, -1), wx.ALIGN_LEFT)
        self.cR2_7.SetBackgroundColour('Grey');  self.cR2_7.SetForegroundColour('White')
        self.cR2_6 = wx.StaticText(self, -1, "无数据", (170, 47+30), (120, -1), wx.ALIGN_LEFT)
        self.cR2_6.SetBackgroundColour('Grey');  self.cR2_6.SetForegroundColour('White')
        self.cR2_5 = wx.StaticText(self, -1, "无数据", (170, 47+50), (120, -1), wx.ALIGN_LEFT)
        self.cR2_5.SetBackgroundColour('Grey');  self.cR2_5.SetForegroundColour('White')
        self.cR2_4 = wx.StaticText(self, -1, "无数据", (170, 47+70), (120, -1), wx.ALIGN_LEFT)
        self.cR2_4.SetBackgroundColour('Grey');  self.cR2_4.SetForegroundColour('White')
        self.cR2_3 = wx.StaticText(self, -1, "无数据", (170, 47+90), (120, -1), wx.ALIGN_LEFT)
        self.cR2_3.SetBackgroundColour('Grey');  self.cR2_3.SetForegroundColour('White')
        self.cR2_2 = wx.StaticText(self, -1, "无数据",  (170, 47+110), (120, -1), wx.ALIGN_LEFT)
        self.cR2_2.SetBackgroundColour('Grey');  self.cR2_2.SetForegroundColour('White')
        self.cR2_1 = wx.StaticText(self, -1, "无数据",  (170, 47+130), (120, -1), wx.ALIGN_LEFT)
        self.cR2_1.SetBackgroundColour('Grey');  self.cR2_1.SetForegroundColour('White')
        self.cR2_0 = wx.StaticText(self, -1, "无数据",  (170, 47+150), (120, -1), wx.ALIGN_LEFT)
        self.cR2_0.SetBackgroundColour('Grey');  self.cR2_0.SetForegroundColour('White')

        self.cRADA = wx.TextCtrl(self, -1,
                        "暂未开通\n", 
                        pos=(170, 47+180),
                        size=(210, 180), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER|wx.TE_READONLY)
        self.cRADA.SetBackgroundColour('Light Grey');

        self.cR2_timeouts = wx.StaticText(self, -1, "  R2 返回超时: 0", (20, 47+390))
        self.cR2_errors   = wx.StaticText(self, -1, "  R2 数据错误: 0", (20, 47+410))

        self.cR0_success  = wx.StaticText(self, -1, "  R0 返回成功: 0", (650, 47+ 95))
        self.cR0_timeouts = wx.StaticText(self, -1, "  R0 返回超时: 0", (650, 47+115))
        self.cR0_errors   = wx.StaticText(self, -1, "  R0 数据错误: 0", (650, 47+135))
        self.R0_success  = 0
        self.R0_timeouts = 0
        self.R0_errors   = 0

        self.cR1_success  = wx.StaticText(self, -1, "  R1 返回成功: 0", (650, 47+240))
        self.cR1_timeouts = wx.StaticText(self, -1, "  R1 返回超时: 0", (650, 47+260))
        self.cR1_errors   = wx.StaticText(self, -1, "  R1 数据错误: 0", (650, 47+280))
        self.R1_success  = 0
        self.R1_timeouts = 0
        self.R1_errors   = 0

        self.cR0_7 = wx.CheckBox(self, -1, "雷达开关")#, (65, 40), (150, 20), wx.NO_BORDER)
        self.cR0_6 = wx.CheckBox(self, -1, "AW6121和摄像头开关")#, (65, 60), (150, 20), wx.NO_BORDER)
        self.cR0_5 = wx.CheckBox(self, -1, "屏幕开关")#, (65, 80), (150, 20), wx.NO_BORDER)
        self.cR0_4 = wx.CheckBox(self, -1, "通知MCU关闭电源")
        self.cR0_3 = wx.CheckBox(self, -1, "屏幕背光电源开关")
        self.cR0_2 = wx.CheckBox(self, -1, "后拉摄像头电源开关")
        self.cR0_1 = wx.CheckBox(self, -1, "屏幕GPIO口电源开关")
        self.cR0_0 = wx.CheckBox(self, -1, "触摸屏电源开关")
        st0 = wx.StaticText(self, -1, "-------------------------")
        self.cR1_7 = wx.CheckBox(self, -1, "E7 MCU 版本设置,0:V1,1:V2")
        self.cR1_6 = wx.CheckBox(self, -1, "保留")
        self.cR1_5 = wx.CheckBox(self, -1, "背光最亮")

        # ------------
        st1 = wx.StaticText(self, -1, "背光调节 0~31:")
        sc = wx.SpinCtrl(self, -1, "", (30, 50))
        sc.SetRange(0,31); sc.SetValue(16)
        self.cR1_4_0 = sc
        self.R1_4_0_val = self.cR1_4_0.GetValue()

        self.Bind(wx.EVT_SPINCTRL, self.OnSpin_R1_4_0, self.cR1_4_0)
        self.Bind(wx.EVT_TEXT, self.OnText_R1_4_0, self.cR1_4_0)

        # ------------
        st2 = wx.StaticText(self, -1, "===========================")
        st3 = wx.StaticText(self, -1, "随机测试: 间隔时间ms")
        sc = wx.SpinCtrl(self, -1, "", (30, 50))
        sc.SetRange(10,1000); sc.SetValue(500)
        self.cRandomTest = sc
        self.RandomTest_val = self.cRandomTest.GetValue()

        self.Bind(wx.EVT_SPINCTRL, self.OnSpin_RandomTest, self.cRandomTest)
        self.Bind(wx.EVT_TEXT, self.OnText_RandomTest, self.cRandomTest)

        b_test = wx.Button(self, -1, "  开始随机测试  .")
        self.Bind(wx.EVT_BUTTON, self.OnClickRandomTest, b_test)
        
        # ------------
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox0, self.cR0_7)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox0, self.cR0_6)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox0, self.cR0_5)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox0, self.cR0_4)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox0, self.cR0_3)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox0, self.cR0_2)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox0, self.cR0_1)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox0, self.cR0_0)

        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox1, self.cR1_7)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox1, self.cR1_6)
        self.Bind(wx.EVT_CHECKBOX, self.EvtCheckBox1, self.cR1_5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddMany( [ 
            (20,46),
            self.cR0_7,
            self.cR0_6,
            (20,8),
            self.cR0_5,
            self.cR0_4,
            (20,8),
            self.cR0_3,
            self.cR0_2,
            (20,8),
            self.cR0_1,
            self.cR0_0,
            (20,4),
            st0,
            (20,4),
            self.cR1_7,
            self.cR1_6,
            (20,8),
            self.cR1_5,
            (20,4),
            st1,
            (20,8),
            self.cR1_4_0,
            (20,16),
            st2,
            (20,3),
            st3,
            (20,3),
            self.cRandomTest,
            (20,3),
            b_test
                      ])

        border = wx.BoxSizer(wx.VERTICAL)
        border.Add(sizer, 0, wx.LEFT, 450)
        self.SetSizer(border)

        # ------------  read R3 软件版本 

        # ------------
        self.t1 = wx.Timer(self, 99)
        # self.t1.Start(332)
        self.t1.Start(332)
        self.log.write("EVT_TIMER timer started\n")
        self.Bind(wx.EVT_TIMER, self.OnMainReadTimer)

    def UpdateUI_R3_version(self):
        if self.R3_version is None:
            return
        r3 = self.R3_version
        if r3[0:4] != 'A03D': # 无效答复 
            self.cR3.SetLabel('无效的答复格式')
            self.cR3.SetForegroundColour('Red')
            self.R3_version = None
        else:
            self.cR3.SetLabel(r3[4:6])
            self.cR3.SetForegroundColour('Blue')
        return

    def UI_R2_TimeOut(self):
        self.cR2_7.SetLabel("无数据-超时")
        self.cR2_7.SetBackgroundColour('Yellow');  self.cR2_7.SetForegroundColour('Red')
        self.cR2_6.SetLabel("无数据-超时")
        self.cR2_6.SetBackgroundColour('Yellow');  self.cR2_6.SetForegroundColour('Red')
        self.cR2_5.SetLabel("无数据-超时")
        self.cR2_5.SetBackgroundColour('Yellow');  self.cR2_5.SetForegroundColour('Red')
        self.cR2_4.SetLabel("无数据-超时")
        self.cR2_4.SetBackgroundColour('Yellow');  self.cR2_4.SetForegroundColour('Red')
        self.cR2_3.SetLabel("无数据-超时")
        self.cR2_3.SetBackgroundColour('Yellow');  self.cR2_3.SetForegroundColour('Red')
        self.cR2_2.SetLabel("无数据-超时")
        self.cR2_2.SetBackgroundColour('Yellow');  self.cR2_2.SetForegroundColour('Red')
        self.cR2_1.SetLabel("无数据-超时")
        self.cR2_1.SetBackgroundColour('Yellow');  self.cR2_1.SetForegroundColour('Red')
        self.cR2_0.SetLabel("无数据-超时")
        self.cR2_0.SetBackgroundColour('Yellow');  self.cR2_0.SetForegroundColour('Red')

        self.cR2_timeouts.SetLabel("  R2 返回超时: " + str(self.R2_timeouts))
        self.cR2_timeouts.SetForegroundColour('Red')

    def UI_R2_Invalide(self):
        self.cR2_7.SetLabel("无效答复-"+self.R2)
        self.cR2_7.SetBackgroundColour('Yellow');  self.cR2_7.SetForegroundColour('Red')
        self.cR2_6.SetLabel("无效答复-"+self.R2)
        self.cR2_6.SetBackgroundColour('Yellow');  self.cR2_6.SetForegroundColour('Red')
        self.cR2_5.SetLabel("无效答复-"+self.R2)
        self.cR2_5.SetBackgroundColour('Yellow');  self.cR2_5.SetForegroundColour('Red')
        self.cR2_4.SetLabel("无效答复-"+self.R2)
        self.cR2_4.SetBackgroundColour('Yellow');  self.cR2_4.SetForegroundColour('Red')
        self.cR2_3.SetLabel("无效答复-"+self.R2)
        self.cR2_3.SetBackgroundColour('Yellow');  self.cR2_3.SetForegroundColour('Red')
        self.cR2_2.SetLabel("无效答复-"+self.R2)
        self.cR2_2.SetBackgroundColour('Yellow');  self.cR2_2.SetForegroundColour('Red')
        self.cR2_1.SetLabel("无效答复-"+self.R2)
        self.cR2_1.SetBackgroundColour('Yellow');  self.cR2_1.SetForegroundColour('Red')
        self.cR2_0.SetLabel("无效答复-"+self.R2)
        self.cR2_0.SetBackgroundColour('Yellow');  self.cR2_0.SetForegroundColour('Red')

        self.cR2_errors.SetLabel("  R2 数据错误: " + str(self.R2_errors))
        self.cR2_errors.SetForegroundColour('VIOLET RED')

    def UI_R2_Valide(self, b):

        b7 = (b & 128) >> 7
        b6 = (b &  64) >> 6
        b5 = (b &  32) >> 5
        b4 = (b &  16) >> 4
        b3 = (b &   8) >> 3
        b2 = (b &   4) >> 2
        b1 = (b &   2) >> 1
        b0 = (b &   1) >> 0
        if b7 == 1:
            self.cR2_7.SetLabel("1 保留")
        else:
            self.cR2_7.SetLabel("0 保留")
        self.cR2_7.SetBackgroundColour('Light Grey');  self.cR2_7.SetForegroundColour('Grey')
        if b6 == 1:
            self.cR2_6.SetLabel("已拔出")
            self.cR2_6.SetBackgroundColour('Light Grey');  self.cR2_6.SetForegroundColour('ORANGE RED')
        else:
            self.cR2_6.SetLabel("已接入")
            self.cR2_6.SetBackgroundColour('White');  self.cR2_6.SetForegroundColour('Dark Green')
        if b5 == 1:
            self.cR2_5.SetLabel("重力感应 !")
            self.cR2_5.SetBackgroundColour('Light Grey');  self.cR2_5.SetForegroundColour('ORANGE RED')
        else:
            self.cR2_5.SetLabel("无感应")
            self.cR2_5.SetBackgroundColour('White');  self.cR2_5.SetForegroundColour('Dark Green')
        if b4 == 1:
            self.cR2_4.SetLabel("无")
            self.cR2_4.SetBackgroundColour('White');  self.cR2_4.SetForegroundColour('Dark Green')
        else:
            self.cR2_4.SetLabel("倒车 !")
            self.cR2_4.SetBackgroundColour('Light Grey');  self.cR2_4.SetForegroundColour('ORANGE RED')
        if b3 == 1:
            self.cR2_3.SetLabel("SD卡拔出 !")
            self.cR2_3.SetBackgroundColour('Light Grey');  self.cR2_3.SetForegroundColour('ORANGE RED')
        else:
            self.cR2_3.SetLabel("有SD卡")
            self.cR2_3.SetBackgroundColour('White');  self.cR2_3.SetForegroundColour('Dark Green')
        if b2 == 1:
            self.cR2_2.SetLabel("USB拔出 !")
            self.cR2_2.SetBackgroundColour('Light Grey');  self.cR2_2.SetForegroundColour('ORANGE RED')
        else:
            self.cR2_2.SetLabel("有USB连接")
            self.cR2_2.SetBackgroundColour('White');  self.cR2_2.SetForegroundColour('Dark Green')
        if b1 == 1:
            self.cR2_1.SetLabel("1")
            self.cR2_1.SetBackgroundColour('Light Grey');  self.cR2_1.SetForegroundColour('ORANGE RED')
        else:
            self.cR2_1.SetLabel("0")
            self.cR2_1.SetBackgroundColour('White');  self.cR2_1.SetForegroundColour('Dark Green')
        if b0 == 1:
            self.cR2_0.SetLabel("有雷达数据 !")
            self.cR2_0.SetBackgroundColour('Light Grey');  self.cR2_0.SetForegroundColour('ORANGE RED')
        else:
            self.cR2_0.SetLabel("无")
            self.cR2_0.SetBackgroundColour('White');  self.cR2_0.SetForegroundColour('Dark Green')


    def UpdateUI_R2(self):
        if self.R2 is None:
            self.R2_timeouts += 1
            self.UI_R2_TimeOut()
            # com_work.clear_read_buf(32)
            return
        r2 = self.R2
        if r2[0:4] != 'A02D': # 无效答复 
            self.R2_errors += 1
            self.UI_R2_Invalide()
            self.R2 = None
            # com_work.clear_read_buf(32)
        else:
            x = eval('0x' + r2[4:6])
            self.UI_R2_Valide(x)

    def OnTimer99(self):
        if self.R3_version is None :
            self.R3_version = com_work.read_R3_soft_version()
            self.UpdateUI_R3_version()
        else :
            self.R2 = com_work.read_R2()
            self.UpdateUI_R2()
        # self.log.write("OnTimer99\n")

    ######################################
    #
    def GetUI_R0(self):
        x = 0
        if self.cR0_7.GetValue(): x += 128
        if self.cR0_6.GetValue(): x +=  64
        if self.cR0_5.GetValue(): x +=  32
        if self.cR0_4.GetValue(): x +=  16
        if self.cR0_3.GetValue(): x +=   8
        if self.cR0_2.GetValue(): x +=   4
        if self.cR0_1.GetValue(): x +=   2
        if self.cR0_0.GetValue(): x +=   1
        return x

    def UpdateUI_R0(self, b):
        if b is None:
            return
        #-=-=-=-=-=-=-=-=-=-=-=-=-#
        self.freezeing = True  
        b7 = True if ( ((b & 128) >> 7) == 1 ) else False
        b6 = True if ( ((b &  64) >> 6) == 1 ) else False
        b5 = True if ( ((b &  32) >> 5) == 1 ) else False
        b4 = True if ( ((b &  16) >> 4) == 1 ) else False
        b3 = True if ( ((b &   8) >> 3) == 1 ) else False
        b2 = True if ( ((b &   4) >> 2) == 1 ) else False
        b1 = True if ( ((b &   2) >> 1) == 1 ) else False
        b0 = True if ( ((b &   1) >> 0) == 1 ) else False
        self.cR0_7.SetValue(b7)
        self.cR0_6.SetValue(b6)
        self.cR0_5.SetValue(b5)
        self.cR0_4.SetValue(b4)
        self.cR0_3.SetValue(b3)
        self.cR0_2.SetValue(b2)
        self.cR0_1.SetValue(b1)
        self.cR0_0.SetValue(b0)
        self.freezeing = False  
        #-=-=-=-=-=-=-=-=-=-=-=-=-#

    def GetUI_R1(self):
        x = 0
        if self.cR1_7.GetValue(): x += 128
        if self.cR1_6.GetValue(): x +=  64
        if self.cR1_5.GetValue(): x +=  32
        x += self.R1_4_0_val
        return x

    def UpdateUI_R1(self, b):
        if b is None:
            return
        #-=-=-=-=-=-=-=-=-=-=-=-=-#
        self.freezeing = True
        b7 = True if ( ((b & 128) >> 7) == 1 ) else False
        b6 = True if ( ((b &  64) >> 6) == 1 ) else False
        b5 = True if ( ((b &  32) >> 5) == 1 ) else False
        self.cR1_7.SetValue(b7)
        self.cR1_6.SetValue(b6)
        self.cR1_5.SetValue(b5)
        self.R1_4_0_val = b & (1+2+4+8+16)
        self.cR1_4_0.SetValue(self.R1_4_0_val)
        self.freezeing = False
        #-=-=-=-=-=-=-=-=-=-=-=-=-#

    def OnTimerTest(self):
        # self.log.write("OnTimerTest\n")
        # 得到一个随机值 0~512
        r = random.randint(0,511)
        if r<255: 
            self.UpdateUI_R0(r)
            self.Do_R0_Operator()
        else:
            self.UpdateUI_R1(r-255)
            self.Do_R1_Operator()
    #
    ######################################

    def OnMainReadTimer(self, evt):
        if 99 == evt.GetTimer().GetId():
            self.OnTimer99()
        else:
            self.OnTimerTest()

    def StartTest(self, ms):
        self.t2 = wx.Timer(self, 808)
        self.t2.Start(ms)
        self.log.write("self.t2 timer started\n")

    def StopTest(self):
        self.t2.Stop()
        self.log.write("self.t2 timer stoped\n")
        del self.t2

    # 开始随机测试
    def OnClickRandomTest(self, evt): 
        obj = evt.GetEventObject()
        lbl = obj.GetLabel()
        self.log.WriteText(lbl)
        if lbl == u"- 停止随机测试 -.":
            self.StopTest()
            obj.SetLabel("  开始随机测试  .")
        else:
            self.StartTest(self.RandomTest_val)
            obj.SetLabel("- 停止随机测试 -.")
        return 0

    # 清除雷达数据
    def OnClickClearRadar(self, evt):
        return 0

    # 清除雷达数据
    def OnClickGet_R0_R1(self, evt):
        self.UpdateUI_R0(com_work.read_R0)
        self.UpdateUI_R1(com_work.read_R1)

    def Do_R0_Operator(self):
        x = self.GetUI_R0()

        data = "W00D" + hex(x)[2:4].upper()
        ret = com_work.send_and_read6(data, 0.2)
        resp = "B00D" + hex(x)[2:4].upper()

        if ret is None or len(ret) < 6: # 返回超时 
            self.R0_timeouts += 1
            self.cR0_timeouts.SetLabel("  R0 返回超时: " + str(self.R0_timeouts))
            self.cR0_timeouts.SetForegroundColour('Red')
        elif ret == resp:
            self.R0_success += 1
            self.cR0_success.SetLabel("  R0 返回成功: " + str(self.R0_success))
            self.cR0_success.SetForegroundColour('Green')
        else:
            self.R0_errors += 1
            self.cR0_errors.SetLabel("  R0 返回错误: " + str(self.R0_errors))
            self.cR0_errors.SetForegroundColour('Red')

    def Do_R1_Operator(self):
        x = self.GetUI_R1()

        data = "W01D" + hex(x)[2:4].upper()
        ret = com_work.send_and_read6(data, 0.2)
        resp = "B01D" + hex(x)[2:4].upper()

        if ret is None or len(ret) < 6: # 返回超时 
            self.R1_timeouts += 1
            self.cR1_timeouts.SetLabel("  R1 返回超时: " + str(self.R1_timeouts))
            self.cR1_timeouts.SetForegroundColour('Red')
        elif ret == resp:
            self.R1_success += 1
            self.cR1_success.SetLabel("  R1 返回成功: " + str(self.R1_success))
            self.cR1_success.SetForegroundColour('Green')
        else:
            self.R1_errors += 1
            self.cR1_errors.SetLabel("  R1 返回错误: " + str(self.R1_errors))
            self.cR1_errors.SetForegroundColour('Red')

    # CheckBox 相应 事件
    def EvtCheckBox0(self, event):
        if not self.freezeing :
            self.Do_R0_Operator()
        # self.log.write('EvtCheckBox: %d\n' % event.IsChecked())
        # cb = event.GetEventObject()
        # self.log.write("EvtCheckBox: %s\n" % cb.GetLabel())
        

    # CheckBox 相应 事件
    def EvtCheckBox1(self, event):
        if not self.freezeing :
            self.Do_R1_Operator()
        # self.log.write('EvtCheckBox: %d\n' % event.IsChecked())
        # cb = event.GetEventObject()
        # self.log.write("EvtCheckBox: %s\n" % cb.GetLabel())

    def OnSpin_RandomTest(self, evt):
        v = self.cRandomTest.GetValue()
        if self.RandomTest_val != v :
            self.log.write('new value: %d\n' % v)
            self.RandomTest_val = v

    def OnText_RandomTest(self, evt):
        self.OnSpin_RandomTest(evt)


    def OnSpin_R1_4_0(self, evt):
        v = self.cR1_4_0.GetValue()
        if self.R1_4_0_val != v :
            self.log.write('new value: %d\n' % v)
            self.R1_4_0_val = v
            if not self.freezeing :
                self.Do_R1_Operator()

    def OnText_R1_4_0(self, evt):
        self.OnSpin_R1_4_0(evt)

    def EvtComboBox(self, evt):
        cb = evt.GetEventObject()
        data = cb.GetClientData(evt.GetSelection())
        self.log.WriteText('EvtComboBox: %s\nClientData: %s\n' % (evt.GetString(), data))

        if evt.GetString() == 'one':
            self.log.WriteText("You follow directions well!\n\n")


#---------------------------------------------------------------------------

def runTest(frame, nb, log):

    #
    com_work.init(log)

    # com_work.send_and_read6('i am wangxiaowu')

    #
    win = TestPanel(nb, log)
    return win


#---------------------------------------------------------------------------

if __name__ == '__main__':
    import sys,os
    import run


    run.main(['', os.path.basename(sys.argv[0])] + sys.argv[1:])

