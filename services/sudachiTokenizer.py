from typing import Dict, List, Union

from sudachipy import dictionary, tokenizer


class MorphologicalAnalysis:
    def tokenize_and_process(
        self, sentence: str
    ) -> Dict[str, Union[bool, str, List[str]]]:
        try:
            # Initialize the tokenizer
            tokenizer_obj = dictionary.Dictionary(dict_type="full").create()

            # Tokenize in Mode A for most detailed segmentation
            tokens = tokenizer_obj.tokenize(sentence, tokenizer.Tokenizer.SplitMode.A)
            words = []
            for token in tokens:
                word = token.dictionary_form()
                pos = token.part_of_speech()
                parts_of_speech = pos[0]
                if "助詞" not in parts_of_speech:
                    if pos[5] and pos[5] != "連体形-一般":
                        words.append(word)
                    else:
                        words.append(word)

            return {"success": True, "message": "", "words": words}

        except Exception as e:
            return {"success": False, "message": str(e), "words": []}
