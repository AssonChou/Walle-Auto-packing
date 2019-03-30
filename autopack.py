#!/usr/bin/python
# -*- coding: UTF-8 -*-
# coding: utf8

import os
from Tkinter import *
import subprocess
import json
import tkMessageBox


class GUI:
    # 定义GUI界面
    def __init__(self, root, param, function):
        root.title("Walle AutoPacking")
        Label(root, width=30, text="Build Tools Path", justify="left").grid(column=0, row=0, pady=10, sticky=E)
        Entry(root, width=60, textvariable=param.build_tools_path, bd=1).grid(column=1, row=0, padx=10)

        Label(root, width=30, text="Before Apk Path", justify="left").grid(column=0, row=1, pady=10, sticky=E)
        Entry(root, width=60, textvariable=param.pre_apk_path, bd=1).grid(column=1, row=1, padx=10)

        Label(root, width=30, text="After Apk Dir", justify="left").grid(column=0, row=2, pady=10, sticky=E)
        Entry(root, width=60, textvariable=param.after_apk_path, bd=1).grid(column=1, row=2, padx=10)

        Label(root, width=30, text="Generate Apk Name", justify="left").grid(column=0, row=3, pady=10, sticky=E)
        Entry(root, width=60, textvariable=param.app_name, bd=1).grid(column=1, row=3, padx=10)

        Label(root, width=30, text="Keystore Path", justify="left").grid(column=0, row=4, pady=10, sticky=E)
        Entry(root, width=60, textvariable=param.keystore_path, bd=1).grid(column=1, row=4, padx=10)

        Label(root, width=30, text="Keystore Password", justify="left").grid(column=0, row=5, pady=10, sticky=E)
        Entry(root, width=60, textvariable=param.password, bd=1).grid(column=1, row=5, padx=10)

        Checkbutton(root, text="(1) Zipalign    ", variable=param.is_zipalign).grid(column=0, row=6, sticky=E)
        Checkbutton(root, text="(2) Sign         ", variable=param.is_sign).grid(column=1, row=6)
        Checkbutton(root, text="(3) Check Sign", variable=param.is_check_sign).grid(column=0, row=7, sticky=E)
        Checkbutton(root, text="(4) Multi Pack", variable=param.is_multi_pack).grid(column=1, row=7)

        Button(root, height=1, width=28, text="Generate", command=lambda: function.select()).grid(column=1, row=8,
                                                                                                  sticky=W, pady=10,
                                                                                                  padx=10)

        Button(root, height=1, width=28, text="Save Config", command=lambda: function.save()).grid(column=1, row=9,
                                                                                                  sticky=W, pady=20,
                                                                                                  padx=10)


class Params:
    def __init__(self):
        self.is_zipalign = BooleanVar()
        self.is_sign = BooleanVar()
        self.is_multi_pack = BooleanVar()
        self.is_check_sign = BooleanVar()
        self.build_tools_path = StringVar()
        self.pre_apk_path = StringVar()
        self.after_apk_path = StringVar()
        self.app_name = StringVar()
        self.walle_jar_path = StringVar()
        self.channel_txt_path = StringVar()
        self.check_jar_path = StringVar()
        self.keystore_path = StringVar()
        self.password = StringVar()
        current_path = os.getcwd()
        print "current_path:" + current_path
        self.config_path = current_path + "\\config.json"
        config_file = open(self.config_path, 'r')
        try:
            json_str = config_file.read()
            if json_str.strip() == '':
                return
            self.channel_txt_path.set(current_path + "\\channel.txt")
            self.check_jar_path.set(current_path + "\\CheckAndroidV2Signature.jar")
            self.walle_jar_path.set(current_path + "\\walle-cli-all.jar")

            self.config_json = json.loads(json_str)
            self.is_zipalign.set(self.config_json["is_zipalign"])
            self.is_sign.set(self.config_json["is_sign"])
            self.is_check_sign.set(self.config_json["is_check_sign"])
            self.is_multi_pack.set(self.config_json["is_multi_pack"])
            self.build_tools_path.set(self.config_json["build_tools_path"])
            self.pre_apk_path.set(self.config_json["pre_apk_path"])
            self.after_apk_path.set(self.config_json["after_apk_path"])
            self.app_name.set(self.config_json["app_name"])
            self.keystore_path.set(self.config_json["keystore_path"])
            self.password.set(self.config_json["password"])
        finally:
            if config_file:
                config_file.close()


class Funtion:
    def __init__(self, root):
        self.parmas = Params()
        self.gui = GUI(root, self.parmas, self)

    def get_generate_apk(self):
        generate_dir_path = self.parmas.after_apk_path.get() + "\\" + self.parmas.app_name.get()
        if not os.path.exists(generate_dir_path):
            os.mkdir(generate_dir_path)
        return generate_dir_path + "\\" + self.parmas.app_name.get() + ".apk"

    def zipalign(self):
        print self.parmas.pre_apk_path.get()
        if not os.path.exists(self.parmas.pre_apk_path.get()):
            return 2
        generate_apk_path = self.get_generate_apk()
        order = self.parmas.build_tools_path.get() + "\zipalign -v 4 " + self.parmas.pre_apk_path.get() + " " + generate_apk_path
        print "------------------zipaligning-----------------" + order
        p = subprocess.Popen(order, shell=True, stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            # print line
            if line.find("Verification succesful") >= 0:
                return 1
        return 2

    def sign(self):
        generate_apk_path = self.get_generate_apk()
        if os.path.exists(generate_apk_path):
            dest_apk_path = generate_apk_path
        else:
            dest_apk_path = self.parmas.pre_apk_path.get()
        order = self.parmas.build_tools_path.get() + "\\apksigner sign --ks " + self.parmas.keystore_path.get() + " --ks-pass pass:" + self.parmas.password.get() + " --out " + dest_apk_path + " " + dest_apk_path
        print "------------------signing-----------------" + order
        os.system(order)
        return 1

    def check_sign(self):
        generate_apk_path = self.get_generate_apk()
        if not os.path.exists(generate_apk_path):
            generate_apk_path = self.parmas.pre_apk_path.get()
        order = "java -jar " + self.parmas.check_jar_path.get() + " " + generate_apk_path
        print "------------------check_signing-----------------" + order
        p = subprocess.Popen(order, shell=True, stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            print line
            if line.find("{") >= 0:
                try:
                    response = json.loads(line)
                    if (response["ret"] == 0) and response["isV2"] and response["isV2OK"]:
                        if __name__ == '__main__':
                            return 1
                except Exception as e:
                    print e
        return 2

    def multi_pack(self):
        generate_apk_path = self.get_generate_apk()
        if os.path.exists(generate_apk_path):
            dest_apk_path = generate_apk_path
        else:
            dest_apk_path = self.parmas.pre_apk_path.get()
        order = "java -jar " + self.parmas.walle_jar_path.get() + " batch -f " + self.parmas.channel_txt_path.get() + " " + dest_apk_path
        print "------------------multi_packing-----------------" + order
        os.system(order)
        return 1

    def select(self):
        result = 0
        if self.parmas.is_zipalign.get():
            result = self.zipalign()
        if result != 2 and self.parmas.is_sign.get():
            result = self.sign()
        if result != 2 and self.parmas.is_check_sign.get():
            result = self.check_sign()
        if result != 2 and self.parmas.is_multi_pack.get():
            result = self.multi_pack()
        if result == 0:
            tkMessageBox.showerror("Tips", "Please select the option!")
        elif result == 1:
            tkMessageBox.showinfo("Tips", "success")
        elif result == 2:
            tkMessageBox.showerror("Tips", "fail")

    def save(self):
        save_file = open(self.parmas.config_path, 'w')
        try:
            self.parmas.config_json["is_zipalign"] = self.parmas.is_zipalign.get()
            self.parmas.config_json["is_sign"] = self.parmas.is_sign.get()
            self.parmas.config_json["is_check_sign"] = self.parmas.is_check_sign.get()
            self.parmas.config_json["is_multi_pack"] = self.parmas.is_multi_pack.get()
            self.parmas.config_json["build_tools_path"] = self.parmas.build_tools_path.get()
            self.parmas.config_json["pre_apk_path"] = self.parmas.pre_apk_path.get()
            self.parmas.config_json["after_apk_path"] = self.parmas.after_apk_path.get()
            self.parmas.config_json["app_name"] = self.parmas.app_name.get()
            self.parmas.config_json["keystore_path"] = self.parmas.keystore_path.get()
            self.parmas.config_json["password"] = self.parmas.password.get()
            save_file.write(json.dumps(self.parmas.config_json))
            save_file.close()
            tkMessageBox.showinfo("Tip", "Save Success")
        except Exception as e:
            print e
            save_file.close()
            tkMessageBox.showerror("Error", "Save Fail!!!")


window = Tk()
Funtion(window)
window.mainloop()
