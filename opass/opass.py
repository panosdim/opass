#!/usr/bin/env python3
# -*- coding: iso-8859-1 -*-
# ---------------------------------------------------------------------------
# Application to calculate toll costs in Olympia Odos
#
# Copyright 2018 Panagiotis Dimopoulos (panosdim@gmail.com)
#
# Version: 2.0
# ---------------------------------------------------------------------------
"""
Olympia Odos Application

This application allows you to calculate your monthly costs of tolls
when using Olympia Pass.
In order to run the application use:
    $ python3 opass.py
"""
import json
import os
from tkinter import (Frame, Text, IntVar, Tk, END, DISABLED, NORMAL)
from tkinter import ttk
from ttkthemes import ThemedStyle
import PIL.Image
import PIL.ImageTk
import opass.workdays


def validate(action, value_if_allowed, text):
    """
    This function allows only numbers to be enter in a Tk Entry.

    :param action: Type of action (1=insert, 0=delete, -1 for others)
    :type action: string
    :param value_if_allowed: value of the entry if the edit is allowed
    :type value_if_allowed: string
    :param text: the text string being inserted or deleted, if any
    :type text: string
    :return: Returns true if text entered is number else false
    :rtype: bool
    """
    if action == '1':
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


class MainApplication(Frame):
    """
    Class for Main GUI of the application

    It inherits from Frame and creates a main window.
    """

    def __init__(self, parent, *args, **kwargs):
        self.abs_path = os.path.dirname(os.path.realpath(__file__))
        # Open configuration file and read it
        self.data_file = open(self.abs_path + '/Tolls.json')
        self.tolls_data = json.load(self.data_file)

        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.grid(pady=10, padx=10)
        self.parent.title("Olympia Odos Pass")

        # Frontal Tolls
        self.lbl_frnt_tolls = ttk.Label(self,
                                        text="Select Frontal Tolls")

        self.lbl_frnt_tolls.grid(row=0, column=0, stick='W')
        self.frontal_stations = {}
        frame0 = Frame(self)
        frame0.grid(row=1, column=0, sticky='WE', pady=5)
        cln = 0
        row = 0
        for choice in self.tolls_data["Frontal"].keys():
            self.frontal_stations[choice] = IntVar(value=0)

            ttk.Checkbutton(frame0,
                            text=choice,
                            command=self.toll_cost,
                            variable=self.frontal_stations[choice]).grid(
                                row=row,
                                column=cln,
                                stick='W')
            cln = cln + 1
            if cln == 5:
                row = row + 1
                cln = 0

        # Ramp Tolls
        self.lbl_ramp_tolls = ttk.Label(self,
                                        text="Select Ramp Tolls")

        self.lbl_ramp_tolls.grid(row=2, column=0, stick='W')
        self.ramp_stations = {}
        frame1 = Frame(self)
        frame1.grid(row=3, column=0, sticky='WE', pady=5)
        cln = 0
        row = 0
        for choice in self.tolls_data["Ramp"].keys():
            self.ramp_stations[choice] = IntVar(value=0)
            ttk.Checkbutton(frame1,
                            text=choice,
                            variable=self.ramp_stations[choice],
                            command=self.toll_cost).grid(
                                row=row,
                                column=cln,
                                stick='W')
            cln = cln + 1
            if cln == 5:
                row = row + 1
                cln = 0

        # Vehicle Type
        self.lbl_vehicle_type = ttk.Label(
            self, text="Select Vehicle Type")
        self.lbl_vehicle_type.grid(row=4, column=0, stick='W')
        frame2 = Frame(self)
        frame2.grid(row=5, column=0, sticky='WE', pady=5)
        self.vehicle_types = ['Motorcycle',
                              'Vehicles',
                              'Vehicles with 2-3 axes',
                              'Vehicles with 4 or more axes']

        self.selected_vehicle_type = IntVar(value=1)
        for idx, val in enumerate(self.vehicle_types):
            ttk.Radiobutton(frame2,
                            text=val,
                            variable=self.selected_vehicle_type,
                            value=idx,
                            command=self.vehicle_type).grid(
                                row=0,
                                column=idx,
                                stick='W')

        # Monthly passes
        frame3 = Frame(self)
        frame3.grid(row=6, column=0, sticky='WE', pady=5)
        self.lbl_monthly_passes = ttk.Label(
            frame3,
            text="Set monthly number of passes manually")
        self.lbl_monthly_passes.grid(
            row=0, column=0, sticky='W')

        vcmd = (parent.register(validate), '%d', '%P', '%S')
        self.ent_monthly_passes = ttk.Entry(
            frame3,
            validate='key',
            validatecommand=vcmd)
        self.ent_monthly_passes.grid(
            row=0, column=1, padx=5, sticky='W')

        self.lbl_monthly_passes_sel = ttk.Label(
            frame3,
            text="or select a month for working days")
        self.lbl_monthly_passes_sel.grid(
            row=1, column=0, sticky='W')

        frame4 = Frame(self)
        frame4.grid(row=7, column=0, sticky='WE', pady=5)
        self.months = ['January',
                       'February',
                       'March',
                       'April',
                       'May',
                       'June',
                       'July',
                       'August',
                       'September',
                       'Octomber',
                       'November',
                       'December']

        cln = 0
        row = 0
        self.selected_month = IntVar(value=0)
        for idx, val in enumerate(self.months):
            ttk.Radiobutton(frame4,
                            text=val,
                            variable=self.selected_month,
                            value=idx,
                            command=self.month_selected).grid(
                                row=row,
                                column=cln,
                                stick='W')
            cln = cln + 1
            if cln == 6:
                row = row + 1
                cln = 0

        # Calculate button
        self.btn_calc = ttk.Button(self, text="Caclulate",
                                   command=self.calculate)
        self.btn_calc.grid(row=8, column=0, columnspan=2, pady=10)

        # Result pane
        self.txt_result = Text(self, width=60, height=10, state=DISABLED)
        self.txt_result.grid(row=9, column=0, columnspan=2, pady=10)
        self.txt_result.tag_configure('color_blue', foreground='blue')
        self.txt_result.tag_configure('color_red', foreground='red')

        self.total = 0
        self.vehicle = 1
        self.month = 1

    def toll_cost(self):
        """Calculate total cost according to tolls selected"""
        self.total = 0
        for name, var in self.frontal_stations.items():
            if var.get() != 0:
                cost = float(self.tolls_data["Frontal"][name][self.vehicle])
                self.total = self.total + cost
        for name, var in self.ramp_stations.items():
            if var.get() != 0:
                cost = float(self.tolls_data["Ramp"][name][self.vehicle])
                self.total = self.total + cost

    def vehicle_type(self):
        """Update total cost according to vehicle type selected"""
        self.vehicle = self.selected_vehicle_type.get()
        self.toll_cost()

    def month_selected(self):
        """Update total cost according to vehicle type selected"""
        self.month = self.selected_month.get() + 1

    def check_inputs(self):
        """Check for valid input in Tk widgets"""
        validation = True
        self.txt_result.configure(state=NORMAL)
        self.txt_result.delete('1.0', END)

        if self.total == 0:
            self.txt_result.insert(
                END,
                'Please select Tolls (Frontal and/or Ramp)\n', 'color_red')
            validation = False

        return validation

    def calculate(self):
        """Calculate the monthly tolls cost"""
        if self.check_inputs():
            if (self.ent_monthly_passes.get() != ''):
                passes = int(self.ent_monthly_passes.get())
            else:
                passes = opass.workdays.getWorkingDays(self.month) * 2
            day_cost = self.total
            total_cost = 0

            for i in range(1, passes + 1):
                if i >= 1 and i <= 5:
                    cost = day_cost
                    if i == 1:
                        if passes >= 5:
                            self.txt_result.insert(
                                END,
                                "Passes %.2d - %.2d: %.2f \u20ac\n" %
                                (1, 5, cost),
                                'color_blue')

                        else:
                            self.txt_result.insert(
                                END,
                                "Passes %.2d - %.2d: %.2f \u20ac\n" %
                                (1, passes, cost),
                                'color_blue')
                elif i >= 6 and i <= 10:
                    cost = day_cost - (day_cost * 15 / 100)
                    if i == 6:
                        if passes >= 10:
                            self.txt_result.insert(
                                END,
                                "Passes %.2d - %.2d: %.2f \u20ac\n" %
                                (6, 10, cost),
                                'color_blue')
                        else:
                            self.txt_result.insert(
                                END,
                                "Passes %.2d - %.2d: %.2f \u20ac\n" %
                                (6, passes, cost),
                                'color_blue')
                elif i >= 11 and i <= 20:
                    cost = day_cost - (day_cost * 30 / 100)
                    if i == 11:
                        if passes >= 20:
                            self.txt_result.insert(
                                END,
                                "Passes %.2d - %.2d: %.2f \u20ac\n" %
                                (11, 20, cost),
                                'color_blue')
                        else:
                            self.txt_result.insert(
                                END,
                                "Passes %.2d - %.2d: %.2f \u20ac\n" %
                                (11, passes, cost),
                                'color_blue')
                elif i >= 21 and i <= 30:
                    cost = day_cost - (day_cost * 40 / 100)
                    if i == 21:
                        if passes >= 30:
                            self.txt_result.insert(
                                END,
                                "Passes %.2d - %.2d: %.2f \u20ac\n" %
                                (21, 30, cost),
                                'color_blue')
                        else:
                            self.txt_result.insert(
                                END,
                                "Passes %.2d - %.2d: %.2f \u20ac\n" %
                                (21, passes, cost),
                                'color_blue')
                elif i >= 31 and i <= 40:
                    cost = day_cost - (day_cost * 50 / 100)
                    if i == 31:
                        if passes >= 40:
                            self.txt_result.insert(
                                END,
                                "Passes %.2d - %.2d: %.2f \u20ac\n" %
                                (31, 40, cost),
                                'color_blue')
                        else:
                            self.txt_result.insert(
                                END,
                                "Passes %.2d - %.2d: %.2f \u20ac\n" %
                                (31, passes, cost),
                                'color_blue')
                elif i >= 41 and i <= 60:
                    cost = day_cost - (day_cost * 60 / 100)
                    if i == 41:
                        if passes >= 60:
                            self.txt_result.insert(
                                END,
                                "Passes %.2d - %.2d: %.2f \u20ac\n" %
                                (41, 60, cost),
                                'color_blue')
                        else:
                            self.txt_result.insert(
                                END,
                                "Passes %.2d - %.2d: %.2f \u20ac\n" %
                                (41, passes, cost),
                                'color_blue')
                else:
                    cost = day_cost
                    if i == 61:
                        self.txt_result.insert(
                            END, "Passes %.2d+: %.2f \u20ac\n" %
                            (61, cost),
                            'color_blue')

                total_cost += cost

            self.txt_result.insert(
                END,
                "Total cost: %.2f \u20ac" % total_cost,
                'color_red')
            self.txt_result.configure(state=DISABLED)


def main():
    ABS_PATH = os.path.dirname(os.path.realpath(__file__))
    ROOT = Tk()
    STYLE = ThemedStyle(ROOT)
    STYLE.set_theme("arc")
    ROOT.resizable(False, False)
    ROOT.update()
    im = PIL.Image.open(ABS_PATH + '/toll.png')
    IMG = PIL.ImageTk.PhotoImage(im)
    ROOT.call('wm', 'iconphoto', ROOT._w, IMG)  # pylint: disable=W0212
    MainApplication(ROOT)
    ROOT.mainloop()


if __name__ == "__main__":
    main()
