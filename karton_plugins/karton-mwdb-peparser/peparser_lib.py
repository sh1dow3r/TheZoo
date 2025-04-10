# peparser_lib.py

import pefile
import json

def parse_pe_file(path):
    try:
        pe = pefile.PE(path)
    except pefile.PEFormatError:
        return {"error": "File is not a PE"}

    def imports(pe):
        imports = []
        if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
            for dll in pe.DIRECTORY_ENTRY_IMPORT:
                importsD = {'name': dll.dll.decode(), 'functions': []}
                for imp in dll.imports:
                    importsD['functions'].append(
                        imp.name.decode() if imp.name else f"Ordinal: {imp.ordinal}")
                imports.append(importsD)
        return imports

    def exports(pe):
        export_list = []
        if hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
            for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
                export_list.append(exp.name.decode() if exp.name else "Unnamed Export")
        return export_list or ['no exports']

    def hashes(pe):
        return {"imphash": pe.get_imphash()}

    def sections(pe):
        section_list = []
        for section in pe.sections:
            section_list.append({
                'Name': section.Name.decode(errors="ignore").strip('\x00'),
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

    return {
        "Size": pe.OPTIONAL_HEADER.SizeOfImage,
        "Hashes": hashes(pe),
        "DOS Header": dos_header(pe),
        "File Header": file_header(pe),
        "Optional Header": optional_header(pe),
        "Sections": sections(pe),
        "Imports": imports(pe),
        "Exports": exports(pe)
    }
