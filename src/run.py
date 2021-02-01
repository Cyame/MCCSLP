import hjson
import csv
import pulp

import os
import sys
import time
import itertools
import logging
import traceback

from auth import *
from env import *

logging.getLogger().setLevel(logging.DEBUG)
#logging.getLogger().setLevel(logging.INFO)

CONSTRAINT_PATH = os.path.join(getPath(), 'config', 'constraints.hjson')
MINERAL_PATH = os.path.join(getPath(), 'config', 'mineral.csv')
AUTHCODE_PATH = os.path.join(getPath(), 'config', 'authcode.txt')
WORKLOAD_PATH = os.path.join(getPath(), 'workload')

def read_constr(path=CONSTRAINT_PATH):
    constr = {}
    with open(path, 'r', encoding='utf-8') as conf:
        constr = hjson.load(conf)
        # S for string
    for conf in list(constr.items()):

        if conf[1] == -1:
            constr.pop(conf[0])

    conrange = {}
    for key, val in constr.items():
        if "Std" in key:
            conrange[key[4:]] = [val]
        elif 'Rls' in key:
            conrange[key[4:]].append(val)
        else:
            conrange[key] = val
    for key, val in conrange.items():
        # upper,lower
        if key != 'main_quantity':
            val[0] += val[1]
            val[1] = val[0] - 2 * val[1]
            round(val[0], 2)
            round(val[1], 2)
    return conrange


def read_mineral(path=MINERAL_PATH):
    data = []

    with open(path, 'r', encoding='gb2312') as form:
        datasource = csv.reader(form)
        header = []
        for d in datasource:
            if d[0] == 'Type':
                header.extend(d)
            else:
                for i in range(len(d)):
                    if i >= 2:
                        if d[i] == '':
                            d[i] = 0
                        else:
                            d[i] = float(d[i])
                data.append(d)
    for mine in data:
        for content_index in range(2, len(mine) - 3):
            mine[content_index] = mine[content_index] / (
                1 - mine[len(mine) - 3] / 100)
    main_mineral = []
    const_content = {}
    for mine in data:
        if mine[0] == 'M':
            main_mineral.append(mine[1:])
        else:
            const_content[mine[0]] = mine[1:]

    return main_mineral, const_content


def execute(conrange,main_mineral,const_content):
    if conrange['main_quantity'] <= 6:
        # CODING
        index = 0
        Result = []
        for p in itertools.combinations(main_mineral, conrange['main_quantity']):
            Result.append({'NO': index, 'MAINS': [m[0] for m in p]})
            content = ['H', 'C', 'Z', 'A1', 'A2', 'J', 'B']
            TFe = {
                'H': const_content['H'][1],
                'C': const_content['C'][1],
                'Z': const_content['Z'][1],
                'A1': const_content['A1'][1],
                'A2': const_content['A2'][1],
                'J': const_content['J'][1],
                'B': const_content['B'][1]
            }
            SiO2 = {
                'H': const_content['H'][2],
                'C': const_content['C'][2],
                'Z': const_content['Z'][2],
                'A1': const_content['A1'][2],
                'A2': const_content['A2'][2],
                'J': const_content['J'][2],
                'B': const_content['B'][2]
            }
            Al2O3 = {
                'H': const_content['H'][3],
                'C': const_content['C'][3],
                'Z': const_content['Z'][3],
                'A1': const_content['A1'][3],
                'A2': const_content['A2'][3],
                'J': const_content['J'][3],
                'B': const_content['B'][3]
            }
            CaO = {
                'H': const_content['H'][4],
                'C': const_content['C'][4],
                'Z': const_content['Z'][4],
                'A1': const_content['A1'][4],
                'A2': const_content['A2'][4],
                'J': const_content['J'][4],
                'B': const_content['B'][4]
            }
            MgO = {
                'H': const_content['H'][5],
                'C': const_content['C'][5],
                'Z': const_content['Z'][5],
                'A1': const_content['A1'][5],
                'A2': const_content['A2'][5],
                'J': const_content['J'][5],
                'B': const_content['B'][5]
            }
            S = {
                'H': const_content['H'][6],
                'C': const_content['C'][6],
                'Z': const_content['Z'][6],
                'A1': const_content['A1'][6],
                'A2': const_content['A2'][6],
                'J': const_content['J'][6],
                'B': const_content['B'][6]
            }
            P = {
                'H': const_content['H'][7],
                'C': const_content['C'][7],
                'Z': const_content['Z'][7],
                'A1': const_content['A1'][7],
                'A2': const_content['A2'][7],
                'J': const_content['J'][7],
                'B': const_content['B'][7]
            }
            FeO = {
                'H': const_content['H'][8],
                'C': const_content['C'][8],
                'Z': const_content['Z'][8],
                'A1': const_content['A1'][8],
                'A2': const_content['A2'][8],
                'J': const_content['J'][8],
                'B': const_content['B'][8]
            }
            ZnO = {
                'H': const_content['H'][9],
                'C': const_content['C'][9],
                'Z': const_content['Z'][9],
                'A1': const_content['A1'][9],
                'A2': const_content['A2'][9],
                'J': const_content['J'][9],
                'B': const_content['B'][9]
            }
            K2O = {
                'H': const_content['H'][10],
                'C': const_content['C'][10],
                'Z': const_content['Z'][10],
                'A1': const_content['A1'][10],
                'A2': const_content['A2'][10],
                'J': const_content['J'][10],
                'B': const_content['B'][10]
            }
            cost = {
                'H': const_content['H'][-1],
                'C': const_content['C'][-1],
                'Z': const_content['Z'][-1],
                'A1': const_content['A1'][-1],
                'A2': const_content['A2'][-1],
                'J': const_content['J'][-1],
                'B': const_content['B'][-1]
            }

            for i in range(conrange['main_quantity']):
                content.append(f'M{i}')
                TFe[f"M{i}"] = p[i][1]
                SiO2[f"M{i}"] = p[i][2]
                Al2O3[f"M{i}"] = p[i][3]
                CaO[f"M{i}"] = p[i][4]
                MgO[f"M{i}"] = p[i][5]
                S[f"M{i}"] = p[i][6]
                P[f"M{i}"] = p[i][7]
                FeO[f"M{i}"] = p[i][8]
                ZnO[f"M{i}"] = p[i][9]
                K2O[f"M{i}"] = p[i][10]
                cost[f"M{i}"] = p[i][-1]
            recipe = pulp.LpProblem("The mineral collocation problem",
                                    pulp.LpMinimize)
            # VAR
            ingredient_vars = pulp.LpVariable.dicts("Ingr", content, 0, 1)
            # OBJ
            recipe += pulp.lpSum(cost[i] * ingredient_vars[i] for i in content)
            # CONS
            if "TFe" in conrange.keys():
                recipe += pulp.lpSum(
                    TFe[i] * ingredient_vars[i]
                    for i in content) <= conrange["TFe"][0], "TFe-upper"
                recipe += pulp.lpSum(
                    TFe[i] * ingredient_vars[i]
                    for i in content) >= conrange["TFe"][1], "TFe-lower"
            if "SiO2" in conrange.keys():
                recipe += pulp.lpSum(
                    SiO2[i] * ingredient_vars[i]
                    for i in content) <= conrange["SiO2"][0], "SiO2-upper"
                recipe += pulp.lpSum(
                    SiO2[i] * ingredient_vars[i]
                    for i in content) >= conrange["SiO2"][1], "SiO2-lower"
            if "Al2O3" in conrange.keys():
                recipe += pulp.lpSum(
                    Al2O3[i] * ingredient_vars[i]
                    for i in content) <= conrange["Al2O3"][0], "Al2O3-upper"
                recipe += pulp.lpSum(
                    Al2O3[i] * ingredient_vars[i]
                    for i in content) >= conrange["Al2O3"][1], "Al2O3-lower"
            if "CaO" in conrange.keys():
                recipe += pulp.lpSum(
                    CaO[i] * ingredient_vars[i]
                    for i in content) <= conrange["CaO"][0], "CaO-upper"
                recipe += pulp.lpSum(
                    CaO[i] * ingredient_vars[i]
                    for i in content) >= conrange["CaO"][1], "CaO-lower"
            if "MgO" in conrange.keys():
                recipe += pulp.lpSum(
                    MgO[i] * ingredient_vars[i]
                    for i in content) <= conrange["MgO"][0], "MgO-upper"
                recipe += pulp.lpSum(
                    MgO[i] * ingredient_vars[i]
                    for i in content) >= conrange["MgO"][1], "MgO-lower"
            if "S" in conrange.keys():
                recipe += pulp.lpSum(
                    S[i] * ingredient_vars[i]
                    for i in content) <= conrange["S"][0], "S-upper"
                recipe += pulp.lpSum(
                    S[i] * ingredient_vars[i]
                    for i in content) >= conrange["S"][1], "S-lower"
            if "P" in conrange.keys():
                recipe += pulp.lpSum(
                    P[i] * ingredient_vars[i]
                    for i in content) <= conrange["P"][0], "P-upper"
                recipe += pulp.lpSum(
                    P[i] * ingredient_vars[i]
                    for i in content) >= conrange["P"][1], "P-lower"
            if "FeO" in conrange.keys():
                recipe += pulp.lpSum(
                    FeO[i] * ingredient_vars[i]
                    for i in content) <= conrange["FeO"][0], "FeO-upper"
                recipe += pulp.lpSum(
                    FeO[i] * ingredient_vars[i]
                    for i in content) >= conrange["FeO"][1], "FeO-lower"
            if "ZnO" in conrange.keys():
                recipe += pulp.lpSum(
                    ZnO[i] * ingredient_vars[i]
                    for i in content) <= conrange["ZnO"][0], "ZnO-upper"
                recipe += pulp.lpSum(
                    ZnO[i] * ingredient_vars[i]
                    for i in content) >= conrange["ZnO"][1], "ZnO-lower"
            if "CaOSiO2" in conrange.keys():
                recipe += pulp.lpSum(
                    CaO[i] * ingredient_vars[i] for i in content) / (
                        pulp.lpSum(SiO2[i] * ingredient_vars[i]
                                   for i in content) <=
                        conrange["CaOSiO2_ratio"][0]), "CaOSiO2_ratio-upper"
                recipe += pulp.lpSum(
                    CaO[i] * ingredient_vars[i] for i in content) / (
                        pulp.lpSum(SiO2[i] * ingredient_vars[i]
                                   for i in content) >=
                        conrange["CaOSiO2_ratio"][1]), "CaOSiO2_ratio-lower"

            if "main_ratio" in conrange.keys():
                recipe += pulp.lpSum(
                    ingredient_vars[i] for i in content if 'M' in
                    i) <= conrange['main_ratio'][0], "main_ratio-upper"
                recipe += pulp.lpSum(
                    ingredient_vars[i] for i in content if 'M' in
                    i) >= conrange['main_ratio'][1], "main_ratio-lower"

            recipe += pulp.lpSum(
                ingredient_vars[i] for i in content
                if ('M' in i or 'H' in i or 'C' in i or 'Z' in i)) == 100

            recipe.writeMPS(os.path.join(WORKLOAD_PATH,'MPS',
                f"MODEL-{index}-({time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())}).mps")
                    )
            recipe.writeLP(os.path.join(WORKLOAD_PATH,'LP',
                f"MODEL-{index}-({time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())}).lp")
                    )
            
            recipe.solve()
            Result[index]["STATUS"] = pulp.LpStatus[recipe.status]
            Result[index]["RESULT"] = {}
            for v in recipe.variables():
                Result[index]["RESULT"][v.name] = v.varValue
            index += 1

        with open(
                os.path.join(WORKLOAD_PATH,f"RESULT({time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())}).txt"),
                'w',
                encoding='utf8') as output_file:
            for plan in Result:
                output_file.write("\n============================\n")
                output_file.write(f"报告编号：{plan['NO']}\n")
                output_file.write(f"使用主矿：{plan['MAINS']}\n")
                if plan["STATUS"] == "Infeasible":
                    output_file.write("运行结果：无可行解\n")
                elif plan["STATUS"] == "Not Solved":
                    output_file.write("运行结果：不可解\n")
                elif plan["STATUS"] == "Optimal":
                    output_file.write("运行结果：最优解\n")
                elif plan["STATUS"] == "Unbounded":
                    output_file.write("运行结果：命题不收敛\n")
                elif plan["STATUS"] == "Undefined":
                    output_file.write("运行结果：命题未定义\n")
                else:
                    output_file.write("运行结果：未知\n")
                    output_file.write("计算时可能发生严重错误，请联系开发者进行处理\n")

                if plan["RESULT"] != None:
                    output_file.write("\n=========配矿结果=========\n\n")
                    output_file.write("\n##主矿配比##\n")
                    for i in range(conrange['main_quantity']):
                        output_file.write(
                            f"主矿-{plan['MAINS'][i]}: {plan['RESULT'][f'Ingr_M{i}']}\n"
                        )

                        output_file.write("\n##其他成分##\n")
                        # H
                        output_file.write(
                            f"{const_content['H'][0]}: {plan['RESULT']['Ingr_H']}\n"
                        )
                        # C
                        output_file.write(
                            f"{const_content['C'][0]}: {plan['RESULT']['Ingr_C']}\n"
                        )
                        # Z
                        output_file.write(
                            f"{const_content['Z'][0]}: {plan['RESULT']['Ingr_Z']}\n"
                        )
                        # A1
                        output_file.write(
                            f"{const_content['A1'][0]}: {plan['RESULT']['Ingr_A1']}\n"
                        )
                        # A2
                        output_file.write(
                            f"{const_content['A2'][0]}: {plan['RESULT']['Ingr_A2']}\n"
                        )
                        # JS
                        output_file.write(
                            f"{const_content['J'][0]}: {plan['RESULT']['Ingr_J']}\n"
                        )
                        # B
                        output_file.write(
                            f"{const_content['B'][0]}: {plan['RESULT']['Ingr_B']}\n"
                        )
                        output_file.write("\n##综合参数##\n")
                else:
                    output_file.write("=========解集为空=========\n")
    else:
        raise ImportError("选定主矿个数不受支持。")


def authrize(code):
    with open(AUTHCODE_PATH,'r',encoding='utf8') as c:
        if generatePSW(str(c)) == code:
            return True
        else:
            return False


def run():
    try:
        constraint = read_constr()
        logging.debug("CONSTRAINT = " + str(constraint))
        main_mineral, const_content = read_mineral()
        logging.debug("main_mineral = " + str(main_mineral))
        logging.debug("const_content = " + str(const_content))
    except Exception as e:
        traceback.print_exc()
        logging.fatal("IMPORT FATAL")
        print(e)
    try:
        execute(constraint, main_mineral, const_content)
    except Exception as e:
        traceback.print_exc()
        logging.fatal("EXEC FATAL")
        print(e)
    pass

if __name__ == "__main__":
    run()
    # if authrize(sys.argv[1]) or sys.argv[1] == 'admin':
    #     run()
    # else:
    #     raise AssertionError("验证口令错误，请联系管理员处理")
    pass