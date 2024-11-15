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
            targeted_pos = ["名詞", "動詞", "形容詞", "副詞"]
            for token in tokens:
                word = token.dictionary_form()
                pos = token.part_of_speech()
                parts_of_speech = pos[0]
                if parts_of_speech in targeted_pos:
                    if pos[5] and "連体形-一般" not in pos[5]:
                        words.append(word)

            return {"success": True, "message": "", "words": words}

        except Exception as e:
            return {"success": False, "message": str(e), "words": []}


# m = MorphologicalAnalysis()
# morphos = m.tokenize_and_process(
#     "今日は雨が降っているので、会社へ行きません。家で寝ます。"
# )
# print(morphos)
