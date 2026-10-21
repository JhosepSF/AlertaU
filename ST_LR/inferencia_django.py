# Referencia de integracion Django; cargar solamente artefactos confiables.
from pathlib import Path
import json
import numpy as np
import pandas as pd
import joblib

class PredictorRiesgo:
    def __init__(self, package_dir):
        package_dir=Path(package_dir)
        config=json.loads((package_dir/'artefactos/config_inferencia.json').read_text(encoding='utf-8'))
        self.features=config['features']
        self.threshold=float(config['threshold'])
        self.preprocessor=joblib.load(package_dir/config['artifact_preprocessor'])
        self.model=joblib.load(package_dir/config['artifact_model'])
        self.classes=[int(c) for c in self.model.classes_]
        if set(self.classes)!={0,1}:raise ValueError('Clases inesperadas')

    def predict(self, factor_dict, elegible_confirmado=False):
        if elegible_confirmado is not True:
            raise ValueError('La elegibilidad debe verificarse antes de inferir')
        if set(factor_dict)!=set(self.features):
            raise ValueError('Las variables de entrada no coinciden con el contrato')
        X=pd.DataFrame([{f:factor_dict[f] for f in self.features}],columns=self.features)
        for f in self.features:
            X[f]=pd.to_numeric(X[f],errors='raise')
        if np.isinf(X.to_numpy(float)).any():
            raise ValueError('Infinitos no permitidos')
        Xt=self.preprocessor.transform(X)
        out=np.asarray(self.model.predict_proba(Xt),float)
        if out.shape!=(1,2) or not np.isfinite(out).all():
            raise ValueError('Probabilidad de salida invalida')
        prob=float(out[0,self.classes.index(1)])
        if not (0<=prob<=1):raise ValueError('Probabilidad fuera de rango')
        return {'probabilidad_recurrencia':prob,'riesgo_predicho':int(prob>=self.threshold),
                'umbral':self.threshold,'uso':'apoyo_academico_no_sancionador'}
