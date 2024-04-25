import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix, classification_report
import xgboost as xgb
import numpy as np
from datetime import datetime

from typing import Tuple, Union, List

class DelayModel:

    def __init__(
        self
    ):
        # self._model = None # Model should be saved in this attribute.
        self._model = xgb.XGBClassifier(random_state=1, learning_rate=0.01)

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        top_10_features = [
            "OPERA_Latin American Wings", 
            "MES_7",
            "MES_10",
            "OPERA_Grupo LATAM",
            "MES_12",
            "TIPOVUELO_I",
            "MES_4",
            "MES_11",
            "OPERA_Sky Airline",
            "OPERA_Copa Air"
        ]
        data['min_diff'] = data.apply(self.get_min_diff, axis = 1)
        threshold_in_minutes = 15
        data['delay'] = np.where(data['min_diff'] > threshold_in_minutes, 1, 0)
        # Crear variable delay con columnas debidas
        # training_data = shuffle(data[['OPERA', 'MES', 'TIPOVUELO', 'SIGLADES', 'DIANOM', 'delay']], random_state = 111)
        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix = 'OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix = 'TIPOVUELO'), 
            pd.get_dummies(data['MES'], prefix = 'MES')], 
            axis = 1
        )

        target = pd.DataFrame(data['delay'], columns=['delay'])
        if target_column is None:
            return features[top_10_features]
        return (features[top_10_features],target)

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        target_series = target['delay']
        n_y0 = len(target[target_series == 0])
        n_y1 = len(target[target_series == 1])
        scale = n_y0/n_y1
        
        # self._model = xgb.XGBClassifier(random_state=1, learning_rate=0.01, scale_pos_weight = scale)
        self._model.set_params(random_state=1, learning_rate=0.01, scale_pos_weight = scale)
        self._model = self._model.fit(features, target)

        return

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        prediction = self._model.predict(features)
        xgboost_y_preds = [1 if y_pred > 0.5 else 0 for y_pred in prediction]
        return xgboost_y_preds
    
    def get_min_diff(self, data):
        fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
        fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
        min_diff = ((fecha_o - fecha_i).total_seconds())/60
        return min_diff