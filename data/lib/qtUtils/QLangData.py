#----------------------------------------------------------------------

    # Libraries
import json, os
from typing import Union
from PySide6.QtCore import QObject, Signal
#----------------------------------------------------------------------

    # Class
class QLangData(QObject):
    warning_received = Signal(str)


    class NoTranslation(str):
        def __new__(cls, value: str = None) -> None:
            instance = super().__new__(cls, 'No translation')
            return instance

        def __init__(self) -> None:
            super().__init__()

        def __getitem__(self, __key: str) -> 'QLangData.NoTranslation':
            return self


        def __getattr__(self, __key: str) -> 'QLangData.NoTranslation':
            return self


        def get(self, *args, **kwargs) -> 'QLangData.NoTranslation':
            return self


        def __call__(self, *args, **kwargs) -> 'QLangData.NoTranslation':
            return self


        def __str__(self) -> str:
            return super().__str__()


        def __repr__(self) -> str:
            return str(self)



    def __init__(self, data: dict = {}, cwd: str = './', current_file: str = '???', path_to_here: str = None) -> None:
        super().__init__()

        self._data = {}
        self._current_file = current_file
        self._path_to_here = path_to_here

        for key, value in data.items():
            if isinstance(value, dict):
                self._data[key] = QLangData(value, cwd, current_file, f'{path_to_here}.{key}' if path_to_here is not None else key)
                self._data[key].warning_received.connect(self.warning_received.emit)
                continue

            if isinstance(value, str):
                if value.startswith('#ref:'):
                    file = value.replace('#ref:', '').replace(' ', '').replace('\\', '/')

                    if not os.path.exists(f'{cwd}{file}.json'): raise Exception(f'Cannot find {cwd}{file}.json')
                    with open(f'{cwd}{file}.json', 'r', encoding = 'utf-8') as infile:
                        try:
                            self._data[key] = QLangData(json.load(infile), cwd, f'{cwd}{file}.json', f'{path_to_here}.{key}' if path_to_here is not None else key)
                            self._data[key].warning_received.connect(self.warning_received.emit)

                        except Exception as e:
                            raise Exception(f'Error in {cwd}{file}.json:\n{e}')

                    continue

            self._data[key] = value


    def get(self, path: str, default: Union[str, 'QLangData', None] = None) -> Union[str, 'QLangData', list[Union[str, 'QLangData']]]:
        keys = path.split('.')
        data = self

        for key in keys:
            try: data = data._data[key]
            except KeyError as e:
                self.warning_received.emit(f'[{self._current_file}] Cannot find {e.args[0]} from\n' + (f'{self._path_to_here}.{path}' if self._path_to_here is not None else path))
                return QLangData.NoTranslation() if default is None else default

        if isinstance(data, QLangData.NoTranslation):
            if default is not None: return default
            self.warning_received.emit(f'Cannot find {path} in {self._current_file}')

        return data


    def __getattr__(self, key: str) -> Union[str, 'QLangData', list[Union[str, 'QLangData']]]:
        return self.get(key)


    def __getitem__(self, key: str) -> Union[str, 'QLangData', list[Union[str, 'QLangData']]]:
        return self.get(key)


    def __call__(self, *args, **kwargs) -> Union[str, 'QLangData', list[Union[str, 'QLangData']]]:
        return self
#----------------------------------------------------------------------
