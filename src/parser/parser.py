from tree_sitter import Language, Parser

from multilspy import SyncLanguageServer
from multilspy.multilspy_config import MultilspyConfig
from multilspy.multilspy_logger import MultilspyLogger


class ParseTool():

    def __init__(self, language, path_to_root):
        config = MultilspyConfig.from_dict({"code_language": language})
        logger = MultilspyLogger()
        lsp = SyncLanguageServer.create(config, logger, path_to_root)

        ts_language = Language(language)
        ts_parser = Parser(ts_language)

    def find_definition(file, location)
        with lsp.start_server():
            result = lsp.request_definition(file, *location)
        
