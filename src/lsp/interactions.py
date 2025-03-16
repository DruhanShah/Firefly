"""
This is a CLI script to play around with LSP predictions
"""

import argparse
import asyncio
import pathlib
import json
import re

import multilspy
import multilspy.multilspy_types as types

def setup_multilspy(src_dir, code_language=multilspy.multilspy_config.Language.PYTHON):
    # Assume that we are using Python, can get it to work for others as well
    config = multilspy.multilspy_config.MultilspyConfig.from_dict({
        "code_language": code_language,
    })
    logger = multilspy.multilspy_logger.MultilspyLogger()
    lsp = multilspy.SyncLanguageServer.create(config, logger, str(src_dir))
    return lsp


def get_symbol_code(lsp, symbol):
    file_path = multilspy.multilspy_utils.PathUtils.uri_to_path(symbol['location']['uri'])
    definition = lsp.request_definition(file_path, file_symbol['location']['range']['start']['line'], file_symbol['location']['range']['start']['character'])
    match definition:
        case []:
            return None
        case [x]:
            definition = x
        case _:
            print(definition)
            raise ValueError("Multiple defitions found!")

    doc_symbols = get_server_doc_symbol(lsp, definition['relativePath'])

    # copy code from file and send it over
    file_content = None
    with open(definition['absolutePath'], 'r') as f:
        file_content = f.readlines()

    
    real_symbol = traverse_doc_symbols(doc_symbols, file_symbol)
    symbol_lines = file_content[real_symbol["range"]["start"]["line"]:real_symbol["range"]["end"]["line"] + 1]

    return symbol_lines
    
def get_code(file_path: str, symbol_name: str, root_dir: str):
    lsp = setup_multilspy(root_dir)

    with lsp.start_server():
        symbols = get_server_symbols(lsp, args.symbol_name)
        if symbols is None or symbols == []:
            raise ValueError("invalid symbol name received! please try again")

        return [get_code(lsp, symbol) for symbol in symbols]

def get_server_symbols(lsp: multilspy.SyncLanguageServer, symbol_name: str):
    response = asyncio.run_coroutine_threadsafe(
        lsp.language_server.server.send.workspace_symbol({
            "query": symbol_name
        }), lsp.loop).result(timeout=lsp.timeout)
    return response

def get_server_doc_symbol(lsp: multilspy.SyncLanguageServer, text_document: str):
    response = asyncio.run_coroutine_threadsafe(
        lsp.language_server.server.send.document_symbol({
            "textDocument": {
                "uri": text_document,
            }
        }), lsp.loop).result(timeout=lsp.timeout)
    return response


def traverse_doc_symbols(doc_symbols, search_symbol):
    target_name = search_symbol["name"] if 'name' in search_symbol else ''
    target_range = search_symbol["location"]["range"]
    
    for symbol in doc_symbols:
        # checks:
        #        name of both is the same
        #        line number of search symbol is in doc symbol
        #        col number is included
        if target_name == '' or symbol["name"] == target_name:
            selection_range = symbol["selectionRange"]
            
            # Compare start and end positions explicitly
            if (selection_range["start"]["line"] == target_range["start"]["line"] and
                selection_range["start"]["character"] == target_range["start"]["character"] and
                selection_range["end"]["line"] == target_range["end"]["line"] and
                selection_range["end"]["character"] == target_range["end"]["character"]):
                return symbol  # Found the matching entry
        
        if symbol['children'] != []:
            output_symbol = traverse_doc_symbols(symbol['children'], search_symbol)
            if output_symbol is not None:
                return output_symbol

    return None
            

def parse_line_col_range(text):
    match = re.match(r'(\d+):(\d+)', text)
    if match:
        line, col = map(int, match.groups())
        return {
            "line": line,
            "col": col,
        }
    else:
        raise ValueError("Invalid format")

parser = argparse.ArgumentParser()
parser.add_argument(
    "--src-file",
    dest='src_file',
    required=True,
    help="Source file for codebase",
    type=pathlib.Path
)
parser.add_argument(
    "--symbol-name",
    dest='symbol_name',
    required=True,
    help="Symbol name to search for",
    type=str
)

args = parser.parse_args()

src_dir = args.src_file.parent.absolute()

# Assume that we are using Python, can get it to work for others as well
code_language = multilspy.multilspy_config.Language.PYTHON

config = multilspy.multilspy_config.MultilspyConfig.from_dict({
    "code_language": code_language,
})

logger = multilspy.multilspy_logger.MultilspyLogger()

lsp = multilspy.SyncLanguageServer.create(config, logger, str(src_dir))

with lsp.start_server():
    # TODO: figure out what does the tree do
    symbols = get_server_symbols(lsp, args.symbol_name)
    # TODO: write code to get one of multiple symbols
    print(symbols)
    match symbols:
        case [] | None:
            raise ValueError("No symbols found!")
        case [x]:
            file_symbol = x
        case _:
            print(symbols)
            raise ValueError("Multiple symbols found!")

    file_path = multilspy.multilspy_utils.PathUtils.uri_to_path(file_symbol['location']['uri'])

    definition = lsp.request_definition(file_path, file_symbol['location']['range']['start']['line'], file_symbol['location']['range']['start']['character'])
    match definition:
        case []:
            raise ValueError("No definitions found!")
        case [x]:
            definition = x
        case _:
            print(definition)
            raise ValueError("Multiple defitions found!")
        
    doc_symbols = get_server_doc_symbol(lsp, definition['relativePath'])
    print("Doc symbol: ", doc_symbols)

    # copy code from file and send it over
    file_content = None
    with open(definition['absolutePath'], 'r') as f:
        file_content = f.readlines()

    real_symbol = traverse_doc_symbols(doc_symbols, file_symbol)
    symbol_lines = file_content[real_symbol["range"]["start"]["line"]:real_symbol["range"]["end"]["line"] + 1]

    current_context = [{
        "location": real_symbol,
        "code": symbol_lines,
        "file_name": file_path
    }]

    print("Enter break to break")
    while True:
        while current_context != []:
            curr = current_context[-1]
            print(curr)
            print(''.join([f"{idx}:{code}" for idx, code in enumerate(curr['code'])]))
            range_in = input("Enter range (line:col format): ")
            if range_in == 'pop':
                current_context.pop()
            else:
                break

        if range_in == 'break':
            break
        range_in = parse_line_col_range(range_in)
        line, col = range_in['line'], range_in['col']

        final_line = curr['location']['range']['start']['line'] + line
        assert final_line <= curr['location']["range"]["end"]["line"]

        locations = lsp.request_definition(curr['file_name'], final_line, col)

        match locations:
            case []:
                raise ValueError("No definitions found!")
            case [x]:
                chosen_location = x
            case _:
                print("Locations: ", locations)
                idx = int(input("Enter index: "))
                chosen_location = locations[idx]
                raise ValueError("Multiple locations found!")

        doc_symbols = get_server_doc_symbol(lsp, chosen_location['relativePath'])
        search_symbol = {
            "location": chosen_location
        }

        definition = lsp.request_definition(chosen_location['relativePath'], chosen_location['range']['start']['line'], chosen_location['range']['start']['character'])
        match definition:
            case []:
                raise ValueError("No definitions found!")
            case [x]:
                definition = x
            case _:
                raise ValueError("Multiple defitions found!")

        # TODO: Use definition for something useful
        
        real_symbol = traverse_doc_symbols(doc_symbols, search_symbol)
        print(real_symbol)
        file_content = []
        with open(chosen_location['absolutePath'], 'r') as f:
            file_content = f.readlines()

        symbol_lines = file_content[real_symbol['range']['start']['line']:real_symbol['range']['end']['line'] + 1]
        print(f"Symbol lines: {symbol_lines}")
        current_context.append({
            "location": real_symbol,
            "code": symbol_lines,
            "file_name": chosen_location['relativePath']
        })
