from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort

from services.jishoDictionaryApi import JishoService
from services.sudachiTokenizer import MorphologicalAnalysis

blp = Blueprint("morphoAnalysis", __name__, description="Morphological Operations")


@blp.route("/morpho_analysis/<string:sentence>")
class MorphoAnalysis(MethodView):
    def get(self, sentence):
        try:
            tokenizer = MorphologicalAnalysis()
            morphos = tokenizer.tokenize_and_process(sentence)
            print(morphos)
            if not morphos["success"]:
                raise Exception(
                    f"Error while analyzing the sentence {morphos['message']}"
                )
            res = []
            words = morphos["words"]
            for word in words:
                print("in")
                dictionary = JishoService()
                word_information = dictionary.getWordMeaning(word)
                if not word_information["success"]:
                    raise Exception(
                        f"Error while searching word meaning in dictionary {word_information['message']}"
                    )
                res.append(
                    {
                        "word": word,
                        "meaning": word_information["data"]["meaning"],
                    }
                )
            return jsonify(
                {
                    "success": True,
                    "message": "Morphological analysis successful.",
                    "data": res,
                }
            ), 200
        except Exception as e:
            abort(500, message=str(e))
            return jsonify({"success": False, "message": str(e), "data": []}), 500


@blp.route("/morpho_analysis/upload")
class UploadMorphoAnalysis(MethodView):
    def get(self):
        pass
