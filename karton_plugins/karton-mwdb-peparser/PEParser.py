# import pereader
# import sys
# import json


# PEInput=sys.argv[1]


# def imports(pe):
#  imports=[]
#  for dll in pe.directory_entry_import.dlls:
#   importsD={}
#   importsD['name']=dll.name
#   #print(dll.name)
#   importsD['funtions']=[]
#   for imp in dll:
#    importsD['funtions'].append(imp.name)
#    #print(" ",hex(imp.address), imp.name)
#   imports.append(importsD)
#  return imports

   
# def exports(pe):
#  exportlist=[]
#  try:
#   for exp in pe.directory_entry_export.symbols:
#    #print(hex(exp.address), exp.name, exp.ordinal)
#    exportlist.append(exp.name)
#  except:
#   exportlist.append('no exports')
#   #print("no exports")
#  return exportlist
  


# def filename(pe):
#  #print(pe.fname)
#  return pe.fname
 
# def hashes(pe):
#  return pe.hashes


 
# def size(pe):
#  return pe.pe_size
 
 
# def versionInfo(pe):
#  #print(pe.directory_entry_resource.resource_directory.str_TimeDateStamp)
#  #print(pe.directory_entry_resource.is_directory)
#  #print(pe)
#  vi={}
#  try:
#   for entry in pe.directory_entry_resource.resource_directory.entries:
#    #print(entry.RESOURCE_DIRECTORY_ENTRY.__dict__)
#    try:
#     if entry.RESOURCE_DIRECTORY_ENTRY.str_Type == 'RT_VERSION':
#      #print(entry.__dict__)
#      version = entry.version
#      for e in version.stringfileinfo:
#       for stringtable in e.stringtables:
#        for string in stringtable.strings:
#         #print("a")
#         vi[string.str_szKey]=string.str_Value		
# 		#print(string.str_szKey, string.str_Value)
#      for e in version.varfileinfo:
#       for var in e.vars:
#        for w1, w2 in var.translations:
#         vi[w1]=w2
#         #print("before")
#         #print(w1, w2)
#    except:
#     pass
#  except:
#   #print("no-info")
#   vi['version info']="no version info"
#  return vi
 
# def strings(pe):
#  for entry in pe.directory_entry_resource.resource_directory.entries:
#   if entry.RESOURCE_DIRECTORY_ENTRY.str_Type == 'RT_STRING':
#    for k in entry.strings:
#     print(k, entry.strings[k])
 
 

 
# # --------------- nt FILE HEADER stuff --------------- #
# def FHSignature(pe):
#  hex_string=str(hex(pe.NT_HEADERS.Signature))[2:]
#  bytes_object=bytes.fromhex(hex_string)
#  ascii_str=bytes_object.decode("ASCII")
#  return ascii_str[::-1]

# def FHMachine(pe):
#  return pe.__MACHINE__[pe.FILE_HEADER.Machine]
 
# def FHNumberOfSections(pe):
#  return pe.FILE_HEADER.NumberOfSections

# def FHTimeDateStamp(pe):
#  return pe.FILE_HEADER.str_TimeDateStamp

# def FHCharcteristics(pe):
#  return pe.FILE_HEADER.flags

# # --------------- nt Section Header --------------- #
# def sections(pe):
#  sectionList=[]
#  for se in pe.section_header:
#   sections={}
#   sections['Name']=se.str_Name
#   sections['Entropy']='{:.3f}'.format(se.flt_Entropy)
#   sections['Characteristics']=se.flags
#   sectionList.append(sections)
#  #print(se.str_Name,se.flags)
#  #print(sectionList)
#  #return sections
#  return sectionList

# # ----------------DOS header stuff---------------- # 
# def DOSSignature(pe):
#  hex_string=str(hex(pe.DOS_HEADER.e_magic))[2:]
#  bytes_object=bytes.fromhex(hex_string)
#  ascii_str=bytes_object.decode("ASCII")
#  #print(ascii_str[::-1])
#  #return str(hex(pe.DOS_HEADER.e_magic))
#  return ascii_str[::-1]
 
# def DOSlfanew(pe):
#  return str(hex(pe.DOS_HEADER.e_lfanew))

#  # ----------------NT optional header ---------------- #
# def OHMagic(pe):
#  return hex(pe.OPTIONAL_HEADER.Magic)

# def OHImageBase(pe):
#  return str(hex(pe.OPTIONAL_HEADER.ImageBase))
 
# def OHSectionAlignment(pe):
#  return str(hex(pe.OPTIONAL_HEADER.SectionAlignment))
 
# def OHFileAlignment(pe):
#  return str(hex(pe.OPTIONAL_HEADER.FileAlignment))
 
# def OHSubsystem(pe):
#  return pe.OPTIONAL_HEADER.Subsystem

# def OHEntryPoint(pe):
#  return str(hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint))

# def OHSizeOfImage(pe):
#  return str(hex(pe.OPTIONAL_HEADER.SizeOfImage))

# def OHDLLcharacteristics(pe):
#  return pe.OPTIONAL_HEADER.flags
 
# def OHMajorOperatingSystemVersion(pe):
#  return pe.OPTIONAL_HEADER.MajorOperatingSystemVersion
 
# def  warnings(pe):
#  return pe.warnings

# def createJSON(PEObject):
#   PEJSON={}
#   PEJSON['File Name']=filename(PEObject)
#   PEJSON['Size']=size(PEObject)
#   PEJSON['Hashes']=hashes(PEObject)
#   PEJSON['Warnings']=warnings(PEObject)
#   PEJSON['DOS Header Signature']=DOSSignature(PEObject)
#   PEJSON['DOS Header e_lfanew']=DOSlfanew(PEObject)
#   PEJSON['File Header Signature']=FHSignature(PEObject)
#   PEJSON['File Header Machine']=FHMachine(PEObject)
#   PEJSON['File Header Number Of Sections']=FHNumberOfSections(PEObject)
#   PEJSON['File Header Time Date Stamp']=FHTimeDateStamp(PEObject)
#   PEJSON['File Header Characteristics']=FHCharcteristics(PEObject)
#   PEJSON['Optional Header Magic']=OHMagic(PEObject)
#   PEJSON['Optional Header Image Base']=OHImageBase(PEObject)
#   PEJSON['Optional Header Section Alignment']=OHSectionAlignment(PEObject)
#   PEJSON['Optional Header File Alignment']=OHFileAlignment(PEObject)
#   PEJSON['Optional Header Subsystem']=OHSubsystem(PEObject)
#   PEJSON['Optional Header Entry Point']=OHEntryPoint(PEObject)
#   PEJSON['Optional Header DLL characteristics']=OHDLLcharacteristics(PEObject)
#   PEJSON['Sections']=sections(PEObject)
#   PEJSON['VERSION INFO']=versionInfo(PEObject)
#   PEJSON['Imports']=imports(PEObject)
#   PEJSON['Exports']=exports(PEObject)
#   return json.dumps(PEJSON, indent=4)

# f=open(PEInput, 'rb')
# if f.read(2) == b'MZ':
#   tempPE=pereader.PE(PEInput)
#   print(createJSON(tempPE))

# else:
#   print("File is not a PE")

# f.close()  



import pefile
import sys
import json

PEInput = sys.argv[1]

def imports(pe):
    imports = []
    if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
        for dll in pe.DIRECTORY_ENTRY_IMPORT:
            importsD = {'name': dll.dll.decode(), 'functions': []}
            for imp in dll.imports:
                importsD['functions'].append(imp.name.decode() if imp.name else "Ordinal: " + str(imp.ordinal))
            imports.append(importsD)
    return imports

def exports(pe):
    export_list = []
    if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
        for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
            export_list.append(exp.name.decode() if exp.name else "Unnamed Export")
    return export_list if export_list else ['no exports']

def filename():
    return PEInput

def hashes(pe):
    return {
        "MD5": pe.get_imphash(),
    }

def size(pe):
    return pe.OPTIONAL_HEADER.SizeOfImage

def sections(pe):
    section_list = []
    for section in pe.sections:
        section_list.append({
            'Name': section.Name.decode().strip('\x00'),
            'Entropy': '{:.3f}'.format(section.get_entropy()),
            'Characteristics': hex(section.Characteristics)
        })
    return section_list

def optional_header(pe):
    return {
        "Magic": hex(pe.OPTIONAL_HEADER.Magic),
        "ImageBase": hex(pe.OPTIONAL_HEADER.ImageBase),
        "SectionAlignment": hex(pe.OPTIONAL_HEADER.SectionAlignment),
        "FileAlignment": hex(pe.OPTIONAL_HEADER.FileAlignment),
        "Subsystem": pe.OPTIONAL_HEADER.Subsystem,
        "EntryPoint": hex(pe.OPTIONAL_HEADER.AddressOfEntryPoint),
        "SizeOfImage": hex(pe.OPTIONAL_HEADER.SizeOfImage),
    }

def file_header(pe):
    return {
        "Machine": hex(pe.FILE_HEADER.Machine),
        "NumberOfSections": pe.FILE_HEADER.NumberOfSections,
        "TimeDateStamp": pe.FILE_HEADER.TimeDateStamp,
        "Characteristics": hex(pe.FILE_HEADER.Characteristics),
    }

def dos_header(pe):
    return {
        "e_magic": hex(pe.DOS_HEADER.e_magic),
        "e_lfanew": hex(pe.DOS_HEADER.e_lfanew)
    }

def create_json(pe):
    pe_json = {
        "File Name": filename(),
        "Size": size(pe),
        "Hashes": hashes(pe),
        "DOS Header": dos_header(pe),
        "File Header": file_header(pe),
        "Optional Header": optional_header(pe),
        "Sections": sections(pe),
        "Imports": imports(pe),
        "Exports": exports(pe)
    }
    return json.dumps(pe_json, indent=4)

# Open and process the file
with open(PEInput, 'rb') as f:
    pe = pefile.PE(PEInput)
    print(create_json(pe))
