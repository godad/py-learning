# -*- coding: utf-8 -*-
# @Time    : 2018/3/16 16:16
# @Author  : flyfish
# @Email   : im@flyfish.im

name = input("Name:")
age = int(input("Age:"))
job = input("Job:")
salary = int(input("Salary:"))

msg = '''
---------------info of %s ----------------
Name   : %s
Age    : %d
Job    : %s
Salary : %d
You will be retired in %d years
-----------------  end  ------------------
''' % (name,name,age,job,salary,65-age)

print(msg)