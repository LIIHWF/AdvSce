

import json
import re


def for_printing(properties):
    ret = dict()
    for p in properties.keys():
        s = str(properties[p])
        if p[-1] == '_':
            s = s.replace('\n', '')
            if len(s) >= 10:
                s = f'{s[:5]}...{s[-5:]}'
        ret[p] = s
    return ret

def remove_brackets(t):
    tt = t.group()
    return f'{tt[1:-2]}:'

def for_neo4j(_id, properties):
    p = properties.copy()
    p['name'] = _id
    del p['type']
    return re.sub(r'"\w+":', remove_brackets, json.dumps(p))


def where_condition(name):
    def f(t):
        tt = t.group()
        return f' AND {name}.{tt[3:-2]} ='
    return f


def for_where_condition(name, properties):
    p = properties.copy()
    ret = re.sub(r', "\w+":', where_condition(name), f'{{, {json.dumps(p)[1:]}')
    return ret.replace(' = [', ' IN [')[6:-1]
