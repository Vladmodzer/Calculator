from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from operator import *
from kivy.config import Config

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '700')


class Calculator(App):
    hold_lbl = False
    hold_math_signs = False
    len_hide_label = None
    overall_font_size = 60

    def build(self):

        self.hide_label = ""
        # BUTTONS
        bl = BoxLayout(orientation="vertical", padding=2)

        bottom_buttons = BoxLayout(size_hint=(1, .17))
        bottom_buttons.add_widget(Button(text="0",
                                         size_hint=(.5, 1),
                                         pos=(0, 0),
                                         background_color="grey",
                                         on_press=self.add_num,
                                         font_size=self.overall_font_size
                                         )
                                  )
        bottom_buttons.add_widget(Button(text=".",
                                         size_hint=(.25, 1),
                                         pos=(400, 0),
                                         background_color="gray",
                                         on_press=self.add_num,
                                         font_size=self.overall_font_size
                                         )
                                  )
        bottom_buttons.add_widget(Button(text="=",
                                         size_hint=(.25, 1),
                                         pos=(600, 0),
                                         background_color="orange",
                                         on_press=self.add_num,
                                         font_size=self.overall_font_size
                                         )
                                  )

        buttons = GridLayout(cols=4, rows=4, size_hint=(1, .7))

        self.ac = Button(text="AC",
                         background_color=(0.93, 0.93, 0.93),
                         on_press=self.clear,
                         font_size=self.overall_font_size
                         )
        buttons.add_widget(self.ac)

        buttons.add_widget(Button(text="+/-",
                                  background_color=(0.93, 0.93, 0.93),
                                  on_press=self.add_num,
                                  font_size=self.overall_font_size)
                           )
        buttons.add_widget(Button(text="%",
                                  background_color=(0.93, 0.93, 0.93),
                                  on_press=self.add_num,
                                  font_size=self.overall_font_size)
                           )
        buttons.add_widget(Button(text="/",
                                  background_color="orange",
                                  on_press=self.add_num,
                                  font_size=self.overall_font_size)
                           )

        for i in range(7, 10):
            buttons.add_widget(Button(text=f"{i}",
                                      background_color="gray",
                                      on_press=self.add_num,
                                      font_size=self.overall_font_size
                                      )
                               )
        buttons.add_widget(Button(text="*",
                                  background_color="orange",
                                  on_press=self.add_num,
                                  font_size=self.overall_font_size
                                  )
                           )

        for i in range(4, 7):
            buttons.add_widget(Button(text=f"{i}",
                                      background_color="gray",
                                      on_press=self.add_num,
                                      font_size=self.overall_font_size
                                      )
                               )
        buttons.add_widget(Button(text="-",
                                  background_color="orange",
                                  on_press=self.add_num,
                                  font_size=self.overall_font_size
                                  )
                           )

        for i in range(1, 4):
            buttons.add_widget(Button(text=f"{i}",
                                      background_color="gray",
                                      on_press=self.add_num,
                                      font_size=self.overall_font_size
                                      )
                               )

        plus_button = Button(text="+",
                                  background_color="orange",
                                  on_press=self.add_num,

                                  font_size=self.overall_font_size
                             )

        buttons.add_widget(plus_button)
        self.lbl = Label(text="0",

                         font_size=150,
                         size_hint=(1, .3),
                         halign="right",
                         valign="bottom"
                         )

        self.lbl.bind(size=self.lbl.setter('text_size'))

        bl.add_widget(self.lbl)
        bl.add_widget(buttons)

        bl.add_widget(bottom_buttons)

        return bl

    # BRAIN
    def add_num(self, instance):

        self.math_signs = "+-*/"
        self.ac.text = "C"
        # IF DIGIT
        if instance.text.isdigit():
            # if zero add one digit
            if self.lbl.text == "0" or self.lbl.text == "-0":
                if not self.hide_label == "0":
                    self.lbl.text = instance.text
                    self.hide_label += instance.text
                    print("0", "hold_lbl", self.hold_lbl)
                    print("0", "hold_math_signs", self.hold_math_signs)
                else:
                    self.hide_label = instance.text
                    self.lbl.text = instance.text
            elif not self.hold_lbl:
                self.check_font_equals(self.lbl.text)
                self.lbl.text += instance.text
                self.hide_label += instance.text


            elif self.hold_lbl and not self.hold_math_signs:
                self.hide_label = instance.text
                self.lbl.text = instance.text
                self.hold_lbl = False
                print("1", "hold_lbl", self.hold_lbl)
                print("1", "hold_math_signs", self.hold_math_signs)

            elif self.hold_lbl and self.hold_math_signs:
                self.lbl.text = instance.text
                self.hide_label += instance.text
                self.hold_lbl = False
        # IF NOT DIGIT

        else:
            # if not math sings
            if instance.text in self.math_signs and not self.hold_math_signs and self.lbl.text != "0":
                self.hide_label = self.lbl.text
                self.hide_label += instance.text
                self.hold_lbl = True
                self.hold_math_signs = True
                self.len_hide_label = len(self.hide_label)

                print("2", "hold_lbl", self.hold_lbl)
                print("2", "hold_math_signs", self.hold_math_signs)
            elif instance.text in self.math_signs and not self.hold_math_signs and self.hide_label == "0":
                self.hide_label += instance.text
                self.hold_math_signs = True
            else:
                # if math sings
                if instance.text in self.math_signs and self.hold_math_signs:
                    if self.hide_label[0].isdigit() and self.hide_label[-1].isdigit()\
                        or self.hide_label[0] == "-"\
                            and self.hide_label[-1].isdigit():
                                if not self.hold_lbl:

                                    self.hide_label = self.answer(self.hide_label)+instance.text

                                    self.lbl.text = self.hide_label[:-1]

                                    self.hold_lbl = True
                                    self.len_hide_label = len(self.hide_label)
                                    print("3", "hold_lbl", self.hold_lbl)
                                    print("3", "hold_math_signs", self.hold_math_signs)

                                else:
                                    self.lbl.text = instance.text
                                    self.hide_label += instance.text
                                    self.hold_lbl = False
                    else:
                        pass

                elif instance.text == "=":
                    if self.hide_label:
                        if self.hide_label[0].isdigit() and self.hide_label[-1].isdigit() \
                                or self.hide_label[0] == "-" \
                                and self.hide_label[-1].isdigit():
                                    self.hide_label = self.answer(self.hide_label)
                                    self.check_font_equals(self.hide_label)

                                    self.lbl.text = self.hide_label
                                    self.hide_label = ""
                                    self.hold_lbl = True
                                    self.hold_math_signs = False
                                    print("4", "hold_lbl", self.hold_lbl)
                                    print("4", "hold_math_signs", self.hold_math_signs)
                                    print(self.lbl.font_size)

                    else:
                        pass
                elif instance.text == ".":
                    if not self.hold_lbl:
                        if "." not in self.lbl.text:
                            if not self.hold_lbl:
                                self.lbl.text += instance.text
                                self.hide_label += instance.text

                elif instance.text == "%":
                    answer = str(float(self.lbl.text) / 100)
                    if not self.hold_lbl:

                        if self.lbl.text.isdigit() or self.lbl.text[0] == "-" or "." in self.hide_label:
                            if not self.hold_math_signs:
                                answer = str(float(self.lbl.text) / 100)
                                self.check_font_equals(answer)

                                self.lbl.text = answer
                                self.hide_label = answer
                                self.hold_lbl = True
                                print("5", "hold_lbl", self.hold_lbl)
                                print("5", "hold_math_signs", self.hold_math_signs)
                            else:
                                end = None
                                for i in self.hide_label:
                                    if i in self.math_signs:
                                        end = self.hide_label.index(i)

                                self.hide_label = self.hide_label[:end+1]
                                self.check_font_equals(answer)

                                self.lbl.text = answer
                                self.hide_label += answer
                    else:
                        if not self.hold_math_signs:
                            answer = str(float(self.lbl.text) / 100)
                            self.check_font_equals(answer)

                            self.hide_label = answer
                            self.lbl.text = answer
                elif instance.text == "+/-":
                    if not self.hold_math_signs:
                        if not self.lbl.text[0] == "-":
                            self.lbl.text = "-"+self.lbl.text
                        else:
                            self.lbl.text = self.lbl.text[1:]
                    else:
                        if not self.lbl.text[0] == "-":
                            self.lbl.text = "-"+self.lbl.text
                            self.hide_label = self.hide_label[:self.len_hide_label]+self.lbl.text
                        else:
                            self.lbl.text = self.lbl.text[1:]
                            self.hide_label = self.hide_label[:self.len_hide_label]+self.hide_label[self.len_hide_label+1:]
                        print(self.len_hide_label)








        print(self.hide_label)





    # FUNCTIONS
    def callback(instance):
        pass


    def check_font_equals(self,font):
        if 9 <= len(font) <= 12 and self.lbl.font_size == 150:
            self.lbl.font_size = 105
        elif 13 <= len(font) <= 18:
            self.lbl.font_size = 73.5
        elif len(font) >= 18:
            self.lbl.font_size = 51.45

    def frontBackAddInstance(self, obj):
        self.lbl.text += obj.text
        self.hide_label += obj.text


    def clear(self, instance):
        self.lbl.text = "0"
        self.hide_label = ""
        self.ac.text = "AC"
        self.hold_math_signs = False
        self.hold_lbl = False
        self.lbl.font_size = 150

    def answer(self, nums):
        ans = str(eval(nums))
        if "." in ans and ans[-1] == "0":
            ans = str(round(float(ans)))
        return ans



    def check_math_signs(self):
        check = False

        for el in self.math_signs:
            if el in self.hide_label:
                check = True
                self.math = el
        return check

    def check_nums_for_equal(self):
       return self.hide_label[0].isdigit() and self.hide_label[-1].isdigit() or not self.hide_label[0].isdigit() and self.hide_label[-1].isdigit()



if __name__ == '__main__':
    Calculator().run()
