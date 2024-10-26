from ollama import Client
from custom_types import DataObj

BASE_OLLAMA_URL = "http://localhost:11434"


class Translator:
    def __init__(self, **ollama_kwargs):
        self.client = Client(host=BASE_OLLAMA_URL)
        self.model = "llama3.1"
        self.system = "You are translator, that accepts Slovak language and return same content translated to English. Retrun just translation, do not include any other information to your answer"
        self.prompt = "Translate from Slovak to English this text: {text}"
        self.ollama_kwargs = ollama_kwargs
        self.translatables = ["title"]

    def _translate_to_eng(self, data_obj: DataObj) -> DataObj:
        translated = {}
        for key, value in data_obj.items():
            if key in self.translatables:
                response = self.client.generate(
                    model=self.model,
                    prompt=self.prompt.format_map({"text": value.replace("_", " ")}),
                    system=self.system,
                    stream=False,
                )
                translated[key] = response["response"]
            else:
                translated[key] = value
        return translated

    def transform_to_eng(self, data_objs: list[DataObj]) -> list[DataObj]:
        return [self._translate_to_eng(data_obj) for data_obj in data_objs]
