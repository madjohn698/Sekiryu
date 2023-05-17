import re, os, xmlrpc.client

from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor


def get_funcs():
    """
    Retrieving functions from the binary
    """
    func = getFirstFunction()
    funcList = []
    nameList = []
    entryList = []
    while func is not None:
        name = ("{}".format(func.getName()))
        entry_point = ("0x{}".format(func.getEntryPoint()))
        func = getFunctionAfter(func)
        nameList.append(str(name))
        entryList.append(str(entry_point))
    names = nameList
    entries = entryList
    return names, entries


def get_namedBlocks():
    """
    Generating block names
    """
    blocks = currentProgram.getMemory().getBlocks()
    nameList = {}
    for block in blocks:
        nameList[block.getName()]=block.getSize()
    proxy.send_block_infos(nameList)

def get_allXREF():    
    """
    Generating XREF from the binary
    """
    func = getFirstFunction()
    xref = []
    while func is not None:
        entry_point = func.getEntryPoint()
        reference = getReferencesTo(entry_point)
        func = getFunctionAfter(func)
        xref.append(reference)
    xrefs = xref
    return xrefs

def cleaning_code(text):
    """
    Cleaning the pseudo-code generated by Ghidra
    """
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    text = re.sub(r'undefined8', '8bytesData', text)
    text = re.sub(r'local_res', 'reservedStack_VAR', text)
    text = re.sub(r'DAT_', 'globalVar', text)
    text = re.sub(r'local_', 'localVar_', text)
    text = re.sub(r'\n(?=\n)', '', text)
    text = re.sub(r'\s{5,}', ' ', text)
    text = re.sub(r'\t+', '', text)
    return text


def get_decomp():
    """
    Generating pseudo code of the functions
    """
    program = getCurrentProgram()
    ifc = DecompInterface()
    ifc.openProgram(program)
    func = getFirstFunction()
    decompiled = {}
    while func is not None:
        function_name = func.getName()
        results = ifc.decompileFunction(func, 0, ConsoleTaskMonitor())
        decompiled[function_name] = cleaning_code(str(results.getDecompiledFunction().getC()))
        func = getFunctionAfter(func)
    proxy.send_decomp(decompiled)

proxy = xmlrpc.client.ServerProxy('http://localhost:13337')
get_decomp()
get_namedBlocks()