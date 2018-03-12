#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
# ---------------------------------------------------------------------------
# Application to calculate toll costs in Olympia Odos
#
# Copyright 2018 Panagiotis Dimopoulos (panosdim@gmail.com)
#
# Version: 1.0
# ---------------------------------------------------------------------------

from tkinter import *
import os
import json


class MainApplication(Frame):
    def __init__(self, parent, *args, **kwargs):
        self.ABS_PATH = os.path.dirname(os.path.realpath(__file__))
        # Open configuration file and read it
        self.data_file = open(self.ABS_PATH + '/Tolls.json')
        self.tolls_data = json.load(self.data_file)

        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.pack(pady=10, padx=10)
        self.parent.title("Olympia Odos Pass")

        self.MB_TOLLS = Menubutton(self,
                                   text="Select Tolls",
                                   indicatoron=True,
                                   borderwidth=1,
                                   width=25,
                                   bg='deep sky blue',
                                   relief="raised")
        self.MENU = Menu(self.MB_TOLLS, tearoff=False)
        self.MB_TOLLS.configure(menu=self.MENU)
        self.MB_TOLLS.grid(row=0, column=0, pady=10, padx=10)
        self.tolls = {}
        for choice in self.tolls_data.keys():
            self.tolls[choice] = IntVar(value=0)
            self.MENU.add_checkbutton(label=choice,
                                      variable=self.tolls[choice],
                                      onvalue=1, offvalue=0,
                                      command=self.tollCost)

        self.MB_VEHICLE = Menubutton(self,
                                     text="Select Vehicle Type",
                                     indicatoron=True,
                                     borderwidth=1,
                                     width=25,
                                     bg='gray61',
                                     relief="raised")
        self.VH_MENU = Menu(self.MB_VEHICLE, tearoff=False)
        self.MB_VEHICLE.configure(menu=self.VH_MENU)
        self.MB_VEHICLE.grid(row=0, column=1, pady=10, padx=10)
        self.vehicle_types = ['Motorcycle',
                              'Vehicles',
                              'Vehicles with 2-3 axes',
                              'Vehicles with 4 or more axes']
        for idx, val in enumerate(self.vehicle_types):
            self.VH_MENU.add_command(
                label=val, command=lambda idx=idx: self.vehicleType(idx))

        self.LBL_TIMES = Label(self, text="Monthly number of passes", width=25)
        self.LBL_TIMES.grid(row=1, column=0, pady=10, padx=10)

        vcmd = (parent.register(self.validate), '%d',
                '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.times = IntVar()
        self.ENT_TIMES = Entry(
            self,
            textvariable=self.times,
            width=25,
            bg='sandy brown',
            validate='key',
            validatecommand=vcmd)
        self.ENT_TIMES.grid(row=1, column=1, pady=10, padx=10)

        self.BTN_CALC = Button(self, text="Caclulate",
                               command=self.calculate, bg='green')
        self.BTN_CALC.grid(row=2, column=0, columnspan=2, pady=10, padx=10)

        self.TXT_RESULT = Text(self, width=60, height=10, state=DISABLED)
        self.TXT_RESULT.grid(row=3, column=0, columnspan=2, pady=10, padx=10)
        self.TXT_RESULT.tag_configure('color_blue', foreground='blue')
        self.TXT_RESULT.tag_configure('color_red', foreground='red')

        self.total = 0
        self.vehicle = 0

    def validate(self, action, index, value_if_allowed,
                 prior_value, text, validation_type,
                 trigger_type, widget_name):
        if(action == '1'):
            if text in '0123456789':
                try:
                    int(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        else:
            return True

    def tollCost(self):
        self.total = 0
        self.MB_TOLLS.configure(text='Select Tolls')
        tolls = ''
        for name, var in self.tolls.items():
            if var.get() != 0:
                cost = float(self.tolls_data[name][self.vehicle])
                self.total = self.total + cost
                tolls = tolls + name + ', '
        if tolls != '':
            tolls = tolls[:-2]
            self.MB_TOLLS.configure(text=tolls)

    def vehicleType(self, idx):
        self.vehicle = idx
        self.MB_VEHICLE.configure(text=self.vehicle_types[idx])
        self.tollCost()

    def checkInputs(self):
        validation = True
        self.TXT_RESULT.configure(state=NORMAL)
        self.TXT_RESULT.delete('1.0', END)

        if self.total == 0:
            self.TXT_RESULT.insert(
                END, 'Please select Tolls\n', 'color_red')
            validation = False

        if self.MB_VEHICLE['text'] == 'Select Vehicle Type':
            self.TXT_RESULT.insert(
                END, 'Please select Vehicle Type\n', 'color_red')
            validation = False

        if self.ENT_TIMES.get() == '':
            self.TXT_RESULT.insert(
                END, 'Please specify the monthly passes\n', 'color_red')
            validation = False

        return validation

    def calculate(self):
        if self.checkInputs():
            passes = self.times.get()
            day_cost = self.total
            totalCost = 0

            for i in range(1, passes + 1):
                if i >= 1 and i <= 5:
                    cost = day_cost
                    if i == 1:
                        if passes >= 5:
                            self.TXT_RESULT.insert(
                                END,
                                "Passes %.2d - %.2d: %.2f \u20ac\n" %
                                (1, 5, cost),
                                'color_blue')

                        else:
                            self.TXT_RESULT.insert(
                                END,
                                "Passes %.2d - %.2d: %.2f \u20ac\n" %
                                (1, passes, cost),
                                'color_blue')
                elif i >= 6 and i <= 10:
                    cost = day_cost - (day_cost * 15 / 100)
                    if i == 6:
                        if passes >= 10:
                            self.TXT_RESULT.insert(
                                END,
                                "Passes %.2d - %.2d: %.2f \u20ac\n" %
                                (6, 10, cost),
                                'color_blue')
                        else:
                            self.TXT_RESULT.insert(
                                END,
                                "Passes %.2d - %.2d: %.2f \u20ac\n" %
                                (6, passes, cost),
                                'color_blue')
                elif i >= 11 and i <= 20:
                    cost = day_cost - (day_cost * 30 / 100)
                    if i == 11:
                        if passes >= 20:
                            self.TXT_RESULT.insert(
                                END,
                                "Passes %.2d - %.2d: %.2f \u20ac\n" %
                                (11, 20, cost),
                                'color_blue')
                        else:
                            self.TXT_RESULT.insert(
                                END,
                                "Passes %.2d - %.2d: %.2f \u20ac\n" %
                                (11, passes, cost),
                                'color_blue')
                elif i >= 21 and i <= 30:
                    cost = day_cost - (day_cost * 40 / 100)
                    if i == 21:
                        if passes >= 30:
                            self.TXT_RESULT.insert(
                                END,
                                "Passes %.2d - %.2d: %.2f \u20ac\n" %
                                (21, 30, cost),
                                'color_blue')
                        else:
                            self.TXT_RESULT.insert(
                                END,
                                "Passes %.2d - %.2d: %.2f \u20ac\n" %
                                (21, passes, cost),
                                'color_blue')
                elif i >= 31 and i <= 40:
                    cost = day_cost - (day_cost * 50 / 100)
                    if i == 31:
                        if passes >= 40:
                            self.TXT_RESULT.insert(
                                END,
                                "Passes %.2d - %.2d: %.2f \u20ac\n" %
                                (31, 40, cost),
                                'color_blue')
                        else:
                            self.TXT_RESULT.insert(
                                END,
                                "Passes %.2d - %.2d: %.2f \u20ac\n" %
                                (31, passes, cost),
                                'color_blue')
                elif i >= 41 and i <= 60:
                    cost = day_cost - (day_cost * 60 / 100)
                    if i == 41:
                        if passes >= 60:
                            self.TXT_RESULT.insert(
                                END,
                                "Passes %.2d - %.2d: %.2f \u20ac\n" %
                                (41, 60, cost),
                                'color_blue')
                        else:
                            self.TXT_RESULT.insert(
                                END,
                                "Passes %.2d - %.2d: %.2f \u20ac\n" %
                                (41, passes, cost),
                                'color_blue')
                else:
                    cost = day_cost
                    if i == 61:
                        self.TXT_RESULT.insert(
                            END, "Passes %.2d+: %.2f \u20ac\n" %
                            (61, cost),
                            'color_blue')

                totalCost += cost

            self.TXT_RESULT.insert(
                END,
                "Total cost: %.2f \u20ac" % totalCost,
                'color_red')
            self.TXT_RESULT.configure(state=DISABLED)


if __name__ == "__main__":
    ABS_PATH = os.path.dirname(os.path.realpath(__file__))
    root = Tk()
    root.resizable(False, False)
    root.update()
    img = PhotoImage(file=ABS_PATH + '/opass.gif')
    root.call('wm', 'iconphoto', root._w, img)
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
